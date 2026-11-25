---
name: slack-gif-creator
description: Conhecimento e utilitários para criar GIFs animados otimizados para Slack. Fornece restrições, ferramentas de validação e conceitos de animação. Use quando usuários solicitarem GIFs animados para Slack como "faça um GIF de X fazendo Y para Slack."
license: Complete terms in LICENSE.txt
---

# Slack GIF Creator

Um toolkit fornecendo utilitários e conhecimento para criar GIFs animados otimizados para Slack.

## Requisitos do Slack

**Dimensões:**
- GIFs de emoji: 128x128 (recomendado)
- GIFs de mensagem: 480x480

**Parâmetros:**
- FPS: 10-30 (menor = arquivo menor)
- Cores: 48-128 (menos = arquivo menor)
- Duração: Manter em menos de 3 segundos para GIFs de emoji

## Workflow Principal

```python
from core.gif_builder import GIFBuilder
from PIL import Image, ImageDraw

# 1. Create builder
builder = GIFBuilder(width=128, height=128, fps=10)

# 2. Generate frames
for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    draw = ImageDraw.Draw(frame)

    # Draw your animation using PIL primitives
    # (circles, polygons, lines, etc.)

    builder.add_frame(frame)

# 3. Save with optimization
builder.save('output.gif', num_colors=48, optimize_for_emoji=True)
```

## Desenhando Gráficos

### Trabalhando com Imagens Enviadas pelo Usuário
Se um usuário enviar uma imagem, considere se ele deseja:
- **Usá-la diretamente** (ex: "animar isto", "dividir isto em frames")
- **Usá-la como inspiração** (ex: "faça algo parecido com isto")

Carregue e trabalhe com imagens usando PIL:
```python
from PIL import Image

uploaded = Image.open('file.png')
# Use directly, or just as reference for colors/style
```

### Desenhando do Zero
Ao desenhar gráficos do zero, use primitivos de PIL ImageDraw:

```python
from PIL import ImageDraw

draw = ImageDraw.Draw(frame)

# Circles/ovals
draw.ellipse([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)

# Stars, triangles, any polygon
points = [(x1, y1), (x2, y2), (x3, y3), ...]
draw.polygon(points, fill=(r, g, b), outline=(r, g, b), width=3)

# Lines
draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=5)

# Rectangles
draw.rectangle([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)
```

**Não use:** Fontes de emoji (não confiáveis em diferentes plataformas) ou assuma que gráficos pré-empacotados existem nesta skill.

### Tornando Gráficos Visualmente Atraentes

Gráficos devem parecer polidos e criativos, não básicos. Aqui está como:

**Use linhas mais grossas** - Sempre defina `width=2` ou superior para contornos e linhas. Linhas finas (width=1) parecem pixelizadas e amadoras.

**Adicione profundidade visual**:
- Use gradientes para fundos (`create_gradient_background`)
- Sobreponha múltiplas formas para complexidade (ex: uma estrela com uma estrela menor dentro)

**Torne formas mais interessantes**:
- Não desenhe apenas um círculo simples - adicione destaques, anéis ou padrões
- Estrelas podem ter brilhos (desenhe versões maiores e semi-transparentes atrás)
- Combine múltiplas formas (estrelas + brilhos, círculos + anéis)

**Preste atenção em cores**:
- Use cores vibrantes e complementares
- Adicione contraste (contornos escuros em formas claras, contornos claros em formas escuras)
- Considere a composição geral

**Para formas complexas** (corações, flocos de neve, etc.):
- Use combinações de polígonos e elipses
- Calcule pontos cuidadosamente para simetria
- Adicione detalhes (um coração pode ter uma curva de destaque, flocos de neve têm ramos intricados)

Seja criativo e detalhado! Um bom GIF para Slack deve parecer polido, não como gráficos de placeholder.

## Utilitários Disponíveis

### GIFBuilder (`core.gif_builder`)
Monta frames e otimiza para Slack:
```python
builder = GIFBuilder(width=128, height=128, fps=10)
builder.add_frame(frame)  # Add PIL Image
builder.add_frames(frames)  # Add list of frames
builder.save('out.gif', num_colors=48, optimize_for_emoji=True, remove_duplicates=True)
```

### Validators (`core.validators`)
Verifique se o GIF atende aos requisitos do Slack:
```python
from core.validators import validate_gif, is_slack_ready

# Detailed validation
passes, info = validate_gif('my.gif', is_emoji=True, verbose=True)

# Quick check
if is_slack_ready('my.gif'):
    print("Ready!")
```

