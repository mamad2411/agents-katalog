---
name: arabic-azure
name_ar: مايكروسوفت أزور
description: Master Microsoft Azure cloud services in Arabic
description_ar: إتقان خدمات سحابة مايكروسوفت أزور بالعربية
category: developer
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

إتقان استخدام خدمات Azure السحابية باللغة العربية.

## الخدمات الأساسية

### ١. الحوسبة (Compute)

| الخدمة | الوصف | الاستخدام |
|--------|-------|----------|
| **Virtual Machines** | خوادم افتراضية | Windows/Linux VMs |
| **App Service** | استضافة تطبيقات | Web Apps, APIs |
| **Functions** | حوسبة بدون خادم | Event-driven |
| **AKS** | Kubernetes managed | حاويات |
| **Batch** | معالجة دفعية | High-performance computing |

### ٢. التخزين (Storage)

| الخدمة | الوصف | النوع |
|--------|-------|-------|
| **Blob Storage** | تخزين كائنات | ملفات، صور، فيديو |
| **File Storage** | تخزين ملفات | SMB/NFS |
| **Disk Storage** | أقراص VMs | SSD/HDD |
| **Archive** | أرشفة | بيانات نادرة |

### ٣. قواعد البيانات

| الخدمة | الوصف | النوع |
|--------|-------|-------|
| **SQL Database** | قواعد علائقية | SQL Server |
| **Cosmos DB** | NoSQL عالمي | Multi-model |
| **MySQL/PostgreSQL** | مفتوحة المصدر | PaaS |
| **Redis Cache** | تخزين مؤقت | In-memory |

### ٤. الشبكات

| الخدمة | الوصف |
|--------|-------|
| **VNet** | شبكة افتراضية |
| **Load Balancer** | موازن حمل |
| **Application Gateway** | بوابة تطبيقات |
| **CDN** | شبكة توزيع محتوى |
| **DNS** | خدمة نطاقات |

### ٥. الأمان

| الخدمة | الوصف |
|--------|-------|
| **Active Directory** | إدارة هوية |
| **Key Vault** | إدارة مفاتيح |
| **Security Center** | مركز أمان |
| **Sentinel** | SIEM سحابي |

## Azure CLI

```bash
# تسجيل دخول
az login

# عرض الموارد
az resource list

# إنشاء VM
az vm create \
  --resource-group myRG \
  --name myVM \
  --image UbuntuLTS \
  --size Standard_B1s

# إنشاء Web App
az webapp create \
  --resource-group myRG \
  --plan myAppServicePlan \
  --name mywebapp

# عرض logs
az monitor activity-log list \
  --resource-group myRG
```

## ARM Template مثال

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "resources": [{
    "type": "Microsoft.Storage/storageAccounts",
    "apiVersion": "2021-02-01",
    "name": "mystorageaccount",
    "location": "[resourceGroup().location]",
    "sku": {
      "name": "Standard_LRS"
    },
    "kind": "StorageV2"
  }]
}
```

## أفضل الممارسات

✅ استخدم Resource Groups للتنظيم
✅ استخدم Tags للتكلفة
✅ فعل Azure Policy
✅ استخدم Managed Identities
✅ راقب التكلفة بـ Cost Management

---

## الكلمات المفتاحية

عربي: "أزور", "سحابة", "مايكروسوفت"
English: "azure arabic", "microsoft cloud", "cloud computing"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
