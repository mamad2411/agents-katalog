---
name: gitops-deploy-workflow
description: Sets up GitOps delivery with ArgoCD or Flux CD — declarative app definitions, app-of-apps/Kustomize overlays, sync policies, progressive delivery (canary/blue-green), and drift reconciliation. Triggers when configuring ArgoCD/Flux, structuring a GitOps repo, or debugging out-of-sync/drift.
when_to_use: ตั้ง/แก้ ArgoCD หรือ Flux, จัดโครง GitOps repo, app out-of-sync/drift, ทำ progressive delivery
---

## When to Use

- ตั้งหรือแก้ ArgoCD / Flux CD ครั้งแรก หรือ refactor โครง GitOps repo
- App ค้าง `OutOfSync` / `Degraded` หรือ manifest จริงใน cluster ถูกแก้มือ (drift)
- เพิ่ม env ใหม่ (dev/staging/prod) หรือ wire promotion path
- ทำ progressive delivery (canary / blue-green) แทน rolling update ตรงๆ

**SKIP** ถ้าเป็น push-based CI deploy (`kubectl apply` ใน pipeline) — นั่นไม่ใช่ GitOps, อย่าฝืนใส่ controller

## Steps

**1. เลือก controller + วาง repo layout ก่อนเขียน manifest แรก**

| | ArgoCD | Flux CD |
|---|---|---|
| Source of truth | `Application` CRD | `Kustomization` + `GitRepository` CRD |
| UI | มี (web) | ไม่มี (CLI `flux`) |
| เหมาะกับ | ทีมที่อยาก see/diff ใน UI | GitOps-native, multi-tenant, น้อย human |

โครง repo แยก **config ออกจาก app source** (คนละ repo หรืออย่างน้อยคนละ dir). Per-env overlay ด้วย Kustomize:
```
clusters/<cluster>/        # bootstrap: app-of-apps หรือ Flux Kustomization root
apps/<app>/base/           # kustomization.yaml + deployment/service/hpa
apps/<app>/overlays/dev/   # patch image tag, replicas, resources
apps/<app>/overlays/staging/
apps/<app>/overlays/prod/
```
**ห้าม** copy-paste manifest เต็มต่อ env — base + `patchesStrategicMerge` เท่านั้น. env ต่างกันที่ image tag / replicas / resource / ingress host

**2. App-of-apps (ArgoCD) — root Application ชี้ไปยังโฟลเดอร์ที่มี child Applications**
- Root `Application.spec.source.path` → dir ที่มี Application manifest ของแต่ละ app
- Child `Application` แต่ละตัวชี้ overlay ของ env นั้น (`overlays/prod`)
- ได้ bootstrap ทั้ง cluster ด้วย `kubectl apply -f root-app.yaml` ครั้งเดียว
- Flux เทียบเท่า: root `Kustomization` ชี้ `clusters/<cluster>/` ที่มี child `Kustomization` per app

**3. Sync policy — เปิด automation แบบมี guard**
- ArgoCD `syncPolicy.automated`: `prune: true` (ลบ resource ที่หายจาก Git), `selfHeal: true` (revert drift ใน cluster), `syncOptions: [CreateNamespace=true]`
- prod ที่ต้อง gate → ใช้ **manual sync** หรือ sync window แทน auto, อย่าเปิด `selfHeal` ถ้ายังมีคนแก้มือเป็นปกติ (จะตีกัน)
- Flux: `Kustomization.spec.prune: true` + `interval: 1m` + `wait: true` (รอ health ก่อนถือว่าสำเร็จ)
- ใส่ `ignoreDifferences` สำหรับ field ที่ controller อื่นเขียน (HPA แก้ `replicas`, webhook inject sidecar) ไม่งั้น OutOfSync ตลอด

**4. Env promotion path: dev → staging → prod**
- Promote = เปลี่ยน image tag ใน overlay ของ env ถัดไป ผ่าน Git commit/PR (ไม่ใช่ `kubectl set image`)
- ใช้ **digest pinning** (`@sha256:...`) ไม่ใช่ mutable tag เช่น `latest` — กัน drift เงียบเมื่อ tag ถูก repush
- Auto image update: ArgoCD Image Updater หรือ Flux `ImagePolicy` + `ImageUpdateAutomation` เขียน tag ใหม่กลับ Git ให้ (write-back ต้องมี deploy key/PAT แบบ write)
- prod ผ่าน PR + required review เสมอ; dev auto-promote ได้

