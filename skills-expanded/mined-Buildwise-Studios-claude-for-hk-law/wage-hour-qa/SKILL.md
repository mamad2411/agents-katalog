---
name: wage-hour-qa
description: >
  Jurisdiction-aware wage/hour and employment Q&A — classification, overtime,
  meal/rest breaks, leave, final pay — answered for the specific state/country
  with the controlling rule researched and cited rather than stated from
  memory. Use when the user asks any employment law question, or says "what's
  the rule in [state]", "is this exempt", "do we have to pay overtime for",
  or "can we classify this as".
argument-hint: "[question]"
---

# /wage-hour-qa

1. Load `~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md` → jurisdictional footprint.
2. Use the workflow below.
3. Identify jurisdiction the question is about. If not specified, ask.
4. Answer per that jurisdiction's rule. Cite. Flag if it's a close call or law is shifting.

---

## Matter context

**Matter context.** Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗` (the default for in-house users), skip the rest of this paragraph — skills use practice-level context and the matter machinery is invisible. If enabled and there is no active matter, ask: "Which matter is this for? Run `/employment-legal:matter-workspace switch <slug>` or say `practice-level`." Load the active matter's `matter.md` for matter-specific context and overrides. Write outputs to the matter folder at `~/.claude/plugins/config/claude-for-hk-law/employment-legal/matters/<matter-slug>/`. Never read another matter's files unless `Cross-matter context` is `on`.

---

## Purpose

"It depends" is true but unhelpful. This skill produces a Hong Kong-specific
answer grounded in the Employment Ordinance (Cap 57), Minimum Wage Ordinance (Cap 608), and
related legislation. HK has fewer jurisdictional variances than the US, but wage-related
entitlements (minimum wage rates, statutory holiday pay, sickness allowance calculation)
change periodically and should be verified against current rates.

## Load context

`~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md` → jurisdictional footprint. If the question doesn't specify a
jurisdiction, ask — or answer for the state with the most employees and note
that.

## The answer

### Step 1: Jurisdiction

Which state/country is this about? If not stated:
- If it's about a specific employee: where do they work?
- If it's a policy question: identify the jurisdictions in the footprint that
  are most likely to be the most restrictive on the question at hand, then
  research those.

### Step 2: Research the rule, then state it

> **Research before answering.** For the Hong Kong question, identify
> the currently operative rule. Cite the controlling primary source (Employment Ordinance section,
> Minimum Wage Ordinance, relevant case law) with a precise cite. Note the effective
> date and whether the rate or rule has been recently updated. If you are uncertain or cannot verify the current state of the
> law, say so and flag for attorney verification — do not state a rule you
> haven't confirmed.

State the rule in one paragraph, tied to the cite. Verify currency through
web search or legal resources — especially for:

> **Source attribution.** Tag every citation in the answer with where it came from.

- Statutory minimum wage rate under Cap 608 (verify current HK$ amount — checked annually by the Minimum Wage Commission).
- Final-wage timing on termination (Cap 57 s. 25 — within 7 days).
- Holiday pay and annual leave pay entitlement (Cap 57 Part VIIA and Part IX).
- Sickness allowance (Cap 57 Part VIII — eligibility after accumulating paid sickness days).
- Statutory holidays vs. statutory annual leave (Cap 57 Part VIII and Part IX — 12+ statutory holidays).
- Maternity/paternity leave entitlements (Cap 57 Part III and Part IIIA).
- End-of-year payment entitlement (Cap 57 Part IIC).
- Severance payment / Long Service Payment (Cap 57 Parts VA/VB).
- Employee vs. contractor classification — see `/employment-legal:worker-classification`.

Common HK question types:

- "What is the current statutory minimum wage?" — Research the current rate under Cap 608.
- "How much sickness allowance should we pay?" — Apply Cap 57 Part VIII (4/5 of normal wages, subject to accumulation rules).
- "Do we have to pay for public holidays?" — Research Cap 57 Part VIII, noting the distinction between statutory holidays and general holidays.
- "What's the correct notice period?" — Cap 57 s. 6 sets the minimum if the contract is silent.
- "How is severance payment calculated?" — Cap 57 Part VA formula: (last month's wages × 2/3) × years of service.
- "Can we classify this person as a contractor?" — Route to `/employment-legal:worker-classification`.

### Step 2a: HK wage calculations

When the question involves computing wages, holiday pay, sickness allowance, or severance/LSP under HK law, use the following principles:

1. **HK does not have a general statutory overtime regime.** Overtime is governed by the employment contract. If the contract is silent, there is no statutory minimum overtime rate.
2. **Wages defined (Cap 57 s. 2):** "Wages" includes all remuneration capable of being expressed in money, including commissions, bonuses, tips, and allowances, but EXCLUDES: end-of-year payments, benefits in kind, employer MPF contributions, travelling allowances, and gratuities.
3. **Sickness allowance:** 4/5 of the employee's normal daily wages. Only payable after the employee has accumulated paid sickness days (at least 4 days of continuous sickness). Cap 57 s. 33 and 35.
4. **Severance payment formula (Cap 57 Part VA):** (last month's wages × 2/3) × number of years of continuous employment, capped at HK$390,000 per employee `[verify current cap]`.
5. **Long Service Payment formula (Cap 57 Part VB):** Varies by age group and years of service — a percentage of (last month's wages × 2/3 × years of service). Cap 57 s. 31V.
6. **Final wages on termination:** Must be paid within 7 days of termination (Cap 57 s. 25). Late payment attracts interest.
7. **Statutory holidays:** 12+ statutory holidays per year (Cap 57 s. 39 Schedule 3). Holiday pay for employees with 3+ months continuous employment.
8. **Statutory annual leave:** 7–14 days depending on length of continuous employment (Cap 57 Part IX). Annual leave pay = daily average wages.
9. **End-of-year payment:** 13th month or contractual bonus. If the contract provides for it, it is payable on termination on a pro-rata basis (Cap 57 Part IIC).
10. **Limitation period for wage claims:** Labour Tribunal — 12 months from the cause of action; District Court / CFI — 6 years under the Limitation Ordinance (Cap 347).

If the question is a wage calculation and any of these inputs are
missing (wage breakdown, length of service, termination reason), **ask before computing**.

### Step 3: The flag

Is this a close call? Be honest.

- If the answer is clear on the researched rule: say so. "Exempt — meets
  each element of the applicable duties test and the current salary
  threshold."
- If it's close: say so. "The duties test is borderline — this role could
  go either way. Recommend classifying as non-exempt to be safe, or getting
  a formal opinion."
- If the law is in flux: say so. "This rule has been amended recently — the
  current version takes effect [date]. Confirm effective date before relying
  on this answer."
- If you could not verify currency: say so. Do not guess.

## Output format

Conversational. This is a Q&A, not a memo.

> **Research-connector pre-flight.** Before emitting the answer, check whether a legal research connector is reachable for this session — Westlaw, CourtListener, or any firm-configured research MCP. Collect this into the reviewer note per CLAUDE.md `## Outputs`: if no connector returns results in Step 2 (or none is configured at run time), record it in the **Sources:** line of the reviewer note — e.g., `not connected — cites from training knowledge; pinpoint cites (volume/page/subsection) carry the highest fabrication risk, spot-check those first`. Per-citation `[model knowledge — verify]` tags remain inline. Do not emit a standalone banner above the output.

