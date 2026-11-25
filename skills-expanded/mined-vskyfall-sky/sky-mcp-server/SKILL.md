---
name: sky-mcp-server
description: >-
  MCP (Model Context Protocol) sunucusu yazma: kavramlar (tools, resources, prompts), TypeScript
  SDK ile sunucu (Zod girdi şemaları, yapılandırılmış çıktı), stdio ve Streamable HTTP taşıma,
  uzak sunucuda OAuth ile kimlik doğrulama, araç tasarımı (az ve net araç, iyi açıklama,
  düzeltici hata mesajları), sayfalama ve büyük çıktılar, güvenlik (en az yetki, onay gerektiren
  işlemler, prompt injection), MCP Inspector ile test ve Claude Code / Claude Desktop'a ekleme.
  "MCP sunucusu yaz", "uygulamamı Claude'a bağla" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · MCP Sunucusu

MCP, uygulamanı/verini AI istemcilerine (Claude Code, Claude Desktop, IDE'ler) standart bir arayüzle açar. Ürün içi ajan tasarımı için `sky-ai-agents`;
güncel SDK ayrıntıları için resmi MCP dokümanı ve `claude-api` skill'i.

## Kavramlar

- **Tools**: modelin çağırdığı eylemler (`search_bookings`, `create_booking`) — en çok kullanılan.
- **Resources**: okunabilir içerik (dosya, kayıt, doküman) — URI ile.
- **Prompts**: kullanıcının seçebileceği hazır istem şablonları.

## TypeScript SDK ile sunucu (stdio)

```ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "sky-bookings", version: "1.0.0" });

server.registerTool(
  "search_bookings",
  {
    title: "Randevu ara",
    description: "Tarih aralığına ve müşteri adına göre randevuları listeler. Tarihler ISO (YYYY-MM-DD). En fazla 50 sonuç döner.",
    inputSchema: { from: z.string().date(), to: z.string().date(), client: z.string().optional(), cursor: z.string().optional() },
  },
  async ({ from, to, client, cursor }) => {
    const page = await api.searchBookings({ from, to, client, cursor, limit: 50 });
    return {
      content: [{ type: "text", text: JSON.stringify({ items: page.items.map(toSummary), nextCursor: page.nextCursor }) }],
    };
  },
);

await server.connect(new StdioServerTransport());
```
Loglar **stderr**'e (stdio'da stdout protokol kanalıdır — `console.log` iletişimi bozar).
API'ler sürümden sürüme değişebilir; kurulu SDK sürümünün dokümanına bak.

## Taşıma

- **stdio**: yerel süreç (istemci başlatır) — kişisel araçlar, yerel dosya/DB erişimi.
- **Streamable HTTP**: uzak sunucu (çok kullanıcı, web uygulamanın yanında route handler olarak) — kimlik doğrulama şart.
- Uzak sunucuda **OAuth 2.1** (MCP yetkilendirme şartnamesi): kullanıcı kendi hesabıyla bağlar, kapsamlar dar, token'lar kullanıcı başına.

## Araç tasarımı (kalitenin çoğu burada)

- Az sayıda, **iş odaklı** araç (`get_upcoming_bookings`), API'nin birebir aynası değil (40 uç noktayı 40 araca çevirme).
- Açıklama: ne yapar, ne zaman kullanılır, girdi biçimi ve sınırlar — model yalnızca buna bakar.
- Girdi şeması sıkı (enum, tarih biçimi), çıktı kısa ve yapılandırılmış (gereksiz alanları at — bağlam pahalı).
- Büyük sonuçlar: sayfalama (`cursor`), özet + ayrıntı aracı ayrımı, kırpma ve "daha fazlası için…" notu.
- Hata mesajı **düzeltici**: "`from` geçmiş 1 yıldan eski olamaz; daha yakın bir tarih ver." — model kendini düzeltir.
- Okuma araçlarıyla başla; yazma araçlarını sonra ve dikkatle ekle.

## Güvenlik

- En az yetki: salt okunur DB kullanıcısı / kapsamlı API anahtarı; kiracı izolasyonu sunucuda.
- Yıkıcı/dışa dönük araçlar (sil, gönder, öde) için açık adlandırma ve istemci tarafında kullanıcı onayı; mümkünse "taslak oluştur" + "onayla" iki adımı.
- Araç sonuçlarındaki içerik (kullanıcı verisi, web sayfaları) prompt injection taşıyabilir — sunucu tarafında talimat gibi davranma, sonuçları veri olarak döndür.
- Sırlar env'de; loglarda kişisel veri yok; rate limit.

## Test ve kullanım

- **MCP Inspector** (`npx @modelcontextprotocol/inspector node dist/server.js`) ile araçları elle dene.
- Claude Code'a ekleme: `claude mcp add sky-bookings -- node /yol/dist/server.js` (uzak için HTTP adresiyle); kapsam (proje/kullanıcı) seçimi.
- Gerçek görevlerle dene ("bu haftaki iptalleri listele ve özetle"), modelin aracı doğru seçip seçmediğine bak, açıklamaları ona göre iyileştir.
- Paketle: npm paketi (`npx sky-bookings-mcp`) veya Docker; README'de kurulum satırları (bkz. `sky-npm-library`).
