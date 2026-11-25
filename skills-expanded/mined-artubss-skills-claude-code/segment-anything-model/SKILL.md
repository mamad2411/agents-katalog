---
name: segment-anything-model
description: Modelo de fundação para segmentação de imagens com transferência zero-shot. Use quando precisar segmentar qualquer objeto em imagens usando pontos, caixas ou máscaras como prompts, ou gerar automaticamente todas as máscaras de objetos em uma imagem.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Multimodal, Image Segmentation, Computer Vision, SAM, Zero-Shot]
dependencies: [segment-anything, transformers>=4.30.0, torch>=1.7.0]
---

# Segment Anything Model (SAM)

Guia abrangente para usar o Segment Anything Model da Meta AI para segmentação de imagens zero-shot.

## Quando usar SAM

**Use SAM quando:**
- Precisar segmentar qualquer objeto em imagens sem treinamento específico da tarefa
- Construir ferramentas de anotação interativas com prompts de ponto/caixa
- Gerar dados de treinamento para outros modelos de visão
- Precisar de transferência zero-shot para novos domínios de imagem
- Construir pipelines de detecção/segmentação de objetos
- Processar imagens médicas, de satélite ou específicas de domínio

**Principais características:**
- **Segmentação zero-shot**: Funciona em qualquer domínio de imagem sem fine-tuning
- **Prompts flexíveis**: Pontos, caixas delimitadoras ou máscaras anteriores
- **Segmentação automática**: Gera todas as máscaras de objetos automaticamente
- **Alta qualidade**: Treinado em 1,1 bilhão de máscaras de 11 milhões de imagens
- **Múltiplos tamanhos de modelo**: ViT-B (mais rápido), ViT-L, ViT-H (mais preciso)
- **Exportação ONNX**: Deploy em navegadores e dispositivos edge

**Use alternativas em vez disso:**
- **YOLO/Detectron2**: Para detecção de objetos em tempo real com classes
- **Mask2Former**: Para segmentação semântica/panóptica com categorias
- **GroundingDINO + SAM**: Para segmentação com prompt de texto
- **SAM 2**: Para tarefas de segmentação de vídeo

## Início rápido

### Instalação

```bash
# Do GitHub
pip install git+https://github.com/facebookresearch/segment-anything.git

# Dependências opcionais
pip install opencv-python pycocotools matplotlib

# Ou use transformers do HuggingFace
pip install transformers
```

### Baixar checkpoints

```bash
# ViT-H (maior, mais preciso) - 2.4GB
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth

# ViT-L (médio) - 1.2GB
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth

# ViT-B (menor, mais rápido) - 375MB
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
```

### Uso básico com SamPredictor

```python
import numpy as np
from segment_anything import sam_model_registry, SamPredictor

# Carregar modelo
sam = sam_model_registry["vit_h"](checkpoint="sam_vit_h_4b8939.pth")
sam.to(device="cuda")

# Criar preditor
predictor = SamPredictor(sam)

# Definir imagem (calcula embeddings uma vez)
image = cv2.imread("image.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
predictor.set_image(image)

# Prever com prompts de ponto
input_point = np.array([[500, 375]])  # coordenadas (x, y)
input_label = np.array([1])  # 1 = foreground, 0 = background

masks, scores, logits = predictor.predict(
    point_coords=input_point,
    point_labels=input_label,
    multimask_output=True  # Retorna 3 opções de máscara
)

# Selecionar melhor máscara
best_mask = masks[np.argmax(scores)]
```

### HuggingFace Transformers

```python
import torch
from PIL import Image
from transformers import SamModel, SamProcessor

# Carregar modelo e processador
model = SamModel.from_pretrained("facebook/sam-vit-huge")
processor = SamProcessor.from_pretrained("facebook/sam-vit-huge")
model.to("cuda")

# Processar imagem com prompt de ponto
image = Image.open("image.jpg")
input_points = [[[450, 600]]]  # Lote de pontos

inputs = processor(image, input_points=input_points, return_tensors="pt")
inputs = {k: v.to("cuda") for k, v in inputs.items()}

# Gerar máscaras
with torch.no_grad():
    outputs = model(**inputs)

# Pós-processar máscaras para tamanho original
masks = processor.image_processor.post_process_masks(
    outputs.pred_masks.cpu(),
    inputs["original_sizes"].cpu(),
    inputs["reshaped_input_sizes"].cpu()
)
```

## Conceitos principais

### Arquitetura do modelo

```
Arquitetura SAM:
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Image Encoder  │────▶│ Prompt Encoder  │────▶│  Mask Decoder   │
│     (ViT)       │     │ (Points/Boxes)  │     │ (Transformer)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
   Image Embeddings      Prompt Embeddings         Masks + IoU
   (computed once)       (per prompt)             predictions
```

### Variantes do modelo

