---
name: android-text-input-forms
description: |
  Text input and form patterns for Android/Compose - TextField vs OutlinedTextField, typed form state models, submit-time and change-time validation, KeyboardOptions and KeyboardActions, FocusRequester for focus traversal, password field toggles, multi-field scrollable forms, and mapping server-side validation errors through UiText. Use this skill whenever building login, registration, settings, or any multi-field input screen. Trigger on phrases like "form", "TextField", "input validation", "keyboard", "imeAction", "focus", "password field", "form state", "validation error", "OutlinedTextField", "KeyboardOptions", "FocusRequester", or "IME action".
---

# Android Text Input & Forms (Compose)

## Overview

Compose form patterns centre on three concerns: state (what the user has typed, what errors exist), keyboard (type, IME actions, navigation), and focus (moving between fields programmatically). Get these three right and every form — login, registration, checkout, settings — follows the same pattern.

---

## TextField vs OutlinedTextField

Both accept the same parameters. Choose based on your design system:

```kotlin
// Filled style — appropriate for forms inside a Surface
TextField(
    value = state.email,
    onValueChange = { onAction(FormAction.EmailChanged(it)) },
    label = { Text("Email") },
    modifier = Modifier.fillMaxWidth()
)

// Outlined style — stands out on a plain background
OutlinedTextField(
    value = state.email,
    onValueChange = { onAction(FormAction.EmailChanged(it)) },
    label = { Text("Email") },
    modifier = Modifier.fillMaxWidth()
)
```

Prefer `OutlinedTextField` in forms — the outline makes the input boundary obvious without requiring a filled background. Use `TextField` only if your design system explicitly uses the filled variant.

---

## Form State Model

Model form state as a single data class in the ViewModel's `UiState`. Each field gets a `value` and an `error`. Errors are typed as `UiText?` (null = no error) so they can be string resources or dynamic strings from the server.

```kotlin
// Presentation model — lives in feature:presentation
data class RegisterFormState(
    val name: String = "",
    val nameError: UiText? = null,
    val email: String = "",
    val emailError: UiText? = null,
    val password: String = "",
    val passwordError: UiText? = null,
    val isPasswordVisible: Boolean = false,
    val isSubmitting: Boolean = false
)
```

Keep form field values as plain `String`. Never store `TextFieldValue` in the ViewModel — it carries cursor and selection state that belongs in the Compose layer.

---

## ViewModel — Handling Actions

```kotlin
@HiltViewModel
class RegisterViewModel @Inject constructor(
    private val authRepository: AuthRepository
) : ViewModel() {

    var state by mutableStateOf(RegisterFormState())
        private set

    fun onAction(action: RegisterAction) {
        when (action) {
            is RegisterAction.NameChanged -> state = state.copy(
                name = action.value,
                nameError = null   // clear error on edit
            )
            is RegisterAction.EmailChanged -> state = state.copy(
                email = action.value,
                emailError = null
            )
            is RegisterAction.PasswordChanged -> state = state.copy(
                password = action.value,
                passwordError = null
            )
            RegisterAction.TogglePasswordVisibility -> state = state.copy(
                isPasswordVisible = !state.isPasswordVisible
            )
            RegisterAction.Submit -> submit()
        }
    }

    private fun submit() {
        // Validate all fields before submitting
        val nameError = validateName(state.name)
        val emailError = validateEmail(state.email)
        val passwordError = validatePassword(state.password)

        if (nameError != null || emailError != null || passwordError != null) {
            state = state.copy(
                nameError = nameError,
                emailError = emailError,
                passwordError = passwordError
            )
            return
        }

        state = state.copy(isSubmitting = true)
        viewModelScope.launch {
            authRepository.register(state.name, state.email, state.password)
                .onSuccess { /* emit navigation event */ }
                .onFailure { error ->
                    // Map server errors back to field errors
                    state = state.copy(
                        isSubmitting = false,
                        emailError = if (error == AuthError.EMAIL_TAKEN)
                            UiText.StringResource(R.string.error_email_taken)
                        else null
                    )
                }
        }
    }
}
```

---

## Validation Strategy

### Validate on Submit (Default)

Validate the full form only when the user taps Submit. Clear each field's error as soon as the user edits it. This reduces noise and is appropriate for most login/register forms.

```kotlin
// Clear error on change (in ViewModel)
is RegisterAction.EmailChanged -> state = state.copy(
    email = action.value,
    emailError = null
)

// Validate on submit (shown above in submit())
```

### Validate on Change (with Debounce)

For fields with expensive validation (e.g., username availability check), validate after the user stops typing:

```kotlin
private var validationJob: Job? = null

is RegisterAction.UsernameChanged -> {
    state = state.copy(username = action.value, usernameError = null)
    validationJob?.cancel()
    validationJob = viewModelScope.launch {
        delay(500)   // 500ms debounce
        val available = authRepository.checkUsernameAvailable(action.value)
        state = state.copy(
            usernameError = if (!available)
                UiText.StringResource(R.string.error_username_taken)
            else null
        )
    }
}
```

