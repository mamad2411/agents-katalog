---
name: research-crawl-email
description: Batched Gmail crawl from N sender addresses across N-day window; per-sender markdown to caller dir; rolled-up + per-source summary.
---

# Research Crawl Email

**Argument:** $ARGUMENTS (required, see Runtime Inputs)

If `$ARGUMENTS` is empty or missing required fields, STOP and report which fields are absent.

---

## Preamble

### Runtime Inputs

Parse from `$ARGUMENTS`:

```
--senders=[EMAIL1,EMAIL2,...]   [JSON-style array of exact RFC-5322 email addresses, non-empty; display names not supported. Singular invocation expressed as a single-element array.]
--raw-output-dir={PATH}          [absolute path to a directory where per-sender rendered markdown files will be written]

# Optional power params (omit when not needed):
--days={N}                       [positive integer time window in days; default 1]
--max-per-sender={N}             [per-sender message cap; default 10; truncates newest-first]
```

Validation rules (executed before §1.0):

- `--senders` and `--raw-output-dir` are mandatory. If either missing, STOP and report which is absent.
- `--senders` must parse as a JSON array of strings, non-empty. Reject otherwise (`senders-malformed`).
- Each entry in `--senders` must match RFC-5322 email shape (`<local>@<host>` with at least one `.` in host). First failing entry → STOP and report the offending value (`senders-malformed`).
- `--raw-output-dir` must be absolute. Reject relative paths (callers own path resolution).
- `--days` must parse as positive integer when supplied; default 1.
- `--max-per-sender` must parse as positive integer when supplied; default 10.

If any validation fails, STOP and report which field failed.

### Global References

```
GMAIL_SEARCH_TOOL  = mcp__claude_ai_Gmail__search_threads
GMAIL_GET_THREAD   = mcp__claude_ai_Gmail__get_thread
```

The leaf composes these two MCP tools directly in the caller's context. Both require harness permission approval on first use per context, any caller may hit the prompt on its first invocation per session; surface which tool needs approval and re-invoke after the user grants it.

### Caller Isolation

