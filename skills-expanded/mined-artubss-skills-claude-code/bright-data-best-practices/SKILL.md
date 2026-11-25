---
name: bright-data-best-practices
description: "Construa integrações prontas para produção com a Bright Data com as melhores práticas incorporadas. Documentação de referência para desenvolvedores usando assistentes de codificação (Claude Code, Cursor, etc.) para implementar web scraping, busca, automação de navegador e extração de dados estruturados. Cobre Web Unlocker API, SERP API, Web Scraper API e Browser API (Scraping Browser)."
user-invocable: false
---

# APIs Bright Data

Bright Data fornece infraestrutura para extração de dados web em escala. Quatro APIs principais cobrem diferentes casos de uso — sempre escolha a ferramenta mais específica para o trabalho.

## Escolhendo a API Correta

| Caso de Uso | API | Por Quê |
|----------|-----|-----|
| Extrair qualquer página por URL (sem interação) | Web Unlocker | Baseada em HTTP, contorna detecção de bot automaticamente, mais barata |
| Resultados de busca Google / Bing / Yandex | SERP API | Especializada em extração de SERP, retorna dados estruturados |
| Dados estruturados da Amazon, LinkedIn, Instagram, TikTok, etc. | Web Scraper API | Scrapers pré-construídos, sem necessidade de análise |
| Clicar, rolar, preencher formulários, executar JS, interceptar XHR | Browser API | Automação de navegador completa |
| Automação Puppeteer / Playwright / Selenium | Browser API | Conecta via CDP/WebDriver |

## Padrão de Autenticação (Todas as APIs)

Todas as APIs compartilham o mesmo modelo de autenticação:

```bash
export BRIGHTDATA_API_KEY="your-api-key"         # De Control Panel > Account Settings
export BRIGHTDATA_UNLOCKER_ZONE="zone-name"       # Nome da zona Web Unlocker
export BRIGHTDATA_SERP_ZONE="serp-zone-name"      # Nome da zona SERP API
export BROWSER_AUTH="brd-customer-ID-zone-NAME:PASSWORD"  # Credenciais Browser API
```

Cabeçalho de autenticação REST API para Web Unlocker e SERP API:
```
Authorization: Bearer YOUR_API_KEY
```

---

## Web Unlocker API

Proxy de scraping baseado em HTTP. Melhor para simples buscas de página sem interação de navegador.

**Endpoint:** `POST https://api.brightdata.com/request`

```python
import requests

response = requests.post(
    "https://api.brightdata.com/request",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "zone": "YOUR_ZONE_NAME",
        "url": "https://example.com/product/123",
        "format": "raw"
    }
)
html = response.text
```

### Parâmetros Principais

| Parâmetro | Tipo | Descrição |
|-----------|------|-------------|
| `zone` | string | Nome da zona (obrigatório) |
| `url` | string | URL alvo com `http://` ou `https://` (obrigatório) |
| `format` | string | `"raw"` (HTML) ou `"json"` (wrapper estruturado) (obrigatório) |
| `method` | string | Verbo HTTP, padrão `"GET"` |
| `country` | string | ISO de 2 letras para geo-direcionamento (ex: `"us"`, `"de"`) |
| `data_format` | string | Transformar: `"markdown"` ou `"screenshot"` |
| `async` | boolean | `true` para modo assíncrono |

### Padrões Rápidos

```python
# Obter markdown (melhor para entrada de LLM)
response = requests.post(
    "https://api.brightdata.com/request",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"zone": ZONE, "url": url, "format": "raw", "data_format": "markdown"}
)

# Requisição geo-direcionada
json={"zone": ZONE, "url": url, "format": "raw", "country": "de"}

# Screenshot para debug
json={"zone": ZONE, "url": url, "format": "raw", "data_format": "screenshot"}

# Async para processamento em lote
json={"zone": ZONE, "url": url, "format": "raw", "async": True}
```

**Regra crítica:** Nunca use Web Unlocker com Puppeteer, Playwright, Selenium ou navegadores anti-detecção. Use Browser API em vez disso.

Veja **[references/web-unlocker.md](references/web-unlocker.md)** para referência completa incluindo interface de proxy, cabeçalhos especiais, fluxo assíncrono, recursos e cobrança.

---

## SERP API

Extração estruturada de resultados de mecanismo de busca para Google, Bing, Yandex, DuckDuckGo.

**Endpoint:** `POST https://api.brightdata.com/request` (mesmo que Web Unlocker)

```python
response = requests.post(
    "https://api.brightdata.com/request",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "zone": "YOUR_SERP_ZONE",
        "url": "https://www.google.com/search?q=python+web+scraping&brd_json=1&gl=us&hl=en",
        "format": "raw"
    }
)
data = response.json()
for result in data.get("organic", []):
    print(result["rank"], result["title"], result["link"])
```

### Parâmetros Essenciais do Google

