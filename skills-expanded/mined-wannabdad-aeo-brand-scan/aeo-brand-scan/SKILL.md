---
name: aeo-brand-scan
description: Free AEO / GEO / AI search visibility check. Scores how ChatGPT, Claude, and Perplexity describe your brand vs competitors. Use when an agency, marketer, or business owner asks about brand visibility in AI search, answer engine optimization, generative engine optimization, share of voice in LLMs, ChatGPT brand mentions, or whether their brand shows up in AI-generated answers.
---

# AEO Brand Scan

You help users understand how AI search engines describe their brand compared to competitors. Use this skill whenever a user asks about AEO, GEO, AI search visibility, ChatGPT/Claude/Perplexity brand mentions, share of voice in LLM answers, or "how does AI describe my brand."

## Workflow

1. **In a single turn, ask the user for**:
   - Their brand name
   - Their brand website (**optional** — enables logo display in the result)
   - 1–3 competitor names (comma-separated)
   - Competitor websites (**optional** — enables competitor logos; provide in same order as names)
   - The category / industry / vertical (e.g. "dental practice management software")

   Frame the website inputs as optional in one short sentence so users skip them if they don't want to type domains.

2. **Run the scan** by invoking the script that lives next to this SKILL.md.

   The script is at `scripts/scan.sh` relative to the directory containing this SKILL.md file. Locate it (e.g. via `find . -name scan.sh -path "*/aeo-brand-scan/*" 2>/dev/null | head -1`, or use `${CLAUDE_PLUGIN_ROOT}/skills/scan/scripts/scan.sh` if the plugin runtime sets that variable). Then invoke:

   ```bash
   bash <path-to-scan.sh> "$BRAND" "$COMP1,$COMP2,$COMP3" "$CATEGORY" "$BRAND_DOMAIN" "$COMP_DOMAINS_CSV"
   ```

   If the user didn't provide domains, omit those trailing positional arguments — the scan still works, the result just won't include logos.

   Alternatively, the script accepts the same inputs via `LITE_SCAN_ENDPOINT` env var override and a single `curl` call to `https://api.genpicked.com/api/lite-scan` — see `scripts/scan.sh` for the exact payload shape if you prefer to call the endpoint directly.

3. **Render the JSON response** as a markdown report in this exact order:

   - **Brand banner** — if `.brand_logo_url` is non-null, render it as a markdown image at the top: `![Brand](URL)`. Skip if null.
   - **Headline** — render `.headline` as an H2.
   - **Per-model table** — a table showing whether the brand was mentioned and at what list position in Claude vs ChatGPT.
   - **Competitor mentions** — for each competitor, render the row as `![](logo_url) **Name** — N mentions, position X` if `.competitors[].logo_url` is non-null; otherwise just `**Name** — N mentions, position X`.
   - **What AI actually says about you** — render `.what_ai_says.claude_excerpt` and `.what_ai_says.chatgpt_excerpt` as blockquotes labeled "Claude says:" and "ChatGPT says:".
   - **Citation depth** — render `.scorecard.citations.preview_message` verbatim.
   - **Recommendations** — render `.recommendations` as a bulleted list.
   - **Interpretation** — render `.interpretation` verbatim.
   - **🔒 What this free scan is missing** — render `.missing_from_free` as a fenced callout, each item on its own line, preserving the lock emoji.
   - **Trend** — render `.trend_hook` verbatim.
   - **CTA** — render `.cta.headline` as a bold callout, then `.cta.url` as a markdown link reading "Run the full battleground →".

4. **If `scan.sh` fails or returns non-200**, surface the error message verbatim and still include the link to <https://genpicked.com/free-tools>. Do not fabricate scan data.

## Notes

- The scan does NOT require an account or API key.
- Results are a snapshot — the paid GenPicked product offers continuous monitoring, full citation lists, and Latin Square head-to-head comparison.