### Easing Functions (`core.easing`)
Movimento suave em vez de linear:
```python
from core.easing import interpolate

# Progress from 0.0 to 1.0
t = i / (num_frames - 1)

# Apply easing
y = interpolate(start=0, end=400, t=t, easing='ease_out')

# Available: linear, ease_in, ease_out, ease_in_out,
#           bounce_out, elastic_out, back_out
```

### Frame Helpers (`core.frame_composer`)
Funções de conveniência para necessidades comuns:
```python
from core.frame_composer import (
    create_blank_frame,         # Solid color background
    create_gradient_background,  # Vertical gradient
    draw_circle,                # Helper for circles
    draw_text,                  # Simple text rendering
    draw_star                   # 5-pointed star
)
```

## Conceitos de Animação

### Shake/Vibração
Desloque a posição do objeto com oscilação:
- Use `math.sin()` ou `math.cos()` com o índice do frame
- Adicione pequenas variações aleatórias para sensação natural
- Aplique à posição x e/ou y

### Pulse/Batida Cardíaca
Dimensione o tamanho do objeto ritmicamente:
- Use `math.sin(t * frequency * 2 * math.pi)` para pulsação suave
- Para batida cardíaca: dois pulsos rápidos e depois pausa (ajuste a onda seno)
- Dimensione entre 0,8 e 1,2 do tamanho base

### Bounce
Objeto cai e quica:
- Use `interpolate()` com `easing='bounce_out'` para o pouso
- Use `easing='ease_in'` para queda (aceleração)
- Aplique gravidade aumentando a velocidade y a cada frame

### Spin/Rotação
Gire o objeto ao redor do centro:
- PIL: `image.rotate(angle, resample=Image.BICUBIC)`
- Para bamboleio: use onda seno para o ângulo em vez de linear

### Fade In/Out
Apareça ou desapareça gradualmente:
- Crie imagem RGBA, ajuste canal alfa
- Ou use `Image.blend(image1, image2, alpha)`
- Fade in: alfa de 0 a 1
- Fade out: alfa de 1 a 0

### Slide
Mova o objeto de fora da tela para a posição:
- Posição inicial: fora dos limites do frame
- Posição final: local de destino
- Use `interpolate()` com `easing='ease_out'` para parada suave
- Para ultrapassagem: use `easing='back_out'`

### Zoom
Dimensione e posicione para efeito de zoom:
- Zoom in: dimensione de 0,1 a 2,0, recorte centro
- Zoom out: dimensione de 2,0 a 1,0
- Pode adicionar motion blur para drama (filtro PIL)

### Explode/Particle Burst
Crie partículas irradiando para fora:
- Gere partículas com ângulos e velocidades aleatórios
- Atualize cada partícula: `x += vx`, `y += vy`
- Adicione gravidade: `vy += gravity_constant`
- Esvanecimento de partículas ao longo do tempo (reduza alfa)

## Estratégias de Otimização

Apenas quando solicitado a tornar o tamanho do arquivo menor, implemente alguns dos seguintes métodos:

1. **Menos frames** - FPS mais baixo (10 em vez de 20) ou duração menor
2. **Menos cores** - `num_colors=48` em vez de 128
3. **Dimensões menores** - 128x128 em vez de 480x480
4. **Remove duplicatas** - `remove_duplicates=True` em save()
5. **Modo emoji** - `optimize_for_emoji=True` otimiza automaticamente

```python
# Maximum optimization for emoji
builder.save(
    'emoji.gif',
    num_colors=48,
    optimize_for_emoji=True,
    remove_duplicates=True
)
```

## Filosofia

Esta skill fornece:
- **Conhecimento**: Requisitos do Slack e conceitos de animação
- **Utilitários**: GIFBuilder, validadores, funções de easing
- **Flexibilidade**: Crie a lógica de animação usando primitivos PIL

NÃO fornece:
- Templates de animação rígidos ou funções pré-fabricadas
- Renderização de fontes de emoji (não confiável em diferentes plataformas)
- Uma biblioteca de gráficos pré-empacotados integrados à skill

**Nota sobre uploads de usuários**: Esta skill não inclui gráficos pré-construídos, mas se um usuário enviar uma imagem, use PIL para carregá-la e trabalhar com ela - interprete com base em seu pedido se ele quer que seja usada diretamente ou apenas como inspiração.

Seja criativo! Combine conceitos (quicando + girando, pulsando + deslizando, etc.) e use as capacidades completas da PIL.

## Dependências

```bash
pip install pillow imageio numpy
```