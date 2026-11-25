---
name: tpl-situacao-internacionalizacao-i18n
description: Template do pack (situacao/18-internacionalizacao-i18n.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/18-internacionalizacao-i18n.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Internationalization (i18n)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/18-internacionalizacao-i18n.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when implementing internationalization (i18n) and localization (l10n) in an application — extracting hardcoded strings, formatting dates/numbers/currencies for different locales, handling right-to-left languages, setting up a translation workflow, or auditing an existing application for i18n completeness. Done wrong, i18n is a permanent source of UI bugs and translator frustration. Done right, it's transparent.

## OBJECTIVES
- Extract all user-visible text into externalized translation keys
- Format dates, numbers, currencies, and units using locale-aware APIs
- Support bidirectional (RTL) text layouts without layout breakage
- Establish a translation workflow that doesn't block development
- Handle plural forms, gender, and context correctly for all target languages

## APPROACH RULES

1. **Externalize every user-visible string.** No hardcoded text in UI code. Every string must have a key in the translation source file. Even single words like "Save" or "Cancel" — they have different lengths and gender forms across languages.

2. **Use locale-aware formatting APIs.** Never format dates, numbers, or currencies manually. Use `Intl.DateTimeFormat`, `Intl.NumberFormat`, `Intl.RelativeTimeFormat` (JavaScript) or the equivalent in your stack. `new Date().toLocaleDateString('pt-BR')` ≠ `new Date().toLocaleDateString('en-US')`.

3. **Translation keys describe context, not content.** Key: `checkout.submit_button` not `save` (too generic) and not `save_your_order_and_proceed` (too fragile). Keys should be stable even if the English text changes.

4. **Plural forms are language-specific.** English has 2 plural forms (1 item, N items). Russian has 4. Arabic has 6. Use your i18n library's plural handling — never `count === 1 ? 'item' : 'items'` in code.

5. **Locale detection with user override.** Auto-detect from `Accept-Language` header or browser `navigator.language`. Always allow the user to manually override. Store preference in their profile.

6. **Missing translation fallback must be configured.** When a translation key is missing in locale X, fall back to the default locale (usually English), not to an ugly key string like `user.settings.theme_selector.label.dark`.

7. **RTL requires CSS architecture, not just text direction.** When supporting Arabic, Hebrew, or Farsi: use CSS logical properties (`margin-inline-start` instead of `margin-left`), set `dir="rtl"` on the root, and test the full UI in RTL mode.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| Hardcoded string in UI component | Extract to translation key immediately. Key naming: `{page/component}.{element}` |
| `count === 1 ? 'X' : 'Xs'` in code | Replace with i18n plural function: `t('items', { count })` with plural forms in translation file |
| `new Date().toString()` in UI | Replace with `new Intl.DateTimeFormat(locale, options).format(date)` or library equivalent |
| Currency formatted with string concatenation | Replace with `new Intl.NumberFormat(locale, { style: 'currency', currency }).format(amount)` |
| Translation key with period in it | Escape the period or use a nested key structure. Most i18n libraries use dot notation for nesting. |
| Same string used in 5+ places | Consider a shared namespace for common UI elements: `common.actions.save`, `common.buttons.cancel` |
| Translation file getting very large | Split by page/feature namespaces. Load namespaces lazily where supported. |
| RTL support needed | Audit CSS for all directional properties. Replace with logical properties. Test with Arabic or Hebrew content strings. |
| "Lost in translation" — translator doesn't know context | Add context/description to every translation key. Modern TMS (Translation Management System) supports this. |
| Gender-sensitive language needed (French, Spanish) | Use ICU MessageFormat for gender variables: `{gender, select, male {Il} female {Elle} other {Ils}}` |

## Key Naming Convention

```
Pattern: {namespace}.{component}.{element}[.{modifier}]

Examples:
  auth.login.title
  auth.login.email_label
  auth.login.submit_button
  auth.login.error.invalid_credentials
  auth.login.error.account_locked

  checkout.order_summary.title
  checkout.order_summary.items_count  → plural: "{{count}} item" / "{{count}} items"
  checkout.order_summary.subtotal
  checkout.order_summary.discount_applied
  checkout.submit.button_text
  checkout.submit_button_loading

  common.actions.save
  common.actions.cancel
  common.actions.delete
  common.labels.optional
  common.errors.required_field
  common.errors.invalid_email
```

## Translation File Structure

```json
// en.json
{
  "auth": {
    "login": {
      "title": "Sign in to your account",
      "email_label": "Email address",
      "password_label": "Password",
      "submit_button": "Sign in",
      "error": {
        "invalid_credentials": "Incorrect email or password.",
        "account_locked": "Account locked after too many attempts. Try again in {{minutes}} minutes."
      }
    }
  },
  "checkout": {
    "order_summary": {
      "items_count_one": "{{count}} item",
      "items_count_other": "{{count}} items"
    }
  }
}
```

```json
// pt-BR.json
{
  "auth": {
    "login": {
      "title": "Entrar na sua conta",
      "email_label": "Endereço de e-mail",
      "submit_button": "Entrar",
      "error": {
        "invalid_credentials": "E-mail ou senha incorretos.",
        "account_locked": "Conta bloqueada após muitas tentativas. Tente novamente em {{minutes}} minutos."
      }
    }
  },
  "checkout": {
    "order_summary": {
      "items_count_one": "{{count}} item",
      "items_count_other": "{{count}} itens"
    }
  }
}
```

## Date, Number, Currency Formatting

```typescript
// ✅ Correct: locale-aware
const formatCurrency = (amount: number, locale: string, currency: string): string =>
  new Intl.NumberFormat(locale, { style: 'currency', currency }).format(amount)

// BRL: R$ 1.299,90
formatCurrency(1299.90, 'pt-BR', 'BRL')

// USD: $1,299.90
formatCurrency(1299.90, 'en-US', 'USD')

// EUR: 1.299,90 €
formatCurrency(1299.90, 'de-DE', 'EUR')

// ✅ Correct: relative time
const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' })
rtf.format(-1, 'day')  // "yesterday" (en) / "ontem" (pt) / "gestern" (de)

// ❌ Wrong: hardcoded formatting
const price = `R$ ${amount.toFixed(2).replace('.', ',')}` // breaks for non-BRL locales
```

## DO NOT

- **DO NOT** use string concatenation to build translated sentences: `t('hello') + ' ' + username` — word order differs between languages. Use interpolation: `t('hello_user', { name: username })`
- **DO NOT** use text content as translation keys: key `"Save"` breaks when the English text changes
- **DO NOT** assume all text expands < 30% when translated — German and Finnish can be 2× longer than English. Test UI with long strings.
- **DO NOT** use `margin-left`/`margin-right` in CSS if RTL support is planned — use `margin-inline-start`/`margin-inline-end`
- **DO NOT** hardcode locale-specific characters like decimal separators or thousands separators
- **DO NOT** store translated content in the database for every locale unless content is user-generated — keep translations in code/files
- **DO NOT** block translation by requiring a full application build to see string changes — use hot-reloading compatible translation loading

## OUTPUT FORMAT

For each i18n implementation or audit, produce:

**i18n Coverage Report:**
```markdown
## i18n Coverage Report

### Audit Results
- Files scanned: 156 component files
- Hardcoded strings found: 23
- Strings already externalized: 891
- Coverage: 97.5%

### Hardcoded Strings Found
| File | Line | String | Suggested Key |
|------|------|--------|---------------|
| CheckoutButton.tsx | 47 | "Complete Purchase" | checkout.submit.button_text |
| ErrorPage.tsx | 12 | "Something went wrong" | common.errors.generic |

### Plural Rules Missing
| Key | Languages Missing Plural Forms |
|-----|-------------------------------|
| cart.items_count | ru, ar, pl |

### Locales Status
| Locale | Keys Total | Keys Missing | Completeness |
|--------|-----------|-------------|-------------|
| en | 892 | 0 | 100% |
| pt-BR | 892 | 15 | 98.3% |
| es | 892 | 67 | 92.5% |
```

## QUALITY GATES

- [ ] Zero hardcoded user-visible strings in component files (audit via grep or ESLint rule)
- [ ] All date/time formatted with `Intl.DateTimeFormat` or library equivalent
- [ ] All currency amounts formatted with `Intl.NumberFormat` style `currency`
- [ ] Plural forms defined for at least the 2 main target locales
- [ ] Missing translation fallback configured and tested (shows English, not key name)
- [ ] Translation completeness ≥ 95% for all launched locales
- [ ] RTL layout tested if Arabic/Hebrew/Farsi is in scope
- [ ] String with interpolation tested with long values (UI does not break)
- [ ] Translation keys have context/description for translators
- [ ] Locale detection works from browser and can be overridden by user
