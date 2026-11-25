---
name: arabic-git-workflow
name_ar: سير عمل جيت
description: Master Git workflows and version control in Arabic
description_ar: إتقان سير عمل جيت والتحكم في الإصدارات باللغة العربية
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

يساعد هذه المهارة في إتقان سير عمل Git والتحكم في الإصدارات باللغة العربية، بما في ذلك الفروع، الدمج، إعادة الكتابة، وحل النزاعات، لتسهيل التعاون في فرق التطوير العربية.

---

## متى تستخدم هذه المهارة (When to Use)

استخدم هذه المهارة عندما تحتاج إلى:

- إدارة مستودعات Git بالعربية
- توثيق سير العمل للفريق
- حل نزاعات الدمج
- إعداد استراتيجيات الفروع
- تدريب المطورين على Git

---

## تعليمات النموذج (Model Instructions)

أنت خبير Git وإدارة الإصدارات. عند التوجيه:

### مفاهيم Git الأساسية

١. **المستودع (Repository)**
٢. **الفرع (Branch)**
٣. **الالتزام (Commit)**
٤. **الدمج (Merge)**
٥. **إعادة الكتابة (Rebase)**
٦. **السحب/الدفع (Pull/Push)**

### سير العمل الشائعة

- Git Flow
- GitHub Flow
- GitLab Flow
- Trunk-Based Development

---

## مثال (Example)

**الطلب:**
```
اشرح Git Flow بالعربية.
```

**النتيجة المتوقعة:**
```
# سير عمل Git الشامل

## Complete Git Workflow Guide

---

## ١. المفاهيم الأساسية

### ١.١ المصطلحات الأساسية

| English | العربية | الوصف |
|---------|---------|-------|
| Repository | المستودع | مجلد المشروع مع سجل التغييرات |
| Branch | الفرع | نسخة مستقلة من المشروع |
| Commit | الالتزام | حفظ التغييرات في السجل |
| Merge | الدمج | دمج فرعين معاً |
| Rebase | إعادة الكتابة | نقل فرع لنقطة بداية جديدة |
| Pull Request | طلب السحب | طلب دمج التغييرات |
| Conflict | نزاع | تعارض في التغييرات |

### ١.٢ إعداد Git

```bash
# إعداد المستخدم
git config --global user.name "أحمد محمد"
git config --global user.email "ahmed@example.com"
git config --global language arabic

# إعداد المحرر
git config --global core.editor "code --wait"

# عرض الإعدادات
git config --list
```

---

## ٢. الأوامر الأساسية

### ٢.١ بدء المشروع

```bash
# إنشاء مستودع جديد
git init

# استنساخ مستودع موجود
git clone https://github.com/user/repo.git

# عرض الحالة
git status

# عرض السجل
git log --oneline --graph --all
```

### ٢.٢ العمل اليومي

```bash
# إضافة الملفات
git add file.txt          # ملف محدد
git add .                 # جميع الملفات
git add -A                # جميع التغييرات

# الالتزام
git commit -m "إضافة ميزة جديدة"
git commit -am "إصلاح خطأ"  # إضافة والتزام معاً

# عرض التغييرات
git diff                  # التغييرات غير الملتزمة
git diff --staged         # التغييرات المجهزة
```

---

## ٣. إدارة الفروع

### ٣.١ الأوامر الأساسية

```bash
# إنشاء فرع جديد
git branch feature/login

# عرض الفروع
git branch                # الفروع المحلية
git branch -r             # الفروع البعيدة
git branch -a             # جميع الفروع

# التبديل بين الفروع
git checkout feature/login
git switch feature/login  # الطريقة الحديثة

# إنشاء والتبديل لفرع جديد
git checkout -b feature/register
git switch -c feature/register

# حذف فرع
git branch -d feature/old
git branch -D feature/old  # فرض الحذف
```

### ٣.٢ تسمية الفروع (Convention)

```
نمط التسمية:
├── feature/وصف-الميزة      # ميزة جديدة
├── bugfix/وصف-الإصلاح      # إصلاح خطأ
├── hotfix/وصف-العاجل       # إصلاح عاجل
├── release/v1.0.0          # إصدار جديد
├── docs/وصف-التوثيق        # توثيق
└── refactor/وصف-إعادة-البنيان  # إعادة بنيان
```

---

## ٤. سير العمل Git Flow

### ٤.١ هيكل الفروع

```
main (أو master)
├── develop
│   ├── feature/login
│   ├── feature/register
│   ├── feature/dashboard
│   ├── bugfix/issue-123
│   └── release/v1.0.0
└── hotfix/critical-fix
```

### ٤.٢ دورة الحياة

```
١. بدء ميزة جديدة:
   git checkout develop
   git checkout -b feature/new-feature

٢. العمل على الميزة:
   git add .
   git commit -m "feat: إضافة تسجيل الدخول"

