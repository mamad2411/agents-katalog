---
name: data-feeds
description: Extraia dados estruturados de 40+ sites, incluindo Amazon, LinkedIn, Instagram, TikTok, Facebook, YouTube e mais. Usa as Web Data APIs do Bright Data com polling automático. Retorna JSON limpo com detalhes de produtos, perfis, avaliações, posts e comentários.
---

# Bright Data - Structured Data Feeds

Extraia dados estruturados de grandes sites com parsing automático. Sem lógica de scraping necessária — apenas forneça uma URL e obtenha dados JSON limpos.

## Configuração

### Variáveis de Ambiente (Obrigatórias)
```bash
export BRIGHTDATA_API_KEY="your-api-key"
```

### Opcional
```bash
export BRIGHTDATA_POLLING_TIMEOUT=600  # Máximo de segundos para aguardar (padrão: 600)
```

Obtenha sua chave de API no [Painel Bright Data](https://brightdata.com/cp).

## Uso

```bash
bash scripts/datasets.sh <dataset_type> <url> [additional_params...]
```

## Datasets Disponíveis

### E-Commerce

| Dataset | Comando | Descrição |
|---------|---------|-----------|
| Amazon Product | `datasets.sh amazon_product <url>` | Detalhes do produto, preço, classificações |
| Amazon Reviews | `datasets.sh amazon_product_reviews <url>` | Avaliações de clientes de um produto |
| Amazon Search | `datasets.sh amazon_product_search <keyword> <domain_url>` | Resultados de busca |
| Walmart Product | `datasets.sh walmart_product <url>` | Detalhes do produto da Walmart |
| Walmart Seller | `datasets.sh walmart_seller <url>` | Informações do vendedor |
| eBay Product | `datasets.sh ebay_product <url>` | Detalhes do anúncio eBay |
| Home Depot | `datasets.sh homedepot_products <url>` | Dados de produtos Home Depot |
| Zara | `datasets.sh zara_products <url>` | Detalhes de produtos Zara |
| Etsy | `datasets.sh etsy_products <url>` | Dados de anúncios Etsy |
| Best Buy | `datasets.sh bestbuy_products <url>` | Informações de produtos Best Buy |

### Redes Profissionais

| Dataset | Comando | Descrição |
|---------|---------|-----------|
| LinkedIn Person | `datasets.sh linkedin_person_profile <url>` | Dados de perfil (experiência, habilidades) |
| LinkedIn Company | `datasets.sh linkedin_company_profile <url>` | Dados de página de empresa |
| LinkedIn Jobs | `datasets.sh linkedin_job_listings <url>` | Detalhes de vagas de emprego |
| LinkedIn Posts | `datasets.sh linkedin_posts <url>` | Conteúdo e engajamento de posts |
| LinkedIn Search | `datasets.sh linkedin_people_search <url> <first> <last>` | Encontrar pessoas |
| Crunchbase | `datasets.sh crunchbase_company <url>` | Financiamento e funcionários da empresa |
| ZoomInfo | `datasets.sh zoominfo_company_profile <url>` | Dados de perfil da empresa |

### Instagram

| Dataset | Comando | Descrição |
|---------|---------|-----------|
| Profiles | `datasets.sh instagram_profiles <url>` | Bio, seguidores, seguindo |
| Posts | `datasets.sh instagram_posts <url>` | Detalhes de posts, curtidas, legendas |
| Reels | `datasets.sh instagram_reels <url>` | Dados de Reels e métricas |
| Comments | `datasets.sh instagram_comments <url>` | Comentários de posts |

### Facebook

| Dataset | Comando | Descrição |
|---------|---------|-----------|
| Posts | `datasets.sh facebook_posts <url>` | Conteúdo e reações de posts |
| Marketplace | `datasets.sh facebook_marketplace_listings <url>` | Detalhes de anúncios |
| Reviews | `datasets.sh facebook_company_reviews <url> [num]` | Avaliações de empresa |
| Events | `datasets.sh facebook_events <url>` | Detalhes de eventos |

### TikTok

| Dataset | Comando | Descrição |
|---------|---------|-----------|
| Profiles | `datasets.sh tiktok_profiles <url>` | Dados de perfil de criador |
| Posts | `datasets.sh tiktok_posts <url>` | Detalhes de vídeos e métricas |
| Shop | `datasets.sh tiktok_shop <url>` | Dados de produtos TikTok Shop |
| Comments | `datasets.sh tiktok_comments <url>` | Comentários de vídeos |

### YouTube

| Dataset | Comando | Descrição |
|---------|---------|-----------|
| Profiles | `datasets.sh youtube_profiles <url>` | Dados de canal |
| Videos | `datasets.sh youtube_videos <url>` | Detalhes de vídeos e estatísticas |
| Comments | `datasets.sh youtube_comments <url> [num]` | Comentários de vídeos (padrão: 10) |

### Outras Redes Sociais

| Dataset | Comando | Descrição |
|---------|---------|-----------|
| X (Twitter) | `datasets.sh x_posts <url>` | Dados de tweets |
| Reddit | `datasets.sh reddit_posts <url>` | Dados de posts e comentários |

### Google Services

| Dataset | Comando | Descrição |
|---------|---------|-----------|
| Maps Reviews | `datasets.sh google_maps_reviews <url> [days]` | Avaliações de negócio (padrão: 3 dias) |
| Shopping | `datasets.sh google_shopping <url>` | Dados de comparação de produtos |
| Play Store | `datasets.sh google_play_store <url>` | Detalhes de aplicativo e avaliações |

### Outros

| Dataset | Comando | Descrição |
|---------|---------|-----------|
| Apple App Store | `datasets.sh apple_app_store <url>` | Dados de aplicativo iOS |
| Reuters News | `datasets.sh reuter_news <url>` | Conteúdo de artigos de notícias |
| GitHub | `datasets.sh github_repository_file <url>` | Dados de arquivo de repositório |
| Yahoo Finance | `datasets.sh yahoo_finance_business <url>` | Dados de ações e empresa |
| Zillow | `datasets.sh zillow_properties_listing <url>` | Detalhes de listagem de propriedade |
| Booking.com | `datasets.sh booking_hotel_listings <url>` | Dados de listagem de hotel |

## Exemplos

### Obter Perfil LinkedIn
```bash
bash scripts/datasets.sh linkedin_person_profile "https://www.linkedin.com/in/satyanadella/"
```

### Obter Produto Amazon
```bash
bash scripts/datasets.sh amazon_product "https://www.amazon.com/dp/B09V3KXJPB"
```

### Obter Perfil Instagram
```bash
bash scripts/datasets.sh instagram_profiles "https://www.instagram.com/natgeo/"
```

### Obter Comentários YouTube
```bash
bash scripts/datasets.sh youtube_comments "https://www.youtube.com/watch?v=dQw4w9WgXcQ" 20
```

### Buscar na Amazon
```bash
bash scripts/datasets.sh amazon_product_search "wireless headphones" "https://www.amazon.com"
```

## Formato de Saída

Retorna JSON estruturado com campos específicos do site. Exemplo para perfil LinkedIn:

```json
{
  "name": "Satya Nadella",
  "headline": "Chairman and CEO at Microsoft",
  "location": "Greater Seattle Area",
  "connections": "500+",
  "experience": [...],
  "education": [...],
  "skills": [...]
}
```

## Como Funciona

1. **Trigger**: Envia URL para a Web Data API do Bright Data
2. **Poll**: Aguarda a conclusão da coleta de dados (verifica a cada segundo)
3. **Return**: Retorna JSON estruturado quando pronto

O mecanismo de polling lida com limites de taxa e garante qualidade de dados aguardando a extração completa.

## Avançado: Fetch Direto

Para IDs de dataset personalizados ou casos de uso avançados:

```bash
bash scripts/fetch.sh <dataset_id> '<json_input>'
```

Exemplo:
```bash
bash scripts/fetch.sh gd_l1viktl72bvl7bjuj0 '{"url":"https://linkedin.com/in/someone"}'
```