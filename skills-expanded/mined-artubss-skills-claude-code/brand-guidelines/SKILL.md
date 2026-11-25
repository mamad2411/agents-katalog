---
name: brand-guidelines
description: Aplica as cores oficiais da marca Anthropic e tipografia em qualquer artefato que se beneficie da aparência e sensação da Anthropic. Use quando diretrizes de cores da marca, guia de estilos, formatação visual ou padrões de design da empresa se aplicarem.
license: Complete terms in LICENSE.txt
---

# Estilo de Marca Anthropic

## Visão Geral

Para acessar os recursos oficiais de identidade visual e estilo da Anthropic, use esta skill.

**Palavras-chave**: branding, identidade corporativa, identidade visual, pós-processamento, estilo, cores da marca, tipografia, marca Anthropic, formatação visual, design visual

## Diretrizes de Marca

### Cores

**Cores Principais:**

- Escuro: `#141413` - Texto primário e fundos escuros
- Claro: `#faf9f5` - Fundos claros e texto sobre escuro
- Cinza Médio: `#b0aea5` - Elementos secundários
- Cinza Claro: `#e8e6dc` - Fundos sutis

**Cores de Destaque:**

- Laranja: `#d97757` - Destaque primário
- Azul: `#6a9bcc` - Destaque secundário
- Verde: `#788c5d` - Destaque terciário

### Tipografia

- **Headings**: Poppins (com fallback Arial)
- **Texto do corpo**: Lora (com fallback Georgia)
- **Nota**: As fontes devem estar pré-instaladas em seu ambiente para melhor resultado

## Recursos

### Aplicação Inteligente de Fontes

- Aplica fonte Poppins aos headings (24pt e maiores)
- Aplica fonte Lora ao texto do corpo
- Fallback automático para Arial/Georgia se fontes customizadas indisponíveis
- Preserva legibilidade em todos os sistemas

### Estilo de Texto

- Headings (24pt+): fonte Poppins
- Texto do corpo: fonte Lora
- Seleção inteligente de cores baseada no fundo
- Preserva hierarquia e formatação de texto

### Formas e Cores de Destaque

- Formas de não-texto usam cores de destaque
- Alterna entre destaques laranja, azul e verde
- Mantém interesse visual enquanto respeita a marca

## Detalhes Técnicos

### Gestão de Fontes

- Usa fontes Poppins e Lora instaladas no sistema quando disponíveis
- Oferece fallback automático para Arial (headings) e Georgia (corpo)
- Não requer instalação de fontes - funciona com fontes existentes do sistema
- Para melhores resultados, pré-instale as fontes Poppins e Lora em seu ambiente

### Aplicação de Cores

- Usa valores de cores RGB para correspondência precisa da marca
- Aplicadas pela classe RGBColor do python-pptx
- Mantém fidelidade de cor em diferentes sistemas