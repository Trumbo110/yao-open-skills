#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


QUESTION_BANK = {
    "goal": "你希望这个问题在什么期限内变成什么状态？怎样算解决？",
    "facts": "哪些是已经发生、别人也能确认的事实？哪些只是你的解释、担心或推测？",
    "resources": "你现在最稀缺的资源是什么：时间、人、钱、权限、注意力、信任、数据，还是其他？",
    "constraints": "有哪些不能突破的边界：法律、健康、安全、现金流、承诺、关系、声誉或伦理？",
    "stage": "这件事现在处在什么阶段：启动、验证、增长、修复、转型、恢复，还是别的阶段？",
    "stakeholders": "涉及哪些人或组织？他们各自最在意的结果和约束是什么？",
    "patterns": "类似问题出现过几次？通常在什么节点爆发？之前尝试过什么，结果如何？",
}


DIMENSION_LABELS = {
    "goal": "目标与成功标准",
    "facts": "事实与证据",
    "stage": "阶段判断",
    "resources": "稀缺资源",
    "constraints": "硬约束",
    "stakeholders": "相关方与利益结构",
    "patterns": "重复模式与已尝试动作",
}

LEVEL_LABELS = {
    "insufficient": "还不够清楚",
    "workable": "基本够用",
    "clear": "清楚",
}


def _text(value: Any) -> str:
    return str(value or "").strip()


def _items(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _situation(request: dict[str, Any]) -> dict[str, Any]:
    value = request.get("situation")
    return value if isinstance(value, dict) else {}


def _facts(request: dict[str, Any]) -> list[dict[str, Any]]:
    values = request.get("facts")
    if not isinstance(values, list):
        return []
    return [item for item in values if isinstance(item, dict) and _text(item.get("text"))]


def _has_previous_attempts_or_patterns(request: dict[str, Any]) -> bool:
    situation = _situation(request)
    keys = [
        "previous_attempts",
        "attempts",
        "patterns",
        "recurring_patterns",
        "bottleneck",
    ]
    if any(_items(request.get(key)) or _text(request.get(key)) for key in keys):
        return True
    if any(_items(situation.get(key)) or _text(situation.get(key)) for key in keys):
        return True
    review = request.get("review") if isinstance(request.get("review"), dict) else {}
    return bool(_items(review.get("evidence_to_collect")))


def _dimension_scores(request: dict[str, Any]) -> tuple[dict[str, float], dict[str, bool]]:
    situation = _situation(request)
    goal = _text(situation.get("goal"))
    deadline = _text(situation.get("deadline"))
    success_metric = _text(situation.get("success_metric"))
    stage = _text(situation.get("stage"))
    resources = _items(situation.get("resources"))
    constraints = _items(situation.get("constraints"))
    stakeholders = _items(situation.get("stakeholders"))
    facts = _facts(request)
    strong_facts = [fact for fact in facts if fact.get("source_type", "assumed") in {"observed", "estimated"}]
    has_patterns = _has_previous_attempts_or_patterns(request)

    scores: dict[str, float] = {}
    present: dict[str, bool] = {}

    if goal and (deadline or success_metric):
        scores["goal"] = 20
    elif goal:
        scores["goal"] = 14
    elif deadline or success_metric:
        scores["goal"] = 8
    else:
        scores["goal"] = 0
    present["goal"] = bool(goal and (deadline or success_metric))

    if len(strong_facts) >= 3:
        scores["facts"] = 20
    elif len(strong_facts) >= 2:
        scores["facts"] = 16
    elif len(strong_facts) == 1:
        scores["facts"] = 9
    elif facts:
        scores["facts"] = 4
    else:
        scores["facts"] = 0
    present["facts"] = len(strong_facts) >= 2

    scores["stage"] = 12 if stage else 0
    present["stage"] = bool(stage)
    scores["resources"] = 12 if resources else 0
    present["resources"] = bool(resources)
    scores["constraints"] = 12 if constraints else 0
    present["constraints"] = bool(constraints)
    scores["stakeholders"] = 8 if stakeholders else 0
    present["stakeholders"] = bool(stakeholders)
    scores["patterns"] = 8 if has_patterns else 0
    present["patterns"] = has_patterns
    return scores, present


def _clarity_level(score: float) -> str:
    if score < 55:
        return "insufficient"
    if score < 75:
        return "workable"
    return "clear"


def _missing_questions(present: dict[str, bool], level: str) -> list[str]:
    priority = ["goal", "facts", "resources", "constraints", "stage", "stakeholders", "patterns"]
    limit = 3 if level == "insufficient" else 5
    questions = [QUESTION_BANK[key] for key in priority if not present.get(key)]
    return questions[:limit]


def _snapshot(request: dict[str, Any], score: float, level: str) -> str:
    situation = _situation(request)
    facts = _facts(request)
    resources = _items(situation.get("resources"))
    constraints = _items(situation.get("constraints"))
    stakeholders = _items(situation.get("stakeholders"))
    fact_preview = "；".join(_text(fact.get("text")) for fact in facts[:3]) or "尚未补齐"
    return "\n".join(
        [
            f"现状清晰度：{score:.0f}/100（{LEVEL_LABELS.get(level, level)}）",
            f"目标：{_text(situation.get('goal')) or '尚未补齐'}",
            f"期限/成功标准：{_text(situation.get('deadline')) or '未说明'} / {_text(situation.get('success_metric')) or '未说明'}",
            f"阶段：{_text(situation.get('stage')) or '尚未补齐'}",
            f"资源：{'、'.join(resources) if resources else '尚未补齐'}",
            f"约束：{'、'.join(constraints) if constraints else '尚未补齐'}",
            f"相关方：{'、'.join(stakeholders) if stakeholders else '尚未补齐'}",
            f"已知事实：{fact_preview}",
        ]
    )


def assess_current_state_clarity(request: dict[str, Any]) -> dict[str, Any]:
    scores, present = _dimension_scores(request)
    total = sum(scores.values())
    level = _clarity_level(total)
    required_ready = all(present.get(key) for key in ["goal", "facts", "resources", "constraints"])
    diagnosis_allowed = total >= 60 and required_ready
    questions = _missing_questions(present, level)
    snapshot_ready = diagnosis_allowed and total >= 75
    return {
        "score": round(total, 1),
        "clarity_level": level,
        "diagnosis_allowed": diagnosis_allowed,
        "snapshot_ready": snapshot_ready,
        "dimension_scores": scores,
        "missing_dimensions": [DIMENSION_LABELS[key] for key, value in present.items() if not value],
        "questions": questions,
        "snapshot": _snapshot(request, total, level),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Assess whether a crux-diagnosis case is clear enough for diagnosis.")
    parser.add_argument("input_json", type=Path)
    args = parser.parse_args()
    request = json.loads(args.input_json.read_text(encoding="utf-8"))
    print(json.dumps(assess_current_state_clarity(request), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