Pure primitive, no agent spawn, no pipeline agents, no telemetry. The skill runs the Gmail search + per-thread body fetch + render directly in the invoking context; the caller absorbs the Gmail thread context cost (full thread bodies land in the caller's window). Callers crawling many senders, or composing this leaf alongside other work, wrap the invocation in their own isolation:

```
Agent({subagent_type: "general-purpose", model: "sonnet", prompt: "Invoke /research-crawl-email with <args>"})
```

Consumer skills document their own isolation choice. The run-pulse composer wraps each source-type leaf in one classifier sub-agent per source-type.

---

## 1.0 Context Capture

### Step 1: Verify raw output directory parent exists

Check that the parent directory of `--raw-output-dir` exists. If not, route to §6.0 (`raw-output-parent-missing`). Do not create parent directories, caller owns path resolution. The `--raw-output-dir` itself MAY or MAY NOT exist; §3.0 Step 1 creates it via `mkdir -p` before writing the first per-sender file.

### Step 2: Compute `after:` boundary

Compute the Gmail query date boundary as `today - days` formatted as `YYYY/MM/DD`. Gmail interprets `after:` as start-of-day in the user's account timezone; ±1 day fuzz is acceptable for batched crawl use.

```
after_date = (today - days).strftime("YYYY/MM/DD")
window_start = (today - days).isoformat()  # YYYY-MM-DD for output frontmatter
window_end   = today.isoformat()
```

### Step 3: Construct batched Gmail query string

Build the batched query joining all senders with `OR`:

```
query_string = f"from:({s1} OR {s2} OR ... OR {sN}) after:{after_date}"
```

Single-element invocation collapses to `from:(s1) after:{after_date}`, Gmail parses both shapes identically. No mode flag needed.

---

## 2.0 Plan & Confirm

This skill runs autonomously, no user pause. Pure primitive; executes directly in the caller's context. Composed leaves never gate parallelization; direct invocations log the execution config and proceed.


State the planned execution config in one structured log statement, then proceed directly to §3.0:

```
## /research-crawl-email: executing crawl

senders:               {--senders}                       # N email addresses in caller-supplied order
raw_output_dir:        {--raw-output-dir}
days:                  {--days}                          # default 1
max_per_sender:        {--max-per-sender}                # default 10
query_string:          {query_string}                    # batched from:(...) after:...
execution:             direct (pure primitive, no sub-agent spawn)
```

---

## 3.0 Crawl

Execute the crawl directly, no sub-agent spawn. Search N email senders via the Gmail MCP server in a single batched search, fetch each matched thread's full body, group messages by sender, then write per-sender rendered markdown files into `--raw-output-dir`. This step writes raw bytes only, it does NOT extract, summarize, template-fill, classify by author, or filter beyond the per-sender message cap; the composing router or domain orchestrator handles all downstream transformation.

### Inputs (from §1.0)

```
Senders:               {--senders}                       # N email addresses in caller-supplied order
Raw output dir:        {--raw-output-dir}
Days:                  {--days}                          # time window
Max per sender:        {--max-per-sender}                # newest-first truncation cap
Query string:          {query_string}                    # pre-constructed
After date:            {after_date}                      # YYYY/MM/DD
Window start:          {window_start}                    # YYYY-MM-DD (for frontmatter)
Window end:            {window_end}                      # YYYY-MM-DD (for frontmatter)
```

### MCP Tools

```
Discovery:             mcp__claude_ai_Gmail__search_threads
Body fetch:            mcp__claude_ai_Gmail__get_thread
```

Both tools require one-time harness permission approval per context. If either call returns a permission-denial error, STOP and report which tool needs approval, the user grants it once and the skill re-invokes.

### Procedure

Execute these steps in order:

```
1. Ensure {--raw-output-dir} exists. Use Bash `mkdir -p {--raw-output-dir}`.

2. Phase 1, Discovery. Call search_threads with the pre-constructed query string and
   pageSize=50 (the documented max). Collect all (threadId, sender) pairs from the
   response.threads array. The response shape is:

     {
       threads: [{ id, messages: [{ sender, subject, date, snippet, ... }] }],
       nextPageToken: <string, optional, present when more results exist>
     }

   Zero-match returns `{}`, an empty object with no `threads` key. Treat as
   `response.get("threads", [])` returning an empty array; this is the expected
   shape for windows with no matches, not an error.

   If `nextPageToken` is present, loop with `pageToken=<token>` until exhausted.
   Cap the loop at 5 pages (250 threads), defensive cap against runaway batches.
   If the cap is hit, log a diagnostic and proceed with what was collected.

3. Phase 2, Per-thread body fetch. For each (threadId, sender) collected in Phase 1,
   call get_thread(threadId, messageFormat="FULL_CONTENT"). Extract each message in
   the returned `messages[]` array.

   Body source rule, primary + fallback:
   - PRIMARY: use `plaintextBody` when present and non-empty. Gmail-provided plain
     text is already clean prose; preserve verbatim.
   - FALLBACK: when `plaintextBody` is absent or empty, extract from `htmlBody` via
     tag-strip. Some senders (typically institutional newsletters) ship HTML-only
     messages with no `plaintextBody` field.
     Tag-strip rules:
       * Drop `<style>` and `<script>` blocks entirely (and their content).
       * Convert paragraph-break tags to newlines: `<p>`, `<br/>`, `<br>`, `</div>`,
         `</li>` → `\n`. `<li>` → `\n- `.
       * Convert `<a href="URL">label</a>` to `label (URL)`, preserve link target.
       * Strip all remaining HTML tags.
       * Collapse runs of whitespace (multiple spaces, tabs) to a single space;
         collapse runs of ≥3 newlines to 2 newlines.
       * Decode common HTML entities (`&amp;` → `&`, `&#39;` → `'`, `&nbsp;` → space,
         `&lt;` → `<`, `&gt;` → `>`, `&quot;` → `"`).
   - For each message extracted, track which path was used (`plaintext` or
     `html_fallback`). Count fallback occurrences per sender for step 6 diagnostic.

   Message shape from get_thread FULL_CONTENT:

     {
       date: <ISO 8601 UTC>,
       id: <message id>,
       sender: <exact email address>,
       subject: <string>,
       snippet: <~160 char excerpt>,
       plaintextBody: <Gmail-provided plain text, clean prose; primary source>,
       htmlBody: <raw HTML, fallback source when plaintextBody absent>,
       labelIds: [...],
       toRecipients: [...],
       attachment_ids: [...]   # populated when attachments present; OUT OF SCOPE for v1
     }

4. Group all messages by `message.sender` (exact string equality against the input
   --senders array). Build:

     groups = { sender1: [msg, msg, ...], sender2: [...], ..., senderN: [...] }

   Initialize the map keyed by ALL N input senders, senders that returned zero
   messages map to empty arrays. This guarantees one output file per input sender.

   For each sender's message array: sort by date descending (newest first), then
   truncate to {--max-per-sender}. Truncation is silent, newest messages preserved.

