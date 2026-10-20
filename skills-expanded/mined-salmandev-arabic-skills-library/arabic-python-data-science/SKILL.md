---
name: arabic-python-data-science
name_ar: بايثون لعلوم بيانات
description: Master Python for data science in Arabic
description_ar: إتقان بايثون لعلوم البيانات بالعربية
category: developer
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

إتقان استخدام Python في تحليل البيانات وعلوم البيانات.

## مكتبات أساسية

### ١. NumPy

**الاستخدامات:**
- حسابات رقمية
- مصفوفات متعددة الأبعاد
- دوال رياضية

### ٢. Pandas

**الاستخدامات:**
- معالجة بيانات
- DataFrames
- قراءة/كتابة ملفات

### ٣. Matplotlib

**الاستخدامات:**
- رسوم بيانية 2D
- تخصيص رسوم
- تصدير صور

### ٤. Seaborn

**الاستخدامات:**
- رسوم إحصائية
- ألوان جاهزة
- تكامل Pandas

## مثال عملي

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# قراءة بيانات
df = pd.read_csv('data.csv')

# تحليل وصفي
print(df.describe())

# رسم بياني
plt.figure(figsize=(10,6))
plt.plot(df['date'], df['value'])
plt.title('تحليل بيانات')
plt.show()
```

## أفضل الممارسات

✅ توثيق كود
✅ استخدام virtual environments
✅ اختبار كود
✅ تحسين أداء

❌ لا تهمل جودة بيانات
❌ لا تهمل ذاكرة
❌ لا تهمل أخطاء

---

## الكلمات المفتاحية

عربي: "بايثون", "علوم بيانات", "Python", "Data Science", "Pandas"
English: "Python arabic", "data science", "pandas", "numpy", "data analysis"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
