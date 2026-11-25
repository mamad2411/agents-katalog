---
name: sky-print-pdf
description: >-
  PDF üretimi ve yazdırma: fatura, makbuz, teklif, rapor, sertifika, bilet ve kargo etiketi
  PDF'leri; react-pdf vs Playwright (HTML→PDF) vs PDF servisleri seçimi, Türkçe font gömme,
  sayfa düzeni (A4, kenar boşluğu, sayfa sonu, başlık/altbilgi, sayfa numarası), QR kod ve
  barkod, print CSS (@media print, @page), "yazdır" butonu ve büyük PDF'leri arka planda
  üretme. "PDF oluştur", "fatura çıktısı", "sertifika", "yazdırılabilir sayfa" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · PDF & Yazdırma

## Hangi yöntem?

| İhtiyaç | Yöntem |
|---|---|
| Fatura, makbuz, bilet — sabit düzen, hızlı | **@react-pdf/renderer** |
| Mevcut HTML/Tailwind sayfasını birebir PDF yap | **Playwright/Puppeteer** `page.pdf()` |
| Sunucusuzda Chrome ağır | Gotenberg (Docker), Browserless, DocRaptor |
| Var olan PDF'e alan doldurma | **pdf-lib** |
| Kullanıcı sadece yazdıracak | **Print CSS** — PDF üretme |

## Türkçe font (en sık hata)

Varsayılan PDF fontları ğ, ş, İ, ı karakterlerini **göstermez**. Her zaman font göm:
```ts
Font.register({ family: "Inter", fonts: [
  { src: "/fonts/Inter-Regular.ttf" }, { src: "/fonts/Inter-SemiBold.ttf", fontWeight: 600 },
]});
```
Font dosyası `latin-ext` içermeli. Playwright yolunda `document.fonts.ready` bekle.

## react-pdf iskeleti (fatura)

```tsx
const s = StyleSheet.create({
  page: { padding: 40, fontFamily: "Inter", fontSize: 10, color: "#16161a" },
  row: { flexDirection: "row", justifyContent: "space-between" },
  num: { textAlign: "right" },
});
export const InvoicePdf = ({ inv }: { inv: Invoice }) => (
  <Document title={`Fatura ${inv.no}`} author={inv.seller.name} language="tr">
    <Page size="A4" style={s.page}>
      <View style={s.row}><Image src={inv.seller.logo} style={{ width: 96 }} /><Text>Fatura No: {inv.no}</Text></View>
      {/* alıcı/satıcı, kalemler tablosu, KDV, toplam */}
      <Text fixed style={{ position: "absolute", bottom: 24, right: 40 }}
        render={({ pageNumber, totalPages }) => `${pageNumber} / ${totalPages}`} />
    </Page>
  </Document>
);
// route handler: const buf = await renderToBuffer(<InvoicePdf inv={inv} />)
// Content-Type: application/pdf; Content-Disposition: inline; filename="fatura-2026-0042.pdf"
```
- Para/tarih tr-TR (bkz. `sky-i18n`); sayılar sağa hizalı.
- Uzun tabloda başlık satırı `fixed` ile her sayfada tekrar.
- Dosya adı anlamlı ve ASCII.

## Playwright yolu (HTML → PDF)

```ts
await page.goto(`${APP_URL}/print/invoice/${id}?token=${signedToken}`, { waitUntil: "networkidle" });
const pdf = await page.pdf({ format: "A4", printBackground: true,
  margin: { top: "16mm", bottom: "16mm", left: "14mm", right: "14mm" }, displayHeaderFooter: true,
  footerTemplate: `<div style="font-size:8px;width:100%;text-align:center"><span class="pageNumber"></span>/<span class="totalPages"></span></div>` });
```
- Yazdırma sayfası ayrı route, kısa ömürlü imzalı token ile.
- Tarayıcı örneğini yeniden kullan; her istekte Chrome başlatma.
- Ağır üretimi kuyruğa at, hazır olunca bildir (bkz. `sky-jobs`).

## Print CSS

```css
@page { size: A4; margin: 16mm 14mm; }
@media print {
  nav, footer, .no-print { display: none !important; }
  body { background: white; color: black; font-size: 11pt; }
  a[href^="http"]::after { content: " (" attr(href) ")"; font-size: 9pt; }
  h2, h3 { break-after: avoid; } tr, img, .card { break-inside: avoid; }
  * { print-color-adjust: exact; }
}
```
"Yazdır" butonu: `window.print()`; yazdırmada açık tema.

## İnsanların sevdiği PDF'ler

- **Sertifika:** isim büyük ve ortalı, imza görseli, benzersiz doğrulama kodu + **QR** (`qrcode`) →
  `site.com/dogrula/ABC123` sayfası sertifikanın gerçek olduğunu gösterir.
- **Etkinlik bileti:** QR kod, tarih/saat/konum, "Takvime ekle", isteğe bağlı Apple/Google Wallet pass.
- **Rapor:** kapak, içindekiler, grafikler (SVG), sayfa numaraları.
- **Kargo etiketi:** 10×15 cm termal boyut, barkod (`bwip-js`).

## Kontrol listesi

- [ ] Türkçe karakterler gömülü fontla doğru
- [ ] A4, kenar boşluğu, sayfa sonları; tablo başlığı tekrar ediyor
- [ ] Para/tarih tr-TR; dosya adı ASCII
- [ ] PDF metadata (title, author, language)
- [ ] Erişim kontrolü: başkasının faturası indirilemiyor
- [ ] Büyük üretim kuyrukta
