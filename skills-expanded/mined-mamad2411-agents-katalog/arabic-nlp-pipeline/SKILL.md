---
name: arabic-nlp-pipeline
name_ar: خط معالجة اللغة الطبيعية
description: Build Arabic NLP preprocessing pipelines with comprehensive documentation
description_ar: بناء خطوط معالجة اللغة الطبيعية العربية مع توثيق شامل
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

يساعد هذه المهارة في بناء خطوط معالجة اللغة الطبيعية (NLP Pipelines) للغة العربية مع توثيق شامل، يتضمن التطبيع، التجزئة (Tokenization)، إزالة stopwords، والتشكيل، مع دعم اللهجات العربية المختلفة.

---

## متى تستخدم هذه المهارة (When to Use)

استخدم هذه المهارة عندما تحتاج إلى:

- معالجة نصوص عربية قبل التحليل
- إعداد بيانات لنماذج NLP
- تطبيع النصوص العربية
- تجزئة النصوص العربية (Tokenization)
- دعم لهجات عربية متعددة

---

## تعليمات النموذج (Model Instructions)

أنت مهندس NLP محترف. عند بناء خط المعالجة:

### مكونات خط المعالجة

١. **التنظيف (Cleaning)**
٢. **التطبيع (Normalization)**
٣. **التشكيل (Diacritization)**
٤. **التجزئة (Tokenization)**
٥. **إزالة stopwords**
٦. **التجذيع (Stemming/Lemmatization)**

---

## مثال (Example)

**الطلب:**
```
أعد خط معالجة NLP لنصوص عربية.
```

**النتيجة المتوقعة:**
```
# خط معالجة اللغة الطبيعية العربية

## Arabic NLP Preprocessing Pipeline

---

## ١. نظرة عامة

### ١.١ المكونات

```
النص الخام → تنظيف → تطبيع → تشكيل (اختياري) → تجزئة → إزالة stopwords → تجذيع → نص معالج
```

### ١.٢ الميزات

- ✅ دعم الفصحى واللهجات
- ✅ معالجة الأرقام العربية
- ✅ التعامل مع الإيموجي
- ✅ كشف اللغة واللهجة
- ✅ سرعة عالية (١٠٠٠ نص/ثانية)

---

## ٢. التطبيع (Normalization)

### ٢.١ قواعد التطبيع

| النوع | من | إلى | المثال |
|-------|----|-----|--------|
| الألف | أ، إ، آ | ا | أحمد → احمد |
| الياء | ى | ي | كتابى → كتابي |
| التاء المربوطة | ة | ه | سيارة → سياره |
| الألف المقصورة | ى | ي | فتى → فتي |
| اللام | ﻻ | لا | ﻻ → لا |

### ٢.٢ الكود

```python
import re

def normalize_arabic(text):
    # تطبيع الألف
    text = re.sub(r'[أإآ]', 'ا', text)
    # تطبيع الياء
    text = re.sub(r'[ى]', 'ي', text)
    # تطبيع التاء المربوطة
    text = re.sub(r'[ة]', 'ه', text)
    # تطبيع اللام ألف
    text = re.sub(r'ﻻ', 'لا', text)
    return text
```

---

## ٣. التنظيف (Cleaning)

### ٣.١ عناصر التنظيف

| العنصر | الإزالة | الاستثناء |
|--------|---------|-----------|
| روابط HTTP | ✅ | لا |
| إشارات @ | ✅ | لا |
| هاشتاج # | ✅ | لا |
| إيموجي | اختياري | تحليل المشاعر |
| تشكيل | اختياري | نصوص دينية |
| مسافات زائدة | ✅ | لا |
| أحرف متكررة | اختياري | تعبير عن عاطفة |

### ٣.٢ الكود

```python
def clean_arabic_text(text, remove_emoji=True, keep_emoji_for_sentiment=False):
    # إزالة الروابط
    text = re.sub(r'http\S+|www\S+', '', text)
    # إزالة الإشارات
    text = re.sub(r'@\w+', '', text)
    # إزالة الهاشتاج (مع الاحتفاظ بالنص)
    text = re.sub(r'#(\w+)', r'\1', text)
    # إزالة الإيموجي
    if remove_emoji:
        text = remove_emojis(text)
    # إزالة التشكيل
    text = remove_tashkeel(text)
    # تطبيع المسافات
    text = normalize_whitespace(text)
    return text
```

---

## ٤. التجزئة (Tokenization)

### ٤.١ طرق التجزئة

| الطريقة | الوصف | الاستخدام |
|---------|-------|----------|
| **بالمسافات** | تقسيم على المسافات | بسيط، سريع |
| **CAMeL Tools** | أداة متخصصة | بحثي، دقيق |
| **Moses Tokenizer** | معياري | مقارنة |
| **Subword (BPE)** | تحت-كلمة | نماذج Transformer |

### ٤.٢ الكود

```python
from camel_tools.tokenizers.word import simple_word_tokenize

def tokenize_arabic(text, method='camel'):
    if method == 'camel':
        return simple_word_tokenize(text)
    elif method == 'simple':
        return text.split()
    elif method == 'bert':
        # استخدام BertTokenizer
        tokenizer = BertTokenizer.from_pretrained('aubmindlab/bert-base-arabert')
        return tokenizer.tokenize(text)
