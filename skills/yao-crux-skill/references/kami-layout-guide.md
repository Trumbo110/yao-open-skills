# Kami Layout Guide

This skill borrows Kami's document discipline, not its whole template package. The goal is a high-trust Chinese diagnostic report that reads well on screen and prints cleanly.

## Visual Direction

- Artifact family: practical diagnostic report with a conclusion-first executive section.
- Tone: restrained editorial, warm paper surface, plain labels, dense but readable evidence tables.
- Primary color: ink-blue accent.
- Avoid: generic gradients, glass effects, oversized marketing hero blocks, decorative images, and repeated card grids.

## Core Tokens

| Token | Value | Use |
| --- | --- | --- |
| parchment | `#f5f4ed` | page background |
| ivory | `#faf9f5` | report panels |
| ink | `#141413` | body text |
| muted | `#6b6a64` | metadata |
| border | `#e8e6dc` | separators |
| brand | `#1B365D` | title accent and key labels |
| soft_brand | `#EEF2F7` | tags and low-emphasis highlights |

## Typography

- Chinese-first font stack: `"TsangerJinKai02", "Source Han Serif SC", "Noto Serif CJK SC", "Songti SC", "STSong", Georgia, serif`.
- If the preferred font is unavailable, the fallback must still render Chinese.
- Heading weight should stay restrained. Do not simulate heavy poster typography.
- Body line-height: `1.55` for reading, `1.4-1.45` for dense tables.

## Layout Rules

- Use A4 print rules for PDF.
- Keep margins around `20mm 22mm`.
- Use a top conclusion panel, then sections with brand-left-bar headings.
- Keep headings practical and action-oriented while preserving the required concepts: `主要矛盾判断过程`, `主要矛盾（最关键的卡点）`, `次要矛盾（先不主攻，但要盯住）`, `接下来怎么做`, `做完以后可能怎样`.
- Tables should be compact and comparison-led.
- Charts should clarify the reasoning, not decorate the report. Use inline SVG for HTML/PDF and compact table fallbacks for DOCX.
- Required chart family for full reports: analysis flow, photo-based iceberg model, contradiction decision matrix, resource allocation, and stage transition.
- The conclusion panel must use a split structure: left side for judgment, right side for first action, with compact metrics below. Do not place long action text inside equal-height metric cards.
- The main report content width must align with the top navigation container width. Avoid narrow centered panels that leave large unused gutters while the navigation spans wider.
- The iceberg model must use a real image where the small visible top and larger underwater mass are both legible. Do not use flat sea ice, glacier walls, abstract triangles, or purely atmospheric ice backgrounds.
- For a wide iceberg image, use it as a full-width visual anchor. Place `水面上` and `水面下` cards underneath, then use a full-width dark long module for `当前主要矛盾`.
- The decision matrix must reserve space for labels and legends inside the chart. Axis labels, dots, candidate names, and explanatory notes must not overlap or be clipped.
- The stage transition chart should prefer vertical cards or another low-collision layout when labels are long. Do not force long Chinese text into a single horizontal arrow chain.
- Use tags for `observed`, `estimated`, `assumed`, and confidence labels.
- Avoid nested cards. Panels may group distinct report sections, but page sections should remain simple.

## HTML/PDF Requirements

- HTML must not contain absolute local filesystem paths.
- Print CSS should hide interactive controls.
- PDF should be generated from the same HTML where possible.
- Long tables need `break-inside: avoid` only where it will not create large blank gaps.
- Check narrow viewport readability for HTML when the report is shared as a web artifact.
- Before handoff, review browser screenshots for the conclusion, content-width alignment, iceberg, decision matrix, and stage transition. Reject screenshots with horizontal overflow, cropped text, overlapping chart labels, large unintended empty zones, mismatched gutters, or image choices that contradict the model.
- Every externally sourced image needs a visible source/credit line in HTML/PDF and a source note in the skill assets or report references.

## Word Requirements

- DOCX should be clean and conservative: title, headings, short paragraphs, and tables.
- Do not attempt to recreate every HTML visual detail in Word.
- Preserve the same section order and language.
