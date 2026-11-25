---
name: ultra-research
description: >-
  Dual-model deep research with adversarial cross-audit. Claude and Codex each run
  their own deep-research skill independently on the same question, then each
  audits the OTHER's citations (claim-support: PASS/WEAK/FAIL → trust-score +
  verdict), and Codex synthesizes one trust-weighted final report with a
  disagreement ledger. All 5 notes (2 reports, 2 audits, 1 final) + an index land
  in a persistent Obsidian-style vault; the main session returns a concise bullet
  summary. Use for high-stakes questions, when the user wants dual-model /
  cross-verified research, or when a prior deep-research run came back mixed /
  unreliable. For ordinary research, use claudex:deep-research instead.
license: MIT
---

# ultra-research

`$SKILL_DIR` is this skill's directory. The Python helper is `scripts/vault.py`;
prompts are in `prompts/`. Read each prompt when you reach its stage.

## When to use (routing)
Prefer plain `claudex:deep-research` by default. Use ultra-research only when: the
question is high-stakes (policy/financial/factual gravity); the user explicitly
asks for dual-model or cross-verified research; or a prior deep-research run on the
topic returned `mixed`/`unreliable` citation integrity.

## Setup
1. Disambiguate like deep-research: if the question is underspecified, ask 2–3
   clarifying questions, then proceed; else state one interpretation and proceed.
   Never block mid-run after this point.
2. Resolve paths and the run id:
   ```bash
   VAULT="$(python3 "$SKILL_DIR/scripts/vault.py" vaultpath)"
   REFINED_QUESTION="$(cat <<'EOF'
<refined question>
EOF
)"
   RUN="$(python3 "$SKILL_DIR/scripts/vault.py" runid --date "$(date +%F)" --question "$REFINED_QUESTION")"
   RUNDIR="$VAULT/$RUN"
   mkdir -p "$RUNDIR"
   ```
   The question must be passed as one safely quoted shell argument; do not inline it
   inside double quotes where embedded quotes can break the command.

## Stage 1 — independent research (parallel)
- **Codex (background):** dispatch `Agent(subagent_type: codex:codex-rescue)` with the
  text of `prompts/codex-research.md`, placeholders filled, including `--write` and
  the absolute target `$RUNDIR/20-report-codex.md`. Prefer background.
- **Claude (inline):** run `claudex:deep-research` yourself on the same refined
  question. When it finishes, write its verified report to
  `$RUNDIR/10-report-claude.md` with the report frontmatter
  (`author-model: claude`, `note-type: report`, `degraded: false`,
  `tags: [ultra-research, report]`).
- **Join:** poll for the Codex file until ready or the deadline. Resolve the
  per-stage timeout via the helper (handles scalar or object `codexTimeoutMs`):
  ```bash
  # Stage-1 research default: 20 min (1,200,000 ms) unless config overrides it.
  DEADLINE=$(( $(date +%s%3N) + $(python3 "$SKILL_DIR/scripts/vault.py" timeout --stage research) ))
  until python3 "$SKILL_DIR/scripts/vault.py" ready "$RUNDIR/20-report-codex.md"; do
    [ "$(date +%s%3N)" -ge "$DEADLINE" ] && break
    sleep 10
  done
  if ! python3 "$SKILL_DIR/scripts/vault.py" ready "$RUNDIR/20-report-codex.md"; then
    # Execute DEGRADED branch A.
  fi
  ```
  If the post-loop `ready` check fails → **DEGRADED branch A** (below).

## Stage 2 — adversarial cross-audit (parallel)
Each report is audited by the OTHER model; auditors are blind to each other.
- **Codex audits Claude (background):** dispatch `codex:codex-rescue` `--write` with
  the `prompts/audit.md` contract + the absolute path `$RUNDIR/10-report-claude.md`,
  writing `$RUNDIR/30-audit-of-claude-by-codex.md` (`author-model: codex`,
  `audited-report-model: claude`).
- **Claude audits Codex (inline `Task`):** dispatch a `Task` (general-purpose)
  subagent and explicitly instruct it to use `WebFetch` for every cited URL. Give
  it the `prompts/audit.md` contract assembled inline and the path
  `$RUNDIR/20-report-codex.md`; it writes
  `$RUNDIR/31-audit-of-codex-by-claude.md` (`author-model: claude`,
  `audited-report-model: codex`). Joined by the subagent's return.
