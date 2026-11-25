---
name: jobs-queues
description: >
  Async jobs and queue patterns with BullMQ + Upstash Redis.
  Invoke automatically when implementing tasks that must not block the HTTP response:
  PDF generation, email sending, report processing, exports, or any
  long-running operation triggered by an event.
---

# Jobs & Queues

## When to use queue vs cron vs direct call

| Situation | Mechanism |
|---|---|
| Periodic task (check overdue items at 00:00) | Cron (`notifications-cron`) |
| Event-triggered task, takes >500ms (generate PDF) | **Job queue** |
| Fast event-triggered task (<500ms) | Direct Event Bus |
| Task that can fail and needs retry | **Job queue** |

---

## Implementation with BullMQ + Upstash Redis

```typescript
// infrastructure/jobs/queues.ts
export const QUEUES = {
  REPORTS:       'reports',
  EMAILS:        'emails',
  NOTIFICATIONS: 'notifications',
} as const;

export const JOBS = {
  GENERATE_REPORT:  'generate-report',
  SEND_EMAIL:       'send-email',
  SEND_PUSH:        'send-push-batch',
} as const;
```

---

## IJobQueue interface (domain depends only on this)

```typescript
// domain/services/i-job-queue.ts
export const JOB_QUEUE = Symbol('JOB_QUEUE');

export interface IJobQueue {
  add<T>(queueName: string, jobName: string, data: T, options?: JobOptions): Promise<void>;
}

export interface JobOptions {
  delay?: number;       // ms before executing
  attempts?: number;    // attempts on failure (default: 3)
  backoff?: number;     // ms between attempts (exponential)
  priority?: number;    // 1 = highest
}
```

---

## Enqueuing a job in a Use Case

```typescript
// application/use-cases/report/request-report.use-case.ts
export class RequestReportUseCase {
  constructor(
    private readonly reportRepo: IReportRepository,
    private readonly jobQueue: IJobQueue,
  ) {}

  async execute(input: RequestReportInput): Promise<RequestReportOutput> {
    // 1. Create report record with PENDING status
    const report = Report.create({
      requestedBy: input.requestedBy,
      type: input.type,
      status: 'PENDING',
    });
    await this.reportRepo.save(report);

    // 2. Enqueue generation — does not block the response
    await this.jobQueue.add(
      QUEUES.REPORTS,
      JOBS.GENERATE_REPORT,
      { reportId: report.id },
      { attempts: 3, backoff: 5000 },
    );

    return { reportId: report.id, status: 'PENDING' };
  }
}
```

---

## Implementing a processor (worker)

```typescript
// infrastructure/jobs/processors/generate-report.processor.ts
@Processor(QUEUES.REPORTS)
export class GenerateReportProcessor {
  private readonly logger = new Logger(GenerateReportProcessor.name);

  constructor(
    private readonly reportRepo: IReportRepository,
    private readonly pdfService: IPdfService,
    private readonly storageService: IStorageService,
    private readonly eventBus: IEventBus,
  ) {}

  @Process(JOBS.GENERATE_REPORT)
  async handle(job: Job<{ reportId: string }>): Promise<void> {
    const { reportId } = job.data;
    this.logger.log(`Generating report reportId=${reportId} attempt=${job.attemptsMade}`);

    const report = await this.reportRepo.findById(reportId);
    if (!report) throw new Error(`Report ${reportId} not found`);

    try {
      await this.reportRepo.updateStatus(reportId, 'PROCESSING');

      const pdf = await this.pdfService.generate(report);
      const url = await this.storageService.upload(`reports/${reportId}.pdf`, pdf);

      await this.reportRepo.markCompleted(reportId, url);
      await this.eventBus.publish(new ReportGeneratedEvent(reportId, url));

    } catch (error) {
      await this.reportRepo.updateStatus(reportId, 'FAILED');
      this.logger.error(`Report generation failed reportId=${reportId}: ${(error as Error).message}`);
      throw error; // BullMQ retries automatically
    }
  }
}
```

---

## Retry configuration per queue

```typescript
export const QUEUE_CONFIGS = {
  [QUEUES.REPORTS]: {
    attempts: 3,
    backoff: { type: 'exponential', delay: 5000 },
    removeOnComplete: 100,  // keep last 100 completed jobs
    removeOnFail: 500,      // keep last 500 failed jobs for debugging
  },
  [QUEUES.EMAILS]: {
    attempts: 5,
    backoff: { type: 'exponential', delay: 2000 },
    removeOnComplete: 50,
    removeOnFail: 200,
  },
  [QUEUES.NOTIFICATIONS]: {
    attempts: 3,
    backoff: { type: 'fixed', delay: 3000 },
    removeOnComplete: 50,
    removeOnFail: 100,
  },
};
```

---

## Project job catalog

Define the job catalog in the project spec (e.g. `PROJECT.md`). Example structure:

| Job | Queue | Triggered by | Timeout | Attempts |
|---|---|---|---|---|
| `generate-report` | `reports` | `ReportRequestedEvent` | 60s | 3 |
| `send-email` | `emails` | `UserInvitedEvent`, `ReportGeneratedEvent` | 10s | 5 |
| `send-push-batch` | `notifications` | `AlertTriggeredEvent` | 15s | 3 |

---

## Job states

```
waiting → active → completed
                 ↘ failed → (retry) → waiting
                           → (no more attempts) → definitively failed
```

Always save the job state on the corresponding entity (`report.status`, etc.)
so the frontend can poll or receive a push when it completes.

---

## Environment variables

```bash
# Shared with cache — Upstash Redis
UPSTASH_REDIS_REST_URL=
UPSTASH_REDIS_REST_TOKEN=
```
