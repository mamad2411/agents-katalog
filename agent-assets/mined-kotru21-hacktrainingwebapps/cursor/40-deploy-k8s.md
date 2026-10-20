---
description: Деплой k3s + ingress-nginx, namespace на команду, NetworkPolicy-изоляция, self-healing.
globs: ["deploy/**", "scripts/**"]
alwaysApply: false
---

# Деплой и инфраструктура (k3s, одна VM)

Спека — `docs/SPEC.md` §3, §8. Оркестрация raundов — `docs/instructor-guide.md`.

## Инфра
- **k3s** запускать с `--disable traefik`; ingress-контроллер — **ingress-nginx** (`ingressClassName: nginx`).
  Не использовать Traefik.
- **StorageClass:** `local-path` (встроен в k3s) для per-team PVC `workspace` и postgres.
- Манифесты — **kustomize**: `base/`, `team-template/` (app+postgres+code-server+PVC+Service+NetworkPolicy+
  ConfigMap/Secret), `overlays/team-a|team-b`, `platform/` (scoreboard+checker+planter+Loki+Alloy+Grafana+
  internal-metadata). Никаких хардкоженных имён namespace в шаблоне — только через overlay.

## Изоляция (NetworkPolicy — критично для безопасности полигона)
- default-deny ingress/egress в namespace команды.
- Разрешён вход от `platform` (checker/planter/scoreboard).
- Вход от АТАКУЮЩЕЙ команды — ТОЛЬКО на HTTP-порт `app`. Никогда на postgres / code-server / платформу.
- Egress стендов наружу запрещён (кроме внутрикластерной SSRF-мишени `internal-metadata`).
- `swap-roles.sh` инвертирует направление политики между раундами.

## Self-healing и сброс
- Каждый под app: `livenessProbe /healthz`, `readinessProbe /readyz`, `resources.limits`, `restartPolicy: Always`.
- В `reference`-оверлеях: `runAsNonRoot`, `readOnlyRootFilesystem`, `drop: [ALL]`, пиннинг образа по digest.
- `reset-round.sh` восстанавливает уязвимый baseline из init-снапшота на `workspace` PVC + пересев БД + planter,
  целевое время < 60 c. Скрипты идемпотентны.

## RBAC команд
kubeconfig команды ограничен своим namespace (edit ConfigMap/Secret/Deployment, exec, apply). Нет доступа
в чужой namespace и в `platform`. code-server запускается под этим же ограниченным ServiceAccount.
