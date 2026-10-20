---
name: i18n-message-key-discipline
description: Use static, namespaced next-intl message keys present in every locale file before use. Never build keys by string concatenation — it defeats type-checking and silently misses translations.
---

# Message-key discipline

Dynamically built message keys (`t(\`status.${value}\`)`) can't be type-checked or statically verified, so a missing translation only surfaces at runtime as a raw key or a thrown error. Keys must be static and present in every locale.

## Rules

- Keep keys **static literals** passed to `t('...')` — never concatenate or interpolate to build a key. Map a variable to a fixed key with a lookup object instead.
- Organize keys into **nested namespaces** by feature/component (`useTranslations('ProductCard')`), not one flat global file; scope each `useTranslations` call to the namespace it needs.
- A key MUST exist in **every** locale file before it's referenced in code — add the key to all locales in the same change, not just the default.
- Treat the default-locale file as the schema: every other locale file MUST have the identical key shape (enable next-intl's typed messages so missing keys are a compile error).
- Pass dynamic values as **ICU placeholders** (`t('greeting', { name })`), never by building the message text or key from the value.

## Examples

```ts
// BAD — key built from a runtime value: untype-checkable, and a new status ships an empty string
const label = t(`order.status.${order.status}`)

// GOOD — static keys; the variable selects a fixed key via a lookup
const STATUS_KEY = { paid: 'order.statusPaid', shipped: 'order.statusShipped' } as const
const label = t(STATUS_KEY[order.status])

// GOOD — namespaced hook + ICU placeholder for the dynamic part
const t = useTranslations('Cart')
t('itemCount', { count })   // key is static; `count` is interpolated by ICU, not concatenated
```

```jsonc
// messages/en-GB.json and messages/de-DE.json MUST share the same key shape
{ "Cart": { "itemCount": "{count, plural, one {# item} other {# items}}" } }
```

## Gotchas

- next-intl throws (or renders the raw key) for a missing key at runtime — without typed messages, a missing translation in one locale passes CI and breaks only that locale in production.
- Pluralization and gender belong in ICU syntax inside the message, not in branching `t()` calls in code.