5. For each input sender, render its message array to a markdown file inside
   {--raw-output-dir}. Filename rule:

     filename = `sender-{slugified-email}.md`

   Slug rule: lowercase the email, replace `@` and `.` with `-`, strip any
   non-alphanumeric-or-hyphen characters. Examples:
   - `news@example.com` → `sender-news-example-com.md`
   - `digest@mail.acme-corp.com` → `sender-digest-mail-acme-corp-com.md`

   File structure per sender:

   ---
   type: Email Crawl Raw
   schema: ephemeral-raw-crawl
   source_tool: mcp__claude_ai_Gmail__search_threads+get_thread
   sender: {this sender's email}
   window_start: {window_start}
   window_end: {window_end}
   days: {--days}
   crawled_at: {ISO 8601 timestamp of this batch run}
   message_count: {N messages in this sender's group after truncation}
   input_params:
     max_per_sender: {--max-per-sender}
   ---

   # Emails, {sender email}

   ## Message 1, {YYYY-MM-DD}, {subject}

   Thread ID: {threadId}

   {plaintextBody, preserve original line breaks; Gmail already strips HTML;
    no further transformation}

   ---

   ## Message 2, {YYYY-MM-DD}, {subject}

   ...

   Rendering rules:
   - Each message is one H2 section separated by horizontal rules (`---`).
   - H2 heading: `Message N, YYYY-MM-DD, {subject}` (1-indexed, newest first).
   - Thread ID line immediately under H2 (one line, bare value).
   - Body is plaintextBody verbatim, preserve newlines, no HTML strip needed.

   When `message_count: 0` for a sender (no matches in window): body has
   frontmatter + H1 + single line `No messages returned for this sender in the
   configured window.` Per-sender `crawl_status: empty` (not failed, empty is
   valid for senders with no recent mail).

6. Build `per_source_outputs[]` array, one entry per input sender in caller order:

     per_source_outputs[i] = {
       sender:          {senders[i]},
       raw_output_path: {--raw-output-dir}/sender-{slug}.md,
       message_count:   {len(groups[senders[i]]) after truncation},
       char_count:      {wc -c on the rendered file},
       crawl_status:    {"clean" | "empty" | "failed"},  # per-sender
       diagnostic:      {one-line note when crawl_status == failed OR when ≥1
                         message used htmlBody fallback; otherwise omit},
     }

   Status semantics:
   - `clean`, sender returned ≥1 message; all get_thread fetches succeeded.
                 May still carry a diagnostic noting htmlBody-fallback count when
                 ≥1 message lacked plaintextBody.
   - `empty`, sender returned zero matches in window (Gmail `{}` response)
   - `failed`, one or more get_thread fetches failed mid-stream; file written
                 with partial body; diagnostic explains

   Diagnostic format for fallback notification (set when ≥1 fallback fired AND
   no fetch failure occurred):
     "N of M messages used htmlBody fallback (plaintextBody absent)"
   When both fallback and failure conditions hold, the failure cause dominates
   the diagnostic string; fallback count appears as a trailing clause:
     "<failure cause>; N of M messages used htmlBody fallback"

7. Compute aggregate fields:

     total_char_count     = sum(entry.char_count for entry in per_source_outputs)
     total_message_count  = sum(entry.message_count for entry in per_source_outputs)
     overall_crawl_status = (
       "clean"   if all entries have crawl_status in {clean, empty}
       else "failed"  if all entries have crawl_status == "failed"
       else "partial"
     )

   Note: `empty` entries do NOT degrade overall status to `partial`, an empty
   window is a clean operational outcome, not a failure. Only mixed clean+failed
   or all-failed produces `partial`/`failed` aggregate.

8. Read-back: list {--raw-output-dir} and confirm exactly N files exist (one per
   input sender). Mismatch → set overall_crawl_status = "failed" with diagnostic =
   "post-write reconciliation failed: expected N files, found M".
```

### Capture

After the read-back (step 8), capture the structured summary as `CRAWL_RETURN` and proceed to §4.0:

```
raw_output_dir:        {--raw-output-dir}
char_count:            <total across all per-sender files>
message_count:         <total across all per-sender message groups>
crawl_status:          <clean | partial | failed>           # aggregate
window_start:          {window_start}
window_end:            {window_end}
per_source_outputs:    [<one entry per input sender, see step 6>]
diagnostic:            <one-line note when crawl_status != clean; otherwise omit>
```

Do NOT surface raw markdown content or Gmail thread payloads to the caller, both are on disk at `{--raw-output-dir}` (rendered) or in Gmail itself (source of truth). §5.0 returns the reference plus summary only.

---

## 4.0 Verify

### Step 1: File-state verification

Verify the raw output directory and per-sender files:

- [ ] Directory exists at `--raw-output-dir` (use Bash: `test -d {DIR}`).
- [ ] One file per input sender exists at each `CRAWL_RETURN.per_source_outputs[i].raw_output_path`.
- [ ] When `entry.crawl_status == clean`: file is non-empty (`char_count > 200`). File-level frontmatter alone exceeds 200 bytes, so any clean entry must have `char_count > 200`.
- [ ] When `entry.crawl_status == empty`: file is a placeholder with `char_count > 0` (frontmatter + empty-window line).
- [ ] When `entry.crawl_status == failed`: file is present with `char_count > 0` (partial body + diagnostic).

If any check fails (entry status `clean` but file empty/missing, file count ≠ N input senders), route to §6.0 (`agent-write-mismatch`).

---

## 5.0 Summary

Return this structured summary to the caller (typically the `/run-pulse` composer):

```
raw_output_dir:        {--raw-output-dir}
char_count:            {CRAWL_RETURN.char_count}            # aggregate
message_count:         {CRAWL_RETURN.message_count}         # aggregate
crawl_status:          {CRAWL_RETURN.crawl_status}          # clean | partial | failed
window_start:          {CRAWL_RETURN.window_start}
window_end:            {CRAWL_RETURN.window_end}
per_source_outputs:    {CRAWL_RETURN.per_source_outputs[]}
  # Each entry: { sender, raw_output_path, message_count, char_count,
  #              crawl_status (clean|empty|failed per-sender), diagnostic? }
diagnostic:            {CRAWL_RETURN.diagnostic if present}
```

Caller decides next action based on overall `crawl_status` (short-circuit on `failed`; proceed with extraction iteration on `clean` or `partial`) and per-sender `crawl_status` (skip extraction on entries with `crawl_status == failed`; treat `empty` as no-content-this-cycle). The leaf does not retry, the caller governs retry policy.

---

## 6.0 Error Handling

| Error | Response |
|---|---|
| `--senders` or `--raw-output-dir` missing from `$ARGUMENTS` | STOP. Report which field is absent. |
| `senders-malformed`, `--senders` does not parse as JSON array, OR array is empty, OR any entry fails RFC-5322 email shape | STOP. Report the malformed value (the offending entry when per-entry). Display names are explicitly rejected, caller must resolve display name → email before invocation. |
| `--raw-output-dir` not absolute | STOP. Report the relative path; caller must resolve. |
| `--days` or `--max-per-sender` does not parse as positive integer | STOP. Report the malformed value. |
| `raw-output-parent-missing`, parent directory of `--raw-output-dir` does not exist | STOP. Report the missing parent path. Do not create, caller scaffolds the directory tree before invocation. The `--raw-output-dir` itself MAY or MAY NOT pre-exist; §3.0 Step 1 creates it. |
| Permission-denied on `search_threads` or `get_thread` | Surface which tool needs approval. Resume requires the user to approve the harness permission prompt then re-invoke. One-time per context per session. |
| Crawl produces overall `crawl_status: failed` (Phase 1 search failed entirely, or all Phase 2 fetches failed) | Proceed to §5.0 with the failure summary. Return to caller with overall `crawl_status: failed` + diagnostic + per-sender entries all marked failed. Caller decides retry / drop. Do not retry within this skill. |
| Crawl produces overall `crawl_status: partial` (some per-sender entries succeeded, others failed) | Proceed to §5.0 normally. Return surfaces overall `partial` + per-sender detail in `per_source_outputs[]`. Caller iterates the array, drops failed entries from downstream extraction, continues with clean entries. |
| Crawl produces `crawl_status: empty` for one or more entries | Proceed normally. Per-sender entry surfaces `message_count: 0` (valid empty-window result for senders with no recent mail). Empty does NOT degrade aggregate status. |
| Sender ships only `htmlBody` (no `plaintextBody` field) | Apply tag-strip fallback per §3.0 step 3 body source rule. Per-sender entry stays `crawl_status: clean`; diagnostic surfaces the fallback count (`N of M messages used htmlBody fallback`). Observed with some institutional-newsletter senders. Not an error; not a degraded status. |
| The render produces a malformed structured summary (missing fields, wrong shape, `per_source_outputs[]` length ≠ N input senders) | List `--raw-output-dir` directly to recover actual file count. Build a degraded summary from `wc -c` per file + heuristic status detection (empty body → empty, non-empty → clean). Surface the malformed summary in a diagnostic line. |
| `agent-write-mismatch`, the render reports an entry's `crawl_status: clean` but file is empty/missing, OR file count in `--raw-output-dir` ≠ N input senders | Surface the mismatch in the return diagnostic. Set affected entry's `crawl_status: failed`; recompute overall status. The file-state on disk is authoritative. |
| Phase 1 pagination loop hits 5-page (250-thread) defensive cap | Note the cap was reached and proceed with collected threads. Aggregate `crawl_status: partial` because the result is known-incomplete. Caller adjusts `--days` or `--max-per-sender` downward, or accepts partial coverage. |
| `nextPageToken` loop fails to advance (same token returned twice) | Treat as Gmail-side pagination bug; log the diagnostic and break the loop with collected results. Aggregate `crawl_status: partial`. |
