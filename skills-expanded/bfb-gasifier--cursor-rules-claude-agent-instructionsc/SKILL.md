---
description: BFB 气化炉项目 Agent 主规则，强制读取并遵循 docs/CLAUDE.md 中的所有开发约定
alwaysApply: true
---

# Agent 强制指引：读取 docs/CLAUDE.md

**在本项目中每次开始任务前，必须先阅读 `docs/CLAUDE.md`**，然后严格遵守其中所有规定。

## 不可违反的核心硬约束（快速参考）

### 单位制
- 全程 SI：Pa, K, m, mol, kg, s
- 唯一例外：R8 WGSR 方程内部将 Pa 换算为 atm，外部接口仍传 Pa

### Arrhenius 形式
- **只能**调用 `src/kinetics/arrhenius.py` 中定义的工厂函数
- R1–R4 用 `k_hobbs`；标准形式用 `k_standard`；R7 用 `k_jensen_r7`
- ❌ 禁止在其他文件中直接写 `k = A * exp(-E/RT)`

### 关键常数（不得硬编码在各函数内）
```python
Rg = 8.314      # J/(mol·K)
g  = 9.81       # m/s²
P0 = 101325.0   # Pa
n_b = 2.7       # Hilligardt 气体交换因子
```

### 其他禁止事项
- ❌ 禁止 R8 中直接用 Pa 代入压力项
- ❌ 禁止假设 Boudouard k_b/k_c 指数为负
- ❌ 禁止使用常数 `n_RZ = 4.65`，必须按 Re_s 分段计算
- ❌ 禁止忽略 R5 悬浮相中的 `C_H2O^0.5` 项
- ❌ 禁止添加 logging、设计模式、抽象基类

### 开发顺序
严格按 `docs/CLAUDE.md` 中 Phase 1→6 的顺序推进，不得跳步。

### 方程注释
每个函数 docstring 必须注明方程编号，例如：
```python
"""
Source: specs/02_hydrodynamics.md §2.1, Hamel (1999) Eq.4.4
"""
```
