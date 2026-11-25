---
name: "figma-implement-design"
description: "Traduza nós do Figma em código pronto para produção com fidelidade visual 1:1 usando o workflow MCP do Figma (contexto de design, screenshots, assets e tradução de convenções de projeto). Ative quando o usuário fornecer URLs do Figma ou IDs de nó, ou solicitar implementar designs ou componentes que devem corresponder às especificações do Figma. Requer uma conexão funcional com servidor MCP do Figma."
author: openai
---

# Implementar Design

## Visão Geral

Esta skill oferece um workflow estruturado para traduzir designs do Figma em código pronto para produção com precisão pixel-perfect. Ela garante integração consistente com o servidor MCP do Figma, uso adequado de design tokens e paridade visual 1:1 com os designs.

## Pré-requisitos

- O servidor MCP do Figma deve estar conectado e acessível
- O usuário deve fornecer uma URL do Figma no formato: `https://figma.com/design/:fileKey/:fileName?node-id=1-2`
  - `:fileKey` é a chave do arquivo
  - `1-2` é o ID do nó (o componente ou frame específico a implementar)
- **OU** ao usar `figma-desktop` MCP: o usuário pode selecionar um nó diretamente no app desktop do Figma (URL não é necessária)
- O projeto deve ter um design system estabelecido ou library de componentes (preferencial)

## Workflow Obrigatório

**Siga estas etapas em ordem. Não pule etapas.**

### Step 0: Configurar Figma MCP (se ainda não estiver configurado)

Se alguma chamada MCP falhar porque o Figma MCP não está conectado, pause e configure-o:

1. Adicione o Figma MCP:
   - `codex mcp add figma --url https://mcp.figma.com/mcp`
2. Habilite remote MCP client:
   - Defina `[features].rmcp_client = true` em `config.toml` **ou** execute `codex --enable rmcp_client`
3. Faça login com OAuth:
   - `codex mcp login figma`

Após login bem-sucedido, o usuário terá que reiniciar codex. Você deve finalizar sua resposta e instruir que tentem novamente para continuar com Step 1.

### Step 1: Obter ID do Nó

#### Opção A: Extrair de URL do Figma

Quando o usuário fornecer uma URL do Figma, extraia a chave do arquivo e o ID do nó para passar como argumentos para as ferramentas MCP.

**Formato de URL:** `https://figma.com/design/:fileKey/:fileName?node-id=1-2`

**Extrair:**

- **Chave do arquivo:** `:fileKey` (o segmento após `/design/`)
- **ID do nó:** `1-2` (o valor do parâmetro de query `node-id`)

**Nota:** Ao usar o MCP desktop local (`figma-desktop`), `fileKey` não é passado como parâmetro para chamadas de ferramenta. O servidor usa automaticamente o arquivo atualmente aberto, então apenas `nodeId` é necessário.

**Exemplo:**

- URL: `https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15`
- Chave do arquivo: `kL9xQn2VwM8pYrTb4ZcHjF`
- ID do nó: `42-15`

#### Opção B: Usar Seleção Atual do App Desktop do Figma (apenas figma-desktop MCP)

Ao usar o MCP `figma-desktop` e o usuário **NÃO** tiver fornecido uma URL, as ferramentas usam automaticamente o nó selecionado no arquivo Figma aberto no app desktop.

**Nota:** Prompting baseado em seleção funciona apenas com o servidor MCP `figma-desktop`. O servidor remoto requer um link para um frame ou camada para extrair contexto. O usuário deve ter o app desktop do Figma aberto com um nó selecionado.

### Step 2: Buscar Contexto de Design

Execute `get_design_context` com a chave do arquivo e ID do nó extraídos.

```
get_design_context(fileKey=":fileKey", nodeId="1-2")
```

Isso fornece os dados estruturados incluindo:

- Propriedades de layout (Auto Layout, constraints, dimensionamento)
- Especificações de tipografia
- Valores de cor e design tokens
- Estrutura de componentes e variantes
- Valores de espaçamento e padding

**Se a resposta for muito grande ou truncada:**

