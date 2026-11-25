---
name: pennylane
description: Biblioteca Python multiplataforma para computação quântica, aprendizado de máquina quântico e química quântica. Permite construir e treinar circuitos quânticos com diferenciação automática, integração perfeita com PyTorch/JAX/TensorFlow e execução independente de dispositivo em simuladores e hardware quântico (IBM, Amazon Braket, Google, Rigetti, IonQ, etc.). Use ao trabalhar com circuitos quânticos, algoritmos quânticos variacionais (VQE, QAOA), redes neurais quânticas, modelos híbridos quântico-clássicos, simulações moleculares, cálculos de química quântica ou qualquer tarefa de computação quântica que exija otimização baseada em gradiente, programação agnóstica a hardware ou fluxos de trabalho de aprendizado de máquina quântico.
---

# PennyLane

## Visão Geral

PennyLane é uma biblioteca de computação quântica que permite treinar computadores quânticos como redes neurais. Ela fornece diferenciação automática de circuitos quânticos, programação independente de dispositivo e integração perfeita com frameworks clássicos de aprendizado de máquina.

## Instalação

Instale usando uv:

```bash
uv pip install pennylane
```

Para acesso a hardware quântico, instale plugins de dispositivos:

```bash
# IBM Quantum
uv pip install pennylane-qiskit

# Amazon Braket
uv pip install amazon-braket-pennylane-plugin

# Google Cirq
uv pip install pennylane-cirq

# Rigetti Forest
uv pip install pennylane-rigetti

# IonQ
uv pip install pennylane-ionq
```

## Início Rápido

Construa um circuito quântico e otimize seus parâmetros:

```python
import pennylane as qml
from pennylane import numpy as np

# Criar dispositivo
dev = qml.device('default.qubit', wires=2)

# Definir circuito quântico
@qml.qnode(dev)
def circuit(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.PauliZ(0))

# Otimizar parâmetros
opt = qml.GradientDescentOptimizer(stepsize=0.1)
params = np.array([0.1, 0.2], requires_grad=True)

for i in range(100):
    params = opt.step(circuit, params)
```

## Capacidades Principais

### 1. Construção de Circuitos Quânticos

Construa circuitos com portas, medições e preparação de estado. Consulte `references/quantum_circuits.md` para:
- Portas de um e múltiplos qubits
- Operações controladas e lógica condicional
- Medições mid-circuit e circuitos adaptativos
- Vários tipos de medição (expectativa, probabilidade, amostras)
- Inspeção e depuração de circuitos

### 2. Aprendizado de Máquina Quântico

Crie modelos híbridos quântico-clássicos. Consulte `references/quantum_ml.md` para:
- Integração com PyTorch, JAX, TensorFlow
- Redes neurais quânticas e classificadores variacionais
- Estratégias de codificação de dados (ângulo, amplitude, base, IQP)
- Treinamento de modelos híbridos com retropropagação
- Transfer learning com circuitos quânticos

### 3. Química Quântica

Simule moléculas e compute energias do estado fundamental. Consulte `references/quantum_chemistry.md` para:
- Geração de Hamiltoniano molecular
- Variational Quantum Eigensolver (VQE)
- Ansatz UCCSD para química
- Otimização de geometria e curvas de dissociação
- Cálculos de propriedades moleculares

### 4. Gerenciamento de Dispositivos

Execute em simuladores ou hardware quântico. Consulte `references/devices_backends.md` para:
- Simuladores integrados (default.qubit, lightning.qubit, default.mixed)
- Plugins de hardware (IBM, Amazon Braket, Google, Rigetti, IonQ)
- Seleção e configuração de dispositivos
- Otimização de desempenho e cache
- Aceleração por GPU e compilação JIT

### 5. Otimização

Treine circuitos quânticos com vários otimizadores. Consulte `references/optimization.md` para:
- Otimizadores integrados (Adam, descida de gradiente, momentum, RMSProp)
- Métodos de computação de gradiente (backprop, parameter-shift, adjunto)
- Algoritmos variacionais (VQE, QAOA)
- Estratégias de treinamento (agendas de taxa de aprendizado, mini-lotes)
- Lidando com planaltos áridos e mínimos locais

### 6. Recursos Avançados

