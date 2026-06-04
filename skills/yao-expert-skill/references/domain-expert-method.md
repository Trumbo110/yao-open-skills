# Domain Expert Method

Use this method to convert any field, industry, technology, role, market, product idea, or vague thought into a structured expert learning packet.

## Default Assumptions

When the user gives only a topic:

- `region`: infer from language and user context; in Chinese conversations, default to China first and note that global comparison can be added.
- `purpose`: quickly build domain expertise.
- `time_horizon`: current state through the next 3 years.
- `depth`: standard.
- `keyword_count`: 80, unless speed requires 50 or deep research requires 100.
- `formats`: Markdown, DOCX, PDF, and HTML.

State these assumptions at the top of the report. Ask at most three questions only when the answer changes sourcing, scope, or output shape.

## Expert Learning Standard

The minimum expert-level threshold is not "knows many facts." It is the ability to make bounded, evidenced, falsifiable judgments under uncertainty.

Evaluate the learner/report across six levels:

| Level | Name | Capability | Output |
|---|---|---|---|
| L0 | Purpose | knows why the domain is being studied | purpose, decision question, boundary |
| L1 | Facts | knows terms, products, players, people, institutions, and data | keyword teaching cards, company/person/case list, data cards |
| L2 | Classification | can split the domain by multiple valid lenses | classification tree, official/statistical/capital-market scope |
| L3 | Structure | can explain value chain, actors, incentives, competition | value-chain map, actor matrix, five-forces view |
| L4 | Dynamics | can judge lifecycle and change drivers | lifecycle diagnosis, trend radar, policy/technology variables |
| L5 | Judgment | can choose opportunities, risks, and next checks | strategic judgments, entry points, validation plan |

## Core Questions

Every report should answer these twelve questions, adapted to the topic:

1. What demand or problem does this domain solve, and why does it persist?
2. Where are the boundaries, and what similar things should be excluded?
3. Which official, statistical, technical, or capital-market classifications apply?
4. How does value flow from upstream inputs to end users?
5. Who buys, who uses, who influences, and who pays?
6. What are the scale, growth, penetration, and profit signals?
7. What are the cost structure, scale economy, and experience-curve dynamics?
8. Is competition fragmented, oligopolistic, platform-led, regionally split, or emerging?
9. How strong are entrants, substitutes, suppliers, buyers, and incumbents?
10. How do policy, standards, regulation, compliance, and qualifications matter?
11. Are technology, product form, data, channel, or business model changing?
12. What are the biggest opportunities, risks, and uncertainties over the next 3-5 years?
13. Which concepts, people, companies, institutions, products, and cases best help a newcomer understand the domain's real operating logic?

## Ten-Stage Workflow

### 0. Brief And Assumptions

Normalize:

- topic and aliases
- region and market scope
- purpose: learning, startup, investment, product, sales, hiring, interview, policy, research
- audience and prior knowledge
- time horizon
- depth: quick, standard, deep
- exclusions and forbidden sources

### 1. Boundary Definition

Create wide, narrow, exclusion, and data/source boundaries.

| Scope | Definition | Include | Exclude |
|---|---|---|---|
| Wide scope | full ecosystem | upstream, core products, channels, services | remote adjacent domains |
| Narrow scope | task-relevant center | target product, customer, region, use case | non-target scenarios |
| Data scope | measurable/researchable scope | official categories, public companies, standards | incompatible source scopes |
| Exclusion scope | false friends | terms and businesses easily confused | scope creep |

### 2. Classification Lenses

Use multiple lenses, then converge into a task-specific classification tree:

- official/statistical categories
- international categories when cross-border comparison matters
- capital-market categories and comparable companies
- value-chain roles
- customer and use-case segmentation
- business model segmentation
- technology/capability stack

For industries, common classification references include national statistical systems, NAICS, ISIC, GICS, and regulator or exchange categories. For non-industry domains, replace these with standards bodies, technical taxonomies, professional role taxonomies, or platform ecosystem categories.

### 3. Evidence Collection

