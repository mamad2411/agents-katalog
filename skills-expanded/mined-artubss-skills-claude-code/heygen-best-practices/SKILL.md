---
name: heygen-best-practices
description: Melhores práticas para HeyGen - API de criação de vídeos com avatar de IA
metadata:
  tags: heygen, video, avatar, ai, api, text-to-video
---

## Quando usar

Use esta skill sempre que estiver lidando com código da API HeyGen para obter conhecimento específico do domínio na criação de vídeos com avatar de IA, gerenciamento de avatares, tratamento de fluxos de trabalho de geração de vídeo e integração com os serviços do HeyGen.

## Como usar

Leia os arquivos de regras individuais para explicações detalhadas e exemplos de código:

### Fundação
- [rules/authentication.md](rules/authentication.md) - Configuração de chave de API, header X-Api-Key e padrões de autenticação
- [rules/quota.md](rules/quota.md) - Sistema de créditos, limites de uso e verificação de cota restante
- [rules/video-status.md](rules/video-status.md) - Padrões de polling, tipos de status e recuperação de URLs de download

### Criação de Vídeo Principal
- [rules/avatars.md](rules/avatars.md) - Listagem de avatares, estilos de avatar e seleção de avatar_id
- [rules/voices.md](rules/voices.md) - Listagem de vozes, locales, configuração de velocidade/tom
- [rules/scripts.md](rules/scripts.md) - Escrita de scripts, pausas/breaks, pacing e templates de estrutura
- [rules/video-generation.md](rules/video-generation.md) - Fluxo de trabalho POST /v2/video/generate e vídeos com múltiplas cenas
- [rules/video-agent.md](rules/video-agent.md) - Geração de vídeo com prompt único usando Video Agent API
- [rules/dimensions.md](rules/dimensions.md) - Opções de resolução (720p/1080p) e aspect ratios

### Personalização de Vídeo
- [rules/backgrounds.md](rules/backgrounds.md) - Cores sólidas, imagens e fundos em vídeo
- [rules/text-overlays.md](rules/text-overlays.md) - Adição de texto com fontes e posicionamento
- [rules/captions.md](rules/captions.md) - Legendas geradas automaticamente e opções de subtítulos

### Recursos Avançados
- [rules/templates.md](rules/templates.md) - Listagem de templates e substituição de variáveis
- [rules/video-translation.md](rules/video-translation.md) - Tradução de vídeos, modos de qualidade/rápido e dublagem
- [rules/streaming-avatars.md](rules/streaming-avatars.md) - Sessões de avatar interativas em tempo real
- [rules/photo-avatars.md](rules/photo-avatars.md) - Criação de avatares a partir de fotos (fotos que falam)
- [rules/webhooks.md](rules/webhooks.md) - Registro de endpoints de webhook e tipos de eventos

### Integração
- [rules/remotion-integration.md](rules/remotion-integration.md) - Uso de vídeos com avatar HeyGen em composições Remotion