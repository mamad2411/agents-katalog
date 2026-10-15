---
name: mustachio
description: "Write correct Mustachio template syntax for Postmark email templates. Use this skill whenever the task involves Postmark templates, Mustachio syntax, or email template HTML that uses {{ }} curly-brace placeholders destined for Postmark. Mustachio looks like Mustache but is a different engine with different rules — this skill prevents you from writing Mustache syntax that silently fails in Mustachio."
---

# Mustachio Templating for Postmark

## Why this skill exists

Mustachio is the templating engine that powers Postmark email templates. It is visually similar to Mustache (both use `{{ }}` curly braces) but it is a **separate engine** with different supported features. Because Mustache dominates training data and Mustachio is comparatively obscure, LLMs consistently generate Mustache syntax when asked to write Mustachio — and the errors are subtle because the two look almost identical. The wrong syntax doesn't throw errors; it silently produces broken output.

This skill is the authoritative reference. When writing or modifying anything that will be processed by Postmark's template engine, follow these rules exactly.

---

## Step Zero: Get the Layout First

Postmark uses a **Layout + Template** architecture. The Layout is a separate Mustachio template that wraps every inner template. It contains:

- The `<html>`, `<head>`, and `<body>` tags
- All shared CSS in `<style>` blocks (Postmark auto-inlines these at send time)
- Common header and footer HTML
- The `{{{ @content }}}` token — this is where the inner template gets injected

The inner template (the part you write) is just the **body content** that gets inserted at `{{{ @content }}}`. It has no `<html>`, `<head>`, `<style>`, or `<body>` tags of its own — those all live in the Layout.

**Why this matters:** The inner template uses CSS classes that are defined in the Layout's `<style>` block. If you don't know what classes exist, you'll either invent class names that don't exist (unstyled output) or add inline styles that conflict with the Layout's design system.

### Before writing any template, always:

1. **Ask the user to paste their Postmark Layout** (the HTML of the Layout template their server uses). Say something like: *"Please paste the Postmark Layout HTML that this template will use. I need to see which CSS classes are available so the template works correctly with your styling."*
2. Read the Layout's `<style>` block to identify all available CSS classes
3. Write the inner template using **only** those CSS classes
4. If the user doesn't have a Layout or wants a standalone template, explicitly confirm this — then you may include full HTML with `<style>` tags, but flag that it won't benefit from Layout-based reuse

### Rules for inner templates (when a Layout is used):

- **Never** include `<!DOCTYPE>`, `<html>`, `<head>`, `<style>`, or `<body>` — the Layout provides these
- **Only** use CSS classes defined in the Layout's stylesheet
- If you need a style not in the Layout, add it as an inline `style=""` attribute and note it to the user as something they may want to add to the Layout for reuse
- The template's HTML starts directly with content elements (e.g., `<div>`, `<table>`, `<h1>`)

---

## The Complete Mustachio Feature Set

Mustachio supports exactly these features and nothing else. If a syntax construct is not listed here, it does not work.

### 1. Variable interpolation (HTML-escaped)
```
{{ name }}
{{ user.address.city }}
```
All output is HTML-encoded by default to prevent XSS.

### 2. Unescaped (raw) output
```
{{{ rawHtml }}}
{{& rawHtml }}
```
Both forms are equivalent. Use sparingly — raw output creates XSS risk in browser contexts.

### 3. Sections (conditional blocks)
```
{{#propertyName}}
  Rendered when propertyName is truthy.
{{/propertyName}}
```
A section renders when its value is present and truthy. Scoping behavior depends on the value type — see "Section Scoping" below.

### 4. Inverted sections (render when falsy/absent)
```
{{^propertyName}}
  Rendered when propertyName is missing, null, false, empty string, or empty array.
{{/propertyName}}
```

### 5. `{{#each}}` loops — the key difference from Mustache
```
{{#each items}}
  {{ name }} — {{ price }}
{{/each}}
```
Arrays are iterated with `{{#each array}}`. This is Mustachio-specific syntax that does not exist in standard Mustache.