٣. دمج مع develop:
   git checkout develop
   git merge feature/new-feature
   git branch -d feature/new-feature

٤. إعداد إصدار:
   git checkout -b release/v1.0.0 develop
   # اختبار وإصلاحات أخيرة
   git checkout main
   git merge release/v1.0.0
   git tag v1.0.0

٥. إصلاح عاجل:
   git checkout -b hotfix/fix main
   # إصلاح
   git checkout main
   git merge hotfix/fix
   git checkout develop
   git merge hotfix/fix
```

### ٤.٣ أوامر Git Flow (Extension)

```bash
# تثبيت Git Flow
# Ubuntu/Debian
sudo apt install git-flow

# macOS
brew install git-flow

# بدء Git Flow
git flow init

# ميزة جديدة
git flow feature start login
git flow feature finish login

# إصدار جديد
git flow release start v1.0.0
git flow release finish v1.0.0

# إصلاح عاجل
git flow hotfix start critical-fix
git flow hotfix finish critical-fix
```

---

## ٥. الدمج وإعادة الكتابة

### ٥.١ Merge vs Rebase

| Merge | Rebase |
|-------|--------|
| يحفظ التاريخ كما هو | يعيد كتابة التاريخ |
| ينشئ commit دمج | لا ينشئ commit إضافي |
| آمن للفروع المشتركة | لا يستخدم للفروع المشتركة |
| موصى به للفروع | موصى به للفروع المحلية |

### ٥.٢ أمثلة

```bash
# Merge
git checkout main
git merge feature/login
# ينشئ: Merge branch 'feature/login'

# Rebase
git checkout feature/login
git rebase main
# يعيد كتابة commits على قمة main

# Rebase التفاعلي
git rebase -i HEAD~3
# خيارات:
# pick   - استخدام commit
# reword - تغيير الرسالة
# edit   - تعديل commit
# squash - دمج مع السابق
# drop   - حذف commit
```

---

## ٦. حل النزاعات

### ٦.١ عندما يحدث نزاع

```
<<<<<<< HEAD
كودك الحالي
=======
كود الفرع الآخر
>>>>>>> feature-branch
```

### ٦.٢ خطوات الحل

```bash
# ١. تحديد الملفات المتأثرة
git status

# ٢. فتح الملف وحل النزاع يدوياً
# احذف علامات النزاع واحتفظ بالكود الصحيح

# ٣. بعد الحل
git add resolved-file.txt
git commit -m "حل نزاع في ملف كذا"

# ٤. أو إلغاء العملية
git merge --abort
git rebase --abort
```

### ٦.٣ أدوات حل النزاعات

```bash
# إعداد أداة الحل
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd "code --wait \$MERGED"

# تشغيل أداة الحل
git mergetool

# أدوات شائعة:
# - VS Code
# - Meld
# - KDiff3
# - P4Merge
```

---

## ٧. العمل مع المستودعات البعيدة

### ٧.١ الأوامر الأساسية

```bash
# إضافة remote
git remote add origin https://github.com/user/repo.git
git remote -v

# السحب
git pull origin main
git pull --rebase origin main

# الدفع
git push origin main
git push -u origin feature/login  # مع تتبع

# جلب بدون دمج
git fetch origin
git fetch --all

# عرض الفروع البعيدة
git branch -r
```

### ٧.٢ المزامنة

```bash
# تحديث الفرع المحلي
git checkout main
git pull origin main

# تحديث جميع الفروع
git fetch --all
git pull --all

# تنظيف الفروع المحذوفة
git fetch -p
git remote prune origin
```

---

## ٨. طلبات السحب (Pull Requests)

### ٨.١ إنشاء PR

```bash
# ١. إنشاء فرع للميزة
git checkout -b feature/new-feature

# ٢. العمل والالتزام
git add .
git commit -m "feat: إضافة الميزة الجديدة"

# ٣. الدفع للفرع
git push -u origin feature/new-feature

# ٤. إنشاء PR على GitHub/GitLab
# اذهب إلى المستودع → Pull Requests → New
```

### ٨.٢ مراجعة PR

```markdown
قالب مراجعة PR:

## الوصف
[وصف التغييرات]

## النوع
- [ ] ميزة جديدة
- [ ] إصلاح خطأ
- [ ] تحسين
- [ ] كسر تغيير

## الاختبار
- [ ] تم اختبار الميزة
- [ ] تم تحديث الاختبارات
- [ ] جميع الاختبارات ناجحة