1. Execute `get_metadata(fileKey=":fileKey", nodeId="1-2")` para obter o mapa de nó de alto nível
2. Identifique os nós filho específicos necessários a partir dos metadados
3. Busque nós filho individuais com `get_design_context(fileKey=":fileKey", nodeId=":childNodeId")`

### Step 3: Capturar Referência Visual

Execute `get_screenshot` com a mesma chave do arquivo e ID do nó para uma referência visual.

```
get_screenshot(fileKey=":fileKey", nodeId="1-2")
```

Este screenshot serve como a fonte de verdade para validação visual. Mantenha-o acessível durante toda a implementação.

### Step 4: Baixar Assets Necessários

Baixe quaisquer assets (imagens, ícones, SVGs) retornados pelo servidor MCP do Figma.

**IMPORTANTE:** Siga estas regras de assets:

- Se o servidor MCP do Figma retornar uma fonte `localhost` para uma imagem ou SVG, use essa fonte diretamente
- NÃO importe ou adicione novos pacotes de ícones — todos os assets devem vir do payload do Figma
- NÃO use ou crie placeholders se uma fonte `localhost` for fornecida
- Assets são servidos através do endpoint de assets integrado do servidor MCP do Figma

### Step 5: Traduzir para Convenções do Projeto

Traduza o output do Figma para o framework, estilos e convenções deste projeto.

**Princípios-chave:**

- Trate o output do Figma MCP (tipicamente React + Tailwind) como uma representação de design e comportamento, não como estilo de código final
- Substitua classes de utilidade Tailwind pelas utilidades preferidas do projeto ou design system tokens
- Reutilize componentes existentes (botões, inputs, tipografia, wrappers de ícones) em vez de duplicar funcionalidade
- Use o sistema de cores, escala tipográfica e tokens de espaçamento do projeto consistentemente
- Respeite padrões existentes de routing, gerenciamento de estado e data-fetch

### Step 6: Alcançar Paridade Visual 1:1

Busque paridade visual pixel-perfect com o design do Figma.

**Diretrizes:**

- Priorize fidelidade ao Figma para corresponder aos designs exatamente
- Evite valores hardcoded — use design tokens do Figma quando disponível
- Quando conflitos surgirem entre design system tokens e specs do Figma, prefira design system tokens mas ajuste espaçamento ou tamanhos minimamente para corresponder aos visuais
- Siga requisitos WCAG para acessibilidade
- Adicione documentação de componentes conforme necessário

### Step 7: Validar Contra Figma

Antes de marcar como completo, valide a UI final contra o screenshot do Figma.

**Checklist de validação:**

- [ ] Layout corresponde (espaçamento, alinhamento, dimensionamento)
- [ ] Tipografia corresponde (fonte, tamanho, peso, altura da linha)
- [ ] Cores correspondem exatamente
- [ ] Estados interativos funcionam como designed (hover, active, disabled)
- [ ] Comportamento responsivo segue constraints do Figma
- [ ] Assets renderizam corretamente
- [ ] Padrões de acessibilidade atendidos

## Regras de Implementação

### Organização de Componentes

- Coloque componentes UI no diretório designado do design system do projeto
- Siga as convenções de nomenclatura de componentes do projeto
- Evite estilos inline a menos que seja necessário para valores dinâmicos

### Integração com Design System

- **SEMPRE** use componentes do design system do projeto quando possível
- Mapeie design tokens do Figma para design tokens do projeto
- Quando um componente correspondente existe, estenda-o em vez de criar um novo
- Documente quaisquer novos componentes adicionados ao design system

### Qualidade do Código

- Evite valores hardcoded — extraia para constantes ou design tokens
- Mantenha componentes compostos e reutilizáveis
- Adicione tipos TypeScript para props de componentes
- Inclua comentários JSDoc para componentes exportados

## Exemplos

### Exemplo 1: Implementar um Componente Button

O usuário diz: "Implemente este componente button do Figma: https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15"

**Ações:**

1. Parse da URL para extrair fileKey=`kL9xQn2VwM8pYrTb4ZcHjF` e nodeId=`42-15`
2. Execute `get_design_context(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodeId="42-15")`
3. Execute `get_screenshot(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodeId="42-15")` para referência visual
4. Baixe quaisquer ícones de button do endpoint de assets
5. Verifique se o projeto tem componente button existente
6. Se sim, estenda-o com nova variante; se não, crie novo componente usando convenções do projeto
7. Mapeie cores do Figma para design tokens do projeto (ex: `primary-500`, `primary-hover`)
8. Valide contra screenshot para padding, border radius, tipografia

