---
name: prompt-compiler
description: Use when the user invokes /prompt or asks to compile, refine, or optimize a prompt before execution — interactive pre-flight optimizer that produces an approved super-prompt saved to .devin/scratch/optimized_ready.md.
argument-hint: What task should the compiled prompt execute?
triggers: [user]
---

# Prompt Compiler

Pre-flight prompt optimizer. **You are the Prompt Engineer Sênior** — the
script only validates and assembles; all semantic judgment (effort level,
persona, the five template blocks) is yours, in whatever language the user
writes.

## The Golden Template (mandatory output structure)

```markdown
# Nível de Esforço Obrigatório: [MEDIUM, HIGH ou MAX]
# Perfil Operacional: [Cargo Sênior, ex: Staff Engineer, Tech Lead, SecOps]

# Goal
[1-2 parágrafos — objetivo final]

# Context
[Contexto arquitetural, ferramentas, estado atual]

# Acceptance Criteria
1. [Critério mensurável]
2. [Critério mensurável]

# Scope & Non-Goals
- **IN SCOPE:** [O que fazer]
- **OUT OF SCOPE:** [Proibido — evita reward hacking]

# Execution Hints & Checkpoints
1. **Fase 1:** [Passo]. **PARE e aguarde aprovação.**
2. **Fase 2:** [Passo].
```

## Flow

1. **Analyze the request semantically** (no script yet). Decide:
   - `effort`: `medium` = spot fixes, single-file edits; `high` = features,
     multi-file work (default for general work); `max` = architecture,
     global refactors, deep research, open-ended tasks.
   - `persona`: senior title matching the domain (Staff Engineer, Tech Lead,
     SecOps, Data Engineer…).
   - Style: read `extensions/ai-tools/knowledge_bases/<model>.json` for the
     target model family's prompt rules and apply them to the draft.

2. **Draft the spec JSON** with keys: `effort`, `persona`, `model`
   (optional), `goal`, `context`, `acceptance[]`, `in_scope[]`,
   `out_scope[]`, `phases[]`. Write it to a scratch file, e.g.
   `.devin/scratch/prompt_spec.json`.

3. **Assemble via the script** (never hand-write the final file):

   ```bash
   python extensions/ai-tools/prompt_compiler.py --draft .devin/scratch/prompt_spec.json --dry-run
   ```

   The script validates all blocks and renders the exact Golden Template.
   Invalid specs return `{ok: false, errors: [...]}` — fix and re-run.
   When `model` is a variant family (`swe-2`), the JSON output includes
   `recommended_model` (e.g. `swe-2-max` for effort `max`).

4. **Iterate with the user.** Present the rendered prompt; on feedback, edit
   the spec JSON and re-run. Loop until the user says `APPROVE`.

5. **On approval**, run without `--dry-run` — the script writes
   `.devin/scratch/optimized_ready.md` and prints `{ok, path, sha256}`.
   Verify `ok: true`.

Interactive TTY fallback (user drives the fields, no agent drafting):

```bash
python extensions/ai-tools/prompt_compiler.py            # prompts per field
python extensions/ai-tools/prompt_compiler.py --draft spec.json   # edit-by-section loop
```

## Knowledge base upkeep

New prompt-engineering guide arrived? Do not hand-edit JSONs blindly —
invoke `knowledge-modeling` to extract entities/rules from the raw source,
then write `knowledge_bases/<model>.json` per that directory's README schema,
and re-run `prompt_compiler.py --self-test`.
