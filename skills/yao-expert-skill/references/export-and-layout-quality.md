# Export And Layout Quality

The user-facing deliverable must work in Markdown, Word, PDF, and HTML. Do not hand-maintain four different documents. Use Markdown as the source of truth, then export and validate.

## Export Command

After drafting the canonical Markdown:

```bash
python scripts/export_expert_report.py path/to/report.md path/to/exports --title "标题" --basename report-name --formats md docx pdf html
python scripts/validate_artifacts.py path/to/exports --basename report-name --formats md docx pdf html
```

If a dependency is missing, state the exact missing tool and which formats were still produced.

## Markdown Requirements

- exactly one H1
- begins with a reader-facing `导读摘要` before formal report sections
- stable H2 sections from the report contract
- readable tables with concise cells
- citations in body kept compact
- source appendix included
- no absolute local paths in public output

## HTML Requirements

- standalone HTML
- fixed left-side navigation menu
- anchor links for H2/H3 sections
- left navigation anchor text should use ordered indices plus compact four-Chinese-character labels for Chinese reports, while keeping full section titles in the body and link `title` attributes
- readable on desktop and mobile
- tables must wrap text and stay inside the page
- generated tables should use compact column widths for low-content columns such as `题号`, `序号`, `编号`, `评分`, `分值`, `权重`, `占比`, and short status columns
- numeric, index, score, and other compact columns should be horizontally centered
- no absolute local filesystem paths
- no decorative visual system that fights the report's purpose

Minimum CSS properties:

```css
.side-nav { position: fixed; left: 0; top: 0; bottom: 0; z-index: 10; }
table { width: 100%; table-layout: fixed; border-collapse: collapse; }
th, td { overflow-wrap: anywhere; word-break: normal; }
th.col-number, td.col-number { text-align: center; font-variant-numeric: tabular-nums; }
```

## Word Requirements

Pandoc DOCX exports can produce poor tables if the Markdown is too wide. Before delivery:

- keep most tables at 6 columns or fewer
- split wide comparison tables
- avoid raw long URLs in cells
- avoid nested tables
- inspect DOCX warnings from `validate_artifacts.py`
- if a table is too wide, rewrite the table rather than relying on Word scaling

## PDF Requirements

PDF should be generated from the validated HTML when possible. Before delivery:

- confirm file exists and is non-empty
- hide the HTML navigation menu in print/PDF
- suppress browser print headers and footers, including date, file URL, and page chrome
- check that print CSS does not hide core content
- avoid fixed-width blocks that can overflow
- keep code blocks and tables wrapping
- if screenshots are available, inspect at least the first page and one dense table page

## Table And Border Rules

Tables should look like report tables, not spreadsheet dumps:

- subtle borders
- shaded header row
- consistent padding
- narrow columns for numbers, index values, score values, weights, short status labels, and date-like fields
- centered alignment for numeric and index columns
- no nested card/table structures
- cell text wraps rather than spills
- long evidence/source detail moves to source appendix
- long explanatory structures use two-column cards rather than six-column comparison tables

## Fixed Left Menu

HTML must include:

- a top-level `.side-nav`
- the report title or short label
- ordered list links to major sections, with visible indices like `01`, `02`, `03`
- Chinese labels like `默认边界`, `专家速览`, `分类地图`, `关键词库`, `费曼自测`, `参考资料`
- left fixed layout on desktop; compact sticky layout on narrow screens
- no standalone sidebar panel treatment: use transparent background, no enclosing border, and active text emphasis instead of a filled menu block
- active-anchor behavior when JavaScript is available

If JavaScript fails, links must still work.

## Validation

`scripts/validate_artifacts.py` checks:

- required formats exist
- Markdown, HTML, DOCX, and PDF all include the required `导读摘要`
- Markdown has one H1 and expected expert-report sections
- HTML contains fixed side nav and anchors
- Chinese HTML nav labels are compact four-character anchor text when applicable
- HTML tables include generated compact column sizing and centered number/index columns
- PDF exports are generated from a temporary print HTML with the navigation node removed, not merely hidden by CSS
- HTML/CSS contains overflow-safe table rules
- DOCX is a valid package and does not expose local paths
- PDF exists and is not empty
- public artifacts do not contain `/Users/`, `file://`, or unresolved placeholders

Treat validation warnings as layout review prompts. Fix warnings when they affect readability.
