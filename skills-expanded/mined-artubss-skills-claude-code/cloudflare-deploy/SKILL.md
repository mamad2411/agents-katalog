---
name: cloudflare-deploy
description: Implante aplicações e infraestrutura na Cloudflare usando Workers, Pages e serviços relacionados da plataforma. Use quando o usuário pedir para implantar, hospedar, publicar ou configurar um projeto na Cloudflare.
author: openai
---

# Cloudflare Deploy

Habilidade consolidada para construir na plataforma Cloudflare. Use as árvores de decisão abaixo para encontrar o produto certo e carregue as referências detalhadas.

## Pré-requisitos

- Quando a sandbox bloqueia as chamadas de rede de implantação, execute novamente com `sandbox_permissions=require_escalated`.
- A implantação pode levar alguns minutos. Use valores de timeout apropriados.

## Autenticação (Obrigatório Antes da Implantação)

Verifique a autenticação antes de `wrangler deploy`, `wrangler pages deploy` ou `npm run deploy`:

```bash
npx wrangler whoami    # Mostra a conta se autenticado
```

Não autenticado? → `references/wrangler/auth.md`
- Interativo/local: `wrangler login` (OAuth único)
- CI/CD: Configure a variável de ambiente `CLOUDFLARE_API_TOKEN`

## Árvores de Decisão Rápidas

### "Preciso executar código"

```
Precisa executar código?
├─ Funções serverless na edge → workers/
├─ Aplicação full-stack com deploys por Git → pages/
├─ Coordenação com estado/tempo real → durable-objects/
├─ Trabalhos multi-etapa de longa duração → workflows/
├─ Executar containers → containers/
├─ Multi-tenant (clientes implantam código) → workers-for-platforms/
├─ Tarefas agendadas (cron) → cron-triggers/
├─ Lógica edge leve (modificar HTTP) → snippets/
├─ Processar eventos de execução do Worker (logs/observabilidade) → tail-workers/
└─ Otimizar latência para infraestrutura backend → smart-placement/
```

### "Preciso armazenar dados"

```
Precisa de armazenamento?
├─ Chave-valor (config, sessões, cache) → kv/
├─ SQL relacional → d1/ (SQLite) ou hyperdrive/ (Postgres/MySQL existente)
├─ Armazenamento de objetos/arquivos (compatível com S3) → r2/
├─ Fila de mensagens (processamento assíncrono) → queues/
├─ Embeddings vetoriais (IA/busca semântica) → vectorize/
├─ Estado consistente e forte por entidade → durable-objects/ (armazenamento DO)
├─ Gerenciamento de segredos → secrets-store/
├─ ETL de streaming para R2 → pipelines/
└─ Cache persistente (retenção de longo prazo) → cache-reserve/
```

### "Preciso de IA/ML"

```
Precisa de IA?
├─ Executar inferência (LLMs, embeddings, imagens) → workers-ai/
├─ Banco de dados vetorial para RAG/busca → vectorize/
├─ Construir agentes de IA com estado → agents-sdk/
├─ Gateway para qualquer provedor de IA (caching, roteamento) → ai-gateway/
└─ Widget de busca alimentado por IA → ai-search/
```

### "Preciso de conectividade/rede"

```
Precisa de rede?
├─ Expor serviço local para internet → tunnel/
├─ Proxy TCP/UDP (não-HTTP) → spectrum/
├─ Servidor TURN WebRTC → turn/
├─ Conectividade de rede privada → network-interconnect/
├─ Otimizar roteamento → argo-smart-routing/
├─ Otimizar latência para backend (não usuário) → smart-placement/
└─ Vídeo/áudio em tempo real → realtimekit/ ou realtime-sfu/
```

### "Preciso de segurança"

```
Precisa de segurança?
├─ Web Application Firewall → waf/
├─ Proteção DDoS → ddos/
├─ Detecção/gerenciamento de bots → bot-management/
├─ Proteção de API → api-shield/
├─ Alternativa CAPTCHA → turnstile/
└─ Detecção de vazamento de credenciais → waf/ (ruleset gerenciado)
```

### "Preciso de mídia/conteúdo"

```
Precisa de mídia?
├─ Otimização/transformação de imagens → images/
├─ Streaming/codificação de vídeo → stream/
├─ Automação do navegador/screenshots → browser-rendering/
└─ Gerenciamento de scripts de terceiros → zaraz/
```