In standard Mustache, `{{#array}}...{{/array}}` iterates over the array. **In Mustachio, `{{#array}}` does NOT iterate** — it only performs a truthiness check (non-empty array = truthy). You must use `{{#each array}}` to iterate.

### 6. Dot notation for nested paths
```
{{ order.shipping.address.city }}
```

### 7. Parent scope navigation with `../`
```
{{#each items}}
  {{ ../companyName }}
  {{#each tags}}
    {{ ../../companyName }}
  {{/each}}
{{/each}}
```
Each `../` traverses one scope level up. Works inside `{{#each}}` and inside section blocks.

### 8. Current context self-reference with `.`
```
{{#title}}{{ . }}{{/title}}
```
The dot operator outputs the current scoped value itself. Primarily used inside scalar sections.

### 9. Postmark-specific tokens
```
{{{ @content }}}          — Layout content insertion point
{{{ pm:unsubscribe }}}    — Unsubscribe link (required for Broadcast streams)
```

**That is the complete list.** Everything below this line is something Mustachio does NOT support.

---

## What Mustachio Does NOT Support

These are features from Mustache, Handlebars, or other templating engines that look plausible but **do not work** in Mustachio. Every one of these is a mistake LLMs commonly make.

| Syntax | Engine it belongs to | What to do instead |
|--------|---------------------|--------------------|
| `{{#if condition}}` | Handlebars | Use `{{#property}}` truthiness section |
| `{{else}}` | Mustache/Handlebars | Use `{{^property}}` inverted section |
| `{{#unless condition}}` | Handlebars | Use `{{^property}}` |
| `{{> partialName}}` | Mustache | Not available in Postmark |
| `{{#helper}}{{val}}{{/helper}}` | Handlebars | No lambdas or helper functions |
| `{{ val \| filter }}` | Liquid/Nunjucks | No filters or pipes |
| `{{! comment }}` | Mustache | Not documented as supported — do not use |
| `{{=<% %>=}}` | Mustache | Cannot change delimiters |
| `{{$block}}...{{/block}}` | Mustache inheritance | Not supported |
| `{{ a + b }}` | Expression engines | No arithmetic in templates |
| `{{#if x > 5}}` | Handlebars | No comparison operators |

**The golden rule:** Mustachio handles display and conditional show/hide only. All data transformation, formatting, arithmetic, and comparison logic must happen server-side before reaching the template.

---

## Section Scoping — The Most Important Concept

Sections (`{{# }}`) behave differently depending on the data type of the value. Getting this wrong produces silent bugs. There are two cases:

### Scalar sections (value is a string, number, or boolean)

When a section opens on a scalar value, the scope changes to that scalar. Inside the section:
- `{{ . }}` outputs the scalar value itself
- **All other variable references require `../`** to navigate back to the parent scope — they will NOT auto-resolve

**This is the #1 source of silent bugs.** It is tempting to write `{{#isActive}}{{ name }}{{/isActive}}` thinking "it's just a boolean gate, scope doesn't change." It does. `{{ name }}` resolves to nothing. You must write `{{ ../name }}`.

```
Model:   { orderId: "ORD-5521", isUrgent: "YES", customer: "Acme" }

-- Access the scalar value itself with {{ . }}
Template: Order{{#orderId}} {{ . }}{{/orderId}}
Output:   Order ORD-5521

-- Access sibling data: MUST use ../
Template: {{#isUrgent}}URGENT: Order {{ ../orderId }} for {{ ../customer }}{{/isUrgent}}
Output:   URGENT: Order ORD-5521 for Acme

-- WRONG: missing ../ — silently outputs nothing for orderId
Template: {{#isUrgent}}URGENT: Order {{ orderId }}{{/isUrgent}}
Output:   URGENT: Order
```

**Rule: Inside ANY section (scalar or object), always use `../` to access properties from the parent scope.**

### Object sections (value is an object)

When a section opens on an object, the scope changes INTO the object. Inside the section, you access child properties by name — without the parent path prefix.

```
Model:   { shipping: { method: "Express", cost: "12.50" } }

Template: {{#shipping}}{{ method }} — {{ cost }} EUR{{/shipping}}
Output:   Express — 12.50 EUR
```

