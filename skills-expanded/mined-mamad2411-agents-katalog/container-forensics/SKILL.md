---
name: container-forensics
description: 侵害された Docker container の image / layer / volume / runtime と Kubernetes API server の audit log を解析し、container 内 attacker 行動 / cluster RBAC 改竄 / 永続化 / 流出経路を再構成する。CTF DFIR や container 環境侵害で発火。docker / k8s-audit の深掘りは references/ 参照
category: forensics
tags:
  - docker
  - kubernetes
  - container
  - audit
  - forensics
  - runtime
---

# Container Forensics

## When to Use

- 侵害された Docker container の image / runtime artefact 解析
- Kubernetes cluster の API audit log で RBAC 変更 / privileged pod / secret 取得 / exec into pod を追跡
- container escape / image supply-chain 侵害の調査
- CTF DFIR で `docker save` 出力や k8s `audit.log` が evidence

**使わない場面**: container runtime syscall (Falco) — `cloud-forensics/references/k8s-runtime-falco.md`、cloud control plane log (CloudTrail / Activity Log) — `cloud-forensics/references/aws-cloudtrail.md`。

variant の深掘りは references/ を参照: Docker image / layer / runtime artefact = `references/docker.md`、Kubernetes API audit log の jq 抽出 + 異常検出 = `references/k8s-audit.md`。

## Approach / Workflow

### Phase 1 — evidence の特定

```
- container image 単独 → references/docker.md (docker save / layer 解析)
- live container → references/docker.md (docker exec / inspect / logs)
- cluster API audit log → references/k8s-audit.md (jq filter / RBAC review)
- kubelet log / containerd log → host-level (別 skill)
```

## Phase 2 — image / layer 解析の主軸

`docker save` した tar から layer を展開し、不審 binary / 永続化 / log を抽出。詳細手順は `references/docker.md`。

## Phase 3 — runtime 状態 (live)

`docker exec` / `docker inspect` で動作中 container の process / network / mount / capability を観察。escape 兆候 (privileged / docker.sock mount / CAP_SYS_ADMIN) を確認。詳細は `references/docker.md`。

## Phase 4 — Kubernetes audit log

audit policy が `RequestResponse` 出力で:

- exec-into-pod / port-forward
- secret 大量取得
- RBAC 改竄 (cluster-admin binding 追加)
- privileged pod 起動 / hostPath mount
- anonymous API access

詳細な jq filter は `references/k8s-audit.md`。

## Phase 5 — 攻撃 chain 再構成

container artefact + cluster audit log を相関:

```
1. compromised SA token → API access (audit log)
2. exec into kube-system pod (audit log)
3. shell spawned in container (image diff / docker logs)
4. install dropper / read /etc/shadow (layer diff)
5. RBAC 変更 → cluster-admin binding (audit log)
6. egress to C2 (network log)
```

## Phase 6 — レポート

```
- image identity / digest / 不審 layer
- audit log 期間 / event 件数 / 危険 verb 別件数
- 関与した user / SA / source IP
- RBAC / privileged 設定の改竄有無
- IOC (file / IP / cmdline / pod name)
- 推奨 (image rebuild / RBAC 縮小 / audit policy 強化 / runtime detection rule)
```

## Tools

```
docker (CLI / inspect / history / save)
kubectl / kubectl-who-can / rakkess
trivy / grype / syft (image scan)
dive (interactive layer browse)
jq (audit log filter)
splunk / OpenSearch / ELK
WebFetch
Bash (sandbox)
```

## Related Skills

- `cloud-forensics` (cross-cloud forensic 横断)
- `cloud-pentester` (offensive 視点)
- `kubernetes-security` (offensive K8s pentest 後の defender)
- `ioc-hunting`
- `dfir`, `blue-teamer`

## Rules

1. **integrity** — image digest / save tar / audit log の SHA-256 を保持
2. **read-only** — image / log を解析時に変更しない
3. **escape risk** — privileged container 解析は sandbox / dedicated host
4. **PII redaction** — image 内 credentials / log 内 token を共有時に mask
