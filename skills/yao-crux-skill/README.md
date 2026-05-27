# Yao Crux Skill

`yao-crux-skill` helps diagnose complex real-world situations by clarifying the current state first, then separating the principal contradiction from secondary contradictions and turning the diagnosis into a practical action report.

It is designed for cases where the user is stuck among many visible problems, limited resources, unclear priorities, and moving constraints. The core question is:

> If we can only focus on one root conflict at this stage, what should it be?

## What It Produces

- concise follow-up questions when the current state is not clear enough
- a current-state snapshot covering goal, facts, stage, constraints, resources, stakeholders, and repeated patterns
- visible symptom and hidden root-variable separation
- principal contradiction and secondary contradiction diagnosis
- principal aspect, reversal conditions, and review triggers
- 1-3 focused actions with owner, deadline, metric, and probability projection
- synchronized Markdown, HTML, DOCX, PDF, and report JSON outputs

## Public Examples

This public release includes three fictional example report bundles:

- `reports/github-examples/example-b2b-saas-sales-conversion.*`
- `reports/github-examples/example-ecommerce-inventory-cashflow.*`
- `reports/github-examples/example-customer-support-delivery.*`

Private real-case reports and private user inputs are intentionally not included.

## Quick Run

From this skill directory:

```bash
python3 scripts/generate_report_bundle.py input/github_examples/b2b_saas_sales_conversion_case.json reports/github-examples
python3 scripts/verify_report_bundle.py reports/github-examples
```

The generator writes:

- `.report.json`
- `.md`
- `.html`
- `.docx`
- `.pdf`

## Source Layout

- `SKILL.md`: routing rules and default workflow
- `references/`: diagnosis logic, questioning rules, report contract, and layout rules
- `scripts/`: current-state scoring, report generation, and report verification
- `templates/`: canonical report schema and HTML/PDF theme
- `input/`: template and fictional example inputs
- `evals/`: routing, reasoning, language, and visual-report checks
- `reports/github-examples/`: fictional example report bundles
