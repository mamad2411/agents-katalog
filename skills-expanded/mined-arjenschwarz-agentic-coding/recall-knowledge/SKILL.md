---
name: recall-knowledge
description: Search the user's Obsidian vault for cross-project technical knowledge previously captured by the /capture-knowledge skill, and apply what's there to the current task. Use this PROACTIVELY at the start of any non-trivial work in a framework, language, or domain the user has touched before — the vault may already hold the gotcha you're about to rediscover. Trigger on explicit asks like "check my vault", "do I have notes on X", "search my knowledge", "what did I write about Y", "recall how I did Z", "look that up in my notes". Examples that should trigger: "do we have anything about embedding MCP servers in Swift apps?", "search my vault for Go pagination patterns", "what did I learn about SwiftData rollback?", "I'm about to wire up CloudKit sync — anything saved about that?". Also use BEFORE diving into integration recipes, SDK wiring, platform quirks, build-system glue, or language-specific gotchas (Swift actor isolation, Go generics, SwiftData, MCP, CloudKit, GraphQL pagination, App Intents, Hummingbird, NWPathMonitor, etc.) — a quick vault check beats reinventing a wheel the user already documented. Do NOT use for questions answerable from the current repo alone (read the repo instead), questions whose answer doesn't depend on the user's prior project work (general programming knowledge, language syntax, public API references), or queries about user preferences (those live in memory / CLAUDE.md, not the vault).
---

# Recall captured knowledge

This skill searches the user's Obsidian vault for notes previously written by the [[capture-knowledge]] skill and feeds the relevant ones back into the current task. It is the lookup half of the capture/recall pair — same vault, same folder, same `tags: [generated, ...]` filter, opposite direction.

The whole point: when the user has already solved a problem on another project and written it down, you should use that prior work instead of starting from scratch. Capture wrote it so future-you could find it; this skill makes future-you actually look.

## Resolving the vault path

The vault path lives in the same per-machine cache `capture-knowledge` uses, so the two skills always agree:

```
~/.config/capture-knowledge/config.json
{
  "vault_path": "/Users/arjen/Documents/Obsidian/Main"
}
```

Resolution order (stop at the first that yields a usable directory):

1. **Read the cache.**

   ```bash
   VAULT_PATH=$(python3 -c "import json,os; p=os.path.expanduser('~/.config/capture-knowledge/config.json'); print(json.load(open(p))['vault_path']) if os.path.exists(p) else None" 2>/dev/null)
   [ -d "$VAULT_PATH" ] || VAULT_PATH=""
   ```

2. **Try the Obsidian CLI** (only useful if Obsidian is running): `obsidian vaults verbose | awk -F'\t' '$1=="Main"{print $2}'`. If it returns an existing directory, ask the user to confirm and write the cache.

3. **Ask the user** for the absolute path, validate it exists, and write the cache.

If the cache exists but the directory is missing, treat it as uncached and re-run resolution. Do not silently fail — say so and ask.

## Where to look

Default scope is the folder `capture-knowledge` writes to:

```
<VAULT_PATH>/03-Notes/Generated/
```

That folder is the canonical home for generated knowledge notes. Every file there has `tags: [generated, ...]` in frontmatter, so you don't need to filter further by default — the folder *is* the filter.

Widen scope only if:

- The user explicitly says "search my whole vault" or names a different folder.
- The default scope returns nothing and the topic is plausibly something the user wrote by hand elsewhere. Then try `<VAULT_PATH>/03-Notes/` more broadly, and tell the user you're widening.

Hand-written notes outside `Generated/` follow different conventions (no guaranteed frontmatter, no `generated` tag), so don't assume the same structure.

## Searching

Keep this fast and dumb — the Generated folder is small and grep over it is cheap. There's no index; rebuild a ranked list each call.

### Build the query

From the current task context, pull 2–5 keywords or short phrases the user would have used in a *note title or tag*, not literal code identifiers. Think the way the title is phrased: `How to embed an MCP server inside a native Swift app` — the searchable terms are `mcp`, `swift`, `embed`, `server`, not the names of the Swift classes you're staring at right now.

If the user gave you the query verbatim ("do I have notes on X"), use X directly. If you're triggering proactively, derive keywords from the task: framework name, platform, the verb of what you're about to do.

### Rank by where the match lives

Score matches roughly:

1. **Frontmatter topic tag match** — strongest signal. The user picked these tags so the note would be findable; treat a tag hit as near-certain relevance.
2. **Filename / H1 title match** — strong. Titles are phrased as questions the user would ask.
3. **Body match** — weakest. Useful for catching notes where the topic is mentioned but isn't the primary subject. De-prioritise unless tag and title searches return nothing.

Use ripgrep (or `grep -r`) — both are fine. Sketch:

```bash
# Tag match (tags sit in a YAML list, prefixed by "  - " inside the frontmatter)
rg -l --no-heading -i "^\s*-\s+<keyword>\s*$" "${VAULT_PATH}/03-Notes/Generated/" 2>/dev/null

# Filename match
ls "${VAULT_PATH}/03-Notes/Generated/" | rg -i "<keyword>"

# Body match (excluding frontmatter would be cleaner, but the noise is tolerable at this scale)
rg -l --no-heading -i "<keyword>" "${VAULT_PATH}/03-Notes/Generated/" 2>/dev/null
```

Run these in parallel as separate tool calls when you have multiple keywords — don't string them together serially.

### Take the top few

Dedupe across the three searches, keep the strongest 3–5 hits, and read each. Don't read every match — at this scale grep returns short lists, and over-reading just burns context.

If nothing matches, say so plainly and proceed without it. A vault miss is normal; don't keep widening the search until you find *something* tangentially related, because false positives are worse than nothing.

### When Obsidian is running

If the `obsidian` CLI is available and Obsidian is running, `obsidian search query="<term>" vault=Main` gives ranked full-text results. It's nicer than grep for fuzzy matches but requires Obsidian to be open, so it's a bonus path, not the default. Don't try to start Obsidian on the user's behalf — fall back to grep.

## Reading and applying

Once you have a shortlist, read the notes the way you'd read documentation: pull out the parts that apply to the *current* task, not the full body.

Notes are written to be project-agnostic (that's a rule in `capture-knowledge`), so the example code uses placeholder names. Translate those onto the actual identifiers in the current repo as you apply the pattern.

If the note has a `source-project` in frontmatter and you can see that repo on disk, it's often worth glancing at the original implementation for context — the note is the distilled pattern, the source repo has the real working code.

## Reporting back

In the user-facing message, be brief:

- If you found something: name the note(s) (title plus absolute path so the user can click through), one short line about what each contains, and then apply the knowledge to the task. Don't paste the full note back — the user can open it.
- If you found nothing: one sentence saying so, then carry on with the task.

Example:

> Found two relevant notes:
> - `How to embed an MCP server inside a native Swift app.md` — covers the Hummingbird + JSON-RPC pattern and actor-isolation gotchas
> - `How to build CLI-friendly App Intents that take a JSON blob.md` — App Intents wiring, less directly relevant
>
> Applying the MCP note to the current task: …

## When to suggest capturing too

If during the recall you notice the user has *no* note on something they're about to learn the hard way, that's a natural moment to offer [[capture-knowledge]] at the end of the task. Don't push it during the recall step — finish the work first, then offer.

## Workflow

1. **Resolve `VAULT_PATH`** via the cache flow above. Reuse the same cache `capture-knowledge` writes.
2. **Build the keyword list** from the user's request or the current task context.
3. **Run tag / filename / body searches** in parallel against `<VAULT_PATH>/03-Notes/Generated/`. Rank by where the match landed.
4. **Read the top 3–5 hits.** Skip body-only matches if tag/title hits already cover the topic.
5. **Apply what's relevant** to the current task. Translate the note's placeholder identifiers onto the real ones in this repo.
6. **Tell the user** which notes you used (titles + paths), in one short message, and proceed with the work.
7. If nothing relevant exists, say so and proceed without it.

## Things to avoid

- **Searching outside `03-Notes/Generated/` by default.** That's where `capture-knowledge` puts notes; other vault folders use different conventions.
- **Reading every match.** Rank first, read few. Short shortlists beat exhaustive ones.
- **Padding the response with the full text of the notes.** Cite the path; the user can open it.
- **Forcing a match.** If the vault has nothing, say nothing and proceed. False positives waste more time than admitting a miss.
- **Hardcoded vault paths.** Always resolve at runtime — different machines store the vault differently.
- **Starting Obsidian to use its CLI search.** If it's not running, grep is fine.
- **Skipping this skill on familiar-sounding topics.** The whole reason the user captured these notes is that the gotchas *aren't* obvious. If the topic plausibly matches a note, check.
