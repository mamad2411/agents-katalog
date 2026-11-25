---
name: form-validation-educacross
description: Implement form validation with VeeValidate 3 and i18n integration in Educacross Front Office. Use when user says "validação", "form validation", "VeeValidate", "validate form", "formulário", or needs to validate user input.
---

# Form Validation - Educacross Front Office

Implement production-ready form validation using VeeValidate 3 with i18n integration and Bootstrap Vue styling.

## Setup

**Dependencies (already installed):**
- VeeValidate 3.x
- Vue I18n
- Bootstrap Vue

**Auto-imported:**
- `ValidationProvider` — Wraps individual form fields
- `ValidationObserver` — Wraps entire forms for submit handling

---

## Quick Start

### Basic Validated Input

```vue
<template>
  <ValidationProvider
    v-slot="{ errors }"
    rules="required"
    name="Nome"
  >
    <b-form-group label="Nome" label-for="name">
      <b-form-input
        id="name"
        v-model="form.name"
        :state="errors.length > 0 ? false : null"
      />
      <b-form-invalid-feedback :state="errors.length === 0">
        {{ errors[0] }}
      </b-form-invalid-feedback>
    </b-form-group>
  </ValidationProvider>
</template>

<script>
import { ValidationProvider } from 'vee-validate'

export default {
  components: { ValidationProvider },
  
  data() {
    return {
      form: {
        name: '',
      },
    }
  },
}
</script>
```

---

## Complete Form Example

```vue
<template>
  <ValidationObserver ref="formValidator" v-slot="{ handleSubmit, invalid }">
    <b-form @submit.prevent="handleSubmit(onSubmit)">
      <b-row>
        <!-- Name field -->
        <b-col cols="12">
          <ValidationProvider
            v-slot="{ errors }"
            rules="required"
            name="Nome"
          >
            <b-form-group label="Nome *" label-for="name">
              <b-form-input
                id="name"
                v-model="form.name"
                :state="errors.length > 0 ? false : null"
              />
              <b-form-invalid-feedback :state="errors.length === 0">
                {{ errors[0] }}
              </b-form-invalid-feedback>
            </b-form-group>
          </ValidationProvider>
        </b-col>
        
        <!-- Email field -->
        <b-col cols="12" md="6">
          <ValidationProvider
            v-slot="{ errors }"
            rules="required|email"
            name="Email"
          >
            <b-form-group label="Email *" label-for="email">
              <b-form-input
                id="email"
                v-model="form.email"
                type="email"
                :state="errors.length > 0 ? false : null"
              />
              <b-form-invalid-feedback :state="errors.length === 0">
                {{ errors[0] }}
              </b-form-invalid-feedback>
            </b-form-group>
          </ValidationProvider>
        </b-col>
        
        <!-- Age field -->
        <b-col cols="12" md="6">
          <ValidationProvider
            v-slot="{ errors }"
            rules="required|numeric|min_value:1|max_value:120"
            name="Idade"
          >
            <b-form-group label="Idade *" label-for="age">
              <b-form-input
                id="age"
                v-model="form.age"
                type="number"
                :state="errors.length > 0 ? false : null"
              />
              <b-form-invalid-feedback :state="errors.length === 0">
                {{ errors[0] }}
              </b-form-invalid-feedback>
            </b-form-group>
          </ValidationProvider>
        </b-col>
        
        <!-- Password field -->
        <b-col cols="12">
          <ValidationProvider
            v-slot="{ errors }"
            rules="required|password"
            name="Senha"
            vid="password"
          >
            <b-form-group label="Senha *" label-for="password">
              <b-form-input
                id="password"
                v-model="form.password"
                type="password"
                :state="errors.length > 0 ? false : null"
              />
              <b-form-invalid-feedback :state="errors.length === 0">
                {{ errors[0] }}
              </b-form-invalid-feedback>
            </b-form-group>
          </ValidationProvider>
        </b-col>
        
        <!-- Password confirmation -->
        <b-col cols="12">
          <ValidationProvider
            v-slot="{ errors }"
            rules="required|confirmed:password"
            name="Confirmação de Senha"
          >
            <b-form-group label="Confirmar Senha *" label-for="password-confirm">
              <b-form-input
                id="password-confirm"
                v-model="form.passwordConfirm"
                type="password"
                :state="errors.length > 0 ? false : null"
              />
              <b-form-invalid-feedback :state="errors.length === 0">
                {{ errors[0] }}
              </b-form-invalid-feedback>
            </b-form-group>
          </ValidationProvider>
        </b-col>
        
        <!-- Submit button -->
        <b-col cols="12">
          <b-button
            type="submit"
            variant="primary"
            :disabled="invalid || submitting"
          >
            <b-spinner v-if="submitting" small class="mr-50" />
            {{ submitting ? 'Salvando...' : 'Salvar' }}
          </b-button>
        </b-col>
      </b-row>
    </b-form>
  </ValidationObserver>
</template>

<script>
import { ValidationProvider, ValidationObserver } from 'vee-validate'

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  
  data() {
    return {
      form: {
        name: '',
        email: '',
        age: null,
        password: '',
        passwordConfirm: '',
      },
      submitting: false,
    }
  },
  
  methods: {
    async onSubmit() {
      this.submitting = true
      try {
        // API call
        await this.saveData()
        
        this.$toast({
          component: ToastificationContent,
          props: {
            title: 'Sucesso!',
            icon: 'CheckIcon',
            variant: 'success',
          },
        })
      } catch (error) {
        console.error('Error submitting form:', error)
      } finally {
        this.submitting = false
      }
    },
  },
}
</script>
```