> **Jurisdiction assumption.** Answers apply only to Hong Kong SAR employment law. The Employment Ordinance (Cap 57), Minimum Wage Ordinance (Cap 608), and related statutory provisions govern wage and hour matters in HK. If the employee works outside HK, or if choice-of-law is different, this answer may not apply as written.

```
**[Jurisdiction]:** [The researched rule, one paragraph, with pinpoint cite
and currency note.]

[If close call or shifting law: the flag.]

[If the answer differs in other footprint jurisdictions: one line noting that,
and whether the differences are material.]
```

> **Verify citations.** Any case, statute, regulation, or wage-order cite above was generated with AI assistance. Before relying on a cite, check it against Westlaw, CourtListener, the relevant state agency's site, or your firm's research tool for accuracy, currency, and subsequent history. Fabricated or misquoted citations in filings or formal advice have resulted in sanctions.

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs`. Customize the options to what this skill just produced — the five default branches (draft the X, escalate, get more facts, watch and wait, something else) are a starting point, not a lock-in. The tree is the output; the lawyer picks.

## What this skill does not do

- State the rule from memory — every answer is grounded in a researched,
  cited primary source verified for currency.
- Make classification decisions for borderline cases. It states the rule and
  flags the close call. Human decides.
- Give a 50-state survey unless asked. Answers for the relevant
  jurisdiction(s).
- Track when the answer changes. If thresholds index or law shifts, the
  answer goes stale. Re-ask for current.
