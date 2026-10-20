---
name: agentic-judge
description: ATDD pipeline'ının agentic/LLM-tool-calling görevlerine özel değerlendirme adımı. `red-team`'in kod incelemesine karşılık gelen sürümü — kodu değil, bir agent'ın bir konuşma turundaki tool-calling trajectory'sini ve nihai cevabını `agentic-judge` subagent'ına (Haiku, pinlenmiş model) yaptırıp sabit JSON şemasıyla puanlar. Sadece `atdd.md`'de acceptance criteria "bir LLM agent/sub-agent davranışını doğrula" diyorsa tetiklenir; normal kod görevlerinde ÇALIŞMAZ.
---

# Agentic-Judge Skill

Bu skill, ATDD pipeline'ının **agentic görevlere özel** bir dalıdır. Normal
kod görevlerinde (`red-team`in kapsadığı alan) tetiklenmez — sadece
`atdd.md`'nin Acceptance Criteria'sı "bir agent/sub-agent'ın tool-calling
davranışını veya LLM cevabını doğrula" diyorsa çalışır.

## Ne zaman tetiklenir

- `atdd.md` bir agentic/tool-calling özelliğini kapsıyorsa (yeni bir
  sub-agent, yeni bir tool, prompt revizyonu, orchestrator değişikliği)
- Kullanıcı açıkça "agentic-judge çalıştır" / "trajectory'yi değerlendir"
  derse
- `code-copilot` bir agent/tool prompt'unu değiştirdiyse ve `verify` bunu
  "agentic davranış değişti" diye işaretlediyse

Tetikleyici yoksa bu adımı atla, doğrudan `red-team`'e geç — bu skill
`red-team`'in yerine geçmez, onu **tamamlar**.

## Ön Koşul

Aynı `<task-slug>` altında:
- `atdd.md` (agentic AC'leri içeren)
- Değerlendirilecek en az bir gerçek konuşma transkripti/log kaydı
  (`obss_project/artifacts/<task-slug>/transcripts/*.json` veya kullanıcının
  verdiği ham transkript)

Transkript yoksa dur, kullanıcıdan hangi konuşma(lar)ın değerlendirileceğini iste.

## Adımlar

1. Her transkripti şu girdi şemasına dönüştür:

```json
{
  "conversation_id": "...",
  "sub_agent": "...",
  "user_intent": "...",
  "available_tools": [{"name": "...", "schema": {}, "sensitive": true|false}],
  "expected_trajectory": ["..."],
  "actual_trajectory": [{"tool": "...", "args": {}, "result_summary": "..."}],
  "final_response": "...",
  "user_feedback": {"signal": "thumbs_down|retry|edit|thumbs_up"} | null
}
```

   `available_tools`'daki `sensitive: true` işaretini atdd.md'de veya
   proje bağlamında PII/finansal veri döndüren tool'lar için sen koy —
   `agentic-judge` subagent'ı bunu kendi uydurmaz.

2. Her transkript için, JSON girdisini önce bir scratchpad dosyasına yaz
   (`Write`, örn. `<scratch>/agentic_judge_input_<conversation_id>.json`) —
   **prompt'a inline gömme**. Token tasarrufu: `agentic-judge` subagent'ı
   zaten `Read` yetkisine sahip (bkz. `.claude/agents/agentic-judge.md`),
   dosyayı kendi (ayrı, ucuz) bağlamında okuyabilir; orkestratörün aynı
   trajectory/tool-args JSON'unu kendi bağlamında tekrar üretip prompt'a
   yazması gereksiz maliyettir — özellikle `actual_trajectory` uzun bir
   tool-calling geçmişiyse. Sonra tek bir `Agent` çağrısı yap:

```
Agent({
  description: "Judge agentic trajectory for <conversation_id>",
  subagent_type: "agentic-judge",
  run_in_background: false,
  prompt: "Şu dosyayı Read et: <scratch dosyasının mutlak yolu>. İçeriği
    1. adımdaki JSON girdi şeması olarak değerlendir, sabit çıktı
    şemasıyla (bkz. bu skill'in JSON şeması) yanıt ver."
})
```

   `subagent_type: "agentic-judge"` zaten Haiku'ya pinli (bkz.
   `.claude/agents/agentic-judge.md`) — model parametresi burada tekrar
   verilmez.

