---
name: audiocraft-audio-generation
description: Biblioteca PyTorch para geração de áudio incluindo text-to-music (MusicGen) e text-to-sound (AudioGen). Use quando precisar gerar música a partir de descrições de texto, criar efeitos sonoros ou realizar geração de música condicionada por melodia.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Multimodal, Audio Generation, Text-to-Music, Text-to-Audio, MusicGen]
dependencies: [audiocraft, torch>=2.0.0, transformers>=4.30.0]
---

# AudioCraft: Geração de Áudio

Guia abrangente para usar AudioCraft da Meta para geração text-to-music e text-to-audio com MusicGen, AudioGen e EnCodec.

## Quando usar AudioCraft

**Use AudioCraft quando:**
- Precisar gerar música a partir de descrições de texto
- Criar efeitos sonoros e áudio ambiente
- Construir aplicações de geração de música
- Precisar de geração de música condicionada por melodia
- Quiser saída de áudio estéreo
- Necessitar de geração de música controlável com style transfer

**Principais recursos:**
- **MusicGen**: Geração text-to-music com condicionamento de melodia
- **AudioGen**: Geração de efeitos sonoros a partir de texto
- **EnCodec**: Codec neural de áudio de alta fidelidade
- **Múltiplos tamanhos de modelo**: Small (300M) a Large (3.3B)
- **Suporte estéreo**: Geração completa de áudio estéreo
- **Condicionamento de estilo**: MusicGen-Style para geração baseada em referência

**Use alternativas em vez disso:**
- **Stable Audio**: Para geração de música comercial mais longa
- **Bark**: Para text-to-speech com música/efeitos sonoros
- **Riffusion**: Para geração de música baseada em spectrograma
- **OpenAI Jukebox**: Para geração de áudio bruto com letras

## Início rápido

### Instalação

```bash
# Do PyPI
pip install audiocraft

# Do GitHub (versão mais recente)
pip install git+https://github.com/facebookresearch/audiocraft.git

# Ou use HuggingFace Transformers
pip install transformers torch torchaudio
```

### Text-to-music básico (AudioCraft)

```python
import torchaudio
from audiocraft.models import MusicGen

# Carregar modelo
model = MusicGen.get_pretrained('facebook/musicgen-small')

# Definir parâmetros de geração
model.set_generation_params(
    duration=8,  # segundos
    top_k=250,
    temperature=1.0
)

# Gerar a partir de texto
descriptions = ["happy upbeat electronic dance music with synths"]
wav = model.generate(descriptions)

# Salvar áudio
torchaudio.save("output.wav", wav[0].cpu(), sample_rate=32000)
```

### Usando HuggingFace Transformers

```python
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy

# Carregar modelo e processador
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
model.to("cuda")

# Gerar música
inputs = processor(
    text=["80s pop track with bassy drums and synth"],
    padding=True,
    return_tensors="pt"
).to("cuda")

audio_values = model.generate(
    **inputs,
    do_sample=True,
    guidance_scale=3,
    max_new_tokens=256
)

# Salvar
sampling_rate = model.config.audio_encoder.sampling_rate
scipy.io.wavfile.write("output.wav", rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())
```

### Text-to-sound com AudioGen

```python
from audiocraft.models import AudioGen

# Carregar AudioGen
model = AudioGen.get_pretrained('facebook/audiogen-medium')

model.set_generation_params(duration=5)

# Gerar efeitos sonoros
descriptions = ["dog barking in a park with birds chirping"]
wav = model.generate(descriptions)

torchaudio.save("sound.wav", wav[0].cpu(), sample_rate=16000)
```

## Conceitos principais

### Visão geral da arquitetura

```
AudioCraft Architecture:
┌──────────────────────────────────────────────────────────────┐
│                    Text Encoder (T5)                          │
│                         │                                     │
│                    Text Embeddings                            │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│              Transformer Decoder (LM)                         │
│     Auto-regressively generates audio tokens                  │
│     Using efficient token interleaving patterns               │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                EnCodec Audio Decoder                          │
│        Converts tokens back to audio waveform                 │
└──────────────────────────────────────────────────────────────┘
```

