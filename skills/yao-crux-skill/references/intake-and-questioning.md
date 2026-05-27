# Intake And Questioning

## Operating Stance

Start from the user's lived situation. The first response should sound like a calm diagnosis partner, not a form. Summarize what the user has already said, then ask only the questions that can change the principal-contradiction judgment.

Core principle: `先追问，后判断；先目标，后矛盾；先事实，后结论。`

## Current-State Gate

The hard part is not the contradiction score. The hard part is making the current situation clear enough that the score means something. Before naming a principal contradiction, build and check a current-state model.

Use `scripts/current_state_clarity.py` for structured cases, or apply the same gate manually in conversation.

| Dimension | Weight | What Counts As Clear |
| --- | ---: | --- |
| Goal and success standard | 20 | The user states what should change, by when, and how success is measured. |
| Facts and evidence | 20 | At least 2 concrete observed or estimated facts, not only interpretations. |
| Stage | 12 | The current phase is named: startup, validation, growth, repair, transition, recovery, etc. |
| Scarce resources | 12 | Time, people, cash, authority, attention, trust, data, or energy constraints are explicit. |
| Hard constraints | 12 | Legal, health, safety, ethical, cash, relationship, or commitment boundaries are explicit. |
| Stakeholders | 8 | Relevant people or organizations and their interests are visible. |
| Repeated patterns and attempts | 8 | The user names recurrence, trigger points, previous attempts, or missing evidence. |

Gate:

- `0-54`: `insufficient`. Do not output a principal contradiction. Ask up to 3 decisive questions.
- `55-74`: `workable`. Output a current-state snapshot and a provisional read only if useful; ask the remaining questions.
- `75-100`: `clear`. Restate the current-state snapshot and ask the user to confirm or correct it before deep diagnosis.

Hard requirements for diagnosis:

- goal with deadline or success metric
- at least 2 concrete facts marked `observed` or `estimated`
- scarce resources
- hard constraints

If any hard requirement is missing, the right output is a clarification turn, not a polished diagnosis.

## Input Contract

| Field | Priority | What To Capture |
| --- | --- | --- |
| conflict_situation | required | The user's natural-language description of what is stuck or conflicting. |
| goal | high | What should change, by when, and how success will be measured. |
| stage | high | Startup, validation, growth, repair, transition, recovery, relationship repair, learning, health habit, or other current phase. |
| resources | high | Time, people, money, authority, attention, trust, data, energy, and external support. |
| constraints | required | Legal, health, safety, ethics, commitments, runway, reputation, or non-negotiable boundaries. |
| previous_attempts | useful | What has already been tried and what happened. |
| stakeholders | useful | People or organizations involved, their interests, power, and incentives. |
| evidence | useful | Metrics, records, feedback, customer interviews, time logs, transactions, repeated patterns, or concrete events. |

## Follow-Up Budget

- If the user gives very little information, ask exactly 3 questions:
  1. `你希望这个问题在什么期限内变成什么状态？怎样算解决？`
  2. `当前最卡住你的是什么？请尽量说事实，而不是解释。`
  3. `你现在最稀缺的资源是什么：时间、人、钱、权限、注意力、信任、数据，还是其他？`
- If the user gives enough context but lacks decisive evidence, ask no more than 5 questions.
- If only one or two fields are missing, ask only those fields.
- Do not ask the user to fill a long template unless they ask for a template.

## Current-State Snapshot

Before scoring contradictions, produce this snapshot and let the user correct it:

```text
我先复述一下我理解的现状，看看有没有偏差：
- 目标：
- 期限/成功标准：
- 当前阶段：
- 已发生事实：
- 最稀缺资源：
- 不可突破约束：
- 相关方：
- 反复出现的模式/已尝试动作：

如果这版现状准确，我再进入主次矛盾判断；如果不准确，你先改这一版。
```

Do not hide this step when the user gives a real case. It is the quality gate for the entire skill.

## High-Value Question Bank

Use these selectively.

| Purpose | Question |
| --- | --- |
| Lock target | `你希望这个问题在什么期限内变成什么状态？怎样算解决？` |
| Identify stage | `这是启动期、验证期、增长期、修复期、转型期，还是恢复期的问题？` |
| Find scarce resource | `现在最稀缺的是时间、人、钱、权限、注意力、信任，还是数据？` |
| Separate fact from interpretation | `哪些是已经发生的事实？哪些是你的解释、担心或推测？` |
| Find recurring pattern | `类似问题出现过几次？通常在什么节点爆发？` |
| Separate internal/external cause | `哪些因素你能直接改变？哪些只能影响、规避或等待？` |
| Stakeholder conflict | `涉及哪些人？每个人最在意的结果分别是什么？` |
| One-problem test | `如果接下来30天只能解决一个问题，解决哪个会带来最大变化？` |
| Secondary contradiction test | `哪些问题很烦，但即使解决也不能明显改变目标结果？` |
| Review condition | `什么信号出现时，说明主要矛盾已经转移？` |

## Upstream Diagnosis Questions

Use these when the user gives many symptoms but the real principal contradiction may be hidden one layer above the symptoms.

| Purpose | Question |
| --- | --- |
| Find common cause | `这些看得见的问题背后，有没有一个共同原因？如果它变了，哪些问题会一起变轻？` |
| Test talent density | `现在是不是少数优秀的人在救火？如果多2到3个同等级或更强的人进来，哪些问题会自然缓解？` |
| Test leader leverage | `作为负责人，你现在最应该亲自做的是交付细节、流程补洞、招人借力、客户边界、还是授权训练？` |
| Separate process from capacity | `流程不成熟是根因，还是因为缺少能设计、推动、训练并维护流程的人？` |
| Find invisible constraint | `有什么问题大家不常说，但它决定了这些表面问题反复出现？比如人才密度、权限、信任、现金、注意力、客户边界。` |
| Rebut obvious answer | `为什么不是先处理那个最明显的问题？什么证据说明它只是表象？` |
| Time allocation | `你或团队现在的时间大概花在哪几类事情上？如果粗略分100%，各占多少？` |
| Attention allocation | `你作为负责人最常被什么事情拉走注意力？这些事情和真正能改变局面的事情一致吗？` |
| Resource tilt | `接下来30到45天，哪些事情应该减少投入，哪些事情应该明显加倍投入？` |
| Stage transfer | `如果当前主要矛盾被缓解，下一阶段最可能冒出来的新主要矛盾是什么？什么信号会说明它已经转移？` |

## First Response Pattern

When the user provides a messy case, respond in this shape:

1. One sentence reflecting the situation.
2. One sentence explaining what must be clarified before a principal contradiction can be responsibly named.
3. Ask 3-5 numbered questions.
4. Promise the output: principal contradiction, principal aspect, secondary contradictions, action focus, probability projection, and report bundle if needed.

Example:

```text
我先把你这件事当成“目标、资源和执行路径互相拉扯”的问题看。要判断主要矛盾，关键不是把所有问题列全，而是先知道哪一个问题最决定接下来30-90天的结果。

我只追问4个会改变判断的问题：
1. ...
```

## When To Proceed Without More Questions

Proceed with a provisional analysis when:

- the user already supplied target, stage, constraints, and at least 2 concrete facts
- the top contradiction can be stated with confidence caveats
- missing information can be listed as assumptions and tested through the action plan

Label this clearly: `临时判断，等待更多证据后可调整。`

Never produce four-format reports from an unconfirmed sparse current-state model unless the user explicitly wants a worksheet instead of a diagnosis.
