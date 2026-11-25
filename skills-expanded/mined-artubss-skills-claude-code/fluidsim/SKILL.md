---
name: fluidsim
description: Framework para simulações de dinâmica de fluidos computacional usando Python. Use ao executar simulações de dinâmica de fluidos, incluindo equações de Navier-Stokes (2D/3D), equações de águas rasas, escoamentos estratificados, ou ao analisar turbulência, dinâmica de vórtices ou escoamentos geofísicos. Fornece métodos pseudoespectrais com FFT, suporte HPC e análise abrangente de saída.
---

# FluidSim

## Visão Geral

FluidSim é um framework Python orientado a objetos para simulações de dinâmica de fluidos computacional (CFD) de alto desempenho. Fornece solvers para equações em domínios periódicos usando métodos pseudoespectrais com FFT, entregando desempenho comparável ao Fortran/C++ mantendo a facilidade de uso do Python.

**Principais forças**:
- Múltiplos solvers: Navier-Stokes 2D/3D, águas rasas, escoamentos estratificados
- Alto desempenho: compilação Pythran/Transonic, paralelização MPI
- Fluxo completo: configuração de parâmetros, execução de simulação, análise de saída
- Análise interativa: pós-processamento e visualização baseados em Python

## Capacidades Principais

### 1. Instalação e Configuração

Instale fluidsim usando uv com flags de recursos apropriados:

```bash
# Instalação básica
uv pip install fluidsim

# Com suporte FFT (necessário para a maioria dos solvers)
uv pip install "fluidsim[fft]"

# Com MPI para computação paralela
uv pip install "fluidsim[fft,mpi]"
```

Defina variáveis de ambiente para diretórios de saída (opcional):

```bash
export FLUIDSIM_PATH=/path/to/simulation/outputs
export FLUIDDYN_PATH_SCRATCH=/path/to/working/directory
```

Nenhuma chave de API ou autenticação necessária.

Veja `references/installation.md` para instruções de instalação completas e configuração de ambiente.

### 2. Executando Simulações

O fluxo padrão consiste em cinco etapas:

**Etapa 1**: Importar solver
```python
from fluidsim.solvers.ns2d.solver import Simul
```

**Etapa 2**: Criar e configurar parâmetros
```python
params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 256
params.oper.Lx = params.oper.Ly = 2 * 3.14159
params.nu_2 = 1e-3
params.time_stepping.t_end = 10.0
params.init_fields.type = "noise"
```

**Etapa 3**: Instanciar simulação
```python
sim = Simul(params)
```

**Etapa 4**: Executar
```python
sim.time_stepping.start()
```

**Etapa 5**: Analisar resultados
```python
sim.output.phys_fields.plot("vorticity")
sim.output.spatial_means.plot()
```

Veja `references/simulation_workflow.md` para exemplos completos, reinicialização de simulações e deployment em clusters.

### 3. Solvers Disponíveis

Escolha o solver baseado no problema físico:

**Navier-Stokes 2D** (`ns2d`): turbulência 2D, dinâmica de vórtices
```python
from fluidsim.solvers.ns2d.solver import Simul
```

**Navier-Stokes 3D** (`ns3d`): turbulência 3D, escoamentos realistas
```python
from fluidsim.solvers.ns3d.solver import Simul
```

**Escoamentos estratificados** (`ns2d.strat`, `ns3d.strat`): escoamentos oceânicos/atmosféricos
```python
from fluidsim.solvers.ns2d.strat.solver import Simul
params.N = 1.0  # frequência de Brunt-Väisälä
```

**Águas rasas** (`sw1l`): escoamentos geofísicos, sistemas rotativos
```python
from fluidsim.solvers.sw1l.solver import Simul
params.f = 1.0  # parâmetro de Coriolis
```

Veja `references/solvers.md` para lista completa de solvers e orientação de seleção.

### 4. Configuração de Parâmetros

Os parâmetros são organizados hierarquicamente e acessados via notação de ponto:

**Domínio e resolução**:
```python
params.oper.nx = 256  # pontos de grade
params.oper.Lx = 2 * pi  # tamanho do domínio
```

**Parâmetros físicos**:
```python
params.nu_2 = 1e-3  # viscosidade
params.nu_4 = 0     # hiperviscosidade (opcional)
```

**Integração temporal**:
```python
params.time_stepping.t_end = 10.0
params.time_stepping.USE_CFL = True  # passo de tempo adaptativo
params.time_stepping.CFL = 0.5
```

**Condições iniciais**:
```python
params.init_fields.type = "noise"  # ou "dipole", "vortex", "from_file", "in_script"
```

**Configurações de saída**:
```python
params.output.periods_save.phys_fields = 1.0  # salvar a cada 1.0 unidades de tempo
params.output.periods_save.spectra = 0.5
params.output.periods_save.spatial_means = 0.1
```

O objeto Parameters levanta `AttributeError` para erros de digitação, prevenindo erros silenciosos de configuração.

Veja `references/parameters.md` para documentação de parâmetros abrangente.

### 5. Saída e Análise

FluidSim produz múltiplos tipos de saída automaticamente salvos durante a simulação:

**Campos físicos**: Velocidade, vorticidade em formato HDF5
```python
sim.output.phys_fields.plot("vorticity")
sim.output.phys_fields.plot("vx")
```

**Médias espaciais**: Séries temporais de quantidades volume-média
```python
sim.output.spatial_means.plot()
```

