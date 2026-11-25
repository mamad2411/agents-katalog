---
name: peft-fine-tuning
description: Ajuste fino com eficiência de parâmetros para LLMs usando LoRA, QLoRA e 25+ métodos. Use ao fazer fine-tuning de modelos grandes (7B-70B) com memória GPU limitada, quando precisa treinar <1% dos parâmetros com perda mínima de precisão, ou para serviços multi-adapter. Biblioteca oficial do HuggingFace integrada ao ecossistema transformers.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Fine-Tuning, PEFT, LoRA, QLoRA, Parameter-Efficient, Adapters, Low-Rank, Memory Optimization, Multi-Adapter]
dependencies: [peft>=0.13.0, transformers>=4.45.0, torch>=2.0.0, bitsandbytes>=0.43.0]
---

# PEFT (Parameter-Efficient Fine-Tuning)

Ajuste fino de LLMs treinando <1% dos parâmetros usando LoRA, QLoRA e 25+ métodos de adapter.

## Quando usar PEFT

**Use PEFT/LoRA quando:**
- Fazer fine-tuning de modelos 7B-70B em GPUs consumer (RTX 4090, A100)
- Precisa treinar <1% dos parâmetros (6MB de adapters vs 14GB do modelo completo)
- Quer iteração rápida com múltiplos adapters específicos por tarefa
- Implantando múltiplas variantes com fine-tuning a partir de um modelo base

**Use QLoRA (PEFT + quantização) quando:**
- Fazendo fine-tuning de modelos 70B em GPU única de 24GB
- Memória é a restrição principal
- Pode aceitar ~5% de trade-off de qualidade vs fine-tuning completo

**Use fine-tuning completo quando:**
- Treinando modelos pequenos (<1B de parâmetros)
- Precisa de qualidade máxima e tem orçamento de computação
- Desvio significativo de domínio requer atualizar todos os pesos

## Guia rápido

### Instalação

```bash
# Instalação básica
pip install peft

# Com suporte a quantização (recomendado)
pip install peft bitsandbytes

# Stack completo
pip install peft transformers accelerate bitsandbytes datasets
```

### Fine-tuning LoRA (padrão)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import get_peft_model, LoraConfig, TaskType
from datasets import load_dataset

# Carregar modelo base
model_name = "meta-llama/Llama-3.1-8B"
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

# Configuração LoRA
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                          # Rank (8-64, maior = mais capacidade)
    lora_alpha=32,                 # Fator de escala (tipicamente 2*r)
    lora_dropout=0.05,             # Dropout para regularização
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],  # Camadas de atenção
    bias="none"                    # Não treina vieses
)

# Aplicar LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Output: trainable params: 13,631,488 || all params: 8,043,307,008 || trainable%: 0.17%

# Preparar dataset
dataset = load_dataset("databricks/databricks-dolly-15k", split="train")

def tokenize(example):
    text = f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['response']}"
    return tokenizer(text, truncation=True, max_length=512, padding="max_length")

tokenized = dataset.map(tokenize, remove_columns=dataset.column_names)

# Treinamento
training_args = TrainingArguments(
    output_dir="./lora-llama",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized,
    data_collator=lambda data: {"input_ids": torch.stack([f["input_ids"] for f in data]),
                                 "attention_mask": torch.stack([f["attention_mask"] for f in data]),
                                 "labels": torch.stack([f["input_ids"] for f in data])}
)

trainer.train()

# Salvar apenas adapter (6MB vs 16GB)
model.save_pretrained("./lora-llama-adapter")
```

### Fine-tuning QLoRA (com eficiência de memória)

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import get_peft_model, LoraConfig, prepare_model_for_kbit_training

# Configuração de quantização 4-bit
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",           # NormalFloat4 (melhor para LLMs)
    bnb_4bit_compute_dtype="bfloat16",   # Computar em bf16
    bnb_4bit_use_double_quant=True       # Quantização aninhada
)

# Carregar modelo quantizado
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-70B",
    quantization_config=bnb_config,
    device_map="auto"
)

# Preparar para treinamento (habilita gradient checkpointing)
model = prepare_model_for_kbit_training(model)

# Configuração LoRA para QLoRA
lora_config = LoraConfig(
    r=64,                              # Rank maior para 70B
    lora_alpha=128,
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
# Modelo 70B agora cabe em GPU única de 24GB!
```

