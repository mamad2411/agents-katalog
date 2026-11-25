---
name: greenhouse-job-application
description: Automate filling job applications on Greenhouse.io and similar React-based ATS platforms via browser automation. Covers React input handling, reCAPTCHA detection, resume upload limitations, and single-expression multi-field filling.
---

# Greenhouse.io Job Application Automation

Automate filling job applications on Greenhouse.io (and similar React-based ATS platforms) via browser automation.

## When to Use
- User asks to apply to a job on Greenhouse.io
- Filling out web forms with profile data
- Uploading resumes to job application systems

## Configuration

Reads PII and the resume path from `profile.yaml` at the repo root (copy from `profile.yaml.example` on first run). Relevant keys:

- `identity.first_name`, `last_name`, `email`, `phone`, `country`
- `resume.path`
- `work_authorization.us_authorized`, `work_authorization.needs_visa_sponsorship`
- `careers_emails` — fallback for when React dropdowns block submission
- `paths.applier_log`

## Form Filling (Single JavaScript Expression)

React-controlled inputs ignore `element.value = x`. Use the native setter. Load values from `profile.yaml` and inject them into one `browser_console` call:

```python
import yaml
from pathlib import Path

cfg = yaml.safe_load(Path("profile.yaml").read_text())
fields = {
    "first_name": cfg["identity"]["first_name"],
    "last_name":  cfg["identity"]["last_name"],
    "email":      cfg["identity"]["email"],
    "phone":      cfg["identity"]["phone"],
    "country":    cfg["identity"]["country"],
}
```

Then execute the snippet below, injecting `fields` as `fieldMap`:

```javascript
(function() {
  function setReactValue(element, value) {
    var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
      window.HTMLInputElement.prototype, 'value'
    ).set;
    nativeInputValueSetter.call(element, value);
    var event = new Event('input', { bubbles: true });
    element.dispatchEvent(event);
  }

  var fieldMap = /* INJECT fields FROM profile.yaml */;

  for (var id in fieldMap) {
    var el = document.getElementById(id);
    if (el) setReactValue(el, fieldMap[id]);
  }

  return { status: 'completed', fields: Object.keys(fieldMap) };
})()
```

**Important**: fill ALL fields in ONE `browser_console` call. Do NOT use individual `browser_type` calls — per-turn iteration limits will be hit.

## Verify Fields After Filling

React may reset values. Always verify in a second call:

```javascript
(function() {
  var checks = ['first_name', 'last_name', 'email', 'phone', 'country'];
  var result = {};
  for (var i = 0; i < checks.length; i++) {
    var el = document.getElementById(checks[i]);
    result[checks[i]] = el ? el.value : 'NOT FOUND';
  }
  return result;
})()
```

## Resume Upload

**Limitation**: you cannot read local files from browser context. The `DataTransfer` API creates an empty `File` — upload will fail server-side validation.

An approach that documents the attempt:

```javascript
(function() {
  var file = new File([new ArrayBuffer(0)], 'resume.pdf', {type: 'application/pdf'});
  var dt = new DataTransfer();
  dt.items.add(file);
  var resumeInput = document.getElementById('resume');
  if (resumeInput) {
    resumeInput.files = dt.files;
    return { resumeUpload: 'attempted', filesCount: resumeInput.files.length };
  }
  return { resumeUpload: 'no_resume_field' };
})()
```

For real resume uploads, switch to CDP and use `DOM.setFileInputFiles` with the resume path from `cfg["resume"]["path"]` — see [`../browser-harness-ats-automation/SKILL.md`](../browser-harness-ats-automation/SKILL.md).

## reCAPTCHA Detection

Check before attempting submit:

```javascript
(function() {
  var recaptcha = document.querySelector('.g-recaptcha, [data-recaptcha], iframe[src*="recaptcha"]');
  return { hasRecaptcha: !!recaptcha };
})()
```

## Submission

If reCAPTCHA is present:
1. Click submit via `browser_click`.
2. Expect validation errors — this is normal.
3. Log partial success and note that manual completion is needed.

## Logging

Append to `paths.applier_log` from `profile.yaml`. Include:

- Timestamp, job title, company, URL
- Fields filled (`✓`/`✗`)
- Resume upload result
- Submission result (success / partial / blocked)
- Next steps for manual completion

## React Select / Dropdown Components (critical — these cannot be automated)

Greenhouse uses custom React dropdowns (`class="select__input"`, `role="combobox"`, `aria-expanded`, `role="listbox"` with `role="option"` children). These are **NOT** standard `<select>` elements — they are `div`/`input` hybrids that ignore:

- Standard `click()` on the input field
- `type_text()` into the input
- The React-value-setter technique used for text fields
- Clicking `[role="option"]` elements directly (click registers but React state doesn't update)

**Symptoms**: `element.value` stays `''`, `aria-expanded` may toggle but options don't filter, and submission fails validation.

**Affected fields typically include**:
- `question_XXXXX` (work authorization: "Yes, I am currently legally authorized..." / "No, I am not...")
- `question_XXXXX` (visa sponsorship: "Yes, I will need..." / "No, I do not need...")
- `question_XXXXX` (country selector — sometimes a React select)

**Workaround**: when a Greenhouse React dropdown can't be filled, **fall back to email application** using `careers_emails[company]` from `profile.yaml`. Don't spend multiple iterations trying to click/type into React selects — email is the only reliable path.

For users whose `work_authorization.us_authorized` is `false`:
- work_auth answer = "No, I am not currently legally authorized to work in the United States" (or similar "No" option)
- visa_sponsorship answer = "Yes, I will need the company to provide sponsorship for a work visa"

## Pitfalls

1. **React state reset**: `.value = x` won't work on React-controlled inputs — use `nativeInputValueSetter`.
2. **React dropdowns unfillable**: `select__input` + `role="listbox"` components cannot be set via CDP — use email fallback.
3. **reCAPTCHA**: Greenhouse runs reCAPTCHA — blocks automated submission on some forms (see the sister `browser-harness-ats-automation` skill for the checkbox-variant bypass).
4. **File upload**: browser security prevents reading local files — resume must be uploaded via CDP `DOM.setFileInputFiles` or manually.
5. **Iteration limits**: fill all fields in ONE `browser_console` call, not multiple `browser_type` calls.
