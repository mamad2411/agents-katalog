---
name: owasp-ml-top-10
description: >-
  OWASP ML Top 10: review machine learning systems against the top ML security risks. Covers OWASP ML Top 10. Use when reviewing machine learning security risks. Triggers: ML Top 10.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OWASP ML Top 10

The OWASP Machine Learning Security Top Ten 2023 (ML01:2023 to ML10:2023): each risk's description and its How to Prevent controls, read from the project's Markdown source at a pinned commit.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Reviewer, builder or operator of a machine learning model, its training data, its supply chain or its serving interface.
- Target version: OWASP ML Top 10 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **ML02:2023.** "Ensure that the training data is thoroughly validated and verified before it is used to train the model."
2. **ML06:2023.** "Before using any packages in your infrastructure or application dependencies, verify the authenticity of the package by checking the digital signature of the package."
3. **ML08:2023.** "Use techniques such as digital signatures and checksums to verify that the feedback data received by the system is genuine, and reject any data that does not match the expected format."
4. **ML09:2023.** "Maintaining tamper-evident logs of all input and output interactions can help detect and respond to any output integrity attacks."

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
- [ ] Each of ML01:2023 to ML10:2023 is assessed, and every finding names its risk id.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `owasp-llm`, `owasp-ai-exchange`, `mitre-atlas`, `model-signing`, `nist-ai-rmf`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [ML01:2023 Input Manipulation Attack](https://raw.githubusercontent.com/OWASP/www-project-machine-learning-security-top-10/b3addcd63769cf3176c1ac75ea9a21a6a7e0241d/docs/ML01_2023-Input_Manipulation_Attack.md): OWASP Project document, Commit b3addcd63769 (2026-09-30), checked 2026-10-06.
- [ML02:2023 Data Poisoning Attack](https://raw.githubusercontent.com/OWASP/www-project-machine-learning-security-top-10/b3addcd63769cf3176c1ac75ea9a21a6a7e0241d/docs/ML02_2023-Data_Poisoning_Attack.md): OWASP Project document, Commit b3addcd63769 (2026-09-30), checked 2026-10-06.
- [ML03:2023 Model Inversion Attack](https://raw.githubusercontent.com/OWASP/www-project-machine-learning-security-top-10/b3addcd63769cf3176c1ac75ea9a21a6a7e0241d/docs/ML03_2023-Model_Inversion_Attack.md): OWASP Project document, Commit b3addcd63769 (2026-09-30), checked 2026-10-06.
- [ML04:2023 Membership Inference Attack](https://raw.githubusercontent.com/OWASP/www-project-machine-learning-security-top-10/b3addcd63769cf3176c1ac75ea9a21a6a7e0241d/docs/ML04_2023-Membership_Inference_Attack.md): OWASP Project document, Commit b3addcd63769 (2026-09-30), checked 2026-10-06.
- [ML05:2023 Model Theft](https://raw.githubusercontent.com/OWASP/www-project-machine-learning-security-top-10/b3addcd63769cf3176c1ac75ea9a21a6a7e0241d/docs/ML05_2023-Model_Theft.md): OWASP Project document, Commit b3addcd63769 (2026-09-30), checked 2026-10-06.
- [ML06:2023 AI Supply Chain Attacks](https://raw.githubusercontent.com/OWASP/www-project-machine-learning-security-top-10/b3addcd63769cf3176c1ac75ea9a21a6a7e0241d/docs/ML06_2023-AI_Supply_Chain_Attacks.md): OWASP Project document, Commit b3addcd63769 (2026-09-30), checked 2026-10-06.
- [ML07:2023 Transfer Learning Attack](https://raw.githubusercontent.com/OWASP/www-project-machine-learning-security-top-10/b3addcd63769cf3176c1ac75ea9a21a6a7e0241d/docs/ML07_2023-Transfer_Learning_Attack.md): OWASP Project document, Commit b3addcd63769 (2026-09-30), checked 2026-10-06.
- [ML08:2023 Model Skewing](https://raw.githubusercontent.com/OWASP/www-project-machine-learning-security-top-10/b3addcd63769cf3176c1ac75ea9a21a6a7e0241d/docs/ML08_2023-Model_Skewing.md): OWASP Project document, Commit b3addcd63769 (2026-09-30), checked 2026-10-06.
- [ML09:2023 Output Integrity Attack](https://raw.githubusercontent.com/OWASP/www-project-machine-learning-security-top-10/b3addcd63769cf3176c1ac75ea9a21a6a7e0241d/docs/ML09_2023-Output_Integrity_Attack.md): OWASP Project document, Commit b3addcd63769 (2026-09-30), checked 2026-10-06.
- [ML10:2023 Model Poisoning](https://raw.githubusercontent.com/OWASP/www-project-machine-learning-security-top-10/b3addcd63769cf3176c1ac75ea9a21a6a7e0241d/docs/ML10_2023-Model_Poisoning.md): OWASP Project document, Commit b3addcd63769 (2026-09-30), checked 2026-10-06.
