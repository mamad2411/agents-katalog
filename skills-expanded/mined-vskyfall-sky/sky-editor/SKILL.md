---
name: sky-editor
description: >-
  Zengin metin editörü ve içerik yazımı: TipTap / Lexical / Plate / BlockNote seçimi, Notion
  tarzı slash menüsü, blok editör, Markdown kısayolları, mention (@kişi), görsel yapıştırma ve
  yükleme, bağlantı önizleme, yapıştırma temizliği, JSON/HTML saklama, sanitize ve render,
  ortak düzenleme (Yjs), karakter sayacı ve otomatik kayıt. "Editör ekle", "Notion gibi",
  "blog yazma ekranı", "rich text" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Zengin Metin Editörü

## Seçim

| İhtiyaç | Seçim |
|---|---|
| Esnek, eklentili, ProseMirror tabanlı, iyi doküman | **TipTap** (varsayılan) |
| Meta'nın, performanslı, kendi düğüm modeli | **Lexical** |
| shadcn uyumlu hazır blok editör | **Plate** |
| Notion klonu hissi hemen | **BlockNote** (hazır blok UI) |
| Sadece Markdown yeter | `textarea` + önizleme veya **MDXEditor** |

Kural: kullanıcı yalnızca kısa biçimli metin giriyorsa (yorum, açıklama) tam editör koyma; 4–5 butonlu
minimal araç çubuğu veya Markdown yeter.

## İnsanların sevdiği detaylar

- **Slash menüsü** (`/`): başlık, liste, alıntı, kod, görsel, tablo, ayraç — klavyeyle filtrelenir.
- **Markdown kısayolları:** `# ` başlık, `- ` liste, `> ` alıntı, `**kalın**`, `---` ayraç.
- **Bubble menü:** metin seçince üstte küçük araç çubuğu (kalın, italik, bağlantı, vurgu).
- **Sürükle tutamacı** (⋮⋮) ile blokları taşıma.
- **Görsel yapıştır / sürükle** → anında yükle, yer tutucu + ilerleme, sonra gerçek URL.
- **Bağlantı yapıştır** → seçili metin üzerine yapıştırınca otomatik bağlantı; tek başına URL → önizleme kartı.
- **@mention** ve `#etiket` önerisi.
- **Otomatik kayıt** + "Kaydedildi · 2 sn önce" göstergesi; çevrimdışı taslak (localStorage).
- **Karakter/kelime sayacı** ve okuma süresi.
- **Odak modu** (araç çubukları gizlenir), tam ekran.

## TipTap kurulum iskeleti

```tsx
const editor = useEditor({
  extensions: [
    StarterKit.configure({ heading: { levels: [2, 3] } }),   // h1 sayfa başlığına ayrılır
    Placeholder.configure({ placeholder: "Yazmaya başla… komutlar için / yaz" }),
    Link.configure({ openOnClick: false, autolink: true, protocols: ["https", "mailto"] }),
    Image.configure({ allowBase64: false }),
    CharacterCount.configure({ limit: 20000 }),
    Mention.configure({ suggestion: mentionSuggestion }),
    Typography,                                            // “akıllı” tırnak, … , — dönüşümleri
  ],
  content: initialJSON,
  immediatelyRender: false,                                // Next SSR hydration için
  onUpdate: ({ editor }) => debouncedSave(editor.getJSON()),
});
```

## Saklama ve render

- **JSON sakla** (belge JSON'u): şema bilinçli, dönüştürülebilir, güvenli.
  Gösterim için sunucuda HTML'e çevir (`generateHTML`) ve **cache'le**.
- HTML saklıyorsan: kaydederken **ve** render ederken sanitize (DOMPurify / `sanitize-html`),
  izinli etiket/öznitelik listesiyle. `javascript:` URL'leri, `on*` öznitelikleri temizlenir.
- Arama/özet için ayrıca düz metin sütunu (`editor.getText()`).
- Belge şeması değişirse JSON migration fonksiyonu (sürüm alanı).

## Yapıştırma temizliği

Word/Google Docs yapıştırması stil çöpü getirir: `transformPastedHTML` ile `style`, `class`, `font`
temizle; yalnızca anlamsal yapı kalsın. Görsel yapıştırılırsa data URI'yi yakala → yükle → URL ile değiştir.

## Görsel yükleme

- Doğrudan depolamaya imzalı URL (bkz. `sky-storage`); istemcide küçült (bkz. `sky-media`).
- Yükleme sırasında bulanık önizleme; hata olursa blokta "Tekrar dene".
- Görsel seçilince `alt` metni alanı (erişilebilirlik).

## Ortak düzenleme

TipTap Collaboration + Yjs + sağlayıcı (Hocuspocus / Liveblocks / PartyKit); renkli imleçler ve isimler.
Detay: `sky-realtime`.

## Erişilebilirlik ve i18n

- Editör `role="textbox" aria-multiline="true"` + görünür etiket.
- Araç çubuğu butonlarında `aria-pressed` ve kısayol tooltip'i ("Kalın · ⌘B").
- Türkçe yazım denetimi: `spellcheck` + `lang="tr"`.
- Mobilde araç çubuğu klavyenin üstüne yapışık.

## Güvenlik kontrol listesi

- [ ] Saklanan içerik JSON veya sanitize edilmiş HTML
- [ ] Render öncesi sanitize (stored XSS)
- [ ] Kullanıcı bağlantıları `rel="noopener noreferrer nofollow ugc"`
- [ ] Gömülü içerik (YouTube vb.) izinli liste
- [ ] Görsel yükleme MIME/boyut kontrolü sunucuda
