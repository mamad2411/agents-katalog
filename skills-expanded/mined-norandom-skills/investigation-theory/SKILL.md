---
name: investigation-theory
version: 1.0.1
description: >
  Guide SOC and DFIR investigations with Investigation Theory's Diagnostic
  Inquiry workflow. Use for alert triage, evidence and log analysis, phishing,
  lateral movement, C2, malware, exfiltration, and insider cases. Produces case
  notes, playbooks, timelines, dispositions, compromise reports, and review
  diagrams. Excludes detection engineering and offensive work.
---

# Investigation Theory: InfoSec / Forensics

This skill operationalizes the Investigation Theory framework so every analyst follows the same methodology, uses the same vocabulary, and produces artifacts (notes, playbooks, timelines, reports, diagrams) that are directly comparable across a team.

Based on *Applied Network Defense* (2024) Sanders et. al. — specifically the *Investigation Theory: Information Security / Forensics* curriculum. Also based on course notes and personal research. CJCSM 6510 disposition codes come from US DoD Joint Chiefs of Staff manual CJCSM 6510.01B. Follow the curriculum closely — the goal is *unified methodic rigor*, not creative reinterpretation.

---

## Prime directive: Diagnostic Inquiry

Every investigation — from a single low-severity alert to a full crisis — follows the same repeating cognitive loop:

1. **Initial Observation** — IDS alert, hunt hit, or third-party notification.
2. **Interpreting Meaning** — Identify *relational*, *dispositional*, and *novelty* cues.
3. **Forecasting & Hypothesis Formation** — Predict what could have happened.
4. **Forming Investigative Questions** — Convert hypotheses into specific, relevant, answerable queries.
5. **Seeking Answers** — Retrieve, filter, manipulate evidence (see GAPSS in `references/methods.md`).
6. **Reaching a Conclusion** — Assign a disposition (see CJCSM 6510 in `references/documentation.md`).

Never skip a stage silently. If a stage is skipped, say so in the case notes and say why. A conclusion without supporting evidence is just an opinion — every conclusion must be explicitly tied to evidence.

Read `references/methods.md` before any non-trivial investigation work. It contains the full question taxonomy, GAPSS data manipulation model, triage strategies, and the discrete-vs-holistic analysis distinction.

---

## How to use this skill

1. **Identify the investigation tier** (see below). Ask the user briefly if unclear.
2. **Identify the use case** (phishing, lateral movement, C2/beaconing, malware, data exfil, insider, etc.). Load `references/use-cases.md` and follow the matching section — it lists key evidence sources and the preceding/context/succeeding questions to ask.
3. **Drive the Diagnostic Inquiry loop** — walk the user through each stage, surface the questions, record answers, and update the running attack timeline.
4. **Document as you go** using the templates in `assets/` — case notes, playbook entries, timeline, final report. Always use the *investigation statement + action statement* formula for case notes.
5. **Offer a diagram** when it helps comprehension (see "Visualization" below).
6. **Close with a disposition** mapped to CJCSM 6510 and a response category.

---

## Investigation tiers

Tiers set the *depth*, *ceremony*, and *required artifacts*. They do not change the underlying Diagnostic Inquiry loop.

### Tier 1 — Simple (single analyst, single alert, likely noise)
- **Context**: IDS/SIEM alert, looks falsifiable, individual contributor triage.
- **Triage strategy**: Threat-Centric (start Green queue, sort by Estimated Time to Falsify).
- **Required artifacts**: Case notes (investigation + action statements), disposition (often `9 — Explained Activity`), link to the evidence used.
- **Questions**: usually 1–3 context questions + 1 preceding/succeeding question.
- **Diagram**: optional — offer a *Triage Decision* diagram only on request.
- **Typical duration**: minutes.

