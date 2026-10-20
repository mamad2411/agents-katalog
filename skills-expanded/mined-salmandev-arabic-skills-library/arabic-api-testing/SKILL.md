---
name: arabic-api-testing
name_ar: اختبار واجهات البرمجة
description: Create comprehensive API testing documentation in Arabic with test cases
description_ar: إعداد توثيق شامل لاختبار واجهات البرمجة بالعربية مع حالات الاختبار
category: developer
language: ar
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

## الهدف (Purpose)

يساعد هذه المهارة في إعداد توثيق شامل لاختبار واجهات البرمجة (API Testing) باللغة العربية الفصحى، يتضمن حالات الاختبار، السيناريوهات، النتائج المتوقعة، وتقارير الأخطاء، لتسهيل عملية ضمان الجودة.

---

## متى تستخدم هذه المهارة (When to Use)

استخدم هذه المهارة عندما تحتاج إلى:

- توثيق حالات اختبار API
- إعداد خطط اختبار شاملة
- كتابة تقارير أخطاء تقنية
- إنشاء أدلة اختبار للمطورين
- توثيق نتائج الاختبار

---

## تعليمات النموذج (Model Instructions)

أنت مهندس جودة برمجيات (QA Engineer) متخصص في اختبار APIs. عند إعداد التوثيق:

### مبادئ الاختبار الجيد

١. **الشمول**: تغطية جميع السيناريوهات
٢. **الوضوح**: خطوات قابلة للتكرار
٣. **الدقة**: نتائج متوقعة محددة
٤. **القابلية للأتمتة**: هيكل قابل للتحويل لكود

### هيكل التوثيق

١. **معلومات الـ API**
٢. **حالات الاختبار**
٣. **البيانات الاختبارية**
٤. **النتائج والتقارير**

---

## مثال (Example)

**الطلب:**
```
وثق اختبار API لنظام مستخدمين.
```

