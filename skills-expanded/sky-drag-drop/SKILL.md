---
name: sky-drag-drop
description: >-
  Sürükle-bırak etkileşimleri: dnd-kit ile sıralanabilir listeler, kanban panosu (sütunlar
  arası taşıma), ızgara yeniden düzenleme, dosya bırakma alanları, sürükleme önizlemesi ve
  animasyonları, dokunmatik destek, klavye ile sürükleme ve Türkçe ekran okuyucu duyuruları,
  sırayı kalıcılaştırma (fractional indexing) ve optimistic UI. "Sürükle bırak", "kanban",
  "sıralanabilir liste", "Trello gibi" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Sürükle-Bırak

## Kütüphane

- **dnd-kit** (`@dnd-kit/core` + `@dnd-kit/sortable`): varsayılan; erişilebilir, dokunmatik, esnek.
- **Pragmatic drag and drop** (Atlassian): performanslı, büyük listeler.
- **Framer Motion `Reorder`**: basit tek liste için en az kod, güzel animasyon.
- Native HTML5 DnD tek başına: dokunmatikte çalışmaz — yalnızca dosya bırakma için.

## Sıralanabilir liste (dnd-kit)

```tsx
const sensors = useSensors(
  useSensor(PointerSensor, { activationConstraint: { distance: 6 } }),   // tıklamayla karışmasın
  useSensor(TouchSensor, { activationConstraint: { delay: 180, tolerance: 6 } }), // mobilde uzun bas
  useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates }),
);
<DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={onDragEnd}
  accessibility={{ announcements: trAnnouncements }}>
  <SortableContext items={ids} strategy={verticalListSortingStrategy}>
    {items.map((i) => <SortableRow key={i.id} item={i} />)}
  </SortableContext>
  <DragOverlay>{activeItem && <RowPreview item={activeItem} />}</DragOverlay>
</DndContext>
```

## Kanban panosu

- Sütunlar yatay `SortableContext`, kartlar her sütunda dikey `SortableContext`.
- `onDragOver` ile kart sütun değiştirir (anlık önizleme), `onDragEnd` ile kalıcılaştır.
- Boş sütuna bırakılabilir alan (min-height + "Buraya bırak" ipucu).
- Sütun başlığında kart sayısı ve WIP limiti ("3/5"); aşılırsa sütun uyarı rengi.
- Kenara yaklaşınca otomatik kaydırma.

## Hissettirme detayları

- **Tutamak** (⋮⋮) hover'da belirir; imleç `grab` / `grabbing`.
- Sürüklenen öğe hafif büyür (`scale(1.02)`), gölge alır, kanban kartında hafif döner (`rotate(2deg)`).
- Yerinde kalan "hayalet" (soluk, kesikli kenarlık) nereden geldiğini gösterir.
- Diğer öğeler yumuşakça yer açar (200ms ease-out); bırakınca spring ile yerleşir.
- Mobilde `navigator.vibrate(10)` dokunsal geri bildirim.
- Geçersiz bırakma alanında imleç `not-allowed`.
- `prefers-reduced-motion`'da animasyonlar anlık.

## Erişilebilirlik (zorunlu)

- Klavye: Tab ile tutamağa gel → Boşluk ile al → oklarla taşı → Boşluk bırak / Esc iptal.
- Türkçe duyurular:
```ts
const trAnnouncements = {
  onDragStart: ({ active }) => `${label(active)} alındı. Ok tuşlarıyla taşı, Boşluk ile bırak, Esc ile iptal et.`,
  onDragOver: ({ active, over }) => over ? `${label(active)}, ${label(over)} üzerinde.` : `${label(active)} bırakılabilir alanın dışında.`,
  onDragEnd: ({ active, over }) => over ? `${label(active)}, ${label(over)} konumuna bırakıldı.` : `${label(active)} bırakıldı.`,
  onDragCancel: ({ active }) => `Taşıma iptal edildi. ${label(active)} eski yerine döndü.`,
};
```
- **Alternatif yol** (WCAG 2.5.7): her öğede "…" menüsü → "Yukarı taşı / Aşağı taşı / Sütuna taşı".

## Sırayı kalıcılaştırma

- **Fractional indexing** (`fractional-indexing`): her öğede `position` string'i; taşınınca yalnızca
  **taşınan öğe** güncellenir (`generateKeyBetween(a, b)`). Tüm listeyi yeniden numaralandırma.
- Optimistic: UI'ı hemen güncelle, sunucuya tek PATCH; hata olursa geri al + toast.
- Çok kullanıcılı panoda değişikliği yayınla (bkz. `sky-realtime`).

## Dosya bırakma alanı

- `react-dropzone`: sayfaya dosya sürüklenince **tam ekran katman** ("Dosyaları buraya bırak") — insanlar bayılır.
- Kabul edilen türler/boyut alanda yazılı; reddedilen dosya için net neden.
- Klasik "Dosya seç" butonu her zaman.
- Bırakılan dosyalar yükleme kartları olarak listelenir (bkz. `sky-media`).

## Performans

- 200+ öğe → sanallaştırma veya Pragmatic DnD.
- Öğe bileşenini `memo`; aktif id'yi context'ten değil dnd-kit hook'larından al.
