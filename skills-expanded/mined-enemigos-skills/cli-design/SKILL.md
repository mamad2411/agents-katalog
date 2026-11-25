---
name: cli-design
description: "Design and review command-line interfaces. Use for command grammar, options, help, prompts, output, JSON contracts, errors, safety, async behavior, or CLI compatibility."
---

Design the capability before the syntax. For an existing CLI, inspect its current help, parser, output, tests, and documented behavior first. Preserve shipped contracts unless the user asked for a redesign. For a review, test real behavior and report concrete user consequences rather than taste.

Apply the sections relevant to the task. Project requirements and established conventions outrank these defaults.

## Establish the command contract

Define each capability by its inputs, permissions, target, effects, result, failures, and recovery. Design first use, empty results, long work, failure, cancellation, and recovery alongside success.

Every command answers four questions:

1. What will it act on?
2. What will change?
3. What happened: completed, accepted, unchanged, partial, canceled, or failed?
4. What exact command or action comes next, when one exists?

Keep these invariants:

- Help works before authentication, configuration, or network access, and does no work.
- Explicit invalid input fails. It never falls back, fuzzy-matches a mutation target, or creates a similarly named resource.
- Complete explicit input behaves the same with and without a terminal. Missing input fails fast in non-interactive mode.
- Validation and required consent finish before the first durable effect.
- stdout holds only the requested result. Diagnostics stay on stderr.
- Report only confirmed states. Accepted work is not complete, local cancellation is not remote cancellation, and a failed read is not an empty result.
- Retries, waits, cleanup, and collection reads are bounded. A retry never duplicates an unsafe mutation.
- Every outcome has a stable ID, receipt, inspect command, or structured result that can verify it.

## Shape the command surface

Use one grammar consistently. A good default is:

```text
<cli> <group> [<subgroup>]... <action> [<resource>] [options]
```

- Name groups with nouns and actions with verbs. Put the resource after the action.
- Reserve top-level verbs for primary workflows on the current directory, session, or machine. Give the single dominant workflow a short path.
- Make only the obvious primary resource positional. Use named options for other resources and context.
- Keep command names, API field names, JSON keys, and configuration keys as separate contracts. Consistency in one does not justify renaming another.
- Teach one canonical name in help and examples. Shortcuts and aliases share its behavior. Deprecated aliases warn and name the replacement.
- Reject unknown commands, options, and extra positionals before work. Offer at most one close suggestion, then the relevant help command.

Choose verbs for their actual consequences. Reuse the verb in prompts, receipts, and structured outcomes.

| Verb | Meaning |
| --- | --- |
| `list` | Read a collection |
| `inspect` | Read one resource in detail |
| `create` | Make a standalone resource with its own lifecycle |
| `add` | Add an existing thing to a container or an entry to a configuration |
| `update` | Change specified fields while omitted fields stay unchanged |
| `set` | Assign a named slot, creating or replacing its value |
| `delete` | Destroy a resource and its data |
| `remove` | Remove a member or configuration entry without destroying the referenced thing |
| `connect` / `disconnect` | Attach or sever a connection while leaving external data in place |
| `revoke` | Invalidate credentials or access while retaining their history |
| `rotate` | Issue a replacement credential and invalidate the old one |
| `empty` | Delete every item while retaining the container |
| `cancel` | Abort an in-flight or scheduled operation |
| `stop` / `start` | Halt a resource so it can be started again, then start it |

Do not soften or overstate consequences. Issuing a credential is a mutation even when it returns one value.

### Resolve targets exactly

- Document each selector's accepted forms, uniqueness scope, and case sensitivity.
- Accept a name and ID through one selector only when they cannot collide. Split them when they can.
- Resolve exactly among resources the caller can access. Never mutate a first match, fuzzy match, or ID prefix.
- Persist stable IDs when later operations must address the same instance. Keep names for display.
- Show inferred context before consequential work. Ambiguous context is an error with candidates, not a choice made by the CLI.

### Standardize options and settings

Use named options from shared command metadata. Do not scan argv piecemeal.