### Tier 2 — Standard investigation (one or more alerts, real lead, potential compromise)
- **Context**: Pivoting across evidence sources, building out an attack timeline, a real hypothesis to prove or disprove.
- **Triage strategy**: Hybrid (Threat-Centric to clear noise, then Risk-Centric by host).
- **Required artifacts**: Full case notes, playbook reference (by name + UUID), attack timeline, evidence chain, disposition (1–7 range as appropriate), case-management ticket (e.g. The Hive) with attached exported evidence.
- **Questions**: Full event-relative set (preceding, succeeding, context, proximate), plus capability-matching questions.
- **Diagram**: *Diagnostic Inquiry Loop* and an *Attack Timeline* diagram are recommended.
- **Typical duration**: hours to days.

### Tier 3 — Crisis / major incident
- **Context**: Confirmed compromise, multi-host, executive visibility, possible regulatory impact.
- **Triage strategy**: Risk-Centric first, full business-impact scoring.
- **Required artifacts**: All Tier 2 artifacts + a formal **compromise report** using the *Once Upon a Time* storytelling pattern + a **Security M&M (Morbidity & Mortality)** peer review with Key Assumptions Check and alternative analysis + explicit response category mapping (elevated/critical/emergent).
- **Questions**: All types. Must include externally-sourced capability-matching questions against known threat intel.
- **Diagram**: *Attack Timeline with functional boundaries*, *Diagnostic Inquiry Loop*, and a *Tier-3 Response Flow* are required.
- **Typical duration**: days to weeks, multi-analyst.

Full tier matrix, escalation triggers, and exit criteria are in `references/tiers.md`.

---

## Use cases covered

The skill ships with standard procedures for these investigation types (see `references/use-cases.md`):

- Phishing & Mail Transaction Analysis
- Malware, Droppers & Suspicious File Execution (Sysmon EID 1, 4688, Prefetch, sandboxes)
- Web Proxy Log Analysis, C2 & Beaconing
- Lateral Movement & Windows Authentication (EID 4624 logon types, 4688, PSExec)
- Insider Threats vs. Compromised Accounts (watch the Base Rate Fallacy)
- Data Exfiltration (NetFlow, HTTP proxy, Producer Consumer Ratio)

Each section in `references/use-cases.md` is structured identically: *Evidence Sources* → *Preceding Questions* → *Context Questions* → *Succeeding Questions* → *Disposition Criteria*. Keep that ordering when you help the analyst — it is what makes results comparable across the team.

---

## Documentation (mandatory)

Read `references/documentation.md` for the full specification. The short version:

- **Case notes** = *investigation statement* (evidence reviewed + why + what found) + *action statement* (what you did + why). Technical audience, brief, exported evidence attached.
- **Attack timeline** is additive and *attacker-centric*; nodes are computers, data, processes; edges cross *functional boundaries* (internet / DMZ / internal / endpoint); spot *gaps* to generate new questions.
- **Disposition** uses the modified CJCSM 6510 scheme: 1 Root Level Intrusion, 2 User Level Intrusion, 3 DoS, 4 Malicious Logic, 5 Unsuccessful Activity Attempt, 6 Non-Compliance, 7 Reconnaissance, 8 Investigating *(working state only — must change before close)*, 9 Explained Activity, 0 Training/Exercise. Exactly one disposition per case; a closed case never carries 8.
- **Final report** is persuasive writing. Use the *Once Upon a Time* plot pattern (`references/documentation.md` has the full template).
- **Quality review** = Security M&M conference, devil's-advocate questioning, Key Assumptions Check, What-If analysis.

Templates live in `assets/`:
- `case-notes-template.md`
- `playbook-template.md` (Human-Centered Playbook Standard)
- `compromise-report-template.md`
- `evidence-wiki-entry-template.md`

---

## Visualization — draw.io diagrams

Diagrams must look the same across analysts so that any reader can recognise the artifact type at a glance. Read `references/diagram-standards.md` **before** generating any diagram — it contains the fixed color palette, node sizes, fonts, and the exact XML skeletons for the five standard diagram types:

1. **Diagnostic Inquiry Loop** — circular 6-node cycle of the loop.
2. **Attack Timeline with Functional Boundaries** — horizontal swimlanes (Internet | DMZ | Internal | Endpoint) with chronological events left-to-right.
3. **Triage Decision (Green/Yellow/Red)** — three-queue sort, Threat-Centric or Risk-Centric variant.
4. **Playbook Question Flow** — preceding → context → succeeding chained blocks with evidence-source callouts.
5. **Tier Escalation Flow** — Tier 1 → 2 → 3 escalation with response category mapping.

To render any diagram:
- Build the XML by copying the skeleton from `references/diagram-standards.md` and substituting labels.
- Use the `mcp__drawio__open_drawio_xml` tool to open it.
- Never invent new colors or shapes — uniformity *is* the point.

### Fallback when draw.io MCP is unavailable

If `mcp__drawio__open_drawio_xml` is not registered, render the diagram as **Mermaid markdown** inside a fenced code block and hand it back in chat. Tell the user they can paste it into a Markdown editor that renders Mermaid (Typora, Obsidian, or VS Code with the "Markdown Preview Mermaid Support" extension). `references/diagram-standards.md` provides a Mermaid version of each of the five standard diagrams; the visual styling is approximate, but the structure (stages, swimlanes, columns, queues, lanes) is preserved so the artifact remains comparable across analysts.

Do **not** write `.drawio` XML files to disk as a fallback — Mermaid in chat is faster to copy, version, and review.

## Routing to intana-viz

This skill owns the *Investigation Theory* workflow and its five standard diagrams. When the case calls for a structured analytic technique beyond that set — ACH (Analysis of Competing Hypotheses), Pre-Mortem on a defensive decision, Cultural Web for an org diagnosis, Devil's Advocacy scorecard, Key Assumptions Check matrix, Four Ways of Seeing, etc. — hand off to the **intana-viz** skill instead of improvising a new diagram type. intana-viz has 80+ techniques catalogued with draw.io templates.

Rule of thumb: if the diagram is *about the investigation itself* (loop, timeline, triage, playbook, tiers), stay here. If it is *about the analytic technique being applied inside the investigation*, route to intana-viz.

## Cross-skill handoff

Use this skill when another workflow depends on truthfulness, evidence, or missing facts. Not every negotiation party is truthful, not every scenario input is reliable, and not every stakeholder claim deserves to be priced at face value.

Export findings as a compact packet:

- Claim: the statement being tested.
- Source: who said it or where it came from.
- Evidence: support, contradiction, and confidence.
- Gap: what would verify or falsify the claim.
- Incentive: who benefits if the claim is true or false.
- Impact: which decision, payoff, scenario, or diagram changes.

Hand this packet to `game-theory-negotiation` when trust changes payoffs, BATNA, authority, or concession strategy. Hand it to `strategic-foresight-viz` when a claim affects future scenarios or early warning signs. Hand it to `intana-viz` when competing explanations need ACH, Red Teaming, or Key Assumptions Check.

---

## Worked example — phishing alert through three loop cycles

A compact end-to-end pass to anchor the workflow. The analyst is at Tier 1, working alone, and the case escalates to Tier 2 mid-investigation. All filenames, process names, domains, accounts, and hostnames below are illustrative evidence values in a fictional case, not bundled inputs or instructions to download files, visit domains, or run commands.

**Initial Observation (t0)** — IDS fires on inbound mail with attachment *Invoice_42.docm* to *jane.doe@corp*. Sender domain *accounts-billing.co* has no prior history.

**Cycle 1 — falsify the alert**
- *Interpreting Meaning:* relational cue (sender → recipient never seen), novelty cue (first-time domain). Dispositional cue (`.docm` macro file type).
- *Hypothesis:* phishing payload delivery.
- *Question (Context):* Do SPF / DKIM / DMARC pass? *(Source: mail headers.)*
- *Seeking Answers (Search):* headers show SPF softfail, DKIM none, DMARC `p=reject` would have blocked but no DMARC published by sender. Suspicious.
- *Conclusion so far:* alert is not falsified. Disposition stays **8 — Investigating**.

