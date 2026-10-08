---
name: liferay-ddm-field-validation
description: >
  Use this skill whenever the user wants to add, understand, or debug validation rules on a
  Dynamic Data Mapping (DDM) / Data Engine field — including fields on Document Types
  (DLFileEntryType), Objects, or the Forms app, since they all share the same underlying DDM
  engine. Trigger for "add a validator to this field", "email/regex validation on a field", "is
  validation enforced server-side", "create a custom validator", "how do I add a new option to
  the Validation dropdown", "DDMValidation", "customProperties.validation", "show/hide field
  based on another field", "dataRules", or any work touching a field's `validation` JSON
  property in a `*.batch-engine-data.json` payload, a Document Type/Object field definition, or
  a custom `DDMValidation`/`DDMExpressionFunction` OSGi component.
---

# Liferay DDM Field Validation Skill

> Source citations below reference `$LIFERAY_PORTAL`, the dynamically-resolved Liferay Portal
> source checkout — see the `liferay-portal-source` skill to resolve/bootstrap it.

## 1. Two distinct mechanisms — know which one you need

| | Declarative expression validation | Custom `DDMValidation` type |
|---|---|---|
| Where it lives | `customProperties.validation` on one field | New OSGi component, registered instance-wide |
| Needs Java/OSGi? | No | Yes |
| Scope | That one field only | Every field sharing the same `dataType`, portal-wide |
| Use when | You need *a* validation rule (built-in or a regex) on *this* field | You want a NEW reusable, named option to appear in the "Validation" dropdown |

Both are enforced by the same backend validator, so both are real server-side guarantees, not
just UI polish (Section 4 covers the one thing that is *not* backend-enforced — Client
Extension DOM tricks).

## 2. Declarative field validation (no code)

Confirmed end-to-end from source, not from docs:

- `customProperties.validation` on a `DataDefinitionField` is converted into a real
  `DDMFormFieldValidation` by
  `DataDefinitionDDMFormUtil._getDDMFormFieldValidation` (`$LIFERAY_PORTAL/modules/apps/data-engine/data-engine-rest-api/src/main/java/com/liferay/data/engine/rest/dto/v2_0/util/DataDefinitionDDMFormUtil.java#L166-L198`),
  dispatched whenever a `customProperties` key's registered settings field type is
  `"validation"` (`dispatch site, line 292-298` (`$LIFERAY_PORTAL/modules/apps/data-engine/data-engine-rest-api/src/main/java/com/liferay/data/engine/rest/dto/v2_0/util/DataDefinitionDDMFormUtil.java#L292-L298`)).
- That `DDMFormFieldValidation` is enforced **server-side**, unconditionally, by
  `DDMFormValuesValidatorImpl` (`$LIFERAY_PORTAL/modules/apps/dynamic-data-mapping/dynamic-data-mapping-validator/src/main/java/com/liferay/dynamic/data/mapping/validator/internal/DDMFormValuesValidatorImpl.java`)
  — the one shared validator the whole Data Engine funnels through (Document Types, Objects,
  Forms all use it), not something wired into just one UI screen. It cannot be bypassed by
  calling headless REST or JSONWS directly instead of the UI form.

### JSON shape (verified working against a live Document Type field)

```json
{
  "fieldType": "text",
  "name": "dt_owner_email",
  "customProperties": {
    "fieldReference": "dt_owner_email",
    "dataType": "string",
    "validation": {
      "expression": {
        "name": "expression",
        "value": "isEmailAddress(dt_owner_email.value())"
      },
      "errorMessage": {"en_US": "Enter a valid email address"}
    }
  }
}
```

The expression is DDM Expression Language and can reference *other* fields in the same form by
name (e.g. `if (dt_category.value() == 'form') { ... }`) — so "field B is required only when
field A = X" is expressible as a validation expression on field B itself, and stays
backend-enforced (unlike the `dataRules` show/hide mechanism in Section 5).

**Built-in expression functions already registered as OOTB `DDMValidation` types** — use these
directly instead of reinventing them: `isEmailAddress()`, `isURL()`, `matches()` (regex), plus
comparison/date-range ones (`IsEqualTo`, `IsGreaterThan`, `IsLessThan`, `Contains`,
`FutureDates`, `PastDates`, etc.). Full list and their exact `getTemplate()` strings:
`validation package` (`$LIFERAY_PORTAL/modules/apps/dynamic-data-mapping/dynamic-data-mapping-form-evaluator-impl/src/main/java/com/liferay/dynamic/data/mapping/form/evaluator/internal/validation/`).

