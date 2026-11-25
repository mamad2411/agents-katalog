---
name: arabic-ci-cd
name_ar: خط الأنابيب المستمر
description: Build CI/CD pipelines in Arabic
description_ar: بناء خطوط الأنابيب المستمرة بالعربية
category: developer
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

بناء خطوط CI/CD باللغة العربية للنشر المستمر.

## المفاهيم

| المصطلح | العربية |
|---------|---------|
| CI | التكامل المستمر |
| CD | النشر المستمر |
| Pipeline | خط الأنابيب |
| Stage | المرحلة |
| Job | المهمة |
| Artifact | المخرجات |

## GitHub Actions مثال

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm test
    
    - name: Build
      run: npm run build
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: build
        path: dist/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
        # أضف أوامر النشر هنا
```

## مراحل خط الأنابيب

1. **Build** - البناء
2. **Test** - الاختبار
3. **Security Scan** - فحص الأمان
4. **Deploy Staging** - نشر تجريبي
5. **Deploy Production** - نشر إنتاجي

## أفضل الممارسات

✅ اختبارات سريعة
✅ فشل مبكر
✅ بيئة مماثلة للإنتاج
✅ مراجعة قبل النشر
✅ تراجع آلي

---

## الكلمات المفتاحية

عربي: "CI/CD", "نشر مستمر", "أتمتة"
English: "CI/CD arabic", "devops pipeline", "github actions"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
