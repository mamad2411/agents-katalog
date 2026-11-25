---
name: blip-2-vision-language
description: Framework de pré-treinamento visão-linguagem que conecta codificadores de imagem congelados e LLMs. Use quando você precisar de legendagem de imagens, resposta a perguntas visuais, recuperação imagem-texto ou chat multimodal com desempenho zero-shot de última geração.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Multimodal, Vision-Language, Image Captioning, VQA, Zero-Shot]
dependencies: [transformers>=4.30.0, torch>=1.10.0, Pillow]
---

# BLIP-2: Pré-treinamento Visão-Linguagem

Guia completo para usar BLIP-2 do Salesforce em tarefas visão-linguagem com codificadores de imagem congelados e grandes modelos de linguagem.

## Quando usar BLIP-2

**Use BLIP-2 quando:**
- Precisar de legendagem de imagem de alta qualidade com descrições naturais
- Estiver construindo sistemas de resposta a perguntas visuais (VQA)
- Exigir compreensão zero-shot de imagem-texto sem treinamento específico da tarefa
- Quiser aproveitar o raciocínio de LLM para tarefas visuais
- Estiver construindo IA conversacional multimodal
- Precisar de recuperação ou correspondência imagem-texto

**Recursos principais:**
- **Arquitetura Q-Former**: Transformer de consulta leve conecta visão e linguagem
- **Eficiência de backbone congelado**: Sem necessidade de afinar modelos de visão/linguagem grandes
- **Múltiplos backends de LLM**: OPT (2.7B, 6.7B) e FlanT5 (XL, XXL)
- **Capacidades zero-shot**: Desempenho forte sem treinamento específico da tarefa
- **Treinamento eficiente**: Treina apenas Q-Former (~188M de parâmetros)
- **Resultados de última geração**: Supera modelos maiores em benchmarks VQA

**Use alternativas em vez disso:**
- **LLaVA**: Para chat multimodal que segue instruções
- **InstructBLIP**: Para melhoria no seguimento de instruções (sucessor BLIP-2)
- **GPT-4V/Claude 3**: Para chat multimodal em produção (proprietário)
- **CLIP**: Para similaridade imagem-texto simples sem geração
- **Flamingo**: Para aprendizado visual em few-shot

## Início rápido

### Instalação

```bash
# HuggingFace Transformers (recomendado)
pip install transformers accelerate torch Pillow

# Ou biblioteca LAVIS (oficial Salesforce)
pip install salesforce-lavis
```

### Legendagem básica de imagem

```python
import torch
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration

# Carregar modelo e processador
processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-2.7b",
    torch_dtype=torch.float16,
    device_map="auto"
)

# Carregar imagem
image = Image.open("photo.jpg").convert("RGB")

# Gerar legenda
inputs = processor(images=image, return_tensors="pt").to("cuda", torch.float16)
generated_ids = model.generate(**inputs, max_new_tokens=50)
caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(caption)
```

### Resposta a perguntas visuais

```python
# Fazer uma pergunta sobre a imagem
question = "What color is the car in this image?"

inputs = processor(images=image, text=question, return_tensors="pt").to("cuda", torch.float16)
generated_ids = model.generate(**inputs, max_new_tokens=50)
answer = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(answer)
```

### Usando biblioteca LAVIS

```python
import torch
from lavis.models import load_model_and_preprocess
from PIL import Image

# Carregar modelo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model, vis_processors, txt_processors = load_model_and_preprocess(
    name="blip2_opt",
    model_type="pretrain_opt2.7b",
    is_eval=True,
    device=device
)

# Processar imagem
image = Image.open("photo.jpg").convert("RGB")
image = vis_processors["eval"](image).unsqueeze(0).to(device)

# Legenda
caption = model.generate({"image": image})
print(caption)

# VQA
question = txt_processors["eval"]("What is in this image?")
answer = model.generate({"image": image, "prompt": question})
print(answer)
```

## Conceitos principais

### Visão geral da arquitetura

