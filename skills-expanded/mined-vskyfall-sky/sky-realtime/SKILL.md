---
name: sky-realtime
description: >-
  Gerçek zamanlı özellikler: polling / SSE / WebSocket / Supabase Realtime / Pusher-Ably /
  Liveblocks seçimi, Next.js ve sunucusuz kısıtları, kanal yetkilendirmesi, yeniden bağlanma
  ve senkronizasyon, olay sıralama ve sürüm, optimistic UI ile uzlaşma, presence ve "yazıyor"
  göstergesi, çakışma çözümü (LWW vs CRDT/Yjs), ölçekleme (Redis pub/sub) ve test. Canlı
  liste, bildirim, sohbet, ortak düzenleme veya "anlık güncellensin" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Gerçek Zamanlı

## Önce: gerçekten gerekli mi?

| İhtiyaç | Yeterli çözüm |
|---|---|
| Veri dakikada bir değişir, kullanıcı bekleyebilir | **Polling** (TanStack Query `refetchInterval: 30_000`, sekme görünürken) |
| Sunucudan istemciye tek yön akış (bildirim, ilerleme, log) | **SSE** |
| İki yönlü, düşük gecikme (sohbet, oyun, imleç) | **WebSocket** veya yönetilen servis |
| Tablo değişince UI güncellensin, Supabase var | **Supabase Realtime** (Postgres Changes / Broadcast) |
| Ortak metin/çizim düzenleme | **CRDT** (Yjs + Liveblocks / PartyKit / Hocuspocus) |

Polling çoğu panel için yeter ve en az hata yüzeyi odur. Gerçek zamanlıya geçerken maliyeti
(bağlantı sayısı, sunucu durumu, yeniden bağlanma karmaşıklığı) kabul ettiğini bil.

## Next.js / sunucusuz kısıtı

Vercel benzeri sunucusuz ortamda **uzun ömürlü WebSocket sunucusu çalışmaz**. Seçenekler:
1. **SSE** route handler (streaming `Response`) — çalışır, ama fonksiyon süre sınırına tabi (yeniden bağlanma şart).
2. **Yönetilen servis**: Supabase Realtime, Pusher, Ably, PartyKit, Liveblocks — Next yalnızca yetki token'ı verir.
3. **Ayrı WebSocket sunucusu** (Node + `ws`/Socket.IO, Fly/Railway/VPS) — Next ile yan yana; ölçekte Redis adapter.

Varsayılan: Supabase varsa Realtime; yoksa SSE (tek yön) ya da Pusher/Ably (iki yön).

## SSE (route handler)

