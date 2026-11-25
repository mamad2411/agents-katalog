---
name: emplaw-cold-start-interview
version: 1.0.0
description: Run a structured onboarding interview that captures an organization's profile so the employment-legal plugin can map which statutes and thresholds apply.
author: matrixx0070
tags: [onboarding, intake, compliance, configuration, employment-law]
capabilities: []
---

## When to use
Use this the first time an organization installs the employment-legal plugin, or after a material change (acquisition, new-state expansion, crossing a headcount threshold). You are gathering the facts that decide which laws attach — headcount, geography, industry, union status — and storing them as the plugin's configuration baseline. **Not for:** applying house style or template defaults once facts are known (that is emplaw-customize); drafting a policy (emplaw-policy-drafting); opening a specific dispute file (emplaw-matter-workspace); reviewing a handbook (emplaw-handbook-updates).

## Method
1. Collect entity basics: legal name, EIN, HQ state, and the full list of operating states. Decision point: if the org operates in more than one state, flag multi-jurisdiction and collect per-state headcount, else default to single-state config.
2. Collect total headcount and per-worksite counts. Decision point: if any worksite plus others within 75 miles reaches 50+, mark FMLA-eligible; if total is 15+, mark Title VII/ADA; 20+ mark ADEA/COBRA; 100+ mark WARN.
3. Record industry (NAICS), contractor vs. employee mix, and remote/hybrid footprint by state.
4. Record union status and any collective-bargaining agreements. Decision point: if unionized, route policy changes through the CBA-review flag.
5. Capture existing handbook and standalone policies; note last-reviewed dates.
6. Capture preferred escalation counsel and their bar jurisdictions.
7. Write results to the plugin config and confirm the triggered-law list with the client.

## Example
A SaaS company: HQ Texas, remote staff in CA, NY, TX; 62 total employees, 40 in TX, 12 CA, 10 NY. Interview flags Title VII/ADA/ADEA/COBRA (62 ≥ 20), no single 75-mile cluster at 50 so FMLA is state-driven, and CA FEHA at 5+ plus NY/NYC thresholds. Output config lists these plus "confirm CA-cluster for federal FMLA."

## Pitfalls
- **Counting only the HQ headcount.** Federal thresholds aggregate across worksites; a distributed 62-person org still clears 20+ triggers.
- **Ignoring remote workers' states.** A single employee can pull an org under CA FEHA (5+) or NYC law; capture every work-location state.
- **Treating contractors as out of scope.** Misclassification can retroactively add covered employees; record the mix, do not assume.
- **Skipping the counsel field.** Escalation is required for advice-adjacent output; a missing counsel contact blocks sign-off downstream.

## Output format
```
EMPLAW ORG PROFILE — <legal name>
HQ state: <state>   Operating states: <list>
Total headcount: <n>   Worksite breakdown: <site:n; ...>
Industry (NAICS): <code>   Contractor mix: <%>
Remote/hybrid footprint: <states>
Union status: <none | CBA: name/expiry>
Existing handbook: <yes/no, last reviewed>   Standalone policies: <list>
Triggered laws: <Title VII, ADA, ADEA, FMLA?, WARN?, COBRA, state: ...>
Escalation counsel: <name, firm, bar states>
Open items to confirm: <...>
```

## Reference
General thresholds (not tailored legal advice — escalate to licensed counsel before relying on any determination): Title VII and ADA at 15+ employees; ADEA at 20+; COBRA at 20+; FMLA at 50+ employees within 75 miles; WARN Act at 100+ with 60-day notice on mass layoff/plant closing; FLSA covers virtually all employers. State variations: CA FEHA at 5+ (harassment 1+), NY State Human Rights Law all employers, NYC at 4+. Count on the calendar-week test (20+ weeks in current or preceding year for most federal statutes). This skill configures scope only; it does not render legal conclusions.
