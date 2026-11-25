---
name: cron-job
description: Creates a cron job with error handling, logging, locking, and monitoring
argument-hint: <job-description> [schedule]
user-invocable: true
allowed-tools: Read Glob Edit
effort: low
---

## Create Cron Job

Job: **$1**
Schedule: **$2** (cron expression, e.g., `0 * * * *` = every hour)

1. Detect scheduler:
```bash
cat package.json | grep -E '"node-cron"|"cron"|"@nestjs/schedule"|"bullmq"|"pg-boss"'
```

2. Generate the job:
```ts
import cron from 'node-cron'
import { logger } from '@/lib/logger'

const JOB_NAME = '$1'

cron.schedule('$2', async () => {
  const startTime = Date.now()
  logger.info({ job: JOB_NAME }, 'Starting')

  // Distributed lock (prevent concurrent runs)
  const lock = await acquireLock(JOB_NAME, ttlSeconds: 300)
  if (!lock) {
    logger.warn({ job: JOB_NAME }, 'Already running, skipping')
    return
  }

  try {
    await runJob()
    logger.info({ job: JOB_NAME, duration: Date.now() - startTime }, 'Completed')
  } catch (error) {
    logger.error({ job: JOB_NAME, error }, 'Failed')
    // Alert if needed
  } finally {
    await releaseLock(JOB_NAME)
  }
})
```

3. Include:
   - Distributed locking (Redis or DB-based) to prevent concurrent execution
   - Structured logging with duration
   - Alert on failure (if project has alerting)
   - Graceful shutdown handling
   - Manual trigger endpoint for testing

4. Add to job registry so all jobs are visible in one place.
