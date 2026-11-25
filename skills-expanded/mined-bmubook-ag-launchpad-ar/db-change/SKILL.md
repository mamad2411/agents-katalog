---
name: db-change
description: "تعديل قاعدة البيانات بأمان (البند 18) — Firestore: نموذج البيانات وقواعد الأمان firestore.rules والفهارس مع اختبارها على المحاكي؛ أو Supabase: هجرات SQL و RLS والمنح مع اختبارات pgTAP على القاعدة المحلية؛ ثم النشر بموافقتك (database change, security rules, RLS, migrations, indexes)."
argument-hint: "[وصف التعديل على قاعدة البيانات]"
---
<div dir="rtl">


# &rlm;/db-change — تعديل قاعدة البيانات بأمان (Firebase)

> **المرجع:** البند 18 (قفل تعديلات قاعدة البيانات — `rules_workflow.md`)، والبند 5 (قواعد الحماية — `rules_security.md`)، والبند 28 (المعرّفات)، والبنود 7 و 8 و 13 و 15 و 16.
> **المبدأ:** قواعد الأمان والفهارس **ملفات في المستودع** تُختبر على المحاكي ثم تُنشر بـ Firebase CLI. يُحظر تعديلها من لوحة تحكم Firebase مباشرة.

- وصف التعديل: `$ARGUMENTS`. إذا كان فارغاً فاسأل المستخدم عن التعديل المطلوب قبل أي خطوة.
- تحقّق من الفرع أولاً (البند 15): إذا كنت على `main` أو `master` فأنشئ فرعاً مؤقتاً: `git switch -c feat/db-<name>`.
- **Supabase:** إذا كان صف "قاعدة البيانات" في القسم 5 من `project_map.md` هو Supabase (أو وُجد مجلد `supabase/migrations`)، فاقرأ `.claude/skills/db-change/supabase.md` واتبعه بدل الأقسام 2–5 أدناه.
- قاعدة أخرى غير Firestore (قرار انحراف موثّق مثل Data Connect أو PostgreSQL آخر): طبّق المبادئ نفسها بأداة الهجرات الرسمية لتلك التقنية: ملف مؤرخ لكل تعديل، وحماية على مستوى الصف، واختبار على قاعدة محلية منفصلة، ونشر بموافقة.

## 1. افهم التعديل وصنّفه
| نوع التعديل | ما يلزم |
|:---|:---|
| مجموعة (Collection) جديدة | توثيق شكل المستند + قواعد أمان جديدة + فهارس إن لزمت + اختبارات قواعد |
| حقل جديد في مجموعة قائمة | تحديث التحقق في القواعد + الأنواع في الكود؛ المستندات القديمة بلا الحقل يجب أن يتعامل معها الكود بأمان |
| تغيير صلاحيات | تعديل القواعد + اختبارات تثبت المسموح والممنوع |
| تحويل بيانات موجودة (إعادة تسمية حقل، تغيير شكل) | سكربت ترحيل مؤرخ في `scripts/migrations/` يُجرَّب على المحاكي أولاً، ويُشغَّل على الإنتاج بموافقة صريحة فقط |

## 2. وثّق شكل البيانات أولاً
في القسم 8 من `project_map.md` (مخطط قاعدة البيانات) أضف أو حدّث صفاً لكل مجموعة: اسم المجموعة، الحقول وأنواعها، العلاقات (معرّفات مستندات أخرى)، ملاحظات الحماية والفهارس. مثال:
`| orders | ownerId, items, total, status, createdAt | string, array, number, string, timestamp | ownerId → users | قواعد: المالك فقط · فهرس: ownerId + createdAt |`

قواعد التصميم:
- المعرّف: معرّف Firestore التلقائي، والترتيب الزمني بحقل `createdAt = serverTimestamp()` (البند 28).
- حقل الملكية (`ownerId`) في كل مستند خاص بمستخدم — تبني عليه القواعد.
- لا تكرار بيانات (Denormalization) إلا لسبب موثّق في `decisions_log.md` (عادةً لتقليل القراءات).
- المستند ≤ 1MB؛ القوائم التي تكبر بلا حد تكون مجموعة فرعية لا مصفوفة.

## 3. اكتب قواعد الأمان (`firestore.rules`)
| ❌ ممنوع | ✅ المطلوب |
|:---|:---|
| «وضع الاختبار» أو `allow read, write: if true` أو شرط تاريخ مؤقت | قاعدة لكل مجموعة، مغلقة افتراضياً |
| `allow write` واحدة لكل العمليات دون تمييز | فصل `create` و `update` و `delete` عند اختلاف شروطها |
| الوثوق بقيم يرسلها العميل (مثل `role: "admin"`) | التحقق من `request.auth.uid` وشكل `request.resource.data` وأنواعه وأطواله |
| حذف القاعدة الختامية `match /{document=**} { allow read, write: if false; }` | إبقاؤها آخر القواعد دائماً |

