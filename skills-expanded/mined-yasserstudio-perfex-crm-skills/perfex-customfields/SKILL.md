---
name: perfex-customfields
description: Use whenever the user is reading, writing, installing, or debugging Perfex CRM custom fields — `tblcustomfields` (definitions), `tblcustomfieldsvalues` (values keyed by `relid`), field types (`input`, `textarea`, `number`, `select`, `multiselect`, `checkbox`, `date_picker`, `date_picker_time`, `link`, `colorpicker`), `fieldto` values (`contacts`, `customers`, `leads`, `invoice`, `estimate`, `contracts`, `tasks`, `tickets`, etc.), `only_admin` visibility, `show_on_client_portal`, `bs_column`, the intentionally-misspelled `disalow_client_to_edit` column, `render_custom_fields()`, `get_custom_field_value()`, or `handle_custom_fields_post()`. Also trigger when the user says "my custom field isn't showing in the client portal", "I added a custom field in code but it doesn't appear", "custom field value not saving", "only_admin isn't respected", or "Perfex custom field types". Preserves the `disalow_client_to_edit` typo that Perfex core queries by exact name.
license: MIT
metadata:
  author: yasserstudio
  version: "1.5.0"
---

# Perfex Custom Fields

You are a Perfex CRM custom-fields specialist. Your job is to read, write, and install custom fields against `tblcustomfields` and `tblcustomfieldsvalues` without tripping over Perfex's quirks — the misspelled `disalow_client_to_edit` column, `only_admin` visibility, `bs_column` Bootstrap sizing, and module-prefixed slug conventions.

Custom fields are Perfex's extensibility mechanism for adding user-defined fields to contacts, clients, leads, invoices, tickets, and most core entities. Two tables: `tblcustomfields` (definitions) and `tblcustomfieldsvalues` (values keyed by `relid`).

## Schema gotchas (critical)

### `only_admin` — NOT `only_admin_area`

The column is `only_admin`. Some older docs and Stack Overflow answers refer to `only_admin_area` — that's wrong. Don't alias, don't "fix".

### `disalow_client_to_edit` — the typo is canonical

Yes, it's misspelled (missing 'l' after 'disa'). **Preserve it.** Perfex core queries this exact column name. If you rename it, core breaks. If you write an abstraction over it, leave the DB column alone and only alias in PHP.

### Full definition-row shape

When inserting a custom field programmatically:

```php
$CI->db->insert(db_prefix() . 'customfields', [
    'fieldto'               => 'contacts',           // company | customers | contacts | leads | invoice | estimate | credit_note | proposal | contracts | expenses | projects | tasks | tickets | staff | items
    'name'                  => 'Account Tier',
    'slug'                  => 'contacts_account_tier',   // unique per fieldto; VARCHAR(150)
    'required'              => 0,
    'type'                  => 'input',              // input | textarea | number | select | multiselect | checkbox | date_picker | date_picker_time | link | colorpicker  (no 'date', 'datetime' or 'file')
    'options'               => '',                   // COMMA-separated for select/multiselect/checkbox; '' otherwise
    'display_inline'        => 0,
    'field_order'           => 0,
    'active'                => 1,
    'show_on_pdf'           => 0,                    // only honoured for fieldto in the model's $pdf_fields list
    'show_on_ticket_form'   => 0,                    // tickets only: show on the public ticket form
    'only_admin'            => 0,                    // 1 = hidden unless is_admin()
    'show_on_table'         => 0,                    // extra column in the admin datatable
    'show_on_client_portal' => 1,
    'disalow_client_to_edit'=> 0,                    // ← preserve the typo
    'bs_column'             => 12,                   // 12 | 6 | 4 | 3 — Bootstrap grid width (INT)
    'default_value'         => '',                   // 2.8.3+ (migration 283)
]);
```

That is the **complete** column list as of 3.4 (18 columns including `id`). There is no `show_on_picker`, `has_permission_view` or `permission_view` — inserting them throws `Unknown column`. Per-staff visibility of custom fields doesn't exist in core; agents borrow those names from other CRMs.

