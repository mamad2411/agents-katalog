---
name: arabic-microservices
name_ar: الخدمات المصغرة
description: Design microservices architecture in Arabic
description_ar: تصميم هندسة الخدمات المصغرة بالعربية
category: developer
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

تصميم وبناء أنظمة Microservices باللغة العربية.

## المفاهيم

| المصطلح | العربية |
|---------|---------|
| Microservice | الخدمة المصغرة |
| Monolith | الأحادي |
| Service Discovery | اكتشاف الخدمات |
| API Gateway | بوابة API |
| Circuit Breaker | قاطع الدائرة |
| Event Bus | ناقل الأحداث |

## المبادئ

1. **خدمة واحدة = مسؤولية واحدة**
2. **استقلالية الخدمات**
3. **لامركزية البيانات**
4. **الفشل المعزول**
5. **التوسع المستقل**

## هيكل النظام

```
┌─────────────┐
│ API Gateway │
└──────┬──────┘
       │
┌──────┼──────┬──────────┐
│      │      │          │
▼      ▼      ▼          ▼
┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
│Users│ │Orders│ │Products│ │Payments│
└─────┘ └─────┘ └─────┘ └─────┘
       │      │      │          │
       └──────┴──────┴──────────┘
                  │
            ┌─────▼─────┐
            │ Event Bus │
            └───────────┘
```

## التواصل بين الخدمات

### متزامن (HTTP/REST)
```
Service A → HTTP → Service B
```

### غير متزامن (Events)
```
Service A → Event → Service B receives
```

## أفضل الممارسات

✅ حدود واضحة للخدمات
✅ قاعدة بيانات لكل خدمة
✅ API Gateway مركزي
✅ Circuit Breaker
✅ Centralized Logging
✅ Distributed Tracing

❌ تجنب耦合 الشديد
❌ لا قاعدة بيانات مشتركة
❌ لا استدعاءات متسلسلة طويلة

---

## الكلمات المفتاحية

عربي: "خدمات مصغرة", "مايكروسيرفيس", "هندسة"
English: "microservices arabic", "architecture", "distributed systems"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
