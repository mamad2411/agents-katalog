---
name: codex-agent-init
description: Initialize or reconnect Codex Agent after cloning or moving this repository. Use when a user asks to set up, initialize, onboard, connect, or repair project memory; when `.agent-memory.local.json` or `.agent-vault` is missing; or when continuing the same Codex Agent project on another computer. Detect the platform and available runtime, guide the user through only ambiguous choices, keep private memory outside Git, validate the connection, and offer an explicitly approved personalization pass.
---

# Initialize Codex Agent

Turn a cloned repository into a working Codex Agent project with minimal user effort. Run this from a local Work or Codex task that can access the cloned folder and its repository skills; a generic or cloud-only chat without local folder access cannot create the connection.

## Keep the setup safe

- Resolve the repository root with `git rev-parse --show-toplevel`; never assume the current directory.
- Keep live memory outside the Git checkout. Never create a fallback vault inside the repository.
- Never overwrite an existing config, vault manifest, private note, or `.agent-vault` target to make setup pass.
- Never put credentials, tokens, private keys, cookies, or raw secrets in the vault.
- Never copy a personalized `SOUL.md` or durable preferences into tracked `AGENTS.md`. Keep only the generic public fallback there; let the reviewed startup hook inject the approved compact event profile.
- Treat context size as a budget. The design target is about 2,000 tokens; automatic rendered output must stay within 12 KiB for `SessionStart` and 8 KiB for `SubagentStart`. Do not fill spare capacity with optional memory.
- Keep total private-memory text made model-visible within 24 KiB for the setup task and 16 KiB for any subagent, including at most 12 KiB and 8 KiB of warm retrieval respectively. Normally retrieve no more than three relevant notes.
- Avoid parallel vault-writing tasks across computers. Read-only work may overlap, but a locally absent lease does not prove that another writer is inactive because synchronized state can lag.
- Ask only for missing or genuinely ambiguous information. Explain each requested choice in plain language.
- When the current Codex surface exposes the structured `request_user_input` UI, prefer it for genuine choices and approvals. If it is unavailable, use one concise numbered text prompt; never treat the UI as a required dependency.
- Structured input is mode- and surface-dependent and may be unavailable in Default mode. If a call is rejected as unavailable, do not retry it in the same turn; state the limitation once and use the text fallback unless the user specifically wants to switch to a supported mode.

## 1. Inspect before asking

1. Select the first suitable runner before deciding that setup is absent:
   - Prefer Python 3 with `<repo>/scripts/agent-memory.py` on every operating system.
   - If Python 3 is unavailable, use `<repo>/scripts/agent-memory.ps1` through Windows PowerShell or cross-platform `pwsh` for connection work, but report that automatic startup injection remains unavailable until Python 3 is installed. Do not describe the agent as fully initialized.
   - If neither Python 3 nor PowerShell is available, explain the smallest installation needed and wait. Do not improvise the vault protocol with ad hoc file operations.
2. Run `doctor` even when `.agent-memory.local.json` and `.agent-vault` are absent from the current checkout. A linked Codex worktree can reuse one compatible connection from another worktree in the same Git worktree family.
3. If `doctor` succeeds, stop connection setup. Continue to startup-hook verification and personalize only when the user requested it.
4. If `doctor` fails, check for `.agent-memory.local.json` and `.agent-vault` at the repository root. If only one exists, preserve it and diagnose the partial state:
   - When only the config exists, validate that it is a regular JSON file and propose reconnecting its recorded project and vault path.
   - When only the link exists, inspect and report its target but do not adopt or replace it automatically; ask the user to confirm the intended vault.
5. Infer a provisional project ID from the repository directory name. Accept it only if it matches `^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`; otherwise ask for a short portable ID.
6. Look only in common, shallow local sync locations for Google Drive. Do not scan an entire home directory or disk. Treat a Drive connector as separate from a locally mirrored or offline folder.
7. If exactly one suitable local sync folder is evident, propose `<sync-folder>/CodexAgent` as the vault root. If none or several are plausible, ask the user which local synchronized folder to use. A Dropbox, OneDrive, iCloud Drive, Syncthing, or mounted Drive folder is acceptable when it is fully local and available offline.
8. After selecting the vault root, inspect only its immediate child folders for `00-system/MANIFEST.json`:
   - Validate candidate manifests before trusting their IDs.
   - If one matches the provisional project ID, propose reconnecting it.
   - If exactly one valid project exists under the root but its ID differs from the clone directory, ask whether this clone should reconnect to it.
   - If several valid projects exist, list only their project IDs and ask which one belongs to this clone.
   - Do not create a new project ID while an existing project may be the intended target without making that choice explicit.

## 2. Show the plan and connect

Before the first external write, show a compact plan containing:

- repository root
- selected runner
- proposed project ID
- proposed vault root and resulting project-vault path
- the current or proposed local device ID and its private `50-devices/<device-id>/` scope
- the fact that `.agent-memory.local.json` and `.agent-vault` remain machine-local and ignored by Git
- the fact that `.codex/hooks.json` is reviewed public source and Codex will require one-time trust before its startup and prompt-relevance commands run
- the hourly device-local scheduler that permanently deletes expired files from the ignored seven-day `output/` delivery outbox
- when Codex desktop automation management is available, the daily device-local LLM task that checks and compacts only approved mutable memory summaries

Resolve any correction, then run one matching command from the repository root:

```text
python3 scripts/agent-memory.py setup --vault-root <path> --project-id <id>
python scripts/agent-memory.py setup --vault-root <path> --project-id <id>
./scripts/agent-memory.ps1 setup -VaultRoot <path> -ProjectId <id>
```

Do not supply a device ID unless the user explicitly needs a stable custom value. Let the tool generate a unique local ID.

When Python is available, install or refresh the device-local outbox sweeper from the repository root. Before the first install, inspect `output/`. If it contains pre-policy entries and no activation state, show the exact directory and item count, then require the user to review and move that legacy directory outside the repository; never enroll it automatically.

```text
python scripts/artifactctl.py sweep --json
python scripts/artifactctl.py install-sweeper --json
```

The install command activates only an empty outbox, uses the current user's Windows Task Scheduler on Windows and the current user's crontab on macOS or Linux, pins the current script hash, and affects only this checkout's ignored `output/` path. Explain this local scheduled write before running it. Use `python scripts/artifactctl.py uninstall-sweeper` when intentionally decommissioning the checkout.

When Codex desktop exposes automation management, create or refresh one standalone local-project automation named `Codex Agent memory compaction` for this repository. Run it daily in the project directory, use a reasoning-capable model at medium effort, and notify only on failures. Keep it local rather than using an isolated worktree because the ignored vault connection belongs to this checkout. Use this prompt:

```text
Maintain this project's portable memory summaries. Run `python scripts/agent-memory.py doctor` and `python scripts/agent-memory.py compaction-plan --json`. If the plan is `ok`, report a no-op and finish. If it is `pending`, load `$portable-agent-memory` and follow its automatic mutable-summary compaction workflow exactly: acquire the advisory lease, use the LLM to compact only listed candidates in place to the reported target, preserve structure and every distinct durable meaning, create no backup or archive, verify the plan returns `ok` and `python scripts/agent-startup-context.py --check` passes, then release the exact lease. If another writer holds the lease, leave the vault read-only and finish without error so a later run can retry. Never compact Soul, immutable records, originals, archives, untrusted material, or another device.
```

Prefer updating the matching automation over creating a duplicate. This registration is local Codex state and must be repeated on each desktop computer. If automation management is unavailable, do not write raw scheduler files; the trusted `SessionStart` hook still injects catch-up work whenever Codex resumes.

If permissions prevent writing the selected external folder or creating the local link, request only the narrow permission needed for those exact paths. Never weaken the repository's ignore or publication rules.

## 3. Verify the result

1. Run `doctor` with the same runner.
2. Run `context --json` for Python or `context -Json` for PowerShell.
3. Confirm that the project ID, device ID, agent profile ID, vault path, and eligible sources are internally consistent. Only `INDEX.md`'s compact `Memory map` and `Write routing` sections are automatic routing context; the remaining index body and full `MEMORY_POLICY.md` stay cold.
4. Confirm that `doctor` bounded its budget scan to the working-set areas, stopped once review was certain or a hard traversal cap was reached, and did not inventory large cold storage. Review any warning it emitted. Run the exhaustive read-only `budget` command when setup adopted a non-empty vault or storage size is otherwise relevant. Its default working-set, whole-vault, and single-file thresholds are 1 MiB/250 files, 100 MiB/1,000 files, and 16 KiB, with warnings at 80%; a successful aggregate report must not expose private filenames or contents. Run `compaction-plan` separately and confirm it can list only the project, preference, and current-device summaries.
5. With Python, run `python scripts/agent-startup-context.py --check`. Confirm `status=ready`, both event profiles, the expected compact sections, the 12 KiB and 8 KiB rendered ceilings, the expected connection mode, and a hook/script hash match. Do not print private rendered content as a setup report.
6. Confirm that `.codex/hooks.json` contains `SessionStart`, `SubagentStart`, and the read-only `UserPromptSubmit` memory-relevance gate; that `SessionStart` also pins `scripts/artifactctl.py sweep`; that every script command pins its current SHA-256; and that the hourly local sweeper is installed. Verify `python scripts/agent-prompt-memory-gate.py --check` without printing prompt or memory content. When desktop automation management is available, confirm exactly one active `Codex Agent memory compaction` automation targets this local project. Treat hook trust as a setup-completion invariant, not an optional follow-up: Codex skips new or changed non-managed hooks until the user reviews and trusts their exact current definitions. After validating those definitions, open the surface's hook review UI, show the user what will run, and obtain their explicit trust decision for every reviewed project hook. In the CLI, direct the user to `/hooks` and wait for that review to finish. Re-open hook status or start a fresh or resumed task and verify that the trusted commands actually run. If trust cannot be completed or verified, report initialization as incomplete with hook trust as the precise blocker; never claim startup memory is active merely because `.codex/hooks.json` is valid.
7. Explain that hook trust, startup injection, and catch-up outbox cleanup begin on a new or resumed task. The independent hourly scheduler handles expiry without spending a model turn. When Python is available and the current setup turn needs the normal session profile without invoking a hook, use `python scripts/agent-startup-context.py --render --event SessionStart`.
8. Confirm the event profiles: `SessionStart` uses compact Soul, project, durable-preference, current-device, and vault-owned memory-map/write-routing sections plus the metadata-only knowledge-scope catalog. `SubagentStart` uses only compact project plus the same bounded current-device/map/routing/catalog view. `UserPromptSubmit` emits only a routing reminder and safe scope names for continuity-sensitive prompts; it never injects a raw prompt or note body. Handoff bodies remain task-retrieved. Confirm that only the current device profile and its note scopes can be selected and another device's folder is never adopted automatically. If an older vault lacks the current profile, explain that setup can add it without overwriting shared memory.
9. For a new vault, confirm that `40-documents/` is a cold, optional preservation area and is absent from bounded startup context. Older compatible vaults may omit it until the first explicitly approved original is preserved. Documents and archives still count toward the whole-vault budget even though they are never automatic context.
10. If validation fails, explain the failed invariant and preserve the existing files. General budget warnings require review. Only a pending `compaction-plan` authorizes the bounded, semantic-preserving summary rewrite defined above.

