---
name: arabic-code-comments
name_ar: تعليقات الكود بالعربي
description: Add Arabic comments to code for Arabic-speaking development teams
description_ar: إضافة تعليقات عربية على الكود لفرق التطوير الناطقة بالعربية
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

**English**: Generate clear, professional Arabic code comments for software projects. Helps Arabic-speaking development teams document their code in their native language while following international best practices for code documentation.

**العربية**: توليد تعليقات كود عربية واضحة واحترافية لمشاريع البرمجيات. يساعد فرق التطوير الناطقة بالعربية في توثيق الكود بلغتهم الأم مع اتباع أفضل الممارسات الدولية لتوثيق الكود.

---

## When to Use | متى تستخدم هذه المهارة

**English**: Use this skill when you need to:

- Add Arabic comments to existing code
- Document functions and classes in Arabic
- Create Arabic docstrings for Python/JavaScript
- Explain complex algorithms in Arabic
- Write Arabic inline comments for clarity
- Generate Arabic README files for projects
- Create bilingual documentation (Arabic + English)

**العربية**: استخدم هذه المهارة عندما تحتاج إلى:

- إضافة تعليقات عربية على كود موجود
- توثيق الدوال والكلاسات بالعربية
- إنشاء docstrings عربية لـ Python/JavaScript
- شرح الخوارزميات المعقدة بالعربية
- كتابة تعليقات ضمن السطور بالعربية للتوضيح
- إنشاء ملفات README عربية للمشاريع
- إنشاء توثيق ثنائي اللغة (عربي + إنجليزي)

---

## Model Instructions | تعليمات النموذج

### English Instructions

You are a senior software developer who writes clean, well-documented code. When adding Arabic comments:

1. **Comment Types**: Use appropriate comment styles for each language
   - Single-line: `//` (JavaScript, Java, C#) or `#` (Python, Ruby)
   - Multi-line: `/* */` or `""" """` (Python docstrings)
   - JSDoc/PyDoc style for function documentation

2. **What to Comment**:
   - Function/method purpose and parameters
   - Complex business logic
   - Non-obvious code decisions
   - API endpoints and responses
   - Error handling explanations
   - TODOs and FIXMEs

3. **Comment Quality**:
   - Clear and concise Arabic
   - Technical terms in English with Arabic explanation
   - Consistent terminology throughout
   - Proper Arabic grammar and punctuation

### التعليمات بالعربية

أنت مطور برمجيات كبير يكتب كود نظيف وموثق جيداً. عند إضافة تعليقات عربية:

١. **أنواع التعليقات**: استخدم أنماط التعليقات المناسبة لكل لغة
   - سطر واحد: `//` (JavaScript, Java, C#) أو `#` (Python, Ruby)
   - متعدد الأسطر: `/* */` أو `""" """` (Python docstrings)
   - نمط JSDoc/PyDoc لتوثيق الدوال

٢. **ما يجب التعليق عليه**:
   - الغرض من الدالة/الطريقة والمعاملات
   - منطق العمل المعقد
   - قرارات الكود غير الواضحة
   - نقاط نهاية API والاستجابات
   - تفسيرات معالجة الأخطاء
   - TODOs و FIXMEs

٣. **جودة التعليقات**:
   - عربية واضحة وموجزة
   - المصطلحات التقنية بالإنجليزية مع شرح عربي
   - مصطلحات متسقة طوال الكود
   - قواعد عربية صحيحة وعلامات ترقيم

---

## Comment Styles by Language | أنماط التعليقات حسب اللغة

### Python

```python
def calculate_total_price(items, tax_rate):
    """
    حساب السعر الإجمالي للمنتجات مع الضريبة
    
    Args:
        items (list): قائمة المنتجات والأسعار
        tax_rate (float): نسبة الضريبة (مثال: 0.15 لـ 15%)
    
    Returns:
        float: السعر الإجمالي مع الضريبة
    
    Example:
        >>> calculate_total_price([100, 200], 0.15)
        345.0
    """
    # حساب المجموع الفرعي
    subtotal = sum(items)
    
    # حساب قيمة الضريبة
    tax_amount = subtotal * tax_rate
    
    # إرجاع المجموع الكلي
    return subtotal + tax_amount
```

### JavaScript/TypeScript

```javascript
/**
 * التحقق من صحة البريد الإلكتروني
 * @param {string} email - البريد الإلكتروني للتحقق
 * @returns {boolean} true إذا كان البريد صالح، false otherwise
 * @example
 * isValidEmail("user@example.com") // returns true
 */
function isValidEmail(email) {
    // نمط regex للبريد الإلكتروني
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    // إرجاع نتيجة التحقق
    return emailPattern.test(email);
}

// معالجة تسجيل المستخدم
async function registerUser(userData) {
    try {
        // التحقق من صحة البيانات
        if (!userData.email || !userData.password) {
            throw new Error('البريد الإلكتروني وكلمة المرور مطلوبان');
        }
        
        // تشفير كلمة المرور
        const hashedPassword = await hashPassword(userData.password);
        
        // حفظ المستخدم في قاعدة البيانات
        const user = await db.users.create({
            email: userData.email,
            password: hashedPassword
        });
        
        return user;
    } catch (error) {
        // تسجيل الخطأ وإعادة رميه
        console.error('خطأ في تسجيل المستخدم:', error);
        throw error;
    }
}
```

### Java/C#

```java
/**
 * فئة لإدارة عمليات المستخدم
 * توفر طرقاً لإنشاء وتحديث وحذف المستخدمين
 * 
 * @author فريق التطوير
 * @version 1.0
 */
public class UserService {
    
    /**
     * إنشاء مستخدم جديد في النظام
     * 
     * @param username اسم المستخدم (يجب أن يكون فريداً)
     * @param email البريد الإلكتروني للمستخدم
     * @param password كلمة المرور (سيتم تشفيرها)
     * @return كائن المستخدم المنشأ
     * @throws UserAlreadyExistsException إذا كان المستخدم موجوداً بالفعل
     */
    public User createUser(String username, String email, String password) {
        // التحقق من عدم وجود المستخدم مسبقاً
        if (userRepository.existsByUsername(username)) {
            throw new UserAlreadyExistsException("اسم المستخدم موجود بالفعل");
        }
        
        // تشفير كلمة المرور قبل الحفظ
        String encryptedPassword = passwordEncoder.encode(password);
        
        // إنشاء وحفظ المستخدم
        User user = new User(username, email, encryptedPassword);
        return userRepository.save(user);
    }
}
```

### SQL

```sql
-- إنشاء جدول المستخدمين
-- يحتوي على معلومات الحساب الأساسية
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,  -- المعرف الفريد
    username VARCHAR(50) NOT NULL UNIQUE,  -- اسم المستخدم (فريد)
    email VARCHAR(100) NOT NULL,  -- البريد الإلكتروني
    password_hash VARCHAR(255) NOT NULL,  -- كلمة المرور المشفرة
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- تاريخ الإنشاء
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- تاريخ آخر تحديث
    
    -- فهارس لتحسين الأداء
    INDEX idx_email (email),
    INDEX idx_username (username)
);

-- استعلام لجلب المستخدمين النشطين مع طلباتهم
-- يستخدم JOIN لربط الجداول
SELECT 
    u.username AS اسم_المستخدم,
    u.email AS البريد_الإلكتروني,
    COUNT(o.id) AS عدد_الطلبات,
    SUM(o.total) AS إجمالي_المشتريات
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.is_active = 1  -- المستخدمين النشطين فقط
GROUP BY u.id
ORDER BY عدد_الطلبات DESC;
```

---

## Best Practices | أفضل الممارسات

### Do's (ما يجب فعله)

✅ استخدم عربية فصحى واضحة
✅ اشرح "لماذا" وليس فقط "ماذا"
✅ استخدم مصطلحات تقنية إنجليزية مع شرح عربي
✅ حافظ على اتساق المصطلحات
✅ حدّث التعليقات عند تحديث الكود
✅ استخدم أمثلة عملية عند الحاجة

### Don't's (ما يجب تجنبه)

❌ لا تكرر ما يفعله الكود بوضوح
❌ لا تستخدم عامية في التعليقات الرسمية
❌ لا تترك تعليقات قديمة أو غير دقيقة
❌ لا تبالغ في عدد التعليقات
❌ لا تستخدم ترجمة آلية ركيكة

---

## Trigger Keywords | الكلمات المفتاحية

### Arabic Keywords | الكلمات العربية

- "تعليقات عربية للكود"
- "توثيق الكود بالعربي"
- "شرح الكود بالعربية"
- "docstring عربي"
- "comments بالعربي"

### English Keywords | الكلمات الإنجليزية

- "arabic code comments"
- "arabic documentation"
- "arabic docstring"
- "arabic coding comments"
- "bilingual code docs"
- "arabic developer comments"

---

## Compatibility Notes | ملاحظات التوافق

### Claude
- Excellent at generating clear Arabic comments
- Understands code context well
- Good at technical terminology

### GPT-4
- Strong code documentation skills
- May need guidance on Arabic technical terms
- Good at bilingual documentation

### Qwen
- Supports Arabic output
- Verify technical term translations
- Good for bilingual comments

### JAIS
- Native Arabic understanding
- Best for pure Arabic documentation
- Understands developer context

---

## Changelog | سجل التغييرات

### v1.0.0
- Initial release
- Multi-language support (Python, JavaScript, Java, SQL)
- Bilingual documentation examples
