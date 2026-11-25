---
name: motion-from-reference
description: Build a new motion-graphics video in Remotion in the style of a reference video. Use when the user names a style from the styles/ library (e.g. "plotter", "doodle", "whiteboard", "chalkboard", "stickman", "isometric", "fake3d", "infographic", "map-journey" or "product") or puts a video in reference/, and asks for a new video, animation, explainer or motion graphics in that style («اصنع فيديو بنفس الستايل»). Covers studying the reference, one round of questions, script and voice timing, building scenes, review in Remotion Studio, and rendering only after the user approves.
---

<div dir="rtl">

# فيديو موشن جرافيك من فيديو مرجعي

**الهدف:** فيديو جديد بموضوع المستخدم، يبدو كأن صانع الفيديو المرجعي هو من صنعه.
- خذ من المرجع **الأسلوب** فقط: الألوان، والإيقاع، والحركة، والخطوط، والتفاصيل.
- لا تنسخ **المحتوى**: النصوص، والشعارات، والصور، والعلامات التجارية.

**قبل أن تبدأ:**
- شغّل كل الأوامر من جذر المشروع.
- السكريبتات في `.agents/skills/motion-from-reference/scripts/`، ونسمّيها هنا `$S`.
- المراحل بالترتيب، ولا تقفز فوق مرحلة.

## المرحلة 0: التجهيز
1. **إن بدأت من رابط الريبو** ولست داخل المشروع، فانسخه وادخل إليه:
   - المجلد الحالي فارغ: `git clone https://github.com/motalim-ai/motion-starter-kit.git .`
   - المجلد فيه ملفات: `git clone https://github.com/motalim-ai/motion-starter-kit.git motion-video`، ثم ادخل `motion-video`.
2. **تحقّق من الأدوات:** `node -v` (الإصدار 18 أو أحدث)، و`ffmpeg -version`، و`uv --version`.
3. **إن نقصت أداة:**
   - اشرح للمستخدم في جملة بسيطة ما هي ولماذا نحتاجها، واعرض أن تثبّتها أنت.
   - بعد موافقته ثبّتها:
     - macOS: `brew install node ffmpeg uv`
     - Windows: `winget install OpenJS.NodeJS.LTS Gyan.FFmpeg astral-sh.uv`
     - إن لم يكن مدير الحزم موجودًا، فاستخدم المثبّت الرسمي لكل أداة.
4. **ثبّت المشروع:** `cd video && npm install`.

## المرحلة 1: افهم المرجع
1. **حدّد المرجع:**
   - إن ذكر المستخدم اسم ستايل، فالمرجع `styles/<الاسم>/reference.mp4`. قائمة الستايلات في `styles/README.md`.
   - وإلا، فالمرجع كل فيديو في `reference/`.
   - إن لم يذكر ستايلًا وكان `reference/` فارغًا: اعرض عليه الستايلات الموجودة في `styles/README.md`، واسأله هل يختار واحدًا منها أم يضع فيديو خاصًا به. هذا هو السؤال الوحيد المسموح قبل التحليل.
2. حلّل المرجع:
   ```
   uv run --no-project --with numpy --with pillow python $S/analyze.py <مسار الفيديو> --out analysis/<اسم الستايل أو الفيديو>
   ```
3. اقرأ `analysis/<الاسم>/report.md`.
4. **انظر** إلى كل صورة في `sheets/` و`motion/`، وإلى `palette.png`.
   - صور `motion/` هي الأهم: كل صورة 8 إطارات بينها 0.1 ثانية.
   - منها تعرف كيف تدخل العناصر وتخرج، وكم تستغرق الحركة، وهل هي ناعمة أم حادة.
5. إن كان نموذجك يستطيع مشاهدة الفيديو أو سماع الصوت مباشرة، فافعل ذلك أيضًا.
6. اكتب `STYLE.md` في جذر المشروع بالقالب الموجود في [references/style-bible.md](references/style-bible.md).
   - كن محددًا بالأرقام: أكواد الألوان، والأحجام بالبكسل، والمدد بالثواني، وأسماء منحنيات الحركة.
   - «حركة ناعمة» لا تكفي. المطلوب مثل: «تصعد الكلمة 40px خلال 0.45 ثانية بـ easeOutCubic».

## المرحلة 2: الأسئلة، مرة واحدة فقط
1. لخّص للمستخدم الأسلوب في 5 أسطر قصيرة، ليعرف أنك فهمته.
2. اسأل كل الأسئلة الموجودة في [references/questions.md](references/questions.md) في رسالة واحدة، مع اقتراحك لكل سؤال.
3. انتظر الإجابات، ولا تبدأ البناء قبلها.

