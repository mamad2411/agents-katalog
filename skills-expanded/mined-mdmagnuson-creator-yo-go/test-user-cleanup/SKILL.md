---
name: test-user-cleanup
description: "Clean up test users created during E2E and integration testing. Use when project.json has authentication.cleanup configured. Triggers on: cleanup test users, remove test data, test teardown, clean test database."
---

# Test User Cleanup

Remove test users created during E2E testing to keep the database clean and avoid pollution from automated test runs.

---

## Prerequisites

1. **Project configuration** in `docs/project.json`:
   ```json
   {
     "authentication": {
       "cleanup": {
         "enabled": true,
         "trigger": "auto",
         "pattern": "test-*@example.com",
         "maxAgeHours": 24,
         "safetyChecks": {
           "requireTestEmailPattern": true,
           "blockProduction": true
         }
       }
     }
   }
   ```

2. **Environment variables** in `.env.local`:
   ```
   NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=eyJ...
   NODE_ENV=development
   ```

---

## Cleanup Trigger Modes

### Manual (`"trigger": "manual"`)

Run cleanup explicitly via script or command:

```bash
npx tsx scripts/cleanup-test-users.ts
```

Use when:
- You want full control over when cleanup happens
- Running cleanup as a separate CI/CD step
- Debugging test data issues

### Auto (`"trigger": "auto"`)

Cleanup runs automatically after each test suite:

```typescript
// In your test setup (e.g., playwright.config.ts globalTeardown)
import { cleanupTestUsers } from './test-utils/cleanup';

export default async function globalTeardown() {
  await cleanupTestUsers();
}
```

Use when:
- You want tests to clean up after themselves
- Test isolation is important
- Running in CI where state shouldn't persist

### Scheduled (`"trigger": "scheduled"`)

Cleanup runs on a schedule (cron job or scheduled action):

```yaml
# .github/workflows/cleanup-test-users.yml
name: Cleanup Test Users
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx tsx scripts/cleanup-test-users.ts
        env:
          SUPABASE_SERVICE_ROLE_KEY: ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}
```

Use when:
- You don't want cleanup to slow down test runs
- Test data can persist for some time
- You have many test users to clean up (batch is more efficient)

---

## Cleanup Configuration

### Pattern Matching

Identify test users by email pattern:

```json
{
  "cleanup": {
    "pattern": "test-*@example.com"
  }
}
```

Pattern supports:
- `*` - matches any characters
- `?` - matches single character
- Examples:
  - `test-*@example.com` - emails starting with "test-"
  - `*@testmail.example.com` - any email at testmail subdomain
  - `e2e-????@example.com` - e2e- followed by exactly 4 characters

### Age-Based Cleanup

Only delete users older than a threshold:

```json
{
  "cleanup": {
    "maxAgeHours": 24,
    "preserveRecentMinutes": 5
  }
}
```

This prevents deleting users from currently running tests.

### Column-Based Identification

Mark test users with a flag column:

```json
{
  "cleanup": {
    "identifyBy": "column",
    "table": "users",
    "column": "is_test_user",
    "value": true
  }
}
```

---

## Safety Checks

### Required Test Email Pattern

Never delete users that don't match the test pattern:

```typescript
function isTestEmail(email: string, pattern: string): boolean {
  const regex = new RegExp(
    '^' + pattern.replace(/\*/g, '.*').replace(/\?/g, '.') + '$'
  );
  return regex.test(email);
}

// Safety: Reject any email that doesn't match
if (!isTestEmail(user.email, config.cleanup.pattern)) {
  console.warn(`Skipping ${user.email}: does not match test pattern`);
  continue;
}
```

### Block Production

Never run cleanup in production:

```typescript
function assertNotProduction(): void {
  const env = process.env.NODE_ENV;
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
  
  if (env === 'production') {
    throw new Error('SAFETY: Cleanup cannot run with NODE_ENV=production');
  }
  
  // Additional check: block if URL looks like production
  if (!url.includes('localhost') && !url.includes('staging') && !url.includes('dev')) {
    throw new Error(
      `SAFETY: Cleanup blocked. URL "${url}" may be production. ` +
      'Set ALLOW_CLEANUP_ON_REMOTE=true to override.'
    );
  }
}
```

### Dry Run Mode

Preview what would be deleted without actually deleting:

```bash
DRY_RUN=true npx tsx scripts/cleanup-test-users.ts
```

---

## Cleanup Implementations

### Supabase Cleanup