- Support `--name value`, `--name=value`, declared short forms, and `--` to end option parsing.
- Accept only full names and declared aliases. Unique prefixes are not stable contracts.
- Use lowercase kebab-case for long options. Render positionals as `<required>` and `[optional]`.
- Define every Boolean's negation, every repeated option's behavior, every empty value's meaning, and every conflict.
- Give a short option one meaning and value type across the CLI. Reserve short forms for frequent, low-risk inputs.
- Keep `--force`, `--dry-run`, and other safety-changing options long.
- Validate identifiers strictly. Pass free-form text intact and encode it only at its destination.

Reuse these names when the concept exists:

| Concept | Option |
| --- | --- |
| Help and version | `-h, --help`, `-v, --version` |
| Machine output | `--json` |
| Field selection | `--fields <FIELDS>` |
| Interaction and consent | `--non-interactive`, `-y, --yes` |
| Replacement and preview | `--force`, `--dry-run` |
| Diagnostics and presentation | `--debug`, `--no-color` |
| Working directory and file output | `--cwd <DIR>`, `-o, --output <PATH>` |
| Payload input | `--file <FILE>`, `--value <VALUE>`, `--data <JSON>` |
| Result size and continuation | `-n, --limit <NUMBER>`, `--next <CURSOR>`, `--all` |
| Search and follow | `-q, --query <TEXT>`, `-f, --follow` |
| Waiting | `--wait`, `--no-wait`, `--timeout <DURATION>` |

`-` means stdin or stdout only for file-shaped inputs and outputs. Only one input may own stdin. Do not overload `--json` as JSON input.

Resolve settings highest first: explicit option, environment variable, project configuration, user configuration, built-in default. An invalid explicit value fails rather than falling through to another source. Document each environment variable's precedence, empty-value behavior, and persistence.

### Make help executable

- Generate human help, completion, and machine-readable command metadata from the same source.
- Keep help offline, side-effect free, and identical across `--help`, `-h`, and `help <path>` entry points.
- Put usage and a one-line imperative summary first. Then list commands, arguments, options, global options, verified examples, and material notes, omitting empty sections.
- Show defaults, accepted values, side effects, stream behavior, pagination, and waiting where they affect use.
- Test every example through the parser without executing mutations. Use canonical names and long options.
- Print suggested commands one per line with no shell prompt or Markdown. Preserve safe supplied context and quote for the destination shell. Suggestions never contain secrets.
- When agents are users, expose command metadata and guaranteed result fields through machine-readable help or a schema command.

## Resolve modes and consent independently

Resolve four settings through shared helpers:

| Setting | Values | Rule |
| --- | --- | --- |
| Interaction | Interactive or non-interactive | Non-interactive for `--non-interactive`, resolved JSON format, CI, payload stdin, or no usable prompt terminal |
| Format | Human or machine | Human by default, JSON with `--json`, or an intentional non-TTY JSON contract |
| Presentation | Rich or plain | Resolved per output stream from terminal capabilities and color preferences |
| Consent | Ask or granted | Granted by `--yes` only within the command's consequence tier |

For a new general CLI, redirection changes presentation, not format. An agent-first CLI may deliberately default to JSON on non-TTY stdout, and an existing CLI must preserve its published policy. Choose one CLI-wide rule in shared mode resolution rather than inferring it per command. Redirection never grants consent. It suppresses prompts only when the resolved format is JSON or another non-interactive signal applies. Stdin used as payload cannot also answer prompts. Non-interactive runs keep results, warnings, and recovery but remove prompts, spinners, and redraws. Missing input fails with the option, argument, or stdin equivalent needed to proceed.

### Prompt for real choices

- Prompt only for data that cannot be inferred, a real choice, required confirmation, or an optional offer after a successful interactive result.
- Render prompts on stderr. Ask one brief question at a time. Mask secret input.
- Give prompts non-interactive equivalents, except required personal acts such as legal acceptance. Explain the human workflow instead of hanging. Never repeat expressed intent.
- Show resolved context before the decision. Defaults must be valid and marked.
- Make cancellation and going back explicit. Preserve earlier answers when going back.
- Summarize a multi-step flow before its first mutation. After success, show an equivalent non-interactive command without embedding secret answers.
- Declining an optional offer after a result preserves that result and its exit code.
- Provide a plain accessible mode with numbered choices, status lines instead of animation, and no required arrow keys or redraws.