**Resultado:** Componente button correspondendo ao design do Figma, integrado com design system do projeto.

### Exemplo 2: Construir um Layout de Dashboard

O usuário diz: "Construa este dashboard: https://figma.com/design/pR8mNv5KqXzGwY2JtCfL4D/Dashboard?node-id=10-5"

**Ações:**

1. Parse da URL para extrair fileKey=`pR8mNv5KqXzGwY2JtCfL4D` e nodeId=`10-5`
2. Execute `get_metadata(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId="10-5")` para entender a estrutura da página
3. Identifique seções principais dos metadados (header, sidebar, área de conteúdo, cards) e seus IDs de nó filho
4. Execute `get_design_context(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId=":childNodeId")` para cada seção principal
5. Execute `get_screenshot(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId="10-5")` para a página completa
6. Baixe todos os assets (logos, ícones, gráficos)
7. Construa layout usando primitivas de layout do projeto
8. Implemente cada seção usando componentes existentes quando possível
9. Valide comportamento responsivo contra constraints do Figma

**Resultado:** Dashboard completo correspondendo ao design do Figma com layout responsivo.

## Boas Práticas

### Sempre Comece com Contexto

Nunca implemente baseado em suposições. Sempre busque `get_design_context` e `get_screenshot` primeiro.

### Validação Incremental

Valide frequentemente durante a implementação, não apenas ao final. Isso detecta problemas cedo.

### Documente Desvios

Se você deve desviar do design do Figma (ex: por acessibilidade ou restrições técnicas), documente por quê em comentários de código.

### Reutilize em Vez de Recriar

Sempre verifique componentes existentes antes de criar novos. Consistência no codebase é mais importante que replicação exata do Figma.

### Design System em Primeiro Lugar

Em dúvida, prefira padrões do design system do projeto sobre tradução literal do Figma.

## Problemas Comuns e Soluções

### Problema: Output do Figma está truncado

**Causa:** O design é muito complexo ou tem muitas camadas aninhadas para retornar em uma única resposta.
**Solução:** Use `get_metadata` para obter a estrutura do nó, depois busque nós específicos individualmente com `get_design_context`.

### Problema: Design não corresponde após implementação

**Causa:** Discrepâncias visuais entre o código implementado e o design original do Figma.
**Solução:** Compare lado a lado com o screenshot do Step 3. Verifique espaçamento, cores e valores de tipografia nos dados de contexto de design.

### Problema: Assets não carregando

**Causa:** O endpoint de assets do servidor MCP do Figma não está acessível ou as URLs estão sendo modificadas.
**Solução:** Verifique se o endpoint de assets do servidor MCP do Figma está acessível. O servidor serve assets em URLs `localhost`. Use estas diretamente sem modificação.

### Problema: Valores de design token diferem do Figma

**Causa:** Os design system tokens do projeto têm valores diferentes dos especificados no design do Figma.
**Solução:** Quando tokens do projeto diferem de valores do Figma, prefira tokens do projeto para consistência, mas ajuste espaçamento/dimensionamento para manter fidelidade visual.

## Entendendo Implementação de Design

O workflow de implementação do Figma estabelece um processo confiável para traduzir designs em código:

**Para designers:** Confiança de que implementações corresponderão aos seus designs com precisão pixel-perfect.
**Para desenvolvedores:** Uma abordagem estruturada que elimina adivinhação e reduz revisões iterativas.
**Para equipes:** Implementações consistentes e de alta qualidade que mantêm integridade do design system.

Ao seguir este workflow, você garante que cada design do Figma é implementado com o mesmo nível de cuidado e atenção aos detalhes.

## Recursos Adicionais

- [Documentação do Servidor MCP do Figma](https://developers.figma.com/docs/figma-mcp-server/)
- [Ferramentas e Prompts do Servidor MCP do Figma](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
- [Variáveis Figma e Design Tokens](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)