### Module-owned custom fields — convention

Prefix your module's slugs with the module name and the entity:

```
onboarding_passport_number      → contacts.onboarding_passport_number
mymodule_plan_type              → customers.mymodule_plan_type
```

This prevents slug collisions with core and other modules.

## Reading values

Values live in `tblcustomfieldsvalues` keyed by **`(fieldid, relid, fieldto)`** — yes, `fieldto` is duplicated onto the values row, and core filters on it. `relid` is the ID of the parent record (contact ID, invoice ID, etc.).

Use the core helper — it accepts a **slug or a numeric ID** in the second argument:

```php
// helper signature: get_custom_field_value($rel_id, $field_id_or_slug, $field_to, $format = true)
$plan = get_custom_field_value($contact_id, 'mymodule_plan', 'contacts');
$raw  = get_custom_field_value($invoice_id, 'invoice_due_note', 'invoice', false); // skip date formatting
```

Returns `''` (empty string, not `null`) when there's no value. With `$format = true` (default), `date_picker` / `date_picker_time` values come back through `_d()` / `_dt()` in the user's display format — pass `false` when you need the raw `Y-m-d` for comparisons.

Don't hand-roll a JOIN for this; the helper already does it and applies the `fieldto` filter you'd forget.

## Writing values

For values coming from a form, use the core helper that Perfex's own controllers use:

```php
// $_POST['custom_fields'] is ['contacts' => [<field_id> => value, ...]]
handle_custom_fields_post($contact_id, $this->input->post('custom_fields'));
```

It applies the type-specific normalisation (`to_sql_date()` for pickers, `nl2br()` for textareas, `implode(', ', …)` — comma **and space** — for checkbox/multiselect, so stored values look like `A, B`) and upserts. If you're setting a value programmatically by slug, write the same row shape core does — **including `fieldto`**, or `get_custom_field_value()` and the admin UI will never find it:

```php
public function set_custom_field_value($fieldto, $relid, $slug, $value) {
    $field = $this->db->select('id')
        ->where(['fieldto' => $fieldto, 'slug' => $slug])
        ->get(db_prefix() . 'customfields')->row();
    if (!$field) return false;

    $key = ['fieldid' => $field->id, 'relid' => $relid, 'fieldto' => $fieldto];

    if ($this->db->where($key)->count_all_results(db_prefix() . 'customfieldsvalues') > 0) {
        $this->db->where($key)->update(db_prefix() . 'customfieldsvalues', ['value' => $value]);
    } else {
        $this->db->insert(db_prefix() . 'customfieldsvalues', $key + ['value' => $value]);
    }
    return true;
}
```

Item custom fields are the exception: values for predefined items (Sales → Items) are stored with `fieldto = 'items_pr'`, not `'items'`.

## Field types — what the `type` column means

| type               | `options` format   | Storage in value column |
|--------------------|--------------------|-------------------------|
| `input`            | —                  | plain string |
| `textarea`         | —                  | string, `nl2br()` applied on save |
| `number`           | —                  | numeric string |
| `select`           | `Opt1,Opt2,…`      | the selected string |
| `multiselect`      | `Opt1,Opt2,…`      | `A, B` — comma+space joined |
| `checkbox`         | `Opt1,Opt2,…`      | `A, B` — comma+space joined |
| `date_picker`      | —                  | `YYYY-MM-DD` |
| `date_picker_time` | —                  | `YYYY-MM-DD HH:MM:SS` |
| `link`             | —                  | URL string |
| `colorpicker`      | —                  | hex string `#rrggbb` |

`options` is **comma-separated** — not JSON, not newline-separated. Core does `explode(',', $options)` and `trim()`s each entry, so an option value can't contain a comma. There is no `date`, `datetime`, or `file` type; agents invent those from other CRMs.

## Bootstrap column width (`bs_column`)

Controls visual width in the admin/client form. Allowed values: `12`, `6`, `4`, `3` (INT column, default 12). Sets the Bootstrap 3 grid class `col-md-N`; `0`/empty falls back to 12 at render time.

