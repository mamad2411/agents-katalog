---
name: optimizing-attention-flash
description: Otimiza atenção em transformers com Flash Attention para ganho de 2-4x em velocidade e redução de 10-20x em memória. Use ao treinar/executar transformers com sequências longas (>512 tokens), ao encontrar problemas de memória GPU com atenção, ou quando precisa de inferência mais rápida. Suporta SDPA nativo do PyTorch, biblioteca flash-attn, H100 FP8 e sliding window attention.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Optimization, Flash Attention, Attention Optimization, Memory Efficiency, Speed Optimization, Long Context, PyTorch, SDPA, H100, FP8, Transformers]
dependencies: [flash-attn, torch, transformers]
---

# Flash Attention - Atenção Rápida e Eficiente em Memória

## Início rápido

Flash Attention oferece ganho de 2-4x em velocidade e redução de 10-20x em memória para atenção em transformers através de tiling consciente de I/O e recomputação.

**PyTorch nativo (mais fácil, PyTorch 2.2+)**:
```python
import torch
import torch.nn.functional as F

q = torch.randn(2, 8, 512, 64, device='cuda', dtype=torch.float16)  # [batch, heads, seq, dim]
k = torch.randn(2, 8, 512, 64, device='cuda', dtype=torch.float16)
v = torch.randn(2, 8, 512, 64, device='cuda', dtype=torch.float16)

# Usa automaticamente Flash Attention se disponível
out = F.scaled_dot_product_attention(q, k, v)
```

**Biblioteca flash-attn (mais recursos)**:
```bash
pip install flash-attn --no-build-isolation
```

```python
from flash_attn import flash_attn_func

# q, k, v: [batch, seqlen, nheads, headdim]
out = flash_attn_func(q, k, v, dropout_p=0.0, causal=True)
```

## Fluxos de trabalho comuns

### Fluxo 1: Habilitar em modelo PyTorch existente

Copie esta lista de verificação:

```
Integração Flash Attention:
- [ ] Passo 1: Verificar versão do PyTorch (≥2.2)
- [ ] Passo 2: Habilitar backend Flash Attention
- [ ] Passo 3: Verificar ganho de velocidade com profiling
- [ ] Passo 4: Testar se acurácia corresponde ao baseline
```

**Passo 1: Verificar versão do PyTorch**

```bash
python -c "import torch; print(torch.__version__)"
# Deve ser ≥2.2.0
```

Se <2.2, atualize:
```bash
pip install --upgrade torch
```

**Passo 2: Habilitar backend Flash Attention**

Substitua atenção padrão:
```python
# Antes (atenção padrão)
attn_weights = torch.softmax(q @ k.transpose(-2, -1) / math.sqrt(d_k), dim=-1)
out = attn_weights @ v

# Depois (Flash Attention)
import torch.nn.functional as F
out = F.scaled_dot_product_attention(q, k, v, attn_mask=mask)
```

Force backend Flash Attention:
```python
with torch.backends.cuda.sdp_kernel(
    enable_flash=True,
    enable_math=False,
    enable_mem_efficient=False
):
    out = F.scaled_dot_product_attention(q, k, v)
```

**Passo 3: Verificar ganho de velocidade com profiling**

```python
import torch.utils.benchmark as benchmark

def test_attention(use_flash):
    q, k, v = [torch.randn(2, 8, 2048, 64, device='cuda', dtype=torch.float16) for _ in range(3)]

    if use_flash:
        with torch.backends.cuda.sdp_kernel(enable_flash=True):
            return F.scaled_dot_product_attention(q, k, v)
    else:
        attn = (q @ k.transpose(-2, -1) / 8.0).softmax(dim=-1)
        return attn @ v

# Benchmark
t_flash = benchmark.Timer(stmt='test_attention(True)', globals=globals())
t_standard = benchmark.Timer(stmt='test_attention(False)', globals=globals())

print(f"Flash: {t_flash.timeit(100).mean:.3f}s")
print(f"Standard: {t_standard.timeit(100).mean:.3f}s")
```

Esperado: ganho de 2-4x para sequências >512 tokens.

**Passo 4: Testar se acurácia corresponde ao baseline**

