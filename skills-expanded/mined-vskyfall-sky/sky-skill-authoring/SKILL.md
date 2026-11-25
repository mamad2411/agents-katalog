---
name: sky-skill-authoring
description: >-
  Claude Code için skill, komut, agent, hook ve eklenti yazma: SKILL.md biçimi (frontmatter,
  tetikleyici açıklama yazımı), ilerlemeli açıklama (references/, scripts/), komut dosyaları
  ($ARGUMENTS, argument-hint), agent tanımları (tools, model), hook olayları ve JSON çıktıları
  (ask, additionalContext, block), eklenti yapısı (plugin.json, marketplace.json), doğrulama
  (claude plugin validate) ve test; Sky'ı genişletme. "Skill yaz", "kendi eklentimi yapayım",
  "Sky'a yeni skill ekle", "hook yaz" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Skill & Eklenti Yazımı

Ayrıntılı rehber ve değerlendirme araçları için Anthropic'in `skill-creator` skill'i de kullanılabilir; güncel şema ayrıntıları için resmi dokümana bak.

## SKILL.md

```markdown
---
name: sky-ornek                     # klasör adıyla aynı, kebab-case
description: >-
  NE yapar (1 cümle) + kapsadığı konular (virgüllü liste) + NE ZAMAN kullanılır
  ("X yaparken", "'Y' dendiğinde kullan"). Tetikleyici kelimeler kullanıcının
  diliyle (Türkçe + İngilizce terimler).
---

# Başlık

Kısa giriş: bu skill neyi kapsar, neyi kapsamaz (ilgili skill'lere bağlantı).

## Bölümler…  (karar tabloları, kod örnekleri, kontrol listeleri)
```
- **Açıklama en önemli kısım**: Claude skill'i yalnızca açıklamaya bakarak seçer. Somut tetikleyiciler, alan terimleri, "ne zaman" cümlesi.
- Gövde: talimat ve bilgi; Claude'a "sen…" diye konuşan net yönergeler, karar tabloları, çalışan kod, kontrol listesi.
- Kısa tut (yüklendiğinde bağlam tüketir); uzun referansları `references/*.md` dosyalarına koy ve gövdeden bağla (gerektiğinde okunur).
- Tekrarlanabilir işler için `scripts/` (Claude çalıştırır, deterministik sonuç).
- Bir skill = bir alan; çakışmayı önlemek için diğer skill'lere `bkz.` ile yönlendir.

## Komut (`commands/<ad>.md`)

```markdown
---
description: Tek cümle — ne yapar
argument-hint: "<gerekli> [isteğe bağlı]"
---
# /ad
Görev: `$ARGUMENTS`
1. … adım adım iş akışı (hangi skill'ler yüklenir, ne doğrulanır, ne raporlanır)
```

## Agent (`agents/<ad>.md`)

```markdown
---
name: sky-ornek-agent
description: Ne yapar ve NE ZAMAN çağrılır (ana Claude bu açıklamaya göre seçer).
tools: Read, Grep, Glob, Bash        # en az yetki: denetçiler yazma aracı almaz
model: sonnet                         # görev zorluğuna göre
---
Sen … uzmanısın. Yöntem: 1… 2… Çıktı biçimi: …
```

## Hook (`hooks/hooks.json` + script)

Olaylar: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `PreCompact`, `Notification`.
Script stdin'den JSON alır (`tool_input`, `prompt`, `cwd`, `stop_hook_active`…), çıktısıyla davranışı etkiler:
| İstek | Çıktı |
|---|---|
| Kullanıcıdan onay iste (PreToolUse) | `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"…"}}` |
| Engelle | `permissionDecision: "deny"` veya exit 2 + stderr |
| Claude'a geri bildirim (PostToolUse) | exit 2 + stderr (işlem zaten oldu) |
| Bağlam ekle (SessionStart / UserPromptSubmit) | `{"hookSpecificOutput":{"hookEventName":"…","additionalContext":"…"}}` |
| Bitirmeyi bir kez durdur (Stop) | `{"decision":"block","reason":"…"}` — `stop_hook_active` true ise tekrar engelleme (sonsuz döngü) |
Kurallar: hızlı (zaman aşımı ver), hata olunca sessizce çık (oturumu bozma), dosya değiştirme konusunda çok dikkatli, kapatma anahtarı (Sky: `SKY_HOOKS_DISABLE`),
yolu `${CLAUDE_PLUGIN_ROOT}` ile ver. Sky örnekleri: `hooks/pre-bash.js`, `hooks/post-edit.js`.

## Eklenti yapısı

```
my-plugin/
  .claude-plugin/plugin.json        # name, version, description, skills/commands/agents/hooks yolları
  .claude-plugin/marketplace.json   # yerel/özel pazar yeri olarak eklenebilmesi için
  skills/<ad>/SKILL.md
  commands/<ad>.md
  agents/<ad>.md
  hooks/hooks.json
```
Kurulum: `claude plugin marketplace add <yol|github>` → `claude plugin install <eklenti>@<pazar>`; güncelleme `claude plugin update`.

## Doğrulama ve test

- `claude plugin validate <yol>` — manifest ve yapı.
- Ad uyumu: frontmatter `name` = klasör/dosya adı; çapraz referanslar gerçek dosyalara işaret ediyor.
- Hook'ları sahte stdin ile test et: `echo '{"tool_input":{"command":"git push --force"}}' | node hooks/pre-bash.js`.
- Tetiklenme testi: skill'in yüklenmesi gereken 5–10 örnek istek yaz, gerçek oturumda dene; açıklamayı ona göre ayarla (gerekirse `claude plugin eval`).

## Sky'a ekleme

1. `skills/sky-<ad>/SKILL.md` yaz. 2. `skills/sky/SKILL.md` yönlendirme tablosuna satır ekle.
3. Gerekirse `hooks/prompt-skill.js` anahtar kelime haritasına ve `hooks/session-start.js` stack haritasına ekle.
4. README ve `plugin.json` (agent eklediysen `agents` listesi). 5. Doğrula ve `claude plugin update sky@sky`.
