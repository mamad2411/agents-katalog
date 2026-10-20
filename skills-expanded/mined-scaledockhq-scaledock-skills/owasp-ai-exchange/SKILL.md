---
name: owasp-ai-exchange
description: >-
  OWASP AI Exchange: identify AI security threats and apply the matching controls. Covers OWASP AI Exchange. Use when applying the OWASP AI Exchange. Triggers: AI Exchange.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OWASP AI Exchange

The OWASP AI Exchange: a threat and control framework for AI systems. It groups threats into threats through use, development-time threats and runtime application security threats, and names each control with a tag such as #MODEL ACCESS CONTROL. Read from the project's Markdown source at a pinned commit.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Builder, operator or reviewer of an AI system: its training data, model, prompts, augmentation data, agents and serving interface.
- Target version: OWASP AI Exchange (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **#LEAST MODEL PRIVILEGE.** "Least model privilege: Minimize what a model can do (trigger actions or access data), to prevent harm in case the model is manipulated, or makes a mistake by itself."
2. **#MODEL ACCESS CONTROL.** "Restrict access to model inference functions to approved and identifiable users."
3. **#INPUT SEGREGATION.** "Input segregation: clearly separate/delimit/delineate untrusted data from trusted instructions when inserting it into a prompt and instruct the model to ignore instructions in that data."
4. **#SUPPLY CHAIN MANAGE.** "Supply chain management focuses on managing the supply chain to minimize the security risk from externally obtained elements."
5. **#ENCODE MODEL OUTPUT.** "Encode model output: apply output encoding on model output if it's text."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Every threat in scope is mapped to at least one control, and every finding names its control tag.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `owasp-llm`, `owasp-ml-top-10`, `owasp-agentic`, `mitre-atlas`, `nist-ai-rmf`, `eu-ai-act`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [OWASP AI Exchange: 1. General controls](https://raw.githubusercontent.com/OWASP/www-project-ai-security-and-privacy-guide/e894338312f9a9f448bfd7ece3e412cfbce890ce/content/ai_exchange/content/docs/1_general_controls.md): OWASP Project document, Commit e894338312f9 (2026-10-04), checked 2026-10-06.
- [OWASP AI Exchange: 2. Threats through use](https://raw.githubusercontent.com/OWASP/www-project-ai-security-and-privacy-guide/e894338312f9a9f448bfd7ece3e412cfbce890ce/content/ai_exchange/content/docs/2_threats_through_use.md): OWASP Project document, Commit e894338312f9 (2026-10-04), checked 2026-10-06.
- [OWASP AI Exchange: 3. Development-time threats](https://raw.githubusercontent.com/OWASP/www-project-ai-security-and-privacy-guide/e894338312f9a9f448bfd7ece3e412cfbce890ce/content/ai_exchange/content/docs/3_development_time_threats.md): OWASP Project document, Commit e894338312f9 (2026-10-04), checked 2026-10-06.
- [OWASP AI Exchange: 4. Runtime application security threats](https://raw.githubusercontent.com/OWASP/www-project-ai-security-and-privacy-guide/e894338312f9a9f448bfd7ece3e412cfbce890ce/content/ai_exchange/content/docs/4_runtime_application_security_threats.md): OWASP Project document, Commit e894338312f9 (2026-10-04), checked 2026-10-06.