```python
# Comparar saídas
q, k, v = [torch.randn(1, 8, 512, 64, device='cuda', dtype=torch.float16) for _ in range(3)]

# Flash Attention
out_flash = F.scaled_dot_product_attention(q, k, v)

# Atenção padrão
attn_weights = torch.softmax(q @ k.transpose(-2, -1) / 8.0, dim=-1)
out_standard = attn_weights @ v

# Verificar diferença
diff = (out_flash - out_standard).abs().max()
print(f"Diferença máxima: {diff:.6f}")
# Deve ser <1e-3 para float16
```

### Fluxo 2: Usar biblioteca flash-attn para recursos avançados

Para atenção multi-query, sliding window, ou FP8 em H100.

Copie esta lista de verificação:

```
Configuração Biblioteca flash-attn:
- [ ] Passo 1: Instalar biblioteca flash-attn
- [ ] Passo 2: Modificar código de atenção
- [ ] Passo 3: Habilitar recursos avançados
- [ ] Passo 4: Fazer benchmark de desempenho
```

**Passo 1: Instalar biblioteca flash-attn**

```bash
# GPUs NVIDIA (CUDA 12.0+)
pip install flash-attn --no-build-isolation

# Verificar instalação
python -c "from flash_attn import flash_attn_func; print('Success')"
```

**Passo 2: Modificar código de atenção**

```python
from flash_attn import flash_attn_func

# Entrada: [batch_size, seq_len, num_heads, head_dim]
# Transponha de [batch, heads, seq, dim] se necessário
q = q.transpose(1, 2)  # [batch, seq, heads, dim]
k = k.transpose(1, 2)
v = v.transpose(1, 2)

out = flash_attn_func(
    q, k, v,
    dropout_p=0.1,
    causal=True,  # Para modelos autorregressivos
    window_size=(-1, -1),  # Sem sliding window
    softmax_scale=None  # Auto-escala
)

out = out.transpose(1, 2)  # Voltar para [batch, heads, seq, dim]
```

**Passo 3: Habilitar recursos avançados**

Atenção multi-query (K/V compartilhados entre cabeças):
```python
from flash_attn import flash_attn_func

# q: [batch, seq, num_q_heads, dim]
# k, v: [batch, seq, num_kv_heads, dim]  # Menos cabeças KV
out = flash_attn_func(q, k, v)  # Lida automaticamente com MQA
```

Sliding window attention (atenção local):
```python
# Só atender janela de 256 tokens antes/depois
out = flash_attn_func(
    q, k, v,
    window_size=(256, 256),  # (esquerda, direita) janela
    causal=True
)
```

**Passo 4: Fazer benchmark de desempenho**

```python
import torch
from flash_attn import flash_attn_func
import time

q, k, v = [torch.randn(4, 4096, 32, 64, device='cuda', dtype=torch.float16) for _ in range(3)]

# Aquecimento
for _ in range(10):
    _ = flash_attn_func(q, k, v)

# Benchmark
torch.cuda.synchronize()
start = time.time()
for _ in range(100):
    out = flash_attn_func(q, k, v)
    torch.cuda.synchronize()
end = time.time()

print(f"Tempo por iteração: {(end-start)/100*1000:.2f}ms")
print(f"Memória alocada: {torch.cuda.max_memory_allocated()/1e9:.2f}GB")
```

### Fluxo 3: Otimização FP8 em H100 (FlashAttention-3)

Para desempenho máximo em GPUs H100.

```
Configuração FP8:
- [ ] Passo 1: Verificar GPU H100 disponível
- [ ] Passo 2: Instalar flash-attn com suporte FP8
- [ ] Passo 3: Converter entradas para FP8
- [ ] Passo 4: Executar com atenção FP8
```

**Passo 1: Verificar GPU H100**

```bash
nvidia-smi --query-gpu=name --format=csv
# Deve mostrar "H100" ou "H800"
```

**Passo 2: Instalar flash-attn com suporte FP8**

```bash
pip install flash-attn --no-build-isolation
# Suporte FP8 incluído para H100
```

**Passo 3: Converter entradas para FP8**

