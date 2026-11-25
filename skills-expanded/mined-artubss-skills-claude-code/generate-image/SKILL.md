---
name: generate-image
description: Gere ou edite imagens usando modelos de IA (FLUX, Gemini). Use para geração de imagens de propósito geral, incluindo fotos, ilustrações, arte, recursos visuais, arte conceitual e qualquer imagem que não seja um diagrama técnico ou esquema. Para fluxogramas, circuitos, caminhos e diagramas técnicos, use a skill scientific-schematics.
---

# Gerar Imagem

Gere e edite imagens de alta qualidade usando os modelos de geração de imagens da OpenRouter, incluindo FLUX.2 Pro e Gemini 3 Pro.

## Quando Usar Esta Skill

**Use generate-image para:**
- Fotos e imagens fotorrealistas
- Ilustrações artísticas e arte
- Arte conceitual e conceitos visuais
- Recursos visuais para apresentações ou documentos
- Edição e modificação de imagens
- Qualquer necessidade geral de geração de imagens

**Use scientific-schematics para:**
- Fluxogramas e diagramas de processo
- Diagramas de circuitos e esquemas elétricos
- Vias biológicas e cascatas de sinalização
- Diagramas de arquitetura de sistemas
- Diagramas CONSORT e fluxogramas de metodologia
- Qualquer diagrama técnico ou esquemático

## Início Rápido

Use o script `scripts/generate_image.py` para gerar ou editar imagens:

```bash
# Gerar uma nova imagem
python scripts/generate_image.py "Um lindo pôr do sol sobre as montanhas"

# Editar uma imagem existente
python scripts/generate_image.py "Deixe o céu roxo" --input photo.jpg
```

Isso gera/edita uma imagem e a salva como `generated_image.png` no diretório atual.

## Configuração da Chave de API

**CRÍTICO**: O script requer uma chave de API da OpenRouter. Antes de executar, verifique se o usuário configurou sua chave de API:

1. Procure por um arquivo `.env` no diretório do projeto ou diretórios pai
2. Verifique `OPENROUTER_API_KEY=<key>` no arquivo `.env`
3. Se não encontrado, informe ao usuário que ele precisa:
   - Criar um arquivo `.env` com `OPENROUTER_API_KEY=your-api-key-here`
   - Ou definir a variável de ambiente: `export OPENROUTER_API_KEY=your-api-key-here`
   - Obter uma chave de API em: https://openrouter.ai/keys

O script detectará automaticamente o arquivo `.env` e fornecerá mensagens de erro claras se a chave de API estiver faltando.

## Seleção de Modelo

**Modelo padrão**: `google/gemini-3-pro-image-preview` (alta qualidade, recomendado)

**Modelos disponíveis para geração e edição**:
- `google/gemini-3-pro-image-preview` - Alta qualidade, suporta geração + edição
- `black-forest-labs/flux.2-pro` - Rápido, alta qualidade, suporta geração + edição

**Apenas para geração**:
- `black-forest-labs/flux.2-flex` - Rápido e econômico, mas não tão alta qualidade quanto o pro

Selecione com base em:
- **Qualidade**: Use gemini-3-pro ou flux.2-pro
- **Edição**: Use gemini-3-pro ou flux.2-pro (ambos suportam edição de imagens)
- **Custo**: Use flux.2-flex apenas para geração

## Padrões de Uso Comum

### Geração básica
```bash
python scripts/generate_image.py "Seu prompt aqui"
```

### Especificar modelo
```bash
python scripts/generate_image.py "Um gato no espaço" --model "black-forest-labs/flux.2-pro"
```

### Caminho de saída customizado
```bash
python scripts/generate_image.py "Arte abstrata" --output artwork.png
```

### Editar uma imagem existente
```bash
python scripts/generate_image.py "Deixe o fundo azul" --input photo.jpg
```

### Editar com um modelo específico
```bash
python scripts/generate_image.py "Adicione óculos escuros à pessoa" --input portrait.png --model "black-forest-labs/flux.2-pro"
```