**النتيجة المتوقعة:**
```
# خطة اختبار واجهة البرمجة

## API Testing Documentation

---

## ١. معلومات الـ API

### ١.١ نظرة عامة

| البند | التفاصيل |
|-------|----------|
| **اسم الـ API** | نظام إدارة المستخدمين |
| **الإصدار** | v1.0.0 |
| **البيئة** | https://api.example.com/v1 |
| **نوع المصادقة** | Bearer Token (JWT) |
| **تنسيق البيانات** | JSON |

### ١.٢ النقاط الطرفية (Endpoints)

| الطريقة | المسار | الوصف | المصادقة |
|---------|--------|-------|----------|
| POST | /auth/register | تسجيل مستخدم جديد | لا |
| POST | /auth/login | تسجيل الدخول | لا |
| GET | /users | قائمة المستخدمين | نعم |
| GET | /users/{id} | تفاصيل المستخدم | نعم |
| PUT | /users/{id} | تحديث المستخدم | نعم |
| DELETE | /users/{id} | حذف المستخدم | نعم |

---

## ٢. حالات الاختبار

### ٢.١ اختبار التسجيل (Register)

#### TC-AUTH-001: تسجيل مستخدم جديد بنجاح

| البند | التفاصيل |
|-------|----------|
| **المعرف** | TC-AUTH-001 |
| **العنوان** | تسجيل مستخدم جديد بنجاح |
| **النقطة الطرفية** | POST /api/v1/auth/register |
| **الأولوية** | عالية 🔴 |
| **النوع** | Functional |

**الطلب (Request):**
```json
{
  "email": "test@example.com",
  "password": "Test@123456",
  "fullName": "أحمد محمد",
  "phone": "+966501234567"
}
```

**الاستجابة المتوقعة (Expected Response):**
```json
Status: 201 Created
{
  "success": true,
  "message": "تم التسجيل بنجاح",
  "data": {
    "userId": "usr_123456",
    "email": "test@example.com",
    "fullName": "أحمد محمد",
    "createdAt": "2025-01-15T10:30:00Z"
  }
}
```

**خطوات الاختبار:**
1. إرسال طلب POST إلى /api/v1/auth/register
2. التحقق من كود الحالة 201
3. التحقق من وجود userId في الاستجابة
4. التحقق من صحة البريد الإلكتروني المسجل
5. التحقق من رسالة النجاح بالعربية

**معايير النجاح:**
- [ ] كود الحالة 201
- [ ] success = true
- [ ] userId غير فارغ
- [ ] email مطابق للطلب
- [ ] رسالة النجاح بالعربية

---

#### TC-AUTH-002: تسجيل ببريد إلكتروني مكرر

| البند | التفاصيل |
|-------|----------|
| **المعرف** | TC-AUTH-002 |
| **العنوان** | تسجيل ببريد إلكتروني مكرر |
| **النقطة الطرفية** | POST /api/v1/auth/register |
| **الأولوية** | عالية 🔴 |
| **النوع** | Negative |

**الطلب:**
```json
{
  "email": "existing@example.com",
  "password": "Test@123456",
  "fullName": "مستخدم جديد",
  "phone": "+966501234567"
}
```

**الاستجابة المتوقعة:**
```json
Status: 409 Conflict
{
  "success": false,
  "error": {
    "code": "EMAIL_EXISTS",
    "message": "البريد الإلكتروني مسجل مسبقاً",
    "field": "email"
  }
}
```

**خطوات الاختبار:**
1. محاولة تسجيل ببريد موجود مسبقاً
2. التحقق من كود الحالة 409
3. التحقق من كود الخطأ EMAIL_EXISTS
4. التحقق من رسالة الخطأ بالعربية

---

#### TC-AUTH-003: تسجيل بكلمة مرور ضعيفة

| البند | التفاصيل |
|-------|----------|
| **المعرف** | TC-AUTH-003 |
| **العنوان** | تسجيل بكلمة مرور ضعيفة |
| **النقطة الطرفية** | POST /api/v1/auth/register |
| **الأولوية** | متوسطة 🟡 |
| **النوع** | Validation |

**الطلب:**
```json
{
  "email": "test2@example.com",
  "password": "123",
  "fullName": "مستخدم اختبار",
  "phone": "+966501234567"
}
```

**الاستجابة المتوقعة:**
```json
Status: 400 Bad Request
{
  "success": false,
  "error": {
    "code": "WEAK_PASSWORD",
    "message": "كلمة المرور ضعيفة جداً. يجب أن تحتوي على ٨ أحرف على الأقل وحرف كبير ورقم ورمز",
    "field": "password",
    "requirements": {
      "minLength": 8,
      "requireUppercase": true,
      "requireNumber": true,
      "requireSpecialChar": true
    }
  }
}
```

---

### ٢.٢ اختبار تسجيل الدخول (Login)

#### TC-AUTH-010: تسجيل دخول ناجح

| البند | التفاصيل |
|-------|----------|
| **المعرف** | TC-AUTH-010 |
| **العنوان** | تسجيل دخول ناجح |
| **النقطة الطرفية** | POST /api/v1/auth/login |
| **الأولوية** | عالية 🔴 |
| **النوع** | Functional |

**الطلب:**
```json
{
  "email": "test@example.com",
  "password": "Test@123456"
}
```

**الاستجابة المتوقعة:**
```json
Status: 200 OK
{
  "success": true,
  "message": "تم تسجيل الدخول بنجاح",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "refreshToken": "dGhpcyBpcyBhIHJlZnJl...",
    "expiresIn": 3600,
    "user": {
      "userId": "usr_123456",
      "email": "test@example.com",
      "fullName": "أحمد محمد",
      "role": "user"
    }
  }
}
```

**خطوات الاختبار:**
1. إرسال بيانات الدخول الصحيحة
2. التحقق من كود الحالة 200
3. التحقق من وجود accessToken
4. التحقق من صحة بيانات المستخدم
5. التحقق من رسالة النجاح بالعربية

---

#### TC-AUTH-011: تسجيل دخول بكلمة مرور خاطئة

| البند | التفاصيل |
|-------|----------|
| **المعرف** | TC-AUTH-011 |
| **العنوان** | تسجيل دخول بكلمة مرور خاطئة |
| **النقطة الطرفية** | POST /api/v1/auth/login |
| **الأولوية** | عالية 🔴 |
| **النوع** | Negative |

**الطلب:**
```json
{
  "email": "test@example.com",
  "password": "WrongPassword123"
}
```

**الاستجابة المتوقعة:**
```json
Status: 401 Unauthorized
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "البريد الإلكتروني أو كلمة المرور غير صحيحة"
  }
}
```

---

### ٢.٣ اختبار إدارة المستخدمين (Users)

#### TC-USR-001: جلب قائمة المستخدمين

| البند | التفاصيل |
|-------|----------|
| **المعرف** | TC-USR-001 |
| **العنوان** | جلب قائمة المستخدمين مع Pagination |
| **النقطة الطرفية** | GET /api/v1/users |
| **الأولوية** | عالية 🔴 |
| **النوع** | Functional |

**الطلب:**
```
GET /api/v1/users?page=1&limit=10&sortBy=createdAt&order=desc
Authorization: Bearer {accessToken}
```

**الاستجابة المتوقعة:**
```json
Status: 200 OK
{
  "success": true,
  "data": {
    "users": [
      {
        "userId": "usr_123456",
        "email": "test@example.com",
        "fullName": "أحمد محمد",
        "role": "user",
        "status": "active",
        "createdAt": "2025-01-15T10:30:00Z"
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 5,
      "totalItems": 50,
      "itemsPerPage": 10,
      "hasNext": true,
      "hasPrev": false
    }
  }
}
```

---

#### TC-USR-002: تحديث بيانات المستخدم

| البند | التفاصيل |
|-------|----------|
| **المعرف** | TC-USR-002 |
| **العنوان** | تحديث بيانات المستخدم |
| **النقطة الطرفية** | PUT /api/v1/users/{userId} |
| **الأولوية** | متوسطة 🟡 |
| **النوع** | Functional |

**الطلب:**
```
PUT /api/v1/users/usr_123456
Authorization: Bearer {accessToken}
```

```json
{
  "fullName": "أحمد محمد علي",
  "phone": "+966509876543",
  "bio": "مطور برمجيات سعودي"
}
```

**الاستجابة المتوقعة:**
```json
Status: 200 OK
{
  "success": true,
  "message": "تم تحديث البيانات بنجاح",
  "data": {
    "userId": "usr_123456",
    "email": "test@example.com",
    "fullName": "أحمد محمد علي",
    "phone": "+966509876543",
    "bio": "مطور برمجيات سعودي",
    "updatedAt": "2025-01-15T12:00:00Z"
  }
}
```

---

#### TC-USR-003: حذف المستخدم

| البند | التفاصيل |
|-------|----------|
| **المعرف** | TC-USR-003 |
| **العنوان** | حذف المستخدم |
| **النقطة الطرفية** | DELETE /api/v1/users/{userId} |
| **الأولوية** | عالية 🔴 |
| **النوع** | Destructive |

**الطلب:**
```
DELETE /api/v1/users/usr_123456
Authorization: Bearer {adminAccessToken}
```

**الاستجابة المتوقعة:**
```json
Status: 204 No Content
```

**خطوات التحقق الإضافية:**
1. التأكد من حذف المستخدم من قاعدة البيانات
2. التأكد من عدم إمكانية الدخول بالحساب المحذوف
3. التأكد من حذف البيانات المرتبطة (Soft Delete إن وجد)

---

## ٣. اختبار الأداء (Performance)

### ٣.١ اختبارات الحمل

| المعرف | السيناريو | المستخدمين المتزامنين | المدة | RPS المستهدف |
|--------|-----------|---------------------|-------|-------------|
| PERF-001 | تسجيل دخول | ١٠٠ | ٥ دقائق | ٥٠ |
| PERF-002 | جلب بيانات | ٢٠٠ | ١٠ دقائق | ١٠٠ |
| PERF-003 | بحث | ١٥٠ | ٥ دقائق | ٧٥ |

### ٣.٢ مقاييس الأداء المقبولة

| المقياس | الهدف | الحد المقبول |
|---------|-------|-------------|
| **زمن الاستجابة المتوسط** | < ٢٠٠ مللي ثانية | < ٥٠٠ مللي ثانية |
| **زمن الاستجابة ٩٥٪** | < ٥٠٠ مللي ثانية | < ١٠٠٠ مللي ثانية |
| **معدل النجاح** | ٩٩.٩٪ | ٩٩٪ |
| **الأخطاء في الثانية** | < ١ | < ٥ |

---

## ٤. اختبار الأمان (Security)

### ٤.١ حالات اختبار الأمان

| المعرف | الاختبار | النوع | الأولوية |
|--------|---------|-------|----------|
| SEC-001 | حقن SQL | Injection | عالية |
| SEC-002 | XSS | Injection | عالية |
| SEC-003 | CSRF | Token Validation | عالية |
| SEC-004 | Rate Limiting | DoS Protection | عالية |
| SEC-005 | JWT Validation | Authentication | عالية |
| SEC-006 | Input Validation | Sanitization | متوسطة |

### ٤.٢ مثال: اختبار Rate Limiting

```
TC-SEC-004: اختبار حد المعدل

الخطوات:
١. إرسال ١٠٠ طلب خلال دقيقة واحدة من نفس IP
٢. التحقق من رفض الطلبات بعد الحد المسموح

الاستجابة المتوقعة بعد تجاوز الحد:
Status: 429 Too Many Requests
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "تجاوزت حد الطلبات المسموح. حاول بعد ٦٠ ثانية",
    "retryAfter": 60
  }
}
```

---

## ٥. أدوات الاختبار

### ٥.١ Postman Collection

```json
{
  "info": {
    "name": "API اختبار - نظام المستخدمين",
    "version": "1.0.0"
  },
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "TC-AUTH-001: تسجيل ناجح",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": "{{baseUrl}}/auth/register",
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"test@example.com\",\n  \"password\": \"Test@123456\"\n}"
            }
          },
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "pm.test('Status is 201', () => pm.response.to.have.status(201));",
                  "pm.test('Success is true', () => pm.expect(pm.response.json().success).to.be.true);"
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}
```

### ٥.٢ اختبار آلي بـ Jest

```javascript
describe('API اختبار - المصادقة', () => {
  
  test('TC-AUTH-001: تسجيل مستخدم جديد بنجاح', async () => {
    const response = await request(app)
      .post('/api/v1/auth/register')
      .send({
        email: 'test@example.com',
        password: 'Test@123456',
        fullName: 'أحمد محمد',
        phone: '+966501234567'
      });
    
    expect(response.status).toBe(201);
    expect(response.body.success).toBe(true);
    expect(response.body.data).toHaveProperty('userId');
    expect(response.body.data.email).toBe('test@example.com');
  });
  
  test('TC-AUTH-002: تسجيل ببريد مكرر', async () => {
    // أولاً نسجل مستخدم
    await registerUser('existing@example.com');
    
    // نحاول تسجيل نفس البريد
    const response = await request(app)
      .post('/api/v1/auth/register')
      .send({
        email: 'existing@example.com',
        password: 'Test@123456'
      });
    
    expect(response.status).toBe(409);
    expect(response.body.error.code).toBe('EMAIL_EXISTS');
  });
  
});
```

---

## ٦. تقارير الاختبار

### ٦.١ قالب تقرير الاختبار

```
# تقرير اختبار API