```
Arquitetura BLIP-2:
┌─────────────────────────────────────────────────────────────┐
│                        Q-Former                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │     Consultas Aprendidas (32 consultas × 768 dim)   │    │
│  └────────────────────────┬────────────────────────────┘    │
│                           │                                  │
│  ┌────────────────────────▼────────────────────────────┐    │
│  │    Cross-Attention com Características de Imagem     │    │
│  └────────────────────────┬────────────────────────────┘    │
│                           │                                  │
│  ┌────────────────────────▼────────────────────────────┐    │
│  │    Camadas de Self-Attention (Transformer)           │    │
│  └────────────────────────┬────────────────────────────┘    │
└───────────────────────────┼─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│  Codificador de Visão Congelado   │  LLM Congelado         │
│  (ViT-G/14 de EVA-CLIP)           │  (OPT ou FlanT5)       │
└─────────────────────────────────────────────────────────────┘
```

### Variantes de modelo

| Modelo | Backend LLM | Tamanho | Caso de uso |
|-------|-------------|---------|----------|
| `blip2-opt-2.7b` | OPT-2.7B | ~4GB | Legendagem geral, VQA |
| `blip2-opt-6.7b` | OPT-6.7B | ~8GB | Melhor raciocínio |
| `blip2-flan-t5-xl` | FlanT5-XL | ~5GB | Seguimento de instruções |
| `blip2-flan-t5-xxl` | FlanT5-XXL | ~13GB | Melhor qualidade |

### Componentes Q-Former

| Componente | Descrição | Parâmetros |
|-----------|----------|------------|
| Consultas aprendidas | Conjunto fixo de embeddings treináveis | 32 × 768 |
| Transformer de imagem | Cross-attention para características visuais | ~108M |
| Transformer de texto | Self-attention para texto | ~108M |
| Projeção linear | Mapeia para dimensão do LLM | Varia |

## Uso avançado

### Processamento em lote

```python
from PIL import Image
import torch

# Carregar múltiplas imagens
images = [Image.open(f"image_{i}.jpg").convert("RGB") for i in range(4)]
questions = [
    "What is shown in this image?",
    "Describe the scene.",
    "What colors are prominent?",
    "Is there a person in this image?"
]

# Processar lote
inputs = processor(
    images=images,
    text=questions,
    return_tensors="pt",
    padding=True
).to("cuda", torch.float16)

# Gerar
generated_ids = model.generate(**inputs, max_new_tokens=50)
answers = processor.batch_decode(generated_ids, skip_special_tokens=True)

for q, a in zip(questions, answers):
    print(f"Q: {q}\nA: {a}\n")
```

### Controlando geração

```python
# Controlar parâmetros de geração
generated_ids = model.generate(
    **inputs,
    max_new_tokens=100,
    min_length=20,
    num_beams=5,              # Beam search
    no_repeat_ngram_size=2,   # Evitar repetição
    top_p=0.9,                # Nucleus sampling
    temperature=0.7,          # Criatividade
    do_sample=True,           # Ativar sampling
)

# Para saída determinística
generated_ids = model.generate(
    **inputs,
    max_new_tokens=50,
    num_beams=5,
    do_sample=False,
)
```

### Otimização de memória

```python
# Quantização 8-bit
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(load_in_8bit=True)

model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-6.7b",
    quantization_config=quantization_config,
    device_map="auto"
)

# Quantização 4-bit (mais agressiva)
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-flan-t5-xxl",
    quantization_config=quantization_config,
    device_map="auto"
)
```

### Correspondência imagem-texto

```python
# Usar LAVIS para ITM (Image-Text Matching)
from lavis.models import load_model_and_preprocess

model, vis_processors, txt_processors = load_model_and_preprocess(
    name="blip2_image_text_matching",
    model_type="pretrain",
    is_eval=True,
    device=device
)

image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
text = txt_processors["eval"]("a dog sitting on grass")

# Obter score de correspondência
itm_output = model({"image": image, "text_input": text}, match_head="itm")
itm_scores = torch.nn.functional.softmax(itm_output, dim=1)
print(f"Match probability: {itm_scores[:, 1].item():.3f}")
```

### Extração de características

```python
# Extrair características de imagem com Q-Former
from lavis.models import load_model_and_preprocess

model, vis_processors, _ = load_model_and_preprocess(
    name="blip2_feature_extractor",
    model_type="pretrain",
    is_eval=True,
    device=device
)

image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)

# Obter características
features = model.extract_features({"image": image}, mode="image")
image_embeds = features.image_embeds  # Shape: [1, 32, 768]
image_features = features.image_embeds_proj  # Projetado para correspondência
```

