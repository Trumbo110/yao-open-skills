# Output Risk Profile

## Top Risks

| Risk | Failure Mode | Guardrail |
|---|---|---|
| Boundary drift | report mixes adjacent domains and becomes unfocused | require wide/narrow/exclusion/data scope |
| Weak evidence | second-hand reports dominate current facts | use source tiers, currentness rule, access dates |
| False certainty | estimates and hypotheses read like facts | label fact/inference/hypothesis/unknown |
| Keyword bloat | 80 terms become a glossary dump | group terms and add decision value, metrics, misconceptions |
| Tutorial shallowness | tutorial repeats report headings without learning steps | require module goal, concept, case, practice, success check |
| Wide table overflow | Word/PDF tables spill or become unreadable | prefer 6 columns or fewer, wrap cells, validate exports |
| HTML navigation failure | long report has no usable anchor menu | export script injects stable H2 anchors and fixed left numbered nav |
| Local path leakage | private file paths appear in public output | validation checks `/Users/`, `file://`, and Windows paths |

## Reviewer Focus

Reviewers should inspect:

- first page summary clarity
- boundary table
- one dense table in Word/PDF
- keyword card readability
- Feynman questions and rubrics
- source appendix quality
- HTML fixed left navigation, ordered labels, and mobile wrapping