| Modelo | Checkpoint | Tamanho | Velocidade | Precisão |
|--------|------------|--------|-----------|----------|
| ViT-H | `vit_h` | 2.4 GB | Mais lenta | Melhor |
| ViT-L | `vit_l` | 1.2 GB | Médium | Boa |
| ViT-B | `vit_b` | 375 MB | Mais rápida | Boa |

### Tipos de prompt

| Prompt | Descrição | Caso de uso |
|--------|-----------|-----------|
| Ponto (foreground) | Clique no objeto | Seleção de objeto único |
| Ponto (background) | Clique fora do objeto | Excluir regiões |
| Caixa delimitadora | Retângulo ao redor do objeto | Objetos maiores |
| Máscara anterior | Entrada de máscara de baixa resolução | Refinamento iterativo |

## Segmentação interativa

### Prompts de ponto

```python
# Ponto único de foreground
input_point = np.array([[500, 375]])
input_label = np.array([1])

masks, scores, logits = predictor.predict(
    point_coords=input_point,
    point_labels=input_label,
    multimask_output=True
)

# Múltiplos pontos (foreground + background)
input_points = np.array([[500, 375], [600, 400], [450, 300]])
input_labels = np.array([1, 1, 0])  # 2 foreground, 1 background

masks, scores, logits = predictor.predict(
    point_coords=input_points,
    point_labels=input_labels,
    multimask_output=False  # Máscara única quando prompts são claros
)
```

### Prompts de caixa

```python
# Caixa delimitadora [x1, y1, x2, y2]
input_box = np.array([425, 600, 700, 875])

masks, scores, logits = predictor.predict(
    box=input_box,
    multimask_output=False
)
```

### Prompts combinados

```python
# Caixa + pontos para controle preciso
masks, scores, logits = predictor.predict(
    point_coords=np.array([[500, 375]]),
    point_labels=np.array([1]),
    box=np.array([400, 300, 700, 600]),
    multimask_output=False
)
```

### Refinamento iterativo

```python
# Predição inicial
masks, scores, logits = predictor.predict(
    point_coords=np.array([[500, 375]]),
    point_labels=np.array([1]),
    multimask_output=True
)

# Refinar com ponto adicional usando máscara anterior
masks, scores, logits = predictor.predict(
    point_coords=np.array([[500, 375], [550, 400]]),
    point_labels=np.array([1, 0]),  # Adicionar ponto de background
    mask_input=logits[np.argmax(scores)][None, :, :],  # Usar melhor máscara
    multimask_output=False
)
```

## Geração automática de máscaras

### Segmentação automática básica

```python
from segment_anything import SamAutomaticMaskGenerator

# Criar gerador
mask_generator = SamAutomaticMaskGenerator(sam)

# Gerar todas as máscaras
masks = mask_generator.generate(image)

# Cada máscara contém:
# - segmentation: máscara binária
# - bbox: [x, y, w, h]
# - area: contagem de pixels
# - predicted_iou: pontuação de qualidade
# - stability_score: pontuação de robustez
# - point_coords: ponto gerador
```

### Geração customizada

```python
mask_generator = SamAutomaticMaskGenerator(
    model=sam,
    points_per_side=32,          # Densidade de grade (mais = mais máscaras)
    pred_iou_thresh=0.88,        # Limiar de qualidade
    stability_score_thresh=0.95,  # Limiar de estabilidade
    crop_n_layers=1,             # Crops multi-escala
    crop_n_points_downscale_factor=2,
    min_mask_region_area=100,    # Remover máscaras minúsculas
)

masks = mask_generator.generate(image)
```

### Filtragem de máscaras

```python
# Ordenar por área (maior primeiro)
masks = sorted(masks, key=lambda x: x['area'], reverse=True)

# Filtrar por IoU predito
high_quality = [m for m in masks if m['predicted_iou'] > 0.9]

# Filtrar por pontuação de estabilidade
stable_masks = [m for m in masks if m['stability_score'] > 0.95]
```

## Inferência em lote

### Múltiplas imagens

```python
# Processar múltiplas imagens eficientemente
images = [cv2.imread(f"image_{i}.jpg") for i in range(10)]

all_masks = []
for image in images:
    predictor.set_image(image)
    masks, _, _ = predictor.predict(
        point_coords=np.array([[500, 375]]),
        point_labels=np.array([1]),
        multimask_output=True
    )
    all_masks.append(masks)
```

### Múltiplos prompts por imagem

```python
# Processar múltiplos prompts eficientemente (uma codificação de imagem)
predictor.set_image(image)

# Lote de prompts de ponto
points = [
    np.array([[100, 100]]),
    np.array([[200, 200]]),
    np.array([[300, 300]])
]

all_masks = []
for point in points:
    masks, scores, _ = predictor.predict(
        point_coords=point,
        point_labels=np.array([1]),
        multimask_output=True
    )
    all_masks.append(masks[np.argmax(scores)])
```

## Deploy ONNX

### Exportar modelo

