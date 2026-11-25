---
name: llava
description: Assistente de Linguagem Grande e Visão. Habilita ajuste de instrução visual e conversas baseadas em imagem. Combina encoder de visão CLIP com modelos de linguagem Vicuna/LLaMA. Suporta chat multi-turno com imagem, resposta a perguntas visuais e seguimento de instruções. Use para chatbots visão-linguagem ou tarefas de compreensão de imagem. Melhor para análise conversacional de imagem.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [LLaVA, Vision-Language, Multimodal, Visual Question Answering, Image Chat, CLIP, Vicuna, Conversational AI, Instruction Tuning, VQA]
dependencies: [transformers, torch, pillow]
---

# LLaVA - Assistente de Linguagem Grande e Visão

Modelo visão-linguagem open-source para compreensão conversacional de imagem.

## Quando usar LLaVA

**Use quando:**
- Construir chatbots visão-linguagem
- Resposta a perguntas visuais (VQA)
- Descrição e legenda de imagem
- Conversas multi-turno com imagem
- Seguimento de instruções visuais
- Compreensão de documentos com imagens

**Métricas**:
- **23.000+ stars no GitHub**
- Capacidades em nível GPT-4V (alvo)
- Licença Apache 2.0
- Múltiplos tamanhos de modelo (7B-34B parâmetros)

**Use alternativas em vez disso**:
- **GPT-4V**: Qualidade máxima, baseado em API
- **CLIP**: Classificação zero-shot simples
- **BLIP-2**: Melhor apenas para legenda
- **Flamingo**: Pesquisa, não open-source

## Quick start

### Instalação

```bash
# Clone repository
git clone https://github.com/haotian-liu/LLaVA
cd LLaVA

# Install
pip install -e .
```

### Uso básico

```python
from llava.model.builder import load_pretrained_model
from llava.mm_utils import get_model_name_from_path, process_images, tokenizer_image_token
from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN
from llava.conversation import conv_templates
from PIL import Image
import torch

# Load model
model_path = "liuhaotian/llava-v1.5-7b"
tokenizer, model, image_processor, context_len = load_pretrained_model(
    model_path=model_path,
    model_base=None,
    model_name=get_model_name_from_path(model_path)
)

# Load image
image = Image.open("image.jpg")
image_tensor = process_images([image], image_processor, model.config)
image_tensor = image_tensor.to(model.device, dtype=torch.float16)

# Create conversation
conv = conv_templates["llava_v1"].copy()
conv.append_message(conv.roles[0], DEFAULT_IMAGE_TOKEN + "\nWhat is in this image?")
conv.append_message(conv.roles[1], None)
prompt = conv.get_prompt()

# Generate response
input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).to(model.device)

with torch.inference_mode():
    output_ids = model.generate(
        input_ids,
        images=image_tensor,
        do_sample=True,
        temperature=0.2,
        max_new_tokens=512
    )

response = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
print(response)
```

## Modelos disponíveis

| Modelo | Parâmetros | VRAM | Qualidade |
|-------|------------|------|---------|
| LLaVA-v1.5-7B | 7B | ~14 GB | Boa |
| LLaVA-v1.5-13B | 13B | ~28 GB | Melhor |
| LLaVA-v1.6-34B | 34B | ~70 GB | Melhor |

```python
# Load different models
model_7b = "liuhaotian/llava-v1.5-7b"
model_13b = "liuhaotian/llava-v1.5-13b"
model_34b = "liuhaotian/llava-v1.6-34b"

# 4-bit quantization for lower VRAM
load_4bit = True  # Reduces VRAM by ~4×
```

## Uso de CLI

```bash
# Single image query
python -m llava.serve.cli \
    --model-path liuhaotian/llava-v1.5-7b \
    --image-file image.jpg \
    --query "What is in this image?"

# Multi-turn conversation
python -m llava.serve.cli \
    --model-path liuhaotian/llava-v1.5-7b \
    --image-file image.jpg
# Then type questions interactively
```

## Interface Web (Gradio)

```bash
# Launch Gradio interface
python -m llava.serve.gradio_web_server \
    --model-path liuhaotian/llava-v1.5-7b \
    --load-4bit  # Optional: reduce VRAM

# Access at http://localhost:7860
```

## Conversas multi-turno

