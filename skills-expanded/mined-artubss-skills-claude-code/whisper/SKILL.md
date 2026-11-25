---
name: whisper
description: Modelo de reconhecimento de fala de propósito geral da OpenAI. Suporta 99 idiomas, transcrição, tradução para inglês e identificação de idioma. Seis tamanhos de modelo, de tiny (39M parâmetros) a large (1550M parâmetros). Use para speech-to-text, transcrição de podcasts ou processamento de áudio multilíngue. Melhor para ASR robusto e multilíngue.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Whisper, Speech Recognition, ASR, Multimodal, Multilingual, OpenAI, Speech-To-Text, Transcription, Translation, Audio Processing]
dependencies: [openai-whisper, transformers, torch]
---

# Whisper - Reconhecimento de Fala Robusto

Modelo de reconhecimento de fala multilíngue da OpenAI.

## Quando usar Whisper

**Use quando:**
- Transcrição speech-to-text (99 idiomas)
- Transcrição de podcasts/vídeos
- Automação de anotações de reuniões
- Tradução para inglês
- Transcrição de áudio com ruído
- Processamento de áudio multilíngue

**Métricas**:
- **72.900+ estrelas no GitHub**
- 99 idiomas suportados
- Treinado em 680 mil horas de áudio
- Licença MIT

**Use alternativas em vez disso**:
- **AssemblyAI**: API gerenciada, diarização de falante
- **Deepgram**: ASR com streaming em tempo real
- **Google Speech-to-Text**: Baseado em nuvem

## Início rápido

### Instalação

```bash
# Requer Python 3.8-3.11
pip install -U openai-whisper

# Requer ffmpeg
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: choco install ffmpeg
```

### Transcrição básica

```python
import whisper

# Carregar modelo
model = whisper.load_model("base")

# Transcrever
result = model.transcribe("audio.mp3")

# Exibir texto
print(result["text"])

# Acessar segmentos
for segment in result["segments"]:
    print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")
```

## Tamanhos de modelo

```python
# Modelos disponíveis
models = ["tiny", "base", "small", "medium", "large", "turbo"]

# Carregar modelo específico
model = whisper.load_model("turbo")  # Mais rápido, boa qualidade
```

| Modelo | Parâmetros | Apenas inglês | Multilíngue | Velocidade | VRAM |
|--------|-----------|---------------|-------------|-----------|------|
| tiny | 39M | ✓ | ✓ | ~32x | ~1 GB |
| base | 74M | ✓ | ✓ | ~16x | ~1 GB |
| small | 244M | ✓ | ✓ | ~6x | ~2 GB |
| medium | 769M | ✓ | ✓ | ~2x | ~5 GB |
| large | 1550M | ✗ | ✓ | 1x | ~10 GB |
| turbo | 809M | ✗ | ✓ | ~8x | ~6 GB |

**Recomendação**: Use `turbo` para melhor velocidade/qualidade, `base` para prototipagem

## Opções de transcrição

### Especificação de idioma

```python
# Detectar idioma automaticamente
result = model.transcribe("audio.mp3")

# Especificar idioma (mais rápido)
result = model.transcribe("audio.mp3", language="en")

# Suportados: en, es, fr, de, it, pt, ru, ja, ko, zh, e mais 89
```

### Seleção de tarefa

```python
# Transcrição (padrão)
result = model.transcribe("audio.mp3", task="transcribe")

# Tradução para inglês
result = model.transcribe("spanish.mp3", task="translate")
# Entrada: áudio em espanhol → Saída: texto em inglês
```

### Prompt inicial

```python
# Melhorar precisão com contexto
result = model.transcribe(
    "audio.mp3",
    initial_prompt="This is a technical podcast about machine learning and AI."
)

# Ajuda com:
# - Termos técnicos
# - Nomes próprios
# - Vocabulário específico de domínio
```

### Timestamps

```python
# Timestamps em nível de palavra
result = model.transcribe("audio.mp3", word_timestamps=True)

for segment in result["segments"]:
    for word in segment["words"]:
        print(f"{word['word']} ({word['start']:.2f}s - {word['end']:.2f}s)")
```

### Fallback de temperatura