```python
import torch

q = torch.randn(2, 4096, 32, 64, device='cuda', dtype=torch.float16)
k = torch.randn(2, 4096, 32, 64, device='cuda', dtype=torch.float16)
v = torch.randn(2, 4096, 32, 64, device='cuda', dtype=torch.float16)

# Converter para float8_e4m3 (FP8)
q_fp8 = q.to(torch.float8_e4m3fn)
k_fp8 = k.to(torch.float8_e4m3fn)
v_fp8 = v.to(torch.float8_e4m3fn)
```

**Passo 4: Executar com atenção FP8**

```python
from flash_attn import flash_attn_func

# FlashAttention-3 usa automaticamente kernels FP8 em H100
out = flash_attn_func(q_fp8, k_fp8, v_fp8)
# Resultado: ~1.2 PFLOPS, 1.5-2x mais rápido que FP16
```

## Quando usar versus alternativas

**Use Flash Attention quando:**
- Treinar transformers com sequências >512 tokens
- Executar inferência com contexto longo (>2K tokens)
- GPU com memória limitada (OOM com atenção padrão)
- Precisa de ganho de 2-4x sem perda de acurácia
- Usando PyTorch 2.2+ ou consegue instalar flash-attn

**Use alternativas em vez disso:**
- **Atenção padrão**: Sequências <256 tokens (overhead não vale a pena)
- **xFormers**: Precisa de mais variantes de atenção (não só velocidade)
- **Atenção eficiente em memória**: Inferência em CPU (Flash Attention precisa GPU)

## Problemas comuns

**Problema: ImportError: cannot import flash_attn**

Instale com flag no-build-isolation:
```bash
pip install flash-attn --no-build-isolation
```

Ou instale toolkit CUDA primeiro:
```bash
conda install cuda -c nvidia
pip install flash-attn --no-build-isolation
```

**Problema: Mais lento que esperado (sem ganho de velocidade)**

Os benefícios de Flash Attention aumentam com o comprimento da sequência:
- <512 tokens: Ganho mínimo (10-20%)
- 512-2K tokens: Ganho de 2-3x
- >2K tokens: Ganho de 3-4x

Verifique se o comprimento da sequência é suficiente.

**Problema: RuntimeError: CUDA error**

Verifique se GPU suporta Flash Attention:
```python
import torch
print(torch.cuda.get_device_capability())
# Deve ser ≥(7, 5) para Turing+
```

Flash Attention requer:
- Ampere (A100, A10): ✅ Suporte completo
- Turing (T4): ✅ Suportado
- Volta (V100): ❌ Não suportado

**Problema: Degradação de acurácia**

Verifique se dtype é float16 ou bfloat16 (não float32):
```python
q = q.to(torch.float16)  # Ou torch.bfloat16
```

Flash Attention usa float16/bfloat16 para velocidade. Float32 não é suportado.

## Tópicos avançados

**Integração com HuggingFace Transformers**: Veja [references/transformers-integration.md](references/transformers-integration.md) para habilitar Flash Attention em modelos BERT, GPT, Llama.

**Benchmarks de desempenho**: Veja [references/benchmarks.md](references/benchmarks.md) para comparações detalhadas de velocidade e memória entre GPUs e comprimentos de sequência.

**Detalhes do algoritmo**: Veja [references/algorithm.md](references/algorithm.md) para análise de estratégia de tiling, recomputação e complexidade de I/O.

**Recursos avançados**: Veja [references/advanced-features.md](references/advanced-features.md) para rotary embeddings, ALiBi, paged KV cache e máscaras de atenção customizadas.

## Requisitos de hardware

- **GPU**: NVIDIA Ampere+ (A100, A10, A30) ou AMD MI200+
- **VRAM**: Igual à atenção padrão (Flash Attention não aumenta memória)
- **CUDA**: 12.0+ (11.8 mínimo)
- **PyTorch**: 2.2+ para suporte nativo

**Não suportado**: V100 (Volta), inferência em CPU

## Recursos

- Paper: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness" (NeurIPS 2022)
- Paper: "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning" (ICLR 2024)
- Blog: https://tridao.me/blog/2024/flash3/
- GitHub: https://github.com/Dao-AILab/flash-attention
- PyTorch docs: https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html