```python
# Initialize conversation
conv = conv_templates["llava_v1"].copy()

# Turn 1
conv.append_message(conv.roles[0], DEFAULT_IMAGE_TOKEN + "\nWhat is in this image?")
conv.append_message(conv.roles[1], None)
response1 = generate(conv, model, image)  # "A dog playing in a park"

# Turn 2
conv.messages[-1][1] = response1  # Add previous response
conv.append_message(conv.roles[0], "What breed is the dog?")
conv.append_message(conv.roles[1], None)
response2 = generate(conv, model, image)  # "Golden Retriever"

# Turn 3
conv.messages[-1][1] = response2
conv.append_message(conv.roles[0], "What time of day is it?")
conv.append_message(conv.roles[1], None)
response3 = generate(conv, model, image)
```

## Tarefas comuns

### Legendagem de imagem

```python
question = "Describe this image in detail."
response = ask(model, image, question)
```

### Resposta a perguntas visuais

```python
question = "How many people are in the image?"
response = ask(model, image, question)
```

### Detecção de objeto (textual)

```python
question = "List all the objects you can see in this image."
response = ask(model, image, question)
```

### Compreensão de cena

```python
question = "What is happening in this scene?"
response = ask(model, image, question)
```

### Compreensão de documento

```python
question = "What is the main topic of this document?"
response = ask(model, document_image, question)
```

## Treinamento de modelo personalizado

```bash
# Stage 1: Feature alignment (558K image-caption pairs)
bash scripts/v1_5/pretrain.sh

# Stage 2: Visual instruction tuning (150K instruction data)
bash scripts/v1_5/finetune.sh
```

## Quantização (reduzir VRAM)

```python
# 4-bit quantization
tokenizer, model, image_processor, context_len = load_pretrained_model(
    model_path="liuhaotian/llava-v1.5-13b",
    model_base=None,
    model_name=get_model_name_from_path("liuhaotian/llava-v1.5-13b"),
    load_4bit=True  # Reduces VRAM ~4×
)

# 8-bit quantization
load_8bit=True  # Reduces VRAM ~2×
```

## Melhores práticas

1. **Comece com modelo 7B** - Boa qualidade, VRAM gerenciável
2. **Use quantização 4-bit** - Reduz VRAM significativamente
3. **GPU obrigatória** - Inferência em CPU é extremamente lenta
4. **Prompts claros** - Perguntas específicas têm respostas melhores
5. **Conversas multi-turno** - Mantenha contexto da conversa
6. **Temperatura 0.2-0.7** - Equilibre criatividade/consistência
7. **max_new_tokens 512-1024** - Para respostas detalhadas
8. **Processamento em lote** - Processe múltiplas imagens sequencialmente

## Performance

| Modelo | VRAM (FP16) | VRAM (4-bit) | Velocidade (tokens/s) |
|-------|-------------|--------------|------------------|
| 7B | ~14 GB | ~4 GB | ~20 |
| 13B | ~28 GB | ~8 GB | ~12 |
| 34B | ~70 GB | ~18 GB | ~5 |

*Em GPU A100*

## Benchmarks

LLaVA atinge pontuações competitivas em:
- **VQAv2**: 78.5%
- **GQA**: 62.0%
- **MM-Vet**: 35.4%
- **MMBench**: 64.3%

## Limitações

1. **Alucinações** - Pode descrever coisas não presentes na imagem
2. **Raciocínio espacial** - Dificuldade com localizações precisas
3. **Texto pequeno** - Dificuldade em ler letras miúdas
4. **Contagem de objetos** - Impreciso para muitos objetos
5. **Requisitos de VRAM** - Precisa de GPU poderosa
6. **Velocidade de inferência** - Mais lento que CLIP

## Integração com frameworks

### LangChain

```python
from langchain.llms.base import LLM

class LLaVALLM(LLM):
    def _call(self, prompt, stop=None):
        # Custom LLaVA inference
        return response

llm = LLaVALLM()
```

### Aplicativo Gradio

```python
import gradio as gr

def chat(image, text, history):
    response = ask_llava(model, image, text)
    return response

demo = gr.ChatInterface(
    chat,
    additional_inputs=[gr.Image(type="pil")],
    title="LLaVA Chat"
)
demo.launch()
```

## Recursos

- **GitHub**: https://github.com/haotian-liu/LLaVA ⭐ 23.000+
- **Paper**: https://arxiv.org/abs/2304.08485
- **Demo**: https://llava.hliu.cc
- **Models**: https://huggingface.co/liuhaotian
- **Licença**: Apache 2.0