### Validation Functions

Keep validation functions pure and in the domain layer (`core:domain` or `feature:domain`):

```kotlin
fun validateEmail(email: String): UiText? {
    if (email.isBlank()) return UiText.StringResource(R.string.error_email_required)
    if (!Patterns.EMAIL_ADDRESS.matcher(email).matches())
        return UiText.StringResource(R.string.error_email_invalid)
    return null
}

fun validatePassword(password: String): UiText? {
    if (password.length < 8) return UiText.StringResource(R.string.error_password_too_short)
    if (!password.any { it.isUpperCase() }) return UiText.StringResource(R.string.error_password_no_uppercase)
    if (!password.any { it.isDigit() }) return UiText.StringResource(R.string.error_password_no_digit)
    return null
}
```

For typed error enums (used with the Result wrapper in android-error-handling), see that skill. For display-only form validation, `UiText?` is simpler.

---

## KeyboardOptions and KeyboardActions

Always set `KeyboardOptions` and `KeyboardActions` so the IME helps users navigate the form without reaching for the next field manually.

```kotlin
OutlinedTextField(
    value = state.email,
    onValueChange = { onAction(FormAction.EmailChanged(it)) },
    label = { Text("Email") },
    keyboardOptions = KeyboardOptions(
        keyboardType = KeyboardType.Email,
        imeAction = ImeAction.Next         // shows "Next" on the IME
    ),
    keyboardActions = KeyboardActions(
        onNext = { focusManager.moveFocus(FocusDirection.Down) }
    ),
    singleLine = true,
    modifier = Modifier.fillMaxWidth()
)
```

### `KeyboardType` Reference

| Field type | `KeyboardType` |
|---|---|
| Email | `KeyboardType.Email` |
| Password | `KeyboardType.Password` |
| Phone number | `KeyboardType.Phone` |
| Integer number | `KeyboardType.Number` |
| Decimal number | `KeyboardType.Decimal` |
| URL | `KeyboardType.Uri` |
| Generic text | `KeyboardType.Text` (default) |

### `ImeAction` Reference

| Position in form | `ImeAction` |
|---|---|
| Not the last field | `ImeAction.Next` |
| Last field | `ImeAction.Done` |
| Search input | `ImeAction.Search` |
| URL bar | `ImeAction.Go` |

---

## FocusRequester and Focus Traversal

`FocusRequester` lets you move focus to a specific field programmatically — useful for auto-focusing the first field, skipping to an error field, or handling "Next" manually.

```kotlin
@Composable
fun RegisterScreen(state: RegisterFormState, onAction: (RegisterAction) -> Unit) {
    val focusManager = LocalFocusManager.current
    val emailFocusRequester = remember { FocusRequester() }
    val passwordFocusRequester = remember { FocusRequester() }

    // Auto-focus name field when screen opens
    LaunchedEffect(Unit) {
        // Small delay to let the composition settle
        delay(100)
        // If you had a nameFocusRequester: nameFocusRequester.requestFocus()
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        // Name field — Next moves to email
        OutlinedTextField(
            value = state.name,
            onValueChange = { onAction(RegisterAction.NameChanged(it)) },
            label = { Text("Full name") },
            isError = state.nameError != null,
            supportingText = state.nameError?.let { { Text(it.asString()) } },
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Text,
                imeAction = ImeAction.Next,
                capitalization = KeyboardCapitalization.Words
            ),
            keyboardActions = KeyboardActions(
                onNext = { emailFocusRequester.requestFocus() }
            ),
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )

        // Email field — Next moves to password
        OutlinedTextField(
            value = state.email,
            onValueChange = { onAction(RegisterAction.EmailChanged(it)) },
            label = { Text("Email") },
            isError = state.emailError != null,
            supportingText = state.emailError?.let { { Text(it.asString()) } },
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Email,
                imeAction = ImeAction.Next
            ),
            keyboardActions = KeyboardActions(
                onNext = { passwordFocusRequester.requestFocus() }
            ),
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .focusRequester(emailFocusRequester)
        )

        // Password field — Done submits the form
        PasswordField(
            value = state.password,
            isVisible = state.isPasswordVisible,
            error = state.passwordError,
            onValueChange = { onAction(RegisterAction.PasswordChanged(it)) },
            onToggleVisibility = { onAction(RegisterAction.TogglePasswordVisibility) },
            onDone = {
                focusManager.clearFocus()
                onAction(RegisterAction.Submit)
            },
            modifier = Modifier
                .fillMaxWidth()
                .focusRequester(passwordFocusRequester)
        )

        Button(
            onClick = { onAction(RegisterAction.Submit) },
            enabled = !state.isSubmitting,
            modifier = Modifier.fillMaxWidth()
        ) {
            if (state.isSubmitting) {
                CircularProgressIndicator(modifier = Modifier.size(18.dp), strokeWidth = 2.dp)
            } else {
                Text("Create account")
            }
        }
    }
}
```

