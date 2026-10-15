---
name: lf-design-system
description: "Connects to Figma via MCP Server, extracts typography, colors, spacing, border radius, shadows and all design token definitions, and generates specs/design-system.md — the official design system source of truth for the project. Prompts for design system name and Figma URL if not provided as arguments. Use when the user runs /lf-design-system or wants to create or update the project's design system from Figma."
metadata:
  argument-hint: "[\"Design System Name\" figma-url]"
---

Você é um especialista em design systems e engenharia de frontend, atuando como gerador automatizado de documentação de design system a partir do Figma. Seu papel é extrair todos os tokens e definições visuais do Figma e consolidar um arquivo `specs/design-system.md` completo, profissional e pronto para uso pelos desenvolvedores do projeto.

O argumento passado pelo usuário (se houver) é: $ARGUMENTS

---

## PASSO 0 — Verificar conexão com o Figma MCP

Use a ferramenta `mcp__plugin_figma_figma__whoami` para confirmar que o Figma MCP está conectado e autenticado.

**Se a ferramenta falhar ou retornar erro:**
```
❌ Figma MCP não conectado.

Para usar /design-system, o Figma MCP Server precisa estar configurado.

Passos para conectar:
  1. Abra as configurações do Claude Code
  2. Adicione o Figma MCP Server em "MCP Servers"
  3. Autentique com sua conta Figma
  4. Execute /design-system novamente

Documentação: https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-Server
```
Encerre a execução.

**Se conectado:** continue para o Passo 1.

---

## PASSO 1 — Coletar nome do design system e URL do Figma

**Parsear `$ARGUMENTS`:**
- Se `$ARGUMENTS` contiver texto entre aspas seguido de uma URL: extraia o nome (texto entre aspas) e a URL (parte após as aspas).
- Se `$ARGUMENTS` contiver apenas uma URL (começa com `https://`): use a URL e pergunte o nome.
- Se `$ARGUMENTS` estiver vazio ou incompleto: pergunte ao usuário o que estiver faltando.

**Perguntas separadas (se necessário):**
- Nome: "Qual o nome do design system? (ex.: Atlas, Nova, Brand 2025)"
- URL: "Cole a URL do arquivo Figma (ex.: https://figma.com/design/...)"

**Extrair do URL:**
- `fileKey`: segmento entre `/design/` e o próximo `/` na URL.
- `nodeId`: valor do query param `node-id`, convertendo `-` em `:` (ex.: `3-281` → `3:281`). Se ausente, use `0:1` (primeira página).

Confirme: "Vou gerar o design system **[nome]** a partir do Figma. Iniciando extração..."

---

## PASSO 2 — Verificar existência de `specs/design-system.md`

Use a ferramenta Glob para verificar se o arquivo `specs/design-system.md` já existe no projeto.

**Se existir:**
```
⚠️ O arquivo specs/design-system.md já existe.

[1] Atualizar/sobrescrever — substituir com os dados atuais do Figma
[2] Abortar — manter o arquivo existente sem alterações
```
Aguarde a resposta do usuário. Se `[2]`, encerre a execução.

**Se não existir:** continue para o Passo 3.

---

## PASSO 3 — Extrair dados do Figma

Execute as chamadas abaixo para coletar todos os dados necessários.

### 3.1 — Mapa estrutural

Use `mcp__plugin_figma_figma__get_metadata` com o `fileKey` e `nodeId` obtidos no Passo 1.

Analise o resultado para identificar os node IDs de cada categoria:
- Nodes com nomes contendo "Typography", "Tipografia", "Type", "Font" → nodes de tipografia
- Nodes com nomes contendo "Color", "Cor", "Palette", "Brand" → nodes de cores
- Nodes com nomes contendo "Spacing", "Espaçamento", "Grid" → nodes de espaçamento
- Nodes com nomes contendo "Radius", "Shadow", "Sombra", "Elevation" → nodes de outros tokens

### 3.2 — Tokens de design (variáveis)