---

## ValidationProvider

Wraps individual form fields.

### Props

```javascript
{
  rules: 'required|email',     // Validation rules (string or object)
  name: 'Email',                // Field name (displayed in errors)
  vid: 'email',                 // Unique ID for cross-field validation
  mode: 'aggressive',           // Validation mode (lazy, aggressive, passive)
  immediate: false,             // Validate immediately on mount
  bails: true,                  // Stop after first error
}
```

### Slot Props

```javascript
{
  errors: [],                   // Array of error messages
  valid: false,                 // Is field valid?
  invalid: false,               // Is field invalid?
  validated: false,             // Has field been validated?
  pending: false,               // Is validation pending?
  touched: false,               // Has field been touched?
  dirty: false,                 // Has value changed?
  pristine: false,              // Is value unchanged?
  reset: Function,              // Reset validation state
  validate: Function,           // Manually trigger validation
}
```

### Usage Pattern

```vue
<ValidationProvider
  v-slot="{ errors, valid, invalid }"
  rules="required|email"
  name="Email"
>
  <b-form-input
    v-model="email"
    :state="errors.length > 0 ? false : null"
  />
  <b-form-invalid-feedback :state="errors.length === 0">
    {{ errors[0] }}
  </b-form-invalid-feedback>
</ValidationProvider>
```

**Key Points:**
- `:state` on input: `false` shows red border, `null` = no styling
- Show first error only: `errors[0]`
- `name` prop appears in error messages

---

## ValidationObserver

Wraps entire forms.

### Props

```javascript
{
  tag: 'form',                  // HTML tag to render
  slim: false,                  // Render without wrapper element
}
```

### Slot Props

```javascript
{
  errors: {},                   // Object with field errors
  validate: Function,           // Validate all fields
  reset: Function,              // Reset all fields
  handleSubmit: Function,       // Submit handler with validation
  invalid: false,               // Is form invalid?
  valid: false,                 // Is form valid?
  pending: false,               // Is validation pending?
  validated: false,             // Has form been validated?
}
```

### Usage

```vue
<ValidationObserver ref="formValidator" v-slot="{ handleSubmit, invalid }">
  <b-form @submit.prevent="handleSubmit(onSubmit)">
    <!-- Fields here -->
    
    <b-button
      type="submit"
      :disabled="invalid"
    >
      Submit
    </b-button>
  </b-form>
</ValidationObserver>
```

### Manual Validation

```javascript
methods: {
  async validateForm() {
    const isValid = await this.$refs.formValidator.validate()
    if (isValid) {
      // Proceed
    } else {
      // Show errors
    }
  },
  
  resetForm() {
    this.$refs.formValidator.reset()
    this.form = { ... }  // Reset form data
  },
}
```

---

## Available Validation Rules

Rules are imported from `@validations` (configured globally).

### Common Rules

| Rule | Description | Example |
|------|-------------|---------|
| `required` | Field is required | `rules="required"` |
| `email` | Valid email address | `rules="required\|email"` |
| `min` | Minimum length | `rules="min:3"` |
| `max` | Maximum length | `rules="max:50"` |
| `min_value` | Minimum number | `rules="min_value:1"` |
| `max_value` | Maximum number | `rules="max_value:100"` |
| `numeric` | Numbers only | `rules="numeric"` |
| `alpha` | Letters only | `rules="alpha"` |
| `alpha_num` | Letters and numbers | `rules="alpha_num"` |
| `alpha_dash` | Letters, numbers, dashes | `rules="alpha_dash"` |
| `alpha_spaces` | Letters and spaces | `rules="alpha_spaces"` |
| `integer` | Integer numbers | `rules="integer"` |
| `digits` | Exact number of digits | `rules="digits:4"` |
| `between` | Value between range | `rules="between:1,100"` |
| `confirmed` | Must match another field | `rules="confirmed:password"` |
| `password` | Strong password | `rules="password"` |
| `url` | Valid URL | `rules="url"` |
| `regex` | Custom regex | `rules="regex:^[A-Z]"` |

