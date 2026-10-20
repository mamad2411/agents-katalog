---
name: "Form Pattern Engine"
version: "1.0.0"
description: "Implements robust form patterns with validation, conditional fields, multi-step wizards, and auto-save."
author: "workspace"
activated: false
---

# Form Pattern Engine

Implements robust form patterns with validation, conditional fields, multi-step wizards, and auto-save.

## Decision Framework

### When to Apply
Use when: Complex forms, multi-step wizards, conditional fields, real-time validation, auto-save needed

### When NOT to Apply
Don't use when: Simple single-field inputs, search boxes

## Anti-Patterns

### 1. No Validation Feedback
```javascript
// BAD: Silent validation
if (!email.includes('@')) return;

// GOOD: Clear error message
if (!email.includes('@')) {
  setErrors({ email: 'Please enter a valid email address' });
  return;
}
```

### 2. Unclear Required Fields
Always mark required fields visually and in ARIA attributes.


## Trigger Phrases

- "Build form"
- "Form validation"
- "Multi-step wizard"
- "Form state"
- "Conditional fields"
- "Auto-save form"

## Patterns

### Form State Manager
```javascript
function useForm(initialValues, validationSchema) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  const validate = useCallback(() => {
    const result = validationSchema.safeParse(values);
    if (!result.success) {
      const fieldErrors = {};
      result.error.errors.forEach(e => {
        fieldErrors[e.path.join('.')] = e.message;
      });
      setErrors(fieldErrors);
      return false;
    }
    setErrors({});
    return true;
  }, [values, validationSchema]);

  const getFieldProps = (name) => ({
    name, value: values[name] || '',
    onChange: (e) => setValues(v => ({ ...v, [name]: e.target.value })),
    onBlur: () => setTouched(t => ({ ...t, [name]: true })),
    'aria-invalid': touched[name] && !!errors[name],
    'aria-describedby': errors[name] ? `${name}-error` : undefined,
  });

  return { values, errors, touched, validate, getFieldProps, setValues };
}
```

### Multi-Step Wizard
```javascript
const FormWizard = ({ steps, onComplete }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [data, setData] = useState({});

  const step = steps[currentStep];
  const isFirst = currentStep === 0;
  const isLast = currentStep === steps.length - 1;

  return (
    <form aria-label={`Step ${currentStep + 1} of ${steps.length}: ${step.title}`}>
      <h2>{step.title}</h2>
      <step.component data={data} onChange={setData} />
      <div>
        {!isFirst && <button type="button" onClick={() => setCurrentStep(s => s - 1)}>Back</button>}
        <button type="button" onClick={() => isLast ? onComplete(data) : setCurrentStep(s => s + 1)}>
          {isLast ? 'Submit' : 'Next'}
        </button>
      </div>
    </form>
  );
};
```

## Integration
- Works with: accessibility-pattern-library, error-message-optimizer, validation-engine

