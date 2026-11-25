---
name: repo-admin-hygiene
description: "Standardize GitHub repository metadata, labels, license, defaults, package metadata, and lightweight governance. Use for GitHub repo setup, org hygiene sweeps, About metadata, labels, default branches, wikis, projects, templates, rulesets, and license checks."
---

# Repo Admin Hygiene

Use this skill for GitHub repository setup and metadata cleanup.

## Inspect

- Description and homepage.
- Topics.
- Root `LICENSE`.
- Default branch.
- Wiki and Projects settings.
- Issue and PR templates.
- Standard labels.
- Branch protection or rulesets.
- Actions settings and reusable workflow access.
- Package metadata for first-party packages.

## Apply

- Keep descriptions product-specific.
- Use verified public URLs only.
- Use `main` as the default branch.
- Disable Wikis and per-repo Projects unless intentionally used.
- Use the label set from `labels/standard-labels.json`.
- Use the selected license text for the repository.
- Keep package metadata consistent with repository visibility, publishability, and the selected license.
- Keep vendored third-party package metadata unchanged unless the task explicitly targets vendored code.
- Prefer explicit template adoption over relying on implicit organization defaults.
- Keep single-developer rulesets lightweight unless the user asks for stricter PR gates.

## Safety

- Re-read current repo metadata before changing it.
- Do not overwrite custom descriptions or homepages unless they are missing or explicitly approved.
- For destructive changes such as deleting labels, changing visibility, or deleting repositories, confirm scope from the user or a prior explicit request.

## Verify

- Re-read GitHub metadata after changes.
- Confirm every active repo has a root `LICENSE`.
- Confirm non-standard labels are absent when strict label sync is requested.
- Confirm default branch and remote HEAD agree.