### Size consent to the damage

| Tier | Examples | Interactive | Non-interactive |
| --- | --- | --- | --- |
| Ordinary | Explicit, reversible, narrow writes | Run without confirmation | Run |
| Destructive | Data loss, access changes, purchases, bulk effects, ownership changes | Preview exact effects, default to No | Require `--yes` |
| Severe | Irreversible loss of a major resource or all of its data | Preview, then type the exact target name | Require `--yes` and an explicit target and context |

Before any charge, show the total and currency, known taxes or usage-based parts, charge timing, payment method, renewal, cancellation, and refund terms. Non-interactive charges require explicit approval and the selected amount or rate. A changed quote needs fresh consent. Never retry a charge without idempotency.

- Preview the exact target and each material downstream effect. State clearly when something cannot be undone.
- `--yes` answers confirmations only. It supplies no missing data, resolves no ambiguity, overrides no permission, and cannot grant required personal legal acceptance.
- `--force` permits a documented replacement or rerun. It is not blanket consent for bulk or severe effects.
- Bind consent to the final resolved target and effects. If either changes, require fresh consent.
- Before committing, compare provider previews with the approved target, amount, currency, and effects. Reject mismatches.
- Consequential mutations should support truthful `--dry-run`: real reads and validation, no mutation or prompts, and outcome `planned`.
- Skip confirmation for ordinary writes. Confirmation fatigue weakens the prompts that matter.
- Open browsers only in interactive local sessions. Always print the URL, honor `--no-open`, and never open one in non-interactive mode.

## Give each output stream one job

- stdout carries the answer: query data, a stable mutation identifier, a requested value, exact file bytes, or a machine document.
- stderr carries context, receipts, progress, prompts, warnings, errors, and next steps.
- Never interleave animation or diagnostics with stdout. Raw API responses, byte streams, and inherited child-process output keep their own protocols instead of being wrapped.

### Human output

- Design human output to answer the user's question, not dump the API response. Let options widen it.
- Lead the final result with the actual outcome and primary destination, followed by supporting facts and at most one useful next step.
- Include in each table row the identifier accepted by the next command. Use a stable, documented order.
- Promote repeated columns into headings. Group by reader action, not backend taxonomy.
- Make metric direction explicit and test counterintuitive calculations in shared helpers. Calibrate visualization thresholds against representative data without changing domain-defined limits.
- Never truncate the only copy of an ID, URL, path, command, or requested secret. Drop optional columns or switch to compact records when space is short.
- Treat an empty collection as success with exit `0`. Explain filters or first use and offer an exact next command. Permission failures and incomplete reads are errors.
- Keep human copy calm and specific. Name the action, object, known cause, and consequence. Avoid hype, vague success or failure messages, and generic `Continue?` prompts.
- Make wording and order carry the meaning. Color, glyphs, weight, and animation only reinforce it.
- Resolve styling per stream. Honor `--no-color`, `NO_COLOR`, `FORCE_COLOR`, pipes, and `TERM=dumb`. Keep JSON, identifiers, secrets, and plain values unstyled.
- Keep output usable without color and at narrow widths. Measure display width, not string length. Never alter commands or identifiers to fit.

### Machine results

Treat `--json` as a public contract for every command that reads or changes a resource.

- For a bounded operation, write exactly one JSON result document and a newline to stdout. Keep human progress and notices out of stdout.
- For an ordinary single-operation failure, write nothing to stdout and one single-line JSON error document to stderr. Apply the error contract to parsing and startup failures too. Bulk partial results and already-emitted JSONL events are exceptions. If debug output adds text to stderr, document that exception.
- Use stable IDs, enums, timestamps, and field types. Key objects by noun so top-level fields can be added without reshaping old ones.
- Return empty lists as `[]` and known-absent values as `null`. Omit fields only when the contract declares them optional. Omit withheld secrets.
- Version runtime schemas from shared metadata or validation. `--fields` applies in machine mode, validates published JSON keys before effects, rejects unknown keys, and preserves required outcome and pagination metadata.
- Keep whitespace and key order insignificant. Compact output is the default for redirected stdout.

