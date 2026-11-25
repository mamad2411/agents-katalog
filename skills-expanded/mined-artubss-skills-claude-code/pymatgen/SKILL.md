---
name: pymatgen
description: "Kit de ferramentas para ciência de materiais. Estruturas cristalinas (CIF, POSCAR), diagramas de fase, estrutura de bandas, DOS, integração com Materials Project, conversão de formatos, para ciência computacional de materiais."
---

# Pymatgen - Python Materials Genomics

## Visão Geral

Pymatgen é uma biblioteca Python abrangente para análise de materiais que alimenta o Materials Project. Crie, analise e manipule estruturas cristalinas e moléculas, calcule diagramas de fase e propriedades termodinâmicas, analise estrutura eletrônica (estruturas de bandas, DOS), gere superfícies e interfaces, e acesse o banco de dados do Materials Project de materiais computados. Suporta 100+ formatos de arquivo de vários códigos computacionais.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:
- Trabalhar com estruturas cristalinas ou sistemas moleculares em ciência de materiais
- Converter entre formatos de arquivo de estrutura (CIF, POSCAR, XYZ, etc.)
- Analisar simetria, grupos espaciais ou ambientes de coordenação
- Calcular diagramas de fase ou avaliar estabilidade termodinâmica
- Analisar dados de estrutura eletrônica (band gaps, DOS, estruturas de bandas)
- Gerar superfícies, placas ou estudar interfaces
- Acessar o banco de dados do Materials Project programaticamente
- Configurar fluxos de trabalho computacionais de alto desempenho
- Analisar difusão, magnetismo ou propriedades mecânicas
- Trabalhar com VASP, Gaussian, Quantum ESPRESSO ou outros códigos computacionais

## Guia de Início Rápido

### Instalação

```bash
# Pymatgen básico
uv pip install pymatgen

# Com acesso à API do Materials Project
uv pip install pymatgen mp-api

# Dependências opcionais para funcionalidade estendida
uv pip install pymatgen[analysis]  # Ferramentas de análise adicionais
uv pip install pymatgen[vis]       # Ferramentas de visualização
```

### Operações Básicas de Estrutura

```python
from pymatgen.core import Structure, Lattice

# Ler estrutura de arquivo (detecção automática de formato)
struct = Structure.from_file("POSCAR")

# Criar estrutura do zero
lattice = Lattice.cubic(3.84)
struct = Structure(lattice, ["Si", "Si"], [[0,0,0], [0.25,0.25,0.25]])

# Escrever em formato diferente
struct.to(filename="structure.cif")

# Propriedades básicas
print(f"Fórmula: {struct.composition.reduced_formula}")
print(f"Grupo espacial: {struct.get_space_group_info()}")
print(f"Densidade: {struct.density:.2f} g/cm³")
```

### Integração com Materials Project

```bash
# Configurar chave de API
export MP_API_KEY="sua_chave_api_aqui"
```

```python
from mp_api.client import MPRester

with MPRester() as mpr:
    # Obter estrutura por ID de material
    struct = mpr.get_structure_by_material_id("mp-149")

    # Buscar materiais
    materials = mpr.materials.summary.search(
        formula="Fe2O3",
        energy_above_hull=(0, 0.05)
    )
```

## Capacidades Principais

### 1. Criação e Manipulação de Estrutura

Crie estruturas usando vários métodos e execute transformações.

**De arquivos:**
```python
# Detecção automática de formato
struct = Structure.from_file("structure.cif")
struct = Structure.from_file("POSCAR")
mol = Molecule.from_file("molecule.xyz")
```

**Do zero:**
```python
from pymatgen.core import Structure, Lattice

# Usando parâmetros de rede
lattice = Lattice.from_parameters(a=3.84, b=3.84, c=3.84,
                                  alpha=120, beta=90, gamma=60)
coords = [[0, 0, 0], [0.75, 0.5, 0.75]]
struct = Structure(lattice, ["Si", "Si"], coords)

# A partir do grupo espacial
struct = Structure.from_spacegroup(
    "Fm-3m",
    Lattice.cubic(3.5),
    ["Si"],
    [[0, 0, 0]]
)
```

