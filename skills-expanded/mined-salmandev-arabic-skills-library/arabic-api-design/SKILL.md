---
name: arabic-api-design
name_ar: تصميم APIs
description: Master API design in Arabic
description_ar: إتقان تصميم واجهات برمجة التطبيقات بالعربية
category: developer
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

إتقان أساسيات تصميم APIs احترافية وقابلة للتوسع.

## مبادئ تصميم

### ١. RESTful Design

**المبادئ:**
- موارد واضحة
- أفعال HTTP صحيحة
- Stateless
- HATEOAS

### ٢. تسمية موارد

```
✓ /users (جمع)
✓ /users/123 (IDs)
✓ /users/123/posts (علاقات)
✗ /getUser (أفعال)
✗ /Users (حروف كبيرة)
```

### ٣. استجابات

**هيكل JSON:**
```json
{
  "success": true,
  "data": {...},
  "message": "تم بنجاح",
  "errors": []
}
```

### ٤. أخطاء

**أكواد HTTP:**
- 200 نجاح
- 201 تم إنشاء
- 400 طلب خاطئ
- 401 غير مصرح
- 404 غير موجود
- 500 خطأ خادم

## أفضل الممارسات

✅ توثيق شامل
✅ إصدار API (v1, v2)
✅ Rate Limiting
✅ Authentication

❌ لا تهمل أمان
❌ لا تهمل توثيق
❌ لا تهمل إصدارات

---

## الكلمات المفتاحية

عربي: "تصميم APIs", "API Design", "REST", "RESTful"
English: "API design arabic", "REST API", "API development", "web services"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