```python
# Tentar novamente com diferentes temperaturas se confiança baixa
result = model.transcribe(
    "audio.mp3",
    temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
)
```

## Uso via linha de comando

```bash
# Transcrição básica
whisper audio.mp3

# Especificar modelo
whisper audio.mp3 --model turbo

# Formatos de saída
whisper audio.mp3 --output_format txt     # Texto simples
whisper audio.mp3 --output_format srt     # Legendas
whisper audio.mp3 --output_format vtt     # WebVTT
whisper audio.mp3 --output_format json    # JSON com timestamps

# Idioma
whisper audio.mp3 --language Spanish

# Tradução
whisper spanish.mp3 --task translate
```

## Processamento em lote

```python
import os

audio_files = ["file1.mp3", "file2.mp3", "file3.mp3"]

for audio_file in audio_files:
    print(f"Transcrevendo {audio_file}...")
    result = model.transcribe(audio_file)

    # Salvar em arquivo
    output_file = audio_file.replace(".mp3", ".txt")
    with open(output_file, "w") as f:
        f.write(result["text"])
```

## Transcrição em tempo real

```python
# Para áudio em streaming, use faster-whisper
# pip install faster-whisper

from faster_whisper import WhisperModel

model = WhisperModel("base", device="cuda", compute_type="float16")

# Transcrever com streaming
segments, info = model.transcribe("audio.mp3", beam_size=5)

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

## Aceleração por GPU

```python
import whisper

# Usa GPU automaticamente se disponível
model = whisper.load_model("turbo")

# Forçar CPU
model = whisper.load_model("turbo", device="cpu")

# Forçar GPU
model = whisper.load_model("turbo", device="cuda")

# 10-20× mais rápido em GPU
```

## Integração com outras ferramentas

### Geração de legendas

```bash
# Gerar legendas SRT
whisper video.mp4 --output_format srt --language English

# Saída: video.srt
```

### Com LangChain

```python
from langchain.document_loaders import WhisperTranscriptionLoader

loader = WhisperTranscriptionLoader(file_path="audio.mp3")
docs = loader.load()

# Usar transcrição em RAG
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())
```

### Extrair áudio de vídeo

```bash
# Use ffmpeg para extrair áudio
ffmpeg -i video.mp4 -vn -acodec pcm_s16le audio.wav

# Depois transcrever
whisper audio.wav
```

## Melhores práticas

1. **Use modelo turbo** - Melhor velocidade/qualidade para inglês
2. **Especifique idioma** - Mais rápido que detecção automática
3. **Adicione prompt inicial** - Melhora termos técnicos
4. **Use GPU** - 10-20× mais rápido
5. **Processe em lote** - Mais eficiente
6. **Converta para WAV** - Melhor compatibilidade
7. **Divida áudio longo** - Chunks de <30 min
8. **Verifique suporte de idioma** - Qualidade varia por idioma
9. **Use faster-whisper** - 4× mais rápido que openai-whisper
10. **Monitore VRAM** - Dimensione modelo conforme hardware

## Desempenho

| Modelo | Fator de tempo real (CPU) | Fator de tempo real (GPU) |
|--------|--------------------------|--------------------------|
| tiny | ~0,32 | ~0,01 |
| base | ~0,16 | ~0,01 |
| turbo | ~0,08 | ~0,01 |
| large | ~1,0 | ~0,05 |

*Fator de tempo real: 0,1 = 10× mais rápido que tempo real*

## Suporte de idiomas

Idiomas mais suportados:
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)

Lista completa: 99 idiomas no total

## Limitações

1. **Alucinações** - Pode repetir ou inventar texto
2. **Precisão em forma longa** - Degrada em áudio >30 min
3. **Identificação de falante** - Sem diarização
4. **Sotaques** - Qualidade varia
5. **Ruído de fundo** - Pode afetar precisão
6. **Latência em tempo real** - Não apropriado para legendagem ao vivo

## Recursos

- **GitHub**: https://github.com/openai/whisper ⭐ 72.900+
- **Paper**: https://arxiv.org/abs/2212.04356
- **Model Card**: https://github.com/openai/whisper/blob/main/model-card.md
- **Colab**: Disponível no repositório
- **Licença**: MIT