## 4. Offer guided personalization

After a healthy connection, offer to configure the compact private session sources. Do not make personalization a prerequisite for the safe connection.

1. Inspect only `.agent-vault/00-system/SOUL.md`, `.agent-vault/10-project/PROJECT.md`, and `.agent-vault/10-project/USER_PREFERENCES.md`.
2. Draft only durable, frequently useful context from the current repository before asking the user. Keep each source concise enough for the combined event budget, and route detailed evidence to warm notes rather than startup sections. Do not ask for facts that current repository sources already establish.
3. Before the interview, explain the available interaction in one short message: Plan mode provides click-to-choose question cards when `request_user_input` is available; Default mode asks the same questions as concise free-form prompts. State that both paths create the same vault and personalization files, and do not imply that Plan mode is required for setup.
4. When `request_user_input` is available, use it for the onboarding interview:
   - Ask at most three related questions per round with two or three concrete choices each.
   - Put the sensible default first and mark it as recommended. Rely on the UI's free-form response for a custom answer instead of adding a fake `Other` choice.
   - A useful first round covers agent role, working style, and communication style. A second round may cover how to address the user, autonomy boundaries, and memory boundaries.
   - Do not set an automatic timeout or default resolution. Personalization answers and approval require explicit user input.
5. If structured input is unavailable, ask the same missing items in one compact numbered text prompt and make clear that the user may accept the recommended defaults.
6. Present the exact proposed edits. When structured input is available, request final approval with choices such as `Approve and save` and `Revise first`; otherwise ask for explicit textual approval. Never edit `SOUL.md` or durable preferences based only on an inferred or timed-out answer.
7. Before an approved `SOUL.md` edit, warn that Google Drive cannot prove another writer is inactive. Ask the user to confirm that other vault-writing tasks are stopped and Drive is up to date, or to explicitly accept the concurrency risk. Do not permanently block personalization after the user confirms and approves the exact content.
8. Before approved writes, acquire the advisory lease with `begin` and retain the exact lease ID only in the current task context. Treat `lock=none` as no visible lease, not proof of global inactivity.
9. Apply approved edits without removing the private-record marker. Release the exact lease with `end`, including after a failed or interrupted edit.
10. Run `doctor` again and report any remaining placeholders rather than inventing answers.
11. Run both event-profile readiness checks again so oversized content, secret-like patterns, an ineligible handoff, or a stale hook hash cannot silently disable the next task's injection.

## 5. Finish clearly

Report:

- that setup is complete or the precise remaining blocker
- the project ID and private project-vault path
- the selected lifecycle runner
- whether personalization is complete
- whether the startup hook is ready and trusted, and whether a new task is needed to activate it
- whether the hourly temporary-delivery sweeper is installed and that `output/` files expire permanently after seven days
- whether the daily local LLM memory-compaction automation is installed, or whether this surface relies on `SessionStart` catch-up
- whether the connection is local to this checkout or inherited safely from a sibling worktree
- the current device ID and whether its device-scoped profile is ready
- that Drive-only coordination cannot reliably detect every active writer and parallel vault writes should be avoided
- that the user should wait for synchronization to finish before switching computers

Keep the handoff concise. Do not expose the lease ID, secret values, or the contents of private memory in the summary.