**Transformações:**
```python
from pymatgen.transformations.standard_transformations import (
    SupercellTransformation,
    SubstitutionTransformation,
    PrimitiveCellTransformation
)

# Criar supercélula
trans = SupercellTransformation([[2,0,0],[0,2,0],[0,0,2]])
supercell = trans.apply_transformation(struct)

# Substituir elementos
trans = SubstitutionTransformation({"Fe": "Mn"})
new_struct = trans.apply_transformation(struct)

# Obter célula primitiva
trans = PrimitiveCellTransformation()
primitive = trans.apply_transformation(struct)
```

**Referência:** Consulte `references/core_classes.md` para documentação abrangente das classes Structure, Lattice, Molecule e relacionadas.

### 2. Conversão de Formato de Arquivo

Converta entre 100+ formatos de arquivo com detecção automática de formato.

**Usando métodos de conveniência:**
```python
# Ler qualquer formato
struct = Structure.from_file("input_file")

# Escrever em qualquer formato
struct.to(filename="output.cif")
struct.to(filename="POSCAR")
struct.to(filename="output.xyz")
```

**Usando o script de conversão:**
```bash
# Conversão de arquivo único
python scripts/structure_converter.py POSCAR structure.cif

# Conversão em lote
python scripts/structure_converter.py *.cif --output-dir ./poscar_files --format poscar
```

**Referência:** Consulte `references/io_formats.md` para documentação detalhada de todos os formatos suportados e integrações de código.

### 3. Análise de Estrutura e Simetria

Analise estruturas quanto a simetria, coordenação e outras propriedades.

**Análise de simetria:**
```python
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

sga = SpacegroupAnalyzer(struct)

# Obter informações de grupo espacial
print(f"Grupo espacial: {sga.get_space_group_symbol()}")
print(f"Número: {sga.get_space_group_number()}")
print(f"Sistema cristalino: {sga.get_crystal_system()}")

# Obter células convencionais/primitivas
conventional = sga.get_conventional_standard_structure()
primitive = sga.get_primitive_standard_structure()
```

**Ambiente de coordenação:**
```python
from pymatgen.analysis.local_env import CrystalNN

cnn = CrystalNN()
neighbors = cnn.get_nn_info(struct, n=0)  # Vizinhos do sítio 0

print(f"Número de coordenação: {len(neighbors)}")
for neighbor in neighbors:
    site = struct[neighbor['site_index']]
    print(f"  {site.species_string} em {neighbor['weight']:.3f} Å")
```

**Usando o script de análise:**
```bash
# Análise abrangente
python scripts/structure_analyzer.py POSCAR --symmetry --neighbors

# Exportar resultados
python scripts/structure_analyzer.py structure.cif --symmetry --export json
```

**Referência:** Consulte `references/analysis_modules.md` para documentação detalhada de todos os recursos de análise.

### 4. Diagramas de Fase e Termodinâmica

Construa diagramas de fase e analise estabilidade termodinâmica.

**Construção de diagrama de fase:**
```python
from mp_api.client import MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter

# Obter entradas do Materials Project
with MPRester() as mpr:
    entries = mpr.get_entries_in_chemsys("Li-Fe-O")

# Construir diagrama de fase
pd = PhaseDiagram(entries)

# Verificar estabilidade
from pymatgen.core import Composition
comp = Composition("LiFeO2")

# Encontrar entrada para composição
for entry in entries:
    if entry.composition.reduced_formula == comp.reduced_formula:
        e_above_hull = pd.get_e_above_hull(entry)
        print(f"Energia acima do casco convexo: {e_above_hull:.4f} eV/átomo")

        if e_above_hull > 0.001:
            # Obter decomposição
            decomp = pd.get_decomposition(comp)
            print("Decompõe em:", decomp)

# Plotar
plotter = PDPlotter(pd)
plotter.show()
```