## المرحلة 3: الخطة
اكتب `PLAN.md` وفيه:
- **السكريبت:** سطر لكل جملة تظهر على الشاشة أو تُقال. احفظه أيضًا في `script.txt` بنفس الأسطر.
- **جدول المشاهد:** المشهد، ويبدأ عند أي جملة، وماذا يظهر، وعلى أي كلمة، والحركة، والمؤثر الصوتي.
- **قائمة مهام** بمربعات `[ ]`، تحدّثها أثناء العمل.

بعدها تابع مباشرة، إلا في حالة واحدة: إن اختار المستخدم تعليقًا صوتيًا ولم يعطك ملفه.
- اكتب `voice-script.md` كما في [references/audio.md](references/audio.md).
- اشرح له بخطوات قصيرة وبسيطة كيف يحوّله إلى صوت (مثلًا في ElevenLabs)، وأين يضع الملف: `video/public/voice.mp3`.
- توقف حتى يضعه.

## المرحلة 4: التوقيت والصوت
- **مع تعليق صوتي:**
  ```
  uv run --no-project --python 3.12 --with torch==2.5.1 --with torchaudio==2.5.1 --with uroman --with numpy python $S/align.py --audio video/public/voice.mp3 --script script.txt --gap 0.5
  ```
- **بلا تعليق صوتي:**
  ```
  uv run --no-project python $S/align.py --script script.txt --wps 2.2 --gap 0.8
  ```
- **المؤثرات الصوتية:**
  ```
  uv run --no-project --with numpy python $S/sfx.py
  ```
  هذا يكتب `video/public/sfx/`. ويمكنك أيضًا استخدام `@remotion/sfx`.
- **الموسيقى** (إن طلبها المستخدم ولم يعطك ملفًا)، بمدة الفيديو:
  ```
  uv run --no-project --with numpy python $S/music.py --mood calm|tech|bright
  ```
  يأخذ المدة من `words.json` وحده، ويكتب `video/public/music.wav`.
- النتيجة في `video/src/data/words.json`. راجع الجدول المطبوع: الكلمات منخفضة الثقة تستحق نظرة، لكنها غالبًا مقبولة.

## المرحلة 5: البناء، مشهدًا بعد مشهد
اقرأ [references/remotion.md](references/remotion.md) و[references/arabic.md](references/arabic.md) قبل أول مشهد. ثم لكل مشهد:
1. أنشئ ملفه في `video/src/scenes/`، وأضفه إلى `SCENES` في `video/src/Video.tsx`.
2. خذ كل توقيت من `line()` و`word()` في `video/src/timing.ts`.
3. التقط صورًا ثابتة عند لحظتين أو ثلاث مهمة:
   ```
   cd video && npm run stills -- <الثواني>
   ```
4. ضع الصور **بجانب** صفحات المرجع واسأل: هل تبدو من نفس الفيديو؟ إن لم تكن كذلك، أصلح قبل المشهد التالي.
5. علّم المهمة في `PLAN.md`.

## المرحلة 6: المراجعة الذاتية
- اتبع [references/review.md](references/review.md) بندًا بندًا.
- شغّل `npm run typecheck`، ويجب ألا يظهر أي خطأ.

## المرحلة 7: التسليم
1. شغّل `npm run studio` في الخلفية من داخل `video/`. العنوان عادة http://localhost:3000.
2. افتح Studio للمستخدم إن كانت لديك أداة متصفح، وإلا فأعطه الرابط.
3. أخبره باختصار وبكلام بسيط:
   - ماذا بنيت.
   - **كيف يشاهد:** زر التشغيل أو المسافة للتشغيل والإيقاف، والشريط في الأسفل للتنقل.
   - عند أي ثوانٍ يتوقف ليراجع.
   - ما الذي لم تكن متأكدًا منه.
   - إن أراد تغيير شيء، يكفي أن يقوله بكلامه العادي.
4. **توقف هنا ولا ترندر.**

## المرحلة 8: التعديلات ثم الرندر
- **لكل ملاحظة من المستخدم:** عدّل، وتحقق بصور ثابتة، ثم اطلب منه المراجعة في Studio (يتحدّث وحده).
- **الرندر** فقط عندما يقول المستخدم «رندر» أو ما يعني ذلك:
  ```
  cd video && npm run render -- --approved
  ```
  الناتج في `video/out/video.mp4`.

</div>
