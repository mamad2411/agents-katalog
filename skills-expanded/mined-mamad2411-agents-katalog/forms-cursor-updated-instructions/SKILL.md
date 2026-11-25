# Form Functionality Library — Instructions

## Project Goals

Build a **modular, flexible form functionality library** to add advanced functionality to **Webflow forms**, supporting:
- ✅ Single-step forms
- ✅ Multi-step forms
- ✅ Multi-step forms with logic branching

This must be reusable across multiple projects. The system is driven exclusively by **data-attributes** — no binding to classes or IDs.  

All modules must be clean, well-typed TypeScript, with verbose `console.log` output for testing, and state managed **in memory** for speed and simplicity.

## Deployment

- When prompted, please commit, and push changes to Github. 
- Once commit has occured, please generrate a JSDelivr URL with the current commit hash. For example https://cdn.jsdelivr.net/gh/CorporateDirect/Form@[Commit Hash]/dist/
- ALWAYS use index.browser.min.js as the entry to the app to comply with CORS.

---

## Project Structure

```
/forms-lib
├── /modules
│   ├── branching.ts
│   ├── multiStep.ts
│   ├── validation.ts
│   ├── events.ts
│   ├── errors.ts
│   ├── summary.ts
│   └── utils.ts
├── index.ts
├── config.ts
├── tsconfig.json
├── console-logs.txt
├── index.html (provided by user)
├── README.md
└── updated-instructions.md
```

---1

## Acceptance Criteria (Modules)

### `/modules/branching.ts`
- Handles all **branching logic** and path evaluation.
- Watches user selections on `[data-go-to]` and `[data-answer]`.
- Supports **nested conditions** and step skipping.
- **Exports**: `initBranching()`, `getNextStep()`, `resetBranching()`.

### `/modules/multiStep.ts`
- Manages **step visibility**, **progression**, **backward navigation**, and **skipping**.
- Syncs with branching for dynamic paths.
- **Exports**: `initMultiStep()`, `goToStep()`, `showStep()`, `hideStep()`.

### `/modules/validation.ts`
- Handles **field validation** with awareness of active/inactive branches.
- Enables/disables validation dynamically based on visibility.
- **Exports**: `initValidation()`, `validateStep()`, `validateField()`.

### `/modules/errors.ts`
- Provides **custom field error messaging**.
- Highlights invalid fields and injects user-friendly error text.
- **Exports**: `showError()`, `clearError()`, `initErrors()`.

### `/modules/summary.ts`
- Listens for inputs with `[data-step-field-name]`.
- Stores field values in memory.
- Populates `[data-summary-field]` with proper formatting using `[data-join]`.
- Supports type/subtype/number segments for complex summaries.
- **Exports**: `initSummary()`, `updateSummary()`, `clearSummary()`.

### `/modules/utils.ts`
- Shared helpers: logging, query selectors, event binding.
- Example: `queryAllByAttr()`, `logVerbose()`.

### `/config.ts`
Must include:
- ✅ All **data-attribute keys** as constants.
- ✅ Default behaviors (e.g., initial step index, log levels).
- ✅ Feature toggles (e.g., debug mode).

**Example:**

```ts
export const DATA_ATTRS = {
  MULTISTEP: 'data-form="multistep"',
  LOGIC: 'data-logic',
  STEP: 'data-form="step"',
  NEXT_BTN: 'data-form="next-btn"',
  // ...and so on
};

export const DEFAULTS = {
  START_STEP: 1,
  DEBUG: true
};
```

## init() Best Practices

- Every module must expose an `init()` method.
- `init()` accepts a DOM root (or `document` by default).
- Bind listeners only to elements with the expected `data-*` attributes.
- Cleanly unbind or rebind if the DOM changes (or use passive listeners).
- Use **delegated event listeners** if dynamic elements are expected.

## State Spec
	- Use a singleton FormState JS object in memory.
	- Required methods:
	- setField(name, value)
	- getField(name)
	- getAll()
	- clear()
	- The summary module must pull values from FormState for output.
	- Branch changes must clear irrelevant values automatically.

## Common Edge Cases

- **Changing answers upstream:** Going backward and changing a previous answer resets dependent steps and clears those values in `FormState`.
- **Inactive paths:** Validation ignores fields/steps hidden due to branching.
- **Converging paths:** Validate only the active path leading to submit.
- **Partial submission:** Block submit if any visible required fields are incomplete.
- **Skip actions:** `[data-skip]` must properly skip steps and update state.

## Coding Standards

- Use **strict TypeScript** — no `any` types.
- Use ESM modules.
- Format with **Prettier**.
- Include **JSDoc** for all exported functions.
- Write meaningful `console.log` statements for:
  - State updates
  - Branch evaluations
  - Step transitions
  - Validation checks
- Remove any temporary test/debug code once validated.
- Keep logic modular and reusable.

## Data attributes and examples

### Form Block

```html
<form data-form="multistep" data-logic="true">
  <!-- Multi-step form with branching -->
</form>
```

### Step Wrapper

```html
<div data-form="step" data-answer="step-2">
  <!-- Step content here -->
</div>
```

### Navigation Buttons

```html
<button data-form="next-btn">Next</button>
<button data-form="back-btn">Back</button>
<button data-form="submit">Submit</button>
```

### Skip Example

```html
<button data-skip="step-7">Skip to Step 7</button>
```

### Step Categorization

```html
<div data-form="step"
     data-step-type="manager"
     data-step-subtype="assistant"
     data-step-number="1">
  <!-- Inputs for manager/assistant -->
</div>
```

### Branch Logic

```html
<input type="radio" name="role" data-go-to="manager-step" value="Manager">
<div data-answer="manager-step" data-form="step">
  <!-- Manager step content -->
</div>
```

### Summary Fields

```html
<input type="text" data-step-field-name="firstName">
<input type="text" data-step-field-name="lastName">

<div data-summary-field="firstName|lastName" data-join="space"></div>

<div data-summary-type="manager"
     data-summary-subtype="assistant"
     data-summary-number="1">
  <!-- Output for this segment -->
</div>
```

## Testing and Debugging

- Load the built JS library via jsDelivr in Webflow.
- Use `index.html` for the current form structure.
- Run tests, then paste the full browser console output in `console-logs.txt`.
- Each module must log:
  - State updates
  - Branch decisions
  - Step transitions
  - Validation results

## Working Process

- Build each module step-by-step.
- Test on the actual Webflow form.
- Review `console-logs.txt`.
- Adjust, refine, and verify.
- Only then move to the next module.

## Reference

- [tryformly.com](https://tryformly.com)


