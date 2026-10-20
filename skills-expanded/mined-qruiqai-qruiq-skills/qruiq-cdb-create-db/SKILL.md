---
name: qruiq-cdb-create-db
description: |
  Create a new database (schema) and a dedicated least-privilege app account
  on an existing Tencent Cloud CDB MySQL instance via tccli, then return a
  ready-to-use connection string. Handles the tccli argparse bug around the
  `%` host wildcard, async request polling, and avoids leaking secrets.
  Use when asked to "create a database on CDB", "add a db to MySQL",
  "在 CDB 上加个 db", "新建一个数据库 + 账号", "create a schema and connection
  string", or any request to provision a new schema on an existing Tencent
  Cloud MySQL instance.
allowed-tools:
  - Bash
---

# qruiq-cdb-create-db

Provision a new database + dedicated app account on an **existing** Tencent Cloud CDB MySQL instance using `tccli`, and return a working connection string. This is the schema-on-existing-instance path, **not** the new-instance path (no `CreateDBInstanceHour`, no money spent).

## Prerequisites

- `tccli` installed and configured (`pipx install tccli` then `tccli configure`).
- Configured region matches the instance you want to target (check via the API, **not** `tccli configure list` — see Gotchas).

## When to use

User wants a fresh database (MySQL schema) carved out on a CDB instance they already own, plus app credentials. Typical cue: "在 cdb-xxx 上建个新库，给我连接串。"

If the user wants a **new CDB instance** (new VM-class resource), this is the wrong skill — use `CreateDBInstanceHour` directly and confirm cost with the user first.

## Step 1 — Find the target instance

```bash
tccli cdb DescribeDBInstances --Limit 100
```

Note the `InstanceId` (e.g. `cdb-1hpx6wwf`), `Region`, `Vip`, `Vport`, `WanStatus`, `UniqVpcId`. If the user owns multiple, ask which one. Don't guess.

Sanity-check what's already there (so you don't collide with existing names):

```bash
tccli cdb DescribeDatabases --InstanceId <ID>
tccli cdb DescribeAccounts  --InstanceId <ID>
```

## Step 2 — Decide naming + charset

- **DB name**: match the user's existing convention. Tencent CDB **does** allow `.` in db names (e.g. `xdone.app`, `subhound.com`) — don't reflexively rewrite `foo.com` to `foo_com` unless the user asks.
- **Charset**: prefer `utf8mb4` for any new database (full Unicode, emoji-safe). Don't blindly copy old `UTF8` databases — they're a legacy three-byte charset.
- **Account name**: use a project-scoped user, not `root`. Pattern: `<project>_app` (e.g. `invoory_app`).
- **Host**: `%` is fine when the network layer (VPC + security group) is the actual boundary. If the user wants tighter, ask.

## Step 3 — Create the database

```bash
tccli cdb CreateDatabase \
  --InstanceId <ID> \
  --DBName "<dbname>" \
  --CharacterSetName "utf8mb4"
```

Returns just a `RequestId`. Database creation on CDB is effectively synchronous — proceed.

## Step 4 — Generate password locally, then create the account

**Critical:** generate the password on the user's machine via `openssl`, never inline it into a prompt or have an LLM produce it. Keep it in a shell variable.

```bash
PASS=$(openssl rand -base64 24 | tr -d '/+=' | cut -c1-24)
```

**The argparse trap.** `tccli cdb CreateAccounts` and `tccli cdb ModifyAccountPrivileges` will both fail with the error `badly formed help string` if you pass arguments directly on the CLI when the value contains `%`. Root cause: Python `argparse` interprets `%` as a printf-style format token in help text, and tccli's auto-generated metadata hits this. Even `tccli cdb CreateAccounts help` (with no args) crashes for the same reason.

**Workaround:** use `--cli-input-json file://...` (must be `file://`, not inline JSON):

```bash
JSON_FILE=$(mktemp /tmp/tccli-create-acct-XXXXXX.json)
cat > "$JSON_FILE" <<EOF
{"InstanceId":"<ID>","Accounts":[{"User":"<project>_app","Host":"%"}],"Password":"$PASS","Description":"App user for <dbname>"}
EOF
RESP=$(tccli cdb CreateAccounts --cli-input-json "file://$JSON_FILE")
rm -f "$JSON_FILE"
echo "$RESP"
```

Capture the `AsyncRequestId` from `$RESP` for the next step.

## Step 5 — Wait for the account to land, then grant privileges

CDB account creation is **async**. If you call `ModifyAccountPrivileges` immediately you'll get `账号user:... host:%不存在`. Poll until done:

```bash
ASYNC_ID=$(echo "$RESP" | python3 -c 'import sys,json;print(json.load(sys.stdin)["AsyncRequestId"])')
until [ "$(tccli cdb DescribeAsyncRequestInfo --AsyncRequestId "$ASYNC_ID" 2>/dev/null \
            | python3 -c 'import sys,json;print(json.load(sys.stdin).get("Status",""))')" = "SUCCESS" ]; do
  sleep 2
done
```

Then grant least-privilege on the new database (same `file://` workaround):

```bash
JSON_FILE=$(mktemp /tmp/tccli-priv-XXXXXX.json)
cat > "$JSON_FILE" <<'EOF'
{"InstanceId":"<ID>","Accounts":[{"User":"<project>_app","Host":"%"}],"DatabasePrivileges":[{"Privileges":["SELECT","INSERT","UPDATE","DELETE","CREATE","DROP","REFERENCES","INDEX","ALTER","CREATE TEMPORARY TABLES","LOCK TABLES","EXECUTE","CREATE VIEW","SHOW VIEW","CREATE ROUTINE","ALTER ROUTINE","EVENT","TRIGGER"],"Database":"<dbname>"}]}
EOF
tccli cdb ModifyAccountPrivileges --cli-input-json "file://$JSON_FILE"
rm -f "$JSON_FILE"
```

These 18 privileges are **app-level ALL** without `GRANT` — the app can do anything inside its database but cannot escalate or hand out access. Don't grant `GRANT`. Don't grant any global privilege. If the user asks for "ALL", give these 18 unless they explicitly say otherwise.

Wait for this async request too (same poll pattern), then verify:

```bash
tccli cdb DescribeAccountPrivileges --InstanceId <ID> --User <project>_app --Host '%'
```

The output's `DatabasePrivileges[].Privileges` should match the 18.

## Step 6 — Output the connection string

Print:

```
Host:     <Vip>          # internal VPC IP unless WAN is open
Port:     <Vport>
Database: <dbname>
User:     <project>_app
Password: $PASS

URI: mysql://<project>_app:$PASS@<Vip>:<Vport>/<dbname>
```

## Step 7 — Network reality check (always include)

The `Vip` is a **VPC-internal address** unless `WanStatus` was non-zero in Step 1. End the response with the three external-access options:

1. **Open WAN**: `tccli cdb OpenWanService --InstanceId <ID>` — gives `WanDomain:WanPort`. **Pair with a security group restriction to specific source IPs**, otherwise the DB is exposed to the internet.
2. **Bastion**: a CVM in the same VPC as a jump host (SSH tunnel).
3. **Co-locate**: deploy the app inside the same VPC (CVM / TKE / SCF), use the internal IP — recommended for production.

Ask the user which they want. Do not unilaterally call `OpenWanService`.

## Step 8 — Security warnings (always include)

- The password generated above appeared in stdout / chat once. Treat it as **already exposed**. Recommend the user immediately log in and rotate via `ALTER USER '<project>_app'@'%' IDENTIFIED BY '<new>';` or via the console.
- If the user pasted SecretId/SecretKey into the chat at any point during setup (or if you ran `tccli configure list` — which dumps both to stdout), tell them to revoke the leaked key in [访问管理 → API 密钥管理](https://console.cloud.tencent.com/cam/capi) and rotate.

## Gotchas

- **`%` in shell args breaks tccli argparse** — see Step 4. Always use `--cli-input-json file://...` for any action whose JSON contains `%`. Even reading `help` for those actions fails.
- **`CreateAccounts` / `ModifyAccountPrivileges` are async** — chain via `DescribeAsyncRequestInfo` polling. Without it you'll race and see `账号...不存在`.
- **`tccli configure list` leaks credentials.** It dumps `secretId` and `secretKey` to stdout. Never use it inside an LLM-driven session — the keys end up in the model's context. Read `~/.tccli/credential` directly only if you must, and never echo the contents.
- **Tencent CLI flags are PascalCase** (`--Limit`, not `--limit`; `--InstanceId`, not `--instance-id`). Lowercase silently produces `Unknown options`.
- **Charset values are case-sensitive at create time** — use lowercase `utf8mb4` for new databases.
- **Don't touch `root`** — don't `ResetPassword` or `ResetRootAccount`. Those affect every other app on the instance.

## What NOT to do

- Don't pass `--Host '%'` on the CLI directly — use `cli-input-json file://`.
- Don't skip the async poll between `CreateAccounts` and `ModifyAccountPrivileges`.
- Don't enable WAN access without an explicit user OK and a security-group source-IP restriction.
- Don't echo `SecretId` / `SecretKey` in any command (`configure list`, `cat ~/.tccli/credential`, etc.) inside an agent session.
- Don't use `--CharacterSetName UTF8` for new databases — it's a legacy 3-byte charset that can't store many emoji or supplementary-plane CJK.
- Don't grant `GRANT` or any global privilege to the app account.
- Don't auto-pick an instance when the user has multiple — confirm.