### Variantes de modelo

| Modelo | Tamanho | Descrição | Caso de uso |
|--------|---------|-----------|-------------|
| `musicgen-small` | 300M | Text-to-music | Geração rápida |
| `musicgen-medium` | 1.5B | Text-to-music | Equilibrado |
| `musicgen-large` | 3.3B | Text-to-music | Melhor qualidade |
| `musicgen-melody` | 1.5B | Texto + melodia | Condicionamento de melodia |
| `musicgen-melody-large` | 3.3B | Texto + melodia | Melhor melodia |
| `musicgen-stereo-*` | Varia | Saída estéreo | Geração estéreo |
| `musicgen-style` | 1.5B | Style transfer | Baseado em referência |
| `audiogen-medium` | 1.5B | Text-to-sound | Efeitos sonoros |

### Parâmetros de geração

| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| `duration` | 8.0 | Comprimento em segundos (1-120) |
| `top_k` | 250 | Amostragem top-k |
| `top_p` | 0.0 | Amostragem nucleus (0 = desabilitado) |
| `temperature` | 1.0 | Temperatura de amostragem |
| `cfg_coef` | 3.0 | Orientação sem classificador |

## Uso de MusicGen

### Geração text-to-music

```python
from audiocraft.models import MusicGen
import torchaudio

model = MusicGen.get_pretrained('facebook/musicgen-medium')

# Configurar geração
model.set_generation_params(
    duration=30,          # Até 30 segundos
    top_k=250,            # Diversidade de amostragem
    top_p=0.0,            # 0 = usar apenas top_k
    temperature=1.0,      # Criatividade (maior = mais variado)
    cfg_coef=3.0          # Aderência ao texto (maior = mais rigoroso)
)

# Gerar múltiplas amostras
descriptions = [
    "epic orchestral soundtrack with strings and brass",
    "chill lo-fi hip hop beat with jazzy piano",
    "energetic rock song with electric guitar"
]

# Gerar (retorna [batch, channels, samples])
wav = model.generate(descriptions)

# Salvar cada uma
for i, audio in enumerate(wav):
    torchaudio.save(f"music_{i}.wav", audio.cpu(), sample_rate=32000)
```

### Geração condicionada por melodia

```python
from audiocraft.models import MusicGen
import torchaudio

# Carregar modelo de melodia
model = MusicGen.get_pretrained('facebook/musicgen-melody')
model.set_generation_params(duration=30)

# Carregar áudio de melodia
melody, sr = torchaudio.load("melody.wav")

# Gerar com condicionamento de melodia
descriptions = ["acoustic guitar folk song"]
wav = model.generate_with_chroma(descriptions, melody, sr)

torchaudio.save("melody_conditioned.wav", wav[0].cpu(), sample_rate=32000)
```

### Geração estéreo

```python
from audiocraft.models import MusicGen

# Carregar modelo estéreo
model = MusicGen.get_pretrained('facebook/musicgen-stereo-medium')
model.set_generation_params(duration=15)

descriptions = ["ambient electronic music with wide stereo panning"]
wav = model.generate(descriptions)

# forma wav: [batch, 2, samples] para estéreo
print(f"Stereo shape: {wav.shape}")  # [1, 2, 480000]
torchaudio.save("stereo.wav", wav[0].cpu(), sample_rate=32000)
```

### Continuação de áudio

```python
from transformers import AutoProcessor, MusicgenForConditionalGeneration

processor = AutoProcessor.from_pretrained("facebook/musicgen-medium")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-medium")

# Carregar áudio para continuar
import torchaudio
audio, sr = torchaudio.load("intro.wav")

# Processar com texto e áudio
inputs = processor(
    audio=audio.squeeze().numpy(),
    sampling_rate=sr,
    text=["continue with a epic chorus"],
    padding=True,
    return_tensors="pt"
)

# Gerar continuação
audio_values = model.generate(**inputs, do_sample=True, guidance_scale=3, max_new_tokens=512)
```

