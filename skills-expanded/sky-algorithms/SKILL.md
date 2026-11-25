---
name: sky-algorithms
description: >-
  Algoritma ve veri yapıları (pratik ve mülakat): Big-O sezgisi, doğru veri yapısını seçme
  (dizi, hash map/set, yığın, kuyruk, deque, heap, ağaç, trie, graf, union-find), sık çözüm
  kalıpları (iki işaretçi, kayan pencere, önek toplamı, ikili arama, BFS/DFS, topolojik sıralama,
  geri izleme, dinamik programlama, açgözlü, aralık birleştirme), gerçek uygulama örnekleri
  (slot üretimi, öneri, arama) ve kodlama mülakatı yaklaşımı. Algoritma sorusu, performans
  problemi veya "LeetCode" sorusunda kullan.
disable-model-invocation: true
---

# Sky · Algoritmalar & Veri Yapıları

## Big-O sezgisi

| n | O(n²) | O(n log n) | O(n) |
|---|---|---|---|
| 1.000 | 1M ✓ | 10k ✓ | ✓ |
| 100.000 | 10^10 ✗ | 1,7M ✓ | ✓ |
~10^8 basit işlem/sn kabaca. Web'de klasik tuzak: iç içe döngüde `array.find` / `includes` → O(n²); çözüm: önce `Map`/`Set`'e koy (O(n)).

## Veri yapısı seçimi

| İhtiyaç | Yapı | JS/TS |
|---|---|---|
| Var mı? / tekilleştir | Hash set | `Set` |
| Anahtarla bul / say / grupla | Hash map | `Map`, `Object.groupBy` |
| LIFO (geri al, parantez eşleşmesi) | Yığın | dizi `push/pop` |
| FIFO (BFS, iş sırası) | Kuyruk | dizi + baş indeksi (shift O(n)) |
| En küçük/büyük k, öncelik | Heap | kendi heap'in / kütüphane |
| Sıralı + aralık sorgusu | Dengeli ağaç / sıralı dizi + ikili arama | — |
| Önek arama (autocomplete) | Trie | — |
| İlişkiler, yollar | Graf (komşuluk listesi) | `Map<id, id[]>` |
| Bağlı bileşenler, gruplama | Union-Find | — |

## Kalıplar

**İki işaretçi** (sıralı dizide çift bulma, tersine çevirme, birleştirme):
```ts
let i = 0, j = a.length - 1;
while (i < j) { const s = a[i] + a[j]; if (s === target) return [i, j]; s < target ? i++ : j--; }
```
**Kayan pencere** (en uzun/kısa alt dizi, ardışık k eleman):
```ts
let best = 0, left = 0; const seen = new Map<string, number>();
for (let right = 0; right < s.length; right++) {
  if (seen.has(s[right]) && seen.get(s[right])! >= left) left = seen.get(s[right])! + 1;
  seen.set(s[right], right); best = Math.max(best, right - left + 1);
}
```
**Önek toplamı** (aralık toplamları O(1)): `pre[i+1] = pre[i] + a[i]`, toplam(l..r) = `pre[r+1] - pre[l]`.
**İkili arama** (sıralı veride veya "cevap üzerinde" — en küçük uygun değer): `while (lo < hi) { mid = (lo+hi) >> 1; ok(mid) ? hi = mid : lo = mid + 1; }`
**BFS** en kısa yol (ağırlıksız), **DFS** keşif/bileşenler, **Dijkstra** ağırlıklı (heap ile), **topolojik sıralama** bağımlılık sırası (görev planlama, build sırası — Kahn algoritması).
**Geri izleme** (permütasyon, kombinasyon, alt küme, bulmaca): seç → in → geri al; budama ile hızlandır.
**Dinamik programlama**: alt problemler örtüşüyorsa — durum tanımı, geçiş, temel durum; önce memoize özyineleme, sonra tablo.
**Açgözlü**: yerel en iyi seçim kanıtlanabiliyorsa (aralık planlama: bitişe göre sırala).
**Aralık birleştirme**: başlangıca göre sırala, çakışanları birleştir — takvim/slot işlerinde çok kullanılır.

## Gerçek dünyadan

- **Boş slot bulma** (bkz. `sky-scheduling`): çalışma aralıklarından dolu aralıkları çıkar = aralık birleştirme + fark; O(n log n).
- **Benzer isim önerisi**: Levenshtein mesafesi (DP) — "Bunu mu demek istedin?" (bkz. `sky-search`).
- **Autocomplete**: trie veya sıralı dizi + ikili arama; büyük ölçekte arama motoru.
- **Bağımlılık sırası**: topolojik sıralama (migration'lar, görev akışları); döngü tespiti.
- **Top-k** (en çok satan 10 ürün): heap veya kısmi sıralama; DB'de `order by … limit`.
- **Rate limiting**: kayan pencere / token bucket.
- **Tekilleştirme**: hash set; çok büyük veri ve kabul edilebilir yanlış pozitif → Bloom filter.

## Kodlama mülakatı yaklaşımı

1. Soruyu kendi cümlenle tekrar et, örnek girdi/çıktı ve kenar durumları sor (boş, tek eleman, negatif, tekrarlar, çok büyük).
2. Önce kaba kuvvet + karmaşıklığı söyle, sonra iyileştir (hangi tekrar eden iş var? hash map? sıralama? pencere?).
3. Kodu yaz, değişken isimleri anlamlı.
4. Örnekle elle izle, kenar durumları test et.
5. Zaman/alan karmaşıklığını söyle.
