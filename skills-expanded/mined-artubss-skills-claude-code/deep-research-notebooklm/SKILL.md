---
name: deep-research-notebooklm
description: "Skill de pesquisa profunda alimentado por NotebookLM MCP. Conduz pesquisa estruturada em múltiplas fontes (análise de mercado, inteligência competitiva, análise de tendências, pesquisa de prospects) usando Google NotebookLM como mecanismo de pesquisa, depois entrega briefs formatados e artefatos opcionais de estúdio (slides, podcasts de áudio, vídeos, infográficos, relatórios, mapas mentais)."
---

# Pesquisa Profunda via NotebookLM

Pesquise **$ARGUMENTS** profundamente usando o servidor NotebookLM MCP e entregue um brief de pesquisa estruturado. Opcionalmente, gere artefatos de estúdio (slides, podcasts de áudio, vídeos, infográficos, relatórios, mapas mentais) a partir da pesquisa.

## Pré-requisitos

- **Servidor NotebookLM MCP** deve estar configurado. Instale via: `nlm setup add claude-code`
- Se as ferramentas NotebookLM MCP não estiverem disponíveis, informe ao usuário para executar o comando de configuração e reiniciar a sessão.

## Fluxo de Trabalho de Pesquisa

### Etapa 1: Definir Escopo

Determine o **tipo de pesquisa** com base na solicitação do usuário:

| Tipo | Foco |
|------|-------|
| **Pesquisa de Mercado** | Tendências do setor, dimensionamento de mercado, oportunidades, TAM/SAM/SOM |
| **Inteligência Competitiva** | Análise de concorrentes, lacunas de posicionamento, comparações de funcionalidades |
| **Pesquisa de Cliente/Prospect** | Histórico da empresa, pontos de dor, tomadores de decisão, notícias recentes |
| **Análise de Tendências** | Tendências tecnológicas, padrões de adoção, previsões, players emergentes |
| **Pesquisa para Proposta** | Base para propostas, dados específicos do setor, estudos de caso |
| **Acadêmica/Técnica** | Papers, frameworks, metodologias, estado da arte |

Diga ao usuário o que você planeja pesquisar e confirme o ângulo:

> "Vou pesquisar [tema]. Meu ângulo: [foco específico]. Vou investigar: [2-3 questões específicas]. Está bom assim, ou devo ajustar?"

Aguarde a confirmação antes de prosseguir.

### Etapa 2: Criar Notebook NotebookLM

Use `notebook_create` para criar um notebook chamado:
`Pesquisa: [Tema] - [YYYY-MM-DD]`

### Etapa 3: Adicionar Fontes de Contexto

Use `source_add` para alimentar o notebook com contexto relevante:
- Adicione qualquer URL fornecida pelo usuário (artigos, páginas da empresa, relatórios)
- Adicione documentos ou arquivos que o usuário referencia
- Adicione resumos de texto de contexto relevante se nenhuma URL estiver disponível
- Se pesquisando uma empresa, adicione seu website, LinkedIn, imprensa recente

### Etapa 4: Executar Pesquisa

Use `research_start` com uma consulta bem elaborada com base no tema e contexto.

**Seleção de modo:**
- Padrão: `"fast"` (~60 segundos, ~10 fontes) -- bom para a maioria das consultas
- Use `"deep"` apenas se o usuário pedir explicitamente por pesquisa exaustiva (pode levar 10+ minutos e pode travar em 0 fontes)

**Dica:** Execute chamadas diretas de `WebSearch` em paralelo com NotebookLM para coleta de dados inicial mais rápida enquanto o mecanismo de pesquisa funciona.

Sonde `research_status` até concluir. Use o parâmetro `query` como fallback de correspondência -- IDs de tarefa podem mudar entre chamadas `research_start` e `research_status`.

### Etapa 5: Importar Fontes Descobertas

Use `research_import` para trazer fontes descobertas para o notebook para análise mais profunda.

### Etapa 6: Consultar para Insights

Use `notebook_query` para fazer 3-5 perguntas direcionadas com base no tipo de pesquisa:

1. **Visão Geral**: "Quais são as principais descobertas sobre [tema]?"
2. **Oportunidades**: "Que oportunidades ou lacunas existem neste espaço?"
3. **Ações**: "Quais são os insights mais acionáveis dessa pesquisa?"
4. **Riscos**: "Quais são os principais riscos, desafios ou contra-argumentos?"
5. **Personalizado**: Uma pergunta específica do tipo de pesquisa (ex: "Quais são os 5 principais concorrentes e como se diferenciam?" para inteligência competitiva)

### Etapa 7: Escrever Brief de Pesquisa

Salve os resultados em um arquivo local usando o template de brief de pesquisa:

**Caminho do arquivo:** `research/[topic-slug]-[YYYY-MM-DD].md`

Use o template em [research-brief-template.md](research-brief-template.md) para estruturar o output. Crie o diretório `research/` se não existir.

### Etapa 8: Apresentar Conclusões-Chave

Após salvar, apresente ao usuário:
- **3-5 descobertas principais** (bullets, diretas, sem fluff)
- **1-2 ações recomendadas** conectadas aos objetivos declarados do usuário
- **Surpresas ou descobertas contrárias** -- tudo que desafie suposições
- **O caminho do arquivo** onde o brief completo foi salvo
- **A URL do notebook NotebookLM** para que o usuário possa explorar as fontes diretamente

### Etapa 9 (Opcional): Gerar Artefatos de Estúdio

Pergunte ao usuário: "Quer que eu gere algum artefato desta pesquisa? Opções: slides, áudio (podcast), vídeo, infográfico, relatório, mapa mental."

Se sim, use `studio_create` com o notebook_id da Etapa 2.

**Tipos de artefato disponíveis e configurações recomendadas:**

| Tipo | Parâmetros-chave | Melhor para |
|------|-----------|----------|
| `slide_deck` | `slide_format`: `detailed_deck` ou `presenter_slides`; `slide_length`: `short` ou `default` | Apresentações executivas, pitches com clientes |
| `audio` | `audio_format`: `deep_dive`, `brief`, `critique` ou `debate`; `audio_length`: `short`, `default`, `long` | Podcasts estilo deep dive, aprendizado em movimento |
| `video` | `video_format`: `explainer`, `brief`, `cinematic`; `visual_style`: `auto_select`, `classic`, `whiteboard`, etc. | Explainers visuais, conteúdo para redes sociais |
| `infographic` | `orientation`: `landscape`, `portrait`, `square`; `infographic_style`: `professional`, `bento_grid`, etc. | One-pagers, compartilhamento em redes sociais |
| `report` | `report_format`: `Briefing Doc`, `Study Guide`, `Blog Post`, `Create Your Own` | Deliverables escritos, resumos |
| `mind_map` | `title` | Mapeamento visual de conhecimento |

**Parâmetros comuns para todos os tipos de artefato:**
- `language`: Configure para o idioma preferido do usuário (ex: `"pt"`, `"en"`, `"es"`)
- `focus_prompt`: Uma diretiva clara sobre o que enfatizar no artefato
- `confirm`: Deve ser `true` para prosseguir com a geração

**Após criar um artefato:**
1. Sonde `studio_status` até `completed` (áudio/vídeo: 5-15 min; slides/infográficos: 2-5 min)
2. Use `download_artifact` para salvar localmente se necessário
3. Forneça a URL do notebook para que o usuário acesse artefatos diretamente

**Dicas:**
- `audio` com formato `deep_dive` produz a melhor análise estilo podcast
- `slide_deck` com formato `detailed_deck` funciona melhor para leitura independente; `presenter_slides` é melhor quando acompanhado de notas do apresentador
- Status de áudio pode mostrar `"unknown"` uma vez concluído -- verifique a presença de `audio_url` em vez de aguardar status `"completed"`

## Notas

- Fast mode é recomendado como padrão. Deep mode é poderoso mas pode levar 10+ minutos e ocasionalmente trava.
- Sempre confirme o escopo de pesquisa com o usuário antes de iniciar -- uma consulta bem-definida produz resultados dramaticamente melhores.
- O template de brief de pesquisa garante output consistente e acionável em todos os tipos de pesquisa.

## Recursos Adicionais

- [research-brief-template.md](research-brief-template.md) -- Template para estruturar output de brief de pesquisa