---
name: openrlhf-training
description: Framework RLHF de alta performance com aceleração Ray+vLLM. Use para treinamento PPO, GRPO, RLOO, DPO de modelos grandes (7B-70B+). Construído em Ray, vLLM, ZeRO-3. 2× mais rápido que DeepSpeedChat com arquitetura distribuída e compartilhamento de recursos GPU.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Post-Training, OpenRLHF, RLHF, PPO, GRPO, RLOO, DPO, Ray, vLLM, Distributed Training, Large Models, ZeRO-3]
dependencies: [openrlhf, ray, vllm, torch, transformers, deepspeed]
---

# OpenRLHF - Treinamento RLHF de Alta Performance

## Início rápido

OpenRLHF é um framework RLHF baseado em Ray otimizado para treinamento distribuído com aceleração de inferência vLLM.

**Instalação**:
```bash
# Inicie contêiner Docker
docker run --runtime=nvidia -it --rm --shm-size="10g" --cap-add=SYS_ADMIN \
  -v $PWD:/openrlhf nvcr.io/nvidia/pytorch:25.02-py3 bash

# Desinstale conflitos
sudo pip uninstall xgboost transformer_engine flash_attn pynvml -y

# Instale OpenRLHF com vLLM
pip install openrlhf[vllm]
```

**Treinamento PPO** (Hybrid Engine):
```bash
ray start --head --node-ip-address 0.0.0.0 --num-gpus 8

ray job submit --address="http://127.0.0.1:8265" \
  --runtime-env-json='{"working_dir": "/openrlhf"}' \
  -- python3 -m openrlhf.cli.train_ppo_ray \
  --ref_num_nodes 1 --ref_num_gpus_per_node 8 \
  --reward_num_nodes 1 --reward_num_gpus_per_node 8 \
  --critic_num_nodes 1 --critic_num_gpus_per_node 8 \
  --actor_num_nodes 1 --actor_num_gpus_per_node 8 \
  --vllm_num_engines 4 --vllm_tensor_parallel_size 2 \
  --colocate_all_models \
  --vllm_gpu_memory_utilization 0.5 \
  --pretrain OpenRLHF/Llama-3-8b-sft-mixture \
  --reward_pretrain OpenRLHF/Llama-3-8b-rm-700k \
  --save_path ./output/llama3-8b-rlhf \
  --micro_train_batch_size 8 --train_batch_size 128 \
  --micro_rollout_batch_size 16 --rollout_batch_size 1024 \
  --max_epochs 1 --prompt_max_len 1024 --generate_max_len 1024 \
  --zero_stage 3 --bf16 \
  --actor_learning_rate 5e-7 --critic_learning_rate 9e-6 \
  --init_kl_coef 0.01 --normalize_reward \
  --gradient_checkpointing --packing_samples \
  --vllm_enable_sleep --deepspeed_enable_sleep
```

**Treinamento GRPO** (Group Normalized Policy Optimization):
```bash
# Mesmo comando que PPO, mas adicione:
--advantage_estimator group_norm
```

## Fluxos de trabalho comuns

### Fluxo de trabalho 1: Pipeline RLHF completo (SFT → Reward Model → PPO)

**Etapa 1: Treine modelo de reward** (DPO):
```bash
deepspeed --module openrlhf.cli.train_rm \
  --save_path ./output/llama3-8b-rm \
  --save_steps -1 --logging_steps 1 \
  --eval_steps -1 --train_batch_size 256 \
  --micro_train_batch_size 1 --pretrain meta-llama/Meta-Llama-3-8B \
  --bf16 --max_epochs 1 --max_len 8192 \
  --zero_stage 3 --learning_rate 9e-6 \
  --dataset OpenRLHF/preference_dataset_mixture2_and_safe_pku \
  --apply_chat_template --chosen_key chosen \
  --rejected_key rejected --flash_attn --gradient_checkpointing
```

**Etapa 2: Treinamento PPO**:
```bash
ray start --head --node-ip-address 0.0.0.0 --num-gpus 8

ray job submit --address="http://127.0.0.1:8265" \
  -- python3 -m openrlhf.cli.train_ppo_ray \
  --ref_num_nodes 1 --ref_num_gpus_per_node 8 \
  --reward_num_nodes 1 --reward_num_gpus_per_node 8 \
  --critic_num_nodes 1 --critic_num_gpus_per_node 8 \
  --actor_num_nodes 1 --actor_num_gpus_per_node 8 \
  --vllm_num_engines 4 --vllm_tensor_parallel_size 2 \
  --colocate_all_models \
  --pretrain OpenRLHF/Llama-3-8b-sft-mixture \
  --reward_pretrain ./output/llama3-8b-rm \
  --save_path ./output/llama3-8b-ppo \
  --micro_train_batch_size 8 --train_batch_size 128 \
  --micro_rollout_batch_size 16 --rollout_batch_size 1024 \
  --max_epochs 1 --prompt_max_len 1024 --generate_max_len 1024 \
  --zero_stage 3 --bf16 \
  --actor_learning_rate 5e-7 --critic_learning_rate 9e-6 \
  --init_kl_coef 0.01 --normalize_reward \
  --vllm_enable_sleep --deepspeed_enable_sleep
```

### Fluxo de trabalho 2: Treinamento GRPO (sem modelo critic necessário)

Alternativa eficiente em memória ao PPO:

```bash
ray job submit --address="http://127.0.0.1:8265" \
  -- python3 -m openrlhf.cli.train_ppo_ray \
  --advantage_estimator group_norm \
  --ref_num_nodes 1 --ref_num_gpus_per_node 8 \
  --reward_num_nodes 1 --reward_num_gpus_per_node 8 \
  --actor_num_nodes 1 --actor_num_gpus_per_node 8 \
  --vllm_num_engines 4 --vllm_tensor_parallel_size 2 \
  --colocate_all_models \
  --pretrain OpenRLHF/Llama-3-8b-sft-mixture \
  --reward_pretrain OpenRLHF/Llama-3-8b-rm-700k \
  --save_path ./output/llama3-8b-grpo \
  --micro_train_batch_size 8 --train_batch_size 128 \
  --micro_rollout_batch_size 16 --rollout_batch_size 1024 \
  --max_epochs 1 --bf16 \
  --actor_learning_rate 5e-7 \
  --init_kl_coef 0.01 --use_kl_loss --kl_estimator k3 \
  --normalize_reward --no_advantage_std_norm
```

**Parâmetros-chave do GRPO**:
- `--advantage_estimator group_norm` - Ativa GRPO
- `--use_kl_loss` - Perda KL do paper GRPO
- `--kl_estimator k3` - Função de perda (k2 ≈ k1)
- `--no_advantage_std_norm` - Desabilita normalização de desvio padrão

### Fluxo de trabalho 3: Treinamento DPO (otimização de preferência)

Alternativa mais simples sem modelo de reward:

```bash
deepspeed --module openrlhf.cli.train_dpo \
  --save_path ./output/llama3-8b-dpo \
  --save_steps -1 --logging_steps 1 \
  --eval_steps -1 --train_batch_size 256 \
  --micro_train_batch_size 2 --pretrain meta-llama/Meta-Llama-3-8B \
  --bf16 --max_epochs 1 --max_len 8192 \
  --zero_stage 3 --learning_rate 5e-7 --beta 0.1 \
  --dataset OpenRLHF/preference_dataset_mixture2_and_safe_pku \
  --apply_chat_template --chosen_key chosen \
  --rejected_key rejected --flash_attn --gradient_checkpointing
```

## Quando usar vs alternativas

**Use OpenRLHF quando**:
- Treinar modelos grandes (7B-70B+) com RL
- Precisa de aceleração de inferência vLLM
- Quer arquitetura distribuída com Ray
- Tem cluster GPU multi-nó
- Precisa de PPO/GRPO/RLOO/DPO em um único framework

**Seleção de algoritmo**:
- **PPO**: Controle máximo, melhor para rewards complexos
- **GRPO**: Eficiente em memória, sem critic necessário
- **RLOO**: PPO modificado com KL por token
- **REINFORCE++**: Mais estável que GRPO, mais rápido que PPO
- **DPO**: Mais simples, sem modelo de reward necessário

**Use alternativas em vez disso**:
- **TRL**: Treinamento em nó único, API mais simples
- **veRL**: Framework da ByteDance para modelos 671B
- **DeepSpeedChat**: Integrado ao ecossistema DeepSpeed

## Problemas comuns

**Problema: OOM em GPU com modelos grandes**

Desabilite colocalização de modelos:
```bash
# Remova a flag --colocate_all_models
# Aloque GPUs separadas para cada modelo
--actor_num_gpus_per_node 8 \
--critic_num_gpus_per_node 8 \
--reward_num_gpus_per_node 8 \
--ref_num_gpus_per_node 8
```

**Problema: Índice GPU fora do intervalo no DeepSpeed**

Configure variável de ambiente:
```bash
export RAY_EXPERIMENTAL_NOSET_CUDA_VISIBLE_DEVICES=1
```

**Problema: Instabilidade no treinamento**

Use Hybrid Engine em vez de assíncrono:
```bash
--colocate_all_models \
--vllm_enable_sleep \
--deepspeed_enable_sleep
```

Ajuste coeficiente KL:
```bash
--init_kl_coef 0.05  # Aumente de 0.01
```

**Problema: Geração lenta durante PPO**

Ative aceleração vLLM:
```bash
--vllm_num_engines 4 \
--vllm_tensor_parallel_size 2 \
--vllm_gpu_memory_utilization 0.5
```

## Tópicos avançados

**Compartilhamento de GPU do Hybrid Engine**: Veja [references/hybrid-engine.md](references/hybrid-engine.md) para sleep mode vLLM, sleep mode DeepSpeed e alocação ideal de nós.

**Comparação de algoritmos**: Veja [references/algorithm-comparison.md](references/algorithm-comparison.md) para benchmarks e hiperparâmetros de PPO vs GRPO vs RLOO vs REINFORCE++.

**Configuração multi-nó**: Veja [references/multi-node-training.md](references/multi-node-training.md) para configuração de cluster Ray e tolerância a falhas.

**Funções de reward customizadas**: Veja [references/custom-rewards.md](references/custom-rewards.md) para ajuste fino reforçado e RLHF de agentes.

## Requisitos de hardware

- **GPU**: NVIDIA A100/H100 recomendado
- **VRAM**:
  - Modelo 7B: 8× A100 40GB (Hybrid Engine)
  - Modelo 70B: 48× A100 80GB (vLLM:Actor:Critic = 1:1:1)
- **Multi-nó**: Cluster Ray com InfiniBand recomendado
- **Docker**: Container PyTorch NVIDIA 25.02+

**Performance**:
- 2× mais rápido que DeepSpeedChat
- Aceleração de inferência vLLM
- Hybrid Engine minimiza tempo ocioso de GPU

## Recursos

- Docs: https://github.com/OpenRLHF/OpenRLHF
- Paper: https://arxiv.org/abs/2405.11143
- Examples: https://github.com/OpenRLHF/OpenRLHF/tree/main/examples
- Discord: Suporte da comunidade