```ts
// app/api/events/route.ts
export const dynamic = "force-dynamic";
export async function GET(req: Request) {
  const user = await requireUser();
  const stream = new ReadableStream({
    start(controller) {
      const send = (event: string, data: unknown) =>
        controller.enqueue(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`);
      const unsubscribe = bus.subscribe(`user:${user.id}`, (e) => send(e.type, e.payload));
      const ping = setInterval(() => controller.enqueue(`: ping\n\n`), 25_000); // proxy zaman aşımı
      req.signal.addEventListener("abort", () => { clearInterval(ping); unsubscribe(); controller.close(); });
    },
  });
  return new Response(stream, { headers: { "Content-Type": "text/event-stream", "Cache-Control": "no-cache, no-transform", Connection: "keep-alive" } });
}
```
İstemci: `new EventSource("/api/events")` — tarayıcı otomatik yeniden bağlanır; `id:` satırı + `Last-Event-ID`
ile kaçırılanları yeniden gönder. Çok örnekli sunucuda `bus` Redis pub/sub olmalı.

## Supabase Realtime

- **Postgres Changes:** tabloya `INSERT/UPDATE/DELETE` dinle; **RLS geçerlidir** — kullanıcı yalnızca
  görebildiği satırların olaylarını alır. Yayın için tabloyu `supabase_realtime` publication'ına ekle.
  Büyük tablolarda filtre kullan (`filter: "org_id=eq.123"`).
- **Broadcast:** sunucu/istemciden geçici mesaj (imleç, "yazıyor"); DB'ye yazılmaz. Yetki için private
  channel + RLS politikası (`realtime.messages`).
- **Presence:** kim çevrim içi; `track({ userId, name })`, `sync/join/leave` olayları.
- İstemci tek `channel` örneği; bileşen unmount'ta `supabase.removeChannel`.
- Olay geldikten sonra UI'yi doğrudan payload'dan **değil**, TanStack Query `invalidateQueries` ile
  tazele (payload eksik/RLS'siz alan içerebilir); yüksek frekanslı olaylarda payload'u doğrudan
  cache'e `setQueryData` ile uygula.

## Yönetilen servisler (Pusher/Ably/PartyKit)

- Kanal adı yetki taşır: `private-org-123`, `presence-room-7`. Abonelikte sunucun **auth endpoint**i
  kullanıcının o kanala hakkı var mı kontrol eder ve imzalı token verir.
- Sunucudan yayın: olayı DB'ye yazdıktan **sonra** yayınla (önce yayınlarsan istemci olmayan veriyi çeker).
- Ücret bağlantı ve mesaj sayısına göre; yayın granülerliğini (oda bazlı) ona göre tasarla.

## İstemci kalıpları

**Yeniden bağlanma:** üstel geri çekilme (1s, 2s, 4s… maks 30s) + jitter; bağlandığında **tam senkron**
(`refetch`) — kaçırılan olaylar olabilir. Bağlantı durumunu UI'da göster ("Bağlantı yeniden kuruluyor…").

**Sıralama ve sürüm:** her kayıtta `version`/`updated_at`; gelen olay yereldekinden eskiyse at.
Olay ID'si ile tekilleştir (aynı olay iki kez gelebilir).

**Optimistic update + uzlaşma:**
```ts
useMutation({
  mutationFn: sendMessage,
  onMutate: async (msg) => { await qc.cancelQueries({ queryKey: ["messages", roomId] });
    const prev = qc.getQueryData(["messages", roomId]);
    qc.setQueryData(["messages", roomId], (old) => [...old, { ...msg, id: tempId, pending: true }]);
    return { prev }; },
  onError: (_e, _v, ctx) => qc.setQueryData(["messages", roomId], ctx.prev),
  onSettled: () => qc.invalidateQueries({ queryKey: ["messages", roomId] }),
});
```
Gerçek zamanlı olay geldiğinde `tempId`'li kaydı sunucu ID'siyle değiştir (istemci `clientId` gönderir, sunucu geri yansıtır).

**"Yazıyor" göstergesi:** `keydown`'da en fazla 2 sn'de bir broadcast; 3 sn olay gelmezse kapat. DB'ye yazma.

**Presence:** liste için `sync` olayında tam set; avatar yığını; 50+ kullanıcıda sayı göster.

**Sekme arka plandayken:** `document.visibilityState === "hidden"` → polling'i durdur, bağlantıyı açık tut ama
UI güncellemesini erteleyebilirsin; öne gelince `refetch`.

## Çakışma çözümü

- **Last-write-wins** (çoğu form/kart için yeter): `version` kontrolü; eski sürümle gelen güncelleme
  `409` → kullanıcıya "başkası değiştirdi, yenile" göster, körlemesine üzerine yazma.
- **Alan bazlı birleştirme:** farklı alanlar çakışmaz; aynı alan LWW.
- **CRDT (Yjs):** ortak metin, çizim, tablo. `y-websocket`/Hocuspocus/Liveblocks/PartyKit sağlayıcı;
  editör: TipTap + `@tiptap/extension-collaboration`. Belge snapshot'ını periyodik DB'ye yaz; geçmiş için `Y.encodeStateAsUpdate`.
- Kilitleme (pessimistic): "Ayşe düzenliyor" kilidi, 2 dk heartbeat, basit ama bloklayıcı; nadiren tercih.

## Ölçekleme ve dayanıklılık

- Çoklu sunucu → **Redis pub/sub** (veya Postgres `LISTEN/NOTIFY` küçük ölçek) ile olay dağıt.
- Bağlantı başına bellek; yetkisiz/boş bağlantıları 60 sn'de kapat; kullanıcı başına bağlantı limiti.
- Olay şeması sürümlü (`v: 1`); eski istemciler kırılmasın.
- Yük testi: `k6` WebSocket/SSE senaryoları; 1k eşzamanlı bağlantı hedefi önce.
- Güvenlik: kanal adında tahmin edilebilir ID yetki değildir; her abonelik sunucuda doğrulanır;
  mesaj boyutu sınırı; hız sınırı (kullanıcı başına sn'de N mesaj).

## Test

- Birim: olay indirgeyicileri (reducer) — sıra dışı, tekrar eden, eski sürüm olaylarla.
- Entegrasyon: iki istemci simülasyonu (Playwright iki `context`) — A yazar, B görür; bağlantı kesilip
  gelince B senkronlanır (`context.setOffline(true)`).
- SSE/WS sunucusu için `ws` istemcisiyle bağlan-yetkisiz-ret testi.

## Kontrol listesi

- [ ] Polling'in yetmediği gerekçelendirildi
- [ ] Kanal/abonelik yetkisi sunucuda; RLS veya auth endpoint
- [ ] Yeniden bağlanma + tam senkron; bağlantı durumu UI'da
- [ ] Olay tekilleştirme ve sürüm kontrolü
- [ ] Optimistic UI hata durumunda geri alınıyor
- [ ] Çoklu sunucu için pub/sub planı
- [ ] Unmount'ta abonelik temizleniyor (sızıntı yok)
