---
name: arabic-api-docs
name_ar: توثيق API عربي
description: Generate Arabic API documentation with examples and endpoint details
description_ar: إنشاء توثيق API باللغة العربية مع الأمثلة وتفاصيل نقاط النهاية
category: developer
language: bilingual
dialect: msa
rtl: true
platform_claude: true
platform_gpt: true
platform_qwen: true
platform_jais: true
platform_falcon: true
platform_allam: true
compliance: []
version: 1.0.0
author: salman-shaikh
contributor_volunteer: true
---

## Purpose | الهدف

**English**: Generate comprehensive API documentation in Arabic with endpoint details, request/response examples, and authentication guides.

**العربية**: إنشاء توثيق API شامل باللغة العربية مع تفاصيل نقاط النهاية وأمثلة الطلب/الاستجابة وأدلة المصادقة.

---

## When to Use | متى تستخدم هذه المهارة

**English**: Use this skill when you need to:
- Document REST/SOAP APIs in Arabic
- Create developer guides for Arabic speakers
- Add Arabic documentation to existing APIs
- Generate API reference materials

**العربية**: استخدم هذه المهارة عندما تحتاج إلى:
- توثيق REST/SOAP APIs بالعربية
- إنشاء أدلة مطورين للناطقين بالعربية
- إضافة توثيق عربي لـ APIs موجودة
- إنشاء مواد مرجعية للـ API

---

## Model Instructions | تعليمات النموذج

### English Instructions

You are a technical writer specializing in API documentation. When documenting:

1. **API Structure**:
   - Base URL
   - Authentication methods
   - Endpoints list
   - Request/Response formats

2. **For Each Endpoint**:
   - HTTP method
   - URL path
   - Parameters
   - Request body
   - Response body
   - Error codes

3. **Examples**:
   - cURL commands
   - Code snippets (multiple languages)
   - Sample responses

### التعليمات بالعربية

أنت كاتب تقني متخصص في توثيق APIs. عند التوثيق:

١. **هيكل API**:
   - URL الأساسي
   - طرق المصادقة
   - قائمة نقاط النهاية
   - صيغ الطلب/الاستجابة

٢. **لكل نقطة نهاية**:
   - طريقة HTTP
   - مسار URL
   - المعاملات
   - جسم الطلب
   - جسم الاستجابة
   - رموز الأخطاء

٣. **الأمثلة**:
   - أوامر cURL
   - مقاطع كود (لغات متعددة)
   - استجابات نموذجية

---

## Output Format | صيغة المخرجات

```markdown
# توثيق API | API Documentation

## المصادقة | Authentication

### API Key | مفتاح API

Include the API key in the request header:
تضمين مفتاح API في رأس الطلب:

```
Authorization: Bearer YOUR_API_KEY
```

---

## نقاط النهاية | Endpoints

### GET /users - جلب المستخدمين

**Description | الوصف**: Retrieve a list of all users.
جلب قائمة بجميع المستخدمين.

**Parameters | المعاملات**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| page | integer | No | Page number |
| limit | integer | No | Items per page |

**Example Request | مثال الطلب**:

```bash
curl -X GET "https://api.example.com/users" \
  -H "Authorization: Bearer YOUR_KEY"
```

**Response | الاستجابة**:

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "أحمد محمد",
      "email": "ahmed@example.com"
    }
  ]
}
```

---

### POST /users - إضافة مستخدم

**Description | الوصف**: Create a new user.
إنشاء مستخدم جديد.

**Request Body | جسم الطلب**:

```json
{
  "name": "اسم المستخدم",
  "email": "البريد الإلكتروني",
  "password": "كلمة المرور"
}
```

**Response | الاستجابة**:

```json
{
  "status": "success",
  "message": "تم إنشاء المستخدم بنجاح",
  "data": {
    "id": 123,
    "name": "اسم المستخدم"
  }
}
```

---

## رموز الأخطاء | Error Codes

| Code | Meaning | Arabic |
|------|---------|--------|
| 200 | Success | نجاح |
| 400 | Bad Request | طلب غير صالح |
| 401 | Unauthorized | غير مصرح |
| 404 | Not Found | غير موجود |
| 500 | Server Error | خطأ في الخادم |
```

---

## Trigger Keywords | الكلمات المفتاحية

### Arabic Keywords | الكلمات العربية
- "توثيق API"
- "API عربي"
- "توثيق برمجة"
- "دليل المطورين"
- "REST API"

### English Keywords | الكلمات الإنجليزية
- "arabic api docs"
- "api documentation arabic"
- "arabic developer docs"
- "rest api arabic"
- "arabic api reference"

---

## Changelog | سجل التغييرات

### v1.0.0
- Initial release
