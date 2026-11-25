---
name: axolotl
description: Orientação especializada para fine-tuning de LLMs com Axolotl - configs YAML, 100+ modelos, LoRA/QLoRA, DPO/KTO/ORPO/GRPO, suporte multimodal
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Fine-Tuning, Axolotl, LLM, LoRA, QLoRA, DPO, KTO, ORPO, GRPO, YAML, HuggingFace, DeepSpeed, Multimodal]
dependencies: [axolotl, torch, transformers, datasets, peft, accelerate, deepspeed]
---

# Axolotl Skill

Assistência abrangente com desenvolvimento em axolotl, gerada a partir da documentação oficial.

## Quando Usar Esta Skill

Esta skill deve ser acionada quando:
- Trabalhar com axolotl
- Fazer perguntas sobre features ou APIs do axolotl
- Implementar soluções com axolotl
- Debugar código em axolotl
- Aprender best practices do axolotl

## Referência Rápida

### Padrões Comuns

**Padrão 1:** Para validar que existem velocidades de transferência de dados aceitáveis para seu job de treinamento, executar NCCL Tests pode ajudar a identificar gargalos, por exemplo:

```
./build/all_reduce_perf -b 8 -e 128M -f 2 -g 3
```

**Padrão 2:** Configure seu modelo para usar FSDP no yaml do Axolotl. Por exemplo:

```
fsdp_version: 2
fsdp_config:
  offload_params: true
  state_dict_type: FULL_STATE_DICT
  auto_wrap_policy: TRANSFORMER_BASED_WRAP
  transformer_layer_cls_to_wrap: LlamaDecoderLayer
  reshard_after_forward: true
```

**Padrão 3:** O context_parallel_size deve ser um divisor do número total de GPUs. Por exemplo:

```
context_parallel_size
```

**Padrão 4:** Por exemplo: - Com 8 GPUs e sem sequence parallelism: 8 batches diferentes processados por step - Com 8 GPUs e context_parallel_size=4: Apenas 2 batches diferentes processados por step (cada um dividido entre 4 GPUs) - Se seu micro_batch_size por GPU é 2, o global batch size diminui de 16 para 4

```
context_parallel_size=4
```

**Padrão 5:** Definir save_compressed: true na sua configuração habilita salvar modelos em formato comprimido, que: - Reduz uso de espaço em disco em aproximadamente 40% - Mantém compatibilidade com vLLM para inferência acelerada - Mantém compatibilidade com llmcompressor para otimização adicional (exemplo: quantização)

```
save_compressed: true
```

**Padrão 6:** Nota Não é necessário colocar sua integração na pasta integrations. Pode estar em qualquer local, desde que esteja instalada em um pacote no seu python env. Veja este repositório para um exemplo: https://github.com/axolotl-ai-cloud/diff-transformer

```
integrations
```

**Padrão 7:** Manipule dados de exemplo único e em lotes. - exemplo único: sample['input_ids'] é uma list[int] - dados em lote: sample['input_ids'] é uma list[list[int]]

```
utils.trainer.drop_long_seq(sample, sequence_len=2048, min_sequence_len=2)
```

### Exemplos de Padrões de Código

**Exemplo 1** (python):
```python
cli.cloud.modal_.ModalCloud(config, app=None)
```

**Exemplo 2** (python):
```python
cli.cloud.modal_.run_cmd(cmd, run_folder, volumes=None)
```

**Exemplo 3** (python):
```python
core.trainers.base.AxolotlTrainer(
    *_args,
    bench_data_collator=None,
    eval_data_collator=None,
    dataset_tags=None,
    **kwargs,
)
```

**Exemplo 4** (python):
```python
core.trainers.base.AxolotlTrainer.log(logs, start_time=None)
```

**Exemplo 5** (python):
```python
prompt_strategies.input_output.RawInputOutputPrompter()
```

## Arquivos de Referência

Esta skill inclui documentação abrangente em `references/`:

- **api.md** - Documentação de API
- **dataset-formats.md** - Documentação de Dataset-Formats
- **other.md** - Outra documentação

Use `view` para ler arquivos de referência específicos quando informações detalhadas forem necessárias.

## Trabalhando com Esta Skill

### Para Iniciantes
Comece com os arquivos de referência getting_started ou tutorials para conceitos fundamentais.

### Para Features Específicas
Use o arquivo de referência da categoria apropriada (api, guides, etc.) para informações detalhadas.

### Para Exemplos de Código
A seção de referência rápida acima contém padrões comuns extraídos da documentação oficial.

## Recursos

### references/
Documentação organizada extraída de fontes oficiais. Estes arquivos contêm:
- Explicações detalhadas
- Exemplos de código com anotações de linguagem
- Links para documentação original
- Índice para navegação rápida

### scripts/
Adicione scripts auxiliares aqui para tarefas comuns de automação.

### assets/
Adicione templates, boilerplate ou projetos de exemplo aqui.

## Notas

- Esta skill foi gerada automaticamente a partir da documentação oficial
- Arquivos de referência preservam a estrutura e exemplos dos documentos originais
- Exemplos de código incluem detecção de linguagem para melhor destaque de sintaxe
- Padrões de referência rápida são extraídos de exemplos de uso comum na documentação

## Atualizando

Para atualizar esta skill com documentação modificada:
1. Re-execute o scraper com a mesma configuração
2. A skill será reconstruída com as informações mais recentes