مثال مجموعة جديدة:

```
match /notes/{noteId} {
  allow read, delete: if request.auth != null && request.auth.uid == resource.data.ownerId;
  allow create: if request.auth != null
    && request.auth.uid == request.resource.data.ownerId
    && request.resource.data.title is string
    && request.resource.data.title.size() > 0
    && request.resource.data.title.size() <= 200;
  allow update: if request.auth != null
    && request.auth.uid == resource.data.ownerId
    && request.resource.data.ownerId == resource.data.ownerId;
}
```

- تخزين الملفات: القواعد نفسها في `storage.rules` (مسار يحوي معرّف المالك، وحد لحجم الملف ونوعه).
- الفهارس المركّبة في `firestore.indexes.json` لكل استعلام يجمع فلترة وترتيباً.

## 4. اختبر على المحاكي (إلزامي)
1. **المراجعة (البند 7):** تعديل قواعد الأمان تعديل أمني. في `production` شغّل `/consensus-gate`. في `prototype` مراجعة أمنية سريعة: هل القاعدة الختامية مغلقة؟ هل كل مجموعة محمية؟
2. **اختبارات القواعد** بـ `@firebase/rules-unit-testing` في `tests/rules/` (البند 13) — لكل مجموعة جديدة أو معدّلة على الأقل:
   - المالك يقرأ ويكتب مستنده ✅
   - مستخدم آخر لا يقرأ ولا يعدّل مستند غيره ❌
   - زائر غير مسجّل لا يقرأ ولا يكتب ❌
   - بيانات بشكل خاطئ تُرفض ❌
   - في اختبارات تدفق التطبيق بمكتبة Firebase العادية (تسجيل مستخدم عبر محاكي Auth ثم القراءة والكتابة): تحقّق من رفض الوصول برمز الخطأ `permission-denied` (مثل `expect.objectContaining({ code: 'permission-denied' })`)، لا من نص الرسالة، لأن المحاكي يكتب نصاً تفصيلياً مختلفاً.
3. شغّلها على المحاكي (يتطلب Firebase CLI و JDK 21 أو أحدث): `firebase emulators:exec "npm run test:rules"`، أو في مشاريع Flutter حيث `tests/rules/` مشروع Node مستقل: `firebase emulators:exec "npm --prefix tests/rules test"`. ثم شغّل كل اختبارات المشروع (البند 16).
4. **عند الفشل:** 3 محاولات كحد أقصى (5 في `prototype`)، ثم سجّل في `bugs_log.md` وتراجع وفق البند 15.
5. **إذا تعذّر تشغيل المحاكي** (Java غير مثبتة أو أقدم من 21 مثلاً — الرسالة: firebase-tools no longer supports Java version before 21): أبلغ المستخدم بأن القواعد غير مختبرة، وأعطه رابط التثبيت الرسمي، ولا تنشرها.

## 5. النشر — بموافقة صريحة فقط
لا تنشر أبداً دون اختبار ناجح وموافقة صريحة من المستخدم. اعرض نتيجة الاختبارات ثم اختم بخيارات مرقّمة لا بنافذة الأسئلة، حتى يراها وهو يقرر (`CLAUDE.md` §3): `1. **انشر الآن**`، `2. **لاحقاً**`. عند الموافقة:
`firebase deploy --only firestore:rules,firestore:indexes` (و `storage` إذا تغيّرت `storage.rules`).

سكربتات تحويل البيانات (`scripts/migrations/`) لا تُشغَّل على الإنتاج إلا بعد: تجربتها على المحاكي، ونسخة احتياطية حديثة، وموافقة صريحة منفصلة.

## 6. وثّق واختم
1. &rlm;`project_map.md` القسم 8 — محدَّث من الخطوة 2.
2. &rlm;`decisions_log.md` — قرارات شكل البيانات والتكرار المقصود وأي انحراف.
3. &rlm;`/document` بنوع:

   | التعديل | الوصف |
   |:---|:---|
   | مجموعة أو حقل جديد | `feat(db): ` + الوصف |
   | قواعد أمان فقط | `security(rules): ` + الوصف |
   | تحويل بيانات | `refactor(db): ` + الوصف |

4. ختم التوثيق بصدق، ثم "بروتوكول الاقتراحات" من `.claude/skills/next/SKILL.md`.

</div>