## Uso de MusicGen-Style

### Geração condicionada por estilo

```python
from audiocraft.models import MusicGen

# Carregar modelo de estilo
model = MusicGen.get_pretrained('facebook/musicgen-style')

# Configurar geração com estilo
model.set_generation_params(
    duration=30,
    cfg_coef=3.0,
    cfg_coef_beta=5.0  # Influência de estilo
)

# Configurar condicionador de estilo
model.set_style_conditioner_params(
    eval_q=3,          # RVQ quantizers (1-6)
    excerpt_length=3.0  # Comprimento do trecho de estilo
)

# Carregar referência de estilo
style_audio, sr = torchaudio.load("reference_style.wav")

# Gerar com texto + estilo
descriptions = ["upbeat dance track"]
wav = model.generate_with_style(descriptions, style_audio, sr)
```

### Geração apenas de estilo (sem texto)

```python
# Gerar com estilo correspondente sem prompt de texto
model.set_generation_params(
    duration=30,
    cfg_coef=3.0,
    cfg_coef_beta=None  # Desabilitar CFG duplo para estilo apenas
)

wav = model.generate_with_style([None], style_audio, sr)
```

## Uso de AudioGen

### Geração de efeitos sonoros

```python
from audiocraft.models import AudioGen
import torchaudio

model = AudioGen.get_pretrained('facebook/audiogen-medium')
model.set_generation_params(duration=10)

# Gerar vários sons
descriptions = [
    "thunderstorm with heavy rain and lightning",
    "busy city traffic with car horns",
    "ocean waves crashing on rocks",
    "crackling campfire in forest"
]

wav = model.generate(descriptions)

for i, audio in enumerate(wav):
    torchaudio.save(f"sound_{i}.wav", audio.cpu(), sample_rate=16000)
```

## Uso de EnCodec

### Compressão de áudio

```python
from audiocraft.models import CompressionModel
import torch
import torchaudio

# Carregar EnCodec
model = CompressionModel.get_pretrained('facebook/encodec_32khz')

# Carregar áudio
wav, sr = torchaudio.load("audio.wav")

# Garantir taxa de amostragem correta
if sr != 32000:
    resampler = torchaudio.transforms.Resample(sr, 32000)
    wav = resampler(wav)

# Codificar em tokens
with torch.no_grad():
    encoded = model.encode(wav.unsqueeze(0))
    codes = encoded[0]  # Códigos de áudio

# Decodificar de volta para áudio
with torch.no_grad():
    decoded = model.decode(codes)

torchaudio.save("reconstructed.wav", decoded[0].cpu(), sample_rate=32000)
```

## Workflows comuns

### Workflow 1: Pipeline de geração de música

```python
import torch
import torchaudio
from audiocraft.models import MusicGen

class MusicGenerator:
    def __init__(self, model_name="facebook/musicgen-medium"):
        self.model = MusicGen.get_pretrained(model_name)
        self.sample_rate = 32000

    def generate(self, prompt, duration=30, temperature=1.0, cfg=3.0):
        self.model.set_generation_params(
            duration=duration,
            top_k=250,
            temperature=temperature,
            cfg_coef=cfg
        )

        with torch.no_grad():
            wav = self.model.generate([prompt])

        return wav[0].cpu()

    def generate_batch(self, prompts, duration=30):
        self.model.set_generation_params(duration=duration)

        with torch.no_grad():
            wav = self.model.generate(prompts)

        return wav.cpu()

    def save(self, audio, path):
        torchaudio.save(path, audio, sample_rate=self.sample_rate)

# Uso
generator = MusicGenerator()
audio = generator.generate(
    "epic cinematic orchestral music",
    duration=30,
    temperature=1.0
)
generator.save(audio, "epic_music.wav")
```

### Workflow 2: Processamento em lote de design sonoro

