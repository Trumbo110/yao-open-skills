# Research And Source Quality

Use this reference before writing any expert report. The output must be useful for learning, but it must also make evidence quality visible.

## Currentness Rule

If a fact could have changed recently, verify it with current sources before using it. This includes market size, regulation, company status, product specs, funding, standards, leadership, pricing, laws, policies, benchmarks, library versions, and active industry trends.

For current facts, record:

- source URL or local file path
- publisher/author
- publication or filing date
- access date
- geography and scope
- whether the fact is still likely current

## Source Priority

Use the highest available tier first:

| Tier | Source Type | Use |
|---|---|---|
| 1 | official statistics, regulators, laws, standards, primary docs | boundaries, rules, market definitions |
| 2 | annual reports, prospectuses, filings, investor materials | company economics, risk language, segment data |
| 3 | industry associations, academic papers, patents, standards groups | technical structure, terminology, consensus |
| 4 | leading company websites, product docs, pricing pages, job posts | real product, capability, buyer, and talent signals |
| 5 | reputable research firms, trade media, expert interviews | market narrative and triangulation |
| 6 | forums, social posts, customer communities, blogs | pain points and weak signals only |

Avoid padding the source list. Fewer strong sources are better than many weak ones.

## Evidence Labels

Every important claim should be labeled:

- `fact`: directly supported by primary or highly credible sources
- `inference`: reasoned from facts, with a clear link
- `hypothesis`: plausible but not yet validated
- `unknown`: missing, conflicting, or unavailable

For high-impact claims, add confidence:

| Confidence | Meaning |
|---|---|
| High | multiple strong sources agree, scope is clear |
| Medium | credible source exists, but scope/time/definition limits remain |
| Low | weak, old, partial, or indirect support |

## Research Plan Pattern

For each topic, build a compact source plan:

1. boundary and classification sources
2. current market/state sources
3. actor/company/case sources
4. technical/policy/standard sources
5. customer/practitioner signal sources
6. counterevidence and uncertainty sources

## Handling Conflicts

When sources conflict:

- compare definition, geography, date, unit, and inclusion/exclusion scope
- do not average numbers blindly
- present the range and explain why the range exists
- prefer primary filings/statistics for facts, and use research reports for interpretation
- move unresolved conflicts into the uncertainty log

## Citation Style

Use concise citations in the report body and a full source appendix at the end. Citations should not interrupt reading flow.

For each source appendix entry include:

```text
Title:
Publisher:
URL or local path:
Date:
Access date:
Scope:
Used for:
Confidence:
```

## Privacy And Local Files

If the user supplies private notes or local files:

- treat them as input material, not public citations unless the user wants that
- never expose absolute local paths in public HTML, DOCX, PDF, or Markdown exports
- refer to them as "user-provided notes" or a safe short label
- do not upload or publish private files unless explicitly requested
