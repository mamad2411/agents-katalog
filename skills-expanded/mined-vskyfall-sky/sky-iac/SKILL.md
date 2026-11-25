---
name: sky-iac
description: >-
  Altyapıyı kodla yönetme (IaC): Terraform/OpenTofu ve Pulumi seçimi, proje yapısı ve modüller,
  uzak state ve kilitleme, ortamlar (workspace vs klasör), değişken ve sır yönetimi, plan/apply
  iş akışı ve CI'da plan yorumu, drift tespiti, import ile mevcut kaynakları alma, güvenli
  değişiklik (prevent_destroy, lifecycle), etiketleme ve maliyet, sık hatalar. "Terraform",
  "altyapıyı kodla", "IaC", "AWS kaynaklarını otomatikleştir" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Altyapı Kod Olarak (IaC)

## Seçim

| Araç | Ne zaman |
|---|---|
| **Terraform / OpenTofu** | en yaygın, her sağlayıcı, HCL; OpenTofu açık kaynak çatalı |
| **Pulumi** | TypeScript/Python ile altyapı, uygulama kodu gibi test ve soyutlama |
| SST | AWS üzerinde full-stack uygulama altyapısı (TS) |
| Sağlayıcıya özel (CDK, Bicep) | tek bulutta derin entegrasyon |

## Yapı (Terraform)

```
infra/
  modules/
    app_service/ {main.tf, variables.tf, outputs.tf}
    database/
  envs/
    staging/ {main.tf, backend.tf, terraform.tfvars}
    prod/    {main.tf, backend.tf, terraform.tfvars}
```
Ortam başına ayrı klasör ve state (workspace'ler yerine) — prod'a yanlışlıkla apply riski azalır.

## State

```hcl
terraform {
  required_version = ">= 1.6"
  backend "s3" {
    bucket       = "acme-tfstate"
    key          = "prod/app.tfstate"
    region       = "eu-central-1"
    encrypt      = true
    use_lockfile = true      # S3 yerel kilit (veya DynamoDB kilit tablosu)
  }
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
}
```
- State **uzakta**, şifreli, kilitli, sürümlü bucket. State dosyası sır içerir → erişim kısıtlı, Git'e asla.
- Sağlayıcı sürümleri sabit (`.terraform.lock.hcl` commit'li).

## İş akışı

1. `terraform fmt` + `validate` + `tflint` (+ `checkov`/`trivy config` güvenlik taraması).
2. PR'da `terraform plan` → çıktı PR yorumu olarak (Atlantis, Spacelift, GitHub Actions). **Plan'ı oku**: `destroy` / `replace` satırları kırmızı bayrak.
3. Onaydan sonra `apply` (CI'dan, kişisel makineden değil); prod için manuel onay adımı.
4. Gece `plan` ile **drift** tespiti (konsoldan elle yapılan değişiklikler).

## Güvenli değişiklik

```hcl
resource "aws_db_instance" "main" {
  # ...
  deletion_protection = true
  lifecycle { prevent_destroy = true }
}
```
- Yeniden adlandırma = sil + oluştur → `moved {}` bloğu ile state taşı.
- Mevcut kaynakları almak: `import {}` bloğu + `terraform plan -generate-config-out=generated.tf`.
- Sırlar değişkende değil sır yöneticisinde (AWS Secrets Manager/SSM, Vault); `sensitive = true` çıktılarda.

## Modüller

Küçük ve odaklı (ağ, veritabanı, uygulama servisi); girdi doğrulaması (`validation {}`), anlamlı çıktılar, README.
Topluluk modülleri (terraform-aws-modules) sürüm sabitleyerek kullan.

## Etiketleme ve maliyet

`default_tags { tags = { project = "sky", env = "prod", owner = "platform" } }` sağlayıcı seviyesinde → maliyet raporu etikete göre.
PR'da maliyet farkı: Infracost.

## Pulumi kısaca

```ts
const bucket = new aws.s3.BucketV2("uploads", { tags: { env: pulumi.getStack() } });
export const bucketName = bucket.id;
```
Stack = ortam; sırlar `pulumi config set --secret`; aynı plan/preview disiplini.

## Sık hatalar

Elle konsol değişiklikleri (drift), tek state'te her şey (patlama alanı büyük), `count` ile liste — sıra değişince kaynaklar yeniden oluşur
(`for_each` + anahtar kullan), plan okumadan apply, kişisel kimlik bilgileriyle prod apply.
