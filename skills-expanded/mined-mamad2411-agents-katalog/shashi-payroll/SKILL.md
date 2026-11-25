# Payroll Application - Cursor Rules

## Core Standards

### 1. Status Codes & Messages
- **ALWAYS** use constants from `server/utils/constants/statusCodes.js` and `server/utils/constants/messages.js`
- **ALWAYS** use constants from `client/src/constants/statusCodes.ts` and `client/src/constants/messages.ts`
- **NEVER** hardcode status codes or messages
- **ALWAYS** return proper HTTP status codes in server responses
- **ALWAYS** check response status in client API calls

### 2. Global UI Components (Loader & Toaster)
- **ALWAYS** use `useUI()` hook from `contexts/ThemeContext` for loader and toaster
- **ALWAYS** show loader during API calls: `showLoader(true)` at start, `showLoader(false)` in finally
- **ALWAYS** show toast for user feedback: success, error, info messages
- **NEVER** use local loading states when global loader is available
- **NEVER** use local alert/notification components when global toaster is available

### 3. API Call Pattern (Client)
```typescript
const handleApiCall = async () => {
  try {
    showLoader(true);
    const response = await api('/endpoint', { method: 'POST', body: data });
    if (response.status !== STATUS.OK) throw new Error(response.message);
    showToast('Success message', 'success');
  } catch (error) {
    showToast(error.message, 'error');
  } finally {
    showLoader(false);
  }
};
```

### 4. Server Response Pattern
```javascript
// Success
res.status(STATUS.OK).json({ data, message: MSG.SUCCESS_MESSAGE });

// Error
res.status(STATUS.BAD_REQUEST).json({ error: MSG.ERROR_MESSAGE });
```

### 5. File Structure Standards
- **Server constants**: `server/utils/constants/statusCodes.js`, `server/utils/constants/messages.js`
- **Client constants**: `client/src/constants/statusCodes.ts`, `client/src/constants/messages.ts`
- **UI context**: `client/src/contexts/ThemeContext.tsx` (contains useUI hook)
- **Layouts**: All layouts must provide UI context to children

### 6. Import Standards
```typescript
// Client - Always import these for API calls
import STATUS from '../constants/statusCodes';
import MSG from '../constants/messages';
import { useUI } from '../contexts/ThemeContext';

// Server - Always import these for responses
const STATUS = require('../utils/constants/statusCodes');
const MSG = require('../utils/constants/messages');
```

### 7. Toast Message Standards
- **Success**: Use for successful operations (save, update, delete, login, logout)
- **Error**: Use for failed operations with specific error messages
- **Info**: Use for informational messages (theme changes, page loads)
- **Warning**: Use for validation warnings or important notices

### 8. Loader Usage Standards
- **ALWAYS** show loader for API calls that take time
- **ALWAYS** hide loader in finally block to ensure it's always hidden
- **NEVER** show loader for instant operations
- **NEVER** forget to hide loader on error

### 9. Error Handling Standards
- **ALWAYS** catch errors in try-catch blocks
- **ALWAYS** show error toasts with meaningful messages
- **ALWAYS** log errors to console for debugging
- **NEVER** let errors crash the UI

### 10. Layout Requirements
- **ALL** protected routes must be wrapped with appropriate layout (AdminLayout, ClientLayout, EmployeeLayout)
- **ALL** layouts must provide UI context via ThemeProvider
- **ALL** layouts must have Profile and Logout in avatar dropdown
- **ALL** layouts must have theme toggle with toast feedback

### 11. Component Standards
- **ALL** components making API calls must use global loader/toaster
- **ALL** forms must show loading state during submission
- **ALL** navigation must show appropriate feedback
- **ALL** user actions must provide visual feedback

### 12. Testing Standards
- **ALWAYS** test that toasts appear for user actions
- **ALWAYS** test that loaders show during API calls
- **ALWAYS** test that errors are handled gracefully
- **ALWAYS** test that success messages are shown

### 13. Code Review Checklist
- [ ] Status codes imported and used correctly
- [ ] Messages imported and used correctly
- [ ] Loader shown/hidden properly
- [ ] Toast messages appropriate and helpful
- [ ] Error handling complete
- [ ] No hardcoded strings for user messages
- [ ] No local loading states when global available
- [ ] Layout provides UI context
- [ ] API calls follow standard pattern

### 14. Common Violations to Avoid
- ❌ Hardcoded status codes: `res.status(400)`
- ❌ Hardcoded messages: `'User not found'`
- ❌ Local loading states: `const [loading, setLoading] = useState(false)`
- ❌ Local alerts: `<Alert>` components for notifications
- ❌ Missing error handling in API calls
- ❌ Forgetting to hide loader on error
- ❌ Generic error messages
- ❌ Components not wrapped with layout
- ❌ Missing UI context imports

### 15. Performance Standards
- **ALWAYS** use useCallback for functions passed to useEffect
- **ALWAYS** include all dependencies in useEffect dependency arrays
- **ALWAYS** clean up event listeners and subscriptions
- **NEVER** create unnecessary re-renders

Remember: Consistency is key. Every API call should follow the same pattern, every user action should provide feedback, and every error should be handled gracefully.
