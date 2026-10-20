# Cursor Rule: Device-Based User Initialization & API Context for Mobile Apps

## 1. Device User ID Generation & Storage
- On first app launch, generate a unique device user ID (UUID).
- Persist this ID securely on the device (e.g., using SecureStore, Keychain, or SharedPreferences).
- On subsequent launches, retrieve the persisted device user ID.

## 2. Backend User Initialization
- On every app startup, ensure the device user exists in the backend by calling a dedicated endpoint (e.g., `/users` with `{ user_id }`).
  - This operation must be idempotent (use upsert semantics).
  - Call this as early as possible (e.g., in the root component’s initialization logic).

## 3. API Call Context
- For all API calls that are user-specific, include the device user ID:
  - Preferably, send the user ID as a custom HTTP header (e.g., `x-device-user-id`).
  - Alternatively, include it as a query parameter or in the request body.
- The backend must extract the user ID from the header (or body/query) and use it to scope all user-specific operations.

## 4. Example Implementation (React Native)
```typescript
// On app startup
useEffect(() => {
  getDeviceUserId(); // Ensures user is created/upserted in backend
}, []);

// API call example with custom header
const userId = await getDeviceUserId();
fetch('/api/books', {
  method: 'GET',
  headers: {
    'x-device-user-id': userId,
    'Content-Type': 'application/json',
  },
});
```

## 5. Security & Consistency
- Never expose or transmit the device user ID insecurely.
- Always check for the existence of the device user ID before making user-specific API calls.
- The backend should validate the presence of the user ID in every request that requires user context.

---

**Summary:**  
Every mobile app must generate and persist a device user ID, ensure the user exists in the backend at startup, and include the user ID in all user-specific API calls (preferably as a custom header). The backend must use this ID to scope all user data and actions.
