---
name: llm-auditor
description: "Fact-checks LLM responses by extracting verifiable claims, verifying each via web search, producing an audit report with verdicts, and optionally revising inaccurate responses. Use when the user asks to audit, fact-check, double-check, or verify a response."
---

# LLM Auditor

Evaluate and improve the factual grounding of LLM-generated responses. Acts as an automated fact-checking layer that systematically analyzes claims against real-world information.

## When to Use This Skill

Activate when the user says things like:

- "audit that", "fact-check that", "double-check that"
- "verify those claims", "is that accurate?"
- "check your sources", "are you sure about that?"
- "audit this: [text]"
- Any request to validate factual accuracy of a previous response or provided text

## The Audit Process

Execute these three phases sequentially. Do NOT skip phases.

### Phase 1: Critic — Extract and Verify Claims

**Announce:** "Starting audit — extracting and verifying claims..."

Act as a professional investigative journalist excelling at critical thinking and verifying information.

**Step 1: Identify all CLAIMS**

Carefully read the response text. Extract every distinct claim made within the text. A claim can be:

- A statement of fact about the world
- A logical argument presented to support a point
- A quantitative assertion (numbers, dates, statistics)
- An attribution (who said/did what)

**Step 2: Verify each CLAIM**

For each claim identified:

1. **Consider the context:** Take into account the original question and other claims in the response.
2. **Search for evidence:** Use the `web_search` tool to find authoritative sources that support or contradict the claim. Conduct multiple searches per claim if initial evidence is insufficient.
3. **Determine the verdict:** Assign one of these verdicts:
   - **Accurate** — Correct, complete, and consistent with reliable sources
   - **Inaccurate** — Contains errors, omissions, or inconsistencies compared to reliable sources
   - **Disputed** — Reliable sources offer conflicting information; no definitive consensus
   - **Unsupported** — No reliable source found to substantiate the claim
   - **N/A** — Subjective opinion, personal belief, or fictional content not requiring verification
4. **Provide justification:** Clearly explain reasoning, referencing the sources consulted.

**Verification tips:**

- Non-trivial factual claims MUST be verified with web search, not just internal knowledge
- Highly-plausible or subjective claims may be assessed with internal knowledge alone
- Conduct multiple searches if the first search is insufficient
- Reference evidence with source URLs when available

**Step 3: Overall assessment**

After evaluating all claims, provide:

- **Overall verdict** for the entire response
- **Overall justification** explaining how individual claim evaluations led to this assessment

### Phase 2: Reviser — Correct Inaccuracies

**Only execute this phase if any claims were found Inaccurate, Disputed, or Unsupported.**

If the overall verdict is Accurate, skip to Phase 3.

Act as a professional editor. Minimally revise the original response to make it accurate while maintaining the overall structure, style, and length.

**Editing rules by verdict:**

| Verdict | Action |
|---------|--------|
| Accurate | No edit needed |
| Inaccurate | Fix following the justification from Phase 1 |
| Disputed | Present multiple sides to make the response more balanced |
| Unsupported | Soften the language, note the claim is unsupported, or omit if not central |
| N/A | No edit needed |

**Constraints:**

- Make minimal edits — preserve original structure and style
- Do NOT introduce any new claims or statements
- Ensure the revised response is self-consistent and fluent
- As a last resort, omit a claim if it's not central and impossible to fix

### Phase 3: Report — Present Results

Present the audit results in this format:

```markdown
## 🔍 Audit Report

| # | Claim | Verdict | Justification |
|---|-------|---------|---------------|
| 1 | [claim text] | ✅ Accurate | [brief justification] |
| 2 | [claim text] | ❌ Inaccurate | [brief justification with source] |
| 3 | [claim text] | ⚠️ Disputed | [brief justification] |
| 4 | [claim text] | ❓ Unsupported | [brief justification] |
| 5 | [claim text] | ➖ N/A | [reason] |

### Overall Assessment

**Verdict:** [Accurate / Inaccurate / Mixed]
**Summary:** [1-2 sentence summary of findings]

### Revised Response

[Only include this section if revisions were made. Present the corrected text.]
```

## Key Principles

- **Thoroughness over speed** — Verify every non-trivial claim, even if it requires multiple searches
- **Source authority matters** — Prefer official sources, academic references, and reputable publications
- **Minimal revision** — When correcting, change as little as possible to fix the issue
- **Transparency** — Always show your reasoning and sources
- **Honest uncertainty** — Use "Disputed" or "Unsupported" rather than guessing when evidence is ambiguous

## Attribution

Architecture and prompts adapted from Google's [LLM Auditor sample](https://github.com/google/adk-samples/tree/main/go/agents/llm-auditor) (Apache 2.0 License).