### "Preciso de infraestrutura como código"

```
Precisa de IaC? → pulumi/ (Pulumi), terraform/ (Terraform), ou api/ (API REST)
```

## Índice de Produtos

### Computação & Runtime
| Produto | Referência |
|---------|-----------|
| Workers | `references/workers/` |
| Pages | `references/pages/` |
| Pages Functions | `references/pages-functions/` |
| Durable Objects | `references/durable-objects/` |
| Workflows | `references/workflows/` |
| Containers | `references/containers/` |
| Workers for Platforms | `references/workers-for-platforms/` |
| Cron Triggers | `references/cron-triggers/` |
| Tail Workers | `references/tail-workers/` |
| Snippets | `references/snippets/` |
| Smart Placement | `references/smart-placement/` |

### Armazenamento & Dados
| Produto | Referência |
|---------|-----------|
| KV | `references/kv/` |
| D1 | `references/d1/` |
| R2 | `references/r2/` |
| Queues | `references/queues/` |
| Hyperdrive | `references/hyperdrive/` |
| DO Storage | `references/do-storage/` |
| Secrets Store | `references/secrets-store/` |
| Pipelines | `references/pipelines/` |
| R2 Data Catalog | `references/r2-data-catalog/` |
| R2 SQL | `references/r2-sql/` |

### IA & Machine Learning
| Produto | Referência |
|---------|-----------|
| Workers AI | `references/workers-ai/` |
| Vectorize | `references/vectorize/` |
| Agents SDK | `references/agents-sdk/` |
| AI Gateway | `references/ai-gateway/` |
| AI Search | `references/ai-search/` |

### Conectividade & Rede
| Produto | Referência |
|---------|-----------|
| Tunnel | `references/tunnel/` |
| Spectrum | `references/spectrum/` |
| TURN | `references/turn/` |
| Network Interconnect | `references/network-interconnect/` |
| Argo Smart Routing | `references/argo-smart-routing/` |
| Workers VPC | `references/workers-vpc/` |

### Segurança
| Produto | Referência |
|---------|-----------|
| WAF | `references/waf/` |
| DDoS Protection | `references/ddos/` |
| Bot Management | `references/bot-management/` |
| API Shield | `references/api-shield/` |
| Turnstile | `references/turnstile/` |

### Mídia & Conteúdo
| Produto | Referência |
|---------|-----------|
| Images | `references/images/` |
| Stream | `references/stream/` |
| Browser Rendering | `references/browser-rendering/` |
| Zaraz | `references/zaraz/` |

### Comunicação em Tempo Real
| Produto | Referência |
|---------|-----------|
| RealtimeKit | `references/realtimekit/` |
| Realtime SFU | `references/realtime-sfu/` |

### Ferramentas para Desenvolvedores
| Produto | Referência |
|---------|-----------|
| Wrangler | `references/wrangler/` |
| Miniflare | `references/miniflare/` |
| C3 | `references/c3/` |
| Observability | `references/observability/` |
| Analytics Engine | `references/analytics-engine/` |
| Web Analytics | `references/web-analytics/` |
| Sandbox | `references/sandbox/` |
| Workerd | `references/workerd/` |
| Workers Playground | `references/workers-playground/` |

### Infraestrutura como Código
| Produto | Referência |
|---------|-----------|
| Pulumi | `references/pulumi/` |
| Terraform | `references/terraform/` |
| API | `references/api/` |

### Outros Serviços
| Produto | Referência |
|---------|-----------|
| Email Routing | `references/email-routing/` |
| Email Workers | `references/email-workers/` |
| Static Assets | `references/static-assets/` |
| Bindings | `references/bindings/` |
| Cache Reserve | `references/cache-reserve/` |

## Resolução de Problemas

### Acesso de Rede Escalado

Se a implantação falhar devido a problemas de rede (timeouts, erros de DNS, conexões resetadas), execute novamente o deploy com permissões escaladas (use `sandbox_permissions=require_escalated`). O deploy requer acesso de rede escalado quando a rede de sandbox bloqueia requisições de saída.

Exemplo de orientação ao usuário:

```
O deploy precisa de acesso de rede escalado para implantar na Cloudflare. Posso executar novamente o comando com permissões escaladas—quer que eu proceda?
```