### Multiple Rules

```vue
<!-- Pipe-separated -->
<ValidationProvider
  rules="required|email|min:5"
  name="Email"
>

<!-- Object format -->
<ValidationProvider
  :rules="{
    required: true,
    email: true,
    min: { length: 5 }
  }"
  name="Email"
>
```

---

## Cross-Field Validation

### Confirmed (Password Match)

```vue
<!-- Password field -->
<ValidationProvider
  rules="required|password"
  name="Senha"
  vid="password"
>
  <b-form-input
    v-model="form.password"
    type="password"
  />
</ValidationProvider>

<!-- Confirmation field -->
<ValidationProvider
  rules="required|confirmed:password"
  name="Confirmação"
>
  <b-form-input
    v-model="form.passwordConfirm"
    type="password"
  />
</ValidationProvider>
```

**Key:** `vid="password"` on first field, `confirmed:password` on second.

---

## Custom Validators

### In Component

```vue
<ValidationProvider
  :rules="customRule"
  name="Campo"
>
  <b-form-input v-model="value" />
</ValidationProvider>

<script>
export default {
  computed: {
    customRule() {
      return {
        required: true,
        custom: value => {
          if (value && value.length > 10) {
            return true
          }
          return 'O campo deve ter mais de 10 caracteres'
        },
      }
    },
  },
}
</script>
```

### Global Custom Rule

```javascript
// src/@core/utils/validations/validations.js
import { extend } from 'vee-validate'

extend('cpf', {
  validate: value => {
    // CPF validation logic
    return validateCPF(value)
  },
  message: 'CPF inválido',
})

// Usage
<ValidationProvider rules="required|cpf" name="CPF">
```

---

## i18n Integration

Validation messages are automatically translated using i18n.

### Message Files

**Location:** `src/locales/{lang}.json`

```json
{
  "validations": {
    "required": "O campo {_field_} é obrigatório",
    "email": "O campo {_field_} deve ser um email válido",
    "min": "O campo {_field_} deve ter no mínimo {length} caracteres",
    "max": "O campo {_field_} deve ter no máximo {length} caracteres",
    "min_value": "O campo {_field_} deve ser no mínimo {min}",
    "max_value": "O campo {_field_} deve ser no máximo {max}",
    "numeric": "O campo {_field_} deve conter apenas números",
    "alpha": "O campo {_field_} deve conter apenas letras",
    "alpha_num": "O campo {_field_} deve conter apenas letras e números",
    "alpha_spaces": "O campo {_field_} deve conter apenas letras e espaços",
    "confirmed": "O campo {_field_} não confere",
    "password": "A senha deve conter pelo menos 8 caracteres, uma letra maiúscula, uma minúscula e um número",
    "url": "O campo {_field_} deve ser uma URL válida"
  }
}
```

**Placeholders:**
- `{_field_}` — Field name from `name` prop
- `{length}`, `{min}`, `{max}` — Rule parameters

---

## Bootstrap State Integration

### State Pattern

```vue
<b-form-input
  v-model="value"
  :state="errors.length > 0 ? false : null"
/>
```

**States:**
- `false` — Invalid (red border + icon)
- `true` — Valid (green border + icon)
- `null` — No styling (default)

**Best Practice:** Use `false` for errors, `null` for no validation (never hardcode `true`).

### Invalid Feedback

```vue
<b-form-invalid-feedback :state="errors.length === 0">
  {{ errors[0] }}
</b-form-invalid-feedback>
```

Or with custom message:

```vue
<b-form-invalid-feedback>
  <span v-if="errors.length > 0">
    {{ errors[0] }}
  </span>
</b-form-invalid-feedback>
```

---

## Validation Modes

Control when validation runs:

```vue
<ValidationProvider
  rules="required|email"
  name="Email"
  mode="aggressive"
>
```

| Mode | Behavior |
|------|----------|
| `aggressive` | Validates on input (real-time) |
| `lazy` | Validates on submit only |
| `passive` | Never validates automatically |
| `eager` | After first validation, validates on input |

**Default:** `eager` (good balance)

---

## Common Patterns

### Required Field with Min Length

```vue
<ValidationProvider
  v-slot="{ errors }"
  rules="required|min:3"
  name="Nome"
>
  <b-form-group label="Nome *" label-for="name">
    <b-form-input
      id="name"
      v-model="form.name"
      :state="errors.length > 0 ? false : null"
    />
    <b-form-invalid-feedback :state="errors.length === 0">
      {{ errors[0] }}
    </b-form-invalid-feedback>
  </b-form-group>
</ValidationProvider>
```

