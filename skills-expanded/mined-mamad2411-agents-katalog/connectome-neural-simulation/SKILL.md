---
name: connectome-neural-simulation
description: Biological connectome modeling, spiking neural network (SNN) simulation, Leaky Integrate-and-Fire (LIF) dynamics, neuromodulatory reward loops, and sensorimotor embodiment (e.g. Drosophila MaleCNS v1.0, StonkFly trading, Minecraft bots, robotics).
version: 1.0.0
author: AI Agent Vault
category: neuromorphic-ai
tags:
  - connectomics
  - spiking-neural-networks
  - drosophila
  - leaky-integrate-and-fire
  - embodiment
  - brain-simulation
  - stonkfly
  - sensorimotor
---

# Connectome Neural Simulation

## Purpose
This skill provides comprehensive architectural patterns, mathematical formulations, and engineering workflows for taking structural biological connectomes (such as the Google Research / HHMI Janelia adult fruit fly *MaleCNS v1.0* or *FlyWire* 166,691-neuron map) and compiling them into executable, interactive dynamical simulations in code, browsers, games, or robotic environments.

---

## When to Use
- Implementing or querying mapped biological connectomes (*Drosophila melanogaster*, *C. elegans*, rodent cortical columns).
- Building Spiking Neural Networks (SNNs) using Leaky Integrate-and-Fire (LIF), Izhikevich, or Hodgkin-Huxley equations.
- Constructing visual, olfactory, or tactile sensory encoder pipelines to map external inputs (e.g. candlestick charts, game voxels, camera streams) into photoreceptor or sensory neuron firing rates.
- Designing synthetic neuromodulatory reward/aversion systems (e.g. PAM dopamine clusters for positive reinforcement, PPL aversive signaling for loss avoidance).
- Connecting neural graph models to game engines (Minecraft, Doom, Sbox, Unity) or robotics control loops.

---

## Core Theoretical Architecture

### 1. The Connectome Graph Representation
A biological connectome is ingested as a directed weighted graph $G = (V, E, W)$:
- **Vertices ($V$)**: Neurons ($N \approx 166,700$ for *Drosophila* CNS), classified by cell class:
  - *Sensory Neurons*: Photoreceptors (R1-R8), Olfactory Receptor Neurons (ORNs), Mechanosensory hair cells.
  - *Interneurons*: Local interneurons (LNs), Projection Neurons (PNs), Kenyon Cells (KCs), Central Complex ring neurons.
  - *Neuromodulatory Neurons*: PAM (dopaminergic reward), PPL (aversive), serotonergic, octopaminergic.
  - *Descending Neurons (DNs)*: Command pathways propagating from the central brain down to the Ventral Nerve Cord (VNC).
  - *Motor Neurons (MNs)*: Direct innervation to flight steering muscles, leg Coxa/Femur/Tibia joints, and proboscis.
- **Edges ($E$) and Weights ($W$)**: Synaptic connections where weight $w_{ij}$ corresponds to the number of physical synapses / presynaptic T-bars identified via electron microscopy.
- **Polarity**: Synapse type based on neurotransmitter:
  - Acetylcholine (ACh): Fast excitatory ($\approx +w_{ij}$)
  - Glutamate (Glu): Inhibitory or excitatory depending on receptor
  - GABA: Fast inhibitory ($\approx -w_{ij}$)

---

### 2. Dynamical Simulation: Leaky Integrate-and-Fire (LIF)
To make the static graph execute in real time, integrate the membrane potential $V_i(t)$ of each neuron $i$:

$$\tau_m \frac{dV_i(t)}{dt} = -(V_i(t) - V_{\text{rest}}) + R_m \left[ \sum_{j \in \text{pre}(i)} w_{ji} S_j(t) + I_{\text{ext}, i}(t) \right]$$

