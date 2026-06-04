#!/usr/bin/env python3
"""Validate exported domain expert report artifacts."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path


LOCAL_PATH_RE = re.compile(r"(/Users/|file://|[A-Za-z]:\\\\)")
PLACEHOLDER_RE = re.compile(r"\{[\u4e00-\u9fffA-Za-z0-9_\-\s]{2,60}\}|__[^_\n]+__")
H1_RE = re.compile(r"^#\s+", re.M)
H2_RE = re.compile(r"^##\s+(.+)$", re.M)
CJK_RE = re.compile(r"[\u4e00-\u9fff]")

EXPECTED_SECTION_KEYWORDS = [
    "导读摘要",
    "默认假设",
    "一页专家速览",
    "边界",
    "分类",
    "价值链",
    "八维诊断",
    "生命周期",
    "竞争",
    "关键词",
    "专家学习教程",
    "费曼",
    "不确定性",
    "参考资料",
]
OPENING_SUMMARY_LABEL = "导读摘要"


@dataclass
class Check:
    status: str
    message: str


class Validator:
    def __init__(self, output_dir: Path, basename: str, formats: list[str], strict: bool) -> None:
        self.output_dir = output_dir
        self.basename = basename
        self.formats = formats
        self.strict = strict
        self.checks: list[Check] = []

    def add(self, status: str, message: str) -> None:
        self.checks.append(Check(status, message))

    def pass_(self, message: str) -> None:
        self.add("PASS", message)

    def warn(self, message: str) -> None:
        self.add("WARN", message)

    def fail(self, message: str) -> None:
        self.add("FAIL", message)

    def run(self) -> int:
        if not self.output_dir.exists():
            self.fail(f"Output directory not found: {self.output_dir}")
            return self.finish()

        self.validate_files()
        if "md" in self.formats:
            self.validate_markdown(self.output_dir / f"{self.basename}.md")
        if "html" in self.formats:
            self.validate_html(self.output_dir / f"{self.basename}.html")
        if "docx" in self.formats:
            self.validate_docx(self.output_dir / f"{self.basename}.docx")
        if "pdf" in self.formats:
            self.validate_pdf(self.output_dir / f"{self.basename}.pdf")
        self.validate_public_path_hygiene()
        return self.finish()

    def validate_files(self) -> None:
        for fmt in self.formats:
            path = self.output_dir / f"{self.basename}.{fmt}"
            if path.exists() and path.stat().st_size > 0:
                self.pass_(f"{fmt.upper()} export exists")
            elif path.exists():
                self.fail(f"{fmt.upper()} export is empty: {path}")
            else:
                self.fail(f"{fmt.upper()} export missing: {path}")

    def validate_markdown(self, path: Path) -> None:
        if not path.exists():
            return
        text = path.read_text(encoding="utf-8", errors="replace")
        h1_count = len(H1_RE.findall(text))
        if h1_count == 1:
            self.pass_("Markdown has exactly one H1")
        else:
            self.warn(f"Markdown should have exactly one H1; found {h1_count}")

        sections = "\n".join(H2_RE.findall(text))
        missing = [keyword for keyword in EXPECTED_SECTION_KEYWORDS if keyword not in sections]
        if missing:
            self.warn("Markdown may be missing expert-report sections: " + ", ".join(missing))
        else:
            self.pass_("Markdown includes expected expert-report sections")

        wide_tables = detect_wide_markdown_tables(text)
        if wide_tables:
            self.warn(f"Markdown has {wide_tables} table row(s) with 6 or more columns; check Word/PDF overflow")
        else:
            self.pass_("Markdown tables stay within the preferred column count")

        if "fact" in text or "inference" in text or "hypothesis" in text or "unknown" in text:
            self.pass_("Markdown includes evidence/judgment labels")
        else:
            self.warn("Markdown should label important judgments as fact, inference, hypothesis, or unknown")

        self.validate_markdown_prose_flow(text)
        self.validate_text_hygiene(text, "Markdown")

    def validate_markdown_prose_flow(self, text: str) -> None:
        summary_index = text.find(f"## {OPENING_SUMMARY_LABEL}")
        first_formal_index = text.find("## 0.")
        if summary_index == -1:
            self.fail("Markdown missing required 导读摘要 section")
        elif first_formal_index != -1 and summary_index > first_formal_index:
            self.fail("Markdown 导读摘要 should appear before the formal report sections")
        else:
            self.pass_("Markdown includes a reader-facing opening summary before formal sections")

        direct_table_sections: list[str] = []
        matches = list(re.finditer(r"^##\s+(.+)$", text, flags=re.M))
        for index, match in enumerate(matches):
            title = match.group(1).strip()
            if title.startswith("15. 参考资料"):
                continue
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            section = text[start:end]
            lines = [line.strip() for line in section.splitlines() if line.strip()]
            first_content = next((line for line in lines if not line.startswith("###")), "")
            if first_content.startswith("|"):
                direct_table_sections.append(title)

        if direct_table_sections:
            self.warn("Sections should open with prose before tables: " + ", ".join(direct_table_sections[:8]))
        else:
            self.pass_("Major sections open with prose before dense tables")

    def validate_html(self, path: Path) -> None:
        if not path.exists():
            return
        text = path.read_text(encoding="utf-8", errors="replace")
        if OPENING_SUMMARY_LABEL in text:
            self.pass_("HTML includes the reader-facing opening summary")
        else:
            self.fail("HTML missing required 导读摘要 section")

        if 'class="side-nav"' in text or "class='side-nav'" in text:
            self.pass_("HTML contains left fixed navigation element")
        else:
            self.fail("HTML missing .side-nav left navigation")

        if "position: fixed" in text and "table-layout: fixed" in text and "overflow-wrap: anywhere" in text:
            self.pass_("HTML/CSS includes fixed side navigation and overflow-safe table rules")
        else:
            self.warn("HTML/CSS may be missing side-nav/table overflow safeguards")

        nav_links = len(re.findall(r'<a href="#section-\d{2}"', text))
        heading_ids = len(re.findall(r'id="section-\d{2}"', text))
        if nav_links and heading_ids:
            self.pass_(f"HTML has {nav_links} nav links and {heading_ids} section anchors")
        else:
            self.fail("HTML missing generated section nav links or anchors")

        self.validate_nav_labels(text)

        if "<table" in text and "</table>" in text:
            self.pass_("HTML contains rendered tables")
        else:
            self.warn("HTML contains no tables; confirm this is intentional for the report")

        self.validate_html_table_widths(text)
        self.validate_text_hygiene(text, "HTML")

    def validate_nav_labels(self, text: str) -> None:
        match = re.search(r'<ol class="nav-links">(.*?)</ol>', text, flags=re.S)
        if not match:
            self.warn("HTML nav-links block not found; cannot inspect menu label length")
            return

        if not re.search(r"<li>\s*<a\b", match.group(1), flags=re.S):
            self.warn("HTML navigation should use ordered list items")
        elif not re.search(r'class="nav-index">0?1</span>', match.group(1)):
            self.warn("HTML navigation should include visible ordered indices")
        else:
            self.pass_("HTML navigation uses ordered numbered list items")

        labels = re.findall(r'<span class="nav-label">(.*?)</span>', match.group(1), flags=re.S)
        labels = [re.sub(r"<[^>]+>", "", label).strip() for label in labels]
        cjk_labels = [label for label in labels if CJK_RE.search(label)]
        if not cjk_labels:
            self.pass_("HTML navigation labels are non-Chinese or absent; four-character Chinese check skipped")
            return

        long_or_short = [label for label in cjk_labels if len(CJK_RE.findall(label)) != 4]
        if long_or_short:
            self.warn(
                "Chinese HTML navigation labels should be four characters: "
                + ", ".join(long_or_short[:8])
            )
        else:
            self.pass_("Chinese HTML navigation labels use four-character short text")

    def validate_html_table_widths(self, text: str) -> None:
        if "<colgroup>" in text and "col-number" in text and "table-fit" in text:
            self.pass_("HTML tables include generated compact column sizing")
        else:
            self.warn("HTML tables should include generated compact column sizing")

        feynman = re.search(
            r"<h2[^>]*>\s*12\.\s*费曼问题、参考答案与评分\s*</h2>(.*?)(?:<h2\b|</main>)",
            text,
            flags=re.S,
        )
        if not feynman:
            self.warn("Could not locate Feynman table section for compact-column validation")
            return

        table = re.search(r"<table[^>]*>(.*?)</table>", feynman.group(1), flags=re.S)
        if not table:
            self.warn("Could not locate Feynman scoring table")
            return

        col_widths = [
            float(width)
            for width in re.findall(r'<col\b[^>]*style="width:\s*([0-9.]+)%', table.group(1))
        ]
        if col_widths and col_widths[0] <= 10:
            self.pass_("Feynman question-number column is compact")
        else:
            self.warn("Feynman question-number column should be 10% width or narrower")

        first_cell = re.search(r"<t[hd][^>]*>题号</t[hd]>", table.group(1))
        if first_cell and "col-center" in first_cell.group(0):
            self.pass_("Feynman question-number column is centered")
        else:
            self.warn("Feynman question-number column should be centered")

    def validate_docx(self, path: Path) -> None:
        if not path.exists():
            return
        try:
            with zipfile.ZipFile(path) as archive:
                names = set(archive.namelist())
                if "word/document.xml" in names:
                    self.pass_("DOCX package contains word/document.xml")
                    document = archive.read("word/document.xml").decode("utf-8", errors="replace")
                    document_text = re.sub(r"<[^>]+>", "", document)
                    if OPENING_SUMMARY_LABEL in document_text:
                        self.pass_("DOCX includes the reader-facing opening summary")
                    else:
                        self.fail("DOCX missing required 导读摘要 section")
                    table_count = document.count("<w:tbl>")
                    if table_count:
                        self.pass_(f"DOCX contains {table_count} table(s)")
                    else:
                        self.warn("DOCX contains no tables; confirm this is intentional")
                    if LOCAL_PATH_RE.search(document):
                        self.fail("DOCX document.xml exposes a local filesystem path")
                    if "<w:tblW" in document:
                        self.pass_("DOCX tables have table width declarations")
                    else:
                        self.warn("DOCX tables may rely on automatic widths; inspect dense tables")
                else:
                    self.fail("DOCX missing word/document.xml")

                local_path_files = []
                for name in names:
                    if not name.endswith((".xml", ".rels")):
                        continue
                    content = archive.read(name).decode("utf-8", errors="replace")
                    if LOCAL_PATH_RE.search(content):
                        local_path_files.append(name)
                if local_path_files:
                    self.fail("DOCX exposes local paths in: " + ", ".join(sorted(local_path_files)[:8]))
                else:
                    self.pass_("DOCX package contains no obvious local filesystem paths")
        except zipfile.BadZipFile:
            self.fail("DOCX is not a valid zip package")

    def validate_pdf(self, path: Path) -> None:
        if not path.exists():
            return
        size = path.stat().st_size
        if size >= 10_000:
            self.pass_(f"PDF size looks non-empty ({size} bytes)")
        elif size > 0:
            self.warn(f"PDF is very small ({size} bytes); inspect for print/export failure")
        else:
            self.fail("PDF is empty")

        pdftotext = shutil.which("pdftotext")
        if not pdftotext:
            self.warn("pdftotext unavailable; cannot inspect PDF text for print chrome or local paths")
            return

        try:
            text = subprocess.check_output([pdftotext, str(path), "-"], text=True, errors="replace")
        except subprocess.CalledProcessError:
            self.warn("pdftotext failed; cannot inspect PDF text for print chrome or local paths")
            return

        if LOCAL_PATH_RE.search(text):
            self.fail("PDF text exposes a local filesystem path, likely from browser print footer")
        else:
            self.pass_("PDF text contains no obvious local filesystem paths")

        if OPENING_SUMMARY_LABEL in text:
            self.pass_("PDF includes the reader-facing opening summary")
        else:
            self.fail("PDF missing required 导读摘要 section")

        if re.search(r"file://|storage-expert-sample\\.html|\\.html\\s+\\d+\\s*/\\s*\\d+", text):
            self.warn("PDF may contain browser print header/footer text")
        else:
            self.pass_("PDF text does not show obvious browser print header/footer")

        if re.search(r"0?1\s+默认边界\s+0?2\s+专家速览", text):
            self.fail("PDF appears to contain the HTML navigation menu")
        else:
            self.pass_("PDF text does not contain the left navigation menu")

    def validate_public_path_hygiene(self) -> None:
        for fmt in ["md", "html"]:
            path = self.output_dir / f"{self.basename}.{fmt}"
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if LOCAL_PATH_RE.search(text):
                self.fail(f"{fmt.upper()} exposes a local filesystem path")
            else:
                self.pass_(f"{fmt.upper()} contains no obvious local filesystem paths")

    def validate_text_hygiene(self, text: str, label: str) -> None:
        unresolved = [match.group(0) for match in PLACEHOLDER_RE.finditer(text)]
        unresolved = [item for item in unresolved if not item.startswith("{#")]
        if unresolved:
            sample = ", ".join(sorted(set(unresolved))[:8])
            self.warn(f"{label} may contain unresolved placeholders: {sample}")
        if LOCAL_PATH_RE.search(text):
            self.fail(f"{label} exposes a local filesystem path")

    def finish(self) -> int:
        failures = [check for check in self.checks if check.status == "FAIL"]
        warnings = [check for check in self.checks if check.status == "WARN"]
        for check in self.checks:
            print(f"[{check.status}] {check.message}")
        print(f"\nSummary: {len(failures)} failures, {len(warnings)} warnings, {len(self.checks)} checks")
        if failures:
            return 1
        if warnings and self.strict:
            return 2
        return 0


def detect_wide_markdown_tables(text: str) -> int:
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        columns = [cell for cell in stripped.strip("|").split("|")]
        if len(columns) >= 6:
            count += 1
    return count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate domain expert report exports.")
    parser.add_argument("output_dir", help="Directory containing exported artifacts.")
    parser.add_argument("--basename", required=True, help="Artifact basename.")
    parser.add_argument(
        "--formats",
        nargs="+",
        choices=["md", "docx", "html", "pdf"],
        default=["md", "docx", "pdf", "html"],
        help="Formats expected in the output directory.",
    )
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when warnings remain.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    validator = Validator(Path(args.output_dir).resolve(), args.basename, args.formats, args.strict)
    raise SystemExit(validator.run())


if __name__ == "__main__":
    sys.exit(main())