## Fluxos de trabalho comuns

### Fluxo 1: Pipeline de legendagem de imagem

```python
import torch
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from pathlib import Path

class ImageCaptioner:
    def __init__(self, model_name="Salesforce/blip2-opt-2.7b"):
        self.processor = Blip2Processor.from_pretrained(model_name)
        self.model = Blip2ForConditionalGeneration.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )

    def caption(self, image_path: str, prompt: str = None) -> str:
        image = Image.open(image_path).convert("RGB")

        if prompt:
            inputs = self.processor(images=image, text=prompt, return_tensors="pt")
        else:
            inputs = self.processor(images=image, return_tensors="pt")

        inputs = inputs.to("cuda", torch.float16)

        generated_ids = self.model.generate(
            **inputs,
            max_new_tokens=50,
            num_beams=5
        )

        return self.processor.decode(generated_ids[0], skip_special_tokens=True)

    def caption_batch(self, image_paths: list, prompt: str = None) -> list:
        images = [Image.open(p).convert("RGB") for p in image_paths]

        if prompt:
            inputs = self.processor(
                images=images,
                text=[prompt] * len(images),
                return_tensors="pt",
                padding=True
            )
        else:
            inputs = self.processor(images=images, return_tensors="pt", padding=True)

        inputs = inputs.to("cuda", torch.float16)

        generated_ids = self.model.generate(**inputs, max_new_tokens=50)
        return self.processor.batch_decode(generated_ids, skip_special_tokens=True)

# Uso
captioner = ImageCaptioner()

# Imagem única
caption = captioner.caption("photo.jpg")
print(f"Caption: {caption}")

# Com prompt para estilo
caption = captioner.caption("photo.jpg", "a detailed description of")
print(f"Detailed: {caption}")

# Processamento em lote
captions = captioner.caption_batch(["img1.jpg", "img2.jpg", "img3.jpg"])
for i, cap in enumerate(captions):
    print(f"Image {i+1}: {cap}")
```

### Fluxo 2: Sistema de Q&A Visual

```python
class VisualQA:
    def __init__(self, model_name="Salesforce/blip2-flan-t5-xl"):
        self.processor = Blip2Processor.from_pretrained(model_name)
        self.model = Blip2ForConditionalGeneration.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.current_image = None
        self.current_inputs = None

    def set_image(self, image_path: str):
        """Carregar imagem para múltiplas perguntas."""
        self.current_image = Image.open(image_path).convert("RGB")

    def ask(self, question: str) -> str:
        """Fazer uma pergunta sobre a imagem atual."""
        if self.current_image is None:
            raise ValueError("No image set. Call set_image() first.")

        # Formatar pergunta para FlanT5
        prompt = f"Question: {question} Answer:"

        inputs = self.processor(
            images=self.current_image,
            text=prompt,
            return_tensors="pt"
        ).to("cuda", torch.float16)

        generated_ids = self.model.generate(
            **inputs,
            max_new_tokens=50,
            num_beams=5
        )

        return self.processor.decode(generated_ids[0], skip_special_tokens=True)

    def ask_multiple(self, questions: list) -> dict:
        """Fazer múltiplas perguntas sobre imagem atual."""
        return {q: self.ask(q) for q in questions}

# Uso
vqa = VisualQA()
vqa.set_image("scene.jpg")

# Fazer perguntas
print(vqa.ask("What objects are in this image?"))
print(vqa.ask("What is the weather like?"))
print(vqa.ask("How many people are there?"))

# Perguntas em lote
results = vqa.ask_multiple([
    "What is the main subject?",
    "What colors are dominant?",
    "Is this indoors or outdoors?"
])
```

### Fluxo 3: Busca/Recuperação de imagem

