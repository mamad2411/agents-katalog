---
name: arabic-python-basics
name_ar: أساسيات بايثون
description: Python programming basics in Arabic
description_ar: أساسيات برمجة بايثون بالعربية
category: developer
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

تعلم أساسيات لغة Python باللغة العربية.

## المتغيرات وأنواع البيانات

```python
# متغيرات
name = "أحمد"
age = ٢٥
height = ١.٧٥
is_student = True

# أنواع بيانات
print(type(name))    # <class 'str'>
print(type(age))     # <class 'int'>
print(type(height))  # <class 'float'>
print(type(is_student))  # <class 'bool'>
```

## الهياكل

### القوائم (Lists)

```python
fruits = ["تفاح", "موز", "برتقال"]

# إضافة
fruits.append("عنب")

# وصول
print(fruits[٠])  # تفاح

# تكرار
for fruit in fruits:
    print(fruit)
```

### القواميس (Dictionaries)

```python
person = {
    "name": "أحمد",
    "age": ٢٥,
    "city": "الرياض"
}

# وصول
print(person["name"])

# إضافة
person["job"] = "مهندس"

# تكرار
for key, value in person.items():
    print(f"{key}: {value}")
```

## الشروط

```python
grade = ٨٥

if grade >= ٩٠:
    print("ممتاز")
elif grade >= ٨٠:
    print("جيد جداً")
elif grade >= ٧٠:
    print("جيد")
else:
    print("مقبول")
```

## الحلقات

### حلقة for

```python
# تكرار على قائمة
for i in range(٥):
    print(f"الرقم: {i}")

# مع enumerate
for index, value in enumerate(fruits):
    print(f"{index}: {value}")
```

### حلقة while

```python
count = ٠
while count < ٥:
    print(count)
    count += ١
```

## الدوال

```python
def greet(name):
    return f"مرحباً {name}!"

# استدعاء
message = greet("أحمد")
print(message)  # مرحباً أحمد!

# مع قيم افتراضية
def greet(name="ضيف"):
    return f"مرحباً {name}!"
```

## أفضل الممارسات

✅ استخدم أسماء واضحة
✅ اكتب تعليقات
✅ اتبع PEP 8
✅ اختبر الكود
✅ أعد استخدام الكود

❌ لا تستخدم أسماء غامضة
❌ لا تكرر الكود
❌ لا تهمل الأخطاء
❌ لا تكتب دوال طويلة

---

## الكلمات المفتاحية

عربي: "بايثون", "برمجة", "Python", "كود"
English: "python arabic", "programming", "coding"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
