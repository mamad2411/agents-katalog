---
tags: [devops, slack, webhook, notify]
name: slack-webhook-notify
description: Slack Incoming Webhook으로 메시지를 전송한다. 빌드/테스트/배포 결과, 작업 완료 알림 등을 Slack 채널에 보낼 때 사용.
category: devops
version: 1.0.0
triggers:
  - slack
  - 슬랙
  - slack notify
  - webhook 알림
  - 빌드 알림
  - 작업 완료 알림
---

# Slack Webhook Notify

## Purpose

Slack Incoming Webhook 을 통해 채널에 메시지를 전송한다. 별도 봇 토큰 없이 URL 하나로 동작하므로 CI/로컬 자동화에 가볍게 붙이기 좋다.

## When to Activate

- "slack 보내", "슬랙으로 알려줘", "slack 메시지" 등 요청
- 빌드/테스트/배포 결과 알림
- 장기 실행 작업 완료 후 사용자 알림

## Prerequisites

1. Slack Workspace 에서 Incoming Webhook 앱을 추가하고 채널별 URL 발급
2. URL 은 **환경변수** 로 주입 (예: `SLACK_WEBHOOK_URL`) — 소스코드/스킬 문서에 하드코딩 금지
3. Windows 환경은 `curl` 한글 깨짐 이슈가 있으므로 Python `urllib` 사용 권장

## How to Send

### 권장: 환경변수 + Python

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXX/YYY/ZZZ"

python -c "
import json, os, urllib.request
url = os.environ['SLACK_WEBHOOK_URL']
data = json.dumps({'text': 'MESSAGE_HERE'}).encode('utf-8')
req = urllib.request.Request(
    url, data=data,
    headers={'Content-Type': 'application/json; charset=utf-8'}
)
with urllib.request.urlopen(req) as res:
    assert res.status == 200, f'slack webhook failed: {res.status}'
print('Sent!')
"
```

### 프로젝트 스크립트가 있는 경우

```bash
python scripts/slack.py "보낼 메시지"
```

## Message Payload Shapes

| 용도 | payload |
|---|---|
| 단순 텍스트 | `{"text": "..."}` |
| 채널 오버라이드 | `{"text": "...", "channel": "#ops-alerts"}` |
| 멘션 | `{"text": "<@U012ABCDE> 배포 실패"}` |
| Block Kit | `{"blocks": [...]}` (리치 레이아웃 필요 시) |

## Notes

- Windows 에서 curl 로 한글을 보낼 때 깨짐 → Python urllib + UTF-8 인코딩
- HTTP 200 응답 = 성공, 그 외 코드는 payload/URL 점검
- Webhook URL 유출 시 즉시 Slack 앱 관리자에서 회전 (rotate)
- CI 에서는 Secret 으로 주입, 로컬 에서는 `.env` 로 관리 (커밋 금지)

## Pitfalls

- SKILL.md/스크립트에 실제 webhook URL 하드코딩 → 레포 유출 시 외부인이 임의 채널 포스팅 가능
- `curl -d` 로 한글 직접 전송 시 인코딩 깨짐
- rate limit (초당 1건 권장) 미준수 시 429
