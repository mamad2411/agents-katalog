---
name: rgaa-forms
description: "Audit a web page for RGAA v4.1.2 Theme 11 – Forms accessibility compliance. Checks that form fields have labels, labels are relevant and visible, labels are properly associated, related fields are grouped with fieldset/legend, select options are grouped, buttons have relevant names, input validation is accessible and helpful, error suggestions are provided, and autocomplete attributes are used. Use this skill when someone asks to check form accessibility, verify RGAA Theme 11, audit form labels, or check form validation accessibility."
---

# RGAA Forms Accessibility Audit (Theme 11)

Audits a web page against the 13 criteria of RGAA v4.1.2 Theme 11: Forms.

## Audit procedure

### Step 1: Gather form data

```javascript
(() => {
  const forms = [];

  document.querySelectorAll('form, [role="form"]').forEach((form, fi) => {
    const fields = [];
    form.querySelectorAll('input, select, textarea, [role="checkbox"], [role="radio"], [role="combobox"], [role="listbox"], [role="slider"], [role="spinbutton"], [role="textbox"], [role="switch"]').forEach(el => {
      const id = el.id;
      const associatedLabel = id ? document.querySelector(`label[for="${id}"]`) : null;
      const parentLabel = el.closest('label');

      fields.push({
        tag: el.tagName.toLowerCase(),
        type: el.type || el.getAttribute('role'),
        id: id,
        name: el.name,
        required: el.required || el.getAttribute('aria-required'),
        ariaLabel: el.getAttribute('aria-label'),
        ariaLabelledby: el.getAttribute('aria-labelledby'),
        ariaDescribedby: el.getAttribute('aria-describedby'),
        ariaInvalid: el.getAttribute('aria-invalid'),
        ariaErrormessage: el.getAttribute('aria-errormessage'),
        title: el.getAttribute('title'),
        placeholder: el.getAttribute('placeholder'),
        autocomplete: el.getAttribute('autocomplete'),
        hasAssociatedLabel: !!associatedLabel,
        labelText: associatedLabel?.textContent.trim().substring(0, 60) || parentLabel?.textContent.trim().substring(0, 60),
        isInFieldset: !!el.closest('fieldset'),
        fieldsetLegend: el.closest('fieldset')?.querySelector('legend')?.textContent.trim().substring(0, 60),
        isHidden: el.type === 'hidden'
      });
    });

    // Fieldsets
    const fieldsets = [];
    form.querySelectorAll('fieldset, [role="group"], [role="radiogroup"]').forEach(fs => {
      fieldsets.push({
        tag: fs.tagName.toLowerCase(),
        role: fs.getAttribute('role'),
        legendText: fs.querySelector('legend')?.textContent.trim().substring(0, 60),
        ariaLabel: fs.getAttribute('aria-label'),
        ariaLabelledby: fs.getAttribute('aria-labelledby'),
        fieldCount: fs.querySelectorAll('input, select, textarea').length
      });
    });

    // Buttons
    const buttons = [];
    form.querySelectorAll('button, input[type="submit"], input[type="reset"], input[type="button"], input[type="image"], [role="button"]').forEach(btn => {
      buttons.push({
        tag: btn.tagName.toLowerCase(),
        type: btn.type,
        text: btn.textContent.trim().substring(0, 60) || btn.value || btn.getAttribute('aria-label'),
        ariaLabel: btn.getAttribute('aria-label'),
        title: btn.getAttribute('title')
      });
    });

    // Select groups
    const selects = [];
    form.querySelectorAll('select').forEach(sel => {
      const optgroups = sel.querySelectorAll('optgroup');
      selects.push({
        name: sel.name,
        hasOptgroups: optgroups.length > 0,
        optgroupLabels: Array.from(optgroups).map(og => og.label),
        optionCount: sel.options.length
      });
    });

    forms.push({
      index: fi,
      action: form.action?.substring(0, 100),
      method: form.method,
      ariaLabel: form.getAttribute('aria-label'),
      fields: fields.slice(0, 30),
      fieldsets: fieldsets,
      buttons: buttons,
      selects: selects
    });
  });

  // Also check for isolated form fields not inside <form>
  const isolatedFields = document.querySelectorAll('input:not(form input), select:not(form select), textarea:not(form textarea)');

  return JSON.stringify({ forms, isolatedFieldCount: isolatedFields.length }, null, 2);
})()
```

### Step 2: Evaluate criteria

**Criterion 11.1** – Every form field has a label.
Each field must have a label via one of: `aria-labelledby`, `aria-label`, `<label for="…">`, or `title`. A placeholder alone is NOT a valid label.

**Criterion 11.2** – Labels are relevant.
The label text must clearly describe what input is expected.

**Criterion 11.3** – Labels are coherent.
The accessible name (computed from aria-label, aria-labelledby, label, title) must be consistent with any visible label.

**Criterion 11.4** – Labels are visually close to their fields.
Labels should be adjacent to their fields:
- Above or to the left for text inputs
- Above or to the left for select/textarea
- To the right or below for checkboxes and radios

**Criterion 11.5** – Related fields are grouped.
Fields of the same nature (e.g., address parts, date components, radio choices) must be grouped with `<fieldset>` + `<legend>`, or `[role="group"]`/`[role="radiogroup"]` + `aria-label`/`aria-labelledby`.

**Criterion 11.6** – Field groupings have a legend.
Each `<fieldset>` must have a non-empty `<legend>`. Each `[role="group"]` or `[role="radiogroup"]` must have `aria-label` or `aria-labelledby`.

**Criterion 11.7** – Grouping legends are relevant.
The legend must describe the purpose of the group.

**Criterion 11.8** – Select options of the same nature are grouped.
Related options in `<select>` should use `<optgroup label="…">`.

**Criterion 11.9** – Button labels are relevant.
Submit, reset, and other buttons must have descriptive accessible names, not just "Submit" on a multi-form page.

**Criterion 11.10** – Input validation is accessible.
- Required fields are indicated with `required` or `aria-required="true"` and a visible indicator
- Field type/format is communicated (e.g., "Date: DD/MM/YYYY")
- Errors are communicated: `aria-invalid="true"` on the field, error message linked via `aria-describedby` or `aria-errormessage`

**Criterion 11.11** – Error messages suggest corrections.
When a field value is rejected, the error message must explain what is expected (format, allowed values, examples). Not just "Invalid input".

**Criterion 11.12** – Data modification/deletion is confirmable.
Forms that modify or delete data, or submit financial/legal transactions, must provide one of: undo mechanism, confirmation step before submission, or ability to review and correct before final submission.

**Criterion 11.13** – Field purpose is programmatically determinable (autocomplete).
Fields for personal data (name, email, phone, address, etc.) should use the appropriate `autocomplete` attribute value to help browsers and assistive technologies.

### Step 3: Generate report

For each form, list all fields with their label status, grouping, validation attributes, and any issues found.

WCAG references: 9.1.3.1 (A), 9.1.3.5 (AA), 9.2.4.6 (AA), 9.3.3.1 (A), 9.3.3.2 (A), 9.3.3.3 (AA), 9.3.3.4 (AA), 9.4.1.2 (A)