## 3. Custom validator (`DDMValidation` OSGi component) — new dropdown option, instance-wide

Only build this when you want a NEW named, reusable validator to appear as a selectable option
in the field settings' "Validation" dropdown (same UI slot as "Email"/"URL"/"Matches"), instead
of hand-writing a raw expression once on one field.

Interface:
`DDMValidation` (`$LIFERAY_PORTAL/modules/apps/dynamic-data-mapping/dynamic-data-mapping-api/src/main/java/com/liferay/dynamic/data/mapping/form/validation/DDMValidation.java`)

```java
@Component(
	property = {
		"ddm.validation.data.type=string",
		"ddm.validation.ranking:Float=4"
	},
	service = DDMValidation.class
)
public class IsEmailDDMValidation implements DDMValidation {

	public String getName() {
		return "email";
	}

	public String getLabel(Locale locale) {
		return _language.get(
			ResourceBundleUtil.getModuleAndPortalResourceBundle(locale, getClass()),
			"is-an-email");
	}

	public String getTemplate() {
		return "isEmailAddress({name})";
	}

	public String getParameterMessage(Locale locale) {
		return StringPool.BLANK;
	}
}
```

Real OOTB example this was copied from:
`IsEmailDDMValidation.java` (`$LIFERAY_PORTAL/modules/apps/dynamic-data-mapping/dynamic-data-mapping-form-evaluator-impl/src/main/java/com/liferay/dynamic/data/mapping/form/evaluator/internal/validation/IsEmailDDMValidation.java`).
Other OOTB implementations live in the same package — copy whichever is closest to the new rule
(e.g. `MatchesDDMValidation` for a parameterized regex) rather than starting from scratch.

### How it binds to a field — confirmed by tracing the consumer, not assumed

`DDMFormTemplateContextFactoryImpl` (`$LIFERAY_PORTAL/modules/apps/dynamic-data-mapping/dynamic-data-mapping-form-renderer/src/main/java/com/liferay/dynamic/data/mapping/form/renderer/internal/DDMFormTemplateContextFactoryImpl.java#L152-L156`)
builds a `ServiceTrackerMap<String, List<DDMValidation>>` keyed by the `ddm.validation.data.type`
component property (grouped by **data type** — `string`/`integer`/`double`/`date`/etc — **not**
by DDM Form Field Type like `text`/`select`), ordered by `ddm.validation.ranking`, and puts the
result into the template context
(`line 354` (`$LIFERAY_PORTAL/modules/apps/dynamic-data-mapping/dynamic-data-mapping-form-renderer/src/main/java/com/liferay/dynamic/data/mapping/form/renderer/internal/DDMFormTemplateContextFactoryImpl.java#L354`))
that renders the field settings' Validation dropdown. `getTemplate()`'s `{name}` placeholder is
substituted with the actual field name at runtime — the resulting string is exactly what ends up
as `customProperties.validation.expression.value` from Section 2, so it goes through the same
`DDMFormValuesValidatorImpl`, same backend guarantee.

**Binding key point:** you bind to `dataType` (string/integer/double/date/boolean/...), not to
one specific field type or one specific Document Type/Object. A new `string`-scoped validator
becomes selectable on every string-backed field across the whole instance at once — there is no
way to scope a `DDMValidation` component to a single Document Type or a single field.

**Complexity ceiling:** `getTemplate()` can only call DDM Expression Language functions. If the
rule needs something an expression can't express (a uniqueness check against the database, a
call to an external system), pair this with a custom `DDMExpressionFunction` OSGi component too
— same module, one more extension point, not covered in depth here.

## 4. Not achievable via Client Extension — confirmed, not assumed

