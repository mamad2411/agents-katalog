---
name: sky-gcp
description: >-
  Google Cloud ile web uygulaması: proje/organizasyon ve IAM (servis hesapları, Workload
  Identity Federation ile anahtarsız CI), Cloud Run (konteyner, en az işletme), Cloud SQL ve
  bağlantı, Firestore, Cloud Storage, Pub/Sub, Cloud Tasks ve Scheduler, Secret Manager,
  Artifact Registry, Cloud Build, Logging/Monitoring, bölge seçimi ve maliyet/bütçe
  alarmları. GCP üzerinde bir şey kurarken kullan.
disable-model-invocation: true
---

# Sky · Google Cloud

## Temeller

- Ortam başına ayrı **proje** (`acme-prod`, `acme-staging`), faturalandırma bütçe alarmı ilk gün.
- İnsanlar Google hesaplarıyla, uygulamalar **servis hesabı** ile; servis hesabı anahtar dosyası (JSON) indirme → yerine Cloud Run'ın kimliği / **Workload Identity Federation** (GitHub Actions OIDC, bkz. `sky-github-actions`).
- En az yetki: önceden tanımlı dar roller (`roles/run.invoker`, `roles/secretmanager.secretAccessor`), `Owner/Editor` uygulamaya asla.
- Bölge: Avrupa için `europe-west1/3/4` (Türkiye'ye yakın, KVKK değerlendirmesi — bkz. `sky-privacy-engineering`).

## Servis seçimi

| İhtiyaç | Seçim |
|---|---|
| Konteyner, sıfıra ölçeklenen, en az iş | **Cloud Run** (servisler + jobs) |
| Postgres/MySQL | **Cloud SQL** (Cloud Run'dan bağlayıcı/Unix socket, özel IP) veya AlloyDB |
| Doküman DB / mobil | Firestore (bkz. `sky-baas`) |
| Dosya | Cloud Storage (imzalı URL, lifecycle) |
| Olay/kuyruk | Pub/Sub; HTTP görev kuyruğu **Cloud Tasks** (gecikmeli/hız sınırlı işler); zamanlama **Cloud Scheduler** |
| Sırlar | Secret Manager (Cloud Run'a env veya volume olarak) |
| İmaj | Artifact Registry; build Cloud Build veya GitHub Actions |
| Statik + CDN | Cloud Storage + Cloud CDN / Firebase Hosting |

## Cloud Run

```bash
gcloud run deploy api --image europe-west1-docker.pkg.dev/acme-prod/app/api:$SHA --region europe-west1 \
  --service-account api-sa@acme-prod.iam.gserviceaccount.com --set-secrets DATABASE_URL=db-url:latest \
  --min-instances 1 --max-instances 20 --concurrency 80 --cpu 1 --memory 512Mi --no-allow-unauthenticated
```
`--min-instances 1` soğuk başlatmayı önler (maliyetli); istek başına eşzamanlılık ayarı; trafik bölme ile kademeli açılış (`--no-traffic` + `update-traffic`); uzun işler için Cloud Run Jobs. Uygulama `PORT` env'ini dinlemeli ve SIGTERM'de kapanmalı.

## Gözlem ve maliyet

Cloud Logging (yapılandırılmış JSON loglar otomatik ayrıştırılır — `severity` alanı), Error Reporting, Cloud Monitoring alarmları (5xx oranı, gecikme), Cloud Trace (OpenTelemetry).
Maliyet: log saklama/hacim, sürekli açık min instance'lar, Cloud SQL boyutu (en büyük kalem genelde), egress, NAT; etiketler (labels) ile maliyet dağılımı. Altyapıyı IaC ile kur (bkz. `sky-iac`).