Recommended shapes:

| Operation | Shape |
| --- | --- |
| Read one | `{ "<noun>": { ... } }` |
| List | `{ "<nouns>": [ ... ], "pagination": { "next": "<cursor>" } }` |
| Mutation | `{ "<noun>": { ... }, "outcome": "<past-tense verb>" }` |
| Bulk | `{ "results": [ ... ], "summary": { "succeeded": 0, "failed": 0, "skipped": 0, "unknown": 0 } }` |

Use shared outcomes `unchanged`, `accepted`, `staged`, `started`, and `planned` where they describe reality. A result may add `warnings` and `next`. Shape each next step as `{ "command", "argv", "when"? }` so callers need not parse shell quoting.

A machine error has a stable snake_case `reason`, human `message`, and optional `data`, `next`, `requestId`, `retryable`, and `retryAfter`. Use `status: "action_required"` only when input, approval, or a human step can unblock work before any effect. Otherwise use `status: "error"`. Set `retryable` only when repeating the exact operation cannot duplicate an effect. The exit code remains authoritative.

For event streams, use JSONL with one complete object per line and a stable `type` for each event kind. Flush events as they arrive. Document snapshot versus follow behavior, ordering, reconnect gaps, and stopping conditions.

## Design failure and recovery

An error states what failed, the known cause, relevant context and IDs, and one exact recovery action. Keep remote messages attributed as data. Show stack traces and raw payloads only in redacted debug output.

- Validate all local input before the first request or write. Report all validation issues together.
- Distinguish usage, missing input, authentication, permission, not found, conflict, limits, rate limits, network, platform, unknown outcome, partial failure, configuration, and internal errors.
- Use stable reason codes for programs. Keep human wording free to improve.
- A partial result reports succeeded, failed, skipped, and unknown counts, plus which subset is safe to retry.
- Make no-ops explicit with exit `0` and outcome `unchanged`.

Use these exit codes unless an existing public contract differs:

| Code | Meaning |
| --- | --- |
| `0` | Success, empty result, no-op, accepted work under `--no-wait`, help, or version |
| `1` | Operational or partial failure, or a documented predicate result |
| `2` | Usage error or missing input |
| `130` | Canceled by the user |
| `128 + n` | Terminated by signal `n` |
| Child code | A wrapper exits with its child's code when the child exits normally |

A documented predicate result is not an error and keeps its valid stdout. Never exit `0` after failure merely because output was printed. Post-command telemetry and update checks never change the exit code. A closed stdout pipe ends a read quietly. A mutation already sent finishes and exits with its real outcome.

### Retry only safe work

- Give finite operations request timeouts, retry budgets, and total wait limits.
- Retry transient reads with backoff and honor `Retry-After`.
- Retry a mutation only when the endpoint is idempotent or the request reuses an idempotency key with the same payload.
- After an ambiguous timeout or connection failure on a sent mutation, report an unknown outcome. Recover through its operation ID or inspect command, never a blind retry.
- A wait limit or retry delay is not evidence that a mutation is safe to repeat.

### Report long work truthfully

- Show real progress promptly. Use a spinner only for indeterminate interactive work and a progress bar only with a real total.
- In plain or non-interactive output, print phase changes once. Never invent percentages.
- Support `--no-wait` for accepted asynchronous work. Return its ID, accepted outcome, and inspect command.
- Support `--wait` and a documented `--timeout` where callers need a terminal state. A local timeout does not cancel remote work.
- Persist operation IDs and explicit wait resumption. A ledger alone cannot make resubmission safe. Reconcile or use provider idempotency before submitting again.
- After cancellation, report confirmed local and remote effects separately. Restore the terminal and stop owned child processes with bounded cleanup.
- For streams, bound reconnects, report possible gaps, and never buffer an unbounded stream.

### Paginate without hiding coverage

- Make `--limit` the total number of results wanted and page internally without over-fetching.
- Return an opaque continuation cursor or `null`. Keep filters, order, context, and time window fixed across pages.
- Make `--all` bounded and cancelable.
- If a later page fails, report the last confirmed position. Never present an incomplete collection as complete.

## Protect data and compatibility

