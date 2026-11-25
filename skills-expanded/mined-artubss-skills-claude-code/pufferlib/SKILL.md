---
name: pufferlib
description: Essa habilidade deve ser usada ao trabalhar com tarefas de reinforcement learning, incluindo treinamento RL de alto desempenho, desenvolvimento de ambientes customizados, simulação paralela vetorizada, sistemas multi-agent ou integração com ambientes RL existentes (Gymnasium, PettingZoo, Atari, Procgen, etc.). Use essa habilidade para implementar treinamento PPO, criar ambientes PufferEnv, otimizar desempenho em RL ou desenvolver políticas com CNNs/LSTMs.
---

# PufferLib - Reinforcement Learning de Alto Desempenho

## Visão Geral

PufferLib é uma biblioteca de reinforcement learning de alto desempenho projetada para simulação paralela rápida de ambientes e treinamento. Ela alcança treinamento em milhões de passos por segundo por meio de vetorização otimizada, suporte nativo a multi-agent e implementação eficiente de PPO (PuffeRL). A biblioteca fornece a suíte Ocean com 20+ ambientes e integração perfeita com Gymnasium, PettingZoo e frameworks RL especializados.

## Quando Usar Essa Habilidade

Use essa habilidade quando:
- **Treinar agentes RL** com PPO em qualquer ambiente (single ou multi-agent)
- **Criar ambientes customizados** usando a API PufferEnv
- **Otimizar desempenho** para simulação paralela de ambientes (vetorização)
- **Integrar ambientes existentes** de Gymnasium, PettingZoo, Atari, Procgen, etc.
- **Desenvolver políticas** com CNN, LSTM ou arquiteturas customizadas
- **Escalar RL** para milhões de passos por segundo para experimentação mais rápida
- **RL multi-agent** com suporte nativo para ambientes multi-agent

## Capacidades Principais

### 1. Treinamento de Alto Desempenho (PuffeRL)

PuffeRL é o algoritmo PPO+LSTM otimizado do PufferLib alcançando 1M-4M passos/segundo.

**Quick start treinamento:**
```bash
# Treinamento via CLI
puffer train procgen-coinrun --train.device cuda --train.learning-rate 3e-4

# Treinamento distribuído
torchrun --nproc_per_node=4 train.py
```

**Loop de treinamento em Python:**
```python
import pufferlib
from pufferlib import PuffeRL

# Criar ambiente vetorizado
env = pufferlib.make('procgen-coinrun', num_envs=256)

# Criar trainer
trainer = PuffeRL(
    env=env,
    policy=my_policy,
    device='cuda',
    learning_rate=3e-4,
    batch_size=32768
)

# Loop de treinamento
for iteration in range(num_iterations):
    trainer.evaluate()  # Coletar rollouts
    trainer.train()     # Treinar no batch
    trainer.mean_and_log()  # Log dos resultados
```

**Para orientação completa de treinamento**, consulte `references/training.md` para:
- Workflow de treinamento completo e opções CLI
- Ajuste de hiperparâmetros com Protein
- Treinamento distribuído multi-GPU/multi-node
- Integração com logger (Weights & Biases, Neptune)
- Checkpointing e retomada de treinamento
- Dicas de otimização de desempenho
- Padrões de curriculum learning

### 2. Desenvolvimento de Ambientes (PufferEnv)

Crie ambientes customizados de alto desempenho com a API PufferEnv.

**Estrutura básica de ambiente:**
```python
import numpy as np
from pufferlib import PufferEnv

class MyEnvironment(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)

        # Definir espaços
        self.observation_space = self.make_space((4,))
        self.action_space = self.make_discrete(4)

        self.reset()

    def reset(self):
        # Resetar estado e retornar observação inicial
        return np.zeros(4, dtype=np.float32)

    def step(self, action):
        # Executar ação, computar recompensa, verificar término
        obs = self._get_observation()
        reward = self._compute_reward()
        done = self._is_done()
        info = {}

        return obs, reward, done, info
```

**Use o script template:** `scripts/env_template.py` fornece templates completos de ambiente single-agent e multi-agent com exemplos de:
- Diferentes tipos de espaço de observação (vetor, imagem, dicionário)
- Variações de espaço de ação (discreto, contínuo, multi-discreto)
- Estrutura de ambiente multi-agent
- Utilitários de teste

**Para desenvolvimento completo de ambientes**, consulte `references/environments.md` para:
- Detalhes da API PufferEnv e padrões de operação in-place
- Definições de espaço de observação e ação
- Criação de ambientes multi-agent
- Suíte Ocean (20+ ambientes pré-construídos)
- Otimização de desempenho (workflow Python para C)
- Wrappers de ambiente e melhores práticas
- Técnicas de debug e validação

### 3. Vetorização e Desempenho

Alcance a máxima throughput com simulação paralela otimizada.

