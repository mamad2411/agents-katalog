---
name: arabic-db-schema
name_ar: مخطط قاعدة البيانات
description: Document database schemas in Arabic with table relationships and descriptions
description_ar: توثيق مخططات قواعد البيانات بالعربية مع علاقات الجداول والأوصاف
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

**English**: Document database schemas in Arabic with detailed table descriptions, column definitions, relationships, and constraints.

**العربية**: توثيق مخططات قواعد البيانات بالعربية مع أوصاف تفصيلية للجداول وتعريفات الأعمدة والعلاقات والقيود.

---

## When to Use | متى تستخدم هذه المهارة

**English**: Use this skill when you need to:
- Document existing database schemas
- Create Arabic database documentation
- Design new database structures
- Share schema with Arabic-speaking team

**العربية**: استخدم هذه المهارة عندما تحتاج إلى:
- توثيق مخططات قواعد البيانات الموجودة
- إنشاء توثيق عربي لقواعد البيانات
- تصميم هياكل قواعد بيانات جديدة
- مشاركة المخطط مع فريق ناطق بالعربية

---

## Output Format | صيغة المخرجات

```markdown
# مخطط قاعدة البيانات | Database Schema

## قاعدة البيانات: نظام إدارة المستخدمين

### ١. جدول: users (المستخدمين)

| العمود | النوع | القيود | الوصف |
|--------|-------|--------|-------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | المعرف الفريد |
| username | VARCHAR(50) | NOT NULL, UNIQUE | اسم المستخدم |
| email | VARCHAR(100) | NOT NULL, UNIQUE | البريد الإلكتروني |
| password_hash | VARCHAR(255) | NOT NULL | كلمة المرور المشفرة |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | تاريخ آخر تحديث |

**الوصف**: يخزن معلومات حسابات المستخدمين الأساسية.

### ٢. جدول: profiles (الملفات الشخصية)

| العمود | النوع | القيود | الوصف |
|--------|-------|--------|-------|
| id | INT | PRIMARY KEY | المعرف الفريد |
| user_id | INT | FOREIGN KEY → users.id | معرف المستخدم |
| first_name | VARCHAR(50) | | الاسم الأول |
| last_name | VARCHAR(50) | | اسم العائلة |
| phone | VARCHAR(20) | | رقم الهاتف |
| bio | TEXT | | نبذة تعريفية |

**الوصف**: يخزن المعلومات الشخصية الإضافية للمستخدمين.

### العلاقات | Relationships

```
users (1) ←→ (1) profiles
users (1) ←→ (many) posts
users (many) ←→ (many) roles (via user_roles)
```

### ٣. جدول: posts (المقالات)

| العمود | النوع | القيود | الوصف |
|--------|-------|--------|-------|
| id | INT | PRIMARY KEY | المعرف الفريد |
| user_id | INT | FOREIGN KEY → users.id | كاتب المقال |
| title | VARCHAR(200) | NOT NULL | عنوان المقال |
| content | TEXT | NOT NULL | محتوى المقال |
| status | ENUM | ('draft','published') | حالة النشر |
| published_at | TIMESTAMP | | تاريخ النشر |

**الوصف**: يخزن مقالات المستخدمين المنشورة والمسودات.

### الفهارس | Indexes

| الجدول | العمود | النوع |
|--------|--------|-------|
| users | email | UNIQUE |
| users | username | UNIQUE |
| posts | user_id | NORMAL |
| posts | status | NORMAL |
```

---

## Trigger Keywords | الكلمات المفتاحية

### Arabic Keywords | الكلمات العربية
- "مخطط قاعدة بيانات"
- "توثيق database"
- "ERD عربي"
- "جداول قاعدة البيانات"
- "علاقات جداول"

### English Keywords | الكلمات الإنجليزية
- "arabic database schema"
- "database documentation arabic"
- "arabic erd"
- "database design arabic"
- "arabic db docs"

---

## Changelog | سجل التغييرات

### v1.0.0
- Initial release
