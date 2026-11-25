---
name: sky-date-time
description: >-
  Tarih ve saat: Türkiye saati, resmi tatiller, Türkçe tarih biçimi, saat dilimi, takvim, "şimdi açık"
  rozeti, takvime ekle. "Tarih seçici", "takvim", "saat dilimi" dendiğinde kullan.
---

# Sky · Tarih & Saat

## Altın kurallar

1. **An (instant)** → `timestamptz` / ISO 8601 UTC.
2. **Yalnızca tarih** (doğum günü, tatil) → `date` tipi; asla `Date` objesiyle gece yarısı UTC'ye çevirme (gün kayar).
3. **Duvar saati + dilim** (randevu "14:30 İstanbul") → yerel saat + `timeZone` alanı, ya da UTC + dilim.
4. **Göster:** her zaman kullanıcının dilimi ve locale'i (`Intl.DateTimeFormat`).
5. **Hesapla:** kütüphane (Temporal/date-fns), elle milisaniye toplama değil.

## Araçlar

- **Temporal**: `PlainDate`, `PlainTime`, `ZonedDateTime`, `Instant` — doğru model.
- **date-fns** + `@date-fns/tz`: olgun, ağaç sallanır, `tr` locale'i var.
- **Day.js**: küçük. **Moment**: yeni projede kullanma.

```ts
formatDistanceToNowStrict(date, { addSuffix: true, locale: tr });          // "3 dakika önce"
new Intl.RelativeTimeFormat("tr", { numeric: "auto" }).format(-1, "day"); // "dün"
```

## Göreli zaman deneyimi

- < 1 dk "az önce"; < 1 saat "12 dk önce"; bugün "14:32"; dün "Dün 14:32"; bu yıl "5 Kas"; eski "5 Kas 2024".
- Üzerine gelince tam tarih: `<time dateTime={iso} title={tamTarih}>`.
- Dakikada bir canlı güncelle; ilk render mutlak, istemcide göreliye geç (hydration).

## Tarih/saat seçici UI

- Mobilde **native** `<input type="date">` / `type="time"` çoğu zaman en iyisi.
- Masaüstünde takvim popover'ı (react-day-picker / shadcn `Calendar`), Türkçe, **pazartesi başlangıç**.
- Kısayollar: "Bugün", "Yarın", "Gelecek hafta"; doğal dil girişi ("yarın 15:00").
- Geçmiş/devre dışı günler soluk; tatiller işaretli; seçili aralık vurgulu.
- Saat seçiminde 15/30 dk adımları, dolu slotlar devre dışı (bkz. `sky-scheduling`).
- Doğum tarihi için takvim değil: `GG.AA.YYYY` maskeli tek alan.

## Takvim görünümleri

- **FullCalendar**, **Schedule-X**, **react-big-calendar** veya basit ay ızgarası.
- Ay görünümü 6×7 sabit (zıplamasın), bugün halkası, gün başına 3 olay + "+2 daha".
- Hafta/gün görünümü: saat çizgileri, **"şimdi" kırmızı çizgisi**, sürükleyerek oluştur/taşı/uzat.
- Mobilde ajanda (liste) görünümü.

## Tekrarlayan olaylar (RRULE)

- `rrule`: `RRULE:FREQ=WEEKLY;BYDAY=MO,WE;UNTIL=20261231T000000Z`.
- Kural + istisnalar (`EXDATE`); "bu ve sonrakileri değiştir" için kuralı böl.
- UI özeti Türkçe: "Her hafta Pazartesi ve Çarşamba, 31 Aralık'a kadar".
- Örnekleri görünen aralık için sorgu anında üret; hepsini DB'ye yazma.

## Çalışma saatleri ve tatiller

- `business_hours(weekday, open, close)` + `closures(date, reason)`.
- **"Şimdi açık · 21:00'e kadar" / "Kapalı · yarın 09:00'da açılıyor"** rozeti (kullanıcılar bayılır).
- Türkiye resmi tatilleri: sabitler (1 Ocak, 23 Nisan, 1 Mayıs, 19 Mayıs, 15 Temmuz, 30 Ağustos, 29 Ekim)
  + dinî bayramlar (her yıl değişir, arife yarım gün) → yıllık veri veya `date-holidays` (`TR`).

## Geri sayım

- "3 gün 04:12:55" — `tabular-nums` ile rakamlar zıplamasın.
- Sunucu saatine göre (istemci saati yanlış olabilir): yüklemede sunucu `now` gönder, farkı tut.
- Bitince net durum değişikliği ("Başladı! 🎉").

## Takvime ekle

- `.ics` (`ics` paketi): `DTSTART;TZID=Europe/Istanbul`, `UID`, `SUMMARY`, `LOCATION`, `VALARM` hatırlatıcı.
- Google: `https://calendar.google.com/calendar/render?action=TEMPLATE&text=…&dates=20261105T113000Z/20261105T123000Z&location=…`
- Outlook web bağlantısı; Apple için .ics. Üçünü tek "Takvime ekle ▾" menüsünde sun.
- Onay e-postalarına .ics eki → randevu otomatik takvime düşer.

## Sık hatalar

| Hata | Doğrusu |
|---|---|
| `new Date("2026-11-05")` → UTC gece yarısı, bazı dilimlerde bir gün önce | date-only string / `PlainDate` |
| Sunucuda `toLocaleString()` arg'sız | `Intl.DateTimeFormat("tr-TR", { timeZone })` |
| Gün farkı = ms / 86400000 | `differenceInCalendarDays` |
| 31 Ocak + 1 ay elle | kütüphane |
| Hafta pazar başlıyor | `weekStartsOn: 1` |
| `timestamp without time zone` | `timestamptz` |