**Escalation trigger fires** — novelty cue + cannot falsify in one cycle. Move to **Tier 2**. Pull the Phishing playbook (`PHISH-001 / <UUID>`), open a Hive ticket, start the attack timeline.

**Cycle 2 — establish first-order impact**
- *Question (Succeeding):* Did Jane open the message and execute the attachment? *(Source: mail gateway delivery log + Sysmon EID 1 on her host.)*
- *Seeking Answers (Pivot):* mail logs confirm delivery 09:14, mail client read receipt 09:21. Sysmon shows *winword.exe* spawning *cmd.exe* spawning *powershell.exe* at 09:22 — macro execution chain.
- *Question (Capability-Matching, internal):* has this parent-child chain been seen on the network before? *(Source: EDR historical search.)*
- *Seeking Answers (Aggregation):* zero prior occurrences in 90 days. Add timeline node `t1: macro → cmd → powershell on JANE-LAPTOP`. Functional boundary: Endpoint.

**Cycle 3 — second-order impact**
- *Question (Succeeding):* What did the PowerShell do? *(Source: PowerShell Script Block logging, proxy logs.)*
- *Seeking Answers (Search expansion):* one outbound HTTPS to *cdn.accounts-billing.co* over port 8443. Proxy shows 412 KB downloaded *update.bin*. Add timeline nodes for the C2 contact and the file pull. Boundary crossings: Endpoint → Internal → Internet.
- *Reaching a Conclusion:* execution chain + outbound retrieval + no prior baseline = **Disposition 4 — Malicious Logic** on JANE-LAPTOP. No evidence yet of additional hosts, so **Response Category: Elevated** (not Critical).

**Close-out (Tier 2)**
- Case notes contain three entries, each in investigation-statement + action-statement form.
- Attack timeline (Diagnostic Inquiry Loop + Attack Timeline with Functional Boundaries diagrams) attached.
- Evidence chain ties every conclusion to its specific log export.
- Hive ticket filed, EDR isolation requested, the case is handed to IR if additional hosts surface.

Gaps to track: lateral movement post-execution (timeline gap → next question), payload analysis of *update.bin* (sandbox → next question), credential exposure on JANE-LAPTOP. Each gap is a candidate for a new loop cycle or an explicit "out of scope" note in the case notes.

---

## When the analyst is stuck

- Re-check which **stage** of Diagnostic Inquiry they are in. Most "stuck" moments are really "I jumped from Observation straight to Seeking Answers without forming a question."
- Ask a **utility question** to collect missing data (e.g., "we need the username before we can pivot to mail logs").
- Apply **GAPSS**: Graphs, Aggregations, Pivots, Search, Statistics.
- Switch **altitude**: discrete analysis of one event → holistic analysis of the timeline → back.
- Run a **Key Assumptions Check** — especially in insider-threat cases where the Base Rate Fallacy is the #1 failure mode.

---

## Reference index

- `references/methods.md` — Diagnostic Inquiry, question taxonomy, GAPSS, triage strategies, analysis techniques.
- `references/tiers.md` — Full tier matrix, escalation and exit criteria.
- `references/use-cases.md` — Per-use-case evidence sources, questions, disposition criteria.
- `references/documentation.md` — Case notes, timeline, evidence chain, disposition (CJCSM 6510), compromise report, M&M review.
- `references/diagram-standards.md` — Mandatory draw.io styling and XML skeletons.
- `assets/case-notes-template.md`
- `assets/case-notes-example.md` — filled-out reference for tone and granularity.
- `assets/playbook-template.md`
- `assets/compromise-report-template.md`
- `assets/evidence-wiki-entry-template.md`
- `evals/evals.json` — three regression scenarios (phishing, lateral movement, insider-vs-compromise).
