# Report And Tutorial Contract

The canonical artifact is one Markdown document that contains both the expert report and the expert learning tutorial. All other formats are generated from this Markdown.

## Canonical File

Name it:

```text
{basename}.md
```

Use stable headings so exports can generate anchors:

```markdown
# {领域/行业/主题} 专家学习报告

## 导读摘要
## 0. 默认假设与研究边界
## 1. 一页专家速览
## 2. 领域定义、边界与排除项
## 3. 多口径分类地图
## 4. 价值链、参与者与利润池
## 5. 当前状态八维诊断
## 6. 生命周期与变化变量
## 7. 竞争结构、壁垒与替代风险
## 8. 政策、标准、技术与资本信号
## 9. 代表公司、人物、机构、案例或实践场景
## 10. 关键词库与概念关系图
## 11. 专家学习教程
## 12. 费曼问题、参考答案与评分
## 13. 机会、风险与验证清单
## 14. 不确定性日志
## 15. 参考资料
```

If the topic is not an industry, translate "value chain" and "profit pool" into an equivalent structure: capability chain, workflow, stakeholder chain, ecosystem role map, or practice pipeline.

## Opening Summary

Every report must begin with `导读摘要` before the assumptions section. This opening is not a formal abstract. It is a reader-facing guide that makes the learning material easier to enter.

It must include:

- `这份学习材料解决什么问题`: explain who the report is for, what problem it helps solve, and what the reader should be able to explain or judge after reading.
- `本报告的三个亮点`: name three concrete strengths, such as structure-first learning, keyword teaching cards, real examples, or Feynman checks.
- `推荐阅读路径`: tell different readers how to use the report, such as newcomers, founders, product people, sales teams, investors, or team leads.
- `底层逻辑说明`: explain why the report moves from boundary, to structure, to dynamics, to examples, to self-test.

Write this section in connected prose. Avoid cold field-list language.

## Depth Modes

| Mode | Use | Keyword Count | Expected Shape |
|---|---|---:|---|
| quick | 30-minute orientation | 20-40 | short brief, one map, key terms, 5 checks |
| standard | default expert learning packet | 50-80 | full report, concept teaching cards, tutorial path, 10 Feynman questions |
| deep | startup/investment/team onboarding | 80-100 | stronger sourcing, richer people/company/case anchors, opportunity/risk map, validation plan |

## One-Page Expert Brief

Include:

- one-sentence definition
- boundary in/out
- top 5 facts or signals
- top 5 judgments
- top 5 risks/unknowns
- next 5 checks

## Module Writing Style

Each major section should start with a short reader-facing introduction before tables, matrices, or bullet lists.

The introduction should:

- explain what this module helps the reader understand
- connect it to the previous module
- state why it matters for a newcomer or decision-maker
- use natural sentences and concrete language

Avoid opening a module directly with a table unless the section is purely an appendix. Tables are for structure; paragraphs are for understanding and transition.

When the report needs technical terms, introduce them with a plain-language explanation first. Prefer `先说人话，再给术语，再给例子`:

1. plain explanation
2. accurate concept
3. real example or application
4. evidence or caveat

## Expert Tutorial Path

The tutorial is not a separate generic course. It should convert the report into a learning sequence:

| Module | Purpose | Content |
|---|---|---|
| orientation | know what the domain is | plain-language definition, false friends |
| vocabulary | speak the domain language | keyword groups and cards |
| structure | see the system | classification, actor map, value/capability chain |
| dynamics | understand change | lifecycle, policy, technology, economics |
| judgment | make decisions | opportunity, risk, entry point, validation |
| self-check | expose gaps | Feynman questions and rubric |

Each module should include:

- what to learn
- why it matters
- key concepts
- example or case
- practice task
- success check

## Representative Anchors

The report must include representative people, companies, institutions, products, projects, and practical scenarios when they help newcomers understand the domain. These anchors should be used as learning examples, not as unsupported rankings.

Each anchor should state:

- role in the domain
- why it is representative
- which concept or bottom logic it illustrates
- what a newcomer should learn from it
- what the learner should not over-infer from it
- source or evidence note

For export safety, render representative anchors as repeated two-column cards when fields are long. Do not use a six-column long-text table for people/company/institution anchors.

## Keyword Teaching Cards

For standard and deep reports, each keyword should be a teaching card, not a bare glossary line. Use this field set:

| Field | Requirement |
|---|---|
| 一句话通俗理解 | 用外行能听懂的一句话解释 |
| 概念阐述 | 准确定义，并说明边界 |
| 底层逻辑 | 它为什么存在，解决什么问题，如何运转 |
| 所属模块 | 需求、产品、技术、价值链、商业模式、政策、财务、风险等 |
| 作用 | 它影响什么判断、决策、成本、收入、风险或学习路径 |
| 行业真实示例 | 公司、人物、机构、产品、项目、政策、标准或事故案例 |
| 应用场景 | 从业者、创业者、投资人、产品、销售或新人如何使用它 |
| 可观察指标 | 可以跟踪什么数据或信号 |
| 相关概念 | 上位、下位、并列、相似和容易混淆的概念 |
| 常见误区 | 新人通常会怎样误解 |
| 证据 | 来源、日期、证据类型或待验证说明 |

For export safety, render each card as a two-column table or a short subsection. Do not put all fields for 50-80 keywords into one wide table.

## Tables

Use tables only when comparison is the main job. Keep table cells concise. Prefer multiple smaller tables over one wide table.

For export safety:

- avoid 6 or more columns when cells contain explanatory text
- prefer 2-column cards for long explanatory fields such as keyword cards, representative anchors, case cards, and source notes
- avoid long unbroken strings
- put URLs in the source appendix, not wide table cells
- split keyword cards into groups
- use compact labels and allow wrapping

## Source Appendix

Group sources by role:

- boundary/classification
- market/current state
- company/case
- policy/standard
- technical/academic
- customer/practitioner signal

## Delivery Note

After generating artifacts, report:

- assumptions used
- source coverage and known gaps
- files created
- validation result
- remaining warnings, if any
- top three next learning or validation moves