```bash
python scripts/export_onnx_model.py \
    --checkpoint sam_vit_h_4b8939.pth \
    --model-type vit_h \
    --output sam_onnx.onnx \
    --return-single-mask
```

### Usar modelo ONNX

```python
import onnxruntime

# Carregar modelo ONNX
ort_session = onnxruntime.InferenceSession("sam_onnx.onnx")

# Executar inferência (embeddings de imagem calculados separadamente)
masks = ort_session.run(
    None,
    {
        "image_embeddings": image_embeddings,
        "point_coords": point_coords,
        "point_labels": point_labels,
        "mask_input": np.zeros((1, 1, 256, 256), dtype=np.float32),
        "has_mask_input": np.array([0], dtype=np.float32),
        "orig_im_size": np.array([h, w], dtype=np.float32)
    }
)
```

## Workflows comuns

### Workflow 1: Ferramenta de anotação

```python
import cv2

# Carregar modelo
predictor = SamPredictor(sam)
predictor.set_image(image)

def on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Ponto de foreground
        masks, scores, _ = predictor.predict(
            point_coords=np.array([[x, y]]),
            point_labels=np.array([1]),
            multimask_output=True
        )
        # Exibir melhor máscara
        display_mask(masks[np.argmax(scores)])
```

### Workflow 2: Extração de objeto

```python
def extract_object(image, point):
    """Extrair objeto no ponto com fundo transparente."""
    predictor.set_image(image)

    masks, scores, _ = predictor.predict(
        point_coords=np.array([point]),
        point_labels=np.array([1]),
        multimask_output=True
    )

    best_mask = masks[np.argmax(scores)]

    # Criar saída RGBA
    rgba = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)
    rgba[:, :, :3] = image
    rgba[:, :, 3] = best_mask * 255

    return rgba
```

### Workflow 3: Segmentação de imagem médica

```python
# Processar imagens médicas (escala de cinza para RGB)
medical_image = cv2.imread("scan.png", cv2.IMREAD_GRAYSCALE)
rgb_image = cv2.cvtColor(medical_image, cv2.COLOR_GRAY2RGB)

predictor.set_image(rgb_image)

# Segmentar região de interesse
masks, scores, _ = predictor.predict(
    box=np.array([x1, y1, x2, y2]),  # Caixa de ROI
    multimask_output=True
)
```

## Formato de saída

### Estrutura de dados de máscara

```python
# Saída de SamAutomaticMaskGenerator
{
    "segmentation": np.ndarray,  # Máscara binária H×W
    "bbox": [x, y, w, h],        # Caixa delimitadora
    "area": int,                 # Contagem de pixels
    "predicted_iou": float,      # Pontuação de qualidade 0-1
    "stability_score": float,    # Pontuação de robustez 0-1
    "crop_box": [x, y, w, h],    # Região de crop de geração
    "point_coords": [[x, y]],    # Ponto de entrada
}
```

### Formato COCO RLE

```python
from pycocotools import mask as mask_utils

# Codificar máscara para RLE
rle = mask_utils.encode(np.asfortranarray(mask.astype(np.uint8)))
rle["counts"] = rle["counts"].decode("utf-8")

# Decodificar RLE para máscara
decoded_mask = mask_utils.decode(rle)
```

## Otimização de desempenho

### Memória GPU

```python
# Usar modelo menor para VRAM limitada
sam = sam_model_registry["vit_b"](checkpoint="sam_vit_b_01ec64.pth")

# Processar imagens em lotes
# Limpar cache CUDA entre lotes grandes
torch.cuda.empty_cache()
```

### Otimização de velocidade

```python
# Usar precisão reduzida
sam = sam.half()

# Reduzir pontos para geração automática
mask_generator = SamAutomaticMaskGenerator(
    model=sam,
    points_per_side=16,  # Padrão é 32
)

# Usar ONNX para deploy
# Exportar com --return-single-mask para inferência mais rápida
```

## Problemas comuns

| Problema | Solução |
|----------|---------|
| Falta de memória | Usar modelo ViT-B, reduzir tamanho da imagem |
| Inferência lenta | Usar ViT-B, reduzir points_per_side |
| Qualidade de máscara ruim | Tentar prompts diferentes, usar caixa + pontos |
| Artefatos nas bordas | Usar filtragem de pontuação de estabilidade |
| Objetos pequenos perdidos | Aumentar points_per_side |

## Referências

- **[Uso avançado](references/advanced-usage.md)** - Batching, fine-tuning, integração
- **[Resolução de problemas](references/troubleshooting.md)** - Problemas comuns e soluções

## Recursos

- **GitHub**: https://github.com/facebookresearch/segment-anything
- **Paper**: https://arxiv.org/abs/2304.02643
- **Demo**: https://segment-anything.com
- **SAM 2 (Vídeo)**: https://github.com/facebookresearch/segment-anything-2
- **HuggingFace**: https://huggingface.co/facebook/sam-vit-huge