Collect only enough evidence to support the report's decisions. Use `references/research-and-source-quality.md`.

Each key claim needs:

- claim text
- source and URL or local file
- source date and access date
- scope/definition
- evidence tier
- confidence
- whether the claim is `fact`, `inference`, `hypothesis`, or `unknown`

### 4. Current State Diagnosis

Analyze eight dimensions:

| Dimension | Core Question | Typical Output |
|---|---|---|
| Market | size, growth, penetration | TAM/SAM/SOM, trend signals |
| Demand | who buys and why | buyer chain, jobs, pain points |
| Supply | capacity and bottlenecks | production, delivery, talent, capability constraints |
| Competition | who competes and how | five forces, strategic groups, player matrix |
| Value chain | who creates/captures value | value-chain and profit-pool table |
| Policy | rules and standards | policy list, qualification gates |
| Technology | route and maturity | stack, S-curve, substitution risk |
| Capital/Finance | funding, valuation, economics | financing, M&A, gross margin, cash-flow clues |

### 5. Lifecycle Diagnosis

Judge lifecycle with evidence, not labels:

| Stage | Signals | Analysis Focus |
|---|---|---|
| Introduction | user education, uncertain demand, few players | demand validation, feasibility, early adopters |
| Growth | fast demand growth, active funding, more entrants | acquisition, channel, scale, standardization |
| Maturity | slower growth, concentration, efficiency pressure | cost, brand, M&A, differentiation |
| Decline | demand fall, substitution, exits | retreat, transition, niche defense, asset reuse |

Diagnose important subdomains separately. A mature overall market can contain high-growth technical or customer segments.

### 6. Actor And Enterprise Role Matrix

For industries and markets, expand beyond "design, manufacturing, service, marketing":

| Role | Core Capability | Revenue Source | Moat | Metrics |
|---|---|---|---|---|
| R&D/design | technology, product definition, IP | license, service, product | patents, talent, standards | R&D ratio, patents, cycle time |
| Materials/components | key inputs, stable quality | materials/components | process, certification, supply chain | yield, capacity, customer concentration |
| Manufacturing | process, scale, cost | OEM, product margin | equipment, yield, delivery | margin, utilization, capex |
| Brand/product | product, brand, channel | product, subscription, accessories | brand, UX, channel | share, repeat rate, AOV |
| Channel/marketing | traffic, distribution, relationships | commission, ads, transaction share | traffic, network, sales team | CAC, conversion, inventory |
| System integration | project delivery, solution packaging | project, maintenance | relationship, delivery record | cycle, collection, gross margin |
| Operations/service | ongoing operations, customer success | subscription, service, O&M | network, SLA, process | retention, renewal, cost to serve |
| Platform/ecosystem | matching, rules, data, network effects | commission, ads, subscription, data | network, rule setting | GMV, active users, supply/demand ratio |
| Compliance/certification | standards, testing, trust | testing, certification, consulting | qualification, credibility | certification cycle, customer count |
| Finance/insurance | capital and risk pricing | spread, premium, service fee | license, risk model, capital cost | default, premium, capital cost |

For non-commercial domains, translate these into roles such as standards body, tooling provider, practitioner, educator, regulator, community, maintainer, buyer, and end user.

### 7. Concept Teaching And Example Layer

Newcomers do not learn a domain from abstract definitions alone. For every important concept, add two layers:

- a simple mental model or analogy, so the learner can understand it without background knowledge
- a real domain anchor, such as a company, person, product, project, policy, institution, standard, user scenario, or failure case

Use representative objects as learning anchors, not as unsupported rankings. Label them by role:

| Anchor Type | What To Capture | Use |
|---|---|---|
| Person | founder, researcher, regulator, operator, buyer, practitioner, critic | show who shaped the field or who makes decisions |
| Company | manufacturer, platform, integrator, service provider, buyer, incumbent, startup | show how concepts appear in real business |
| Institution | regulator, association, standards body, exchange, university, lab | show rules, standards, legitimacy, and knowledge sources |
| Product/project | product line, project, pilot, benchmark, failure case | show practical implementation |
| Scenario | customer workflow, procurement scene, operating scene, risk event | show where the concept is used |