```python
import torch
import numpy as np
from PIL import Image
from lavis.models import load_model_and_preprocess

class ImageSearchEngine:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.vis_processors, self.txt_processors = load_model_and_preprocess(
            name="blip2_feature_extractor",
            model_type="pretrain",
            is_eval=True,
            device=self.device
        )
        self.image_features = []
        self.image_paths = []

    def index_images(self, image_paths: list):
        """Construir índice de imagens."""
        self.image_paths = image_paths

        for path in image_paths:
            image = Image.open(path).convert("RGB")
            image = self.vis_processors["eval"](image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                features = self.model.extract_features({"image": image}, mode="image")
                # Usar características projetadas para correspondência
                self.image_features.append(
                    features.image_embeds_proj.mean(dim=1).cpu().numpy()
                )

        self.image_features = np.vstack(self.image_features)

    def search(self, query: str, top_k: int = 5) -> list:
        """Buscar imagens por query de texto."""
        # Obter características de texto
        text = self.txt_processors["eval"](query)
        text_input = {"text_input": [text]}

        with torch.no_grad():
            text_features = self.model.extract_features(text_input, mode="text")
            text_embeds = text_features.text_embeds_proj[:, 0].cpu().numpy()

        # Calcular similaridades
        similarities = np.dot(self.image_features, text_embeds.T).squeeze()
        top_indices = np.argsort(similarities)[::-1][:top_k]

        return [(self.image_paths[i], similarities[i]) for i in top_indices]

# Uso
engine = ImageSearchEngine()
engine.index_images(["img1.jpg", "img2.jpg", "img3.jpg", ...])

# Buscar
results = engine.search("a sunset over the ocean", top_k=5)
for path, score in results:
    print(f"{path}: {score:.3f}")
```

## Formato de saída

### Saída de geração

```python
# Geração direta retorna IDs de token
generated_ids = model.generate(**inputs, max_new_tokens=50)
# Shape: [batch_size, sequence_length]

# Decodificar para texto
text = processor.batch_decode(generated_ids, skip_special_tokens=True)
# Retorna: lista de strings
```

### Saída de extração de características

```python
# Saídas Q-Former
features = model.extract_features({"image": image}, mode="image")

features.image_embeds          # [B, 32, 768] - Saídas Q-Former
features.image_embeds_proj     # [B, 32, 256] - Projetado para correspondência
features.text_embeds          # [B, seq_len, 768] - Características de texto
features.text_embeds_proj     # [B, 256] - Texto projetado (CLS)
```

## Otimização de desempenho

### Requisitos de memória GPU

| Modelo | VRAM FP16 | VRAM INT8 | VRAM INT4 |
|-------|-----------|-----------|-----------|
| blip2-opt-2.7b | ~8GB | ~5GB | ~3GB |
| blip2-opt-6.7b | ~16GB | ~9GB | ~5GB |
| blip2-flan-t5-xl | ~10GB | ~6GB | ~4GB |
| blip2-flan-t5-xxl | ~26GB | ~14GB | ~8GB |

### Otimização de velocidade

```python
# Usar Flash Attention se disponível
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-2.7b",
    torch_dtype=torch.float16,
    attn_implementation="flash_attention_2",  # Requer flash-attn
    device_map="auto"
)

# Compilar modelo (PyTorch 2.0+)
model = torch.compile(model)

# Usar imagens menores (se qualidade permitir)
processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
# Padrão é 224x224, que é ótimo
```

## Problemas comuns

| Problema | Solução |
|-------|----------|
| CUDA OOM | Use quantização INT8/INT4, modelo menor |
| Geração lenta | Use decodificação greedy, reduza max_new_tokens |
| Legendas ruins | Tente variante FlanT5, use prompts |
| Alucinações | Diminua temperature, use beam search |
| Respostas erradas | Reformule pergunta, forneça contexto |

## Referências

- **[Uso avançado](references/advanced-usage.md)** - Fine-tuning, integração, deployment
- **[Resolução de problemas](references/troubleshooting.md)** - Problemas comuns e soluções

## Recursos

- **Paper**: https://arxiv.org/abs/2301.12597
- **GitHub (LAVIS)**: https://github.com/salesforce/LAVIS
- **HuggingFace**: https://huggingface.co/Salesforce/blip2-opt-2.7b
- **Demo**: https://huggingface.co/spaces/Salesforce/BLIP2
- **InstructBLIP**: https://arxiv.org/abs/2305.06500 (sucessor)