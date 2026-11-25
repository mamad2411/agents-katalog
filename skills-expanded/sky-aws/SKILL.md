---
name: sky-aws
description: >-
  AWS'yi web uygulaması için pratik kullanma: hesap güvenliği (root kilitleme, IAM Identity
  Center, MFA), IAM en az yetki ve rol tabanlı erişim, doğru servis seçimi (S3, CloudFront,
  Lambda, ECS Fargate, App Runner, RDS/Aurora, DynamoDB, SQS/SNS/EventBridge, SES, Secrets
  Manager, CloudWatch), bölge seçimi, maliyet tuzakları ve bütçe alarmları, CLI ve SDK
  kullanımı. AWS üzerinde bir şey kurarken veya "AWS faturası arttı" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · AWS

## Hesap güvenliği (ilk gün)

1. Root kullanıcıya MFA, root erişim anahtarı **yok**, root'u günlük işte kullanma.
2. **IAM Identity Center** (SSO) ile insan kullanıcılar; uzun ömürlü erişim anahtarı yerine `aws sso login`.
3. Organizations: ayrı hesaplar (prod / staging / dev) — patlama alanı ve fatura ayrımı.
4. **Bütçe alarmı** (AWS Budgets) ve maliyet anomalisi tespiti açık — sürpriz fatura en büyük AWS korkusu.
5. CloudTrail tüm bölgelerde açık; GuardDuty önerilir.

## IAM

- İnsan → SSO rolü; uygulama → **IAM rolü** (Lambda execution role, ECS task role) — koda anahtar gömme.
- CI (GitHub Actions) → **OIDC** ile rol üstlenme, statik anahtar yok.
- En az yetki: belirli kaynak ARN'leri, `"Action": "*"` yok; IAM Access Analyzer ile kullanılmayan izinleri temizle.

## Servis seçimi (web uygulaması için)

| İhtiyaç | Seçim |
|---|---|
| Statik site / SPA | S3 + **CloudFront** (OAC ile bucket özel) — veya Amplify Hosting |
| Konteyner, en az iş | **App Runner** veya **ECS Fargate** (+ ALB) |
| Olay tabanlı / az trafik | **Lambda** (+ API Gateway veya Function URL) |
| İlişkisel DB | **RDS Postgres** / Aurora Serverless v2 |
| Anahtar-değer, büyük ölçek | DynamoDB (erişim kalıplarını önceden tasarla) |
| Kuyruk | **SQS** (+ DLQ); olay yönlendirme EventBridge; fan-out SNS |
| E-posta | **SES** (sandbox'tan çıkış talebi, SPF/DKIM/DMARC) |
| Sırlar | Secrets Manager (rotasyon) / SSM Parameter Store (ucuz) |
| Log/metrik/alarm | CloudWatch (log saklama süresini ayarla!) |
| Dosya | S3 (presigned URL, lifecycle, versiyonlama) — bkz. `sky-storage` |

Bölge: Türkiye'ye yakın ve servis zengin `eu-central-1` (Frankfurt); KVKK yurt dışı aktarım değerlendirmesi (bkz. `sky-privacy-engineering`).

## Maliyet tuzakları

- **NAT Gateway** (saatlik + GB başına) — özel alt ağdaki Lambda/ECS'in internete çıkışı pahalı; VPC endpoint'leri (S3, DynamoDB) ücretsiz/ucuz.
- CloudWatch Logs saklama "sonsuz" varsayılan → 14–30 gün yap.
- Kullanılmayan EBS hacimleri, eski snapshot'lar, boşta RDS, ayrılmış Elastic IP.
- Veri çıkışı (egress) — CloudFront arkasına koy.
- Lambda'da aşırı bellek veya sonsuz döngü (özyinelemeli tetikleme: S3 → Lambda → aynı bucket'a yazma).
- Cost Explorer'da etiket bazlı rapor (bkz. `sky-iac` default_tags).

## CLI ve SDK

```bash
aws sso login --profile acme-prod
aws s3 sync ./out s3://acme-site --delete --profile acme-prod
aws logs tail /aws/lambda/api --follow
```
SDK v3 (JS): modüler istemciler (`@aws-sdk/client-s3`), bölgeyi açık ver, kimliği ortamdan/rolden al. Altyapıyı elle değil IaC ile kur (bkz. `sky-iac`).

## Mimari ipuçları

- Özel alt ağda RDS, yalnızca uygulamanın güvenlik grubundan erişim; RDS Proxy (Lambda'dan bağlantı patlamasına karşı).
- Çok AZ (prod DB), otomatik yedek + PITR.
- Sağlık kontrolleri ve alarmlar (5xx oranı, DB CPU, SQS en eski mesaj yaşı) → SNS → e-posta/Slack.