```

---

## ٥. إزالة كلمات التوقف (Stopwords)

### ٥.١ قائمة stopwords

```python
ARABIC_STOPWORDS = [
    'من', 'على', 'في', 'إلى', 'عن', 'مع',
    'هذا', 'هذه', 'ذلك', 'تلك',
    'التي', 'الذي', 'الذين', 'اللواتي',
    'كان', 'كانت', 'يكون', 'تكون',
    'قد', 'لن', 'لا', 'لم', 'لما',
    'ما', 'من', 'منه', 'منها',
    'به', 'بها', 'هم', 'هن',
    # ... ٥٠٠+ كلمة
]
```

### ٥.٢ الكود

```python
def remove_stopwords(tokens, custom_stopwords=None):
    stopwords = set(ARABIC_STOPWORDS)
    if custom_stopwords:
        stopwords.update(custom_stopwords)
    return [t for t in tokens if t not in stopwords]
```

---

## ٦. التجذيع (Stemming/Lemmatization)

### ٦.١ الجذاعة vs اللممة

| النوع | الوصف | مثال |
|-------|-------|------|
| **Stemming** | إزالة اللواحق والزوائد | "ويكتبون" → "كتب" |
| **Lemmatization** | إرجاع للأصل المعجمي | "ويكتبون" → "كتب" (فعل) |

### ٦.٢ الكود

```python
from camel_tools.morphology import analyzer

def lemmatize_arabic(tokens):
    lemmas = []
    for token in tokens:
        # استخدام CAMeL Tools لللممة
        analysis = analyzer.analyze(token)
        if analysis:
            lemmas.append(analysis[0].lemma)
        else:
            lemmas.append(token)
    return lemmas
```

---

## ٧. خط المعالجة الكامل

### ٧.١ الكود الكامل

```python
class ArabicNLPipeline:
    def __init__(self, config=None):
        self.config = config or {
            'normalize': True,
            'clean': True,
            'remove_tashkeel': True,
            'remove_stopwords': True,
            'lemmatize': False,
            'dialect': 'all'
        }
    
    def process(self, text):
        if self.config['clean']:
            text = clean_arabic_text(text)
        if self.config['normalize']:
            text = normalize_arabic(text)
        if self.config['remove_tashkeel']:
            text = remove_tashkeel(text)
        
        tokens = tokenize_arabic(text)
        
        if self.config['remove_stopwords']:
            tokens = remove_stopwords(tokens)
        
        if self.config['lemmatize']:
            tokens = lemmatize_arabic(tokens)
        
        return tokens
    
    def process_batch(self, texts):
        return [self.process(t) for t in texts]
```

### ٧.٢ مثال الاستخدام

```python
# تهيئة الخط
pipeline = ArabicNLPipeline(config={
    'normalize': True,
    'clean': True,
    'remove_stopwords': True,
    'lemmatize': True
})

# معالجة نص
text = "وَقَالَ الرَّجُلُ يَا رَبِّ إِنَّ هَؤُلَاءِ قَوْمٌ لَّا يُؤْمِنُونَ"
tokens = pipeline.process(text)
print(tokens)
# ['قال', 'رجل', 'رب', 'إن', 'هؤلاء', 'قوم', 'لم', 'يؤمن']
```

---

## ٨. دعم اللهجات

### ٨.١ اللهجات المدعومة

| اللهجة | الحالة | الميزات |
|--------|--------|---------|
| **مصرية** | ✅ كامل | تطبيع، تجزئة |
| **خليجي** | ✅ كامل | تطبيع، تجزئة |
| **شامية** | ✅ كامل | تطبيع، تجزئة |
| **مغاربية** | 🟡 جزئي | تطبيع أساسي |
| **عراقية** | 🟡 جزئي | تطبيع أساسي |

### ٨.٢ كشف اللهجة

```python
def detect_dialect(text):
    egyptian_markers = ['إيه', 'أوي', 'خلاص', 'دلوقتي']
    gulf_markers = ['يا هلا', 'بخير', 'شلون', 'الحين']
    levantines_markers = ['شو', 'هلق', 'أبدا', 'كتير']
    
    score = {'egyptian': 0, 'gulf': 0, 'levantine': 0}
    
    for marker in egyptian_markers:
        if marker in text:
            score['egyptian'] += 1
    # ... بقية اللهجات
    
    return max(score, key=score.get)
```

---

## ٩. الأداء

### ٩.١ مقاييس الأداء

| المقياس | القيمة |
|---------|--------|
| سرعة المعالجة | ١٠٠٠ نص/ثانية |
| دقة التجزئة | ٩٦.٥٪ |
| دقة اللممة | ٩٢.٠٪ |
| استخدام الذاكرة | ٢٠٠ ميجابايت |

### ٩.٢ التحسينات

- معالجة متوازية (Multiprocessing)
- Caching للنتائج
- استخدام GPU للتشكيل

---

## ١٠. التوثيق

### ١٠.١ API Reference

```python
"""
ArabicNLPipeline - خط معالجة اللغة الطبيعية العربية

Parameters:
    config (dict): إعدادات الخط
        - normalize (bool): تطبيع النص
        - clean (bool): تنظيف النص
        - remove_tashkeel (bool): إزالة التشكيل
        - remove_stopwords (bool): إزالة كلمات التوقف
        - lemmatize (bool): لممة الكلمات
        - dialect (str): اللهجة المستهدفة

Returns:
    list: قائمةtokens المعالجة

Example:
    >>> pipeline = ArabicNLPipeline()
    >>> tokens = pipeline.process("مرحباً بالعالم")
    >>> print(tokens)
    ['مرحب', 'عالم']
"""
```

---

## المراجع

- CAMeL Tools Documentation
- Arabic NLP Guide (Hugging Face)
- Stanford Arabic NLP

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي

```

---

## الكلمات المفتاحية

### العربية:
- "معالجة NLP عربية"
- "تطبيع نص عربي"
- "تجزئة عربية"
- "خط معالجة NLP"
- "تجذيع عربي"

### English:
- "arabic NLP pipeline"
- "arabic text preprocessing"
- "arabic tokenization"
- "arabic stemming"
- "arabic lemmatization"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
