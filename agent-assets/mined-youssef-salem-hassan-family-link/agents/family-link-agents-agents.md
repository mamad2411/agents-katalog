<!--
  Keep in sync with ../AGENTS.md (repository root).
  Some tools only load this path under .agents/
-->
# Family-Link — Agent instructions

Single Flutter app repo: **`lib/`** is the codebase; there are no sibling “backend/front-end” repos in this checkout.

## Quick facts

| Area | Detail |
|------|--------|
| App | Family social / Firebase-backed Flutter mobile app |
| State | **flutter_bloc** (Bloc + Cubit); `bloc_test` / `mocktail` in tests |
| DI | **get_it** + **injectable** — bootstrap **`lib/injection_container.dart`**, codegen **`dart run build_runner build`** → **`di_injection.config.dart`**, accessors via **`locator.dart`** (`sl`) |
| Routes | **go_router** (`lib/config/routes/`) |
| i18n | ARB **`lib/l10n/arb/app_en.arb`** + **`app_ar.arb`** — `flutter gen-l10n`, `context.l10n` |
| Theme / type | **`AppColors`**, **`AppTheme`**, typography via **`BuildContext`** (`lib/core/utils/app_fonts.dart` extensions: `bodyMedium`, `head3`, `buttonText`, …) |
| Primary CTAs | **`AppFilledPrimaryButton`**, **`AppOutlinedPrimaryButton`**, **`AppTextLink`** (`lib/shared/widgets/`) — avoid raw **`TextButton`**, **`ElevatedButton`**, **`FilledButton`**, **`OutlinedButton`** outside those wrappers (only inside shared primitives) |
| Data | Firebase (Auth, Firestore, Storage, Messaging) + repositories under `features/*/data/` |

## Where to read more

- **Architecture:** `tech_readme_files/1_getting_started/PROJECT_ARCHITECTURE.md`
- **Docs hub:** `tech_readme_files/README.md`
- **Cursor rules:** `.cursor/rules/` — mirrored as **`.agents/rules/`** (Markdown)
- **Detailed assistant instructions:** **`CLAUDE.md`** at repo root
- **Token / index noise:** Repo root **`*ignore`** files and **`.cursorindexingignore`** exclude builds, codegen, assets, **`mcps/`**, secrets — keep patterns aligned when adding excludes.

## Do / don’t

- **Do** keep changes scoped to **`lib/`**, **`test/`**, **`l10n/`**, config/platform folders as needed for the task.
- **Do** match existing import style (`package:family_link/...`) and barrel **`app_imports`** where the file already uses it.
- **Don’t** copy patterns from unrelated templates (Technology 92 / job marketplace leftovers are obsolete here).
