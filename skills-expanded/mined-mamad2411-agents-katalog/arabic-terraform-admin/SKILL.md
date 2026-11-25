---
name: arabic-terraform-admin
name_ar: إدارة تيرا فورم
description: Master Terraform administration in Arabic
description_ar: إتقان إدارة تيرا فورم بالعربية
category: cloud-devops
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

إتقان أساسيات Terraform لإدارة البنية التحتية ككود.

## مفاهيم أساسية

### ١. الملفات الأساسية

```
main.tf        # موارد أساسية
variables.tf   # متغيرات
outputs.tf     # مخرجات
terraform.tfvars # قيم متغيرات
```

### ٢. أوامر أساسية

```bash
# تهيئة
terraform init

# تنسيق
terraform fmt

# التحقق
terraform validate

# عرض خطة
terraform plan

# تطبيق
terraform apply

# تدمير
terraform destroy

# عرض حالة
terraform state list
```

### ٣. مورد مثال

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "Web Server"
  }
}

output "public_ip" {
  value = aws_instance.web.public_ip
}
```

## أفضل الممارسات

✅ استخدم Remote State
✅ استخدم Modules
✅ وثّق المتغيرات
✅ راجع Plan قبل Apply

❌ لا commit ملف tfstate
❌ لا تستخدم hard-coded values
❌ لا تهمل Version Locking

---

## الكلمات المفتاحية

عربي: "تيرا فورم", "Terraform", "IaC", "بنية تحتية"
English: "Terraform arabic", "infrastructure as code", "IaC", "DevOps"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