### Editar com saída customizada
```bash
python scripts/generate_image.py "Remova o texto da imagem" --input screenshot.png --output cleaned.png
```

### Múltiplas imagens
Execute o script várias vezes com diferentes prompts ou caminhos de saída:
```bash
python scripts/generate_image.py "Descrição da imagem 1" --output image1.png
python scripts/generate_image.py "Descrição da imagem 2" --output image2.png
```

## Parâmetros do Script

- `prompt` (obrigatório): Descrição em texto da imagem a gerar ou instruções de edição
- `--input` ou `-i`: Caminho da imagem de entrada para edição (ativa modo de edição)
- `--model` ou `-m`: ID do modelo OpenRouter (padrão: google/gemini-3-pro-image-preview)
- `--output` ou `-o`: Caminho do arquivo de saída (padrão: generated_image.png)
- `--api-key`: Chave de API da OpenRouter (sobrescreve arquivo .env)

## Exemplos de Casos de Uso

### Para Documentos Científicos
```bash
# Gerar uma ilustração conceitual para um artigo
python scripts/generate_image.py "Visão microscópica de células cancerosas sendo atacadas por agentes de imunoterapia, estilo ilustração científica" --output figures/immunotherapy_concept.png

# Criar um visual para uma apresentação
python scripts/generate_image.py "Estrutura de dupla hélice de DNA com site de mutação destacado, visualização científica moderna" --output slides/dna_mutation.png
```

### Para Apresentações e Pôsteres
```bash
# Fundo de slide de título
python scripts/generate_image.py "Fundo abstrato azul e branco com padrões moleculares sutis, estilo profissional de apresentação" --output slides/background.png

# Imagem hero do pôster
python scripts/generate_image.py "Configuração de laboratório com equipamento moderno, fotorrealista, bem iluminada" --output poster/hero.png
```

### Para Conteúdo Visual Geral
```bash
# Imagens para website ou documentação
python scripts/generate_image.py "Colaboração profissional de equipe ao redor de um whiteboard digital, escritório moderno" --output docs/team_collaboration.png

# Materiais de marketing
python scripts/generate_image.py "Conceito futurista de cérebro de IA com redes neurais brilhantes" --output marketing/ai_concept.png
```

## Tratamento de Erros

O script fornece mensagens de erro claras para:
- Chave de API faltante (com instruções de configuração)
- Erros de API (com códigos de status)
- Formatos de resposta inesperados
- Dependências faltantes (biblioteca requests)

Se o script falhar, leia a mensagem de erro e resolva o problema antes de tentar novamente.

## Notas

- Imagens são retornadas como URLs de dados codificados em base64 e salvas automaticamente como arquivos PNG
- O script suporta tanto formatos de resposta `images` quanto `content` de diferentes modelos da OpenRouter
- O tempo de geração varia por modelo (tipicamente 5-30 segundos)
- Para edição de imagens, a imagem de entrada é codificada em base64 e enviada ao modelo
- Formatos de imagem de entrada suportados: PNG, JPEG, GIF, WebP
- Verifique os preços da OpenRouter para informações de custo: https://openrouter.ai/models

## Dicas de Edição de Imagem

- Seja específico sobre quais mudanças você quer (ex: "mude o céu para cores de pôr do sol" vs "edite o céu")
- Faça referência a elementos específicos na imagem quando possível
- Para melhores resultados, use instruções de edição claras e detalhadas
- Tanto Gemini 3 Pro quanto FLUX.2 Pro suportam edição de imagens através da OpenRouter

## Integração com Outras Skills

- **scientific-schematics**: Use para diagramas técnicos, fluxogramas, circuitos, vias
- **generate-image**: Use para fotos, ilustrações, arte, conceitos visuais
- **scientific-slides**: Combine com generate-image para apresentações visualmente ricas
- **latex-posters**: Use generate-image para visuais de pôsteres e imagens hero