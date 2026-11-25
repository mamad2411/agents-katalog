---
name: orchestra-router
description: >
  Runtime router for the orchestra system (v3 lean doctrine). Invoke when genuinely orchestrating
  multi-agent work or when unsure which specialist domain fits — build, design, research, marketing,
  content, SEO, leads, product, video, analytics, knowledge, documents, ads, automation, AI/ML, iOS,
  planning, growth, investing, cybersecurity — or for ideation/business-planning (which escalates to
  the NEXUS meta-conductor). Reference ~/.claude/rules/orchestra-system.md for the full roster.
---

# Orchestra Router

Routes requests to the right orchestra(s). **v3 doctrine: route silently — announce only delegation,
in one line.** This is the runtime companion to the reference doctrine at
`~/.claude/rules/orchestra-system.md`.

## Routing algorithm (run on every task)

1. **Check NEXUS first.** If the message signals ideation or business planning ("I have an idea",
   "thinking of building", "plan a business", "what if I built", "is this a good idea", "I've been
   thinking about", "should I build") → invoke the `nexus-strategy` skill. NEXUS becomes the
   meta-conductor and sequences orchestras across its 7 phases. This overrides single-orchestra
   routing — err toward firing it.

2. **Match intent to orchestra(s).** Use the trigger table below. Match on meaning, not just exact
   words. A request can match several — that's a stack.

3. **Detect stacks.** Compound requests activate multiple orchestras in sequence. Examples:
   - "make a landing page" → PLANNING → DESIGN → BUILD (QA inside) → optionally SEO/GROWTH
   - "launch my app" → MARKETING → CONTENT → SEO → PAID ADS → GROWTH → ANALYTICS
   - "find clients and email them" → LEAD GEN → CONTENT (email) → (ASK before sending)

4. **Announce delegation only, in one line.** No ensemble blocks. Format: `→ <conductor/agent>: <task>`
   (e.g. `→ search-agent: competitor pricing sweep`). Routing that doesn't delegate stays silent —
   the work leads the reply.

5. **Let the conductor lead.** Hand the work to the orchestra's conductor agent, which sequences
   its First Chair + Section players. One conductor per orchestra — no free-for-all.

6. **Respect allowances + gates.** Honor each orchestra's ASK-before rules and quality gate
   (see constitution). Reserve Bench agents never auto-fire — explicit name only.

## Trigger → Orchestra quick table

| If the message is about… | Activate |
|---|---|
| ideation, business idea, "what if", "should I build" | **NEXUS** (meta) → orchestras |
| build, fix, refactor, implement, deploy, code review, hard bug, diagnose, flaky test, can't reproduce, intermittent bug, investigate this error, debug this | 🏗️ BUILD |
| UI, UX, design, mockup, Figma, layout, brand visuals, component, 21st.dev, design inspiration, "give me UI ideas", build a component | 🎨 DESIGN — reach for **Magic / 21st.dev** MCP FIRST (component inspiration + generation) |
| research, investigate, competitive analysis, deep dive | 🔍 RESEARCH |
| marketing strategy, social, campaign, GTM, awareness | 📣 MARKETING |
| copy, blog, newsletter, carousel, email sequence | ✍️ CONTENT |
| SEO, rank, schema, AI search, GEO, AEO | 📈 SEO+GEO |
| find leads/clients, prospect, outreach, sales pipeline | 💼 LEAD GEN |
| PRD, product strategy, roadmap, prioritization | 🧩 PRODUCT |
| video, reels, image gen, thumbnail, Higgsfield | 🎬 VIDEO+MEDIA |
| analytics, metrics, funnel, cohort, A/B results, demand forecasting, trend prediction | 📊 ANALYTICS |
| remember, knowledge graph, Obsidian, map codebase, query NotebookLM, ask my notebooks (Python), notebooklm-scripts | 🧠 KNOWLEDGE |
| report, deck, PDF, doc, slides, save to Notion/Drive | 📄 DOCUMENTS |
| Google/Meta ads, PPC, paid media, ad creative | 💰 PAID ADS |
| automate, workflow, n8n, "when X do Y", recurring | ⚙️ AUTOMATION |
| stealth browser, cloakbrowser, bypass bot detection, bypass Cloudflare, bypass DataDome, fingerprint evasion, scrape without detection, AI agent browsing undetected | ⚙️ AUTOMATION |
| AI pipeline, multi-agent, build MCP, RAG, fine-tune, time-series forecast, TimesFM, predict future values, forecasting model | 🤖 AI/ML |
| iOS, Swift, SwiftUI, Xcode | 📱 iOS/SWIFT |
| plan, sprint, OKRs, user stories, pre-mortem | 📋 PLANNING |
| conversion, churn, paywall, ASO, pricing, retention | 🚀 GROWTH |
| invest, stock, valuation, DCF, earnings, portfolio | 💵 PERSONAL FINANCE |
| as CEO/CFO/CTO, founder advice, board deck, M&A, scenario plan, org health, strategic decision, devil's advocate, stress-test this | 👔 EXECUTIVE ADVISORY |
| RevOps, deal desk, pricing strategy, partnerships, RFP, customer success | 💼 LEAD GEN & SALES (RevOps section) |
| process mapping, vendor mgmt, procurement, capacity planning | ⚙️ AUTOMATION & OPS (Business Ops) |
| security incident, pentest, malware, forensics, DFIR, threat intel, CTI, vulnerability, CVE, exploit, ransomware, phishing investigation, red team, blue team, purple team, zero trust, OSINT, IOC, TTPs, MITRE ATT&CK, compliance audit, NIST, ISO 27001, PCI-DSS, OT/ICS/SCADA security, cloud breach, lateral movement, C2, threat hunting, detection engineering, Sigma, Volatility, Ghidra, BloodHound | 🛡️ CYBERSECURITY |

Full rosters (conductor, first chair, section, harness, gates) → `~/.claude/rules/orchestra-system.md`.

---

## Announcement format v3 (one-line delegation only)

The v2.3 mandatory-ensemble-block format is **retired** (2026-07-03, CLAUDE.md v3). Rules:

- Delegating to an agent/conductor → one line: `→ <conductor>: <task>`.
- Search-ladder hit/miss → one line: `🔍 Found in <rung>: <path>` / `🔍 Internal miss → external`.
- Everything else (skill picks, MCP usage, tool combinations) → **silent**. Use the right tool;
  don't narrate it. The work leads the reply.

Historical v2.3 format: `rules/orchestra-system.md` (reference only — do not revive).

---

## Internal-first search ladder (research tasks)

When 🔍 RESEARCH activates — alone, as part of a stack, or as a research sub-step inside another
orchestra (e.g. ✍️ CONTENT researching positioning, 📣 MARKETING checking competitor moves) — run
this ladder BEFORE spawning any external research agent (`search-agent`, `research-manager`,
WebSearch, WebFetch, brightdata, nimble, firecrawl, etc.).

**The ladder:**

1. **Obsidian brain** → `qmd` MCP. Query with both `type: 'lex'` (BM25 keyword) AND `type: 'vec'`
   (semantic). Provide `intent: <one-sentence task summary>` for snippet quality.
2. **`~/.claude/`** → grep across `CLAUDE.md`, `rules/*.md`, `workflows/*.md`,
   `docs/learnings/*.md`, project `memory/*.md`. Use `Grep` tool, not `find` + `read`.
3. **Score Archive** → `Skill(score-archive)` with `args: "search: <task description>"` — curated, high-signal namespace inside claude-mem of ✅ AUDIT-verified outcomes. Returns entries with `reusable_pattern` field for direct application. (Phase 1.6 shipped 2026-05-26.)
4. **claude-mem** → search via the `claude-mem` MCP if connected. Captures every prior session
   automatically — high recall on "what did we decide about X last week."

Only if rungs 1–4 return no useful hits → escalate to external.

**Announce which rung hit (always):**

- On hit: `🔍 Found in Obsidian: notes/decisions/orchestra-routing.md` (cite path + 1-line snippet)
- On full miss: `🔍 Internal ladder: 0 hits across 4 rungs → going external`

**Skip the ladder when:**

- Task is "fix this stack trace" / "debug this error message" (paste = self-contained)
- the user explicitly says "just web search" / "skip the ladder"
- Topic provably post-dates the last Obsidian sync (e.g. a tool released this week)

**Doctrine source:** `~/.claude/CLAUDE.md` § MEMORY & SEARCH — INTERNAL FIRST (non-negotiable).

---

## Chain protocol (reference only)

When multiple orchestras chain (e.g. DESIGN → BUILD → AUDIT), the full v2 protocol — chain-shape
selection, structured handoff payloads, quality gates, cycle detection, ASK_HUMAN pause/resume —
lives in `~/.claude/rules/orchestra-system.md` § Chain protocol. For routine stacks
(single conductor, linear order) it runs implicitly; read the reference only when orchestrating
3+ phase transitions or debugging multi-agent handoffs. The AUDIT gate for high-stakes work
(defaults NEEDS WORK, max 3 bounce-backs, then ask the user) always applies regardless.

---

## Notes

- **iOS axiom-* skills** don't auto-fire (disable-model-invocation). When 📱 activates, invoke them
  by name as needed (e.g. "use axiom-audit-swiftui-architecture").
- **Creative/feature work** still runs `superpowers:brainstorming` first (HARD-GATE) before BUILD.
- **"From now on when X"** automation requests need a HOOK (update-config skill), not memory.
- If a request matches nothing cleanly, say so and ask — don't force-fit.

### v2.1 primitives (added 2026-05-25)

- **Session start?** Read `HANDOFF.md` at project root FIRST, before any other action — that's
  the Handoff Standard (see `~/.claude/rules/orchestra-system.md` v2.1 Orchestra Primitives §1).
- **Context filling / about to compact?** The PreCompact hook + Context-Compaction Protocol
  preserves `handoff_registry`, pending ASK_HUMAN, and active chain state to
  `~/.claude/.compact-state.md` for rehydration after compaction (orchestra-system.md §2).
- **Caught a failure or false-positive?** Run the Calibration Loop — log → name the past mistake
  → embed as calibration anchor in doctrine → verify next time (orchestra-system.md §3).
- **Two skills could do the job?** `skill-selector` will pick a STACK (up to 3) if they're
  complementary, or a single winner if they're substitutes. Stack mode added in v2.1.
