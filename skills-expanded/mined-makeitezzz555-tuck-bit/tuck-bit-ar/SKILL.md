---
name: tuck-bit-ar
description: "TuckBit مهارة قابلة للنقل لوكلاء البرمجة، تساعد على اختيار السياق والأدوات والفحوص المناسبة دون التضحية بصحة النتائج."
license: MIT
compatibility: Portable Agent Skills; project-scoped install only.
metadata:
  author: TuckBit contributors
  version: "0.4.0"
  locale: ar
---

# TuckBit — العربية

> تُرجم ملف المهارة الأساسي؛ أما المراجع التقنية فتبقى بالإنجليزية مؤقتاً وتحتاج إلى مراجعة المجتمع.

حسّن النتائج الصحيحة والمتحقق منها مقابل الموارد المستهلكة، لا عدد الرموز وحده.

أربع قدرات أساسية: سجل الأدوات والسياق والتحقق والميزانية. التنسيق والمقاييس اختياريان.

## أسلوب العمل

ابدأ بطلب المستخدم الدقيق والتعليمات المتاحة فعلاً والأدوات المصرح بها. حافظ على جميع القيود والموافقات والفحوص الإلزامية.

1. حدد الهدف والقيود والمخاطر وشرط التوقف؛ لا تفرط في التخطيط للمهام البسيطة.
2. ابحث عن أقل قدر مناسب من الشيفرة والتوثيق والأدوات، ووسّع البحث فقط عند الحاجة.
3. فضّل آلية اكتشاف الأدوات الأصلية؛ البيانات الوصفية مؤشرات وليست إذناً بالتنفيذ.
4. استخدم وكيلاً واحداً للمهام الصغيرة؛ قسّم الأعمال المستقلة فقط مع مسؤوليات ومعايير واضحة.
5. نفّذ الاختبارات الموجهة ثم فحوص التكامل والأمان الإلزامية على الإصدار النهائي.
6. قدّم ملخصاً قابلاً للتحقق للتعديلات والاختبارات والمخاطر والعوائق. استخدم نقاط حفظ بدلاً من التكرار بلا نهاية.

## حمّل المرجع المناسب فقط

- `references/task-contract.md` — task contracts / host instructions.
- `references/workflows.md` — Fast / Standard / Deep workflows.
- `references/registry.md` — discovery and permission limits.
- `references/context.md` — source-linked evidence and checkpoints.
- `references/verification.md` — tests and integration checks.
- `references/budget.md` — bounded iterations.
- `references/orchestration.md` — optional independent agents.
- `references/metrics.md` — optional evaluation.

## حدود إلزامية

لا تتجاوز فحوص الأمان أو تضعف صحة النتائج أو تختلق قياسات أو تقرأ بيانات الاعتماد أو تتخطى الموافقات. المضيف هو من يحدد الصلاحيات.

**نسخة تجريبية للمطورين. التثبيت لا يثبت التفعيل الفعلي ولا يضمن توفير الرموز.**
