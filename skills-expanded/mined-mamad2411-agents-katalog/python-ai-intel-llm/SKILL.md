---
name: python-ai-intel-llm
description: "LLMs en hardware Intel: OpenVINO GenAI, llama.cpp con backend Intel, vLLM, optimum-intel, cuantización AWQ/GPTQ/SmoothQuant, y serving de transformers. Actívala para correr, cuantizar o servir LLMs en GPUs Intel Arc, Core Ultra, o Xeon."
disable-model-invocation: true
---

# LLMs on Intel Hardware

Large Language Models en hardware Intel: llama.cpp, OpenVINO GenAI, vLLM, y optimum-intel. Quantization es obligatoria — sin INT4, un LLM de 7B no cabe en una Arc A770.

---

## Stack de LLM en Intel

| Herramienta | Hardware | Caso de uso |
|------------|----------|-------------|
| **OpenVINO GenAI** | CPU, GPU, NPU | API unificada con sampling, streaming |
| **llama.cpp + OpenVINO** | CPU, GPU | Compatibilidad GGUF + inference Intel |
| **optimum-intel** | CPU, GPU | HuggingFace transformers → OpenVINO |
| **vLLM** | GPU Arc | Serving alta concurrencia |
| **ollama + OpenVINO** | CPU, GPU | Experiencia local estilo Ollama |

```bash
uv add openvino-genai optimum-intel transformers
# llama.cpp: compilar con soporte OpenVINO
```

---

## OpenVINO GenAI API (recomendado 2026)

```python
import openvino_genai as ov_genai

# ─── Cargar modelo (ya convertido a IR) ───
pipe = ov_genai.LLMPipeline("llama-3-8b-int4/", device="GPU")

# ─── Generación simple ───
output = pipe.generate(
    "Explain Intel Arc GPU architecture in one paragraph.",
    max_new_tokens=256,
    temperature=0.7,
    do_sample=True,
)
print(output)

# ─── Streaming ───
streamer = ov_genai.StreamerBase()
for token in pipe.generate("Tell me a joke about GPUs.",
                           max_new_tokens=100,
                           streamer=streamer):
    print(token, end="", flush=True)

# ─── Batch generation ───
prompts = [
    "What is OpenVINO?",
    "Explain oneAPI.",
    "Define SYCL.",
]
results = pipe.generate(prompts, max_new_tokens=128)
for r in results:
    print(r)

# ─── Config avanzada ───
config = pipe.get_generation_config()
config.max_new_tokens = 512
config.temperature = 0.7
config.top_p = 0.95
config.top_k = 50
config.repetition_penalty = 1.1
config.do_sample = True
pipe.set_generation_config(config)
```

---

## optimum-intel — HuggingFace → OpenVINO

```python
from optimum.intel import OVModelForCausalLM
from transformers import AutoTokenizer

model_id = "meta-llama/Llama-3.2-3B-Instruct"

# ─── Cargar y convertir a OpenVINO automáticamente ───
model = OVModelForCausalLM.from_pretrained(
    model_id,
    export=True,              # Convierte a IR al cargar
    device="GPU",
    ov_config={
        "PERFORMANCE_HINT": "LATENCY",
        "NUM_STREAMS": 1,
    },
)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# ─── Inference ───
inputs = tokenizer("What is Intel Arc?", return_tensors="pt")
outputs = model.generate(
    **inputs,
    max_new_tokens=128,
    do_sample=True,
    temperature=0.6,
)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))

# ─── Guardar modelo IR para reuso ───
model.save_pretrained("llama-3.2-3b-ov/")
```

---

## Quantization de LLMs

### INT8 con NNCF

```python
import nncf
from optimum.intel import OVModelForCausalLM
import openvino as ov

# Cargar modelo FP32
model = OVModelForCausalLM.from_pretrained("llama-3.2-3b", export=True)

# ─── Weight compression INT8 ───
compressed = nncf.compress_weights(
    model.model,
    mode=nncf.CompressWeightsMode.INT8,
    ratio=1.0,
)
ov.save_model(compressed, "llama-3b-int8.xml")
```

### INT4 con group size

```python
# ─── INT4 con group_size=128 ───
compressed = nncf.compress_weights(
    model.model,
    mode=nncf.CompressWeightsMode.INT4_SYM,
    ratio=1.0,
    group_size=128,
    # Ignorar capa de logits (mejora precisión)
    ignored_scope=nncf.IgnoredScope(names=["lm_head"]),
)
ov.save_model(compressed, "llama-3b-int4.xml")

# ─── INT4 asimétrico con AWQ ───
compressed = nncf.compress_weights(
    model.model,
    mode=nncf.CompressWeightsMode.INT4_ASYM,
    ratio=1.0,
    group_size=128,
    awq=True,                  # Activation-aware
    dataset=calibration_data,  # Dataset pequeño (~128 samples)
)
```

