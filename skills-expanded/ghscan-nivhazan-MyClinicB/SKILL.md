Perform a comprehensive code review of the MyClinicB clinic management app.

## Review Dimensions

### 1. Security
- Check for API keys or secrets exposed in frontend code (VITE_ env vars, hardcoded tokens)
- Verify input validation on Express endpoints
- Check for XSS vectors in React components (dangerouslySetInnerHTML, unescaped user input)
- Ensure Anthropic API key stays server-side only

### 2. Prisma Schema Consistency
- Verify all entities used in frontend (`base44.entities.X`) exist in `server/prisma/schema.prisma`
- Check that `expressClient.js` entity map matches the schema
- Verify relations and constraints (unique, required fields)
- Check `base44Client.mock.js` has matching entities

### 3. API & Error Handling
- Verify all Express routes return proper status codes and error messages
- Check that `asyncHandler` wraps all route handlers
- Verify business logic guards in payment creation (duplicate, future appointment, billing model)
- Check error messages are user-friendly (Hebrew)

### 4. Frontend/Backend Logic
- Detect duplicated validation between frontend and backend
- Verify frontend relies on backend for business rules (no client-side guards that bypass server)
- Check React Query keys are consistent and invalidated properly

### 5. Code Quality
- Find dead imports and unused files
- Check for console.log statements that should be removed
- Verify snake_case/camelCase mapping consistency

## Output Format

Organize findings by severity:

### Critical (must fix)
Security vulnerabilities, data loss risks, broken functionality.

### Important (should fix)
Logic errors, missing validation, inconsistencies.

### Minor (nice to fix)
Code quality, cleanup, naming.

For each finding include:
- **File:** `path/to/file.js:line`
- **Issue:** Description
- **Fix:** Suggested solution

## Action Rules
- For **minor** and **important** issues: fix them directly and commit
- For **critical** issues: describe them and wait for user approval before changing