| Parâmetro | Descrição | Exemplo |
|-----------|-------------|---------|
| `q` | Consulta de busca | `q=python+web+scraping` |
| `brd_json` | Saída JSON analisada | `brd_json=1` (sempre use para pipelines de dados) |
| `gl` | País para busca | `gl=us` |
| `hl` | Idioma | `hl=en` |
| `start` | Offset de paginação | `start=10` (página 2), `start=20` (página 3) |
| `tbm` | Tipo de busca | `tbm=nws` (notícias), `tbm=isch` (imagens), `tbm=vid` (vídeos) |
| `brd_mobile` | Dispositivo | `brd_mobile=1` (mobile), `brd_mobile=ios` |
| `brd_browser` | Navegador | `brd_browser=chrome` |
| `brd_ai_overview` | Ativar AI Overview | `brd_ai_overview=2` |
| `uule` | Localização geográfica codificada | para direcionamento de localização preciso |

**Nota:** O parâmetro `num` está **descontinuado** desde setembro de 2025. Use `start` para paginação.

### Estrutura de Resposta JSON Analisada

```json
{
  "organic": [{"rank": 1, "global_rank": 1, "title": "...", "link": "...", "description": "..."}],
  "paid": [],
  "people_also_ask": [],
  "knowledge_graph": {},
  "related_searches": [],
  "general": {"results_cnt": 1240000000, "query": "..."}
}
```

### Parâmetros Principais do Bing

| Parâmetro | Descrição |
|-----------|-------------|
| `q` | Consulta de busca |
| `setLang` | Idioma (prefira 4 letras: `en-US`) |
| `cc` | Código de país |
| `first` | Paginação (incremente por 10: 1, 11, 21...) |
| `safesearch` | `off`, `moderate`, `strict` |
| `brd_mobile` | Tipo de dispositivo |

### Async para SERP em Lote

```python
# Enviar
response = requests.post(
    "https://api.brightdata.com/request",
    params={"async": "1"},
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"zone": SERP_ZONE, "url": "https://www.google.com/search?q=test&brd_json=1", "format": "raw"}
)
response_id = response.headers.get("x-response-id")

# Recuperar (chamadas de recuperação NÃO são cobradas)
result = requests.get(
    "https://api.brightdata.com/serp/get_result",
    params={"response_id": response_id},
    headers={"Authorization": f"Bearer {API_KEY}"}
)
```

**Cobrança:** Pague por 1.000 requisições bem-sucedidas apenas. Chamadas de recuperação assíncrona não são cobradas.

Veja **[references/serp-api.md](references/serp-api.md)** para referência completa incluindo parâmetros de Maps, Trends, Reviews, Lens, Hotels, Flights.

---

## Web Scraper API

Scrapers pré-construídos para extração de dados estruturados de 100+ plataformas. Nenhuma lógica de análise necessária.

**Endpoint Síncrono:** `POST https://api.brightdata.com/datasets/v3/scrape`
**Endpoint Assíncrono:** `POST https://api.brightdata.com/datasets/v3/trigger`

```python
# Síncrono (até 20 URLs, retorna imediatamente)
response = requests.post(
    "https://api.brightdata.com/datasets/v3/scrape",
    params={"dataset_id": "YOUR_DATASET_ID", "format": "json"},
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"input": [{"url": "https://www.amazon.com/dp/B09X7M8TBQ"}]}
)

if response.status_code == 200:
    data = response.json()  # Resultados prontos
elif response.status_code == 202:
    snapshot_id = response.json()["snapshot_id"]  # Fazer poll para conclusão
```

### Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-------------|
| `dataset_id` | string | Identificador do scraper da Scraper Library (obrigatório) |
| `format` | string | `json` (padrão), `ndjson`, `jsonl`, `csv` |
| `custom_output_fields` | string | Campos separados por barra: `url\|title\|price` |
| `include_errors` | boolean | Incluir informações de erro nos resultados |

### Corpo da Requisição

```json
{
  "input": [
    { "url": "https://www.amazon.com/dp/B09X7M8TBQ" },
    { "url": "https://www.amazon.com/dp/B0B7CTCPKN" }
  ]
}
```

### Fazer Poll para Resultados Assíncronos

```python
import time

# Disparar
snapshot_id = requests.post(
    "https://api.brightdata.com/datasets/v3/trigger",
    params={"dataset_id": DATASET_ID, "format": "json"},
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"input": [{"url": u} for u in urls]}
).json()["snapshot_id"]

# Fazer poll
while True:
    status = requests.get(
        f"https://api.brightdata.com/datasets/v3/progress/{snapshot_id}",
        headers={"Authorization": f"Bearer {API_KEY}"}
    ).json()["status"]

    if status == "ready": break
    if status == "failed": raise Exception("Job failed")
    time.sleep(10)

# Baixar
data = requests.get(
    f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}",
    params={"format": "json"},
    headers={"Authorization": f"Bearer {API_KEY}"}
).json()
```

**Valores de status de progresso:** `starting` → `running` → `ready` | `failed`
**Retenção de dados:** 30 dias.
**Cobrança:** Por registro entregue. URLs de entrada inválidas que falham ainda são cobráveis.