**Setup de vetorização:**
```python
import pufferlib

# Vetorização automática
env = pufferlib.make('environment_name', num_envs=256, num_workers=8)

# Benchmarks de desempenho:
# - Ambientes Python puro: 100k-500k SPS
# - Ambientes baseados em C: 100M+ SPS
# - Com treinamento: 400k-4M SPS total
```

**Otimizações principais:**
- Buffers de memória compartilhada para passagem de observação sem cópia
- Flags busy-wait ao invés de pipes/queues
- Ambientes excedentes para retornos assíncronos
- Múltiplos ambientes por worker

**Para otimização de vetorização**, consulte `references/vectorization.md` para:
- Arquitetura e características de desempenho
- Configuração de worker e batch size
- Modos serial vs multiprocessing vs async
- Padrões de memória compartilhada e zero-copy
- Vetorização hierárquica em larga escala
- Estratégias de vetorização multi-agent
- Profiling e troubleshooting de desempenho

### 4. Desenvolvimento de Políticas

Construa políticas como módulos PyTorch padrão com utilitários opcionais.

**Estrutura básica de política:**
```python
import torch.nn as nn
from pufferlib.pytorch import layer_init

class Policy(nn.Module):
    def __init__(self, observation_space, action_space):
        super().__init__()

        # Encoder
        self.encoder = nn.Sequential(
            layer_init(nn.Linear(obs_dim, 256)),
            nn.ReLU(),
            layer_init(nn.Linear(256, 256)),
            nn.ReLU()
        )

        # Actor e critic heads
        self.actor = layer_init(nn.Linear(256, num_actions), std=0.01)
        self.critic = layer_init(nn.Linear(256, 1), std=1.0)

    def forward(self, observations):
        features = self.encoder(observations)
        return self.actor(features), self.critic(features)
```

**Para desenvolvimento completo de políticas**, consulte `references/policies.md` para:
- Políticas CNN para observações de imagem
- Políticas recorrentes com LSTM otimizado (3x mais rápido em inferência)
- Políticas multi-input para observações complexas
- Políticas de ação contínua
- Políticas multi-agent (parâmetros compartilhados vs independentes)
- Arquiteturas avançadas (attention, residual)
- Normalização de observação e gradient clipping
- Debug e teste de política

### 5. Integração de Ambientes

Integre perfeitamente ambientes de frameworks RL populares.

**Integração Gymnasium:**
```python
import gymnasium as gym
import pufferlib

# Envolver ambiente Gymnasium
gym_env = gym.make('CartPole-v1')
env = pufferlib.emulate(gym_env, num_envs=256)

# Ou usar make diretamente
env = pufferlib.make('gym-CartPole-v1', num_envs=256)
```

**PettingZoo multi-agent:**
```python
# Ambiente multi-agent
env = pufferlib.make('pettingzoo-knights-archers-zombies', num_envs=128)
```

**Frameworks suportados:**
- Gymnasium / OpenAI Gym
- PettingZoo (parallel e AEC)
- Atari (ALE)
- Procgen
- NetHack / MiniHack
- Minigrid
- Neural MMO
- Crafter
- GPUDrive
- MicroRTS
- Griddly
- E mais...

**Para detalhes de integração**, consulte `references/integration.md` para:
- Exemplos de integração completos para cada framework
- Wrappers customizados (observação, recompensa, frame stacking, action repeat)
- Achatamento e desachatamento de espaço
- Registro de ambiente
- Padrões de compatibilidade
- Considerações de desempenho
- Debug de integração

## Workflow Quick Start

### Para Treinar Ambientes Existentes

1. Escolha ambiente da suíte Ocean ou framework compatível
2. Use `scripts/train_template.py` como ponto de partida
3. Configure hiperparâmetros para sua tarefa
4. Execute treinamento com CLI ou script Python
5. Monitore com Weights & Biases ou Neptune
6. Consulte `references/training.md` para otimização

### Para Criar Ambientes Customizados

1. Comece com `scripts/env_template.py`
2. Defina espaços de observação e ação
3. Implemente métodos `reset()` e `step()`
4. Teste ambiente localmente
5. Vetorize com `pufferlib.emulate()` ou `make()`
6. Consulte `references/environments.md` para padrões avançados
7. Otimize com `references/vectorization.md` se necessário

### Para Desenvolvimento de Política

1. Escolha arquitetura baseada em observações:
   - Observações vetorizadas → política MLP
   - Observações de imagem → política CNN
   - Tarefas sequenciais → política LSTM
   - Observações complexas → política multi-input
2. Use `layer_init` para inicialização correta de pesos
3. Siga padrões em `references/policies.md`
4. Teste com ambiente antes do treinamento completo

### Para Otimização de Desempenho

1. Faça profiling da throughput atual (passos por segundo)
2. Verifique configuração de vetorização (num_envs, num_workers)
3. Otimize código do ambiente (ops in-place, vetorização numpy)
4. Considere implementação em C para caminhos críticos
5. Use `references/vectorization.md` para otimização sistemática

## Recursos

### scripts/

