---
name: forge-experimenter
description: Use when a forge experiment is at phase `built` and needs a bounded real-world experiment run against it inside the Docker sandbox. Skipped automatically for `build-failed` experiments (they route straight to reporter). Trigger via "/forge-experimenter EXP-NNNN", or invoked by forge-orchestrator. Picks a template per spec §10 taxonomy (cli / library / webapp / mcp / service / model), runs it in the same or a fresh container, captures observations and artifacts (screenshots, sample outputs), advances phase to `experimented`.
---

# forge-experimenter — classify type → template → bounded run

Mode is **hybrid** (manifest.experiment.mode): classify, pick a template, improvise within bounds. Templates prevent flailing; improvisation keeps it useful.

## When to use

- An experiment is at phase `built` (skip if `build-failed`).

## Inputs

- `experiment.yaml` — already has `experiment.type` from the builder.
- The built working copy + container image from the builder.
- A comparables list from the research block (for cli-style A/B).

## Outputs

- `experiment.experiment.{template, steps[], observations, result}` populated.
- `experiments/EXP-NNNN-<slug>/artifacts/` — screenshots, sample outputs, harness scripts.
- Phase advanced to `experimented`.

## Templates (spec §10, extended)

**Build-shaped sources** — there is a clonable repo with code to run:

| type | template | what to do |
|---|---|---|
| cli | `cli-sample-input` | run against a curated sample input; A/B against the named comparable on the same input |
| library | `library-headline-api` | 20-line harness exercising the headline API; capture output |
| webapp | `webapp-boot-probe` | boot dev server; curl health/route; screenshot via headless browser |
| mcp | `mcp-list-and-call` | connect, list tools, call one with a known-safe payload |
| service | `service-compose-probe` | `compose up`; probe declared port; capture response |
| model | `model-one-inference` | load weights; run one inference on a fixture |

**Non-build sources** — there is no clonable system, only a description. The operating principle for these templates: **operationalize the work**. After research and critique, produce a portable, functional artifact (code, harness, or skill) that someone else could pick up and run. A non-build experiment that ends at "this is interesting" has failed forge's bar; a non-build experiment that ends at "here is a 200-line implementation of the idea, and we ran it" has cleared it.

| type | template | what to do |
|---|---|---|
| article-as-spec | `article-as-spec` | Read source. Extract the system being described — its inputs, outputs, core algorithm, contracts. Implement the minimum viable harness that exercises the claim. Run it against a toy fixture. Write tests. Package as a reusable skill where the artifact has a stable API. The article becomes a *spec*; forge ships the *system*. |
| research-paper | `paper-claim-reproduce` | Identify one falsifiable headline claim. Build the smallest fixture that lets you check it (hand-rolled or, if compute permits, an actual reproduction). Honest result: "claim holds on our fixture," "claim fails on our fixture," or "claim is not testable in our sandbox — here is why." Bias toward honest negative results. |
| third-party-app | `tpa-pin-and-bench` | The vendor product itself is out of scope. Operationalize the *contract* it offers: if it's a hosted API, write a thin client and run sample requests with secrets-from-env; if it's a desktop GUI launcher, package one of its "scripts/pins/recipes" as a headless equivalent and bench that. The forge artifact is the portable wrapper, not the vendor product. |
| commentary-only | `commentary-pattern-note` | Source is a tweet, X post, Slack message, or short essay too thin to operationalize. Decline gracefully: write a pattern note (forge build-failed style — see EXP-0001), list the open-source projects that could be operationalized instead, recommend specific follow-up 🧪 candidates. Do NOT publish a full report; this is a short note. |

### The operationalization rule

For every non-build experiment, ask in this order:
1. **Can I implement the system the source describes?** If yes → `article-as-spec` or `paper-claim-reproduce`.
2. **Can I implement a portable wrapper around what it offers?** If yes → `tpa-pin-and-bench`.
3. **Is the source too thin to operationalize?** If yes → `commentary-pattern-note`, short, with explicit follow-ups.

The artifact's lifetime success criterion is **a future reader can pip-install / docker-pull / clone-and-run what we shipped, with no reference back to the original source needed.**

## Procedure

1. `forge-state read` the EXP record; abort if phase != `built`. For non-build sources (article/paper/third-party-app/commentary), `built` is reached either by a successful skeleton scaffold or by a deliberate `phase: built` annotation from the researcher noting "no clone, proceeding to non-build template."
2. Select template from the table above based on `experiment.type`. For non-build sources, apply the operationalization rule first.
3. Build a fresh container from the build image (or reuse) — same egress policy, same caps. Non-build templates may need a scaffolded workdir under `/tmp/forge/EXP-NNNN/<artifact-name>/` instead of a cloned repo.
4. Execute template steps inside the container; capture stdout, exit codes, durations, and artifacts.
5. **Operationalize.** If the template produced runnable code or a working harness, also:
   - Stage it under `experiments/EXP-NNNN-<slug>/deploy/` so the packager finds a real bundle.
   - If it's reusable across future experiments, draft a companion skill at `plugin/skills/<name>/SKILL.md` describing how to invoke it. Skills emitted by experiments must include an `experiment_origin: EXP-NNNN` frontmatter field.
6. Synthesize:
   - `steps[]`: human-readable list of what was done.
   - `observations`: 2–6 sentences, factual.
   - `result`: `success` (template completed, observations are interesting, artifact is portable), `partial` (template completed, results equivocal), `failed` (template ran but produced nothing usable).
7. Save artifacts to `experiments/EXP-NNNN-<slug>/artifacts/` via `forge-state write`.
8. `forge-state advance-phase EXP-NNNN experimented`.

## Error handling

- Template cannot select sample input → record `result: failed`, observations note "no representative input available," still advance.
- Timeout inside template → terminate, record partial observations.
- Network needed beyond registries-only → record `result: failed` with reason; do not weaken egress policy.

## Out of scope

This skill's own git activity is limited to staging deploy-bundle files
under `experiments/EXP-NNNN-<slug>/deploy/` for the packager to find — it
never runs `git init`/`commit`/`push` itself, never touches `~/forge`'s own
repo state, and never creates a GitHub repo (that's `forge-packager`'s job,
gated by the promote-to-repo decision).

## References

- Spec §10 (experiment taxonomy), §2.4 (isolation), §9 (sandbox), §6 (lifecycle).