Aproveite templates, transformações e compilação. Consulte `references/advanced_features.md` para:
- Templates e camadas de circuito
- Transformações e otimização de circuitos
- Programação em nível de pulso
- Compilação JIT Catalyst
- Modelos de ruído e mitigação de erros
- Estimativa de recursos

## Fluxos de Trabalho Comuns

### Treinar um Classificador Variacional

```python
# 1. Definir ansatz
@qml.qnode(dev)
def classifier(x, weights):
    # Codificar dados
    qml.AngleEmbedding(x, wires=range(4))

    # Camadas variacionais
    qml.StronglyEntanglingLayers(weights, wires=range(4))

    return qml.expval(qml.PauliZ(0))

# 2. Treinar
opt = qml.AdamOptimizer(stepsize=0.01)
weights = np.random.random((3, 4, 3))  # 3 camadas, 4 wires

for epoch in range(100):
    for x, y in zip(X_train, y_train):
        weights = opt.step(lambda w: (classifier(x, w) - y)**2, weights)
```

### Executar VQE para Estado Fundamental Molecular

```python
from pennylane import qchem

# 1. Construir Hamiltoniano
symbols = ['H', 'H']
coords = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.74])
H, n_qubits = qchem.molecular_hamiltonian(symbols, coords)

# 2. Definir ansatz
@qml.qnode(dev)
def vqe_circuit(params):
    qml.BasisState(qchem.hf_state(2, n_qubits), wires=range(n_qubits))
    qml.UCCSD(params, wires=range(n_qubits))
    return qml.expval(H)

# 3. Otimizar
opt = qml.AdamOptimizer(stepsize=0.1)
params = np.zeros(10, requires_grad=True)

for i in range(100):
    params, energy = opt.step_and_cost(vqe_circuit, params)
    print(f"Step {i}: Energy = {energy:.6f} Ha")
```

### Alternar Entre Dispositivos

```python
# Mesmo circuito, diferentes backends
circuit_def = lambda dev: qml.qnode(dev)(circuit_function)

# Testar em simulador
dev_sim = qml.device('default.qubit', wires=4)
result_sim = circuit_def(dev_sim)(params)

# Executar em hardware quântico
dev_hw = qml.device('qiskit.ibmq', wires=4, backend='ibmq_manila')
result_hw = circuit_def(dev_hw)(params)
```

## Documentação Detalhada

Para cobertura abrangente de tópicos específicos, consulte os arquivos de referência:

- **Primeiros passos**: `references/getting_started.md` - Instalação, conceitos básicos, primeiros passos
- **Circuitos quânticos**: `references/quantum_circuits.md` - Portas, medições, padrões de circuito
- **ML quântico**: `references/quantum_ml.md` - Modelos híbridos, integração de frameworks, QNNs
- **Química quântica**: `references/quantum_chemistry.md` - VQE, Hamiltonianos moleculares, fluxos de química
- **Dispositivos**: `references/devices_backends.md` - Simuladores, plugins de hardware, configuração de dispositivos
- **Otimização**: `references/optimization.md` - Otimizadores, gradientes, algoritmos variacionais
- **Avançado**: `references/advanced_features.md` - Templates, transformações, compilação JIT, ruído

## Melhores Práticas

1. **Comece com simuladores** - Teste em `default.qubit` antes de implantar em hardware
2. **Use parameter-shift para hardware** - Retropropagação funciona apenas em simuladores
3. **Escolha codificações apropriadas** - Combine codificação de dados com estrutura do problema
4. **Inicialize com cuidado** - Use pequenos valores aleatórios para evitar planaltos áridos
5. **Monitore gradientes** - Verifique se há gradientes desaparecendo em circuitos profundos
6. **Cache de dispositivos** - Reutilize objetos de dispositivo para reduzir sobrecarga de inicialização
7. **Analise circuitos** - Use `qml.specs()` para analisar complexidade do circuito
8. **Teste localmente** - Valide em simuladores antes de enviar para hardware
9. **Use templates** - Aproveite templates integrados para padrões de circuito comuns
10. **Compile quando possível** - Use Catalyst JIT para código crítico de desempenho

## Recursos

- Documentação oficial: https://docs.pennylane.ai
- Codebook (tutoriais): https://pennylane.ai/codebook
- Demonstrações QML: https://pennylane.ai/qml/demonstrations
- Fórum da comunidade: https://discuss.pennylane.ai
- GitHub: https://github.com/PennyLaneAI/pennylane