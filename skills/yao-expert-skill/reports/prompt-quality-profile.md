# Prompt Quality Profile

## Explicit Need

The user needs a reusable expert skill that accepts any field or idea and produces a polished, evidence-backed expert learning report and tutorial in four formats.

## Implicit Need

The skill must avoid becoming a vague "research this topic" prompt. It needs routing boundaries, a repeatable method, artifact contracts, and export checks.

## Role/Task/Format Mapping

| Layer | Skill Behavior |
|---|---|
| Role | domain expert teacher and research analyst |
| Task | build boundary, structure, evidence, keywords, learning path, and self-test |
| Format | canonical Markdown plus DOCX/PDF/HTML exports |

## Completeness Checks

- Does the description route broad expert-learning requests?
- Does it exclude quick answers, generic tutorials, pure business analysis, and conversion-only tasks?
- Does the workflow tell the agent when to research, write, export, and validate?
- Are artifact failure modes named in references rather than hidden in the prompt?

## Prompt Risks

- Over-asking intake questions: fixed by default assumptions.
- Over-writing generic frameworks: fixed by topic-specific boundary and evidence.
- Overloading `SKILL.md`: fixed by moving theory to `references/`.
- Skipping export validation: fixed by scripts in the workflow.