## معلومات التقرير

| البند | التفاصيل |
|-------|----------|
| **اسم الـ API** | نظام إدارة المستخدمين |
| **الإصدار** | v1.0.0 |
| **تاريخ الاختبار** | ١٥/٠٧/١٤٤٧هـ |
| **المختبِر** | فريق الجودة |
| **البيئة** | Staging |

## ملخص النتائج

| الحالة | العدد | النسبة |
|--------|-------|--------|
| ✅ نجح | ٤٥ | ٩٠٪ |
| ❌ فشل | ٣ | ٦٪ |
| ⚠️ تحذير | ٢ | ٤٪ |
| **المجموع** | **٥٠** | **١٠٠٪** |

## الأخطاء المكتشفة

| # | المعرف | العنوان | الأولوية | الحالة |
|---|--------|---------|----------|--------|
| ١ | BUG-001 | رسالة الخطأ بالإنجليزية بدلاً من العربية | عالية | مفتوح |
| ٢ | BUG-002 | زمن استجابة بطيء في جلب القائمة | متوسطة | قيد المعالجة |
| ٣ | BUG-003 | عدم وجود Validation للرقم الهاتفي | منخفضة | مفتوح |

## التوصيات

١. تعريب جميع رسائل الأخطاء
٢. تحسين أداء نقطة endpoint جلب القائمة
٣. إضافة validation إضافي للرقم الهاتفي

## الاعتماد

☐ مقبول للإنتاج
☐ مقبول بشروط (معالجة الأخطاء العالية)
☐ مرفوض - يحتاج إصلاح

التوقيع: _______________
```

---

## ٧. مسرد المصطلحات

| English | العربية |
|---------|---------|
| API | واجهة البرمجة |
| Endpoint | النقطة الطرفية |
| Request | الطلب |
| Response | الاستجابة |
| Authentication | المصادقة |
| Authorization | التفويض |
| Token | رمز |
| Payload | الحمولة |
| Header | الترويسة |
| Query Parameter | معامل الاستعلام |
| Path Parameter | معامل المسار |
| Status Code | كود الحالة |
| Test Case | حالة الاختبار |
| Test Suite | مجموعة الاختبارات |

---

## المراجع

- OWASP API Security Top 10
- Postman API Testing Best Practices
- REST API Testing Guidelines

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
```

---

## الكلمات المفتاحية

### العربية:
- "اختبار API"
- "توثيق اختبار"
- "حالات اختبار"
- "تقرير أخطاء"
- "QA عربي"

### English:
- "API testing arabic"
- "test cases arabic"
- "QA documentation arabic"
- "API test plan"
- "bug report arabic"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
