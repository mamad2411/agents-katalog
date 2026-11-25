---
name: owasp-proactive-controls
description: >-
  OWASP Proactive Controls: Insecure software is undermining our financial, healthcare, defense, energy, and other critical infrastructure worldwide. Covers OWASP Proactive Controls. Use when applying proactive security controls. Triggers: Proactive Controls.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OWASP Proactive Controls

The OWASP Top 10 Proactive Controls 2024 (C1 to C10): the implementation practices of each control, read from the project's Markdown source at the v4.0.0 release tag.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Software architect or developer building or reviewing an application.
- Target version: OWASP Proactive Controls (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **C1.** "Ensure that by default, all the requests are denied, unless they are specifically allowed."
2. **C2.** "Don’t store secrets in code, config files or pass them through environment variables."
3. **C3.** "Always perform Input validation on the server side for security."
4. **C7.** "Ensure that the session id is long, unique and random, i.e., is of high entropy."

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
- [ ] Each of C1 to C10 is applied or recorded as not relevant, and every finding names its control id.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `owasp-asvs`, `owasp-top-10`, `owasp-cheat-sheets`, `owasp-wstg`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [C1: Implement Access Control](https://raw.githubusercontent.com/OWASP/www-project-proactive-controls/v4.0.0/docs/the-top-10/c1-accesscontrol.md): OWASP Project document, Tag v4.0.0 (2024-10-20), 2024 list, checked 2026-10-06.
- [C2: Use Cryptography to Protect Data](https://raw.githubusercontent.com/OWASP/www-project-proactive-controls/v4.0.0/docs/the-top-10/c2-crypto.md): OWASP Project document, Tag v4.0.0 (2024-10-20), 2024 list, checked 2026-10-06.
- [C3: Validate all Input & Handle Exceptions](https://raw.githubusercontent.com/OWASP/www-project-proactive-controls/v4.0.0/docs/the-top-10/c3-validate-input-and-handle-exceptions.md): OWASP Project document, Tag v4.0.0 (2024-10-20), 2024 list, checked 2026-10-06.
- [C4: Address Security from the Start](https://raw.githubusercontent.com/OWASP/www-project-proactive-controls/v4.0.0/docs/the-top-10/c4-secure-architecture.md): OWASP Project document, Tag v4.0.0 (2024-10-20), 2024 list, checked 2026-10-06.
- [C5: Secure By Default Configurations](https://raw.githubusercontent.com/OWASP/www-project-proactive-controls/v4.0.0/docs/the-top-10/c5-secure-by-default.md): OWASP Project document, Tag v4.0.0 (2024-10-20), 2024 list, checked 2026-10-06.
- [C6: Keep your Components Secure](https://raw.githubusercontent.com/OWASP/www-project-proactive-controls/v4.0.0/docs/the-top-10/c6-use-secure-dependencies.md): OWASP Project document, Tag v4.0.0 (2024-10-20), 2024 list, checked 2026-10-06.
- [C7: Secure Digital Identities](https://raw.githubusercontent.com/OWASP/www-project-proactive-controls/v4.0.0/docs/the-top-10/c7-secure-digital-identities.md): OWASP Project document, Tag v4.0.0 (2024-10-20), 2024 list, checked 2026-10-06.
- [C8: Leverage Browser Security Features](https://raw.githubusercontent.com/OWASP/www-project-proactive-controls/v4.0.0/docs/the-top-10/c8-leverage-browser-security-features.md): OWASP Project document, Tag v4.0.0 (2024-10-20), 2024 list, checked 2026-10-06.
- [C9: Implement Security Logging and Monitoring](https://raw.githubusercontent.com/OWASP/www-project-proactive-controls/v4.0.0/docs/the-top-10/c9-security-logging-and-monitoring.md): OWASP Project document, Tag v4.0.0 (2024-10-20), 2024 list, checked 2026-10-06.
- [C10: Stop Server Side Request Forgery](https://raw.githubusercontent.com/OWASP/www-project-proactive-controls/v4.0.0/docs/the-top-10/c10-stop-server-side-request-forgery.md): OWASP Project document, Tag v4.0.0 (2024-10-20), 2024 list, checked 2026-10-06.
