# Vue 3 Multi-API Project Rules

## 1. Architecture & File Structure
- **SFC Standard**: Always use `<script setup>` with the Composition API. No Options API.
- **Logic Separation**: If a component's script exceeds 50 lines, suggest moving logic to a 'composable' (e.g., `src/composables/use[Feature].js`).
- **API Centralization**: All API calls must go through `src/api/auth.js` or `src/api/crud.js`. Never use `axios` directly inside a `.vue` file.

## 2. Coding Patterns (Performance & Safety)
- **Token Handling**: Retrieve tokens via `getAuthorization()` from the store. Never hardcode "Bearer" strings in components.
- **Reactivity**: Use `shallowRef` for large arrays (document lists, logs) to save CPU/RAM on Intel Macs.
- **CRUD Operations**: Use the `crud.js` actions (`list`, `read`, `create`) to maintain consistent URL structures.
- **GET Requests**: Always use the `params` key for GET requests in Axios, never the `data` key.

## 3. Security Guardrails
- **Input Sanitization**: Always use `{{ }}` for data binding. Flag any use of `v-html` as a security risk for XSS.
- **Redirection**: Ensure `router.push` only triggers after a successful API response and a valid token check.
- **Error Handling**: Every async function must use `try/catch/finally`. The `finally` block MUST reset `isLoading.value = false`.

## 4. Document Flow Specifics
- **File Uploads**: Ensure `uploadPdf` and `uploadPicture` use `formData` and have the `Content-Type: multipart/form-data` header.
- **Cleanup**: In pages with PDF previews or large data sets, always include `onUnmounted` to clear refs and stop memory leaks.