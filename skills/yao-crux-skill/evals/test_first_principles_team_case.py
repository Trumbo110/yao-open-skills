#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from generate_report_bundle import build_report, render_markdown


def test_support_case_can_select_hidden_root_closure_as_principal_contradiction() -> None:
    request = json.loads((ROOT / "input" / "github_examples" / "customer_support_delivery_case.json").read_text(encoding="utf-8"))

    report = build_report(request)

    principal_name = report["principal"]["name"]
    assert "根因闭环" in principal_name or "真实解决" in principal_name
    assert report["principal"]["weighted_total"] >= 4.5


def test_support_case_report_explains_why_visible_response_pressure_is_secondary() -> None:
    request = json.loads((ROOT / "input" / "github_examples" / "customer_support_delivery_case.json").read_text(encoding="utf-8"))
    markdown = render_markdown(build_report(request))

    assert "看得见的问题" in markdown
    assert "工单量" in markdown
    assert "客服压力" in markdown
    assert "看不见的根部变量" in markdown
    assert "根因闭环" in markdown
    assert "如果只是增加客服" in markdown or "客服人手不是唯一解" in markdown


if __name__ == "__main__":
    test_support_case_can_select_hidden_root_closure_as_principal_contradiction()
    test_support_case_report_explains_why_visible_response_pressure_is_secondary()
    print("PASS: first principles support case tests")