To reach properties outside the current scope, use `../`:
```
{{#shipping}}
  {{ method }} for order {{ ../orderId }}
{{/shipping}}
```

### Choosing the right pattern

| Situation | Template pattern |
|-----------|-----------------|
| Show value only if present | `{{#discount}}{{ . }}{{/discount}}` |
| Show value with surrounding text | `{{#discount}}You save {{ . }}{{/discount}}` |
| Show section with multiple child values | `{{#shipping}}{{ method }}: {{ cost }}{{/shipping}}` |
| Show/hide block (no value needed) | `{{#isPremium}}Premium Member{{/isPremium}}` |
| Show/hide block, access sibling data | `{{#isPremium}}{{ ../memberName }}{{/isPremium}}` |

---

## If/Else Logic Without `if` or `else`

Mustachio has no `if`/`else` keywords. Use a section immediately followed by its inverted counterpart:

```
{{#hasAccount}}
  Welcome back!
{{/hasAccount}}
{{^hasAccount}}
  Create an account to get started.
{{/hasAccount}}
```

This is the only way to implement either/or logic. The `{{#prop}}` block renders when truthy; the `{{^prop}}` block renders when falsy. Together they cover both cases.

---

## Truthiness Rules

All conditional logic in Mustachio works through truthiness checks. There is no other conditional mechanism.

| Value | Truthy? | `{{#x}}` renders? | `{{^x}}` renders? |
|-------|---------|--------------------|--------------------|
| `"hello"` (non-empty string) | Yes | Yes | No |
| `""` (empty string) | No | No | Yes |
| `true` | Yes | Yes | No |
| `false` | No | No | Yes |
| `null` | No | No | Yes |
| Property absent from model | No | No | Yes |
| `{ key: "val" }` (object) | Yes | Yes (scopes in) | No |
| `{}` (empty object) | Yes | Yes (scopes in, no children) | No |
| `[item1, item2]` (non-empty array) | Yes | Yes (does NOT iterate) | No |
| `[]` (empty array) | No | No | Yes |

Key subtlety: `{}` (empty object) is **truthy** — it will cause a `{{#section}}` to render. And non-empty arrays are truthy but `{{#array}}` does NOT iterate — always use `{{#each array}}` to loop.

---

## Long Values Breaking Layout Width

Postmark Layouts typically constrain the email body to a fixed width (e.g. 570px). Long unbroken strings — URLs, API keys, file paths, hashes — contain no spaces or hyphens, so the browser/email client cannot word-wrap them. The string forces its table cell wider than the Layout container, breaking the entire email layout.

**Fix:** Add `word-break: break-all` to any `<td>` that may contain long unbroken values:

```html
<tr>
  <td class="attributes_item" style="word-break: break-all;">
    <strong>Target URL:</strong> {{ targetUrl }}
  </td>
</tr>
```

Apply this proactively to cells displaying URLs, tokens, file paths, or any value likely to exceed ~60 characters without whitespace. It is better to add `word-break: break-all` unnecessarily than to ship a layout-breaking email.

---

## Quick Self-Check

Before considering any template complete, verify:

1. **Layout compatibility:** If a Layout is in use, the template has no `<!DOCTYPE>`, `<html>`, `<head>`, `<style>`, or `<body>` tags — and only uses CSS classes from the Layout
2. No `{{#if`, `{{else}}`, `{{#unless` anywhere
3. Every array uses `{{#each arrayName}}`, never `{{#arrayName}}`
4. No `{{> partial}}` references
5. No helpers, filters, pipes, or functions in template expressions
6. Inside scalar sections, values are accessed with `{{ . }}`
7. Inside object sections, child properties are accessed by name (not `.`)
8. **Every variable inside a `{{#section}}` that refers to a sibling/parent property uses `../`** — this applies to BOTH scalar and object sections
9. All formatting is done server-side, not in the template
10. **Cells containing URLs, tokens, or other long unbroken strings** have `style="word-break: break-all;"` to prevent layout overflow