## قائمة المراجعة
- [ ] الكود يتبع المعايير
- [ ] التوثيق محدث
- [ ] لا تحذيرات جديدة
```

---

## ٩. رسائل الالتزام

### ٩.١ Conventional Commits

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### ٩.٢ الأنواع

| النوع | الوصف | مثال |
|-------|-------|------|
| `feat` | ميزة جديدة | feat(auth): إضافة تسجيل الدخول |
| `fix` | إصلاح خطأ | fix(api): إصلاح خطأ في endpoint |
| `docs` | توثيق | docs(readme): تحديث التعليمات |
| `style` | تنسيق | style(css): إصلاح المسافات |
| `refactor` | إعادة بنيان | refactor(core): تحسين الأداء |
| `test` | اختبارات | test(auth): إضافة اختبارات |
| `chore` | مهام صيانة | chore: تحديث التبعيات |

### ٩.٣ أمثلة

```bash
# جيد
git commit -m "feat(auth): إضافة تسجيل الدخول عبر Google"
git commit -m "fix(api): إصلاح خطأ 404 في users endpoint"

# سيء
git commit -m "fix"
git commit -m "update"
git commit -m "تغييرات بسيطة"
```

---

## ١٠. نصائح متقدمة

### ١٠.١ Stash

```bash
# حفظ التغييرات مؤقتاً
git stash
git stash save "عمل قيد التقدم"

# عرض المحفوظات
git stash list

# استعادة
git stash pop          # استعادة وحذف
git stash apply        # استعادة والاحتفاظ

# استعادة محدد
git stash apply stash@{2}
```

### ١٠.٢ Cherry-pick

```bash
# نسخ commit محدد
git cherry-pick abc123

# نسخ نطاق
git cherry-pick abc123..def456

# مع الاحتفاظ بالمعلومات الأصلية
git cherry-pick -x abc123
```

### ١٠.٣ Bisect (تتبع الأخطاء)

```bash
# بدء البحث
git bisect start

# تحديد commit السيء
git bisect bad

# تحديد commit الجيد
git bisect good v1.0.0

# Git سيقوم بالبحث الثنائي
# اختبر كل commit وأشر:
git bisect good  # أو git bisect bad

# إنهاء
git bisect reset
```

### ١٠.٤ Reset & Revert

```bash
# Reset (يغير التاريخ)
git reset --soft HEAD~1    # التراجع عن commit فقط
git reset --mixed HEAD~1   # الافتراضي
git reset --hard HEAD~1    # حذف كل شيء

# Revert (آمن للفروع المشتركة)
git revert abc123          # عكس commit
git revert HEAD~3..HEAD    # عكس نطاق
```

---

## ١١. Hooks

### ١١.١ Git Hooks

```bash
# الموقع
.git/hooks/

# Hooks شائعة
pre-commit      # قبل الالتزام
commit-msg      # التحقق من رسالة الالتزام
pre-push        # قبل الدفع
post-merge      # بعد الدمج
```

### ١١.٢ مثال: pre-commit hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# التحقق من تنسيق الكود
echo "Running linter..."
npm run lint

# التحقق من الاختبارات
echo "Running tests..."
npm test

# التحقق من رسالة الالتزام
if ! grep -q "^feat:\|^fix:\|^docs:" "$1"; then
    echo "❌ رسالة الالتزام يجب أن تتبع Conventional Commits"
    exit 1
fi

echo "✅ جميع الفحوصات ناجحة"
```

---

## ١٢. أفضل الممارسات

### ١٢.١ ما يجب فعله

✅ الالتزامات الصغيرة والمتكررة
✅ رسائل وصفية واضحة
✅ فرع واحد لكل ميزة
✅ دمج متكرر مع main
✅ مراجعة الكود قبل الدمج
✅ اختبار قبل الالتزام
✅ استخدام .gitignore

### ١٢.٢ ما يجب تجنبه

❌ الالتزامات الكبيرة النادرة
❌ رسائل غامضة ("fix", "update")
❌ العمل المباشر على main
❌ فروع قديمة غير مدمجة
❌ كود غير مختبر
❌ ملفات حساسة (كلمات مرور، مفاتيح)

---

## ١٣. أدوات مساعدة

### ١٣.١ واجهات رسومية

| الأداة | المنصة | السعر |
|--------|--------|-------|
| GitHub Desktop | Win/Mac/Linux | مجاني |
| GitKraken | Win/Mac/Linux | مدفوع |
| Sourcetree | Win/Mac | مجاني |
| VS Code Git | جميع | مجاني |

### ١٣.٢ أوامر مفيدة

```bash
# alias مفيدة
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'

# الاستخدام
git co feature/login
git st
```

---

## المراجع

- Git Official Documentation
- Pro Git Book (متاح مجاناً)
- Atlassian Git Tutorial
- Conventional Commits Specification

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
```

---

## الكلمات المفتاحية

### العربية:
- "جيت سير عمل"
- "Git بالعربي"
- "تحكم إصدارات"
- "فرع ودمج"
- "commit رسالة"

### English:
- "git workflow arabic"
- "git tutorial arabic"
- "version control arabic"
- "git branch merge"
- "git commit message"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
