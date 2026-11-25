---
name: sky-state
description: >-
  State mimarisi: hangi veri nerede yaşar (URL, sunucu cache, form, yerel UI, global istemci,
  kalıcı), state'i türetme, Zustand slice kalıpları, context bölme, XState/durum makinesi ne
  zaman, nuqs ile URL state, optimistic güncelleme ve "prop drilling mi context mi" kararları.
  "State nerede tutulsun", "her şey yeniden render oluyor", "Redux gerekir mi", "global state"
  dendiğinde kullan.
disable-model-invocation: true
---

# Sky · State Mimarisi

## Karar ağacı: bu veri nerede yaşamalı?

```
Sunucudan mı geliyor?             → Sunucu state'i: RSC / TanStack Query. ASLA useState'e kopyalama.
Paylaşılabilir/yer imi olmalı mı?  → URL (searchParams, nuqs): filtre, sekme, sayfa, sıralama, seçili öğe.
Form verisi mi?                    → Form kütüphanesi (RHF) veya native form + action.
Tek bileşene mi ait?               → useState / useReducer.
Birkaç kardeş mi paylaşıyor?       → En yakın ortak ebeveyne kaldır.
Uzak, çok yerde mi okunuyor?       → Context (seyrek değişen) veya Zustand (sık değişen).
Yenilemeden sonra kalmalı mı?      → localStorage (tercih), çerez (SSR'da gerekiyorsa), DB (cihazlar arası).
Başka değerden hesaplanabiliyor mu? → State DEĞİL; render'da hesapla.
```

En sık hata: sunucu verisini `useState`e kopyalayıp senkron tutmaya çalışmak. İkinci en sık:
URL'de olması gereken filtreyi state'te tutup paylaşılamaz yapmak.

## Türetme

```tsx
// ✗ senkron tutulması gereken iki state
const [items, setItems] = useState(data);
const [count, setCount] = useState(data.length);
// ✓ tek kaynak, gerisi türetilir
const visible = items.filter((i) => i.status === filter);
const count = visible.length;
```
Pahalıysa `useMemo` (ölç). "Prop değişince state'i sıfırla" ihtiyacı → `key` ile bileşeni yeniden bağla:
`<Editor key={doc.id} doc={doc} />`.

## useReducer

3+ ilişkili alan veya birbirine bağlı geçişler varsa: `useReducer` + discriminated union action'lar
(bkz. `sky-typescript`). Reducer saf fonksiyon → kolay test.

## Context ölçüsü

- Seyrek değişen değerler için: tema, oturum kullanıcısı, locale, feature flag'ler.
- Her değişimde tüm tüketiciler render olur → sık değişen değeri context'e koyma.
- Değer ve setter'ı ayrı context'lere böl; value objesini `useMemo` ile sabitle.
- Provider'ı ihtiyaç duyulan alt ağaca indir; kök layout'ta 12 provider kuleleri kurma.

## Zustand (varsayılan global istemci state)

```ts
type CartSlice = { items: Item[]; add: (i: Item) => void; remove: (id: string) => void };
export const useCart = create<CartSlice>()(persist((set) => ({
  items: [],
  add: (i) => set((s) => ({ items: [...s.items, i] })),
  remove: (id) => set((s) => ({ items: s.items.filter((x) => x.id !== id) })),
}), { name: "cart-v1" }));

// tüketici yalnızca ihtiyacını seçer → yalnızca o değişince render
const count = useCart((s) => s.items.length);
```
- Obje döndüren selector → `useShallow`. Store'u slice'lara böl; aksiyonları store içinde tut.
- SSR'da (Next) store'u modül seviyesinde paylaşma — istekler arası sızar. İstek başına store için
  context + `createStore` kalıbı.
- `persist` anahtarına sürüm koy (`cart-v1`); şema değişince `migrate`.

## URL state (nuqs)

```ts
const [tab, setTab] = useQueryState("tab", parseAsStringLiteral(["genel", "fatura"]).withDefault("genel"));
```
Geri tuşu, paylaşım, yenileme bedava. `shallow: false` ile sunucu bileşenlerini de tetikle.
Sık değişen (yazarken) değerlerde `throttleMs`.

## Durum makinesi (XState) ne zaman?

Çok adımlı sihirbaz, ödeme akışı, medya oynatıcı, sürükle-bırak, "imkânsız durum" hatalarının
tekrarlandığı yerler. Basit durumlar için discriminated union + reducer yeter; XState'i her yere koyma.

## Optimistic güncelleme

- React 19 `useOptimistic` (server action ile) veya TanStack Query `onMutate` + geri alma.
- Yalnızca geri alınabilir ve yüksek başarı olasılıklı işlemlerde (beğeni, sıralama, onay kutusu).
- Ödeme, silme, kalıcı işlemler: bekle + göster.

## Kokular → tedavi

| Koku | Tedavi |
|---|---|
| `useEffect(() => setX(f(y)), [y])` | Türet: `const x = f(y)` |
| Sunucu verisi `useState(initialData)` | Query/RSC'den doğrudan oku |
| 5 seviye prop geçişi | Composition (`children`) önce, sonra context/store |
| Her tuşta tüm sayfa render | State'i input'a indir, `useDeferredValue` |
| Global store'da form taslağı | Form kütüphanesinde tut, gerekiyorsa sessionStorage |
| `isLoading && isError && data` kombinasyonları | Discriminated union |