## Seleção de parâmetros LoRA

### Rank (r) - capacidade vs eficiência

| Rank | Parâmetros Treináveis | Memória | Qualidade | Caso de Uso |
|------|----------------------|---------|-----------|------------|
| 4 | ~3M | Mínima | Menor | Tarefas simples, prototipagem |
| **8** | ~7M | Baixa | Boa | **Ponto de partida recomendado** |
| **16** | ~14M | Média | Melhor | **Fine-tuning geral** |
| 32 | ~27M | Maior | Alta | Tarefas complexas |
| 64 | ~54M | Alta | Máxima | Adaptação de domínio, modelos 70B |

### Alpha (lora_alpha) - fator de escala

```python
# Regra prática: alpha = 2 * rank
LoraConfig(r=16, lora_alpha=32)  # Padrão
LoraConfig(r=16, lora_alpha=16)  # Conservador (taxa de aprendizado menor)
LoraConfig(r=16, lora_alpha=64)  # Agressivo (taxa de aprendizado maior)
```

### Módulos alvo por arquitetura

```python
# Llama / Mistral / Qwen
target_modules = ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]

# GPT-2 / GPT-Neo
target_modules = ["c_attn", "c_proj", "c_fc"]

# Falcon
target_modules = ["query_key_value", "dense", "dense_h_to_4h", "dense_4h_to_h"]

# BLOOM
target_modules = ["query_key_value", "dense", "dense_h_to_4h", "dense_4h_to_h"]

# Detecção automática de todas as camadas lineares
target_modules = "all-linear"  # PEFT 0.6.0+
```

## Carregando e mesclando adapters

### Carregar adapter treinado

```python
from peft import PeftModel, AutoPeftModelForCausalLM
from transformers import AutoModelForCausalLM

# Opção 1: Carregar com PeftModel
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")
model = PeftModel.from_pretrained(base_model, "./lora-llama-adapter")

# Opção 2: Carregar diretamente (recomendado)
model = AutoPeftModelForCausalLM.from_pretrained(
    "./lora-llama-adapter",
    device_map="auto"
)
```

### Mesclar adapter no modelo base

```python
# Mesclar para implantação (sem overhead de adapter)
merged_model = model.merge_and_unload()

# Salvar modelo mesclado
merged_model.save_pretrained("./llama-merged")
tokenizer.save_pretrained("./llama-merged")

# Fazer push para Hub
merged_model.push_to_hub("username/llama-finetuned")
```

### Serviço multi-adapter

```python
from peft import PeftModel

# Carregar base com primeiro adapter
model = AutoPeftModelForCausalLM.from_pretrained("./adapter-task1")

# Carregar adapters adicionais
model.load_adapter("./adapter-task2", adapter_name="task2")
model.load_adapter("./adapter-task3", adapter_name="task3")

# Alternar entre adapters em tempo de execução
model.set_adapter("task1")  # Usar adapter task1
output1 = model.generate(**inputs)

model.set_adapter("task2")  # Alternar para task2
output2 = model.generate(**inputs)

# Desabilitar adapters (usar modelo base)
with model.disable_adapter():
    base_output = model.generate(**inputs)
```

## Comparação de métodos PEFT

| Método | Treináveis % | Memória | Velocidade | Melhor Para |
|--------|------------|---------|-----------|------------|
| **LoRA** | 0.1-1% | Baixa | Rápido | Fine-tuning geral |
| **QLoRA** | 0.1-1% | Muito Baixa | Médio | Memória limitada |
| AdaLoRA | 0.1-1% | Baixa | Médio | Seleção automática de rank |
| IA3 | 0.01% | Mínima | Mais rápido | Adaptação few-shot |
| Prefix Tuning | 0.1% | Baixa | Médio | Controle de geração |
| Prompt Tuning | 0.001% | Mínima | Rápido | Adaptação simples de tarefa |
| P-Tuning v2 | 0.1% | Baixa | Médio | Tarefas NLU |

### IA3 (parâmetros mínimos)

```python
from peft import IA3Config

ia3_config = IA3Config(
    target_modules=["q_proj", "v_proj", "k_proj", "down_proj"],
    feedforward_modules=["down_proj"]
)
model = get_peft_model(model, ia3_config)
# Treina apenas 0.01% dos parâmetros!
```

### Prefix Tuning

