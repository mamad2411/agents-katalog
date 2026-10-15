# Dynamic Config Management

**Extracted from**: Make a Million app debugging session  
**Pattern**: Hardcoded configuration values causing production failures  
**Category**: Configuration Management

---

## Overview

Stop hardcoding configuration values in your code. This skill teaches you how to dynamically load configuration from centralized config files, preventing maintenance nightmares and ensuring config stays in sync with your build environment.

## The Problem

**Symptom**: Features completely non-functional in production due to hardcoded placeholder values.

**Example from Make a Million app**:
```typescript
// ❌ BAD: Hardcoded placeholder
const token = await Notifications.getExpoPushTokenAsync({
  projectId: 'your-project-id', // Placeholder!
});
```

**Impact**:
- Push notifications completely broken
- Production blocker
- Easy to miss in code review
- Creates maintenance debt

---

## The Solution Pattern

### For Expo/React Native Apps

**Use `expo-constants` to dynamically load from `app.config.ts`:**

```typescript
import Constants from 'expo-constants';

// ✅ GOOD: Dynamic config loading
const projectId = Constants.expoConfig?.extra?.eas?.projectId;

if (!projectId) {
  console.error('No Expo project ID found in app.config.ts');
  return null;
}

const token = await Notifications.getExpoPushTokenAsync({
  projectId,
});
```

**Why this works**:
- Config sourced from single source of truth (`app.config.ts`)
- Automatically stays in sync with build configuration
- Prevents mismatches between code and build config
- Easy to validate during CI/CD

---

### For Node.js/Backend Apps

**Use environment variables with validation:**

```typescript
// config.ts
import { z } from 'zod';

const configSchema = z.object({
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
  PORT: z.coerce.number().default(3000),
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
});

export const config = configSchema.parse(process.env);
```

**Usage**:
```typescript
import { config } from './config';

// ✅ Type-safe, validated config
const db = createConnection(config.DATABASE_URL);
```

---

### For Web Apps

**Use build-time environment variables:**

```typescript
// vite.config.ts
export default defineConfig({
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    __API_URL__: JSON.stringify(process.env.VITE_API_URL),
  },
});
```

**Usage**:
```typescript
// ✅ Replaced at build time
const apiUrl = __API_URL__;
```

---

## Implementation Checklist

### 1. Identify Hardcoded Values

Search your codebase for common patterns:

```bash
# Find hardcoded URLs
grep -r "http://" src/ | grep -v "//http"

# Find hardcoded API keys (common patterns)
grep -r "api[_-]key.*=.*['\"]" src/

# Find TODO/FIXME placeholders
grep -r "your-.*-here\|REPLACE_ME\|TODO.*config" src/
```

### 2. Create Config Schema

Define all configuration in one place:

```typescript
// app.config.ts (Expo)
export default {
  expo: {
    name: 'My App',
    extra: {
      eas: {
        projectId: process.env.EXPO_PROJECT_ID,
      },
      apiUrl: process.env.API_URL,
      sentryDsn: process.env.SENTRY_DSN,
    },
  },
};
```

### 3. Add Validation

Fail fast if required config is missing:

```typescript
function getConfig() {
  const projectId = Constants.expoConfig?.extra?.eas?.projectId;
  
  if (!projectId) {
    throw new Error(
      'Missing required config: EXPO_PROJECT_ID. ' +
      'Add it to your .env file or app.config.ts'
    );
  }
  
  return { projectId };
}
```

### 4. Document Required Config

Create `.env.example`:

```bash
# .env.example
EXPO_PROJECT_ID=your-expo-project-id-here
API_URL=https://api.example.com
SENTRY_DSN=https://your-sentry-dsn-here
```

---

## Prevention Strategies

### 1. Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for common placeholder patterns
if git diff --cached | grep -E "your-.*-here|REPLACE_ME|TODO.*config"; then
  echo "❌ Found placeholder config values in staged changes"
  echo "Replace placeholders with dynamic config loading"
  exit 1
fi
```

### 2. ESLint Rule

```javascript
// .eslintrc.js
module.exports = {
  rules: {
    'no-restricted-syntax': [
      'error',
      {
        selector: 'Literal[value=/your-.*-here/]',
        message: 'Do not hardcode placeholder values. Use dynamic config instead.',
      },
    ],
  },
};
```

### 3. CI/CD Validation

```yaml
# .github/workflows/validate.yml
- name: Validate Config
  run: |
    # Check that all required env vars are documented
    grep -q "EXPO_PROJECT_ID" .env.example || exit 1
    grep -q "API_URL" .env.example || exit 1
```

---

## Common Patterns

### API URLs

```typescript
// ❌ BAD
const API_URL = 'https://api.example.com';

// ✅ GOOD
const API_URL = Constants.expoConfig?.extra?.apiUrl || process.env.API_URL;
```

### API Keys

```typescript
// ❌ BAD
const SENTRY_DSN = 'https://abc123@sentry.io/456';

// ✅ GOOD
const SENTRY_DSN = process.env.SENTRY_DSN;
if (!SENTRY_DSN) {
  console.warn('Sentry not configured - error tracking disabled');
}
```

### Feature Flags

```typescript
// ❌ BAD
const ENABLE_NEW_FEATURE = true;

// ✅ GOOD
const ENABLE_NEW_FEATURE = 
  Constants.expoConfig?.extra?.features?.newFeature ?? false;
```

---

## Troubleshooting

### Config Not Loading

**Problem**: `Constants.expoConfig?.extra` is undefined

**Solution**:
1. Check `app.config.ts` exports the config correctly
2. Restart Metro bundler: `npx expo start -c`
3. Verify environment variables are loaded: `console.log(process.env)`

### Build-time vs Runtime

**Problem**: Config works locally but not in production build

**Solution**:
- Expo: Use `extra` in `app.config.ts` (available at runtime)
- Web: Use `import.meta.env` (Vite) or `process.env` (Next.js)
- Never use `process.env` directly in React Native (not available at runtime)

---

## Key Takeaways

1. **Never hardcode config values** - Always use dynamic loading
2. **Single source of truth** - Centralize all config in one file
3. **Validate early** - Fail fast if required config is missing
4. **Document requirements** - Use `.env.example` to show what's needed
5. **Automate checks** - Use pre-commit hooks and CI/CD validation

---

## Related Patterns

- **Environment-specific Config**: Different config for dev/staging/prod
- **Secret Management**: Secure handling of API keys and credentials
- **Feature Flags**: Runtime feature toggles without code changes

---

**Extracted from Make a Million app**: This pattern emerged from debugging a critical production issue where hardcoded placeholder values caused push notifications to fail completely. The solution saved hours of debugging and prevented future config-related issues.

**"The answer lies in the darkness"** - This gem was mined from a production failure! 💎
