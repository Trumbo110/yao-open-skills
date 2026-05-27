# Contradiction Model

## Practical Translation

矛盾分析 is a structured way to describe mutually constraining forces inside a real situation. For practical diagnosis:

- `主要矛盾`: the conflict that most determines the current stage's outcome.
- `矛盾的主要方面`: within the principal contradiction, the side currently dominating the situation's nature.
- `次要矛盾`: real conflicts that should be monitored or lightly handled, but should not consume core resources in the current stage.
- `转化条件`: signals that principal and secondary contradictions may switch positions.

Write every candidate contradiction as:

```text
力量A 与 力量B 的冲突
```

Avoid naming symptoms as contradictions. `会议太多` is a symptom. `多目标并行 与 关键人时间有限的冲突` is a contradiction.

## First-Principles Layer Gate

The main diagnosis risk is staying too close to the user's visible complaint. The principal contradiction is often upstream and partly invisible.

Run this gate before final scoring:

1. `看得见的问题`: list the symptoms the user can already name, such as overtime, rework, meetings, low conversion, repeated arguments, or unfinished tasks.
2. `上升一层`: ask which hidden variable can explain several visible problems at once.
3. `看不见的根部变量`: name the upstream constraint in operational terms, such as talent density, decision rights, value proof, cash runway, trust, attention allocation, or capability generation.
4. `反证`: ask what evidence would prove the visible problem is actually the principal contradiction, not a symptom.

Use these questions:

- If only one variable could be changed in the current stage, which one would make several visible problems easier?
- Which constraint explains why capable people are still trapped in details?
- What is the leader's scarcest high-leverage job right now: doing, deciding, recruiting, selling, learning, repairing trust, or building a system?
- Is this mainly a process problem, or a capacity/talent/system-generation problem that makes process fail?
- Is the current pain caused by lack of effort, or by the wrong scarce resource being consumed?

Team-management example:

```text
Visible symptoms:
- everyone works late
- standards and handoffs are immature
- capable people are stuck in communication and rescue work

Higher-layer read:
- the principal contradiction may be business complexity upgrading faster than the team's density of excellent people and system builders

Practical implication:
- the leader's main work may shift from personally optimizing every process to bringing in 2-3 stronger people, borrowing external expertise, and freeing existing strong people to build standards
```

This does not mean process is unimportant. It means process may be a secondary contradiction or a stop-loss action while the principal contradiction is talent density or organization capability.

## Method Anchors From Contradiction Theory

Use these as operating principles rather than slogans:

- Complex situations contain many contradictions; one current-stage contradiction usually leads and determines the others.
- Principal and secondary contradictions can change when the stage or external condition changes.
- The principal aspect inside the principal contradiction decides what currently defines the situation.
- Different contradictions require different methods; do not apply one fixed solution to every case.

In report language, show the logic plainly: `为什么不是先改流程`, `为什么不是先招人`, `为什么不是先做营销`, etc. The point is to prove why the chosen principal contradiction is more upstream than the obvious alternatives.

## Bayesian And Ockham Checks

Use these as supporting checks, not as a replacement for contradiction analysis.

Bayesian-style update:

- Treat each candidate contradiction as an explanation hypothesis.
- Start with a neutral prior unless strong domain evidence says otherwise.
- Raise confidence when the candidate explains observed facts, repeated patterns, scarce-resource consumption, and stage urgency.
- Lower confidence when the candidate only explains one local symptom or depends on weak assumptions.

Ockham razor:

- If two candidates have similar evidence, prefer the one that explains more visible problems with fewer extra assumptions.
- Do not choose a shallow answer just because it is simpler.
- A deeper principal contradiction can be the simplest explanation when it unifies many surface problems.

Example:

```text
加班 is visible.
流程不成熟 is closer to mechanism.
优秀人才密度不足 may be the simpler higher-layer explanation if it explains why流程不成熟、琐事膨胀、少数强人被困住 all happen together.
```

## Dynamic Time View

Principal contradiction is stage-bound. Every report should include a transfer view:

- current-stage principal contradiction
- conditions showing it has been relieved
- next likely principal contradictions
- evidence to collect before switching focus

Do not treat the current principal contradiction as a permanent label.

## Candidate Contradiction Types

| Type | Typical Shape |
| --- | --- |
| goal | Short-term survival vs long-term positioning |
| resource | Ambitious scope vs scarce people, cash, authority, or attention |
| value | User pain vs product value proposition |
| process | Demand inflow vs delivery capacity |
| relationship | Fairness, trust, or recognition gap between stakeholders |
| information | Decision need vs missing evidence |
| market | Customer buying barrier vs sales narrative |
| habit | Long-term benefit vs immediate feedback |
| risk | Growth attempt vs safety, legal, health, or reputation boundary |