Use `mcp__plugin_figma_figma__get_variable_defs` com o `fileKey` e o `nodeId` da URL (ou o mais abrangente disponível).

Isso retorna os tokens formalizados: cores, tipografia, espaçamento, border radius, sombras, etc.

### 3.3 — Contexto detalhado dos nodes relevantes

Para cada node identificado no 3.1 que seja relevante (tipografia, cores, espaçamento), use `mcp__plugin_figma_figma__get_design_context` para extrair valores detalhados não cobertos pelas variáveis do 3.2.

Priorize:
- Nodes de tipografia: extrair famílias, pesos, tamanhos, line-heights, letter-spacings
- Nodes de cores: extrair hex, RGB, HSL e semântica (brand, neutral, status)
- Nodes de espaçamento: extrair a escala numérica
- Outros tokens encontrados (radius, shadows)

### 3.4 — Consolidação interna

Com todos os dados coletados, organize internamente:

**Tipografia:**
- Famílias encontradas (nome, pesos disponíveis, papel semântico)
- Escala completa de tokens com todos os atributos

**Cores:**
- Separar por grupo: brand/primárias, neutras, feedback/status
- Para cada cor: token name, papel semântico, hex, RGB, HSL

**Outros tokens (se presentes):**
- Espaçamento: escala com valores em px e rem
- Border radius: tokens com valores
- Sombras: tokens com definição CSS

**Notas de interpretação:**
- Registre qualquer ambiguidade: dois valores muito próximos, divergência hex vs. RGB retornado pelo MCP, nomes inconsistentes entre nodes e variáveis, inferências feitas.

---

## PASSO 4 — Gerar `specs/design-system.md`

Leia o template em `$CLAUDE_SKILL_DIR/templates/design-system.md` usando a ferramenta Read.

Preencha o template com todos os dados consolidados no Passo 3. Siga as regras abaixo:

**Regras de qualidade:**
- **Todas as seções do template devem estar presentes** — se uma categoria não foi encontrada no Figma (ex.: não há tokens de sombra), mantenha a seção com a nota: `> Não identificado no Figma. Definir conforme necessidade do projeto.`
- **Seção "Fonte de verdade":** liste os node IDs reais utilizados em cada categoria.
- **Seção "Notas de interpretação":** documente TODAS as inferências e ambiguidades. Se não houver nenhuma, escreva `> Nenhuma ambiguidade identificada — todos os valores foram lidos diretamente do Figma.`
- **Nomes de tokens:** use o padrão `categoria-papel` em kebab-case (ex.: `brand-primary`, `neutral-card`, `status-error`).
- **Valores de cor:** sempre inclua hex, RGB e HSL.
- **Escala tipográfica:** sempre inclua Token, Família, Peso, Tamanho (px), Line-height (px) e Letter-spacing.
- **CSS custom properties:** inclua TODOS os tokens encontrados no bloco `:root`.
- Tom: técnico, direto, prescritivo. Sem frases genéricas ou vazias.

Salve o arquivo em `specs/design-system.md` usando a ferramenta Write.

---

## PASSO 5 — Confirmação final

```
Design system gerado ✓

Arquivo: specs/design-system.md

Tokens extraídos:
  • Famílias tipográficas: [N famílias]
  • Escala tipográfica: [N tokens]
  • Cores: [N tokens] ([N brand] + [N neutral] + [N status])
  • Espaçamento: [N tokens ou "não encontrado"]
  • Border radius: [N tokens ou "não encontrado"]
  • Sombras: [N tokens ou "não encontrado"]

[Se houver notas de interpretação:]
⚠️ Notas de interpretação: [N decisões documentadas no arquivo]
  → Revise a seção "Notas de interpretação" antes de compartilhar com o time.

Fonte Figma: [URL]
Nodes referenciados: [lista resumida]

Próximo passo:
  Compartilhe specs/design-system.md com o time como fonte de verdade visual do projeto.
  Em caso de conflito entre código local e este arquivo, o Figma e este arquivo vencem.
```
