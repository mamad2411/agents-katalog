---
name: airflow-dag-security
description: >
  Secure Apache Airflow DAGs and deployment: connections/variables secrecy, DAG code
  injection risks, RBAC, example-DAG disable, executor isolation, and callback hardening.
  Use when reviewing Airflow 2.x ops or authoring production DAGs on owned platforms —
  not for attacking third-party Airflow instances.
---

# Airflow DAG Security

## Scope And Authorization

- **In scope:** Airflow deployments and DAGs your organization owns or is authorized to assess.
- **Out of scope:** Unauthorized access to others’ Airflow UIs or metadata DBs.
- Prefer staging for config changes (`airflow.cfg`, secrets backends).
- Never print connection passwords in logs, tickets, or `airflow connections get` output shared widely.
- Pair DAG Python with `code-quality-standards` and `python-style-and-typing`.

## When To Use

- Production DAG review (secrets, `BashOperator` injection, pickle).
- Hardening webserver RBAC/SSO, disabling example DAGs.
- Moving connections/variables to a secrets backend.
- Executor isolation (KubernetesExecutor pods, least privilege).
- Incident after credential leak via task logs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Dataset-aware scheduling patterns | `airflow-dataset-scheduling` |
| Generic secrets program | `secrets-management-hygiene` |
| Airbyte connector trust | `airbyte-connector-security` |
| K8s pod hardening broadly | kubernetes security skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Secrets | Connections/Variables via backend (Vault/SM); not raw in DAG files |
| DAG code | No `pickle`; no untrusted `Jinja` user input into bash; pin images |
| Auth | RBAC on; example DAGs off; SSO; no default admin |
| Executors | Isolate tasks; don’t run webserver as task user with broad cloud admin |
| Logs | Redact; limit who can read task logs with secrets |
| Callbacks | Failure callbacks must not embed secrets in HTTP posts |

## Workflow

### 1. Confirm scope and success criteria

1. Record Airflow version, executor, deployment (MWAA/Composer/self-host), DAG repo.
2. Success: no secrets in git DAGs; RBAC roles least privilege; example DAGs disabled; `donot_pickle`/safe XCom; operators use templating safely.
3. List high-value connections (warehouses, prod APIs).

### 2. Inventory configuration and auth

```bash
airflow version
airflow config get-value core executor
airflow config get-value webserver expose_config
airflow users list
airflow dags list
# Ensure example DAGs off in config: load_examples = False
```

1. Confirm auth manager / RBAC roles (Admin, Op, User, Viewer).
2. Check public webserver exposure and TLS termination.

### 3. Secrets backend and connections

```ini
# airflow.cfg pattern (illustrative)
[secrets]
backend = airflow.providers.hashicorp.secrets.vault.VaultBackend
backend_kwargs = {"connections_path": "airflow/connections", "url": "https://vault"}
```

```bash
# Prefer not to echo passwords
airflow connections list
# Test DAG parses without plaintext secrets in repo
rg -n "password\s*=|aws_secret|BEGIN RSA|api_key" dags/
```

1. Migrate Variables containing secrets out of metadata UI plain storage when possible.
2. Rotate any secret found in git history.

### 4. DAG code review checklist

| Pattern | Risk | Prefer |
| --- | --- | --- |
| `BashOperator(bash_command=f"... {user} ...")` | Injection | Typed params + strict allowlists |
| `PythonOperator` with `pickle` | RCE | `airflow.providers` serializers / raw python callable in code |
| Secrets in default args | Leak in UI/logs | Secrets backend macros |
| Unpinned `docker` images | Supply chain | Digest pins |
| Broad `GcpHook` / AWS conn | Overprivilege | Scoped IAM roles per DAG owner |

```python
# Bad
BashOperator(task_id="t", bash_command=f"process.sh {dag_run.conf['name']}")
# Better: validate conf against enum/regex before use; or map to fixed argv list
```

### 5. Executor and network isolation

1. KubernetesExecutor: task ServiceAccount least privilege; NetworkPolicy default deny egress except needs.
2. Celery workers: no shared filesystem secrets world-readable.
3. Prevent DAGs from reaching cloud metadata if not required.

### 6. Verify

```bash
airflow dags list-import-errors
airflow tasks test my_dag my_task 2020-01-01
# Static secrets scan on dags/
gitleaks detect -s dags/ -v || true
```

1. Login as Viewer: cannot edit connections or clear DAGs inappropriately.
2. Confirm `expose_config` is not leaking secrets to UI.
3. Trigger a deliberate failure: callback does not post secrets.

### 7. Hand off

1. DAG authoring standard in repo README.
2. CODEOWNERS for production DAGs.
3. Alert on new Admin users and connection mutations.
4. Runbook for secret rotation and compromised DAG PR.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Secrets | Vault backend | `password = "..."` in DAG |
| RBAC | SSO + least roles | Single shared admin |
| Examples | `load_examples=False` | Example DAGs in prod |
| Bash | Fixed scripts + validated args | Untrusted conf → shell |
| Logs | Restricted + redaction | World-readable task logs with tokens |

## Output Checklist

- [ ] Version/executor/deployment recorded
- [ ] Example DAGs disabled; RBAC/SSO reviewed
- [ ] Secrets backend / connection storage reviewed
- [ ] DAG repo scanned for secrets and unsafe operators
- [ ] Executor isolation / IAM scoped
- [ ] Import errors clean; sample task test OK
- [ ] Log access and callbacks reviewed
- [ ] Monitoring on admin/connection changes
- [ ] `code-quality-standards` on DAG code

## Rules

- Owned Airflow only.
- DAGs are code execution — treat PRs as privileged.
- Never commit connections passwords or service account JSON.
- Fail closed on secret access errors when possible.
- Route pure scheduling-design (datasets) to `airflow-dataset-scheduling`.