**Spike Generation Condition**:
- If $V_i(t) \ge V_{\text{th}}$:
  1. Emit spike: $S_i(t) = 1$ (propagate to postsynaptic targets with synaptic delay $\Delta t$).
  2. Reset potential: $V_i(t) \leftarrow V_{\text{reset}}$.
  3. Enter refractory state: $V_i$ held clamped at $V_{\text{reset}}$ for duration $\tau_{\text{ref}}$ (typically 1–2 ms).

---

## End-to-End Implementation Workflows

### Pattern 1: Visual Sensory Transduction (e.g., StonkFly Financial Vision)
1. **Input Encoding**: Convert real-time 2D imagery (e.g. candlestick chart, game frame) into a low-resolution grid (e.g. $320 \times 180$ or $32 \times 32$ ommatidia).
2. **Photoreceptor Current Injection**:
   $$I_{\text{ext}, k}(t) = I_{\text{max}} \cdot \frac{\text{Luminance}(x_k, y_k)}{255}$$
3. **Lamina / Medulla Filter**: Feed $I_{\text{ext}}$ into R1–R6 photoreceptor nodes, activating downstream motion-detecting T4 and T5 cells.

```python
import numpy as np

def encode_visual_to_photoreceptors(image_gray, num_ommatidia=800):
    """
    Downsample an input grayscale frame and project onto hexagonal ommatidia.
    """
    resized = cv2.resize(image_gray, (40, 20), interpolation=cv2.INTER_AREA)
    normalized = resized.flatten().astype(np.float32) / 255.0
    # Map to external input currents (in microamperes)
    return normalized * 5.0  # 5.0 uA max injection
```

---

### Pattern 2: Neuromodulatory Plasticity & Reinforcement (PAM vs PPL)
1. **Dopaminergic Clusters**:
   - **PAM11 Neurons (Reward)**: Fire when the organism achieves a positive reward (e.g. food odor, profit in Bitcoin trading).
   - **PPL101 Neurons (Punishment)**: Fire upon negative valence (e.g. electric shock, heat, trading drawdown / fees).
2. **Three-Factor Synaptic Plasticity**:
   Update synaptic weights using eligibility traces $e_{ij}(t)$ gated by the global dopamine concentration $D(t)$:
   $$\frac{de_{ij}}{dt} = -\frac{e_{ij}}{\tau_e} + S_j^{\text{pre}}(t) \cdot S_i^{\text{post}}(t)$$
   $$\Delta w_{ij} = \eta \cdot D(t) \cdot e_{ij}(t)$$

---

### Pattern 3: Motor Decoding & Environment Actuation
1. Extract firing rates from identified Descending Neurons (DNs):
   - $r_{\text{DN\_left}}$ and $r_{\text{DN\_right}}$ (asymmetric steering)
   - $r_{\text{DN\_forward}}$ (locomotion thrust)
   - $r_{\text{DN\_stop}}$ (halting reflex)
2. In discrete environments (e.g., Trading or Game Input):
   $$\text{Action} = \arg\max \left( \sum_{k \in \text{Buy}} r_k(t), \sum_{k \in \text{Sell}} r_k(t), \sum_{k \in \text{Hold}} r_k(t) \right)$$
3. In continuous physics environments (e.g. Flight Simulator):
   $$\text{Thrust} = K_t \cdot r_{\text{flight\_CPG}}(t)$$
   $$\text{Yaw Rate} = K_y \cdot (r_{\text{DN\_R}}(t) - r_{\text{DN\_L}}(t))$$

---

## Best Practices & Watchouts
- **Avoid naive point-to-point explosion**: Do not simulate all 166,700 neurons on a single CPU thread with fine Euler steps; use vectorized matrix operations on GPU or aggregate neuropil sub-circuits for real-time web execution.
- **Neurotransmitter signs are critical**: Synapse count alone does not specify excitation vs inhibition. Ensure GABAergic and Glutamatergic inhibitory connections are accurately signed to prevent runaway epileptic seizure states.
- **Guard against over-interpreting "sentience"**: Without plasticity and active body chemistry, static connectome simulations are deterministic dynamical networks running insect-shaped routing architectures.