Checked every registered `@CETType` in
`client-extension-type-api` (`$LIFERAY_PORTAL/modules/apps/client-extension/client-extension-type-api/src/main/java/com/liferay/client/extension/type/`):
`fdsCellRenderer`, `fdsFilter`, `customElement`, `iframe`, `themeCSS`, `globalJS`, `globalCSS`,
`staticContent`, `themeFavicon`, `jsImportMapsEntry`, `themeSpritemap`, `commerceCheckoutStep`,
`audiencesCustomAttributes`, `editorConfigContributor`. None of them hook into `DDMValidation`,
`DDMExpressionFunction`, or any other DDM/Data Engine backend extension point — same absence
confirmed separately for the actual field *editor* component registry (each DDM Form Field Type,
e.g. `Text.es.js` under `dynamic-data-mapping-form-field-type`, is a bundled portal OSGi module
JS resource with no CX-pluggable seam). Both mechanisms in this skill genuinely require a
traditional OSGi module — this is one of the few real cases (per this project's CLAUDE.md
escalation rule: "only suggest traditional OSGi modules if Client Extensions cannot fulfill the
requirements") where that escalation is justified rather than reached for by default.

What a `globalJS` Client Extension *can* still do instead, if backend enforcement isn't
required: add **client-side-only** UX on top of an existing field's already-rendered `<input>`
— formatting help, a live character count, a soft inline warning, or (a stronger option, see
below) an actual blocked submit. See the `liferay-global-extension` client extension in this
workspace (`client-extensions/liferay-global-extension/`, sample under
`src/extensions/documentType/managedDocument/`) for the pattern: screen detection via
`p_p_id`/`mvcRenderCommandName` query params, field targeting via a `ddm$$<fieldName>$`
substring marker restricted to `input`/`select`/`textarea` tags (a bare `[id*=...]` selector
without the tag restriction can match a field's own `<label>` when it has an `id` for
`aria-labelledby` — a real bug found live, not hypothetical), `Liferay.Service` for JSONWS calls,
and a `MutationObserver` because DLAdminPortlet's edit form re-renders via AJAX without a full
page reload.

**None of this is backend-enforced and all of it can be bypassed by any direct API call** — use
it only for UX affordances or blocking the UI's own submit path, never as the actual validation
guarantee; pair it with Section 2 or 3 for anything that must actually hold regardless of client.

**A genuinely stronger client-side-only option than a passive warning: capture-phase `submit`
interception, to actually block the Publish button.** `edit_file_entry.jsp`'s form uses a
property-based `onSubmit` handler (`onSubmit="event.preventDefault(); <namespace>saveFileEntry
(...)"`), which per the DOM event spec always fires *after* any capture-phase listener on an
ancestor. So `document.addEventListener('submit', handler, {capture: true})`, checking a custom
condition and calling `event.preventDefault(); event.stopImmediatePropagation()`, reliably stops
Liferay's own `onSubmit` — and therefore the actual save — from ever running, before the user
ever leaves the page. This is standard, version-independent DOM behavior, not reliant on
Liferay's internal naming (unlike the tempting-but-rejected alternative: monkey-patching
`window['<namespace>saveFileEntry']` directly — an undocumented internal global that could change
across versions or get silently redefined if Liferay re-executes its inline `<aui:script>` block
on an AJAX re-render, undoing the patch with no `activate()`/`deactivate()` transition to notice
it by). Still purely client-side — a direct API call bypassing the UI is untouched — but it's the
right technique when "block this specific UI's submit button" is genuinely the whole ask, as
opposed to "prevent this value from ever being invalid anywhere."

## 5. `dataRules` (show/hide, dependent-field UI rules) — real mechanism, but blocked for Document Types

`DataLayout.dataRules` (`actions`/`conditions`/`logicalOperator` — see
`DataRule.java` (`$LIFERAY_PORTAL/modules/apps/data-engine/data-engine-rest-api/src/main/java/com/liferay/data/engine/rest/dto/v2_0/DataRule.java`))
is the mechanism for show/hide/enable/disable/require-field rules between fields on the same
form — Data Engine's own Form Rules feature. Confirmed genuinely useful for "field B required
only when field A = X" **and** genuinely client-side-only (see the nuance at the end of this
section) — but there's a real access blocker specific to Document Types, found while trying to
use it.

### The exact JSON shape on `dataLayout.dataRules` is still unverified — but the underlying action/condition syntax now is

