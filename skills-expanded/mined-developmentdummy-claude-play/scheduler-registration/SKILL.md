---
name: scheduler-registration
description: Use when the user asks to design or implement a scheduler, queue worker, automation runner, polling loop, batch processor, cron-like flow, job orchestrator, or start/stop/restart/inspect controls for long-running work in ClaudePlay. Covers session-bound server-side async loop design, lifecycle rules, scheduler registration, metadata, inspect/start/stop/restart APIs, and MCP observability. Do not use for simple one-shot panel actions or a single direct tool call.
---

# Scheduler Registration

Use this skill when a builder or service task introduces:

- scheduler
- scheduler registration
- automation runner
- automation pipeline
- batch loop
- batch processor
- background-like polling
- polling loop
- queue worker
- job runner
- job orchestrator
- cron-like flow
- start/stop/restart controls
- service status inspection

Do not use this for simple panel buttons that only trigger one-shot actions.

Typical trigger requests:

- "스케줄러 설계해줘"
- "자동 실행 루프를 붙여줘"
- "배치 러너를 서비스 엔진으로 옮기자"
- "start/stop/restart API를 만들자"
- "inspect/status MCP 도구를 붙이자"
- "백그라운드처럼 도는 작업을 등록하자"

## Default Mental Model

ClaudePlay schedulers should default to:

- service-side
- session-bound
- async loop based
- tick driven
- observable through API/MCP

Unless the service explicitly needs durable background execution, do not propose a separate worker process or "background thread".

Prefer this wording:

- "server-side async loop"
- "session-bound scheduler handle"
- "tick-based runner"

Avoid this wording unless it is literally true:

- "background thread"
- "independent daemon"
- "always-on worker"

## Registration Rules

When registering a scheduler, define all of these clearly:

1. Ownership
   - Which service module owns the handle?
   - Where is runtime state stored?

2. Lifecycle
   - How it starts
   - How it stops
   - What happens on completion
   - What happens on error
   - What happens when connected clients become zero

3. Tick contract
   - What one tick does
   - How the next action is chosen
   - Sleep policy after work / idle
   - Stop flag check points

4. Observability
   - inspect API/MCP route
   - client/session counts
   - scheduler metadata
   - last error and last tick time

5. Controls
   - inspect
   - start
   - stop
   - restart

## Recommended Metadata

Always include observable scheduler metadata where useful:

- `label`
- `source`
- `requestedBy`
- `note`
- `phase`
- `startedAt`
- `lastTickAt`
- `lastError`

If multiple schedulers may exist later, metadata is not optional in practice.

## Safe Default Policy

For ClaudePlay, the default-safe scheduler policy is:

- session-bound
- stop when no clients remain in the session
- stop on explicit user request
- stop on completion
- stop on fatal error

Only propose durable execution beyond session lifetime when the user explicitly wants a real job runner.

## Recommended Architecture

Prefer this shape:

1. panel/button or MCP tool calls service API
2. service API validates session activity
3. runtime registry creates or reuses a scheduler handle
4. handle runs an async loop
5. each tick calls domain logic or session tool
6. scheduler state is exposed through inspect/status APIs

## Anti-Patterns

Avoid these unless there is a strong reason:

- browser-local timer loops as the primary scheduler
- panel HTML owning long-running orchestration
- hidden loops without inspectable status
- start/stop without runtime metadata
- session client count and scheduler state diverging silently

## Output Expectations

When asked to design or implement scheduler registration, produce:

- runtime ownership point
- lifecycle rules
- start/stop/restart/inspect surface
- metadata schema
- stop/completion policy
- brief note on why this is session-bound or durable

If code changes are requested, keep the design consistent across:

- service runtime
- API routes
- MCP tools
- panel controls
- status/inspection views

## Scheduler Notifications

스케줄러의 `scheduler_tick` 반환값에 `notifications` 배열을 포함하면, 서버가 클라이언트(UI)와 AI 세션에 메시지를 자동으로 전달한다.

### Notification Schema

```javascript
// scheduler_tick 반환값 예시
return {
  success: true,
  phase: "source",
  did_work: true,
  notifications: [
    // 클라이언트(UI)에 알림 — wsBroadcast로 전달
    {
      target: "client",
      event: "scheduler:progress",     // WebSocket 이벤트 타입 (기본: "scheduler:notify")
      payload: { step: 3, total: 10 }  // 자유 형태
    },
    // AI에 이벤트 큐 — 다음 유저 메시지에 같이 전달
    {
      target: "ai",
      mode: "queue",                   // "queue" (기본) 또는 "send"
      message: "[SCHEDULER] 3/10 완료"
    },
    // AI에 직접 턴 트리거 — 응답 중이면 완료 대기 후 전송
    {
      target: "ai",
      mode: "send",
      message: "[SCHEDULER_COMPLETE] 작업이 완료되었습니다. 결과를 확인하고 유저에게 알려주세요."
    }
  ]
};
```

### target별 동작

| target | mode | 동작 |
|--------|------|------|
| `client` | — | `wsBroadcast(event, payload, { sessionId })` 호출. 해당 세션의 모든 클라이언트에 WebSocket 이벤트 전달 |
| `ai` | `queue` (기본) | `instance.queueEvent(message)` 호출. 이벤트 큐에 쌓이고, 다음 유저 메시지 전송 시 AI에 함께 전달 |
| `ai` | `send` | `instance.sendMessage(message)` 호출. AI에 직접 새 턴을 트리거. AI가 응답 중이면 완료 대기 후 전송 |

### 사용 가이드

- **진행 상황 알림**: `target: "client"` — 프론트엔드에서 토스트, 프로그레스 바, 패널 업데이트에 활용
- **AI에 중간 보고**: `target: "ai", mode: "queue"` — 급하지 않은 정보. 다음 대화 턴에 자연스럽게 포함
- **AI에 즉시 알림**: `target: "ai", mode: "send"` — 완료/에러 등 AI가 즉시 반응해야 하는 이벤트. 대화가 끊긴 상태에서도 AI 턴을 시작함
- 매 틱마다 0~N개 알림 가능. 완료 틱(`completed: true`)에도 알림이 처리된 후 루프가 종료됨
- notification 처리 중 에러는 로그만 남기고 스케줄러 루프는 중단하지 않음
