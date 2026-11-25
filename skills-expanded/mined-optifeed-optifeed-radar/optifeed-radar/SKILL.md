---
name: optifeed-radar
description: Measure whether the models behind ChatGPT, Perplexity, Gemini, or Claude recommend a brand or specific named products, audit a site's AI-readiness, generate buyer questions, inspect cited sources, or compare saved AI-visibility runs. Use for AI visibility, GEO, AEO, AI-SEO, brand recommendation, product recommendation, competitor share-of-voice, and readiness-audit requests. Run Optifeed Radar locally through its CLI or MCP server. The readiness audit uses no API keys or AI calls; visibility and product checks use the user's own provider keys and spend their API credit.
---

# Optifeed Radar

Use Optifeed Radar to collect inspectable, point-in-time evidence about what AI
engines recommend. Keep readiness findings separate from recommendation
visibility: they answer different questions and have different scores.

## Choose a surface

- Prefer the Optifeed Radar MCP tools when they are available in the current AI
  agent. They return structured output and apply non-interactive cost caps.
- Otherwise run `npx optifeed-radar <command>` with Node 20 or newer.
- From an Optifeed Radar source clone, run
  `npx tsx src/cli/index.ts <command>` instead.

## Follow the workflow

1. Normalize the target to a bare hostname such as `example.com`. Do not pass a
   path, query string, credentials, or an unrelated URL.
2. Start with the free audit unless the user asks only for a paid visibility
   run. Use `audit_store` over MCP or `npx optifeed-radar audit <domain>`. Report
   the AI-readiness score as readiness, not as the AI Visibility Score.
3. Decide what evidence the user needs:
   - Use a brand check to test whether unbranded buyer questions surface the
     brand and to measure position and competitor share of voice.
   - Generate the buyer-query pack first when the user wants to review or edit
     the sample before a full run. Query generation uses a small number of API
     calls.
   - Use a product check only for products the user explicitly names.
   - Use saved-run diff or sources commands when no new engine calls are needed.
4. Before spending API credit, inspect the available engines with
   `npx optifeed-radar config` when using the CLI. Get explicit approval for the
   engines, mode, and maximum cost unless the user's request already specifies
   all three. Never expose, print, or persist key values.
5. Default a first paid brand check to quick mode, the requested engines, and a
   conservative `--max-cost`. Add `--yes` only after approval so an AI agent can
   run the CLI unattended. Treat the cap as a strong bound, not a guaranteed
   exact ceiling: one in-flight call per engine can finish after the cap is
   reached, and Radar reports any overshoot.
6. Present the score with its sampling context, engine coverage, actual spend,
   skipped engines, grounded versus parametric split, and partial or capped
   status. Link conclusions to the raw answers or cited sources in the output.
7. Describe a single run as a dated estimate. Use at least two saved runs before
   claiming movement, and disclose when prompt or engine sets changed.

## Map requests to commands and tools

| Intent                           | CLI                                   | MCP                         |
| -------------------------------- | ------------------------------------- | --------------------------- |
| Free site readiness              | `audit <domain>`                      | `audit_store`               |
| Brand recommendation visibility  | `check <domain>`                      | `check_visibility`          |
| Review buyer questions           | `queries <domain>`                    | `generate_buyer_queries`    |
| Named-product visibility         | `shopping <domain> --products "A, B"` | `shopping_check`            |
| Change between saved runs        | `diff <domain>`                       | `get_snapshot_diff`         |
| Cited domains and share of voice | `sources <domain>`                    | Read the saved check output |
| Key and state status             | `config`                              | Not exposed                 |

Useful brand-check flags include `--quick`, `--engines openai,perplexity`,
`--grounded`, `--max-cost 0.50`, `--json`, `--report report.html`,
`--fail-under 50`, and `--yes`. The MCP brand check accepts `domain`, optional
`engines`, `quick`, and `max_cost`; it defaults to a $0.50 cap.

## Handle products carefully

- Ask for the product list; do not infer or import it. Radar checks at most 10
  named products per run.
- Treat input order as a stable tie-break only, never as the merchant's ranking.
- Add a descriptor for an opaque name, such as `Aria 2: quiet home espresso
machine`, so product questions target the right category.
- Start with two or three products and a maximum cost. The MCP product check
  defaults to $0.20 per product.
- Explain that each product is tested on its own shelf. Product scores do not
  mean one listed product directly beat another.

For richer CLI input, use a YAML file:

```yaml
products:
  - name: Aria 2
    aliases: [Aria II]
    descriptor: quiet home espresso machine
  - name: Presto X
    descriptor: fast dual-boiler espresso machine
```

Then run:

```bash
npx optifeed-radar shopping example.com \
  --products-file products.yml \
  --max-cost 0.50 \
  --yes
```

## Configure provider access

Set at least one of `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, or
`PERPLEXITY_API_KEY` for buyer-query generation, brand checks, or product
checks. Put keys in the calling process environment or a `.env` file in the
working directory. Exported values take precedence. The free audit needs none.

Radar runs locally and has no Optifeed-hosted backend. Each provider key is sent
only to its matching provider. Do not paste keys into a prompt, command output,
report, snapshot, or source file.

## Keep conclusions honest

- Treat scores as estimates from generated buyer questions, not panel data or a
  guaranteed ranking. AI engine answers vary between runs.
- Distinguish actual retrieval from requested grounded mode. A model can decline
  to search, and Radar reports retrieval answer by answer.
- State that provider APIs can differ from consumer chat interfaces.
- Do not claim continuous monitoring; Radar performs point-in-time checks.
- Do not claim catalog discovery or product-feed linting. Those capabilities are
  on the roadmap and waitlist at optifeed.com.
- A non-zero exit from `check` means the run measured nothing, not that the
  brand scored badly. All buyer prompts come from one judge call, so a failure
  there - no API credit, a rate limit, an unusable response - leaves nothing to
  ask and the run stops before querying engines. The reason is printed; report
  it and stop. Never present an unmeasured run as a low or zero visibility
  result. Declining the cost prompt also aborts, but exits zero.

Measured July 2026, a quick brand check cost about $0.09 on one engine,
$0.41-$0.46 across four parametric engines, and $0.85-$1.09 across four with
grounding. A measured two-product, four-engine grounded shopping run cost
$0.70. Those figures predate the August 2026 switch of the OpenAI engine to a
pinned reasoning model, whose reasoning tokens bill as output: measured
2026-08-13, a quick check on OpenAI alone cost $0.2297, roughly double that
engine's earlier share. Provider prices and model behavior change, so use all
of these only as dated planning ranges and rely on Radar's current estimate and
actual-spend report.

More at optifeed.com