**train_template.py** - Template de script de treinamento completo com:
- Criação e configuração de ambiente
- Inicialização de política
- Integração com logger (WandB, Neptune)
- Loop de treinamento com checkpointing
- Parsing de argumentos command-line
- Setup de treinamento distribuído multi-GPU

**env_template.py** - Templates de implementação de ambiente:
- Exemplo PufferEnv single-agent (grid world)
- Exemplo PufferEnv multi-agent (navegação cooperativa)
- Múltiplos padrões de espaço de observação/ação
- Utilitários de teste

### references/

**training.md** - Guia abrangente de treinamento:
- Workflow de treinamento e opções CLI
- Configuração de hiperparâmetros
- Treinamento distribuído (multi-GPU, multi-node)
- Monitoramento e logging
- Checkpointing
- Ajuste de hiperparâmetros com Protein
- Otimização de desempenho
- Padrões comuns de treinamento
- Troubleshooting

**environments.md** - Guia de desenvolvimento de ambiente:
- API PufferEnv e características
- Espaços de observação e ação
- Ambientes multi-agent
- Ambientes da suíte Ocean
- Workflow de desenvolvimento de ambiente customizado
- Caminho de otimização Python para C
- Integração com ambiente de terceiros
- Wrappers e melhores práticas
- Debug

**vectorization.md** - Otimização de vetorização:
- Arquitetura e otimizações principais
- Modos de vetorização (serial, multiprocessing, async)
- Configuração de worker e batch
- Padrões de memória compartilhada e zero-copy
- Vetorização avançada (hierárquica, customizada)
- Vetorização multi-agent
- Monitoramento e profiling de desempenho
- Troubleshooting e melhores práticas

**policies.md** - Guia de arquitetura de política:
- Estrutura básica de política
- Políticas CNN para imagens
- Políticas LSTM com otimização
- Políticas multi-input
- Políticas de ação contínua
- Políticas multi-agent
- Arquiteturas avançadas (attention, residual)
- Processamento e desachatamento de observação
- Inicialização e normalização
- Debug e teste

**integration.md** - Guia de integração de framework:
- Integração Gymnasium
- Integração PettingZoo (parallel e AEC)
- Ambientes de terceiros (Procgen, NetHack, Minigrid, etc.)
- Wrappers customizados (observação, recompensa, frame stacking, etc.)
- Conversão de espaço e desachatamento
- Registro de ambiente
- Padrões de compatibilidade
- Considerações de desempenho
- Debug de integração

## Dicas para Sucesso

1. **Comece simples**: Comece com ambientes Ocean ou integração Gymnasium antes de criar ambientes customizados

2. **Faça profiling cedo**: Meça passos por segundo desde o início para identificar gargalos

3. **Use templates**: `scripts/train_template.py` e `scripts/env_template.py` fornecem pontos de partida sólidos

4. **Leia referências conforme necessário**: Cada arquivo de referência é autossuficiente e focado em uma capacidade específica

5. **Otimize progressivamente**: Comece com Python, faça profiling, depois otimize caminhos críticos com C se necessário

6. **Aproveite a vetorização**: A vetorização do PufferLib é essencial para alcançar alta throughput

7. **Monitore treinamento**: Use WandB ou Neptune para rastrear experimentos e identificar problemas cedo

8. **Teste ambientes**: Valide lógica de ambiente antes de escalar treinamento

9. **Verifique ambientes existentes**: A suíte Ocean fornece 20+ ambientes pré-construídos

10. **Use inicialização correta**: Sempre use `layer_init` de `pufferlib.pytorch` para políticas

## Casos de Uso Comuns

### Treinamento em Benchmarks Padrão
```python
# Atari
env = pufferlib.make('atari-pong', num_envs=256)

# Procgen
env = pufferlib.make('procgen-coinrun', num_envs=256)

# Minigrid
env = pufferlib.make('minigrid-empty-8x8', num_envs=256)
```

### Aprendizado Multi-Agent
```python
# PettingZoo
env = pufferlib.make('pettingzoo-pistonball', num_envs=128)

# Política compartilhada para todos os agentes
policy = create_policy(env.observation_space, env.action_space)
trainer = PuffeRL(env=env, policy=policy)
```

### Desenvolvimento de Tarefa Customizada
```python
# Criar ambiente customizado
class MyTask(PufferEnv):
    # ... implementar ambiente ...

# Vetorizar e treinar
env = pufferlib.emulate(MyTask, num_envs=256)
trainer = PuffeRL(env=env, policy=my_policy)
```

### Otimização de Alto Desempenho
```python
# Maximizar throughput
env = pufferlib.make(
    'my-env',
    num_envs=1024,      # Batch grande
    num_workers=16,     # Muitos workers
    envs_per_worker=64  # Otimizar por worker
)
```

## Instalação

```bash
uv pip install pufferlib
```

## Documentação

- Docs oficiais: https://puffer.ai/docs.html
- GitHub: https://github.com/PufferAI/PufferLib
- Discord: Suporte da comunidade disponível