---
name: figma
description: Use o servidor Figma MCP para buscar contexto de design, screenshots, variáveis e assets do Figma, além de traduzir nós do Figma em código de produção. Ative quando uma tarefa envolver URLs do Figma, IDs de nós, implementação design-to-code ou configuração e troubleshooting do Figma MCP.
author: openai
---

# Figma MCP

Use o servidor Figma MCP para implementação orientada por Figma. Para detalhes de configuração e debug (variáveis de ambiente, config, verificação), veja `references/figma-mcp-config.md`.

## Regras de Integração do Figma MCP
Estas regras definem como traduzir inputs do Figma em código para este projeto e devem ser seguidas em toda mudança orientada por Figma.

### Fluxo obrigatório (não pule)
1. Execute get_design_context primeiro para buscar a representação estruturada dos nó(s) exato(s).
2. Se a resposta for muito grande ou truncada, execute get_metadata para obter o mapa de nós de alto nível e depois busque novamente apenas os nó(s) necessário(s) com get_design_context.
3. Execute get_screenshot para obter uma referência visual da variante do nó sendo implementada.
4. Somente após ter tanto get_design_context quanto get_screenshot, baixe quaisquer assets necessários e inicie a implementação.
5. Traduza o output (normalmente React + Tailwind) para as convenções, estilos e framework deste projeto. Reutilize os tokens de cor, componentes e tipografia do projeto sempre que possível.
6. Valide contra o Figma para correspondência visual 1:1 e comportamento antes de marcar como completo.

### Regras de implementação
- Trate o output do Figma MCP (React + Tailwind) como uma representação de design e comportamento, não como estilo de código final.
- Substitua classes utilitárias Tailwind pelos utilitários preferidos do projeto/tokens do design-system quando aplicável.
- Reutilize componentes existentes (ex: botões, inputs, tipografia, wrappers de ícones) em vez de duplicar funcionalidade.
- Use o sistema de cores, escala tipográfica e tokens de espaçamento do projeto de forma consistente.
- Respeite os padrões de roteamento, gerenciamento de estado e fetch de dados já adotados no repositório.
- Busque paridade visual 1:1 com o design do Figma. Quando houver conflitos, prefira tokens do design-system e ajuste espaçamento ou tamanhos minimamente para corresponder aos visuais.
- Valide a UI final contra o screenshot do Figma para aparência e comportamento.

### Tratamento de assets
- O Servidor Figma MCP fornece um endpoint de assets que pode servir image e SVG assets.
- IMPORTANTE: Se o Servidor Figma MCP retornar uma fonte localhost para uma imagem ou SVG, use essa fonte de imagem ou SVG diretamente.
- IMPORTANTE: NÃO importe/adicione novos pacotes de ícones, todos os assets devem estar no payload do Figma.
- IMPORTANTE: NÃO use ou crie placeholders se uma fonte localhost for fornecida.

### Prompting baseado em links
- O servidor é baseado em links: copie o link do frame/layer do Figma e forneça essa URL ao cliente MCP ao pedir ajuda de implementação.
- O cliente não pode navegar pela URL mas extrai o ID do nó do link; sempre certifique-se de que o link aponta para o nó/variante exato que você quer.

## Referências
- `references/figma-mcp-config.md` — configuração, verificação, troubleshooting e lembretes de uso baseado em links.
- `references/figma-tools-and-prompts.md` — catálogo de ferramentas e padrões de prompt para seleção de frameworks/componentes e busca de metadata.