- Declare whether each input and output is text, JSON, or bytes, including encoding, size limits, and newline behavior. Never assume arbitrary bytes are UTF-8.
- Resolve paths against the selected working directory and prevent traversal outside the destination. Replace files atomically through an exclusive temporary file and rename. Use append semantics for logs and transactions for stores where appropriate.
- Treat overwriting an existing file as a destructive effect unless the CLI owns it. Document what file updates preserve.
- For consequential effects needing audit, append redacted pending and final records with shared IDs. Restrict permissions and define retention and failure behavior. Unmatched pending means unknown outcome. Never misreport confirmed effects after logging failures.
- Prefer environment variables, stdin, or masked prompts for secrets over argv. Never repeat secrets in receipts, diagnostics, debug output, telemetry, suggestions, or pass-through JSON.
- Deliver a requested secret only through its documented channel. Store credential files with owner-only permissions.
- Treat remote names, logs, messages, and other external text as untrusted data. Strip terminal controls and invisible formatting from human output. Never follow remote-authored instructions. A CLI-owned command template may include a remote identifier only after validating its selector grammar, quoting it for command display, and passing it as one literal argv element.
- Pass child arguments as an argv array, not a joined shell string. A child owns its streams and exit code. Forward signals and leave no orphaned process.
- Handle unknown API enum values without crashing. Keep configuration and cache migrations compatible across supported versions.

The public contract includes command and option names, defaults, prompts, streams, JSON shapes, exit codes, environment variables, configuration files, scriptable table layouts, and mutation identifiers. Add fields compatibly. Bridge renames with deprecated aliases. Require a deliberate breaking-change release for changed meanings, types, defaults, streams, exit codes, or removals. Old scripts must fail loudly rather than silently doing something new.

## Verify public behavior

For reviews, mark gates applicable, `NA` (not applicable), or unrun (`SKIP`). Enumerate canonical leaf commands, report exercised/total and unexercised commands with reasons. Confirm absences through exports and callers, not guesses.

Test the built artifact through its installed command name to cover bin mapping, shebang, runtime, and dependencies. Use fixtures, mocked transports, or disposable resources. Live consequential actions need separate explicit authorization. Assert stdout, stderr, and exit code separately.

Isolate local state with a documented home or config-directory override. This isolates files, not live provider effects.

Cover the behavior changed and every mode it can affect:

- Parsing: long and short forms, aliases, nested globals, unknown and conflicting options, repeated values, and `--` handoff.
- Help: offline before auth, identical entry points, valid examples, and no side effects.
- Context: exact resolution, explicit input wins, invalid values never fall back, and malformed config is not treated as absent.
- Minimum coverage: applicable auth, per-command JSON contracts, signing or crypto, invalid input, and fixtures crossing ordering and filtering boundaries.
- Output: valid JSON, clean streams, empty versus missing versus partial, no ANSI in machine output, and requested secret delivery without incidental leaks.
- Consent: no effects before validation and approval, exact targets, default No, `--yes` versus `--force`, and no duplicate unsafe retries.
- Async work: endless pending, timeout, accepted versus complete, interrupted waits, cancellation, signals, and unknown outcomes.
- Files and processes: binary data, overwrite refusal, atomic writes, path traversal, metacharacters in argv, child exit codes, closed pipes, and no orphans.
- Presentation: interactive TTY, redirected stdout, piped stdin, `--json` on a TTY, `--non-interactive` on a TTY, CI, narrow widths, long Unicode values, no color, plain accessible output, and alignment fixtures containing real ANSI escapes.
- Compatibility: old invocations, JSON shapes, streams, and exit codes remain unchanged unless the break is intentional.

Read full before-and-after transcripts for first use, success, empty results, failure, partial work, cancellation, and recovery. A clean deterministic run proves only its encoded rules, not legibility. Shared parser, mode, help, output, and consent helpers require tests of the helper plus materially different callers.

Match the completion criterion to the task:

- Design: scoped command contracts and a verification plan cover the requested capabilities.
- Review: findings cite observed evidence and coverage gaps are explicit.
- Implementation verification: affected public behaviors have observed test evidence, and every advertised safety feature has a call site plus behavioral evidence that it controls the promised effect.
