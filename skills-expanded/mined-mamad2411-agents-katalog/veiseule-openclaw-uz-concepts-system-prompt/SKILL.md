---
summary: "3. OpenClaw tizim prompti nimalarni o‘z ichiga oladi va u qanday yig‘iladi"
read_when:
  - 4. Tizim prompti matnini, asboblar ro‘yxatini yoki vaqt/heartbeat bo‘limlarini tahrirlash
  - 5. Workspace bootstrap yoki ko‘nikmalarni kiritish (skills injection) xatti-harakatini o‘zgartirish
title: "6. System Prompt"
---

# 7. System Prompt

8. OpenClaw har bir agent ishga tushirilishi uchun maxsus tizim promptini yaratadi. Prompt **OpenClaw’ga tegishli** va pi-coding-agent standart promptidan foydalanmaydi.

10. Prompt OpenClaw tomonidan yig‘iladi va har bir agent ishga tushirilishiga kiritiladi.

## 11. Tuzilma

12. Prompt ataylab ixcham qilingan va qat’iy bo‘limlardan foydalanadi:

- 13. **Tooling**: joriy asboblar ro‘yxati + qisqa tavsiflar.
- 14. **Safety**: kuchga intilish xatti-harakatlari yoki nazoratni chetlab o‘tishdan qochish uchun qisqa qo‘riqlovchi eslatma.
- 15. **Skills** (mavjud bo‘lganda): modelga ko‘nikma ko‘rsatmalarini talab bo‘yicha qanday yuklashni aytadi.
- 16. **OpenClaw Self-Update**: `config.apply` va `update.run` ni qanday ishga tushirish.
- 17. **Workspace**: ishchi katalog (`agents.defaults.workspace`).
- 18. **Documentation**: OpenClaw hujjatlarining lokal yo‘li (repo yoki npm paketi) va ularni qachon o‘qish kerakligi.
- 19. **Workspace Files (injected)**: bootstrap fayllari quyida kiritilganini bildiradi.
- 20. **Sandbox** (yoqilganda): sandboxlangan runtime, sandbox yo‘llari va yuqori huquqli exec mavjud yoki yo‘qligini bildiradi.
- 21. **Current Date & Time**: foydalanuvchi lokal vaqti, vaqt zonasi va vaqt formati.
- 22. **Reply Tags**: qo‘llab-quvvatlanadigan provayderlar uchun ixtiyoriy javob teglari sintaksisi.
- 23. **Heartbeats**: heartbeat prompti va tasdiqlash (ack) xatti-harakati.
- 24. **Runtime**: xost, OS, node, model, repo ildizi (aniqlanganda), fikrlash darajasi (bir qatorda).
- 25. **Reasoning**: joriy ko‘rinish darajasi + /reasoning almashtirish bo‘yicha ishora.

26. Tizim promptidagi xavfsizlik qo‘riqlovchilari maslahat xarakteriga ega. 27. Ular model xatti-harakatini yo‘naltiradi, ammo siyosatni majburan ijro etmaydi. 28. Qattiq ijro uchun asbob siyosati, exec tasdiqlashlari, sandboxing va kanal ruxsat ro‘yxatlaridan foydalaning; operatorlar bularni dizayn bo‘yicha o‘chirib qo‘yishi mumkin.

## 29. Prompt rejimlari

30. OpenClaw sub-agentlar uchun kichikroq tizim promptlarini yaratishi mumkin. 31. Runtime har bir ishga tushirish uchun `promptMode` ni o‘rnatadi (foydalanuvchi ko‘radigan sozlama emas):

- `promptMode=minimal` bo‘lganda, qo‘shimcha kiritilgan promptlar **Group Chat Context** o‘rniga **Subagent
  Context** deb belgilanadi.
- 33. `minimal`: sub-agentlar uchun ishlatiladi; **Skills**, **Memory Recall**, **OpenClaw
      Self-Update**, **Model Aliases**, **User Identity**, **Reply Tags**,
      **Messaging**, **Silent Replies** va **Heartbeats** bo‘limlarini chiqarib tashlaydi. 34. Tooling, **Safety**,
      Workspace, Sandbox, Current Date & Time (ma’lum bo‘lganda), Runtime va kiritilgan
      kontekst mavjud bo‘lib qoladi.
