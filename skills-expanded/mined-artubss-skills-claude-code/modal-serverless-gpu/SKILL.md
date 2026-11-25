---
name: modal-serverless-gpu
description: Plataforma GPU serverless em nuvem para executar workloads de ML. Use quando você precisar de acesso GPU sob demanda sem gerenciamento de infraestrutura, fazendo deploy de modelos de ML como APIs, ou executando jobs em batch com auto-scaling.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Infrastructure, Serverless, GPU, Cloud, Deployment, Modal]
dependencies: [modal>=0.64.0]
---

# Modal Serverless GPU

Guia completo para executar workloads de ML na plataforma GPU serverless em nuvem do Modal.

## Quando usar Modal

**Use Modal quando:**
- Executar workloads de ML intensivos em GPU sem gerenciar infraestrutura
- Fazer deploy de modelos de ML como APIs com auto-scaling
- Executar jobs de processamento em batch (treinamento, inferência, processamento de dados)
- Precisar de preços GPU pay-per-second sem custos de ociosidade
- Prototipando aplicações de ML rapidamente
- Executar jobs agendados (workloads tipo cron)

**Funcionalidades-chave:**
- **GPUs Serverless**: T4, L4, A10G, L40S, A100, H100, H200, B200 sob demanda
- **Nativo em Python**: Define infraestrutura em código Python, sem YAML
- **Auto-scaling**: Escale a zero, escale para 100+ GPUs instantaneamente
- **Cold starts sub-segundo**: Infraestrutura baseada em Rust para lançamentos rápidos de containers
- **Cache de containers**: Camadas de imagem em cache para iteração rápida
- **Web endpoints**: Faça deploy de funções como APIs REST com atualizações sem downtime

**Use alternativas em vez disso:**
- **RunPod**: Para pods de execução mais longa com estado persistente
- **Lambda Labs**: Para instâncias GPU reservadas
- **SkyPilot**: Para orquestração multi-cloud e otimização de custos
- **Kubernetes**: Para arquiteturas complexas multi-serviço

## Quick start

### Instalação

```bash
pip install modal
modal setup  # Abre navegador para autenticação
```

### Hello World com GPU

```python
import modal

app = modal.App("hello-gpu")

@app.function(gpu="T4")
def gpu_info():
    import subprocess
    return subprocess.run(["nvidia-smi"], capture_output=True, text=True).stdout

@app.local_entrypoint()
def main():
    print(gpu_info.remote())
```

Execute: `modal run hello_gpu.py`

### Endpoint básico de inferência

```python
import modal

app = modal.App("text-generation")
image = modal.Image.debian_slim().pip_install("transformers", "torch", "accelerate")

@app.cls(gpu="A10G", image=image)
class TextGenerator:
    @modal.enter()
    def load_model(self):
        from transformers import pipeline
        self.pipe = pipeline("text-generation", model="gpt2", device=0)

    @modal.method()
    def generate(self, prompt: str) -> str:
        return self.pipe(prompt, max_length=100)[0]["generated_text"]

@app.local_entrypoint()
def main():
    print(TextGenerator().generate.remote("Hello, world"))
```

## Conceitos principais

### Componentes-chave

| Componente | Propósito |
|-----------|---------|
| `App` | Container para funções e recursos |
| `Function` | Função serverless com especificações de compute |
| `Cls` | Funções baseadas em classe com lifecycle hooks |
| `Image` | Definição de imagem de container |
| `Volume` | Armazenamento persistente para modelos/dados |
| `Secret` | Armazenamento seguro de credenciais |

### Modos de execução

| Comando | Descrição |
|---------|-------------|
| `modal run script.py` | Executa e sai |
| `modal serve script.py` | Desenvolvimento com live reload |
| `modal deploy script.py` | Deploy persistente em nuvem |

## Configuração de GPU

### GPUs disponíveis

| GPU | VRAM | Melhor para |
|-----|------|----------|
| `T4` | 16GB | Inferência com orçamento limitado, modelos pequenos |
| `L4` | 24GB | Inferência, arquitetura Ada Lovelace |
| `A10G` | 24GB | Treinamento/inferência, 3.3x mais rápido que T4 |
| `L40S` | 48GB | Recomendado para inferência (melhor custo/performance) |
| `A100-40GB` | 40GB | Treinamento de modelos grandes |
| `A100-80GB` | 80GB | Modelos muito grandes |
| `H100` | 80GB | Mais rápido, FP8 + Transformer Engine |
| `H200` | 141GB | Auto-upgrade do H100, 4.8TB/s de largura de banda |
| `B200` | Latest | Arquitetura Blackwell |

### Padrões de especificação de GPU

```python
# GPU única
@app.function(gpu="A100")

# Variante de memória específica
@app.function(gpu="A100-80GB")

# Múltiplas GPUs (até 8)
@app.function(gpu="H100:4")

# GPU com fallbacks
@app.function(gpu=["H100", "A100", "L40S"])

# Qualquer GPU disponível
@app.function(gpu="any")
```