**Espectros**: Espectros de energia e enstrofia
```python
sim.output.spectra.plot1d()
sim.output.spectra.plot2d()
```

**Carregar simulações anteriores**:
```python
from fluidsim import load_sim_for_plot
sim = load_sim_for_plot("simulation_dir")
sim.output.phys_fields.plot()
```

**Visualização avançada**: Abra arquivos `.h5` em ParaView ou VisIt para visualização 3D.

Veja `references/output_analysis.md` para fluxos de análise detalhados, análise de estudos paramétricos e exportação de dados.

### 6. Recursos Avançados

**Forçamento customizado**: Manter turbulência ou dirigir dinâmicas específicas
```python
params.forcing.enable = True
params.forcing.type = "tcrandom"  # forçamento aleatório correlacionado no tempo
params.forcing.forcing_rate = 1.0
```

**Condições iniciais customizadas**: Definir campos em script
```python
params.init_fields.type = "in_script"
sim = Simul(params)
X, Y = sim.oper.get_XY_loc()
vx = sim.state.state_phys.get_var("vx")
vx[:] = sin(X) * cos(Y)
sim.time_stepping.start()
```

**Paralelização MPI**: Executar em múltiplos processadores
```bash
mpirun -np 8 python simulation_script.py
```

**Estudos paramétricos**: Executar múltiplas simulações com parâmetros diferentes
```python
for nu in [1e-3, 5e-4, 1e-4]:
    params = Simul.create_default_params()
    params.nu_2 = nu
    params.output.sub_directory = f"nu{nu}"
    sim = Simul(params)
    sim.time_stepping.start()
```

Veja `references/advanced_features.md` para tipos de forçamento, solvers customizados, submissão em clusters e otimização de desempenho.

## Casos de Uso Comuns

### Estudo de Turbulência 2D

```python
from fluidsim.solvers.ns2d.solver import Simul
from math import pi

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 512
params.oper.Lx = params.oper.Ly = 2 * pi
params.nu_2 = 1e-4
params.time_stepping.t_end = 50.0
params.time_stepping.USE_CFL = True
params.init_fields.type = "noise"
params.output.periods_save.phys_fields = 5.0
params.output.periods_save.spectra = 1.0

sim = Simul(params)
sim.time_stepping.start()

# Analisar cascata de energia
sim.output.spectra.plot1d(tmin=30.0, tmax=50.0)
```

### Simulação de Escoamento Estratificado

```python
from fluidsim.solvers.ns2d.strat.solver import Simul

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 256
params.N = 2.0  # força de estratificação
params.nu_2 = 5e-4
params.time_stepping.t_end = 20.0

# Inicializar com camada densa
params.init_fields.type = "in_script"
sim = Simul(params)
X, Y = sim.oper.get_XY_loc()
b = sim.state.state_phys.get_var("b")
b[:] = exp(-((X - 3.14)**2 + (Y - 3.14)**2) / 0.5)
sim.state.statephys_from_statespect()

sim.time_stepping.start()
sim.output.phys_fields.plot("b")
```

### Simulação 3D de Alta Resolução com MPI

```python
from fluidsim.solvers.ns3d.solver import Simul

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = params.oper.nz = 512
params.nu_2 = 1e-5
params.time_stepping.t_end = 10.0
params.init_fields.type = "noise"

sim = Simul(params)
sim.time_stepping.start()
```

Execute com:
```bash
mpirun -np 64 python script.py
```

### Validação de Vórtice de Taylor-Green

```python
from fluidsim.solvers.ns2d.solver import Simul
import numpy as np
from math import pi

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 128
params.oper.Lx = params.oper.Ly = 2 * pi
params.nu_2 = 1e-3
params.time_stepping.t_end = 10.0
params.init_fields.type = "in_script"

sim = Simul(params)
X, Y = sim.oper.get_XY_loc()
vx = sim.state.state_phys.get_var("vx")
vy = sim.state.state_phys.get_var("vy")
vx[:] = np.sin(X) * np.cos(Y)
vy[:] = -np.cos(X) * np.sin(Y)
sim.state.statephys_from_statespect()

sim.time_stepping.start()

# Validar decaimento de energia
df = sim.output.spatial_means.load()
# Comparar com solução analítica
```

## Referência Rápida

**Importar solver**: `from fluidsim.solvers.ns2d.solver import Simul`

**Criar parâmetros**: `params = Simul.create_default_params()`

**Definir resolução**: `params.oper.nx = params.oper.ny = 256`

**Definir viscosidade**: `params.nu_2 = 1e-3`

**Definir tempo final**: `params.time_stepping.t_end = 10.0`

**Executar simulação**: `sim = Simul(params); sim.time_stepping.start()`

**Plotar resultados**: `sim.output.phys_fields.plot("vorticity")`

**Carregar simulação**: `sim = load_sim_for_plot("path/to/sim")`

## Recursos

**Documentação**: https://fluidsim.readthedocs.io/

**Arquivos de referência**:
- `references/installation.md`: Instruções de instalação completas
- `references/solvers.md`: Solvers disponíveis e guia de seleção
- `references/simulation_workflow.md`: Exemplos de fluxo detalhados
- `references/parameters.md`: Documentação abrangente de parâmetros
- `references/output_analysis.md`: Tipos de saída e métodos de análise
- `references/advanced_features.md`: Forçamento, MPI, estudos paramétricos, solvers customizados