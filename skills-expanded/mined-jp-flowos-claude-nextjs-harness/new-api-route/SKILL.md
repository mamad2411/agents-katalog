---
name: new-api-route
description: Next.js App Router API 라우트 스캐폴딩. 인증 + Zod + 세션 격리 + DB 접근 패턴 주입. 새 /api/... route.ts 작성 시 사용.
---

# API Route 스캐폴드 (Next.js App Router)

새 API 라우트는 아래 형태를 따른다. 훅이 인증 누락을 차단하지만, 올바른 패턴을 처음부터 주입하는 게 낫다.

## Minimum Viable Route

```ts
// src/app/api/<feature>/route.ts
import { NextResponse } from "next/server";
import { z } from "zod";
import { requireAuth } from "@/lib/auth/guards";     // 프로젝트별 경로
import { getDb } from "@/lib/db";                    // 프로젝트별 경로
import { logger } from "@/lib/logger";

// 세션 식별자(userId, tenantId 등)는 body에 넣지 말 것 — 세션에서 추출
const bodySchema = z.object({
  // ...
});

export async function POST(req: Request) {
  const auth = await requireAuth(req);
  const { userId, tenantId } = auth;

  let body: z.infer<typeof bodySchema>;
  try {
    body = bodySchema.parse(await req.json());
  } catch (err) {
    return NextResponse.json(
      { error: "invalid body", details: err instanceof z.ZodError ? err.flatten() : String(err) },
      { status: 400 },
    );
  }

  const db = getDb();
  try {
    // 모든 쿼리는 tenantId/userId 필터링
    return NextResponse.json({ ok: true });
  } catch (err) {
    logger.error("[api/<feature>] failed", { err, tenantId });
    return NextResponse.json({ error: "internal" }, { status: 500 });
  }
}
```

## 변형

### 역할 기반

```ts
import { requireRole } from "@/lib/auth/guards";

export async function POST(req: Request) {
  const auth = await requireRole(req, ["admin", "owner"]);
  // ...
}
```

### 공개 엔드포인트

인증 대신 Rate limit:

```ts
import { checkRateLimit } from "@/lib/ratelimit";

export async function POST(req: Request) {
  const rl = await checkRateLimit(req, { prefix: "public-feature", limit: 20, window: "1m" });
  if (!rl.ok) {
    return NextResponse.json({ error: "rate limited" }, { status: 429 });
  }
  // ...
}
```

### Dynamic params (App Router)

```ts
export async function GET(
  req: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  const auth = await requireAuth(req);
  const { id } = await params;
  // ...
}
```

## 체크리스트

- [ ] `requireAuth` / `requireRole` / `checkRateLimit` 중 하나 첫 줄에 있음
- [ ] 세션 식별자(userId/tenantId)는 `auth.*`에서만 (body에서 안 받음)
- [ ] Zod 스키마로 입력 검증
- [ ] DB helper 사용 (raw 연결 생성 금지)
- [ ] 에러 시 `logger.error` + 5xx (console.log 금지)
- [ ] 성공/실패 모두 `NextResponse.json` 반환

## 테스트 (Vitest)

```ts
// src/app/api/<feature>/__tests__/route.test.ts
import { describe, it, expect, vi } from "vitest";
import { POST } from "../route";

vi.mock("@/lib/auth/guards", () => ({
  requireAuth: vi.fn(async () => ({ userId: "u1", tenantId: "t1" })),
}));

describe("POST /api/<feature>", () => {
  it("rejects invalid body", async () => {
    const res = await POST(new Request("http://x", { method: "POST", body: "{}" }));
    expect(res.status).toBe(400);
  });
});
```

## 프로젝트별 교체 포인트

이 스킬은 제네릭하다. 각 프로젝트에서 아래 식별자를 프로젝트 관례에 맞춰 교체:
- `requireAuth` 함수명 (e.g. `requireSession`, `requireAuthOrDemo`)
- `getDb` 함수명 (e.g. `getDbAdmin`, `prisma`)
- 세션 프로퍼티 (e.g. `auth.staff.clinicId`, `auth.user.id`, `session.tenantId`)
- 경로 alias (`@/lib/...`)
