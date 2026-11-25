---
name: sky-ai-agents
description: >-
  Ürün içine AI ajanı yerleştirme: çok adımlı görev yapan asistan (araç seçimi, planlama,
  döngü), Claude Agent SDK / Managed Agents / Vercel AI SDK agent döngüsü, araç tasarımı ve
  izinler, insan onayı (human-in-the-loop) noktaları, ajan hafızası, uzun süren ajan işleri
  (arka planda), ilerlemeyi kullanıcıya gösterme, MCP sunucusu ile uygulamanı dışa açma,
  güvenlik ve maliyet sınırları. "Kendi işini yapan asistan", "AI ajan", "MCP sunucusu",
  "otomatik yapsın" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · AI Ajanları

Ajan = model + araçlar + döngü. Basit bir LLM çağrısı yetiyorsa ajan kurma; ajan **birden çok adım ve
karar** gerektiğinde değer katar ("bu haftaki iptalleri bul, boş slotları bekleme listesindekilere öner,
onay verince SMS at").

## Seçim

- Uygulama içi asistan, sunucunda araçlar: **Vercel AI SDK** (`streamText` + tools + `stopWhen`) veya Anthropic SDK tool runner.
- Kod/dosya/terminal yetenekli otonom ajan: **Claude Agent SDK**; yönetilen sandbox: Managed Agents.
- Uygulamanı başka AI'lara (Claude, ChatGPT, IDE'ler) açmak: **MCP sunucusu**.
Güncel API ayrıntıları için `claude-api` skill'ini yükle.

## Araç tasarımı (ajan kalitesinin %70'i)

- Az sayıda, iyi adlandırılmış, **tek amaçlı** araç: `searchClients`, `getAvailableSlots`, `draftSms`, `sendSms`.
- Açıklama: ne yapar, ne zaman kullanılır, girdi örneği. Zod şema ile parametre doğrulama.
- Çıktı kısa ve yapılandırılmış; hata mesajları **düzeltici** ("tarih geçmişte; bugünden sonra bir tarih ver").
- Okuma araçları serbest; **yazma/gönderme/silme/ödeme** araçları onay gerektirir.
- Araçlar kullanıcının yetkisiyle çalışır; org filtresi araç içinde zorunlu.

## İnsan onayı

```ts
sendSms: tool({
  description: "Onaylanan taslak SMS'leri gönderir",
  inputSchema: z.object({ draftIds: z.array(z.string()) }),
  needsApproval: true,          // UI'da "Gönder / Düzenle / Vazgeç" kartı çıkar
  execute: async ({ draftIds }) => sendDrafts(user, draftIds),
}),
```
Onay kartı **ne olacağını** net söyler: "12 kişiye SMS gönderilecek · tahmini maliyet ₺4,80". Kullanıcılar
kontrolde olduklarını hissettikçe ajana güvenir.

## Döngü sınırları

- Maks adım (ör. 8), maks süre (ör. 60 sn senkron; daha uzunsa arka plan işi), maks token/maliyet.
- Aynı aracı aynı girdiyle tekrar çağırma tespiti (döngüye girme).
- Başarısızlıkta zarif çıkış: "Şunları yaptım, şurada takıldım, şunu yapmamı ister misin?"

## İlerlemeyi göstermek

- Adım listesi canlı: "🔎 İptalleri arıyorum… ✓ 7 iptal bulundu → 📅 Boş slotlar… ✓ 9 slot → ✍️ Taslaklar hazır".
- Araç çağrılarını katlanabilir ayrıntı olarak göster (şeffaflık).
- Uzun işler arka planda (bkz. `sky-jobs`), bitince bildirim; kullanıcı sayfadan ayrılabilsin.

## Hafıza

- Kısa vadeli: konuşma geçmişi (uzunsa özetle).
- Uzun vadeli: kullanıcı tercihleri tablosu ("SMS'lerde 'siz' kullan", "cumartesi çalışmıyoruz") — ajan okur,
  kullanıcı görür ve siler. Gizli hafıza yok.
- Org bilgisi (hizmetler, çalışma saatleri) araçla getirilir, prompta gömülmez (güncel kalır).

## MCP sunucusu (uygulamanı AI'lara aç)

- `@modelcontextprotocol/sdk` ile; araçlar = uygulamanın API'si (okuma ağırlıklı başla).
- Kimlik: OAuth 2.1 (MCP auth spec) — kullanıcı kendi hesabıyla bağlar, kapsamlar dar.
- Uzak (Streamable HTTP) sunucu; route handler olarak barındırılabilir.
- "Claude'dan randevularımı yönet" — kullanıcıların çok sevdiği bir entegrasyon.

## Güvenlik

- Prompt injection: araç sonuçları ve kullanıcı içerikleri veri; yıkıcı adımlar her zaman onaylı (bkz. `sky-ai`).
- Kiracı izolasyonu araç seviyesinde test edilir (başka org'un verisine erişim denemesi eval'de).
- Audit log: ajanın yaptığı her yazma işlemi "ajan adına, kullanıcı X onayıyla" kaydı.
- Kota ve maliyet tavanı (bkz. `sky-metering-quotas`).

## Değerlendirme

Görev başarı oranı (senaryo setiyle), ortalama adım sayısı, onay reddi oranı, maliyet/görev. Bkz. `sky-ai-eval`.