- **Join Codex audit:** recompute the deadline from a fresh clock read and the
  Stage-2 audit timeout (default 10 min):
  ```bash
  DEADLINE=$(( $(date +%s%3N) + $(python3 "$SKILL_DIR/scripts/vault.py" timeout --stage audit) ))
  until python3 "$SKILL_DIR/scripts/vault.py" ready "$RUNDIR/30-audit-of-claude-by-codex.md"; do
    [ "$(date +%s%3N)" -ge "$DEADLINE" ] && break
    sleep 10
  done
  if ! python3 "$SKILL_DIR/scripts/vault.py" ready "$RUNDIR/30-audit-of-claude-by-codex.md"; then
    # Execute DEGRADED branch B.
  fi
  ```
  If the post-loop `ready` check fails → **DEGRADED branch B**.

## Stage 3 — trust-weighted final synthesis
Dispatch `codex:codex-rescue` `--write` with `prompts/final-synthesis.md`, the four
absolute paths filled in. It writes `$RUNDIR/90-final-report.md` and prints a bullet
summary to stdout.
- Poll with a freshly recomputed Stage-3 synthesis timeout (default 10 min):
  ```bash
  DEADLINE=$(( $(date +%s%3N) + $(python3 "$SKILL_DIR/scripts/vault.py" timeout --stage synthesis) ))
  until python3 "$SKILL_DIR/scripts/vault.py" ready "$RUNDIR/90-final-report.md"; do
    [ "$(date +%s%3N)" -ge "$DEADLINE" ] && break
    sleep 10
  done
  if ! python3 "$SKILL_DIR/scripts/vault.py" ready "$RUNDIR/90-final-report.md"; then
    # Execute DEGRADED branch C.
  fi
  ```
  If the post-loop `ready` check fails → **DEGRADED branch C**.
- The **file** is canonical; the rescue **stdout is display-only**.

## Index + present
- Assemble `$RUNDIR/00-index.md` from `prompts/index.md`. Read audit verdicts for
  the status table with:
  ```bash
  python3 "$SKILL_DIR/scripts/vault.py" get "$RUNDIR/30-audit-of-claude-by-codex.md" trust-verdict
  python3 "$SKILL_DIR/scripts/vault.py" get "$RUNDIR/30-audit-of-claude-by-codex.md" trust-score
  python3 "$SKILL_DIR/scripts/vault.py" get "$RUNDIR/31-audit-of-codex-by-claude.md" trust-verdict
  python3 "$SKILL_DIR/scripts/vault.py" get "$RUNDIR/31-audit-of-codex-by-claude.md" trust-score
  ```
- Present to the user: the bullet summary, the two trust-verdicts, and the vault
  path `$RUNDIR`.

## Degraded branches (never hard-fail; always label)
Degraded notes get `degraded: true` in frontmatter AND a first-line banner:
`> **⚠️ DEGRADED — single-model run; adversarial cross-audit merit absent.**`
- **A — no Codex report:** do NOT fake adversarial merit. Base the final on Claude's
  deep-research report (already deterministically verified). Optionally attach a
  Claude self-audit ONLY if labeled `self-audit — NOT adversarial; equivalent to plain deep-research integrity`. Write a degraded
  `90-final-report.md` and a degraded `00-index.md`.
- **B — Codex audit failed:** Claude audits Codex's report normally (adversarial in
  that direction) AND self-audits its own report under the explicit
  `self-audit — NOT adversarial; equivalent to plain deep-research integrity` label; proceed to Stage 3; mark the run partially
  degraded.
- **C — Codex synthesis failed:** Claude writes `90-final-report.md` from the four
  inputs using the Stage-3 merge algorithm; set both `author-model: claude` and
  `synthesized-by: claude`. Not full DEGRADED (all four inputs exist) — just note
  the synthesis fallback.

## Hard rules
1. Each side's own deterministic citation verification still runs inside its own
   report; the cross-audit is an ADDITIONAL adversarial layer.
2. An auditor never audits its own report (except the explicitly-labelled degraded
   self-audit, which never counts as adversarial merit).
3. The `90-final-report.md` file — not any stdout — is the canonical final report.
4. Always deliver a labeled result; never stop to ask permission mid-run.