No populated `dataRules` fixture exists anywhere in the portal source tree, and a live PATCH test
to check the REST JSON syntax was correctly blocked by the harness (mutating a real resource just
to confirm shape needs explicit user permission first, even on a disposable resource) — so don't
hand-write a `dataLayout.dataRules` REST payload from a guessed shape.

What **is** now confirmed, from real non-test source (`DDMRESTDataProviderSettings.java`), is the
underlying expression/action syntax Form Rules are built from — the same DDM Expression Language
engine covers both this and Section 2's `validation` expressions. It's a **custom ANTLR4 grammar**
(`dynamic-data-mapping-expression` module's `DDMExpression.g4`), not MVEL/JEXL, evaluated by
`DDMExpressionImpl`/`DDMExpressionFactoryImpl`. Confirmed supported syntax: `&&`/`and`, `||`/`or`,
`not` (prefix only, no unary `!`), `==`/`!=`/`>`/`>=`/`<`/`<=`, `+ - * /`, parentheses, string/
number/boolean literals, array literals `[1,2,3]`, function calls, bare identifiers as field
references. **No `if/else`, no ternary `?:`** — it's expression-only. Real confirmed
cross-field example (a `@DDMFormRule` action string, referencing a *different* field):

```java
actions = {"setRequired('paginationStartParameterName', equals(getValue('pagination'), true))"}
```

`getValue('OtherField')` is the confirmed way to read another field from within a rule
expression — this is the annotation-based Java form, so whether the REST API's `dataLayout.
dataRules` JSON uses these same raw strings or wraps them into structured `actions: Map[]`/
`conditions: Map[]` objects is still the one open unknown. Get the real JSON shape one of two
ways, same as before — **but see the blocker below before reaching for method 1**:

1. Build one rule through the Control Panel's Data Layout designer UI (the drag-and-drop rule
   builder), then `GET /o/data-engine/v2.0/data-layouts/{id}` to read back the canonical JSON
   Liferay itself produced. **Does not work for Document Types or Journal (Web Content) —
   see below.** Works for the standalone Forms app.
2. Ask the user for explicit permission to test-PATCH a disposable/test data layout directly via
   the REST API (bypassing the missing UI), inspect the round-trip, then restore the original
   value. Untested whether the REST resource accepts/persists `dataRules` for
   `content.type=document-library` at all, or whether the runtime form renderer (a separate
   component from the builder) would honor it if present — a real next step if this matters.

### Document Types (and Journal) have no Rules builder UI at all — confirmed from source, not a discoverability issue

`DataLayoutBuilderDefinition.allowRules()` (default `false`,
`interface` (`$LIFERAY_PORTAL/modules/apps/data-engine/data-engine-taglib/`) —
per-`content.type` OSGi component) gates whether the Data Layout Builder's Rules sidebar panel
gets sent to the browser at all. `document-library-web`'s
`DocumentLibraryDataLayoutBuilderDefinition` (backing Document Type field editing,
`content.type=document-library`) never overrides it, so it inherits `false`. Confirmed in
`DataLayoutBuilderTag._getSidebarPanels()`: when the flag is off, the "rules" panel entry is
`null` — never rendered, not hidden behind an easy-to-miss button. `JournalDataLayoutBuilderDefinition`
(Web Content structures) explicitly sets it to `false` too. The standalone Forms app is the
exception — it doesn't even use this builder component; it uses an older, separate
`<ddm-form-builder>` taglib with rules hard-enabled (`initialConfigState.es.js`:
`allowRules: true`).

**Important nuance even once the real REST JSON shape is known:** `dataRules` show/hide/enable/
disable/require is evaluated **entirely client-side**, by Data Engine's own form JS — genuinely
useful as a front-end-only enforcement mechanism (it reuses Data Engine's native "required"
UI/blocking, not a hand-rolled one), but by itself never a backend guarantee, unlike Sections 2
and 3. Confirmed: a `setRequired` rule does not touch the field's static `required` DB flag, so
`DDMFormValuesValidatorImpl` never sees it — a direct API call bypassing the UI sails through
untouched. If a field must actually be *required* regardless of client, express that as a
validation expression on the dependent field itself (Section 2) — `dataRules` and Section 2's
expressions are not substitutes for each other; they enforce at different layers (UI vs. server)
and can be used together.