### SmoothQuant (INT8 activaciones + pesos)

```python
import nncf

# SmoothQuant: escala activaciones para hacerlas cuantizables
quantized = nncf.quantize(
    model.model,
    calibration_data,
    preset=nncf.QuantizationPreset.MIXED,
    model_type=nncf.ModelType.TRANSFORMER,
    smooth_quant_alpha=0.8,   # 0.0 = solo pesos, 1.0 = solo activaciones
)
```

### Tabla de tamaños estimados (LLaMA 3 8B)

| Formato | Tamaño | VRAM necesaria |
|---------|--------|:-------------:|
| FP32 | ~32 GB | 40+ GB |
| FP16 | ~16 GB | 22+ GB |
| INT8 | ~8 GB | 12 GB |
| INT4 (g128) | ~4.5 GB | 7 GB |
| INT4 (g32) | ~4 GB | 6 GB |

---

## llama.cpp con backend OpenVINO

```bash
# Compilar llama.cpp con soporte OpenVINO
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build -DGGML_OPENVINO=ON
cmake --build build --config Release
```

```bash
# Convertir GGUF a IR y correr con OpenVINO
# Convertir (GGUF → IR)
python convert_hf_to_gguf.py llama3-8b/

# Inference con llama.cpp + OpenVINO
./build/bin/llama-cli \
  -m llama3-8b-Q4_K_M.gguf \
  -p "Explain Intel oneAPI." \
  -ngl 33 \
  -ov-device GPU \
  -n 256

# Con GPU y métricas
./build/bin/llama-bench \
  -m llama3-8b-Q4_K_M.gguf \
  -ov-device GPU \
  -n 128
```

---

## vLLM en Intel GPUs

```bash
# vLLM con backend Intel XPU
uv add vllm

# Lanzar servidor
VLLM_ATTENTION_BACKEND=TORCH_SDPA python -m vllm.entrypoints.openai.api_server \
  --model llama-3.2-3b-instruct \
  --device xpu \
  --dtype bfloat16 \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.90
```

```python
# Cliente vLLM desde Python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed",
)

response = client.chat.completions.create(
    model="llama-3.2-3b-instruct",
    messages=[{"role": "user", "content": "What is OpenVINO?"}],
    max_tokens=256,
    temperature=0.7,
)
print(response.choices[0].message.content)
```

---

## KV-cache y optimizaciones de memoria

```python
import openvino_genai as ov_genai

# ─── KV-cache comprimido ───
pipe = ov_genai.LLMPipeline("llama-3-8b-int4/", device="GPU")

config = pipe.get_generation_config()
config.cache_enc_dec = True         # Cache encoder/decoder
config.enable_prefix_caching = True  # Reusa cache para prompts con prefijo común

# ─── Continuous batching ───
scheduler_config = ov_genai.SchedulerConfig(
    max_num_batched_tokens=8192,
    max_num_seqs=32,
    num_kv_blocks=512,
    block_size=16,
)
pipe.set_scheduler_config(scheduler_config)

# ─── Prompt lookup decoding (speculative) ───
config.assistant_model = "llama-3-8b-int4-draft/"  # Modelo pequeño para spec decode
```

---

## Token streaming con buffer

```python
import openvino_genai as ov_genai

pipe = ov_genai.LLMPipeline("llama-3-8b-int4/", device="GPU")

class BufferedStreamer(ov_genai.StreamerBase):
    def __init__(self, tokenizer):
        super().__init__()
        self.tokenizer = tokenizer
        self.buffer = []

    def write(self, token_ids):
        for tid in token_ids:
            self.buffer.append(tid)
        text = self.tokenizer.decode(self.buffer, skip_special_tokens=True)
        print(text, end="\r", flush=True)
        return True

    def end(self):
        text = self.tokenizer.decode(self.buffer, skip_special_tokens=True)
        print(text)
```

---

## Checklist LLM en Intel

- [ ] Modelo cuantizado a INT4 (o INT8 si la GPU tiene suficiente VRAM)
- [ ] `nncf.compress_weights` con `group_size=128` para balance velocidad/precisión
- [ ] `awq=True` si hay dataset de calibración para mejor precisión
- [ ] OpenVINO GenAI API para casos simples, vLLM para serving multi-usuario
- [ ] KV-cache configurado (`block_size`, `max_num_seqs`)
- [ ] `PERFORMANCE_HINT` en `LATENCY` para chat interactivo, `THROUGHPUT` para batch
- [ ] Streaming habilitado para UX interactiva
- [ ] Context window ajustada a la VRAM disponible
- [ ] Speculative decoding (draft model) si hay VRAM sobrante
- [ ] Sin `.safetensors` / `.pth` en producción — siempre IR cuantizado
