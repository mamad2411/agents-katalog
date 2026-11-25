---
name: policy-analysis
description: Use when analyzing policy, regulation, law, government documents, official guidance, consultation papers, enforcement actions, industry rules, public-sector decisions, macro policy, industry policy, compliance implications, policy timelines, policy comparisons, or policy impact on companies, markets, products, operations, investment research, or risk. Prefer this Skill for source-grounded policy interpretation and impact mapping, not formal legal advice or unsupported speculation.
meta:
  version: 1
  display_name: 政策分析
---

# Policy Analysis

## Purpose

Analyze policies, regulations, government documents, official guidance, consultation papers, enforcement actions, industry rules, or public-sector decisions. The Skill identifies what the policy says, who it affects, when it applies, what changes, what risks or opportunities it creates, and what actions may need human review.

This Skill is a process-only built-in Skill for XAgent. It does not depend on any policy database, legal database, web search provider, MCP, parser, or script.

## Use When

Use for:

- interpreting policy, regulation, law, rules, notices, guidance, consultation drafts, implementation rules, enforcement actions, or public-sector decisions;
- analyzing macro, industry, regulatory, legal, compliance, company, market, product, or operational impact;
- comparing new and old policy requirements;
- extracting obligations, restrictions, incentives, penalties, timelines, transition periods, reporting requirements, and affected entities;
- mapping policy impact into business operations, compliance risks, market structure, industry winners and losers, financial exposure, or investment research inputs;
- preparing policy briefs, impact memos, company exposure notes, industry matrices, risk registers, timelines, or compliance action checklists.

Use `research-synthesis` when the main task is broad source gathering or cross-source validation. Use `investment-research` when the user needs a complete investment thesis or diligence memo. Use `financial-statement-analysis` when the policy impact must be translated into sourced financial metrics.

## Do Not Use When

Do not use for:

- formal legal advice, legal opinions, compliance sign-off, tax advice, accounting advice, or regulatory approval;
- pretending a media report, rumor, analyst comment, or market interpretation is official policy;
- predicting enforcement outcomes without evidence;
- making investment, trading, portfolio, or transaction recommendations;
- searching, downloading, filing, submitting, monitoring, or sending anything unless an XAgent tool explicitly performs that action.

## Material Gate

Before analyzing, identify:

- policy object: title, issuing authority, jurisdiction, policy type, publication date, effective date, current status, and source;
- status: draft, consultation paper, official rule, guidance, notice, enforcement action, implementation rule, interpretation, media report, or secondary commentary;
- affected parties: entities, industries, activities, products, regions, customer groups, investors, public bodies, or intermediaries;
- requested lens: plain-language interpretation, new-old comparison, compliance implication, company exposure, industry impact, investment research input, timeline, or action checklist;
- source scope and freshness: provided document only, official sources, secondary sources, current status needed, or historical analysis;
- uncertainty: missing official text, unclear effective date, pending rules, local implementation, enforcement discretion, conflicting sources, or translation risk.

If official text or dates are missing, mark the analysis as source-limited and use `待确认` for unresolved facts. Do not invent policy facts, obligations, penalties, effective dates, or regulator positions.

## Workflow

1. Define the policy question, jurisdiction, source scope, and what the analysis can and cannot decide.
2. Identify the policy object and status before interpreting impact. Drafts, consultations, official rules, enforcement actions, and media reports must not be treated as the same authority level.
3. Extract explicit policy facts: issuer, target entities, regulated activities, obligations, restrictions, incentives, penalties, deadlines, transition periods, reporting or disclosure requirements, and implementation mechanism.
4. Separate direct text, reasonable inference, assumptions, uncertainty, and items requiring official clarification or professional review.
5. Compare against previous state when relevant: new duties, removed duties, stricter requirements, relaxed requirements, implementation details, enforcement intensity, and changed incentives.
6. Map impact chain from rule to consequence using `references/policy-analysis-rules.md`: measure, affected actors, operational impact, financial impact, compliance impact, competitive impact, market impact, and second-order effects.
7. Assess materiality only when evidence supports it: high, medium, low, or uncertain. Explain the driver rather than only labeling severity.
8. For monetary policy, securities rules, banking rules, insurance rules, asset-management rules, disclosure rules, capital requirements, liquidity rules, IPO/refinancing/delisting rules, AML/KYC, crypto, or cross-border capital rules, use `references/financial-regulatory-impact-rules.md`.
9. Produce the user's requested artifact without forcing a fixed format.
10. Validate with the checks below before finalizing.

## Checks

- Policy source, source type, jurisdiction, issuer, publication date, effective date, and status are explicit or marked `待确认`.
- Drafts, consultations, official rules, guidance, enforcement notices, media reports, and analyst interpretations are not confused.
- Direct policy text, interpretation, assumptions, and uncertainty are separated.
- Affected entities, activities, obligations, restrictions, incentives, penalties, deadlines, and transition periods are identified when available.
- Impact claims are supported by policy content, source evidence, or stated assumptions.
- Legal, compliance, tax, accounting, or regulatory conclusions are caveated and routed to qualified human review when high-impact.
- Investment or market implications are framed as research inputs, not transaction instructions.

## Outputs

Return the form the user asks for: policy brief, impact memo, company exposure analysis, industry impact matrix, risk register, timeline, comparison table, investment implication summary, compliance action checklist, open-question list, or handoff context. Do not force a fixed template when a concise answer is enough.

## Boundary

Skill owns policy interpretation workflow, source/status discipline, obligation extraction, change comparison, impact-chain analysis, materiality framing, uncertainty labeling, and policy-risk/opportunity mapping.

This Skill does not provide formal legal advice, compliance approval, tax advice, accounting advice, regulatory assurance, investment advice, trade recommendations, or guaranteed enforcement predictions. It does not replace professional legal, compliance, tax, regulatory, or investment review.

It must not run shell, Python, Node, npm, curl, MCP, browser automation, legal database, policy database, filing, compliance system, trading, brokerage, banking, email, CRM, Office, or document-export commands by itself; those actions belong to XAgent tools visible in the current session.

## Resources

- `references/policy-analysis-rules.md`: policy object classification, extraction checklist, impact-chain rules, materiality factors, risk/opportunity categories, and comparison guidance.
- `references/financial-regulatory-impact-rules.md`: financial regulation and macro policy impact channels for financial institutions, listed companies, markets, products, and investors.
- `LICENSE`: source and license notice.
