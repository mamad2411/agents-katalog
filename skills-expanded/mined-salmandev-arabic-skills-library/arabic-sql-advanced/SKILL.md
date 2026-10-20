---
name: arabic-sql-advanced
name_ar: إس كيو إل متقدم
description: Master advanced SQL in Arabic
description_ar: إتقان إس كيو إل متقدم بالعربية
category: data-science
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

إتقان تقنيات SQL المتقدمة للتعامل مع بيانات معقدة.

## استعلامات متقدمة

### ١. Window Functions

```sql
-- ترتيب مع تقسيم
SELECT 
    name,
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;

-- متوسط متحرك
SELECT 
    date,
    sales,
    AVG(sales) OVER (ORDER BY date ROWS 6 PRECEDING) as moving_avg
FROM daily_sales;
```

### ٢. Common Table Expressions (CTE)

```sql
WITH sales_summary AS (
    SELECT 
        region,
        SUM(amount) as total_sales
    FROM sales
    GROUP BY region
)
SELECT * FROM sales_summary
WHERE total_sales > 100000;
```

### ٣. Pivot Tables

```sql
SELECT * FROM (
    SELECT product, quarter, revenue
    FROM sales_data
) AS source
PIOT (
    SUM(revenue)
    FOR quarter IN (Q1, Q2, Q3, Q4)
) AS pivot_table;
```

## تحسين استعلامات

| التقنية | الوصف |
|---------|-------|
| **Indexes** | تسريع بحث |
| **Query Plan** | تحليل أداء |
| **Partitioning** | تقسيم جداول |
| **Caching** | تخزين مؤقت |

## أفضل الممارسات

✅ استخدم Indexes صحيحة
✅ تجنب SELECT *
✅ حلل Query Plan
✅ حدّث Statistics

❌ لا تهمل Performance
❌ لا تبالغ في Joins
❌ لا تهمل Security

---

## الكلمات المفتاحية

عربي: "SQL متقدم", "advanced SQL", "قواعد بيانات", "window functions"
English: "advanced SQL arabic", "SQL", "database", "window functions", "CTE"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