- 35. `none`: faqat asosiy identifikatsiya qatorini qaytaradi.

36. `promptMode=minimal` bo‘lganda, qo‘shimcha kiritilgan promptlar **Group Chat Context** o‘rniga **Subagent
    Context** deb belgilanadi.

## 37. Workspace bootstrap kiritilishi

38. Bootstrap fayllari **Project Context** ostida qisqartiriladi va qo‘shiladi, shunda model aniq o‘qishlarsiz identifikatsiya va profil kontekstini ko‘ra oladi:

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `IDENTITY.md`
- `USER.md`
- `HEARTBEAT.md`
- 45. `BOOTSTRAP.md` (faqat mutlaqo yangi workspace-larda)
- `MEMORY.md` va/yoki `memory.md` (workspace’da mavjud bo‘lsa; bittasi yoki ikkalasi ham kiritilishi mumkin)

Ushbu fayllarning barchasi **har bir turn’da context window’ga kiritiladi**, bu esa
tokenlar sarflashini anglatadi. Ularni ixcham saqlang — ayniqsa vaqt o‘tishi bilan
kattalashishi mumkin bo‘lgan `MEMORY.md`, bu kutilmaganda yuqori context ishlatilishiga va tez-tez
compaction’ga olib kelishi mumkin.

> **Eslatma:** `memory/*.md` kundalik fayllar avtomatik ravishda **kiritilmaydi**. Ular
> `memory_search` va `memory_get` vositalari orqali talab bo‘yicha olinadi, shuning uchun
> model ularni aniq o‘qimaguncha context window hisobiga kirmaydi.

46. Katta fayllar belgi (marker) bilan qisqartiriladi. 47. Har bir fayl uchun maksimal hajm
    `agents.defaults.bootstrapMaxChars` (standart: 20000) tomonidan boshqariladi. Fayllar bo‘yicha jami kiritiladigan bootstrap
    kontent `agents.defaults.bootstrapTotalMaxChars`
    (standart: 24000) bilan cheklangan. Mavjud bo‘lmagan fayllar uchun qisqa missing-file belgisi kiritiladi.

Sub-agent session’lari faqat `AGENTS.md` va `TOOLS.md` fayllarini kiritadi (boshqa bootstrap fayllar
sub-agent context’ini kichik saqlash uchun filtrlanadi).

49. Ichki hooklar `agent:bootstrap` orqali bu bosqichni ushlab qolib, kiritilgan bootstrap fayllarini o‘zgartirishi yoki almashtirishi mumkin (masalan, `SOUL.md` ni muqobil persona bilan almashtirish).

50. Har bir kiritilgan fayl qancha hissa qo‘shishini (xom vs kiritilgan, qisqartirish va asbob sxemasi ustama xarajatlari bilan) tekshirish uchun `/context list` yoki `/context detail` dan foydalaning. See [Context](/concepts/context).

## Time handling

The system prompt includes a dedicated **Current Date & Time** section when the
user timezone is known. To keep the prompt cache-stable, it now only includes
the **time zone** (no dynamic clock or time format).

Use `session_status` when the agent needs the current time; the status card
includes a timestamp line.

Configure with:

- `agents.defaults.userTimezone`
- `agents.defaults.timeFormat` (`auto` | `12` | `24`)

See [Date & Time](/date-time) for full behavior details.

## Skills

When eligible skills exist, OpenClaw injects a compact **available skills list**
(`formatSkillsForPrompt`) that includes the **file path** for each skill. The
prompt instructs the model to use `read` to load the SKILL.md at the listed
location (workspace, managed, or bundled). If no skills are eligible, the
Skills section is omitted.

```
<available_skills>
  <skill>
    <name>...</name>
    <description>...</description>
    <location>...</location>
  </skill>
</available_skills>
```

This keeps the base prompt small while still enabling targeted skill usage.

## Documentation

When available, the system prompt includes a **Documentation** section that points to the
local OpenClaw docs directory (either `docs/` in the repo workspace or the bundled npm
package docs) and also notes the public mirror, source repo, community Discord, and
ClawHub ([https://clawhub.com](https://clawhub.com)) for skills discovery. The prompt instructs the model to consult local docs first
for OpenClaw behavior, commands, configuration, or architecture, and to run
`openclaw status` itself when possible (asking the user only when it lacks access).