**5. Progressive delivery — แทน rolling update**
- ArgoCD → **Argo Rollouts**: เปลี่ยน `Deployment` เป็น `Rollout`, ใส่ `strategy.canary.steps` (`setWeight` + `pause`) หรือ `strategy.blueGreen` (`activeService`/`previewService`)
- Flux → **Flagger**: สร้าง `Canary` CRD ชี้ target Deployment, กำหนด `analysis.metrics` (success-rate/latency จาก Prometheus) + `stepWeight` + `threshold`
- ผูก analysis เข้า metric จริง — canary ที่ไม่มี metric gate = blue-green ปลอม. ตั้ง `maxWeight`/`threshold` ให้ rollback อัตโนมัติเมื่อ error rate เกิน

**6. RBAC + secrets — ห้าม commit plain secret ลง Git เด็ดขาด**
- ใช้ **Sealed Secrets** (encrypt ด้วย controller public key, commit ciphertext ได้) หรือ **External Secrets Operator** (sync จาก Vault/cloud secret manager) หรือ SOPS + age/KMS
- ArgoCD RBAC: `policy.csv` map group → `role:` + จำกัด `applications, sync` ต่อ project; ใช้ `AppProject` คุม source repo/dest namespace ที่อนุญาต
- Flux: multi-tenancy ผ่าน `Kustomization.spec.serviceAccountName` + impersonation, แยก namespace ต่อ tenant
- ถ้าเจอ secret ดิบใน manifest → หยุด, แจ้ง, แนะนำ rotate ทันที (committed = leaked แม้ลบทีหลัง)

**7. Verify sync + health** (ดู ## Verify)

## Common Errors

- **OutOfSync ไม่หาย แต่ diff ว่าง** → controller (HPA/sidecar injector/webhook) เขียน field ที่ Git ไม่มี → เพิ่ม `ignoreDifferences` (ArgoCD) หรือ exclude ใน Flux, อย่า force replicas ใน manifest
- **selfHeal ตีกับ HPA** → manifest hardcode `replicas` + auto-sync revert ค่าที่ HPA ตั้ง ทุก loop → ลบ `replicas` ออกจาก manifest หรือ ignore field นั้น
- **`ComparisonError: app path does not exist`** → `source.path` ผิด หรือ `targetRevision` ชี้ branch/tag ที่ไม่มีไฟล์ — เช็ก path สัมพัทธ์จาก repo root, ไม่ใช่จาก cluster dir
- **Prune ลบ resource ที่ไม่ได้ตั้งใจ** → resource ถูกสร้างนอก Git (manual / helm hook) → mark `Prune=false` annotation หรือย้ายเข้า Git; อย่าเปิด prune ครั้งแรกบน cluster ที่มี resource เก่าค้าง — dry-run ก่อน
- **Image tag `latest` → ไม่ trigger sync** → Git ไม่เปลี่ยน controller ไม่ rollout แม้ image ใหม่ → pin digest หรือใช้ Image Updater เขียน tag กลับ Git
- **Flux reconcile เงียบ ไม่ apply** → `GitRepository` auth fail (deploy key) หรือ `Kustomization` `dependsOn` ค้างที่ dependency ยัง not-ready — เช็ก `flux get sources git` ก่อน
- **Canary ไม่ promote / ค้าง progressing** → metric provider (Prometheus) ไม่ตอบ หรือ query คืน no-data → Flagger ตีเป็น fail → verify metric query แยกก่อนผูก
- **Secret ใน Git history** → ลบไฟล์ไม่พอ, ยังอยู่ใน history → rotate ค่าจริง + ใช้ Sealed/External Secrets แทน

## Verify

```bash
# ArgoCD
argocd app get <app>                  # Sync Status = Synced, Health = Healthy
argocd app diff <app>                  # ต้องว่าง (no diff = no drift)
argocd app sync <app> --dry-run        # ก่อน sync จริงครั้งแรก/หลังเปิด prune
kubectl get applications -n argocd     # ทุก app ไม่ค้าง OutOfSync/Degraded

# Flux
flux get sources git                   # READY=True, ไม่มี auth error
flux get kustomizations                # READY=True, ไม่ค้าง dependency
flux get helmreleases                  # ถ้าใช้ helm
flux reconcile kustomization <name> --with-source   # force reconcile + ดูผล

# Progressive delivery
kubectl argo rollouts get rollout <name>            # canary steps + weight
kubectl describe canary <name>                       # Flagger: phase Succeeded, ไม่ใช่ Failed
```
**ผ่านเมื่อ:** Synced/Healthy ทุก app · `app diff` ว่าง · ไม่มี plain secret ใน Git (grep `password:|token:|sk-|AKIA|BEGIN PRIVATE KEY` ใน repo ต้องไม่เจอ) · canary promote ถึง 100% หรือ rollback อัตโนมัติเมื่อ metric เกิน threshold (ทดสอบด้วย bad image ครั้งหนึ่ง) · selfHeal revert drift ได้จริง (ลอง `kubectl edit` resource แล้วดูมัน revert)
