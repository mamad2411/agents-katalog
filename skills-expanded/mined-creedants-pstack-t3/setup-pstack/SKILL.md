---
name: setup-pstack
description: Configure which T3 providers and models pstack uses per role, at what reasoning budget, and whether mode is full or light. Reads the live T3 catalog and writes a roles file that every pstack skill reads. Use for /setup-pstack, "configure pstack models", "pstack budget", "pstack mode", or changing pstack's model choices.
---

# Setup pstack

Read [the pstack-t3 runtime](../pstack-runtime/SKILL.md) before spawning workers, choosing models, scheduling, or isolating work. It maps those steps onto T3's orchestrator tools.

Write `~/.config/pstack-t3/roles.json`, the per-role seat table that every pstack-t3 skill reads through [the runtime](../pstack-runtime/SKILL.md). A project can override roles in `.pstack/t3-roles.json`.

`<runtime>` below is the `pstack-runtime` skill directory next to this one.

## Steps

### 1. Check the host and read the catalog

Check the host's tool list for `watch_pull_request`. Accept the T3 harness prefixes described in [the runtime](../pstack-runtime/SKILL.md). A tool listed by name counts as present, including a harness prefix. A deferred `watch_pull_request` counts as present and does not fail this gate. If tools load lazily, use the host's tool discovery and make one bounded `orchestrator_capabilities` call before checking again. A provider catalog does not prove that the watch tool exists. Do not call `watch_pull_request` with a dummy PR to test it.

If `watch_pull_request` is absent, stop setup before writing roles or a saved catalog. Say "Setup cannot finish. This host does not expose watch_pull_request, and pstack-t3 requires T3 Code 0.1.3 or later." Ask the user to update T3 Code and rerun setup. Do not report setup complete.

The runtime host notes state the T3 Code version floor. See [host notes](../pstack-runtime/host.md).

