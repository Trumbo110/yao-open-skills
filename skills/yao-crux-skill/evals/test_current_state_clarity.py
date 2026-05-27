#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from current_state_clarity import assess_current_state_clarity
from generate_report_bundle import build_report, render_markdown


def test_sparse_input_blocks_diagnosis_and_asks_three_or_fewer_questions() -> None:
    request = {
        "title": "我现在很卡",
        "situation": {
            "summary": "团队最近事情很多，大家都很忙，但关键结果没有推进，我也说不清到底哪里出了问题。"
        },
        "facts": [{"text": "大家都很忙。", "source_type": "assumed"}],
    }

    assessment = assess_current_state_clarity(request)

    assert assessment["diagnosis_allowed"] is False
    assert assessment["clarity_level"] == "insufficient"
    assert 1 <= len(assessment["questions"]) <= 3
    joined = "\n".join(assessment["questions"])
    assert "目标" in joined or "期限" in joined
    assert "事实" in joined or "已经发生" in joined


def test_rich_sample_allows_diagnosis_with_confirmable_snapshot() -> None:
    request = json.loads((ROOT / "input" / "github_examples" / "b2b_saas_sales_conversion_case.json").read_text(encoding="utf-8"))

    assessment = assess_current_state_clarity(request)

    assert assessment["diagnosis_allowed"] is True
    assert assessment["clarity_level"] in {"workable", "clear"}
    assert assessment["score"] >= 75
    assert assessment["snapshot_ready"] is True
    assert "目标" in assessment["snapshot"]
    assert len(assessment["questions"]) <= 1


def test_generated_report_exposes_current_state_clarity_gate() -> None:
    request = json.loads((ROOT / "input" / "github_examples" / "b2b_saas_sales_conversion_case.json").read_text(encoding="utf-8"))

    report = build_report(request)

    assert report["current_state_clarity"]["diagnosis_allowed"] is True
    assert "现状清晰度" in report["current_state_clarity"]["snapshot"]
    assert report["summary"]["current_state_score"] >= 75


def test_markdown_uses_user_facing_clarity_dimension_labels() -> None:
    request = json.loads((ROOT / "input" / "github_examples" / "b2b_saas_sales_conversion_case.json").read_text(encoding="utf-8"))

    markdown = render_markdown(build_report(request))

    assert "目标与成功标准" in markdown
    assert "| goal |" not in markdown


if __name__ == "__main__":
    test_sparse_input_blocks_diagnosis_and_asks_three_or_fewer_questions()
    test_rich_sample_allows_diagnosis_with_confirmable_snapshot()
    test_generated_report_exposes_current_state_clarity_gate()
    test_markdown_uses_user_facing_clarity_dimension_labels()
    print("PASS: current state clarity tests")