```typescript
import { createClient } from '@supabase/supabase-js';
import * as fs from 'fs';
import * as path from 'path';

interface CleanupConfig {
  enabled: boolean;
  trigger: 'manual' | 'auto' | 'scheduled';
  pattern: string;
  maxAgeHours?: number;
  preserveRecentMinutes?: number;
  safetyChecks?: {
    requireTestEmailPattern?: boolean;
    blockProduction?: boolean;
  };
}

function loadCleanupConfig(projectRoot: string): CleanupConfig {
  const projectJsonPath = path.join(projectRoot, 'docs', 'project.json');
  const projectJson = JSON.parse(fs.readFileSync(projectJsonPath, 'utf-8'));
  return projectJson.authentication?.cleanup || { enabled: false };
}

function loadEnv(projectRoot: string): void {
  const envPath = path.join(projectRoot, '.env.local');
  if (fs.existsSync(envPath)) {
    const content = fs.readFileSync(envPath, 'utf-8');
    content.split('\n').forEach(line => {
      const match = line.trim().match(/^([^=]+)=(.*)$/);
      if (match && !process.env[match[1]]) {
        process.env[match[1]] = match[2];
      }
    });
  }
}

function getSupabaseServiceClient() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  
  if (!url || !key) {
    throw new Error('Missing Supabase env vars');
  }
  
  return createClient(url, key, {
    auth: { autoRefreshToken: false, persistSession: false }
  });
}

function isTestEmail(email: string, pattern: string): boolean {
  const regex = new RegExp(
    '^' + pattern.replace(/\*/g, '.*').replace(/\?/g, '.') + '$',
    'i'
  );
  return regex.test(email);
}

function assertNotProduction(): void {
  if (process.env.NODE_ENV === 'production') {
    throw new Error('SAFETY: Cleanup cannot run in production');
  }
}

interface CleanupResult {
  deleted: string[];
  skipped: string[];
  errors: Array<{ email: string; error: string }>;
}

async function cleanupSupabaseTestUsers(
  projectRoot: string,
  options: { dryRun?: boolean } = {}
): Promise<CleanupResult> {
  loadEnv(projectRoot);
  const config = loadCleanupConfig(projectRoot);
  
  if (!config.enabled) {
    console.log('Cleanup is disabled in project.json');
    return { deleted: [], skipped: [], errors: [] };
  }
  
  // Safety checks
  if (config.safetyChecks?.blockProduction !== false) {
    assertNotProduction();
  }
  
  const supabase = getSupabaseServiceClient();
  const result: CleanupResult = { deleted: [], skipped: [], errors: [] };
  
  // Get all users
  const { data: { users }, error } = await supabase.auth.admin.listUsers();
  
  if (error) {
    throw new Error(`Failed to list users: ${error.message}`);
  }
  
  const now = new Date();
  const maxAgeMs = (config.maxAgeHours || 24) * 60 * 60 * 1000;
  const preserveMs = (config.preserveRecentMinutes || 5) * 60 * 1000;
  
  for (const user of users) {
    const email = user.email || '';
    
    // Check pattern
    if (config.safetyChecks?.requireTestEmailPattern !== false) {
      if (!isTestEmail(email, config.pattern)) {
        result.skipped.push(email);
        continue;
      }
    }
    
    // Check age
    const createdAt = new Date(user.created_at);
    const ageMs = now.getTime() - createdAt.getTime();
    
    if (ageMs < preserveMs) {
      console.log(`Preserving ${email}: created ${Math.round(ageMs / 1000)}s ago (too recent)`);
      result.skipped.push(email);
      continue;
    }
    
    if (config.maxAgeHours && ageMs < maxAgeMs) {
      console.log(`Preserving ${email}: only ${Math.round(ageMs / 3600000)}h old`);
      result.skipped.push(email);
      continue;
    }
    
    // Delete user
    if (options.dryRun) {
      console.log(`[DRY RUN] Would delete: ${email}`);
      result.deleted.push(email);
    } else {
      try {
        const { error: deleteError } = await supabase.auth.admin.deleteUser(user.id);
        if (deleteError) {
          result.errors.push({ email, error: deleteError.message });
        } else {
          console.log(`Deleted: ${email}`);
          result.deleted.push(email);
        }
      } catch (err) {
        result.errors.push({ email, error: String(err) });
      }
    }
  }
  
  return result;
}

// Main execution
async function main() {
  const projectRoot = process.cwd();
  const dryRun = process.env.DRY_RUN === 'true';
  
  console.log(`Running test user cleanup (dry run: ${dryRun})`);
  
  const result = await cleanupSupabaseTestUsers(projectRoot, { dryRun });
  
  console.log('\n--- Cleanup Summary ---');
  console.log(`Deleted: ${result.deleted.length} users`);
  console.log(`Skipped: ${result.skipped.length} users`);
  console.log(`Errors: ${result.errors.length}`);
  
  if (result.errors.length > 0) {
    console.error('\nErrors:');
    result.errors.forEach(e => console.error(`  ${e.email}: ${e.error}`));
    process.exit(1);
  }
}

main().catch(console.error);
```