## Imagens de container

```python
# Imagem básica com pip
image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "torch==2.1.0", "transformers==4.36.0", "accelerate"
)

# Baseado em CUDA
image = modal.Image.from_registry(
    "nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04",
    add_python="3.11"
).pip_install("torch", "transformers")

# Com pacotes de sistema
image = modal.Image.debian_slim().apt_install("git", "ffmpeg").pip_install("whisper")
```

## Armazenamento persistente

```python
volume = modal.Volume.from_name("model-cache", create_if_missing=True)

@app.function(gpu="A10G", volumes={"/models": volume})
def load_model():
    import os
    model_path = "/models/llama-7b"
    if not os.path.exists(model_path):
        model = download_model()
        model.save_pretrained(model_path)
        volume.commit()  # Persistir mudanças
    return load_from_path(model_path)
```

## Web endpoints

### Decorator FastAPI endpoint

```python
@app.function()
@modal.fastapi_endpoint(method="POST")
def predict(text: str) -> dict:
    return {"result": model.predict(text)}
```

### App ASGI completo

```python
from fastapi import FastAPI
web_app = FastAPI()

@web_app.post("/predict")
async def predict(text: str):
    return {"result": await model.predict.remote.aio(text)}

@app.function()
@modal.asgi_app()
def fastapi_app():
    return web_app
```

### Tipos de web endpoint

| Decorator | Caso de uso |
|-----------|----------|
| `@modal.fastapi_endpoint()` | Função simples → API |
| `@modal.asgi_app()` | Apps FastAPI/Starlette completos |
| `@modal.wsgi_app()` | Apps Django/Flask |
| `@modal.web_server(port)` | Servidores HTTP arbitrários |

## Dynamic batching

```python
@app.function()
@modal.batched(max_batch_size=32, wait_ms=100)
async def batch_predict(inputs: list[str]) -> list[dict]:
    # Inputs automaticamente agrupados em batch
    return model.batch_predict(inputs)
```

## Gerenciamento de segredos

```bash
# Criar segredo
modal secret create huggingface HF_TOKEN=hf_xxx
```

```python
@app.function(secrets=[modal.Secret.from_name("huggingface")])
def download_model():
    import os
    token = os.environ["HF_TOKEN"]
```

## Agendamento

```python
@app.function(schedule=modal.Cron("0 0 * * *"))  # Diariamente à meia-noite
def daily_job():
    pass

@app.function(schedule=modal.Period(hours=1))
def hourly_job():
    pass
```

## Otimização de performance

### Mitigação de cold start

```python
@app.function(
    container_idle_timeout=300,  # Mantém aquecido por 5 min
    allow_concurrent_inputs=10,  # Processa requests concorrentes
)
def inference():
    pass
```

### Melhores práticas para carregamento de modelos

```python
@app.cls(gpu="A100")
class Model:
    @modal.enter()  # Executado uma vez no início do container
    def load(self):
        self.model = load_model()  # Carrega durante warm-up

    @modal.method()
    def predict(self, x):
        return self.model(x)
```

## Processamento paralelo

```python
@app.function()
def process_item(item):
    return expensive_computation(item)

@app.function()
def run_parallel():
    items = list(range(1000))
    # Distribui para containers paralelos
    results = list(process_item.map(items))
    return results
```

## Configuração comum

```python
@app.function(
    gpu="A100",
    memory=32768,              # 32GB RAM
    cpu=4,                     # 4 cores de CPU
    timeout=3600,              # 1 hora máximo
    container_idle_timeout=120,# Mantém aquecido 2 min
    retries=3,                 # Retry em caso de falha
    concurrency_limit=10,      # Máximo de containers concorrentes
)
def my_function():
    pass
```

## Debug

```python
# Teste localmente
if __name__ == "__main__":
    result = my_function.local()

# Ver logs
# modal app logs my-app
```

## Problemas comuns

| Problema | Solução |
|-------|----------|
| Latência de cold start | Aumente `container_idle_timeout`, use `@modal.enter()` |
| GPU OOM | Use GPU maior (`A100-80GB`), ative gradient checkpointing |
| Falha no build de imagem | Fixe versões de dependências, verifique compatibilidade CUDA |
| Erros de timeout | Aumente `timeout`, adicione checkpointing |

## Referências

- **[Uso Avançado](references/advanced-usage.md)** - Multi-GPU, treinamento distribuído, otimização de custos
- **[Troubleshooting](references/troubleshooting.md)** - Problemas comuns e soluções

## Recursos

- **Documentação**: https://modal.com/docs
- **Exemplos**: https://github.com/modal-labs/modal-examples
- **Preços**: https://modal.com/pricing
- **Discord**: https://discord.gg/modal