**Usando o script de gerador de diagrama de fase:**
```bash
# Gerar diagrama de fase
python scripts/phase_diagram_generator.py Li-Fe-O --output li_fe_o.png

# Analisar composição específica
python scripts/phase_diagram_generator.py Li-Fe-O --analyze "LiFeO2" --show
```

**Referência:** Consulte `references/analysis_modules.md` (seção Diagramas de Fase) e `references/transformations_workflows.md` (Fluxo de trabalho 2) para exemplos detalhados.

### 5. Análise de Estrutura Eletrônica

Analise estruturas de bandas, densidade de estados e propriedades eletrônicas.

**Estrutura de bandas:**
```python
from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import BSPlotter

# Ler de cálculo VASP
vasprun = Vasprun("vasprun.xml")
bs = vasprun.get_band_structure()

# Analisar
band_gap = bs.get_band_gap()
print(f"Band gap: {band_gap['energy']:.3f} eV")
print(f"Direto: {band_gap['direct']}")
print(f"É metal: {bs.is_metal()}")

# Plotar
plotter = BSPlotter(bs)
plotter.save_plot("band_structure.png")
```

**Densidade de estados:**
```python
from pymatgen.electronic_structure.plotter import DosPlotter

dos = vasprun.complete_dos

# Obter DOS projetado em elemento
element_dos = dos.get_element_dos()
for element, element_dos_obj in element_dos.items():
    print(f"{element}: {element_dos_obj.get_gap():.3f} eV")

# Plotar
plotter = DosPlotter()
plotter.add_dos("DOS Total", dos)
plotter.show()
```

**Referência:** Consulte `references/analysis_modules.md` (seção Estrutura Eletrônica) e `references/io_formats.md` (seção VASP).

### 6. Análise de Superfície e Interface

Gere placas, analise superfícies e estude interfaces.

**Geração de placa:**
```python
from pymatgen.core.surface import SlabGenerator

# Gerar placas para índice de Miller específico
slabgen = SlabGenerator(
    struct,
    miller_index=(1, 1, 1),
    min_slab_size=10.0,      # Å
    min_vacuum_size=10.0,    # Å
    center_slab=True
)

slabs = slabgen.get_slabs()

# Escrever placas
for i, slab in enumerate(slabs):
    slab.to(filename=f"slab_{i}.cif")
```

**Construção de forma de Wulff:**
```python
from pymatgen.analysis.wulff import WulffShape

# Definir energias de superfície
surface_energies = {
    (1, 0, 0): 1.0,
    (1, 1, 0): 1.1,
    (1, 1, 1): 0.9,
}

wulff = WulffShape(struct.lattice, surface_energies)
print(f"Área de superfície: {wulff.surface_area:.2f} Ų")
print(f"Volume: {wulff.volume:.2f} ų")

wulff.show()
```

**Busca de sítio de adsorção:**
```python
from pymatgen.analysis.adsorption import AdsorbateSiteFinder
from pymatgen.core import Molecule

asf = AdsorbateSiteFinder(slab)

# Encontrar sítios
ads_sites = asf.find_adsorption_sites()
print(f"Sítios on-top: {len(ads_sites['ontop'])}")
print(f"Sítios de ponte: {len(ads_sites['bridge'])}")
print(f"Sítios vazios: {len(ads_sites['hollow'])}")

# Adicionar adsorvato
adsorbate = Molecule("O", [[0, 0, 0]])
ads_struct = asf.add_adsorbate(adsorbate, ads_sites["ontop"][0])
```

**Referência:** Consulte `references/analysis_modules.md` (seção Superfície e Interface) e `references/transformations_workflows.md` (Fluxos de trabalho 3 e 9).

### 7. Acesso ao Banco de Dados do Materials Project

Acesse programaticamente o banco de dados do Materials Project.

**Configuração:**
1. Obtenha chave de API em https://next-gen.materialsproject.org/
2. Defina variável de ambiente: `export MP_API_KEY="sua_chave_aqui"`

