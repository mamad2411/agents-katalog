---
name: google-ai-mode
description: Web research through Google AI Mode (the google-ai-mode MCP server) — one call returns Google's AI answer synthesized from many sources, with citations and follow-ups in the same conversation. Use for any question that needs current information from the web: latest versions and release notes, news, prices, docs and APIs, how-to commands, comparisons, facts to verify, multi-step research. Prefer it over reading search results page by page; trigger words — найди, погугли, поищи, что нового, какая последняя версия, сколько стоит, сравни, search, google, look up, latest.
---

# Google AI Mode search

The `google-ai-mode` MCP server asks Google AI Mode in the user's own browser (their Google account) and returns the answer as Markdown with source links.

AI Mode splits a question into subtopics and searches them in parallel ("query fan-out"), then writes one answer. So one call already does what a researcher would do with several keyword searches: ask it **full questions**, not keyword strings.

## Tools

| Goal | Tool | Notes |
|---|---|---|
| One question | `search(query)` | Answer + `citations` + `thread_id` |
| Several independent questions | `search_many(queries=[...])` | Up to 10 in parallel; about the time of one search |
| Dig deeper into the same topic | `follow_up(query, thread_id)` | Keeps the conversation context; 1–3 follow-ups, then start a new search |
| Local prices, availability, news | `search(query, gl="us")` | `gl` = country; without it results follow the user's location |
| Check the setup | `health()` | Server and browser-extension status |

Leave `mode` at its default. In tests `mode="fast"` was no faster on simple facts and dropped the sources.

## Writing the query

1. **One complete, neutral question.**
   - Name the subject without ambiguity, with version, OS, units or year where they matter.
   - Do not lead: "is X good?" and "is X bad?" get different answers, because AI Mode follows the framing.
   - Ask in the language you want the answer in.
2. **Ask for the source you would trust, inside the question.** Examples:
   - "Cite the official PostgreSQL documentation."
   - "Cite primary sources such as NIST."
   - "Give sources from nobelprize.org."

   Without this, simple facts often come back with blog sources or none. With it, the same questions cited NIST, docs.python.org, postgresql.org and nobelprize.org.
3. **Put constraints in words, not operators.**
   - "Answer only from postgresql.org documentation", "news from October 2026".
   - `site:`, `after:`, quotes and `-` are treated as hints, not filters: with `site:` other domains still appear.
4. **Say what shape the answer should take.**
   - "Give the command and a one-line explanation", "answer in 2–3 sentences", "list the top 5".
   - Add "no follow-up offers" to drop the closing "Would you like…" paragraph.
5. **Multi-step questions:** ask it to "state the intermediate facts with sources, then the answer" and to "show the calculation". This makes every hop checkable.

## Query templates

| Task | Template |
|---|---|
| Fact, number, date | `<question>? Cite <official/primary source>. Answer in 2–3 sentences, no follow-up offers.` |
| Command or how-to | `<goal> on <OS/tool + version>? Give the command and a one-line explanation, with the official <tool> documentation as the source; no follow-up offers.` |
| Error | `<exact error text> in <tool + version> on <OS>: what causes it and how to fix it? Cite the issue tracker or official docs.` |
| Compare or choose | `Compare <A> and <B> for <use case> by <criteria>; list the top <N> with sources, as of <month year>.` |
| Fresh information | `What changed in <subject> in <month year>? Cite official release notes or announcements.` |
| Multi-step | `<question>? State the intermediate facts with sources, then the answer; show the calculation.` |

Example: `How do I undo the last git commit but keep its changes staged? Give the command and a one-line explanation with the official git documentation as the source; no follow-up offers.`

## Checking an answer

- **Numbers and versions.** For anything you will act on, open the cited primary page.
- **Critical claims.** Ask a second, differently framed version or the counter-question in a new `search`, then compare. If they disagree, use `follow_up` to ask which source, version, date or region explains the difference.
- **No sources, or only blogs.** Use `follow_up`: "Which official sources confirm this?" Or re-ask with the source named in the question.
- **Refusal.** AI Mode sometimes answers only "can't answer this search" (in Russian: «Не удается дать ответ…»). Rephrase as the underlying question, without meta wording like "official prompt guide of <brand>".
- **Wrong subject or close but not the same.** If the answer is about a different year, product or company, rephrase with the exact name and version. Do not accept it as the answer.

## Research (several sources, a report)

1. **Split the task into 3–6 independent questions.** Cover:
   - the core facts;
   - the official or primary sources;
   - recent changes;
   - alternatives and criticism;
   - limits and failure modes.

   Write each one by the rules above and send them together with `search_many`.
2. **Fill gaps with `follow_up`** on the thread that has them.
3. **Confirm each key claim** with 2+ independent sources, at least one primary. Mark claims that rest on a single source.
4. **Report claims with their sources.** Report conflicts with their cause (version, date, region, plan), and what could not be found.

For a large report, use the `deep-research` skill and let its researchers search with this server.

## Errors

Every error comes with a `hint`. The common ones:

- `google_captcha` — ask the user to open Google in the browser and solve the CAPTCHA, then retry.
- `Extension not connected` / timeout — the browser with the extension must be running; ask the user to open Chrome.
- `Thread expired` — start a new `search`; threads live 30 minutes.
- `quota_exhausted_all_accounts` — retry later.

Do not fall back silently to other search tools when this server fails: report the error and its hint to the user.
