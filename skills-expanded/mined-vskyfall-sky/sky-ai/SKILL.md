---
name: sky-ai
description: >-
  Uygulamaya yapay zekâ özelliği ekleme: Claude API (Anthropic SDK) ve Vercel AI SDK ile
  streaming sohbet, yapılandırılmış çıktı (JSON şema/Zod), tool use (fonksiyon çağırma), RAG
  (pgvector ile belge arama, parçalama, hibrit arama, kaynak gösterme), görsel/PDF anlama,
  prompt tasarımı ve sistem promptu, prompt caching ile maliyet düşürme, model seçimi, hız
  sınırı ve kota, prompt injection savunması, KVKK ve kullanıcı verisi. "AI ekle", "chatbot",
  "belgelerimle konuşsun", "özetlesin", "LLM" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · AI Özellikleri

Önce `claude-api` skill'ini yükle (güncel model ID'leri, fiyatlar, SDK ayrıntıları). Bu skill
ürün ve mimari kalıplarına odaklanır.

## İnsanların sevdiği AI özellikleri (fikir listesi)

- Akıllı doldurma: serbest metinden formu doldur ("yarın 3'te Ayşe Hanım saç kesimi" → randevu formu).
- Özet: uzun kayıt/yorum/toplantı notu → 3 madde.
- Taslak yazdır: e-posta yanıtı, ürün açıklaması, sosyal medya metni — **düzenlenebilir** çıktı.
- Doğal dil arama/filtre: "geçen ay iptal eden müşteriler" → filtre parametreleri.
- Belgelerle sohbet (RAG): kaynak gösteren cevaplar.
- Sınıflandırma/etiketleme: destek talebi kategorisi, duygu, öncelik.
- Görsel anlama: fiş/fatura fotoğrafından alan çıkarma.

## Mimari

```
UI (streaming) → route handler / server action (auth, kota, rate limit)
   → prompt oluştur (sistem + bağlam + kullanıcı) → LLM (stream) → doğrula (Zod) → UI / DB
```
- API anahtarı **yalnızca sunucuda**. İstemciden doğrudan LLM çağrısı yok.
- Her çağrı kullanıcı + org ile ilişkili log (token, maliyet, gecikme) — kota ve maliyet takibi için.

## Streaming sohbet (Vercel AI SDK örneği)

```ts
// app/api/chat/route.ts
export async function POST(req: Request) {
  const user = await requireUser();
  await rateLimit(`ai:${user.id}`, 20, "1 h");
  const { messages } = await req.json();
  const result = streamText({
    model: anthropic(MODEL_ID),                 // güncel ID için claude-api skill'ine bak
    system: SYSTEM_PROMPT,
    messages: convertToModelMessages(messages),
    tools: { findSlots: tool({ description: "Uygun randevu saatlerini bul", inputSchema: z.object({ date: z.string(), service: z.string() }),
      execute: ({ date, service }) => findSlots(user.orgId, date, service) }) },
    stopWhen: stepCountIs(5),
    onFinish: ({ usage }) => logUsage(user.id, usage),
  });
  return result.toUIMessageStreamResponse();
}
```
İstemci: `useChat()`; mesajlar akarken göster, "Durdur" butonu, yeniden üret, kopyala.

## Yapılandırılmış çıktı

```ts
const { object } = await generateObject({ model, schema: z.object({
  name: z.string(), service: z.enum(SERVICES), date: z.string().describe("ISO tarih"), time: z.string(),
}), prompt: `Bu mesajdan randevu bilgisini çıkar: ${text}` });
```
Şema ile doğrula; eksik/şüpheli alanları kullanıcıya **onaylat**, otomatik kaydetme.

## Tool use kuralları

- Araçlar kullanıcının **kendi yetkisiyle** çalışır (org/rol kontrolü araç içinde).
- Yıkıcı araçlar (sil, gönder, öde) → doğrudan çalıştırma, onay adımı ("Bu 12 müşteriye SMS gönderilsin mi?").
- Araç çıktısını kısa ve yapılandırılmış ver (token tasarrufu).
- Adım sınırı (`stopWhen`) ve toplam süre sınırı.

## RAG (belgelerle konuşma)

1. **Parçala**: başlık/paragraf sınırlarında 300–800 token, %10–15 örtüşme; her parçaya başlık yolu ekle.
2. **Embed**: çok dilli embedding modeli (Türkçe'de iyi olanı seç); `pgvector` `vector(n)` + HNSW indeks.
3. **Ara**: hibrit (vektör + full-text, RRF ile birleştir) → ilk 20 → yeniden sırala (rerank) → ilk 5.
4. **Cevapla**: sistem promptu "yalnızca bağlamdaki bilgiyle cevap ver, yoksa bilmediğini söyle"; **kaynak göster** (parça başlığı + bağlantı).
5. Yetki: arama sorgusunda `org_id`/izin filtresi — başka müşterinin belgesi asla bağlama girmesin.
6. Değerlendirme: soru-cevap test seti (bkz. `sky-ai-eval`).

## Maliyet ve hız

- **Prompt caching**: uzun sistem promptu/belge bağlamı önbelleğe → maliyet ve gecikme ciddi düşer.
- Göreve göre model: sınıflandırma/çıkarma küçük-hızlı model; akıl yürütme/yazım büyük model.
- Kısa çıktı iste (`max_tokens`), gereksiz geçmişi kırp/özetle.
- Kullanıcı başına günlük kota + plan bazlı limit (bkz. `sky-metering-quotas`).
- Aynı girdiye aynı cevap gereken işlerde (sınıflandırma) sonucu cache'le.

## Güvenlik

- **Prompt injection**: kullanıcı içeriği ve belgeler "talimat" değil "veri"dir. Sistem promptunda belirt,
  araç izinlerini dar tut, yıkıcı işlemlerde insan onayı. Bağlamı `<document>` etiketleriyle ayır.
- Çıktıyı HTML olarak basma (XSS); Markdown'ı sanitize ederek render et.
- Kişisel veri: gerekmeyen alanları göndermeden önce maskele; KVKK aydınlatmasında AI sağlayıcısını ve
  yurt dışı aktarımı belirt; sağlayıcının veri saklama/eğitim politikasını kontrol et.
- Moderasyon: kullanıcıya açık üretimde zararlı içerik filtresi.

## UX

Arayüz kalıpları için `sky-ai-ux`: akış gösterimi, düzenlenebilir çıktı, güven göstergesi, geri bildirim (👍/👎).