When an expected model is missing, enable Provider update checks in T3's Maintenance settings and refresh provider status. This setting also controls model catalog updates. Read `orchestrator_capabilities` again after the refresh before replacing a seat. Call `orchestrator_capabilities`. Save its JSON result verbatim to a temporary file, for example `/tmp/pstack-t3-catalog.json`. That result is a short list. Outside Codex, Claude, Muse, and Grok it holds at most eight models per provider, and each provider's `omittedModels` counts the rest. The tool takes an optional `search` string that returns the same shape with only the matching models. That file with a search result merged into it is the only source of valid providers, models, and options. Never write a seat that is not in it. Keep the file for the commands in this skill. A host whose `orchestrator_capabilities` takes no `search` parameter returns the whole catalog, so a model it lacks is genuinely missing. `show` and `write` both read it, and a user-level `write` saves a copy as the snapshot. A skill that only resolves a role from a tool result uses the quoted heredoc in [Where roles live](../pstack-runtime/SKILL.md#where-roles-live) instead of a file.

List the runnable providers (`canRunChildTask: true`) with their first three models. List the providers that are not runnable with their `constraints`, such as "Provider is not authenticated", so the user knows what to fix in T3 settings. Muse is beta and disabled by default. Its status can come from a cached catalog without a login or model check, so `canRunChildTask: true` does not prove a Muse seat works. Step 5's smoke delegation decides it. Match a Muse instance by `driverKind: "muse"`, not by the ID `muse`.

### 2. Load current state

```bash
python3 <runtime>/scripts/roles.py show --cwd "$PWD" --catalog /tmp/pstack-t3-catalog.json
```

This prints every role with its seats and `source` (`default`, the user file, or the project file), already resolved against the catalog. It also prints `mode`, `modeSource`, and `escalate`. `notes` name seats that no longer match, such as a model T3 dropped. A note that names a model the saved catalog lacks does not prove T3 dropped it, because step 1's result is a short list. When the host exposes the `search` parameter, call `orchestrator_capabilities` with `search` set to that model id or its name, and save the result to a temporary file. On a host without `search`, keep using the saved catalog and skip search and merge. Merge it with `python3 <runtime>/scripts/roles.py catalog merge --catalog /tmp/pstack-t3-catalog.json --from /tmp/pstack-t3-search.json`. Rerun `show` in this step before calling the seat dropped or rewriting it. Merging a search result with no models exits 2 with `error: search result names no model to merge` and leaves the saved catalog unchanged. An empty result does not prove the model is unavailable. Check the model id and search again before replacing the seat. A merge exits 2 when the result brings a model for a provider the saved catalog lacks or cannot run, and it writes nothing. A role entry that carries a `search` list names configured seats whose models are absent from a provider with omitted models. Each entry is `providerInstanceId/model`. Remove only the provider instance id and the first slash to get the model id. Call `orchestrator_capabilities` with `search` set to that model id, and merge the results the same way. A saved `contextWindow` on a native Claude 5 seat shows as `dropped unknown options contextWindow`, because T3 Code fixes those models at 1M context. Rewrite that seat without it in step 4.

When a configured `claude-opus-5-5`, `claude-sonnet-5-5`, or `claude-haiku-5-5` seat is missing on a native Claude provider, look at T3's model picker for an update notice that names the Claude Code version that model needs. If the notice is there, tell the user to update Claude Code in T3's provider settings and rerun setup. Do not seat a replacement family without saying so.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Use the host's question tool if it has one. Offer these labels, and name the current budget.

- `default — configured seat options as written`
- `unlimited — max reasoning`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

The budget caps the reasoning option (`effort`, `reasoningEffort`, `reasoning_effort`, or `reasoning`). A seat at or below the cap keeps its level. A seat above the cap drops to the cap, or the closest lower level the model offers. A seat that names no level receives the cap. `default` leaves a configured level as it is. `unlimited` lowers a configured `ultra` seat to max when the model offers a level at or below max. `default` keeps a configured `ultra` seat. When every offered level is above the cap, the seat gets the lowest level. A configured seat that names its own level keeps that level when it is at or below the cap. A model without such an option is unaffected. `ultracode` and `ultrathink` are never set by a budget.

**Ask for a mode.** Use the host's question tool. Name the current `mode` and `modeSource` from step 2. Offer these options, in this order.

- `light` (recommended)
- `full`

Store the chosen value beside the budget. When the write target is the project file, name the current `escalate` from `show`. `null` means none. Suggest `**/migrations/**` plus the lock, install, and deploy scripts the repository keeps. Pass one `--escalate` per pattern the user keeps. Omitting both escalate flags leaves a stored project list in place. `--clear-escalate` removes it.

**(b) Propose roles.** Reason over the live catalog from step 1 and propose a seat per role. Weigh the role's work. A code role needs a model that writes code well. A judgment or prose role needs a strong reasoner. A read-only role fits a cheaper, high-volume model. Spread a review panel across model families so agreement means something. When the catalog holds no runnable seat from a family other than the author's, the light-mode gate review takes a same-family seat where one is available and writes `same-family` beside the verifier, per [the runtime's Gate review](../pstack-runtime/SKILL.md#gate-review). Tell the user those reviews lose model diversity. Propose `review backups` when the user wants a panel. It has no built-in seats, and it refuses `inherit`, because the parent can be the author. Set at least two seats of different model families, because `write` refuses `review backups` when it keeps fewer than two usable seats, unless `--force` is passed. Start from `roles.py show` in step 2. Keep every configured role unless the user changes it. Any role the user leaves unset resolves to `inherit`, unless the `exclude` list refuses the inherited seat, and `review backups` stays unset. Offer `large` for a new setup. Show the user each role, its proposed seat, and why it fits, and let them change any role. `write` refuses a seat the `exclude` list refuses, even with `--force`, per [the runtime's Excluded seats](../pstack-runtime/SKILL.md#excluded-seats). When the user names a model the saved catalog lacks and the host exposes the `search` parameter, call `orchestrator_capabilities` with `search` set to that model id and merge the result as step 2 says before proposing it. On a host without `search`, keep using the saved catalog. Never propose a seat no catalog result contains.

**(c) Confirm.** Show every role with its seats. Ask whether to accept as-is or change specific roles. For panel roles the seat count is the panel size. `arena cross-judge pool` is also a list, but Arena runs one judge. It tries only seats from a family other than the parent's, in list order, so order it by preference. An `inherit` seat never judges.

### 4. Write

Build one `--set` per role you are writing. A seat is `inherit` or `provider/model`, with options as a query string. Separate panel seats with `;`.

```bash
python3 <runtime>/scripts/roles.py write --catalog /tmp/pstack-t3-catalog.json --budget large --mode full \
  --set "judgment and prose=claudeAgent/claude-opus-5-5?effort=xhigh" \
  --set "swarm workers=grok/grok-4.7?reasoningEffort=xhigh" \
  --set "interrogate reviewers=claudeAgent/claude-opus-5-5?effort=xhigh;grok/grok-4.7?reasoningEffort=xhigh"
```

The provider, model, and option IDs above are examples of the `--set` shape. Use IDs from step 1. The `exclude` key refuses a model. Add an object entry such as `{"model": "grok-4.7-build-fast"}` to refuse a fast Grok id, or `{"model": "grok-4.7", "options": {"fastMode": true}}` to refuse by declared option, per [the runtime's Excluded seats](../pstack-runtime/SKILL.md#excluded-seats). `write` refuses a seat the exclude list refuses, even with `--force`, and `validate` lists it and exits 1. Write `contextWindow` only for a model whose catalog entry offers it. Cursor's Claude 5 models still offer it. T3's native Claude 5 models do not.

- A default write keeps the stored roles, budget, mode, and unknown top-level keys, so re-runs are idempotent. `--keep` is accepted and changes nothing. Pass `--replace` only when the user asks to start over; it rewrites the roles, budget, and mode from the flags, keeps the stored allow list and a stored project `escalate` list, and writes `<file>.bak` beside it first when the file exists. A write refuses an invalid-JSON or non-UTF-8 target and writes nothing, naming the file and the error. A write refuses a stored `roles` value that is not an object, including with `--replace`, and leaves the file untouched. A user write with no stored mode and no `--mode` stores `light`. A project write with no stored mode and no `--mode` omits the key. Omitting `--escalate` leaves a stored project list in place.
- With no excluded seat, it runs `validate`'s checks on the roles it is about to store. When they list a problem, it prints each one and writes nothing unless `--force` is passed. Fix each problem and rerun. Do not pass `--force` unless the user asks. Write refuses a seat on a metered OpenCode model unless that same file's allow list names the full model id or `--force` is passed. Pass the allow flag on write with that id and rerun.
- Add `--project` to write `.pstack/t3-roles.json` for this repository instead.
- A user-level write also saves the catalog snapshot to `~/.config/pstack-t3/catalog.json`, which `roles.py show` uses later to resolve fallbacks.

### 5. Verify

Run `python3 <runtime>/scripts/roles.py show --cwd "$PWD" --parent "<inheritedProviderInstanceId>/<inheritedModel>"`. Check that configured seats resolve with no mismatch notes. For each unset role other than `review backups`, report the inherit note when it is present, or the replacement, refusal, or `catalog-required` result when `exclude` prevents inheritance. Report `review backups` as unset only when the user left it unset. An unset role does not invalidate an otherwise runnable setup. `info` lines, such as an `inherit` seat made explicit for the budget, are expected. Then run one smoke delegation to each distinct provider in the table: `delegate_task` with `mode: "wait"`, `timeoutMs: 120000`, the seat's target, and the task "Reply with the single word ready." A seat that fails here is not usable. Fix it and rerun step 4. The smoke task runs no command, so it does not prove a Muse child can work under this thread's runtime mode. Check that per [Permissions](../pstack-runtime/SKILL.md#permissions).

### 6. Confirm

Do this only after step 1 found `watch_pull_request` and step 5's smoke delegations succeeded. Tell the user which file was written, the budget, the mode, any provider they could enable in T3 settings to widen the seats they can choose, any seat that replaced a Muse seat on a private project, and that new sessions pick it up immediately. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof, such as a `verify-*` skill or an existing harness. If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, invoke `create-verification-skill`. On no, move on.

### 8. Offer a formal verification skill (optional)

Check whether the project already has a formal verification skill (a project skill that runs a model checker, a proof, or another verifier against the code). If not, offer once: "want a formal verification skill, so agents can prove a key property of your code holds in every case in scope, not only the cases tests reach? I can generate one with /create-formal-verification-skill." On yes, invoke `create-formal-verification-skill`. On no, move on without pushing.

## Set up a second project

When the user asks to set up another project, run the steps above against that repository and write its own roles file.

1. Read the repository's visibility with `gh repo view --json visibility` run in that repository, or the host's equivalent. When the command fails or the host has no equivalent, treat the repository as private.
2. Run step 2's `roles.py show` with `--cwd <root>`, and read that project's seats, budget, and mode.
3. Run the write from step 4 with `--cwd <root> --project`, so it writes `<root>/.pstack/t3-roles.json`. For a private repository, write no seat on `opencode-go/muse-spark-1.3-contributor`. Seat the roles you would have given it on another model from the catalog, and name each replacement seat when you confirm in step 6.
4. Run step 5 with `--cwd <root>`. In step 6, name `<root>/.pstack/t3-roles.json` as the file written, not the user file.