---

## Password Field

Extract the password field into its own composable — the toggle logic is reusable across login and register screens.

```kotlin
@Composable
fun PasswordField(
    value: String,
    isVisible: Boolean,
    error: UiText?,
    onValueChange: (String) -> Unit,
    onToggleVisibility: () -> Unit,
    onDone: () -> Unit,
    modifier: Modifier = Modifier,
    label: String = "Password"
) {
    OutlinedTextField(
        value = value,
        onValueChange = onValueChange,
        label = { Text(label) },
        isError = error != null,
        supportingText = error?.let { { Text(it.asString()) } },
        visualTransformation = if (isVisible) VisualTransformation.None
                               else PasswordVisualTransformation(),
        trailingIcon = {
            IconButton(onClick = onToggleVisibility) {
                Icon(
                    imageVector = if (isVisible) Icons.Default.VisibilityOff
                                  else Icons.Default.Visibility,
                    contentDescription = if (isVisible) "Hide password" else "Show password"
                )
            }
        },
        keyboardOptions = KeyboardOptions(
            keyboardType = KeyboardType.Password,
            imeAction = ImeAction.Done
        ),
        keyboardActions = KeyboardActions(onDone = { onDone() }),
        singleLine = true,
        modifier = modifier
    )
}
```

Key points:
- `PasswordVisualTransformation()` replaces each character with a bullet. The actual value in state is always the plain text.
- The toggle icon's `contentDescription` changes with visibility state so screen readers announce the correct action.
- `KeyboardType.Password` prevents the IME from suggesting autocomplete for this field.

---

## Showing Errors — `isError` and `supportingText`

Material3 `OutlinedTextField` / `TextField` natively support error state:

```kotlin
OutlinedTextField(
    value = state.email,
    onValueChange = { onAction(FormAction.EmailChanged(it)) },
    label = { Text("Email") },
    isError = state.emailError != null,       // turns field outline red
    supportingText = state.emailError?.let {  // shown below the field
        { Text(it.asString(), color = MaterialTheme.colorScheme.error) }
    },
    singleLine = true,
    modifier = Modifier.fillMaxWidth()
)
```

`isError = true` changes the outline, label, and cursor to `MaterialTheme.colorScheme.error` automatically. The `supportingText` slot shows the message below the field. Both are reset by setting `isError = false` and `supportingText = null`.

---

## Mapping Server-Side Validation Errors

When the server returns field-level errors (e.g., "email already taken"), map them to `UiText` in the ViewModel after receiving the API response:

```kotlin
authRepository.register(state.email, state.password)
    .onFailure { error ->
        state = state.copy(
            isSubmitting = false,
            emailError = when (error) {
                AuthError.EMAIL_TAKEN ->
                    UiText.StringResource(R.string.error_email_taken)
                AuthError.INVALID_EMAIL_FORMAT ->
                    UiText.StringResource(R.string.error_email_invalid)
                else -> null
            },
            passwordError = when (error) {
                AuthError.PASSWORD_TOO_WEAK ->
                    UiText.StringResource(R.string.error_password_weak)
                else -> null
            }
        )
    }
```

For the `UiText` type and `DataError` / `AuthError` definitions, see the android-error-handling skill.

---

## Multi-Field Form: Scrollable Layout

Wrap the form in a `verticalScroll` column so the keyboard does not obscure the active field. Combine with `WindowInsets.ime` padding so the form shifts up when the keyboard appears:

```kotlin
Column(
    modifier = Modifier
        .fillMaxSize()
        .imePadding()                    // shifts content above keyboard
        .verticalScroll(rememberScrollState())
        .padding(horizontal = 16.dp)
        .padding(top = 24.dp, bottom = 32.dp),
    verticalArrangement = Arrangement.spacedBy(12.dp)
) {
    // fields...
}
```

`imePadding()` requires the Activity to handle window insets (`WindowCompat.setDecorFitsSystemWindows(window, false)` in `onCreate`). This is the standard setup in any app using `enableEdgeToEdge()`.

---

## Form Checklist

- [ ] All fields have a `label`
- [ ] All fields set appropriate `KeyboardType`
- [ ] All fields except the last set `ImeAction.Next`; the last field sets `ImeAction.Done`
- [ ] `KeyboardActions.onNext` moves focus to the next field
- [ ] `KeyboardActions.onDone` on the last field submits the form or clears focus
- [ ] Password fields use `PasswordVisualTransformation` and have a visibility toggle
- [ ] `isError` and `supportingText` are wired to each field's error in state
- [ ] Errors are cleared immediately when the user edits the field
- [ ] Full validation runs on submit before any network call
- [ ] `isSubmitting = true` disables the submit button to prevent double-submission
- [ ] `imePadding()` + `verticalScroll` ensure fields are not hidden by the keyboard
- [ ] Server-side field errors are mapped back to `UiText?` in the ViewModel
