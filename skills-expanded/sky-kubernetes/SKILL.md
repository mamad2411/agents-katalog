---
name: sky-kubernetes
description: >-
  Kubernetes ile uygulama çalıştırma: ne zaman gerçekten gerekli, Deployment/Service/Ingress/
  ConfigMap/Secret temelleri, kaynak istek ve limitleri, liveness/readiness/startup probe'ları,
  HPA ile otomatik ölçekleme, sıfır kesintili rolling update, Helm ve Kustomize, migration'ları
  Job ile çalıştırma, gizli bilgi yönetimi, ağ politikaları, gözlem ve hata ayıklama (kubectl
  komutları), yönetilen kümeler ve daha basit alternatifler. Kubernetes işlerinde kullan.
disable-model-invocation: true
---

# Sky · Kubernetes

## Önce: gerekli mi?

Tek uygulama + DB için Kubernetes çoğu zaman fazladır: Vercel/Fly/Railway/Render, Coolify/Dokploy (VPS), ECS/Cloud Run
daha az iş çıkarır. K8s şu durumlarda mantıklı: çok servis, takım zaten biliyor, şirket platformu K8s, özel ölçekleme ihtiyacı.

## Minimum manifest seti

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: api, labels: { app: api } }
spec:
  replicas: 2
  selector: { matchLabels: { app: api } }
  strategy: { rollingUpdate: { maxUnavailable: 0, maxSurge: 1 } }
  template:
    metadata: { labels: { app: api } }
    spec:
      securityContext: { runAsNonRoot: true }
      containers:
        - name: api
          image: ghcr.io/acme/api:3f2a9c1          # SHA etiketi
          ports: [{ containerPort: 8080 }]
          envFrom: [{ configMapRef: { name: api-config } }, { secretRef: { name: api-secrets } }]
          resources:
            requests: { cpu: 100m, memory: 256Mi }
            limits: { memory: 512Mi }               # CPU limiti çoğu zaman throttling yaratır; bellek limiti koy
          readinessProbe: { httpGet: { path: /health/ready, port: 8080 }, periodSeconds: 5 }
          livenessProbe: { httpGet: { path: /health/live, port: 8080 }, periodSeconds: 10, failureThreshold: 3 }
          startupProbe: { httpGet: { path: /health/live, port: 8080 }, failureThreshold: 30, periodSeconds: 2 }
          securityContext: { allowPrivilegeEscalation: false, readOnlyRootFilesystem: true }
---
apiVersion: v1
kind: Service
metadata: { name: api }
spec: { selector: { app: api }, ports: [{ port: 80, targetPort: 8080 }] }
```
Ingress (veya Gateway API) + cert-manager ile TLS; PodDisruptionBudget (`minAvailable: 1`).

## Probe'lar (en sık yanlış yapılan)

- **readiness**: trafik alabilir mi? (DB bağlantısı dahil olabilir) → başarısızsa yalnızca trafikten çıkarılır.
- **liveness**: süreç kilitlendi mi? → başarısızsa yeniden başlatılır. **DB'ye bağlı yapma** (DB düşünce tüm pod'lar sonsuz yeniden başlar).
- **startup**: yavaş açılan uygulamada liveness'ı açılış bitene kadar beklet.
- Uygulama SIGTERM'de: readiness'ı kapat, açık istekleri bitir, çık (`terminationGracePeriodSeconds`).

## Ölçekleme

`HorizontalPodAutoscaler` (CPU %70 veya özel metrik), en az 2 replika (tek pod = tek hata noktası). Arka plan worker'ları
kuyruk derinliğine göre KEDA ile ölçeklenebilir.

## Yapılandırma ve sırlar

- ConfigMap düz ayarlar; Secret base64 — **şifreleme değil**. Gerçek sır yönetimi: External Secrets Operator (AWS/GCP secret manager, Vault),
  Sealed Secrets veya SOPS ile Git'te şifreli.
- Sır değişince pod'ları yeniden başlat (checksum annotation / Reloader).

## Paketleme

- **Kustomize**: base + overlays (staging/prod) — basit, kubectl'de yerleşik.
- **Helm**: parametreli chart'lar, üçüncü parti yazılım kurulumu (ingress-nginx, cert-manager, Postgres operatörleri).
- GitOps: Argo CD / Flux — küme durumu Git'ten senkron, geri alma = git revert.

## Migration

Deploy öncesi `Job` (veya Helm pre-upgrade hook / Argo sync wave) ile migration; uygulama pod'ları başlangıçta migration çalıştırmasın
(çoklu replika yarışır). Geriye uyumlu migration şart (bkz. `sky-data`).

## Ağ ve güvenlik

NetworkPolicy ile varsayılan reddet + gerekli akışlara izin; RBAC en az yetki; imaj tarama; Pod Security Standards (restricted).
Veritabanını küme içinde çalıştırmak yerine yönetilen DB (RDS/Cloud SQL) çoğu ekip için daha güvenli.

## Hata ayıklama

```bash
kubectl get pods -l app=api -o wide
kubectl describe pod <pod>              # Events: ImagePullBackOff, OOMKilled, probe hataları
kubectl logs <pod> --previous           # çöken önceki konteynerin logu
kubectl rollout status deploy/api && kubectl rollout undo deploy/api
kubectl port-forward svc/api 8080:80
kubectl top pods                         # metrics-server gerekli
```
| Durum | Sebep |
|---|---|
| `CrashLoopBackOff` | uygulama açılışta çöküyor — `logs --previous` |
| `OOMKilled` | bellek limiti düşük veya sızıntı |
| `ImagePullBackOff` | etiket yok / registry kimliği |
| Pending | kaynak isteği karşılanamıyor / node seçici |

Yönetilen kümeler: EKS, GKE (Autopilot en az bakım), AKS, DigitalOcean/Hetzner (k3s). Yerel: kind, k3d, OrbStack.