**Busca e recuperação:**
```python
from mp_api.client import MPRester

with MPRester() as mpr:
    # Buscar por fórmula
    materials = mpr.materials.summary.search(formula="Fe2O3")

    # Buscar por sistema químico
    materials = mpr.materials.summary.search(chemsys="Li-Fe-O")

    # Filtrar por propriedades
    materials = mpr.materials.summary.search(
        chemsys="Li-Fe-O",
        energy_above_hull=(0, 0.05),  # Estável/metaestável
        band_gap=(1.0, 3.0)            # Semicondutor
    )

    # Obter estrutura
    struct = mpr.get_structure_by_material_id("mp-149")

    # Obter estrutura de bandas
    bs = mpr.get_bandstructure_by_material_id("mp-149")

    # Obter entradas para diagrama de fase
    entries = mpr.get_entries_in_chemsys("Li-Fe-O")
```

**Referência:** Consulte `references/materials_project_api.md` para documentação abrangente de API e exemplos.

### 8. Configuração de Fluxo de Trabalho Computacional

Configure cálculos para vários códigos de estrutura eletrônica.

**Geração de entrada VASP:**
```python
from pymatgen.io.vasp.sets import MPRelaxSet, MPStaticSet, MPNonSCFSet

# Relaxação
relax = MPRelaxSet(struct)
relax.write_input("./relax_calc")

# Cálculo estático
static = MPStaticSet(struct)
static.write_input("./static_calc")

# Estrutura de bandas (não auto-consistente)
nscf = MPNonSCFSet(struct, mode="line")
nscf.write_input("./bandstructure_calc")

# Parâmetros personalizados
custom = MPRelaxSet(struct, user_incar_settings={"ENCUT": 600})
custom.write_input("./custom_calc")
```

**Outros códigos:**
```python
# Gaussian
from pymatgen.io.gaussian import GaussianInput

gin = GaussianInput(
    mol,
    functional="B3LYP",
    basis_set="6-31G(d)",
    route_parameters={"Opt": None}
)
gin.write_file("input.gjf")

# Quantum ESPRESSO
from pymatgen.io.pwscf import PWInput

pwin = PWInput(struct, control={"calculation": "scf"})
pwin.write_file("pw.in")
```

**Referência:** Consulte `references/io_formats.md` (seção I/O de Código de Estrutura Eletrônica) e `references/transformations_workflows.md` para exemplos de fluxo de trabalho.

### 9. Análise Avançada

**Padrões de difração:**
```python
from pymatgen.analysis.diffraction.xrd import XRDCalculator

xrd = XRDCalculator()
pattern = xrd.get_pattern(struct)

# Obter picos
for peak in pattern.hkls:
    print(f"2θ = {peak['2theta']:.2f}°, hkl = {peak['hkl']}")

pattern.plot()
```

**Propriedades elásticas:**
```python
from pymatgen.analysis.elasticity import ElasticTensor

# A partir da matriz de tensor elástico
elastic_tensor = ElasticTensor.from_voigt(matrix)

print(f"Módulo de volume: {elastic_tensor.k_voigt:.1f} GPa")
print(f"Módulo de cisalhamento: {elastic_tensor.g_voigt:.1f} GPa")
print(f"Módulo de Young: {elastic_tensor.y_mod:.1f} GPa")
```

**Ordem magnética:**
```python
from pymatgen.transformations.advanced_transformations import MagOrderingTransformation

# Enumerar ordenações magnéticas
trans = MagOrderingTransformation({"Fe": 5.0})
mag_structs = trans.apply_transformation(struct, return_ranked_list=True)

# Obter estrutura magnética de menor energia
lowest_energy_struct = mag_structs[0]['structure']
```

**Referência:** Consulte `references/analysis_modules.md` para documentação abrangente do módulo de análise.

## Recursos Inclusos

### Scripts (`scripts/`)

Scripts Python executáveis para tarefas comuns:

- **`structure_converter.py`**: Converter entre formatos de arquivo de estrutura
  - Suporta conversão em lote e detecção automática de formato
  - Uso: `python scripts/structure_converter.py POSCAR structure.cif`

- **`structure_analyzer.py`**: Análise abrangente de estrutura
  - Simetria, coordenação, parâmetros de rede, matriz de distância
  - Uso: `python scripts/structure_analyzer.py structure.cif --symmetry --neighbors`

- **`phase_diagram_generator.py`**: Gerar diagramas de fase do Materials Project
  - Análise de estabilidade e propriedades termodinâmicas
  - Uso: `python scripts/phase_diagram_generator.py Li-Fe-O --analyze "LiFeO2"`

Todos os scripts incluem ajuda detalhada: `python scripts/script_name.py --help`

### Referências (`references/`)

Documentação abrangente carregada no contexto conforme necessário:

- **`core_classes.md`**: Classes Element, Structure, Lattice, Molecule, Composition
- **`io_formats.md`**: Suporte de formato de arquivo e integração de código (VASP, Gaussian, etc.)
- **`analysis_modules.md`**: Diagramas de fase, superfícies, estrutura eletrônica, simetria
- **`materials_project_api.md`**: Guia completo de API do Materials Project
- **`transformations_workflows.md`**: Framework de transformações e fluxos de trabalho comuns

Carregue referências quando informações detalhadas são necessárias sobre módulos ou fluxos de trabalho específicos.

## Fluxos de Trabalho Comuns

### Geração de Estrutura de Alto Desempenho

```python
from pymatgen.transformations.standard_transformations import SubstitutionTransformation
from pymatgen.io.vasp.sets import MPRelaxSet

# Gerar estruturas dopadas
base_struct = Structure.from_file("POSCAR")
dopants = ["Mn", "Co", "Ni", "Cu"]

for dopant in dopants:
    trans = SubstitutionTransformation({"Fe": dopant})
    doped_struct = trans.apply_transformation(base_struct)

    # Gerar entradas VASP
    vasp_input = MPRelaxSet(doped_struct)
    vasp_input.write_input(f"./calcs/Fe_{dopant}")
```

### Fluxo de Trabalho de Cálculo de Estrutura de Bandas

```python
# 1. Relaxação
relax = MPRelaxSet(struct)
relax.write_input("./1_relax")

# 2. Estático (após relaxação)
relaxed = Structure.from_file("1_relax/CONTCAR")
static = MPStaticSet(relaxed)
static.write_input("./2_static")

# 3. Estrutura de bandas (não auto-consistente)
nscf = MPNonSCFSet(relaxed, mode="line")
nscf.write_input("./3_bandstructure")

# 4. Análise
from pymatgen.io.vasp import Vasprun
vasprun = Vasprun("3_bandstructure/vasprun.xml")
bs = vasprun.get_band_structure()
bs.get_band_gap()
```

### Cálculo de Energia de Superfície

```python
# 1. Obter energia em massa
bulk_vasprun = Vasprun("bulk/vasprun.xml")
bulk_E_per_atom = bulk_vasprun.final_energy / len(bulk)

# 2. Gerar e calcular placas
slabgen = SlabGenerator(bulk, (1,1,1), 10, 15)
slab = slabgen.get_slabs()[0]

MPRelaxSet(slab).write_input("./slab_calc")

# 3. Calcular energia de superfície (após cálculo)
slab_vasprun = Vasprun("slab_calc/vasprun.xml")
E_surf = (slab_vasprun.final_energy - len(slab) * bulk_E_per_atom) / (2 * slab.surface_area)
E_surf *= 16.021766  # Converter eV/Ų para J/m²
```

**Mais fluxos de trabalho:** Consulte `references/transformations_workflows.md` para 10 exemplos de fluxo de trabalho detalhados.

## Melhores Práticas

### Manipulação de Estrutura

