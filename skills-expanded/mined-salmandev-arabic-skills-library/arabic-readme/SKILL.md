---
name: arabic-readme
name_ar: ملف README عربي
description: Generate bilingual README files for GitHub repositories
description_ar: إنشاء ملفات README ثنائية اللغة لمستودعات GitHub
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

**English**: Generate professional bilingual README files for GitHub repositories with Arabic and English content, proper formatting, and all essential sections.

**العربية**: إنشاء ملفات README احترافية ثنائية اللغة لمستودعات GitHub بمحتوى عربي وإنجليزي وتنسيق صحيح وجميع الأقسام الأساسية.

---

## When to Use | متى تستخدم هذه المهارة

**English**: Use this skill when you need to:
- Create a new GitHub repository README
- Add Arabic documentation to a project
- Make your project accessible to Arabic developers
- Create bilingual project documentation

**العربية**: استخدم هذه المهارة عندما تحتاج إلى:
- إنشاء README لمستودع GitHub جديد
- إضافة توثيق عربي لمشروع
- جعل مشروعك متاحاً للمطورين العرب
- إنشاء توثيق مشروع ثنائي اللغة

---

## Model Instructions | تعليمات النموذج

### English Instructions

You are a technical writer specializing in open-source documentation. When creating READMEs:

1. **Essential Sections**:
   - Project Title & Description
   - Features
   - Installation
   - Usage
   - Contributing
   - License

2. **Bilingual Format**:
   - English section first
   - Arabic section parallel
   - Consistent structure

3. **Technical Details**:
   - Code examples
   - Commands in English
   - Screenshots placeholders

### التعليمات بالعربية

أنت كاتب تقني متخصص في توثيق المصادر المفتوحة. عند إنشاء README:

١. **الأقسام الأساسية**:
   - عنوان ووصف المشروع
   - المميزات
   - التثبيت
   - الاستخدام
   - المساهمة
   - الترخيص

٢. **التنسيق ثنائي اللغة**:
   - القسم الإنجليزي أولاً
   - القسم العربي بالتوازي
   - هيكل متسق

٣. **التفاصيل التقنية**:
   - أمثلة الكود
   - الأوامر بالإنجليزية
   - أماكن للصور

---

## Output Format | صيغة المخرجات

```markdown
# Project Name | اسم المشروع

> Description in English
> الوصف بالعربية

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Arabic](https://img.shields.io/badge/Arabic-Support-green.svg)](README.ar.md)

---

## Table of Contents | المحتويات

- [About](#about--عن-المشروع)
- [Features](#features--المميزات)
- [Installation](#installation--التثبيت)
- [Usage](#usage--الاستخدام)
- [Contributing](#contributing--المساهمة)
- [License](#license--الترخيص)

---

## About | عن المشروع

**English**: Brief description of what the project does and why it exists.

**العربية**: وصف موجز لما يفعله المشروع ولماذا وُجد.

---

## Features | المميزات

- Feature 1 | الميزة ١
- Feature 2 | الميزة ٢
- Feature 3 | الميزة ٣

---

## Installation | التثبيت

```bash
# Clone the repository
git clone https://github.com/username/project.git

# Install dependencies
npm install

# Run the project
npm start
```

---

## Usage | الاستخدام

```javascript
// Example code
const project = require('project');
project.init();
```

---

## Contributing | المساهمة

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

المساهمات مرحب بها! يرجى قراءة [CONTRIBUTING.md](CONTRIBUTING.md) أولاً.

---

## License | الترخيص

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

هذا المشروع مرخص بموجب ترخيص MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

---

## Contact | التواصل

- GitHub: [@username](https://github.com/username)
- Email: email@example.com

```

---

## Trigger Keywords | الكلمات المفتاحية

### Arabic Keywords | الكلمات العربية
- "README عربي"
- "توثيق مشروع"
- "ملف README"
- "توثيق GitHub"
- "README ثنائي اللغة"

### English Keywords | الكلمات الإنجليزية
- "arabic readme"
- "bilingual readme"
- "arabic documentation"
- "github readme arabic"
- "arabic project docs"

---

## Changelog | سجل التغييرات

### v1.0.0
- Initial release
