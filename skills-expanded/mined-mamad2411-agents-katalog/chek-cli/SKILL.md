---
name: "chek-cli"
description: "Operate CHEK app capabilities through an agent-first CLI: AI product publication, review rooms, config, auth, schema, raw backend API calls, and stable shortcut workflows."
---

# CHEK CLI

Use this skill when an agent needs to operate CHEK app functionality through a
CLI protocol instead of browser clicks. The primary interface is backend API
access; frontend build/browser commands are auxiliary diagnostics.

## Install

```bash
python -m pip install -e ".[dev]"
```

## Core Rules

- Prefer machine-readable JSON output. It is the default; `--json` is an alias.
- Start with `chek config show` and `chek auth status` to understand the session.
- Use Lark-style identity switching: `chek --as user ...`, `chek --as service ...`, or `chek config default-as user`.
- Use `chek registry status` to verify OpenAPI coverage.
- Use `chek manifest` when an agent needs machine-readable capability discovery.
- Use `chek ai-product +research-plan` before publishing AI product review rooms.
- Use `chek ai-product +publish --dry-run` to inspect duplicate-check and publish requests before mutation.
- Use `chek ai-product +review --dry-run` before submitting ratings and evidence.
- Use `chek schema <service.resource.method>` before constructing non-trivial request bodies.
- Prefer generated command trees such as `chek vehicle vehicles batch-search`.
- Use `chek call <service.resource.method> --dry-run` when the method exists in the registry.
- Use `chek api METHOD PATH --dry-run` before calling unfamiliar backend paths.
- Prefer `+shortcut` commands for common app jobs because their flags are stable.
- Use `chek examples show <name-or-schema>` when you need canonical command shapes.
- Use frontend commands only when visual or build evidence is specifically needed.

## API-First Commands

```bash
chek config show
chek config set-env dev
chek config default-as user
chek auth status
chek auth login --method token --token "$CHEK_ACCESS_TOKEN" --profile dev-agent
chek registry status
chek manifest --include-operations --operation-limit 20
chek ai-product +research-plan --category 生产力工具 --product-name Kimi --software-version "2026 年 7 月网页版"
chek ai-product +duplicate-check --category 具身机器人 --product-name "Unitree G1" --hardware-model EDU --software-version v1.2.4 --dry-run
chek ai-product +publish --category 生产力工具 --product-name Kimi --software-version "2026 年 7 月网页版" --reason "值得复评长文本能力" --source-url "https://example.com/source" --dry-run
chek ai-product +review --post-id "<room_uuid>" --stars 4.5 --comment "版本确认后体验稳定" --evidence-url "https://example.com/evidence" --dry-run
chek schema
chek schema vehicle.vehicles.batchSearch
chek vehicle +buying-plan --query "小米 SU7" --scene urban --city 上海 --dry-run
chek vehicle +compare --id veh_1 --id veh_2 --include-raw --dry-run
chek vehicle +rankings --scene urban --window latest --dry-run
chek humanoid +search --query "Unitree" --page-size 10 --dry-run
chek humanoid +compare --id robot_1 --id robot_2 --dry-run
chek vehicle vehicles batch-search --data '{"queries":[{"query":"小米 SU7"}]}' --dry-run
chek backend-saas app-vehicle-metrics rank-top3 --param scene=urban --dry-run
chek call vehicle.vehicles.detail --path id=veh_123 --dry-run
chek api GET /api/backend-app/login/checkToken --dry-run
chek vehicle +search --query "小米 SU7" --dry-run
chek discovery +feed --page-size 10 --dry-run
chek share +resolve --share-id "$SHARE_ID" --share-token "$SHARE_TOKEN"
```

## Auth

```bash
chek auth set-token --token "$CHEK_ACCESS_TOKEN"
chek auth login --method token --token "$CHEK_ACCESS_TOKEN" --profile dev-agent
chek auth credential set --profile dev-agent --identity service --token "$CHEK_SERVICE_TOKEN"
chek --as service auth status
chek auth check --scope vehicle:read --verify
chek auth status --check
chek auth sms-send --phone "13800000000"
chek auth sms-login --phone "13800000000" --code "123456"
chek auth login-password --phone "13800000000" --password "$CHEK_PASSWORD"
chek auth profile list
chek auth profile save dev-agent --activate
chek auth profile use dev-agent
chek auth logout
```

If a command returns an auth error, refresh credentials first rather than
retrying blindly.

## Raw API Pattern

Use `call` for registry methods:

```bash
chek schema crowd.me.tasks
chek crowd me tasks --param status=OPEN --dry-run
chek call crowd.me.tasks --param status=OPEN --dry-run
```

Use `api` for paths that are not yet in the registry:

```bash
chek api GET /api/backend-app/login/checkToken
chek api POST /api/vms/api/vehicles:batchSearch \
  --data '{"queries":[{"query":"小米 SU7","topK":10}],"options":{"includeDetails":true}}'
```

## Examples And Smoke

```bash
chek examples list
chek examples show vehicle.buying-plan
chek examples generate --service vehicle --resource vehicles --limit 5
chek smoke api --dry-run
chek smoke auth --dry-run
chek smoke api --include-authenticated --include-auth-check
```

## Optional Frontend Diagnostics

```bash
chek doctor
chek routes list
chek routes find vehicles
chek serve h5 --port 10086 --wait-seconds 60
chek flow smoke --url http://localhost:10086 --retries 10 --interval 2
chek page snapshot pages/vehicles/index/index --base-url http://localhost:10086
```
