---
name: sky-bots
description: >-
  Sohbet botları ve entegrasyonlar: Telegram (grammY), Discord (discord.js — slash komutlar,
  butonlar, modallar), Slack (Bolt — komutlar, etkileşimli mesajlar), WhatsApp Business Cloud
  API (resmi, şablon mesajlar), webhook vs polling, komut tasarımı ve konuşma akışları, oturum/
  durum saklama, imza doğrulama, rate limit, barındırma (sunucusuz/konteyner), AI destekli bot
  ve kötüye kullanım önleme. "Telegram botu", "Discord botu", "Slack uygulaması", "WhatsApp
  botu" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Botlar

## Platform ve kütüphane

| Platform | Kütüphane | Not |
|---|---|---|
| Telegram | **grammY** (TS), python-telegram-bot | en kolayı; BotFather'dan token, inline klavyeler, ödemeler |
| Discord | **discord.js**, discord.py | slash komutları, butonlar, select menüler, modallar, roller |
| Slack | **Bolt** (JS/Python) | slash komut, Block Kit etkileşimli mesajlar, App Home |
| WhatsApp | **Meta WhatsApp Cloud API** (resmi) veya BSP | onaylı şablonlar, 24 saatlik oturum penceresi |
Resmi olmayan WhatsApp kütüphaneleri (WhatsApp Web otomasyonu) hizmet şartlarını ihlal eder ve numara kapatılabilir — iş için resmi API kullan.

## Telegram (grammY)

```ts
import { Bot, InlineKeyboard, session } from "grammy";
const bot = new Bot(process.env.TELEGRAM_TOKEN!);
bot.use(session({ initial: () => ({ step: "idle" as "idle" | "awaiting_date" }) }));

bot.command("start", (ctx) => ctx.reply("Merhaba! Randevu almak için /randevu yaz."));
bot.command("randevu", async (ctx) => {
  const kb = new InlineKeyboard().text("Bugün", "day:0").text("Yarın", "day:1");
  await ctx.reply("Hangi gün?", { reply_markup: kb });
});
bot.callbackQuery(/^day:(\d)$/, async (ctx) => {
  const slots = await getSlots(Number(ctx.match[1]));
  await ctx.answerCallbackQuery();
  await ctx.editMessageText("Uygun saatler:", { reply_markup: slotsKeyboard(slots) });
});
bot.catch((err) => log.error({ err }, "bot hatası"));
```
Üretimde **webhook** (`webhookCallback(bot, "hono")` ile route handler); geliştirmede long polling (`bot.start()`).
Webhook'ta `secret_token` başlığını doğrula.

## Discord (discord.js)

- Slash komutlarını kaydet (`REST` + `Routes.applicationGuildCommands` geliştirmede, global üretimde).
- `interactionCreate` → `isChatInputCommand()` / `isButton()`; 3 sn içinde yanıt ver veya `deferReply()` (uzun işler).
- En az yetki: gerekli **intent**'ler (MessageContent ayrıcalıklı intent'tir — gerçekten gerekmedikçe isteme), bot rol izinleri.
- Sunucusuz mümkün: HTTP interactions uç noktası (Ed25519 imza doğrulamalı) — gateway bağlantısı gerektirmeyen botlar için.

## Slack (Bolt)

Slash komut + Block Kit (butonlar, seçiciler, modal formlar), App Home sekmesi, olay abonelikleri; istek imzası (`X-Slack-Signature`) doğrulaması Bolt'ta yerleşik;
3 sn kuralı (`ack()` hemen, iş sonra). Kurulum: OAuth ile çalışma alanına yükleme, token'ları çalışma alanı başına sakla.

## WhatsApp Cloud API

- Webhook: doğrulama (`hub.verify_token`) + `X-Hub-Signature-256` imza kontrolü.
- Kullanıcı 24 saat içinde yazdıysa serbest mesaj; değilse **onaylı şablon** (randevu hatırlatma, sipariş durumu) — şablonlar Meta onayından geçer.
- Etkileşimli mesajlar: butonlar (en fazla 3), listeler; Flows ile form benzeri akışlar.
- Rıza: kullanıcının açık onayı; ticari iletilerde İYS kuralları (bkz. `sky-tr-integrations`, `sky-notifications`).

## Konuşma tasarımı

- Komut + buton ağırlıklı akış serbest metinden daha güvenilir; her adımda "İptal" ve "Geri".
- Durum (hangi adımda) sunucuda (Redis/DB) — sunucusuzda bellek kaybolur.
- Kısa mesajlar, emoji ölçülü, hata durumunda yönlendirici ("Bu tarihi anlayamadım, örn: 5 Kasım").
- AI ile serbest dil anlama (bkz. `sky-ai`) — ama kritik eylemlerde (ödeme, iptal) buton onayı.

## Güvenlik ve işletim

- Token'lar env'de; sızarsa platformdan hemen yenile.
- Tüm webhook isteklerinde imza doğrulama; yönetici komutları kullanıcı ID izin listesiyle.
- Platform rate limitlerine uy (toplu mesajda kuyruk + gecikme, bkz. `sky-jobs`); spam yapma — botlar kapatılır.
- Barındırma: webhook botları sunucusuz (Vercel/Workers) çalışır; Discord gateway botu sürekli süreç ister (Fly/Railway/VPS).
- Log ve hata izleme (bkz. `sky-observability`); kişisel veriyi loglama.
