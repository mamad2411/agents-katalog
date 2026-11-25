---
name: test-url-resolution
description: "Resolve the test base URL for E2E and verification testing. Use when you need to determine where to run tests - localhost, staging, or preview environment. Triggers on: test URL, base URL, test environment, preview URL, staging URL, where to run tests."
---

# Test URL Resolution

> Load this skill when: you need to determine the correct base URL for E2E tests, screenshots, or any browser-based verification.

## Overview

This skill resolves the test base URL using a priority chain that supports:
- Explicit configuration overrides
- Dynamic preview environment detection (Vercel, Netlify, Railway, Render, Fly.io)
- Staging environment URLs
- Local development servers

**Why use this skill:** Ensures consistent URL resolution across all testing agents instead of hardcoded `localhost:${devPort}`.

## Input

When invoking this skill, provide:
- **projectPath**: Absolute path to the project root (e.g., `/Users/mark/code/my-project`)

## Output

Returns one of:
- **URL string**: The resolved test base URL (e.g., `https://my-app.vercel.app` or `http://localhost:3000`)
- **null**: Cannot resolve URL — project cannot be tested in current environment

Also outputs a log message indicating the source:
```
🌐 Test environment: [type]
   URL: [resolved-url]
   Source: [where the URL came from]
```

## Resolution Priority

The URL is resolved in this order (first match wins):

| Priority | Source | Description |
|----------|--------|-------------|
| 1 | `projects.json` → `testBaseUrl` | Explicit per-project override in registry |
| 2 | `project.json` → `agents.verification.testBaseUrl` | Explicit override in project config |
| 3 | Environment variables | Auto-detected preview URLs (Vercel, Netlify, etc.) |
| 4 | `project.json` → `environments.staging.url` | Configured staging environment |
| 5 | `projects.json` → `devPort` | Local dev server (`http://localhost:${devPort}`) |
| 6 | null | Cannot resolve — no testable environment |

## Steps

### Step 1: Check Explicit Configuration (projects.json)

```bash
# Check for testBaseUrl in projects.json registry
TEST_URL=$(jq -r --arg path "$PROJECT_PATH" \
  '.projects[] | select(.path == $path) | .testBaseUrl // empty' \
  ~/.config/opencode/projects.json)

if [ -n "$TEST_URL" ]; then
  echo "🌐 Test environment: Custom"
  echo "   URL: $TEST_URL"
  echo "   Source: testBaseUrl in projects.json"
  export TEST_BASE_URL="$TEST_URL"
  exit 0
fi
```

### Step 2: Check Explicit Configuration (project.json)

```bash
# Check for testBaseUrl in project.json
TEST_URL=$(jq -r '.agents.verification.testBaseUrl // empty' \
  "$PROJECT_PATH/docs/project.json" 2>/dev/null)

if [ -n "$TEST_URL" ]; then
  echo "🌐 Test environment: Custom"
  echo "   URL: $TEST_URL"
  echo "   Source: agents.verification.testBaseUrl in project.json"
  export TEST_BASE_URL="$TEST_URL"
  exit 0
fi
```

### Step 3: Detect Preview Environment

Check for preview environment variables from common deployment platforms:

```bash
# Vercel
if [ -n "$VERCEL_URL" ]; then
  TEST_URL="https://$VERCEL_URL"
  echo "🌐 Test environment: Vercel preview"
  echo "   URL: $TEST_URL"
  echo "   Source: VERCEL_URL environment variable"
  export TEST_BASE_URL="$TEST_URL"
  exit 0
fi

if [ -n "$NEXT_PUBLIC_VERCEL_URL" ]; then
  TEST_URL="https://$NEXT_PUBLIC_VERCEL_URL"
  echo "🌐 Test environment: Vercel preview"
  echo "   URL: $TEST_URL"
  echo "   Source: NEXT_PUBLIC_VERCEL_URL environment variable"
  export TEST_BASE_URL="$TEST_URL"
  exit 0
fi

# Netlify
if [ -n "$DEPLOY_URL" ]; then
  TEST_URL="$DEPLOY_URL"
  echo "🌐 Test environment: Netlify preview"
  echo "   URL: $TEST_URL"
  echo "   Source: DEPLOY_URL environment variable"
  export TEST_BASE_URL="$TEST_URL"
  exit 0
fi

if [ -n "$DEPLOY_PRIME_URL" ]; then
  TEST_URL="$DEPLOY_PRIME_URL"
  echo "🌐 Test environment: Netlify preview"
  echo "   URL: $TEST_URL"
  echo "   Source: DEPLOY_PRIME_URL environment variable"
  export TEST_BASE_URL="$TEST_URL"
  exit 0
fi

# Railway
if [ -n "$RAILWAY_PUBLIC_DOMAIN" ]; then
  TEST_URL="https://$RAILWAY_PUBLIC_DOMAIN"
  echo "🌐 Test environment: Railway"
  echo "   URL: $TEST_URL"
  echo "   Source: RAILWAY_PUBLIC_DOMAIN environment variable"
  export TEST_BASE_URL="$TEST_URL"
  exit 0
fi

# Render
if [ -n "$RENDER_EXTERNAL_URL" ]; then
  TEST_URL="$RENDER_EXTERNAL_URL"
  echo "🌐 Test environment: Render"
  echo "   URL: $TEST_URL"
  echo "   Source: RENDER_EXTERNAL_URL environment variable"
  export TEST_BASE_URL="$TEST_URL"
  exit 0
fi

# Fly.io
if [ -n "$FLY_APP_NAME" ]; then
  TEST_URL="https://${FLY_APP_NAME}.fly.dev"
  echo "🌐 Test environment: Fly.io"
  echo "   URL: $TEST_URL"
  echo "   Source: FLY_APP_NAME environment variable"
  export TEST_BASE_URL="$TEST_URL"
  exit 0
fi
```

### Step 4: Check Staging Configuration

```bash
# Check for staging URL in project.json
STAGING_URL=$(jq -r '.environments.staging.url // empty' \
  "$PROJECT_PATH/docs/project.json" 2>/dev/null)

if [ -n "$STAGING_URL" ]; then
  echo "🌐 Test environment: Staging"
  echo "   URL: $STAGING_URL"
  echo "   Source: environments.staging.url in project.json"
  export TEST_BASE_URL="$STAGING_URL"
  exit 0
fi
```

### Step 5: Fall Back to Local Dev Server

```bash
# Check for devPort in projects.json
DEV_PORT=$(jq -r --arg path "$PROJECT_PATH" \
  '.projects[] | select(.path == $path) | .devPort // empty' \
  ~/.config/opencode/projects.json)

if [ -n "$DEV_PORT" ] && [ "$DEV_PORT" != "null" ]; then
  TEST_URL="http://localhost:$DEV_PORT"
  echo "🌐 Test environment: Local dev server"
  echo "   URL: $TEST_URL"
  echo "   Source: devPort in projects.json"
  export TEST_BASE_URL="$TEST_URL"
  exit 0
fi
```

### Step 6: Cannot Resolve — Report Error

```bash
echo "❌ Cannot determine test URL"
echo ""
echo "   This project has:"
echo "   - devPort: ${DEV_PORT:-not set} (no local server)"
echo "   - No staging URL configured"
echo "   - No preview environment detected"
echo ""
echo "   Options:"
echo "   1. Add testBaseUrl to projects.json"
echo "   2. Add environments.staging.url to project.json"
echo "   3. Set devPort if you have a local server"

export TEST_BASE_URL=""
exit 1
```

## Complete Resolution Script

Copy this script for use in agents:

```bash
#!/bin/bash
# resolve-test-url.sh
# Usage: source resolve-test-url.sh /path/to/project
# Sets: TEST_BASE_URL environment variable

PROJECT_PATH="${1:-.}"

# 1. Check projects.json testBaseUrl
TEST_URL=$(jq -r --arg path "$PROJECT_PATH" \
  '.projects[] | select(.path == $path) | .testBaseUrl // empty' \
  ~/.config/opencode/projects.json 2>/dev/null)

if [ -n "$TEST_URL" ]; then
  echo "🌐 Test environment: Custom (projects.json)"
  echo "   URL: $TEST_URL"
  export TEST_BASE_URL="$TEST_URL"
  return 0 2>/dev/null || exit 0
fi

# 2. Check project.json agents.verification.testBaseUrl
TEST_URL=$(jq -r '.agents.verification.testBaseUrl // empty' \
  "$PROJECT_PATH/docs/project.json" 2>/dev/null)

if [ -n "$TEST_URL" ]; then
  echo "🌐 Test environment: Custom (project.json)"
  echo "   URL: $TEST_URL"
  export TEST_BASE_URL="$TEST_URL"
  return 0 2>/dev/null || exit 0
fi

# 3. Check preview environment variables
for VAR in VERCEL_URL NEXT_PUBLIC_VERCEL_URL; do
  VAL="${!VAR}"
  if [ -n "$VAL" ]; then
    [[ "$VAL" != https://* ]] && VAL="https://$VAL"
    echo "🌐 Test environment: Vercel preview"
    echo "   URL: $VAL"
    export TEST_BASE_URL="$VAL"
    return 0 2>/dev/null || exit 0
  fi
done

for VAR in DEPLOY_URL DEPLOY_PRIME_URL; do
  VAL="${!VAR}"
  if [ -n "$VAL" ]; then
    echo "🌐 Test environment: Netlify preview"
    echo "   URL: $VAL"
    export TEST_BASE_URL="$VAL"
    return 0 2>/dev/null || exit 0
  fi
done

if [ -n "$RAILWAY_PUBLIC_DOMAIN" ]; then
  TEST_URL="https://$RAILWAY_PUBLIC_DOMAIN"
  echo "🌐 Test environment: Railway"
  echo "   URL: $TEST_URL"
  export TEST_BASE_URL="$TEST_URL"
  return 0 2>/dev/null || exit 0
fi

if [ -n "$RENDER_EXTERNAL_URL" ]; then
  echo "🌐 Test environment: Render"
  echo "   URL: $RENDER_EXTERNAL_URL"
  export TEST_BASE_URL="$RENDER_EXTERNAL_URL"
  return 0 2>/dev/null || exit 0
fi

if [ -n "$FLY_APP_NAME" ]; then
  TEST_URL="https://${FLY_APP_NAME}.fly.dev"
  echo "🌐 Test environment: Fly.io"
  echo "   URL: $TEST_URL"
  export TEST_BASE_URL="$TEST_URL"
  return 0 2>/dev/null || exit 0
fi

# 4. Check staging URL
STAGING_URL=$(jq -r '.environments.staging.url // empty' \
  "$PROJECT_PATH/docs/project.json" 2>/dev/null)

if [ -n "$STAGING_URL" ]; then
  echo "🌐 Test environment: Staging"
  echo "   URL: $STAGING_URL"
  export TEST_BASE_URL="$STAGING_URL"
  return 0 2>/dev/null || exit 0
fi

# 5. Fall back to localhost
DEV_PORT=$(jq -r --arg path "$PROJECT_PATH" \
  '.projects[] | select(.path == $path) | .devPort // empty' \
  ~/.config/opencode/projects.json 2>/dev/null)

if [ -n "$DEV_PORT" ] && [ "$DEV_PORT" != "null" ]; then
  TEST_URL="http://localhost:$DEV_PORT"
  echo "🌐 Test environment: Local dev server"
  echo "   URL: $TEST_URL"
  export TEST_BASE_URL="$TEST_URL"
  return 0 2>/dev/null || exit 0
fi

# 6. Cannot resolve
echo "❌ Cannot determine test URL"
echo ""
echo "   Options:"
echo "   1. Add testBaseUrl to projects.json"
echo "   2. Add environments.staging.url to project.json"
echo "   3. Set devPort for local development"
export TEST_BASE_URL=""
return 1 2>/dev/null || exit 1
```

## Inline Resolution Logic for Agents

For agents that need inline resolution (without loading the skill), use this pattern:

```markdown
### Resolve Test Base URL

Before running tests, resolve the test URL:

1. **Check explicit config:**
   ```bash
   # Check projects.json for testBaseUrl
   TEST_URL=$(jq -r --arg path "$PROJECT_PATH" '.projects[] | select(.path == $path) | .testBaseUrl // empty' ~/.config/opencode/projects.json)
   
   # If not set, check project.json
   [ -z "$TEST_URL" ] && TEST_URL=$(jq -r '.agents.verification.testBaseUrl // empty' "$PROJECT_PATH/docs/project.json" 2>/dev/null)
   ```

2. **Check preview environment (if no explicit config):**
   ```bash
   [ -z "$TEST_URL" ] && [ -n "$VERCEL_URL" ] && TEST_URL="https://$VERCEL_URL"
   [ -z "$TEST_URL" ] && [ -n "$DEPLOY_URL" ] && TEST_URL="$DEPLOY_URL"
   [ -z "$TEST_URL" ] && [ -n "$RAILWAY_PUBLIC_DOMAIN" ] && TEST_URL="https://$RAILWAY_PUBLIC_DOMAIN"
   [ -z "$TEST_URL" ] && [ -n "$RENDER_EXTERNAL_URL" ] && TEST_URL="$RENDER_EXTERNAL_URL"
   [ -z "$TEST_URL" ] && [ -n "$FLY_APP_NAME" ] && TEST_URL="https://${FLY_APP_NAME}.fly.dev"
   ```

3. **Check staging config (if no preview):**
   ```bash
   [ -z "$TEST_URL" ] && TEST_URL=$(jq -r '.environments.staging.url // empty' "$PROJECT_PATH/docs/project.json" 2>/dev/null)
   ```

4. **Fall back to localhost:**
   ```bash
   if [ -z "$TEST_URL" ]; then
     DEV_PORT=$(jq -r --arg path "$PROJECT_PATH" '.projects[] | select(.path == $path) | .devPort // empty' ~/.config/opencode/projects.json)
     [ -n "$DEV_PORT" ] && [ "$DEV_PORT" != "null" ] && TEST_URL="http://localhost:$DEV_PORT"
   fi
   ```

5. **Handle no URL:**
   ```bash
   if [ -z "$TEST_URL" ]; then
     echo "❌ Cannot determine test URL — see test-url-resolution skill for options"
     # Skip testing or fail gracefully
   fi
   ```
```

## Supabase Preview Branch Detection

For database-aware testing, also detect Supabase preview branches:

```bash
# Check if using a Supabase preview branch
if [ -n "$SUPABASE_URL" ]; then
  # Compare with configured default
  DEFAULT_SUPABASE=$(jq -r '.integrations.supabase.url // empty' "$PROJECT_PATH/docs/project.json" 2>/dev/null)
  
  if [ -n "$DEFAULT_SUPABASE" ] && [ "$SUPABASE_URL" != "$DEFAULT_SUPABASE" ]; then
    echo "🗄️  Database: Supabase preview branch"
    echo "   URL: $SUPABASE_URL"
    echo "   (differs from default: $DEFAULT_SUPABASE)"
  fi
fi

# Check for explicit branch ID
if [ -n "$SUPABASE_BRANCH_ID" ]; then
  echo "🗄️  Database: Supabase branch $SUPABASE_BRANCH_ID"
fi
```

## Health Check for Remote URLs

When testing against non-localhost URLs, perform a health check first:

```bash
if [[ "$TEST_BASE_URL" != http://localhost* ]]; then
  # Use configured health check path or default to /
  HEALTH_PATH=$(jq -r '.devServer.healthCheck // "/"' "$PROJECT_PATH/docs/project.json" 2>/dev/null)
  HEALTH_URL="${TEST_BASE_URL}${HEALTH_PATH}"
  
  echo "🏥 Checking remote server health: $HEALTH_URL"
  
  # 10 second timeout for remote URLs (shorter than local)
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$HEALTH_URL" 2>/dev/null)
  
  if [ "$HTTP_STATUS" -ge 200 ] && [ "$HTTP_STATUS" -lt 400 ]; then
    echo "   ✅ Server responding (HTTP $HTTP_STATUS)"
  else
    echo "   ❌ Server not responding (HTTP $HTTP_STATUS)"
    echo ""
    echo "   Suggestions:"
    echo "   - Check deployment status"
    echo "   - Verify the URL is correct"
    echo "   - Try using localhost with devPort instead"
    exit 1
  fi
fi
```

## Related Skills

- `start-dev-server` — Use this skill AFTER URL resolution if testing against localhost
- `auth-headless` — For authenticated testing (works with any resolved URL)
- `screenshot` — For visual verification (pass resolved URL)