---

### Optional Field with Validation

```vue
<ValidationProvider
  v-slot="{ errors }"
  rules="email"
  name="Email Alternativo"
>
  <b-form-group label="Email Alternativo" label-for="alt-email">
    <b-form-input
      id="alt-email"
      v-model="form.altEmail"
      :state="errors.length > 0 ? false : null"
    />
    <b-form-invalid-feedback :state="errors.length === 0">
      {{ errors[0] }}
    </b-form-invalid-feedback>
  </b-form-group>
</ValidationProvider>
```

**Key:** No `required` rule means field is optional but validated when filled.

---

### Select Validation

```vue
<ValidationProvider
  v-slot="{ errors }"
  rules="required"
  name="Turma"
>
  <b-form-group label="Turma *" label-for="class">
    <ESelect
      id="class"
      v-model="form.classId"
      :options="classes"
      label="name"
      :state="errors.length > 0 ? false : null"
    />
    <b-form-invalid-feedback :state="errors.length === 0">
      {{ errors[0] }}
    </b-form-invalid-feedback>
  </b-form-group>
</ValidationProvider>
```

---

### Checkbox Validation

```vue
<ValidationProvider
  v-slot="{ errors }"
  :rules="{ required: { allowFalse: false } }"
  name="Termos"
>
  <b-form-group>
    <b-form-checkbox
      v-model="form.acceptTerms"
      :state="errors.length > 0 ? false : null"
    >
      Aceito os termos *
    </b-form-checkbox>
    <b-form-invalid-feedback :state="errors.length === 0">
      {{ errors[0] }}
    </b-form-invalid-feedback>
  </b-form-group>
</ValidationProvider>
```

---

### Date Validation

```vue
<ValidationProvider
  v-slot="{ errors }"
  rules="required"
  name="Data de Nascimento"
>
  <b-form-group label="Data de Nascimento *" label-for="birth-date">
    <b-form-datepicker
      id="birth-date"
      v-model="form.birthDate"
      :state="errors.length > 0 ? false : null"
    />
    <b-form-invalid-feedback :state="errors.length === 0">
      {{ errors[0] }}
    </b-form-invalid-feedback>
  </b-form-group>
</ValidationProvider>
```

---

## Composition API Pattern

```vue
<script>
import { ref } from 'vue'
import { useForm } from '@/composables/useForm'

export default {
  setup() {
    const formValidator = ref(null)
    
    const form = ref({
      name: '',
      email: '',
    })
    
    const { submitting, handleSubmit } = useForm(formValidator)
    
    const onSubmit = async () => {
      try {
        await api.saveData(form.value)
        // Success
      } catch (error) {
        console.error(error)
      }
    }
    
    return {
      formValidator,
      form,
      submitting,
      onSubmit: handleSubmit(onSubmit),
    }
  },
}
</script>
```

---

## Checklist

Before submitting a form:

- [ ] All required fields wrapped in `ValidationProvider`
- [ ] Form wrapped in `ValidationObserver`
- [ ] Each `ValidationProvider` has `name` prop
- [ ] `:state` prop bound to validation errors
- [ ] `b-form-invalid-feedback` shows first error
- [ ] Submit button uses `handleSubmit` from observer
- [ ] Submit button disabled when `invalid` is true
- [ ] Validation messages exist in i18n locale files
- [ ] Cross-field validation uses `vid` prop

---

## Common Mistakes

❌ **DON'T:**
```vue
<!-- Missing state binding -->
<b-form-input v-model="value" />

<!-- Hardcoded error messages -->
<b-form-invalid-feedback>
  Campo obrigatório
</b-form-invalid-feedback>

<!-- Not using handleSubmit -->
<b-form @submit.prevent="onSubmit">
```

✅ **DO:**
```vue
<!-- Proper state binding -->
<b-form-input
  v-model="value"
  :state="errors.length > 0 ? false : null"
/>

<!-- Dynamic error messages -->
<b-form-invalid-feedback :state="errors.length === 0">
  {{ errors[0] }}
</b-form-invalid-feedback>

<!-- Use handleSubmit -->
<ValidationObserver v-slot="{ handleSubmit }">
  <b-form @submit.prevent="handleSubmit(onSubmit)">
</ValidationObserver>
```

---

## References

- **VeeValidate 3 Docs:** https://vee-validate.logaretm.com/v3/
- **Component Usage:** See `component-usage-educacross` skill for form components
- **Feature Creator:** See `feature-creator-educacross` skill for complete form examples