### Prisma/Generic SQL Cleanup

```typescript
import { PrismaClient } from '@prisma/client';

async function cleanupPrismaTestUsers(
  pattern: string,
  options: { dryRun?: boolean; maxAgeHours?: number } = {}
): Promise<CleanupResult> {
  const prisma = new PrismaClient();
  const result: CleanupResult = { deleted: [], skipped: [], errors: [] };
  
  try {
    // Convert glob pattern to SQL LIKE pattern
    const likePattern = pattern.replace(/\*/g, '%').replace(/\?/g, '_');
    
    const cutoffDate = options.maxAgeHours
      ? new Date(Date.now() - options.maxAgeHours * 60 * 60 * 1000)
      : new Date(0);
    
    // Find matching users
    const users = await prisma.user.findMany({
      where: {
        email: { like: likePattern },
        createdAt: { lt: cutoffDate }
      },
      select: { id: true, email: true }
    });
    
    for (const user of users) {
      if (options.dryRun) {
        console.log(`[DRY RUN] Would delete: ${user.email}`);
        result.deleted.push(user.email);
      } else {
        try {
          await prisma.user.delete({ where: { id: user.id } });
          console.log(`Deleted: ${user.email}`);
          result.deleted.push(user.email);
        } catch (err) {
          result.errors.push({ email: user.email, error: String(err) });
        }
      }
    }
  } finally {
    await prisma.$disconnect();
  }
  
  return result;
}
```

---

## Script Templates

### Standalone Cleanup Script

Save as `scripts/cleanup-test-users.ts`:

```typescript
#!/usr/bin/env npx tsx

// Full Supabase cleanup implementation from above
// Run with: npx tsx scripts/cleanup-test-users.ts
// Dry run: DRY_RUN=true npx tsx scripts/cleanup-test-users.ts
```

### Playwright Global Teardown

```typescript
// playwright.config.ts
export default defineConfig({
  globalTeardown: './tests/global-teardown.ts',
});

// tests/global-teardown.ts
import { cleanupSupabaseTestUsers } from '../scripts/cleanup-test-users';

export default async function globalTeardown() {
  const config = JSON.parse(
    await fs.promises.readFile('./docs/project.json', 'utf-8')
  );
  
  if (config.authentication?.cleanup?.trigger === 'auto') {
    console.log('Running automatic test user cleanup...');
    await cleanupSupabaseTestUsers(process.cwd());
  }
}
```

### Jest afterAll Hook

```typescript
// tests/setup.ts
import { cleanupSupabaseTestUsers } from '../scripts/cleanup-test-users';

afterAll(async () => {
  if (process.env.CLEANUP_AFTER_TESTS === 'true') {
    await cleanupSupabaseTestUsers(process.cwd());
  }
});
```

---

## Cleanup Related Data

When deleting test users, also clean up related records:

```typescript
async function cleanupUserAndRelatedData(
  prisma: PrismaClient,
  userId: string
): Promise<void> {
  // Delete in order of dependencies
  await prisma.session.deleteMany({ where: { userId } });
  await prisma.account.deleteMany({ where: { userId } });
  await prisma.userSettings.deleteMany({ where: { userId } });
  await prisma.user.delete({ where: { id: userId } });
}
```

For Supabase with RLS and foreign keys, consider using CASCADE or cleaning up in order:

```sql
-- If your schema uses CASCADE, auth.users deletion handles it
-- Otherwise, clean up manually:
DELETE FROM public.user_profiles WHERE user_id = $1;
DELETE FROM public.user_settings WHERE user_id = $1;
-- Then delete from auth.users via admin API
```

---

## Troubleshooting

### "SAFETY: Cleanup cannot run in production"
This is intentional. Never run cleanup in production. If you need to clean test data from a staging environment that looks like production, set:
```
ALLOW_CLEANUP_ON_REMOTE=true
```

### "Missing Supabase env vars"
Ensure environment variables are set:
```
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

### Users not being deleted
Check:
- Email matches the pattern
- User is old enough (maxAgeHours, preserveRecentMinutes)
- `cleanup.enabled` is `true`

### Related data causing foreign key errors
Clean up related records first, or configure CASCADE deletes in your schema.

---

## Integration

This skill is used after test runs by:
- `ui-tester-playwright` - when `cleanup.trigger` is `auto`
- CI/CD pipelines - when `cleanup.trigger` is `scheduled`
- Manual invocation - when `cleanup.trigger` is `manual`

Agents should:
1. Check `project.json` for `authentication.cleanup` config
2. Only run cleanup when trigger mode matches context
3. Always use dry run first when debugging
4. Log cleanup results for audit purposes
