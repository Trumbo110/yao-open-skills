#!/usr/bin/env python3
"""Export a domain expert Markdown report to Markdown, DOCX, HTML, and PDF."""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET


HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)(?:\s+\{#[-A-Za-z0-9_:.]+\})?\s*$", re.M)
ATTR_RE = re.compile(r"\s+\{#([-A-Za-z0-9_:.]+)\}\s*$")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
LEADING_NUMBER_RE = re.compile(r"^\s*\d+\s*[.、．]\s*")
SIDE_NAV_RE = re.compile(r"\s*<nav class=\"side-nav\"[\s\S]*?</nav>\s*", re.M)
TABLE_RE = re.compile(r"<table(?P<attrs>[^>]*)>(?P<inner>[\s\S]*?)</table>", re.M)
COLGROUP_RE = re.compile(r"\s*<colgroup>[\s\S]*?</colgroup>\s*", re.M)
ROW_RE = re.compile(r"<tr(?P<attrs>[^>]*)>(?P<inner>[\s\S]*?)</tr>", re.M)
CELL_RE = re.compile(r"<(?P<tag>t[hd])(?P<attrs>[^>]*)>(?P<content>[\s\S]*?)</(?P=tag)>", re.M)
TAG_RE = re.compile(r"<[^>]+>")
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

ET.register_namespace("w", W_NS)

NAV_LABEL_RULES = [
    ("导读摘要", "导读摘要"),
    ("默认假设", "默认边界"),
    ("一页专家速览", "专家速览"),
    ("领域定义", "边界定义"),
    ("研究边界", "边界定义"),
    ("多口径分类", "分类地图"),
    ("分类地图", "分类地图"),
    ("价值链", "价值利润"),
    ("利润池", "价值利润"),
    ("八维诊断", "八维诊断"),
    ("当前状态", "八维诊断"),
    ("生命周期", "生命周期"),
    ("竞争结构", "竞争壁垒"),
    ("壁垒", "竞争壁垒"),
    ("政策", "政策信号"),
    ("资本信号", "政策信号"),
    ("代表公司", "代表锚点"),
    ("代表人物", "代表锚点"),
    ("实践场景", "代表锚点"),
    ("关键词库", "关键词库"),
    ("概念关系", "关键词库"),
    ("专家学习教程", "学习教程"),
    ("学习教程", "学习教程"),
    ("费曼", "费曼自测"),
    ("机会", "机会风险"),
    ("风险", "机会风险"),
    ("不确定性", "不确定性"),
    ("参考资料", "参考资料"),
]


@dataclass
class Heading:
    level: int
    text: str
    anchor: str


@dataclass
class ColumnSpec:
    percent: float
    classes: tuple[str, ...]
    center: bool


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"Missing required tool: {name}")
    return path


def find_pdf_browser() -> str:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    for candidate in candidates:
        if os.access(candidate, os.X_OK):
            return candidate

    for name in ["google-chrome", "chromium", "chromium-browser", "msedge", "brave"]:
        path = shutil.which(name)
        if path:
            return path

    raise SystemExit("Missing PDF browser: install Google Chrome, Microsoft Edge, Brave, or Chromium.")


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def w_tag(name: str) -> str:
    return f"{{{W_NS}}}{name}"


def ensure_child(parent: ET.Element, name: str, index: int | None = None) -> ET.Element:
    child = parent.find(w_tag(name))
    if child is not None:
        return child
    child = ET.Element(w_tag(name))
    if index is None:
        parent.append(child)
    else:
        parent.insert(index, child)
    return child


def clean_heading_text(text: str) -> str:
    text = ATTR_RE.sub("", text).strip()
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", lambda m: m.group(0).split("]")[0].lstrip("["), text)
    return re.sub(r"[*_`~]", "", text).strip()


def nav_label(text: str) -> str:
    cleaned = LEADING_NUMBER_RE.sub("", text).strip()
    for keyword, label in NAV_LABEL_RULES:
        if keyword in cleaned:
            return label

    if CJK_RE.search(cleaned):
        cjk_chars = CJK_RE.findall(cleaned)
        if len(cjk_chars) >= 4:
            return "".join(cjk_chars[:4])
        return "".join(cjk_chars)

    return cleaned[:18]


def anchor_for(index: int, text: str) -> str:
    # Stable ASCII anchors avoid inconsistent slugging for Chinese headings.
    return f"section-{index:02d}"


def add_heading_anchors(markdown: str) -> tuple[str, list[Heading]]:
    headings: list[Heading] = []
    index = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal index
        marks = match.group(1)
        raw_text = match.group(2).strip()
        level = len(marks)
        existing = ATTR_RE.search(match.group(0))
        text = clean_heading_text(raw_text)
        if level == 1:
            anchor = "top"
            headings.append(Heading(level=level, text=text, anchor=anchor))
            return f"{marks} {text} {{#{anchor}}}"
        if existing:
            anchor = existing.group(1)
            headings.append(Heading(level=level, text=text, anchor=anchor))
            return match.group(0)
        index += 1
        anchor = anchor_for(index, text)
        headings.append(Heading(level=level, text=text, anchor=anchor))
        return f"{marks} {raw_text} {{#{anchor}}}"

    return HEADING_RE.sub(replace, markdown), headings


def nav_html(headings: list[Heading]) -> str:
    nav_items = [heading for heading in headings if heading.level == 2]
    if not nav_items:
        nav_items = [heading for heading in headings if heading.level <= 3 and heading.anchor != "top"]
    return "\n".join(
        (
            f'      <li><a href="#{html.escape(item.anchor)}" title="{html.escape(item.text)}">'
            f'<span class="nav-index">{index:02d}</span>'
            f'<span class="nav-label">{html.escape(nav_label(item.text))}</span>'
            f"</a></li>"
        )
        for index, item in enumerate(nav_items, start=1)
    )


def pandoc_body(pandoc: str, source: Path) -> str:
    cmd = [
        pandoc,
        str(source),
        "--from",
        "markdown+header_attributes+pipe_tables+fenced_code_blocks+footnotes",
        "--to",
        "html",
    ]
    return subprocess.check_output(cmd, text=True)


def html_cell_text(content: str) -> str:
    text = re.sub(r"<br\s*/?>", " ", content, flags=re.I)
    text = TAG_RE.sub("", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def visual_len(text: str) -> int:
    return sum(2 if CJK_RE.match(char) else 1 for char in text)


def is_number_like(text: str) -> bool:
    cleaned = text.strip()
    if not cleaned:
        return False
    return bool(
        re.match(
            r"^(?:\d+(?:\.\d+)?|[A-Za-z]|\d+\s*[-–—~至]\s*\d+|\d+(?:\.\d+)?%|[高中过低]+)$",
            cleaned,
        )
    )


def infer_column_specs(headers: list[str], body_columns: list[list[str]]) -> list[ColumnSpec]:
    specs: list[tuple[float, tuple[str, ...], bool]] = []
    short_headers = {
        "类型",
        "状态",
        "阶段",
        "层级",
        "模块",
        "角色",
        "来源",
        "证据",
        "口径",
        "年份",
        "时间",
        "周期",
        "置信度",
        "判断类型",
        "所属模块",
        "证据层级",
    }
    index_headers = {"题号", "序号", "编号", "排名", "序列", "ID", "No", "No."}
    score_headers = {"评分", "评分标准", "分值", "权重", "占比", "比例"}

    for index, header in enumerate(headers):
        body = [cell for cell in body_columns[index] if cell] if index < len(body_columns) else []
        lengths = [visual_len(cell) for cell in body]
        avg_len = sum(lengths) / len(lengths) if lengths else visual_len(header)
        max_len = max(lengths) if lengths else visual_len(header)
        number_ratio = sum(1 for cell in body if is_number_like(cell)) / len(body) if body else 0
        normalized_header = re.sub(r"\s+", "", header)

        if normalized_header in index_headers or (number_ratio >= 0.9 and visual_len(header) <= 6):
            specs.append((5.5, ("col-compact", "col-number"), True))
        elif normalized_header in score_headers and avg_len <= 12:
            specs.append((9.5, ("col-compact", "col-number"), True))
        elif number_ratio >= 0.8 and avg_len <= 12:
            specs.append((7.0, ("col-compact", "col-number"), True))
        elif normalized_header in short_headers and avg_len <= 18:
            specs.append((10.5, ("col-compact", "col-short"), True))
        elif avg_len <= 12 and max_len <= 18 and len(headers) >= 3:
            center = number_ratio >= 0.5
            classes = ("col-compact", "col-number") if center else ("col-compact", "col-short")
            specs.append((10.5, classes, center))
        elif avg_len <= 24 and max_len <= 42:
            specs.append((18.0, ("col-medium",), False))
        else:
            weight = max(24.0, min(58.0, avg_len))
            specs.append((weight, ("col-long",), False))

    total = sum(weight for weight, _, _ in specs) or 1
    normalized: list[ColumnSpec] = []
    for weight, classes, center in specs:
        percent = round(weight / total * 100, 2)
        normalized.append(ColumnSpec(percent=percent, classes=classes, center=center))

    if normalized:
        drift = round(100 - sum(spec.percent for spec in normalized), 2)
        normalized[-1].percent = round(normalized[-1].percent + drift, 2)
    return normalized


def widths_from_specs(specs: list[ColumnSpec]) -> list[int]:
    widths = [max(1, int(round(spec.percent * 100))) for spec in specs]
    if widths:
        widths[-1] += 10000 - sum(widths)
    return widths


def add_classes(attrs: str, classes: tuple[str, ...]) -> str:
    if not classes:
        return attrs

    class_value = " ".join(classes)
    match = re.search(r'\sclass="([^"]*)"', attrs)
    if match:
        existing = match.group(1).split()
        merged = existing + [item for item in classes if item not in existing]
        return attrs[: match.start(1)] + " ".join(merged) + attrs[match.end(1) :]

    return f'{attrs} class="{class_value}"'


def optimize_html_table(match: re.Match[str]) -> str:
    attrs = match.group("attrs")
    inner = COLGROUP_RE.sub("\n", match.group("inner"))
    if "colspan" in inner or "rowspan" in inner:
        return f"<table{add_classes(attrs, ('report-table',))}>{inner}</table>"

    rows = list(ROW_RE.finditer(inner))
    if not rows:
        return f"<table{add_classes(attrs, ('report-table',))}>{inner}</table>"

    row_cells: list[list[re.Match[str]]] = []
    for row in rows:
        cells = list(CELL_RE.finditer(row.group("inner")))
        if cells:
            row_cells.append(cells)
    if not row_cells:
        return f"<table{add_classes(attrs, ('report-table',))}>{inner}</table>"

    column_count = max(len(cells) for cells in row_cells)
    headers = ["" for _ in range(column_count)]
    first_row = row_cells[0]
    for index, cell in enumerate(first_row):
        headers[index] = html_cell_text(cell.group("content"))

    body_columns: list[list[str]] = [[] for _ in range(column_count)]
    for cells in row_cells[1:]:
        for index, cell in enumerate(cells[:column_count]):
            body_columns[index].append(html_cell_text(cell.group("content")))

    specs = infer_column_specs(headers, body_columns)
    colgroup = "\n<colgroup>\n" + "\n".join(
        f'  <col class="{" ".join(spec.classes)}" style="width: {spec.percent:.2f}%;">'
        for spec in specs
    ) + "\n</colgroup>"

    row_index = -1

    def rewrite_row(row_match: re.Match[str]) -> str:
        nonlocal row_index
        row_index += 1
        cell_index = -1

        def rewrite_cell(cell_match: re.Match[str]) -> str:
            nonlocal cell_index
            cell_index += 1
            spec = specs[cell_index] if cell_index < len(specs) else ColumnSpec(0, tuple(), False)
            tag = cell_match.group("tag")
            cell_attrs = add_classes(cell_match.group("attrs"), spec.classes)
            if spec.center:
                cell_attrs = add_classes(cell_attrs, ("col-center",))
            return f'<{tag}{cell_attrs}>{cell_match.group("content")}</{tag}>'

        rewritten_inner = CELL_RE.sub(rewrite_cell, row_match.group("inner"))
        return f'<tr{row_match.group("attrs")}>{rewritten_inner}</tr>'

    optimized_inner = ROW_RE.sub(rewrite_row, inner)
    return f"<table{add_classes(attrs, ('report-table', 'table-fit'))}>{colgroup}{optimized_inner}</table>"


def optimize_html_tables(body: str) -> str:
    return TABLE_RE.sub(optimize_html_table, body)


def render_html(shell: Path, css: Path, title: str, body: str, nav: str) -> str:
    template = shell.read_text(encoding="utf-8")
    css_text = css.read_text(encoding="utf-8")
    replacements = {
        "__TITLE__": html.escape(title),
        "__CSS__": css_text,
        "__NAV_HTML__": nav,
        "__BODY_HTML__": optimize_html_tables(body),
        "__GENERATED_AT__": datetime.now().isoformat(timespec="seconds"),
    }
    output = template
    for key, value in replacements.items():
        output = output.replace(key, value)
    return output


def export_docx(pandoc: str, source: Path, target: Path, title: str, reference_doc: Path | None) -> None:
    cmd = [
        pandoc,
        str(source),
        "--from",
        "markdown+header_attributes+pipe_tables+fenced_code_blocks+footnotes",
        "-o",
        str(target),
        "-M",
        f"title={title}",
    ]
    if reference_doc:
        cmd.append(f"--reference-doc={reference_doc}")
    run(cmd)
    polish_docx(target)


def preferred_widths(column_count: int) -> list[int]:
    widths_by_count = {
        1: [10000],
        2: [2200, 7800],
        3: [2000, 3300, 4700],
        4: [1600, 2700, 3300, 2400],
        5: [1350, 2150, 2600, 2600, 1300],
        6: [1150, 1250, 1800, 2300, 2300, 1200],
    }
    if column_count in widths_by_count:
        return widths_by_count[column_count]
    base = 10000 // column_count
    widths = [base] * column_count
    widths[-1] += 10000 - sum(widths)
    return widths


def xml_cell_text(cell: ET.Element) -> str:
    return re.sub(r"\s+", " ", "".join(cell.itertext())).strip()


def polish_docx(path: Path) -> None:
    """Post-process Pandoc DOCX tables for report-style layout."""
    with zipfile.ZipFile(path, "r") as zin:
        entries = {item.filename: zin.read(item.filename) for item in zin.infolist()}

    document_name = "word/document.xml"
    if document_name not in entries:
        return

    root = ET.fromstring(entries[document_name])
    polish_docx_sections(root)
    for table in root.findall(f".//{w_tag('tbl')}"):
        polish_docx_table(table)

    entries[document_name] = ET.tostring(root, encoding="utf-8", xml_declaration=True)

    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for name, data in entries.items():
            zout.writestr(name, data)


def polish_docx_sections(root: ET.Element) -> None:
    for sect_pr in root.findall(f".//{w_tag('sectPr')}"):
        pg_sz = ensure_child(sect_pr, "pgSz")
        pg_sz.set(w_tag("w"), "11906")
        pg_sz.set(w_tag("h"), "16838")

        pg_mar = ensure_child(sect_pr, "pgMar")
        pg_mar.set(w_tag("top"), "900")
        pg_mar.set(w_tag("right"), "850")
        pg_mar.set(w_tag("bottom"), "900")
        pg_mar.set(w_tag("left"), "850")
        pg_mar.set(w_tag("header"), "450")
        pg_mar.set(w_tag("footer"), "450")
        pg_mar.set(w_tag("gutter"), "0")


def polish_docx_table(table: ET.Element) -> None:
    tbl_pr = table.find(w_tag("tblPr"))
    if tbl_pr is None:
        tbl_pr = ET.Element(w_tag("tblPr"))
        table.insert(0, tbl_pr)

    tbl_w = ensure_child(tbl_pr, "tblW")
    tbl_w.set(w_tag("type"), "pct")
    tbl_w.set(w_tag("w"), "5000")

    tbl_layout = ensure_child(tbl_pr, "tblLayout")
    tbl_layout.set(w_tag("type"), "fixed")

    tbl_cell_mar = ensure_child(tbl_pr, "tblCellMar")
    for side, width in [("top", "70"), ("bottom", "70"), ("left", "90"), ("right", "90")]:
        node = ensure_child(tbl_cell_mar, side)
        node.set(w_tag("type"), "dxa")
        node.set(w_tag("w"), width)

    rows = table.findall(w_tag("tr"))
    first_row = rows[0] if rows else None
    cells = first_row.findall(w_tag("tc")) if first_row is not None else []
    column_count = max(len(cells), 1)
    headers = [xml_cell_text(cell) for cell in cells]
    body_columns: list[list[str]] = [[] for _ in range(column_count)]
    for row in rows[1:]:
        for idx, cell in enumerate(row.findall(w_tag("tc"))[:column_count]):
            body_columns[idx].append(xml_cell_text(cell))

    column_specs = infer_column_specs(headers, body_columns) if headers else []
    widths = widths_from_specs(column_specs) if column_specs else preferred_widths(column_count)
    center_columns = {idx for idx, spec in enumerate(column_specs) if spec.center}

    tbl_grid = table.find(w_tag("tblGrid"))
    if tbl_grid is None:
        tbl_grid = ET.Element(w_tag("tblGrid"))
        insert_at = 1 if table.find(w_tag("tblPr")) is not None else 0
        table.insert(insert_at, tbl_grid)
    for child in list(tbl_grid):
        tbl_grid.remove(child)
    for width in widths:
        grid_col = ET.SubElement(tbl_grid, w_tag("gridCol"))
        grid_col.set(w_tag("w"), str(width))

    for row in table.findall(w_tag("tr")):
        row_pr = ensure_child(row, "trPr", 0)
        cant_split = ensure_child(row_pr, "cantSplit")
        cant_split.set(w_tag("val"), "0")
        row_cells = row.findall(w_tag("tc"))
        for idx, cell in enumerate(row_cells):
            cell_pr = ensure_child(cell, "tcPr", 0)
            width = widths[min(idx, len(widths) - 1)]
            tc_w = ensure_child(cell_pr, "tcW")
            tc_w.set(w_tag("type"), "dxa")
            tc_w.set(w_tag("w"), str(width))
            v_align = ensure_child(cell_pr, "vAlign")
            v_align.set(w_tag("val"), "top")
            for para in cell.findall(w_tag("p")):
                para_pr = ensure_child(para, "pPr", 0)
                spacing = ensure_child(para_pr, "spacing")
                spacing.set(w_tag("before"), "0")
                spacing.set(w_tag("after"), "0")
                spacing.set(w_tag("line"), "240")
                spacing.set(w_tag("lineRule"), "auto")
                if idx in center_columns:
                    justify = ensure_child(para_pr, "jc")
                    justify.set(w_tag("val"), "center")


def export_pdf(browser: str, html_file: Path, pdf_file: Path) -> None:
    printable_html = html_file.read_text(encoding="utf-8")
    printable_html = SIDE_NAV_RE.sub("\n", printable_html, count=1)

    with tempfile.TemporaryDirectory() as tmp:
        printable_file = Path(tmp) / html_file.name
        printable_file.write_text(printable_html, encoding="utf-8")
        run_pdf_browser(browser, printable_file, pdf_file)


def run_pdf_browser(browser: str, html_file: Path, pdf_file: Path) -> None:
    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=5000",
        f"--print-to-pdf={pdf_file}",
        html_file.resolve().as_uri(),
    ]
    run(cmd)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export a domain expert report from Markdown.")
    parser.add_argument("source", help="Canonical Markdown source file.")
    parser.add_argument("output_dir", help="Directory for exported artifacts.")
    parser.add_argument("--title", default=None, help="Report title. Defaults to the Markdown H1 or filename.")
    parser.add_argument("--basename", default=None, help="Output basename. Defaults to source stem.")
    parser.add_argument("--css", default=None, help="CSS override. Defaults to templates/expert-report.css.")
    parser.add_argument("--html-shell", default=None, help="HTML shell override. Defaults to templates/report-html-shell.html.")
    parser.add_argument("--reference-doc", default=None, help="Optional Pandoc reference DOCX.")
    parser.add_argument(
        "--formats",
        nargs="+",
        choices=["md", "docx", "html", "pdf"],
        default=["md", "docx", "pdf", "html"],
        help="Formats to generate.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = Path(args.source).resolve()
    if not source.exists():
        raise SystemExit(f"Source file not found: {source}")

    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    basename = args.basename or source.stem
    raw_markdown = source.read_text(encoding="utf-8")
    anchored_markdown, headings = add_heading_anchors(raw_markdown)
    first_h1 = next((heading.text for heading in headings if heading.level == 1), None)
    title = args.title or first_h1 or source.stem.replace("-", " ").replace("_", " ").title()

    css = Path(args.css).resolve() if args.css else skill_dir / "templates" / "expert-report.css"
    shell = Path(args.html_shell).resolve() if args.html_shell else skill_dir / "templates" / "report-html-shell.html"
    reference_doc = Path(args.reference_doc).resolve() if args.reference_doc else None

    pandoc = require_tool("pandoc") if any(fmt in args.formats for fmt in ["docx", "html", "pdf"]) else ""
    browser = find_pdf_browser() if "pdf" in args.formats else ""

    with tempfile.TemporaryDirectory() as tmp:
        anchored_source = Path(tmp) / f"{basename}.anchored.md"
        anchored_source.write_text(anchored_markdown, encoding="utf-8")

        if "md" in args.formats:
            (output_dir / f"{basename}.md").write_text(anchored_markdown, encoding="utf-8")

        html_target = output_dir / f"{basename}.html"
        if "html" in args.formats or "pdf" in args.formats:
            body = pandoc_body(pandoc, anchored_source)
            html_output = render_html(shell, css, title, body, nav_html(headings))
            html_target.write_text(html_output, encoding="utf-8")

        if "docx" in args.formats:
            export_docx(pandoc, anchored_source, output_dir / f"{basename}.docx", title, reference_doc)

        if "pdf" in args.formats:
            export_pdf(browser, html_target, output_dir / f"{basename}.pdf")

    print(f"Export complete: {output_dir}")
    for fmt in args.formats:
        print(f"- {output_dir / f'{basename}.{fmt}'}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(f"Command failed with exit code {exc.returncode}: {exc.cmd}", file=sys.stderr)
        raise SystemExit(exc.returncode)
