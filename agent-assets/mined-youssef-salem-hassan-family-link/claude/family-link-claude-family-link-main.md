# Claude / assistant instructions — Family-Link

Flutter app **family_link** — repository root **is** the project (see `pubspec.yaml`, `lib/`).

## Response style

- Prefer concise answers; cite paths as `lib/...` / `test/...`.
- Prefer **implementing or editing** code over handing the user vague shell-only instructions (when the workspace allows).
- Align with **`AGENTS.md`** (repo root), **`.agents/AGENTS.md`** (mirror for **`.agents/`**-only hosts), **`.cursor/rules/*.mdc`**, and **`.agents/rules/`** (Markdown mirror), e.g. `project-scope`, `dart-conventions`, `bloc-patterns`, `feature-architecture`, `ui-design-system`, `api-integration`, `security`, `documentation-updates`.

---

## Environment

- **Development OS:** Windows — use PowerShell-friendly examples where relevant (`;` chaining, `\` paths).
- **Flutter:** `flutter pub get`, `flutter gen-l10n`, `flutter analyze`, `flutter test`, `dart format .`
- **Codegen:** `dart run build_runner build --delete-conflicting-outputs` after changing injectable/register annotations (`di_injection.config.dart`).

---

## Scope

This checkout contains **only the Family-Link Flutter application**. Older references to:

- another app folder (e.g. `technology_ninety_two_app/`),  
- Laravel / Next sibling repos,  

are **obsolete** — ignore them.

---

## Architecture (short)

- Feature-first **`lib/features/<name>/`** with **presentation** (Bloc/Cubit, pages, widgets), **domain** (entities, repository contracts, use cases), **data** (sources, models, repo impl).
- **`lib/core/`** — shared services, routing, theme, fonts, localization glue, utilities.
- **`lib/shared/widgets/`** — reusable UI (**`AppFilledPrimaryButton`**, **`AppOutlinedPrimaryButton`**, **`AppTextLink`**, **`CustomAppBar`**, etc.).
- **Imports barrel:** `package:family_link/core/utils/app_imports/app_imports.dart` (many screens already use it).
- **DI:** `lib/injection_container.dart` bootstraps the app; **`lib/di_injection.dart`** + generated **`di_injection.config.dart`** register injectable types; **`lib/locator.dart`** exposes **`sl`** (GetIt).

Authoritative narrative: **`tech_readme_files/1_getting_started/PROJECT_ARCHITECTURE.md`**.

---

## UI & tokens

- **Colors:** **`AppColors`** (`lib/core/utils/app_colors.dart`) and theme (`AppTheme`).
- **Text:** Typography extensions on **`BuildContext`** (`lib/core/utils/app_fonts.dart`): e.g. `context.bodyMedium`, `context.head3`, `context.buttonText` — prefer these over ad-hoc **`TextStyle`**. **`ColorUtils`** extensions live in **`app_colors.dart`** (e.g. `context.primaryColor`, `context.cardColor`).
- **Buttons:** Use shared **`AppFilledPrimaryButton`** / **`AppOutlinedPrimaryButton`** / **`AppTextLink`** for standard CTAs — do **not** introduce raw **`TextButton`**, **`ElevatedButton`**, **`FilledButton`**, or **`OutlinedButton`** in feature **`lib/`** (reserved for **`app_text_link.dart`**, **`app_filled_primary_button.dart`**, **`app_outlined_primary_button.dart`**, and theme defaults).
- **Localization:** All user-visible strings **`context.l10n.*`**; edit **`lib/l10n/arb/app_en.arb`** and **`app_ar.arb`**, then `flutter gen-l10n`.

---

## State & routing

- **Bloc/Cubit:** `BlocBuilder`, `BlocListener`, `context.read<>()` / `context.watch<>()` as appropriate; follow **`bloc-patterns`** rule.
- **GoRouter:** register paths in **`lib/config/routes/`** — avoid hard-coded route strings sprinkled without central definitions.

---

## Testing

- **`flutter test`**, **`bloc_test`**, **`mocktail`**.
- Mirror **`lib/features/...`** under **`test/features/...`** where tests exist.

---

## Documentation edits

Structural or milestone notes often belong under **`tech_readme_files/`**. See **`.cursor/rules/documentation-updates.mdc`** (and **`.agents/rules/documentation-updates.md`**). There is **no** top-level **`CHANGELOG.md`** requirement unless the team adds one. Start from **`tech_readme_files/README.md`** for navigation.

---

## Scripts

Repo may include **`scripts/*.ps1`** for Android/deploy helpers — prefer existing scripts when modifying build/deploy flows.