For each anchor, explain:

- why it is representative
- which concept or logic it illustrates
- what a newcomer should learn from it
- what not to over-infer from it
- source and date when factual

### 8. Keyword System

Generate `50-100` keyword cards. Group by:

- boundary and classification
- demand and customer
- product and service
- technology and process
- value chain
- business model
- competition
- policy and risk
- finance and operations
- trends and opportunities

Score candidates by frequency, centrality, decision impact, misunderstanding risk, beginner learning value, real-world observability, and evidence availability.

Keyword card fields:

| Field | Requirement |
|---|---|
| Keyword | include Chinese/English, abbreviation, aliases when useful |
| Plain one-liner | explain in one sentence for an intelligent outsider |
| Concept explanation | define the concept accurately and state its boundary |
| Bottom logic | explain why it exists, what problem it solves, and how it works |
| Module | demand, product, technology, value chain, policy, finance, etc. |
| Role/effect | what role it plays in the domain system |
| Real example | company, person, product, scenario, standard, project, or case |
| Practical application | where and how a practitioner would use it |
| Observable metric | what to track |
| Related concepts | parent, child, peer, and confused terms |
| Common misconception | how beginners misread it |
| Evidence | source or evidence type |

If the full report uses `50-80` keywords, do not compress all keyword fields into one wide table. Use grouped two-column cards or compact subsection cards so Word and PDF exports remain readable.

### 9. Concept Map

Do not leave keywords as isolated glossary entries. Add at least one relationship map:

- hierarchy: parent, child, peer concepts
- causality: variables that influence each other
- value: which concepts affect revenue, cost, growth, risk, compliance, or trust
- application: where the term appears in real companies, products, policy, or user behavior

Mermaid is acceptable for Markdown. HTML output must render as readable text/table if Mermaid is not processed.

### 10. Feynman Test

Generate ten self-test questions, each with a reference answer and `0-5` rubric:

1. Explain the domain in three plain-language sentences.
2. Define the boundary and name false friends.
3. Draw or describe the value chain and actors.
4. Compare three actor types and how each earns money or value.
5. Judge lifecycle stage and give evidence.
6. Identify where profit, power, or adoption leverage concentrates.
7. Name the top three entry barriers.
8. Choose a startup, product, investment, sales, or learning entry point.
9. Name the biggest 3-year change variable and how to track it.
10. Explain the domain with a simple analogy and one limitation of that analogy.

Scoring:

| Score | Standard |
|---:|---|
| 5 | simple language, structure, evidence, example, and counterexample |
| 4 | clear core logic with basic evidence |
| 3 | correct concepts but weak structure or evidence |
| 2 | term listing without causal links |
| 1 | weak relevance |
| 0 | cannot answer |

### 11. Final Synthesis

End with:

- reader-facing opening summary
- one-page executive brief
- expert tutorial path
- opportunity/risk/validation checklist
- uncertainty log
- source appendix
- next learning loop

## Writing Rhythm

This skill produces learning material for humans, not only a database of tables. Keep the writing coherent:

- Start the report with a `导读摘要` that introduces the material, its highlights, its reading path, and the logic behind the structure.
- Start every major module with a short paragraph that explains what the reader is about to learn and why it follows from the previous module.
- Use tables after the paragraph to organize information, not as a substitute for explanation.
- Prefer concrete examples and simple analogies before abstract framework names.
- When using a hard term, immediately explain it in ordinary language and tie it to a real domain example.
- Add transition sentences between sections when the next section changes lens, such as from boundary to classification, or from value chain to lifecycle.

## Common Failure Modes

- boundary drift: fix by explicit include/exclude scope
- data conflicts: fix by naming source definitions and dates
- second-hand-report dependence: add annual reports, policy, standards, primary docs, customer/JD signals
- hot terms without decision value: score keywords before including
- lifecycle overreach: diagnose subdomains separately
- learning without retrieval: force Feynman tests
- false certainty: label facts, inferences, hypotheses, and unknowns
