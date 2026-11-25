---
name: recording-studio-new-gem
description: Start a new Recording Studio addon from RecordingStudio_gem_template, rename it, and strip leftover template identity. Use when creating or extracting a recording-studio-* gem, or when a new gem still says it is a template.
---

# New Recording Studio gem

Do not start from `rails plugin new`. Start from **[RecordingStudio_gem_template](https://github.com/bowerbird-app/RecordingStudio_gem_template)** (dummy app, Flatpack, v3 declarations, both test suites).

## 1. Copy, then rename

Create a new repo (`RecordingStudio_webhooks`, `RecordingStudio_moveable`). Do not keep working in the template repo.

```bash
bin/rename_gem recording_studio_webhooks --dry-run
bin/rename_gem recording_studio_webhooks
```

Use snake_case Rubygems names (`recording_studio_moveable`). Then search for leftovers the script will not productize:

- README still titled GemTemplate / “internal template”
- Gemspec summary about the template; homepage still the template repo
- Dummy sidebar starter docs, `example_service`, sample home controller
- Comments that say “example” or “template”

Public **README is the product**. `docs/gem_template/` stays as engine internals — leave it, do not treat it as the README.

Dummy login (`admin@admin.com`) can stay in dummy; it is not product copy.

## 2. Then follow the other skills

- Mixin vs addon: `recording-studio-capabilities` / `recording-studio-gems`
- Add the new gem to the approved kit in `recording-studio-gems`
- Screens and helpers: `recording-studio-ui`
- Same domain action on the API if there is an API: `recording-studio-api`
- Admin only if staff operate this capability: `recording-studio-admin`
- Tests: `recording-studio-tests`

Keep dummy as a **host that proves the gem**, not as the product. Bump the gem version once per branch; changelog and upgrade notes with the change.