## Weighted Scoring Model

Score every candidate from `0` to `5` on each dimension.

| Dimension | Weight | Question | High-Score Signal |
| --- | ---: | --- | --- |
| goal_impact | 0.25 | Does it directly decide whether the goal can be reached? | Without solving it, other efforts create only marginal improvement. |
| causal_leverage | 0.20 | Would solving it improve several other problems? | It is upstream of multiple symptoms. |
| stage_urgency | 0.15 | Is it decisive in this specific time window? | Missing the window increases cost sharply. |
| resource_constraint | 0.15 | Does it block the scarcest resource? | It consumes key people, cash, authority, attention, trust, or data. |
| changeability | 0.10 | Can the user directly change or influence it? | Action can create feedback in a short cycle. |
| spillover_risk | 0.10 | Will it amplify other risks if ignored? | It can trigger chain reactions. |
| evidence_strength | 0.05 | Is the judgment backed by facts, metrics, or repeated patterns? | There are records, interviews, time logs, or multiple observations. |

Formula:

```text
weighted_total =
  goal_impact * 0.25 +
  causal_leverage * 0.20 +
  stage_urgency * 0.15 +
  resource_constraint * 0.15 +
  changeability * 0.10 +
  spillover_risk * 0.10 +
  evidence_strength * 0.05
```

Decision rules:

- If the highest score is below `3.5/5`, output `不足以稳定判断` and ask for the missing evidence.
- If the top two are within `0.25`, prefer the one that is more upstream and releases the scarcest resource.
- If health, safety, law, major financial loss, or psychological crisis appears, treat it as a hard boundary even when it is not the highest-scoring contradiction.
- Do not rank only by emotional intensity. Emotion is evidence, not the scoring model.

## Principal Aspect

After selecting the principal contradiction, identify which side currently dominates.

Use this pattern:

```text
主要矛盾：A 与 B 的冲突。
矛盾主要方面：B 当前占支配地位，因为 ...
```

Common signals:

- the side that currently defines the outcome or blocks movement
- the side reinforced by environment, incentives, habit, or resource allocation
- the side that would change the situation's nature if reversed

## Secondary Contradictions

Do not call secondary contradictions unimportant. They should receive defer reasons and monitor triggers.

| Defer Reason | Meaning | Monitor Trigger |
| --- | --- | --- |
| low_leverage | Solving it does not change the key target much. | Metric worsens for 2-3 cycles. |
| low_control | It cannot be directly changed now. | External condition changes or influence path appears. |
| high_consumption | It consumes scarce resources. | Principal contradiction is relieved or risk crosses threshold. |
| replaceable_patch | A simple workaround is enough for now. | Patch failure affects target metric. |
| wrong_stage | It matters later, not in the current stage. | Stage transition or new milestone reached. |

## Probability Projection

The skill's probability numbers are decision-support estimates. They are not promises, guarantees, or statistical proofs.

Use a small transparent model:

```text
recommended_probability =
  baseline_success_probability
  + sum(action_completion_probability * estimated_uplift * dependency_discount)
  - sum(risk_probability * risk_impact)
```

Definitions:

- `baseline_success_probability`: probability of reaching the target if no focused intervention happens.
- `action_completion_probability`: likelihood that the action can actually be completed at the stated quality.
- `estimated_uplift`: expected improvement in target probability if the action works.
- `dependency_discount`: discount for action dependencies or overlapping effects.
- `risk_probability * risk_impact`: expected drag from risks that may offset the action.

Scenario defaults:

| Scenario | Calculation |
| --- | --- |
| maintain_status_quo | `baseline - 0.5 * expected_risk_drag` |
| recommended_execution | formula above |
| high_quality_execution | `baseline + 1.15 * sum(action uplift before completion discount) - 0.6 * expected_risk_drag` |
| low_execution_or_blocked | `baseline + 0.35 * expected_action_uplift - 1.1 * expected_risk_drag` |

Always show:

- probability interval or range, not only one number
- what assumptions most affect the result
- which evidence would raise or lower the probability
- why the probability should be revisited after action feedback

Confidence labels:

| Label | Use When |
| --- | --- |
| low | Mostly assumptions, sparse evidence, high dependency. |
| medium | Some facts and repeated patterns, but missing metrics or short feedback history. |
| medium-high | Concrete data, repeated observations, and clear feedback loop. |
