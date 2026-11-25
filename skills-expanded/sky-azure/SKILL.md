---
name: sky-azure
description: >-
  Microsoft Azure ile web uygulaması: abonelik/kaynak grupları ve Entra ID (kimlik), managed
  identity ile anahtarsız erişim, App Service ve Container Apps, Azure Functions, Azure Database
  for PostgreSQL, Blob Storage, Service Bus ve Queue Storage, Key Vault, Azure OpenAI erişimi,
  Application Insights, Bicep/Terraform, kurumsal müşteri gereksinimleri (SSO, uyumluluk) ve
  maliyet yönetimi. Azure kullanan veya kurumsal (Microsoft ekosistemi) müşteri projesinde kullan.
disable-model-invocation: true
---

# Sky · Azure

## Temeller

- Hiyerarşi: Management group → **Subscription** (ortam/fatura sınırı) → **Resource group** (birlikte yaşayan kaynaklar) → kaynaklar. Ortam başına ayrı abonelik veya en az ayrı kaynak grubu.
- Kimlik: **Entra ID** (eski Azure AD); uygulamalar **managed identity** ile Key Vault/Storage/DB'ye erişir — bağlantı dizesinde sır yok.
- RBAC en az yetki (`Key Vault Secrets User`, `Storage Blob Data Contributor`); CI için workload identity federation (GitHub OIDC).
- Bütçe ve maliyet alarmları (Cost Management), etiketler.

## Servis seçimi

| İhtiyaç | Seçim |
|---|---|
| Web uygulaması (kod veya konteyner), basit | **App Service** (deployment slot'ları ile sıfır kesinti) |
| Konteyner, mikroservis, sıfıra ölçeklenme | **Container Apps** (KEDA tabanlı ölçekleme, Dapr) |
| Olay tabanlı fonksiyon | Azure Functions |
| Postgres | Azure Database for PostgreSQL – Flexible Server |
| Dosya | Blob Storage (SAS token ile kısa ömürlü erişim) |
| Kuyruk/olay | **Service Bus** (kurumsal mesajlaşma, oturumlar, DLQ), Queue Storage (basit), Event Grid |
| Sırlar | **Key Vault** (App Service'te Key Vault referansları) |
| Gözlem | **Application Insights** (+ Azure Monitor, OpenTelemetry distro) |
| LLM | Azure OpenAI / Azure AI Foundry (veri bölgesi ve kurumsal sözleşme gerektiren müşteriler) |

## Kurumsal müşteri gereksinimleri

Microsoft ekosistemindeki kurumlar sıklıkla ister: **Entra ID ile SSO** (OIDC/SAML — bkz. `sky-auth`), SCIM ile kullanıcı sağlama, veri bölgesi (AB), denetim kayıtları, özel ağ (Private Endpoint), uyumluluk belgeleri.

## IaC ve dağıtım

**Bicep** (Azure'a özgü, ARM'ın okunur hali) veya Terraform `azurerm` (bkz. `sky-iac`); `az` CLI; GitHub Actions `azure/login` (OIDC). App Service slot swap ile önce staging'e dağıt, ısındır, değiştir; Container Apps revizyonları ile trafik bölme.

## Dikkat

Kaynak adları genelde küresel benzersiz ve kısıtlı karakterli (storage hesabı: küçük harf + rakam, ≤ 24); bölge bazlı servis/kota farkları; ücretsiz katman sınırları; silinen Key Vault'un geçici silme (soft delete) koruması (aynı adı hemen yeniden kullanamazsın).
