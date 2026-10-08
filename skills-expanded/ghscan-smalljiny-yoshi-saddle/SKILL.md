---
version: 1
name: flow-topic
description: Check the current topic and phase, or switch to another topic. Topic registration is handled by /flow-spec.
origin: harness
user-invocable: true
---

# /flow-topic

Check the current work topic and phase, or switch between topics.

Topic registration is no longer a separate step — use `/flow-spec <topic>` to start a new topic and write its spec.

## Usage

```
/flow-topic                   Check the current topic and phase
/flow-topic switch <name>     Switch to another active topic
/flow-topic <name>            ⚠ Deprecated — use /flow-spec <name> instead
```

## Execution Flow

### No arguments — Check current topic

1. Read `docs/_local/dev-context.json` — source of truth for active topics and their phase
2. Scan `docs/_local/backlog/` for backlog topics
3. Print status (active topics from `dev-context.json`, backlog topics from directory scan):

   ```
   현재 주제: <topic>
   단계: <phase>

   Active 토픽:
     * <current_topic> (현재) — <phase>
       <other_active_topic> — <phase>

   Backlog 토픽:
     - <backlog_topic_a>
     - <backlog_topic_b>
   ```

4. If no active topic exists:
   ```
   진행 중인 주제가 없습니다.
   새 주제를 시작하려면: /flow-spec <topic>
   백로그에서 구현을 시작하려면: /flow-plan <topic>
   ```

5. If no backlog topics exist, omit the "Backlog 토픽" section.

### `/flow-topic switch <name>` — Switch topic

1. Check if `<name>` exists in `dev-context.json` topics (active topics only)
   - If found: update `current_topic` to `<name>` and save
   - If not found in active topics: check if `<name>` exists in `docs/_local/backlog/`
     - If in backlog: stop with guidance:
       ```
       '<name>'은 backlog 토픽입니다.
       플래닝을 시작하려면: /flow-plan <name>
       ```
     - If not found anywhere: stop with guidance:
       ```
       '<name>' 토픽을 찾을 수 없습니다.
       스펙을 작성하려면: /flow-spec <name>
       ```

2. Confirm switch:
   ```
   현재 주제가 '<name>'으로 전환되었습니다.
   단계: <phase>
   ```

### `/flow-topic <name>` — Deprecated

Show a redirect message and stop:

```
⚠ /flow-topic <name>으로 주제를 등록하는 방식은 더 이상 사용하지 않습니다.
스펙 작성과 주제 등록을 함께 시작하려면:
  /flow-spec <name>
```

## Next Steps

- Start a new topic: `/flow-spec <topic>`
- Plan a backlog topic: `/flow-plan <topic>`
- Continue implementation: `/flow-impl`
