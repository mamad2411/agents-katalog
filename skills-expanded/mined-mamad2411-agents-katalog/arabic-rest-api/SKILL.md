---
name: arabic-rest-api
name_ar: واجهة REST
description: Design REST APIs in Arabic
description_ar: تصميم واجهات REST بالعربية
category: developer
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

تصميم وبناء REST APIs باللغة العربية.

## مبادئ REST

- **Resources** - الموارد
- **HTTP Methods** - طرق HTTP
- **Stateless** - بدون حالة
- **Uniform Interface** - واجهة موحدة

## طرق HTTP

| Method | الاستخدام | مثال |
|--------|----------|------|
| GET | جلب | GET /users |
| POST | إنشاء | POST /users |
| PUT | تحديث كامل | PUT /users/1 |
| PATCH | تحديث جزئي | PATCH /users/1 |
| DELETE | حذف | DELETE /users/1 |

## تصميم المسارات

```
جيد:
GET    /users
GET    /users/123
POST   /users
PUT    /users/123
DELETE /users/123

سيء:
GET    /getUsers
POST   /createUser
GET    /getUserById?id=123
```

## رموز الحالة

| الكود | المعنى |
|-------|--------|
| 200 | نجاح |
| 201 | تم الإنشاء |
| 400 | طلب خاطئ |
| 401 | غير مصرح |
| 403 | ممنوع |
| 404 | غير موجود |
| 500 | خطأ خادم |

## مثال استجابة

```json
{
  "success": true,
  "data": {
    "id": 123,
    "name": "أحمد محمد",
    "email": "ahmed@example.com"
  },
  "message": "تم جلب البيانات بنجاح"
}
```

## التوثيق

استخدم OpenAPI/Swagger:

```yaml
openapi: 3.0.0
info:
  title: API المستخدمين
  version: 1.0.0
paths:
  /users:
    get:
      summary: جلب جميع المستخدمين
      responses:
        '200':
          description: نجاح
```

---

## الكلمات المفتاحية

عربي: "REST API", "واجهة برمجة", "HTTP"
English: "REST API arabic", "API design", "backend"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