1. **Use detecção automática de formato**: `Structure.from_file()` manipula a maioria dos formatos
2. **Prefira estruturas imutáveis**: Use `IStructure` quando a estrutura não deve mudar
3. **Verifique simetria**: Use `SpacegroupAnalyzer` para reduzir à célula primitiva
4. **Valide estruturas**: Verifique átomos sobrepostos ou comprimentos de ligação irrealistas

### I/O de Arquivo

1. **Use métodos de conveniência**: `from_file()` e `to()` são preferidos
2. **Especifique formatos explicitamente**: Quando a detecção automática falhar
3. **Trate exceções**: Encapsule I/O de arquivo em blocos try-except
4. **Use serialização**: `as_dict()`/`from_dict()` para armazenamento seguro em versão

### API do Materials Project

1. **Use gerenciador de contexto**: Sempre use `with MPRester() as mpr:`
2. **Consultas em lote**: Solicite vários itens de uma vez
3. **Resultados em cache**: Salve dados usados com frequência localmente
4. **Filtre efetivamente**: Use filtros de propriedade para reduzir transferência de dados

### Fluxos de Trabalho Computacionais

1. **Use conjuntos de entrada**: Prefira `MPRelaxSet`, `MPStaticSet` sobre INCAR manual
2. **Verifique convergência**: Sempre verifique se os cálculos convergiram
3. **Acompanhe transformações**: Use `TransformedStructure` para rastreabilidade
4. **Organize cálculos**: Use estruturas de diretório claras

### Desempenho

1. **Reduza simetria**: Use células primitivas quando possível
2. **Limite buscas de vizinhos**: Especifique raios de corte razoáveis
3. **Use métodos apropriados**: Diferentes ferramentas de análise têm diferentes compensações de velocidade/precisão
4. **Paralelizar quando possível**: Muitas operações podem ser paralelizadas

## Unidades e Convenções

Pymatgen usa unidades atômicas em todo:
- **Comprimentos**: Angstroms (Å)
- **Energias**: Electronvolts (eV)
- **Ângulos**: Graus (°)
- **Momentos magnéticos**: Magnetons de Bohr (μB)
- **Tempo**: Femtosegundos (fs)

Converta unidades usando `pymatgen.core.units` quando necessário.

## Integração com Outras Ferramentas

Pymatgen se integra perfeitamente com:
- **ASE** (Atomic Simulation Environment)
- **Phonopy** (cálculos de fônons)
- **BoltzTraP** (propriedades de transporte)
- **Atomate/Fireworks** (gerenciamento de fluxo de trabalho)
- **AiiDA** (rastreamento de rastreabilidade)
- **Zeo++** (análise de poros)
- **OpenBabel** (conversão de moléculas)

## Solução de Problemas

**Erros de importação**: Instale dependências ausentes
```bash
uv pip install pymatgen[analysis,vis]
```

**Chave de API não encontrada**: Defina variável de ambiente MP_API_KEY
```bash
export MP_API_KEY="sua_chave_aqui"
```

**Falhas ao ler estrutura**: Verifique formato e sintaxe do arquivo
```python
# Tente especificação de formato explícita
struct = Structure.from_file("file.txt", fmt="cif")
```

**Análise de simetria falha**: A estrutura pode ter problemas de precisão numérica
```python
# Aumentar tolerância
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
sga = SpacegroupAnalyzer(struct, symprec=0.1)
```

## Recursos Adicionais

- **Documentação**: https://pymatgen.org/
- **Materials Project**: https://materialsproject.org/
- **GitHub**: https://github.com/materialsproject/pymatgen
- **Forum**: https://matsci.org/
- **Notebooks de exemplo**: https://matgenb.materialsvirtuallab.org/

## Notas de Versão

Esta habilidade foi projetada para pymatgen 2024.x e posterior. Para a API do Materials Project, use o pacote `mp-api` (separado do `pymatgen.ext.matproj` legado).

Requisitos:
- Python 3.10 ou superior
- pymatgen >= 2023.x
- mp-api (para acesso ao Materials Project)