3. Dönen her JSON'ı doğrula (2026-08-25'te sentetik testte üçü de canlı
   yakalandı — atlanabilir formalite değil):
   - Ham çıktı ` ```json ` gibi bir kod bloğuyla sarılıysa önce bunu
     temizle, sonra parse et.
   - `severity`/`category` sabit listede mi.
   - `response_review.criteria` alanlarının HER BİRİ 1-5 aralığında mı
     (Haiku bazen 1-10 skalasına kayıyor — aralık dışıysa reddet, subagent'a
     "1-5 skalasını kullan" notuyla geri gönder).
   - `scope_review.scope_expansion: true` iken `trigger_finding_index`
     doluysa ilgili `findings[i].category == "scope-creep"` mi.
   - `scope_review.sensitive_tool_involved: true` ise, bu bayrağın
     `available_tools` girdisinde `sensitive: true` işaretli VE
     `trigger_finding_index`'in gösterdiği bulguda gerçekten o tool adı
     geçiyor mu — geçmiyorsa bayrak yanlış, düzelt. Ayrıca bu durumda
     ilgili bulgunun `severity`si `critical` DEĞİLSE bu da bir tutarsızlık,
     subagent'a geri gönder (kural: sensitive tool + scope-creep = critical).
   - Şema dışı alan eklenmiş mi (varsa temizle, kullanıcıya not düş).
   Tutarsızsa subagent'a tek seferlik düzeltme isteğiyle geri gönder;
   ikinci denemede de tutarsızsa kullanıcıya ham çıktıyla birlikte bildir.

4. Doğrulanan sonuçları `obss_project/artifacts/<task-slug>/agentic_judge/<conversation_id>.json` yoluna yaz (append-only — var olan bir kaydı asla üzerine yazma, her transkript kendi dosyasında kalır, bu dosyalar sonradan aggregation job'una girdi olur).

5. Task-slug bazında bir özet üret: kaç transkript `approve`/`approve-with-changes`/`block`, `sensitive_tool_involved` olan var mı. Kullanıcıya bu özeti ve dosya yollarını bildir.

## Aggregation (bu skill'in tek seferlik çalıştırdığı, ama tetiklediği ayrı iş)

Bu skill tek bir görevi/transkripti değerlendirir; **tekrar eden kalıbı**
bulmak `postmortem`'in agentic karşılığıdır — ayrı bir zamanlanmış iş
olarak düşünülmeli, bu skill'in kapsamında değildir:

- `trajectory_review`: `category`/`extra_calls`/`missing_calls` sayımı →
  hangi tool'un hangi agent'ta sürekli fazladan/eksik çağrıldığı
- `response_review`: `criteria` alanlarının haftalık ortalaması (trend) +
  `user_feedback` ile judge skoru arasındaki uyuşmazlık oranı (judge
  kalibrasyon sinyali)
- `scope_review`: `scope_expansion` oranı, özellikle `sensitive_tool_involved:
  true` olanlar — bu ayrı bir güvenlik/audit kanalına da düşmeli

Bu aggregation `postmortem` skill'ine yeni bir bölüm olarak eklenmeli
(bkz. Kural). Bu skill kendi başına toplu istatistik üretmez, sadece
tek-tek `agentic_judge/*.json` dosyalarını yazar.

## Kural

- Bu skill kod/prompt DEĞİŞTİRMEZ, sadece transkript okur ve JSON bulgu
  üretir (`red-team` ile aynı disiplin).
- `agentic-judge` subagent'ı **her koşulda Haiku** ile çalışır (maliyet —
  bu adım çok sayıda transkriptte tekrarlanacağı için Sonnet/Opus kotası
  harcanmaz). Subagent tanımında model pinli; burada override etme.
- Bulgu uydurma — her bulgu kanıt (transkript alıntısı) içermeli.
- `block` verdict'i veya `sensitive_tool_involved: true` varsa kullanıcıyı
  açıkça uyar; bu görev için `commit`/deploy önerisinde bulunma.
- Bu adım normal kod görevlerinde (`red-team`in kapsadığı alan) OTOMATİK
  TETİKLENMEZ — pipeline'a "her zaman çalışan" bir adım olarak eklenmedi,
  koşullu bir dal olarak eklendi (bkz. pipeline SKILL.md).
