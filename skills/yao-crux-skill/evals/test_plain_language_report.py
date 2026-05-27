#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from generate_report_bundle import build_report, render_markdown


def sample_markdown() -> str:
    request = json.loads((ROOT / "input" / "github_examples" / "b2b_saas_sales_conversion_case.json").read_text(encoding="utf-8"))
    return render_markdown(build_report(request))


def test_report_uses_plain_language_main_sections() -> None:
    markdown = sample_markdown()

    for heading in [
        "## 先看结论",
        "## 先把现状说清楚",
        "## 现状够不够清楚",
        "## 主要矛盾判断过程",
        "## 主要矛盾（最关键的卡点）",
        "## 次要矛盾（先不主攻，但要盯住）",
        "## 接下来怎么做",
        "## 做完以后可能怎样",
        "## 什么时候回头看",
        "## 注意事项",
    ]:
        assert heading in markdown


def test_report_integrates_contradiction_terms_with_plain_explanations() -> None:
    markdown = sample_markdown()

    assert "主要矛盾" in markdown
    assert "次要矛盾" in markdown
    assert "最关键的卡点" in markdown
    assert "先不主攻" in markdown


def test_summary_table_uses_actionable_labels() -> None:
    markdown = sample_markdown()

    assert "| 最该先解决 | 为什么是它 | 把握 | 做完后大概到哪 | 第一步 |" in markdown
    assert "| 主要矛盾 | 主要方面 |" not in markdown


def test_report_shows_first_principles_logic() -> None:
    markdown = sample_markdown()

    assert "第一性原理" in markdown
    assert "上升一层" in markdown
    assert "看得见的问题" in markdown
    assert "看不见的根部变量" in markdown


if __name__ == "__main__":
    test_report_uses_plain_language_main_sections()
    test_report_integrates_contradiction_terms_with_plain_explanations()
    test_summary_table_uses_actionable_labels()
    test_report_shows_first_principles_logic()
    print("PASS: plain language report tests")
