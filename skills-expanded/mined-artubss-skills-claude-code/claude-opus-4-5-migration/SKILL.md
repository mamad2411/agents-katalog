---
name: claude-opus-4-5-migration
description: Migre prompts e código de Claude Sonnet 4.0, Sonnet 4.5 ou Opus 4.1 para Opus 4.5. Use quando o usuário quiser atualizar sua base de código, prompts ou chamadas de API para usar Opus 4.5. Lida com atualizações de string de modelo e ajustes de prompt para diferenças comportamentais conhecidas de Opus 4.5. NÃO migra Haiku 4.5.
---

# Guia de Migração Opus 4.5

Migração única de Sonnet 4.0, Sonnet 4.5 ou Opus 4.1 para Opus 4.5.

## Workflow de Migração

1. Procure na base de código strings de modelo e chamadas de API
2. Atualize strings de modelo para Opus 4.5 (veja strings específicas da plataforma abaixo)
3. Remova headers beta não suportados
4. Adicione parâmetro effort definido como `"high"` (veja `references/effort.md`)
5. Resuma todas as mudanças realizadas
6. Diga ao usuário: "Se você encontrar algum problema com Opus 4.5, me avise que posso ajudar a ajustar seus prompts."

## Atualizações de String de Modelo

Identifique qual plataforma a base de código usa e substitua as strings de modelo de acordo.

### Headers Beta Não Suportados

Remova o header beta `context-1m-2025-08-07` se presente—ainda não é suportado com Opus 4.5. Deixe um comentário anotando isso:

```python
# Nota: Beta de contexto 1M (context-1m-2025-08-07) ainda não suportado com Opus 4.5
```

### Strings de Modelo Alvo (Opus 4.5)

| Plataforma | String de Modelo Opus 4.5 |
|----------|----------------------|
| Anthropic API (1P) | `claude-opus-4-5-20251101` |
| AWS Bedrock | `anthropic.claude-opus-4-5-20251101-v1:0` |
| Google Vertex AI | `claude-opus-4-5@20251101` |
| Azure AI Foundry | `claude-opus-4-5-20251101` |

### Strings de Modelo de Origem para Substituir

| Modelo de Origem | Anthropic API (1P) | AWS Bedrock | Google Vertex AI |
|--------------|-------------------|-------------|------------------|
| Sonnet 4.0 | `claude-sonnet-4-20250514` | `anthropic.claude-sonnet-4-20250514-v1:0` | `claude-sonnet-4@20250514` |
| Sonnet 4.5 | `claude-sonnet-4-5-20250929` | `anthropic.claude-sonnet-4-5-20250929-v1:0` | `claude-sonnet-4-5@20250929` |
| Opus 4.1 | `claude-opus-4-1-20250422` | `anthropic.claude-opus-4-1-20250422-v1:0` | `claude-opus-4-1@20250422` |

**Não migre**: Nenhum modelo Haiku (ex: `claude-haiku-4-5-20251001`).

## Ajustes de Prompt

Opus 4.5 tem diferenças comportamentais conhecidas em relação aos modelos anteriores. **Aplique esses ajustes apenas se o usuário solicitá-los explicitamente ou relatar um problema específico.** Por padrão, apenas atualize as strings de modelo.

**Diretrizes de integração**: Ao adicionar snippets, não os apenda simplesmente aos prompts. Integre-os criteriosamente:
- Use tags XML (ex: `<code_guidelines>`, `<tool_usage>`) para organizar adições
- Combine com o estilo e estrutura do prompt existente
- Coloque snippets em locais lógicos (ex: diretrizes de código perto de outras instruções de código)
- Se o prompt já usa tags XML, adicione novo conteúdo dentro de tags existentes apropriadas ou crie novas consistentes

### 1. Overtriggering de Tools

Opus 4.5 é mais responsivo a prompts de sistema. Linguagem agressiva que evitava undertriggering em modelos anteriores agora pode causar overtriggering.

**Aplique se**: Usuário relata tools sendo chamadas com muita frequência ou desnecessariamente.

**Encontre e suavize**:
- `CRITICAL:` → remova ou suavize
- `You MUST...` → `You should...`
- `ALWAYS do X` → `Do X`
- `NEVER skip...` → `Don't skip...`
- `REQUIRED` → remova ou suavize

Aplique apenas a instruções de triggering de tools. Deixe outros usos de ênfase intactos.

### 2. Prevenção de Over-Engineering

Opus 4.5 tende a criar arquivos extras, adicionar abstrações desnecessárias ou construir flexibilidade não solicitada.

**Aplique se**: Usuário relata arquivos indesejados, abstração excessiva ou funcionalidades não solicitadas. Adicione o snippet de `references/prompt-snippets.md`.

### 3. Exploração de Código

Opus 4.5 pode ser excessivamente conservador sobre exploração de código, propondo soluções sem ler arquivos.

**Aplique se**: Usuário relata o modelo propondo correções sem inspecionar código relevante. Adicione o snippet de `references/prompt-snippets.md`.

### 4. Design Frontend

**Aplique se**: Usuário solicita qualidade melhorada de design frontend ou relata outputs genéricos.

Adicione o snippet de estética frontend de `references/prompt-snippets.md`.

### 5. Sensibilidade do Thinking

Quando extended thinking não está ativado (o padrão), Opus 4.5 é particularmente sensível à palavra "think" e suas variantes. Extended thinking é ativado apenas se a requisição de API contém um parâmetro `thinking`.

**Aplique se**: Usuário relata problemas relacionados a "thinking" enquanto extended thinking não está ativado (sem parâmetro `thinking` na requisição).

Substitua "think" por alternativas como "consider", "believe" ou "evaluate".

## Referência

Veja `references/prompt-snippets.md` para o texto completo de cada snippet a adicionar.

Veja `references/effort.md` para configurar o parâmetro effort (apenas se o usuário solicitar).