## Programmatically installing fields in a module

In your `install.php`:

```php
$fields = [
    [
        'fieldto' => 'contacts',
        'slug'    => 'mymodule_plan',
        'name'    => 'Plan',
        'type'    => 'select',
        'options' => 'Basic,Pro,Enterprise',   // comma-separated
        'bs_column' => 6,
    ],
    // ...
];

foreach ($fields as $f) {
    $exists = $CI->db->where(['fieldto' => $f['fieldto'], 'slug' => $f['slug']])
        ->get(db_prefix() . 'customfields')->num_rows();
    if ($exists) continue;

    $CI->db->insert(db_prefix() . 'customfields', array_merge([
        'required' => 0, 'active' => 1, 'only_admin' => 0,
        'disalow_client_to_edit' => 0, 'show_on_client_portal' => 1,
        'display_inline' => 0, 'field_order' => 0, 'show_on_pdf' => 0,
        'show_on_ticket_form' => 0, 'show_on_table' => 0,
        'default_value' => '', 'bs_column' => 12, 'options' => '',
    ], $f));
}
```

## Rendering in a custom view

Perfex ships `render_custom_fields($belongs_to, $rel_id = false, $where = [], $items_cf_params = [])`. The **third argument is a `$where` array** passed straight to `$db->where()` on `tblcustomfields` — it is not an options bag.

```php
<!-- admin view: everything active for this entity -->
<?= render_custom_fields('contacts', $contact_id); ?>

<!-- client-area view: what core's own theme views do -->
<?= render_custom_fields('contacts', $contact_id, ['show_on_client_portal' => 1]); ?>
```

What the helper enforces on its own, and what it doesn't:
- `only_admin = 1` fields are skipped when `is_admin()` is false — automatic.
- `disalow_client_to_edit = 1` renders the input `disabled` when `is_client_logged_in()` — automatic.
- `show_on_client_portal` is **not** checked by the helper. If you omit `['show_on_client_portal' => 1]` in a client-area view, portal-hidden fields render. Core's `contact.php` / `company_profile.php` pass it explicitly; copy that.
- Wrap the output in a `<form>` whose POST is handled by `handle_custom_fields_post()` — the inputs are named `custom_fields[<fieldto>][<id>]`.

`get_custom_fields($field_to, $where = [], $exclude_only_admin = false)` gives you the same filtered definition list when you need to render by hand (e.g. a table column per field).

## Required item custom fields (Perfex 3.3.0+)

As of Perfex 3.3.0, **required item custom fields on select inputs are now enforced** server-side. Previously, marking an item custom field as `required` only triggered client-side validation (which could be bypassed). Now:

- If `fieldto = 'items'` and `required = 1` and `type = 'select'`, Perfex validates on save
- Empty select values are rejected with a validation error
- This applies to invoice items, estimate items, and proposal items

If your module programmatically creates invoice items, ensure you populate all required item custom fields or the save will fail silently in older code paths that don't check for validation errors.

## Don't assume core columns haven't drifted

Older Perfex installs may lack later columns (`show_on_client_portal` arrived in 1.0.7, `only_admin` in 1.1.8, `bs_column` in 1.2.8, `default_value` in 2.8.3). Before writing migration or install code that references them, run:

```sql
SHOW COLUMNS FROM `tblcustomfields`;
```

If your code will run on older installs, wrap inserts with defensive column inclusion (only set a column if `$CI->db->field_exists()` says so).

## Related skills

- **`perfex-database`** — `tblcustomfields` schema (`only_admin`, `disalow_client_to_edit`) and why you can't "fix" the typo.
- **`perfex-module-dev`** — programmatically installing fields in a module's `install.php`.
- **`perfex-core-apis`** — `_l()` for localized field labels when rendering.

## Upstream docs

- Perfex custom fields: https://help.perfexcrm.com/custom-fields/

---

*Verified against Perfex CRM 3.4.0 core source on 2026-09-15 with `scripts/verify-against-core.sh`. Version-specific notes in the text are from official changelogs.*
