---
description: Run Health Monitoring and Uptime Verification
globs: ["src/app/api/health/**/*.ts", "src/pages/api/health/**/*.ts"]
---
# Observability: Health Monitoring

<audit_rules>
- You MUST verify the existence of a `/api/health` or `/healthz` endpoint that returns a 200 OK status.
- The health check MUST verify database connectivity and critical external dependencies (e.g., Redis), not just application uptime.
- The endpoint MUST return structured JSON with `status`, `timestamp`, and `version` fields.
- You MUST verify that the health check responds in under 100ms to prevent timeout issues in synthetic monitoring.
- NEVER expose sensitive data (e.g., internal IP addresses or secret keys) in the health check response.
</audit_rules>

<example_good>
```typescript
// /api/health/route.ts
export async function GET() {
  try {
    await prisma.$queryRaw`SELECT 1`; // Verify DB connection
    return NextResponse.json({ status: 'ok', timestamp: new Date().toISOString(), version: '1.0.0' }, { status: 200 });
  } catch (error) {
    return NextResponse.json({ status: 'error', message: 'Database connection failed' }, { status: 503 });
  }
}
```
</example_good>

<example_bad>
```typescript
// /api/health/route.ts
export async function GET() {
  return new Response("OK"); // Missing structured JSON and DB check
}
```
</example_bad>