Veja **[references/web-scraper-api.md](references/web-scraper-api.md)** para referência completa incluindo tipos de scraper, formatos de saída, opções de entrega e detalhes de cobrança.

---

## Browser API (Scraping Browser)

Automação de navegador completa via CDP/WebDriver. Trata CAPTCHA, fingerprinting e detecção anti-bot automaticamente.

**Conexão:**
- Playwright/Puppeteer: `wss://${AUTH}@brd.superproxy.io:9222`
- Selenium: `https://${AUTH}@brd.superproxy.io:9515`

```javascript
const { chromium } = require("playwright-core");

const AUTH = process.env.BROWSER_AUTH;
const browser = await chromium.connectOverCDP(`wss://${AUTH}@brd.superproxy.io:9222`);
const page = await browser.newPage();
page.setDefaultNavigationTimeout(120000); // Sempre defina como 2 minutos

await page.goto("https://example.com", { waitUntil: "domcontentloaded" });
const html = await page.content();
await browser.close();
```

```python
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.connect_over_cdp(f"wss://{AUTH}@brd.superproxy.io:9222")
    page = await browser.new_page()
    page.set_default_navigation_timeout(120000)
    await page.goto("https://example.com", wait_until="domcontentloaded")
    html = await page.content()
    await browser.close()
```

### Funções CDP Personalizadas

| Função | Propósito |
|----------|---------|
| `Captcha.solve` | Disparar manualmente resolução de CAPTCHA |
| `Captcha.setAutoSolve` | Ativar/desativar resolução automática de CAPTCHA |
| `Proxy.setLocation` | Definir localização geográfica precisa (chamar ANTES de goto) |
| `Proxy.useSession` | Manter o mesmo IP entre sessões |
| `Emulation.setDevice` | Aplicar perfil de dispositivo (iPhone 14, etc.) |
| `Emulation.getSupportedDevices` | Listar perfis de dispositivo disponíveis |
| `Unblocker.enableAdBlock` | Bloquear anúncios para economizar largura de banda |
| `Unblocker.disableAdBlock` | Reativar anúncios |
| `Input.type` | Entrada de texto rápida para preenchimento em lote de formulários |
| `Browser.addCertificate` | Instalar certificado SSL do cliente para sessão |
| `Page.inspect` | Obter URL de debug de DevTools para sessão ao vivo |

```javascript
// Padrão de sessão CDP para funções personalizadas
const client = await page.target().createCDPSession();

// Resolver CAPTCHA com timeout
const result = await client.send("Captcha.solve", { timeout: 30000 });

// Localização geográfica precisa (deve ser antes de goto)
await client.send("Proxy.setLocation", {
  latitude: 37.7749,
  longitude: -122.4194,
  distance: 10,
  strict: true
});

// Bloquear recursos desnecessários
await client.send("Network.setBlockedURLs", { urls: ["*google-analytics*", "*.ads.*"] });

// Emulação de dispositivo
await client.send("Emulation.setDevice", { deviceName: "iPhone 14" });
```

### Regras de Sessão
- **Uma navegação inicial por sessão** — nova URL = nova sessão
- **Timeout inativo:** 5 minutos
- **Duração máxima:** 30 minutos

### Geolocalização
- Nível de país: acrescente `-country-us` ao nome de usuário das credenciais
- Em toda a UE: acrescente `-country-eu` (roteia através de 29+ países europeus)
- Preciso: use comando CDP `Proxy.setLocation` (antes da navegação)

### Códigos de Erro

| Código | Problema | Solução |
|------|-------|-----|
| `407` | Porta incorreta | Playwright/Puppeteer → `9222`, Selenium → `9515` |
| `403` | Autenticação incorreta | Verifique o formato de credenciais e tipo de zona |
| `503` | Escalabilidade de serviço | Aguarde 1 minuto, reconecte |

**Cobrança:** Baseada em tráfego apenas. Bloqueie imagens/CSS/fontes para reduzir custos.

Veja **[references/browser-api.md](references/browser-api.md)** para referência completa incluindo todas as funções CDP, otimização de largura de banda, padrões de CAPTCHA e debug.

---

## Referências Detalhadas

- **[references/web-unlocker.md](references/web-unlocker.md)** — Web Unlocker: lista completa de parâmetros, interface de proxy, cabeçalhos especiais, fluxo assíncrono, recursos, cobrança, anti-padrões
- **[references/serp-api.md](references/serp-api.md)** — SERP API: todos os parâmetros do Google (Maps, Trends, Reviews, Lens, Hotels, Flights), parâmetros do Bing, estrutura JSON analisada, async, cobrança
- **[references/web-scraper-api.md](references/web-scraper-api.md)** — Web Scraper API: síncrono vs assíncrono, todos os parâmetros, polling, tipos de scraper, formatos de saída, cobrança
- **[references/browser-api.md](references/browser-api.md)** — Browser API: strings de conexão, regras de sessão, todas as funções CDP, geo-direcionamento, otimização de largura de banda, CAPTCHA, debug, códigos de erro