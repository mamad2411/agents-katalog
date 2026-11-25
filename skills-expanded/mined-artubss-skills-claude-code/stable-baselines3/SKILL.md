---
name: stable-baselines3
description: Use this skill for reinforcement learning tasks including training RL agents (PPO, SAC, DQN, TD3, DDPG, A2C, etc.), creating custom Gym environments, implementing callbacks for monitoring and control, using vectorized environments for parallel training, and integrating with deep RL workflows. This skill should be used when users request RL algorithm implementation, agent training, environment design, or RL experimentation.
---

# Stable Baselines3

## Visão Geral

Stable Baselines3 (SB3) é uma biblioteca baseada em PyTorch que fornece implementações confiáveis de algoritmos de aprendizado por reforço. Esta skill oferece orientação abrangente para treinar agentes de RL, criar ambientes customizados, implementar callbacks e otimizar workflows de treinamento usando a API unificada do SB3.

## Capacidades Principais

### 1. Treinamento de Agentes de RL

**Padrão de Treinamento Básico:**

```python
import gymnasium as gym
from stable_baselines3 import PPO

# Create environment
env = gym.make("CartPole-v1")

# Initialize agent
model = PPO("MlpPolicy", env, verbose=1)

# Train the agent
model.learn(total_timesteps=10000)

# Save the model
model.save("ppo_cartpole")

# Load the model (without prior instantiation)
model = PPO.load("ppo_cartpole", env=env)
```

**Observações Importantes:**
- `total_timesteps` é um limite inferior; o treinamento real pode exceder isso devido à coleta de batches
- Use `model.load()` como um método estático, não em uma instância existente
- O buffer de replay NÃO é salvo com o modelo para economizar espaço

**Seleção de Algoritmo:**
Use `references/algorithms.md` para orientação detalhada sobre características de algoritmos e seleção. Referência rápida:
- **PPO/A2C**: Uso geral, suporta todos os tipos de espaço de ação, bom para multiprocessamento
- **SAC/TD3**: Controle contínuo, off-policy, eficiente em amostragem
- **DQN**: Ações discretas, off-policy
- **HER**: Tarefas com objetivos condicionados

Veja `scripts/train_rl_agent.py` para um template completo de treinamento com melhores práticas.

### 2. Ambientes Customizados

**Requisitos:**
Ambientes customizados devem herdar de `gymnasium.Env` e implementar:
- `__init__()`: Definir action_space e observation_space
- `reset(seed, options)`: Retornar observação inicial e dicionário info
- `step(action)`: Retornar observation, reward, terminated, truncated, info
- `render()`: Visualização (opcional)
- `close()`: Limpeza de recursos

**Restrições-Chave:**
- Observações de imagem devem ser `np.uint8` no intervalo [0, 255]
- Use formato channel-first quando possível (channels, height, width)
- SB3 normaliza imagens automaticamente dividindo por 255
- Defina `normalize_images=False` em policy_kwargs se pré-normalizado
- SB3 NÃO suporta espaços `Discrete` ou `MultiDiscrete` com `start!=0`

**Validação:**
```python
from stable_baselines3.common.env_checker import check_env

check_env(env, warn=True)
```

Veja `scripts/custom_env_template.py` para um template completo de ambiente customizado e `references/custom_environments.md` para orientação abrangente.

### 3. Ambientes Vetorizados

**Propósito:**
Ambientes vetorizados executam múltiplas instâncias do ambiente em paralelo, acelerando o treinamento e habilitando certos wrappers (frame-stacking, normalização).

**Tipos:**
- **DummyVecEnv**: Execução sequencial no processo atual (para ambientes leves)
- **SubprocVecEnv**: Execução paralela entre processos (para ambientes computacionalmente pesados)

**Configuração Rápida:**
```python
from stable_baselines3.common.env_util import make_vec_env

# Create 4 parallel environments
env = make_vec_env("CartPole-v1", n_envs=4, vec_env_cls=SubprocVecEnv)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=25000)
```

**Otimização Off-Policy:**
Ao usar múltiplos ambientes com algoritmos off-policy (SAC, TD3, DQN), defina `gradient_steps=-1` para executar uma atualização de gradiente por passo de ambiente, equilibrando tempo de relógio e eficiência de amostragem.

**Diferenças de API:**
- `reset()` retorna apenas observações (info disponível em `vec_env.reset_infos`)
- `step()` retorna tupla de 4 elementos: `(obs, rewards, dones, infos)` não 5-tupla
- Ambientes auto-reiniciam após episódios
- Observações terminais disponíveis via `infos[env_idx]["terminal_observation"]`

Veja `references/vectorized_envs.md` para informações detalhadas sobre wrappers e uso avançado.

### 4. Callbacks para Monitoramento e Controle

**Propósito:**
Callbacks habilitam monitoramento de métricas, salvamento de checkpoints, implementação de parada antecipada e lógica de treinamento customizada sem modificar algoritmos principais.

**Callbacks Comuns:**
- **EvalCallback**: Avaliar periodicamente e salvar melhor modelo
- **CheckpointCallback**: Salvar checkpoints de modelo em intervalos
- **StopTrainingOnRewardThreshold**: Parar quando recompensa alvo é alcançada
- **ProgressBarCallback**: Exibir progresso de treinamento com temporizações