```python
import json
from pathlib import Path
from audiocraft.models import AudioGen
import torchaudio

def batch_generate_sounds(sound_specs, output_dir):
    """
    Gerar múltiplos sons a partir de especificações.

    Args:
        sound_specs: lista de {"name": str, "description": str, "duration": float}
        output_dir: caminho do diretório de saída
    """
    model = AudioGen.get_pretrained('facebook/audiogen-medium')
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    results = []

    for spec in sound_specs:
        model.set_generation_params(duration=spec.get("duration", 5))

        wav = model.generate([spec["description"]])

        output_path = output_dir / f"{spec['name']}.wav"
        torchaudio.save(str(output_path), wav[0].cpu(), sample_rate=16000)

        results.append({
            "name": spec["name"],
            "path": str(output_path),
            "description": spec["description"]
        })

    return results

# Uso
sounds = [
    {"name": "explosion", "description": "massive explosion with debris", "duration": 3},
    {"name": "footsteps", "description": "footsteps on wooden floor", "duration": 5},
    {"name": "door", "description": "wooden door creaking and closing", "duration": 2}
]

results = batch_generate_sounds(sounds, "sound_effects/")
```

### Workflow 3: Demo Gradio

```python
import gradio as gr
import torch
import torchaudio
from audiocraft.models import MusicGen

model = MusicGen.get_pretrained('facebook/musicgen-small')

def generate_music(prompt, duration, temperature, cfg_coef):
    model.set_generation_params(
        duration=duration,
        temperature=temperature,
        cfg_coef=cfg_coef
    )

    with torch.no_grad():
        wav = model.generate([prompt])

    # Salvar em arquivo temporário
    path = "temp_output.wav"
    torchaudio.save(path, wav[0].cpu(), sample_rate=32000)
    return path

demo = gr.Interface(
    fn=generate_music,
    inputs=[
        gr.Textbox(label="Music Description", placeholder="upbeat electronic dance music"),
        gr.Slider(1, 30, value=8, label="Duration (seconds)"),
        gr.Slider(0.5, 2.0, value=1.0, label="Temperature"),
        gr.Slider(1.0, 10.0, value=3.0, label="CFG Coefficient")
    ],
    outputs=gr.Audio(label="Generated Music"),
    title="MusicGen Demo"
)

demo.launch()
```

## Otimização de performance

### Otimização de memória

```python
# Usar modelo menor
model = MusicGen.get_pretrained('facebook/musicgen-small')

# Limpar cache entre gerações
torch.cuda.empty_cache()

# Gerar durações mais curtas
model.set_generation_params(duration=10)  # Em vez de 30

# Usar precisão half
model = model.half()
```

### Eficiência de processamento em lote

```python
# Processar múltiplos prompts de uma vez (mais eficiente)
descriptions = ["prompt1", "prompt2", "prompt3", "prompt4"]
wav = model.generate(descriptions)  # Lote único

# Em vez de
for desc in descriptions:
    wav = model.generate([desc])  # Múltiplos lotes (mais lento)
```

### Requisitos de memória GPU

| Modelo | FP32 VRAM | FP16 VRAM |
|--------|-----------|-----------|
| musicgen-small | ~4GB | ~2GB |
| musicgen-medium | ~8GB | ~4GB |
| musicgen-large | ~16GB | ~8GB |

## Problemas comuns

| Problema | Solução |
|----------|---------|
| CUDA OOM | Use modelo menor, reduza duração |
| Qualidade ruim | Aumente cfg_coef, melhore prompts |
| Geração muito curta | Verifique configuração de duração máxima |
| Artefatos de áudio | Tente diferentes temperaturas |
| Estéreo não funciona | Use variante de modelo estéreo |

## Referências

- **[Uso Avançado](references/advanced-usage.md)** - Treinamento, fine-tuning, deployment
- **[Solução de Problemas](references/troubleshooting.md)** - Problemas comuns e soluções

## Recursos

- **GitHub**: https://github.com/facebookresearch/audiocraft
- **Paper (MusicGen)**: https://arxiv.org/abs/2306.05284
- **Paper (AudioGen)**: https://arxiv.org/abs/2209.15352
- **HuggingFace**: https://huggingface.co/facebook/musicgen-small
- **Demo**: https://huggingface.co/spaces/facebook/MusicGen