```python
from peft import PrefixTuningConfig

prefix_config = PrefixTuningConfig(
    task_type="CAUSAL_LM",
    num_virtual_tokens=20,      # Tokens prependidos
    prefix_projection=True       # Usar projeção MLP
)
model = get_peft_model(model, prefix_config)
```

## Padrões de integração

### Com TRL (SFTTrainer)

```python
from trl import SFTTrainer, SFTConfig
from peft import LoraConfig

lora_config = LoraConfig(r=16, lora_alpha=32, target_modules="all-linear")

trainer = SFTTrainer(
    model=model,
    args=SFTConfig(output_dir="./output", max_seq_length=512),
    train_dataset=dataset,
    peft_config=lora_config,  # Passar configuração LoRA diretamente
)
trainer.train()
```

### Com Axolotl (config YAML)

```yaml
# axolotl config.yaml
adapter: lora
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - v_proj
  - k_proj
  - o_proj
lora_target_linear: true  # Almejar todas as camadas lineares
```

### Com vLLM (inference)

```python
from vllm import LLM
from vllm.lora.request import LoRARequest

# Carregar modelo base com suporte LoRA
llm = LLM(model="meta-llama/Llama-3.1-8B", enable_lora=True)

# Servir com adapter
outputs = llm.generate(
    prompts,
    lora_request=LoRARequest("adapter1", 1, "./lora-adapter")
)
```

## Benchmarks de desempenho

### Uso de memória (Llama 3.1 8B)

| Método | Memória GPU | Parâmetros Treináveis |
|--------|------------|----------------------|
| Fine-tuning completo | 60+ GB | 8B (100%) |
| LoRA r=16 | 18 GB | 14M (0.17%) |
| QLoRA r=16 | 6 GB | 14M (0.17%) |
| IA3 | 16 GB | 800K (0.01%) |

### Velocidade de treinamento (A100 80GB)

| Método | Tokens/seg | vs Fine-tuning Completo |
|--------|-----------|------------------------|
| Fine-tuning Completo | 2.500 | 1x |
| LoRA | 3.200 | 1.3x |
| QLoRA | 2.100 | 0.84x |

### Qualidade (benchmark MMLU)

| Modelo | Fine-tuning Completo | LoRA | QLoRA |
|--------|----------|------|-------|
| Llama 2-7B | 45.3 | 44.8 | 44.1 |
| Llama 2-13B | 54.8 | 54.2 | 53.5 |

## Problemas comuns

### CUDA OOM durante treinamento

```python
# Solução 1: Habilitar gradient checkpointing
model.gradient_checkpointing_enable()

# Solução 2: Reduzir batch size + aumentar acumulação
TrainingArguments(
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16
)

# Solução 3: Usar QLoRA
from transformers import BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4")
```

### Adapter não está aplicando

```python
# Verificar se adapter está ativo
print(model.active_adapters)  # Deve mostrar nome do adapter

# Verificar parâmetros treináveis
model.print_trainable_parameters()

# Garantir que modelo está em modo treinamento
model.train()
```

### Degradação de qualidade

```python
# Aumentar rank
LoraConfig(r=32, lora_alpha=64)

# Almejar mais módulos
target_modules = "all-linear"

# Usar mais dados de treinamento e épocas
TrainingArguments(num_train_epochs=5)

# Taxa de aprendizado menor
TrainingArguments(learning_rate=1e-4)
```

## Melhores práticas

1. **Comece com r=8-16**, aumente se qualidade for insuficiente
2. **Use alpha = 2 * rank** como ponto de partida
3. **Almejar camadas de atenção + MLP** para melhor qualidade/eficiência
4. **Habilitar gradient checkpointing** para economizar memória
5. **Salvar adapters frequentemente** (arquivos pequenos, rollback fácil)
6. **Avaliar em dados retidos** antes de mesclar
7. **Use QLoRA para modelos 70B+** em hardware consumer

## Referências

- **[Advanced Usage](references/advanced-usage.md)** - DoRA, LoftQ, estabilização de rank, módulos customizados
- **[Troubleshooting](references/troubleshooting.md)** - Erros comuns, debugging, otimização

## Recursos

- **GitHub**: https://github.com/huggingface/peft
- **Docs**: https://huggingface.co/docs/peft
- **LoRA Paper**: arXiv:2106.09685
- **QLoRA Paper**: arXiv:2305.14314
- **Models**: https://huggingface.co/models?library=peft