**Estrutura de Callback Customizado:**
```python
from stable_baselines3.common.callbacks import BaseCallback

class CustomCallback(BaseCallback):
    def _on_training_start(self):
        # Called before first rollout
        pass

    def _on_step(self):
        # Called after each environment step
        # Return False to stop training
        return True

    def _on_rollout_end(self):
        # Called at end of rollout
        pass
```

**Atributos Disponíveis:**
- `self.model`: A instância do algoritmo de RL
- `self.num_timesteps`: Total de passos do ambiente
- `self.training_env`: O ambiente de treinamento

**Encadeamento de Callbacks:**
```python
from stable_baselines3.common.callbacks import CallbackList

callback = CallbackList([eval_callback, checkpoint_callback, custom_callback])
model.learn(total_timesteps=10000, callback=callback)
```

Veja `references/callbacks.md` para documentação abrangente de callbacks.

### 5. Persistência e Inspeção de Modelos

**Salvamento e Carregamento:**
```python
# Save model
model.save("model_name")

# Save normalization statistics (if using VecNormalize)
vec_env.save("vec_normalize.pkl")

# Load model
model = PPO.load("model_name", env=env)

# Load normalization statistics
vec_env = VecNormalize.load("vec_normalize.pkl", vec_env)
```

**Acesso a Parâmetros:**
```python
# Get parameters
params = model.get_parameters()

# Set parameters
model.set_parameters(params)

# Access PyTorch state dict
state_dict = model.policy.state_dict()
```

### 6. Avaliação e Gravação

**Avaliação:**
```python
from stable_baselines3.common.evaluation import evaluate_policy

mean_reward, std_reward = evaluate_policy(
    model,
    env,
    n_eval_episodes=10,
    deterministic=True
)
```

**Gravação de Vídeo:**
```python
from stable_baselines3.common.vec_env import VecVideoRecorder

# Wrap environment with video recorder
env = VecVideoRecorder(
    env,
    "videos/",
    record_video_trigger=lambda x: x % 2000 == 0,
    video_length=200
)
```

Veja `scripts/evaluate_agent.py` para um template completo de avaliação e gravação.

### 7. Recursos Avançados

**Agendamentos de Taxa de Aprendizado:**
```python
def linear_schedule(initial_value):
    def func(progress_remaining):
        # progress_remaining goes from 1 to 0
        return progress_remaining * initial_value
    return func

model = PPO("MlpPolicy", env, learning_rate=linear_schedule(0.001))
```

**Políticas Multi-Input (Observações Dict):**
```python
model = PPO("MultiInputPolicy", env, verbose=1)
```
Use quando observações são dicionários (p.ex., combinando imagens com dados de sensores).

**Hindsight Experience Replay:**
```python
from stable_baselines3 import SAC, HerReplayBuffer

model = SAC(
    "MultiInputPolicy",
    env,
    replay_buffer_class=HerReplayBuffer,
    replay_buffer_kwargs=dict(
        n_sampled_goal=4,
        goal_selection_strategy="future",
    ),
)
```

**Integração com TensorBoard:**
```python
model = PPO("MlpPolicy", env, tensorboard_log="./tensorboard/")
model.learn(total_timesteps=10000)
```

## Orientação de Workflow

**Iniciando um Novo Projeto de RL:**

1. **Defina o problema**: Identifique espaço de observação, espaço de ação e estrutura de recompensa
2. **Escolha algoritmo**: Use `references/algorithms.md` para orientação de seleção
3. **Crie/adapte ambiente**: Use `scripts/custom_env_template.py` se necessário
4. **Valide ambiente**: Sempre execute `check_env()` antes de treinar
5. **Configure treinamento**: Use `scripts/train_rl_agent.py` como template inicial
6. **Adicione monitoramento**: Implemente callbacks para avaliação e checkpointing
7. **Otimize desempenho**: Considere ambientes vetorizados para velocidade
8. **Avalie e itere**: Use `scripts/evaluate_agent.py` para avaliação

**Problemas Comuns:**

- **Erros de memória**: Reduza `buffer_size` para algoritmos off-policy ou use menos ambientes em paralelo
- **Treinamento lento**: Considere SubprocVecEnv para ambientes em paralelo
- **Treinamento instável**: Tente algoritmos diferentes, ajuste hiperparâmetros ou verifique escalonamento de recompensa
- **Erros de importação**: Garanta que `stable_baselines3` está instalado: `uv pip install stable-baselines3[extra]`

## Recursos

### scripts/
- `train_rl_agent.py`: Template de script de treinamento completo com melhores práticas
- `evaluate_agent.py`: Template de avaliação de agente e gravação de vídeo
- `custom_env_template.py`: Template de ambiente Gym customizado

### references/
- `algorithms.md`: Comparação detalhada de algoritmos e guia de seleção
- `custom_environments.md`: Guia abrangente para criação de ambiente customizado
- `callbacks.md`: Referência completa do sistema de callbacks
- `vectorized_envs.md`: Uso de ambientes vetorizados e wrappers

## Instalação

```bash
# Basic installation
uv pip install stable-baselines3

# With extra dependencies (Tensorboard, etc.)
uv pip install stable-baselines3[extra]
```