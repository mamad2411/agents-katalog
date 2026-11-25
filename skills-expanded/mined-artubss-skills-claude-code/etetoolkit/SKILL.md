---
name: etetoolkit
description: "Toolkit de árvore filogenética (ETE). Manipulação de árvore (Newick/NHX), detecção de eventos evolutivos, ortologia/paralogia, taxonomia NCBI, visualização (PDF/SVG), para filognoômica."
---

# Skill ETE Toolkit

## Visão geral

ETE (Environment for Tree Exploration) é um toolkit para análise filogenética e de árvores hierárquicas. Manipule árvores, analise eventos evolutivos, visualize resultados e integre-se com bancos de dados biológicos para pesquisa filognoômica e análise de agrupamentos.

## Capacidades principais

### 1. Manipulação e análise de árvores

Carregue, manipule e analise estruturas de árvore hierárquicas com suporte para:

- **I/O de árvores**: Leia e escreva em formatos Newick, NHX, PhyloXML e NeXML
- **Traversal de árvores**: Navegue em árvores usando estratégias preorder, postorder ou levelorder
- **Modificação de topologia**: Poda, raiz, colapso de nós, resolução de politomias
- **Cálculos de distância**: Calcule comprimentos de ramo e distâncias topológicas entre nós
- **Comparação de árvores**: Calcule distâncias de Robinson-Foulds e identifique diferenças topológicas

**Padrões comuns:**

```python
from ete3 import Tree

# Load tree from file
tree = Tree("tree.nw", format=1)

# Basic statistics
print(f"Leaves: {len(tree)}")
print(f"Total nodes: {len(list(tree.traverse()))}")

# Prune to taxa of interest
taxa_to_keep = ["species1", "species2", "species3"]
tree.prune(taxa_to_keep, preserve_branch_length=True)

# Midpoint root
midpoint = tree.get_midpoint_outgroup()
tree.set_outgroup(midpoint)

# Save modified tree
tree.write(outfile="rooted_tree.nw")
```

Use `scripts/tree_operations.py` para manipulação de árvores via linha de comando:

```bash
# Display tree statistics
python scripts/tree_operations.py stats tree.nw

# Convert format
python scripts/tree_operations.py convert tree.nw output.nw --in-format 0 --out-format 1

# Reroot tree
python scripts/tree_operations.py reroot tree.nw rooted.nw --midpoint

# Prune to specific taxa
python scripts/tree_operations.py prune tree.nw pruned.nw --keep-taxa "sp1,sp2,sp3"

# Show ASCII visualization
python scripts/tree_operations.py ascii tree.nw
```

### 2. Análise filogenética

Analise árvores gênicas com detecção de eventos evolutivos:

- **Integração de alinhamento de sequências**: Vinculue árvores a alinhamentos múltiplos de sequências (FASTA, Phylip)
- **Nomeação de espécies**: Extração automática ou customizada de espécies a partir de nomes de genes
- **Eventos evolutivos**: Detecte eventos de duplicação e especiação usando Species Overlap ou reconciliação de árvores
- **Detecção de ortologia**: Identifique ortólogos e parálogos com base em eventos evolutivos
- **Análise de família gênica**: Divida árvores por duplicações, colapso de expansões lineage-specific

**Workflow para análise de árvore gênica:**

```python
from ete3 import PhyloTree

# Load gene tree with alignment
tree = PhyloTree("gene_tree.nw", alignment="alignment.fasta")

# Set species naming function
def get_species(gene_name):
    return gene_name.split("_")[0]

tree.set_species_naming_function(get_species)

# Detect evolutionary events
events = tree.get_descendant_evol_events()

# Analyze events
for node in tree.traverse():
    if hasattr(node, "evoltype"):
        if node.evoltype == "D":
            print(f"Duplication at {node.name}")
        elif node.evoltype == "S":
            print(f"Speciation at {node.name}")

# Extract ortholog groups
ortho_groups = tree.get_speciation_trees()
for i, ortho_tree in enumerate(ortho_groups):
    ortho_tree.write(outfile=f"ortholog_group_{i}.nw")
```

**Encontrando ortólogos e parálogos:**

```python
# Find orthologs to query gene
query = tree & "species1_gene1"

orthologs = []
paralogs = []

for event in events:
    if query in event.in_seqs:
        if event.etype == "S":
            orthologs.extend([s for s in event.out_seqs if s != query])
        elif event.etype == "D":
            paralogs.extend([s for s in event.out_seqs if s != query])
```

### 3. Integração com a taxonomia NCBI

Integre informações taxonômicas do banco de dados NCBI Taxonomy:

- **Acesso ao banco de dados**: Download automático e cache local da taxonomia NCBI (~300MB)
- **Tradução taxid/nome**: Converta entre IDs taxonômicos e nomes científicos
- **Recuperação de linhagem**: Obtenha linhagens evolutivas completas
- **Árvores de taxonomia**: Construa árvores de espécies conectando táxons especificados
- **Anotação de árvore**: Anote automaticamente árvores com informações taxonômicas

**Construindo árvores baseadas em taxonomia:**

```python
from ete3 import NCBITaxa

ncbi = NCBITaxa()

# Build tree from species names
species = ["Homo sapiens", "Pan troglodytes", "Mus musculus"]
name2taxid = ncbi.get_name_translator(species)
taxids = [name2taxid[sp][0] for sp in species]

# Get minimal tree connecting taxa
tree = ncbi.get_topology(taxids)

# Annotate nodes with taxonomy info
for node in tree.traverse():
    if hasattr(node, "sci_name"):
        print(f"{node.sci_name} - Rank: {node.rank} - TaxID: {node.taxid}")
```

**Anotando árvores existentes:**

```python
# Get taxonomy info for tree leaves
for leaf in tree:
    species = extract_species_from_name(leaf.name)
    taxid = ncbi.get_name_translator([species])[species][0]

    # Get lineage
    lineage = ncbi.get_lineage(taxid)
    ranks = ncbi.get_rank(lineage)
    names = ncbi.get_taxid_translator(lineage)

    # Add to node
    leaf.add_feature("taxid", taxid)
    leaf.add_feature("lineage", [names[t] for t in lineage])
```

### 4. Visualização de árvores

Crie visualizações de árvores com qualidade de publicação:

- **Formatos de saída**: PNG (raster), PDF e SVG (vetor) para publicações
- **Modos de layout**: Layouts de árvore retangular e circular
- **GUI interativa**: Explore árvores interativamente com zoom, pan e busca
- **Styling customizado**: NodeStyle para aparência de nós (cores, formas, tamanhos)
- **Faces**: Adicione elementos gráficos (texto, imagens, gráficos, heatmaps) aos nós
- **Funções de layout**: Styling dinâmico baseado em propriedades de nós

**Workflow básico de visualização:**

```python
from ete3 import Tree, TreeStyle, NodeStyle

tree = Tree("tree.nw")

# Configure tree style
ts = TreeStyle()
ts.show_leaf_name = True
ts.show_branch_support = True
ts.scale = 50  # pixels per branch length unit

# Style nodes
for node in tree.traverse():
    nstyle = NodeStyle()

    if node.is_leaf():
        nstyle["fgcolor"] = "blue"
        nstyle["size"] = 8
    else:
        # Color by support
        if node.support > 0.9:
            nstyle["fgcolor"] = "darkgreen"
        else:
            nstyle["fgcolor"] = "red"
        nstyle["size"] = 5

    node.set_style(nstyle)

# Render to file
tree.render("tree.pdf", tree_style=ts)
tree.render("tree.png", w=800, h=600, units="px", dpi=300)
```

Use `scripts/quick_visualize.py` para visualização rápida:

```bash
# Basic visualization
python scripts/quick_visualize.py tree.nw output.pdf

# Circular layout with custom styling
python scripts/quick_visualize.py tree.nw output.pdf --mode c --color-by-support

# High-resolution PNG
python scripts/quick_visualize.py tree.nw output.png --width 1200 --height 800 --units px --dpi 300

# Custom title and styling
python scripts/quick_visualize.py tree.nw output.pdf --title "Species Phylogeny" --show-support
```

**Visualização avançada com faces:**

```python
from ete3 import Tree, TreeStyle, TextFace, CircleFace

tree = Tree("tree.nw")

# Add features to nodes
for leaf in tree:
    leaf.add_feature("habitat", "marine" if "fish" in leaf.name else "land")

# Layout function
def layout(node):
    if node.is_leaf():
        # Add colored circle
        color = "blue" if node.habitat == "marine" else "green"
        circle = CircleFace(radius=5, color=color)
        node.add_face(circle, column=0, position="aligned")

        # Add label
        label = TextFace(node.name, fsize=10)
        node.add_face(label, column=1, position="aligned")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_leaf_name = False

tree.render("annotated_tree.pdf", tree_style=ts)
```

### 5. Análise de agrupamentos

Analise resultados de agrupamento hierárquico com integração de dados:

- **ClusterTree**: Classe especializada para dendrogramas de agrupamento
- **Vinculação de matriz de dados**: Conecte folhas de árvore a perfis numéricos
- **Métricas de agrupamento**: Coeficiente de silhueta, índice de Dunn, distâncias intra/inter-cluster
- **Validação**: Teste a qualidade de agrupamento com diferentes métricas de distância
- **Visualização de heatmap**: Exiba matrizes de dados ao lado de árvores

**Workflow de agrupamento:**

```python
from ete3 import ClusterTree

# Load tree with data matrix
matrix = """#Names\tSample1\tSample2\tSample3
Gene1\t1.5\t2.3\t0.8
Gene2\t0.9\t1.1\t1.8
Gene3\t2.1\t2.5\t0.5"""

tree = ClusterTree("((Gene1,Gene2),Gene3);", text_array=matrix)

# Evaluate cluster quality
for node in tree.traverse():
    if not node.is_leaf():
        silhouette = node.get_silhouette()
        dunn = node.get_dunn()

        print(f"Cluster: {node.name}")
        print(f"  Silhouette: {silhouette:.3f}")
        print(f"  Dunn index: {dunn:.3f}")

# Visualize with heatmap
tree.show("heatmap")
```

### 6. Comparação de árvores

Quantifique diferenças topológicas entre árvores:

- **Distância de Robinson-Foulds**: Métrica padrão para comparação de árvores
- **RF normalizado**: Distância scale-invariant (0.0 a 1.0)
- **Análise de partições**: Identifique bipartições únicas e compartilhadas
- **Árvores de consenso**: Analise suporte em múltiplas árvores
- **Comparação em lote**: Compare múltiplas árvores aos pares

**Comparar duas árvores:**

```python
from ete3 import Tree

tree1 = Tree("tree1.nw")
tree2 = Tree("tree2.nw")

# Calculate RF distance
rf, max_rf, common_leaves, parts_t1, parts_t2 = tree1.robinson_foulds(tree2)

print(f"RF distance: {rf}/{max_rf}")
print(f"Normalized RF: {rf/max_rf:.3f}")
print(f"Common leaves: {len(common_leaves)}")

# Find unique partitions
unique_t1 = parts_t1 - parts_t2
unique_t2 = parts_t2 - parts_t1

print(f"Unique to tree1: {len(unique_t1)}")
print(f"Unique to tree2: {len(unique_t2)}")
```

**Comparar múltiplas árvores:**

```python
import numpy as np

trees = [Tree(f"tree{i}.nw") for i in range(4)]

# Create distance matrix
n = len(trees)
dist_matrix = np.zeros((n, n))

for i in range(n):
    for j in range(i+1, n):
        rf, max_rf, _, _, _ = trees[i].robinson_foulds(trees[j])
        norm_rf = rf / max_rf if max_rf > 0 else 0
        dist_matrix[i, j] = norm_rf
        dist_matrix[j, i] = norm_rf
```

## Instalação e configuração

Instale o toolkit ETE:

```bash
# Basic installation
uv pip install ete3

# With external dependencies for rendering (optional but recommended)
# On macOS:
brew install qt@5

# On Ubuntu/Debian:
sudo apt-get install python3-pyqt5 python3-pyqt5.qtsvg

# For full features including GUI
uv pip install ete3[gui]
```

**Configuração da taxonomia NCBI na primeira execução:**

Na primeira vez que NCBITaxa é instanciada, ele automaticamente baixa o banco de dados de taxonomia NCBI (~300MB) para `~/.etetoolkit/taxa.sqlite`. Isso acontece apenas uma vez:

```python
from ete3 import NCBITaxa
ncbi = NCBITaxa()  # Downloads database on first run
```

Atualize o banco de dados de taxonomia:

```python
ncbi.update_taxonomy_database()  # Download latest NCBI data
```

## Casos de uso comuns

### Caso de uso 1: Pipeline de filognoômica

Workflow completo de árvore gênica para identificação de ortólogos:

```python
from ete3 import PhyloTree, NCBITaxa

# 1. Load gene tree with alignment
tree = PhyloTree("gene_tree.nw", alignment="alignment.fasta")

# 2. Configure species naming
tree.set_species_naming_function(lambda x: x.split("_")[0])

# 3. Detect evolutionary events
tree.get_descendant_evol_events()

# 4. Annotate with taxonomy
ncbi = NCBITaxa()
for leaf in tree:
    if leaf.species in species_to_taxid:
        taxid = species_to_taxid[leaf.species]
        lineage = ncbi.get_lineage(taxid)
        leaf.add_feature("lineage", lineage)

# 5. Extract ortholog groups
ortho_groups = tree.get_speciation_trees()

# 6. Save and visualize
for i, ortho in enumerate(ortho_groups):
    ortho.write(outfile=f"ortho_{i}.nw")
```

### Caso de uso 2: Pré-processamento e formatação de árvores

Processe árvores em lote para análise:

```bash
# Convert format
python scripts/tree_operations.py convert input.nw output.nw --in-format 0 --out-format 1

# Root at midpoint
python scripts/tree_operations.py reroot input.nw rooted.nw --midpoint

# Prune to focal taxa
python scripts/tree_operations.py prune rooted.nw pruned.nw --keep-taxa taxa_list.txt

# Get statistics
python scripts/tree_operations.py stats pruned.nw
```

### Caso de uso 3: Figuras com qualidade de publicação

Crie visualizações estilizadas:

```python
from ete3 import Tree, TreeStyle, NodeStyle, TextFace

tree = Tree("tree.nw")

# Define clade colors
clade_colors = {
    "Mammals": "red",
    "Birds": "blue",
    "Fish": "green"
}

def layout(node):
    # Highlight clades
    if node.is_leaf():
        for clade, color in clade_colors.items():
            if clade in node.name:
                nstyle = NodeStyle()
                nstyle["fgcolor"] = color
                nstyle["size"] = 8
                node.set_style(nstyle)
    else:
        # Add support values
        if node.support > 0.95:
            support = TextFace(f"{node.support:.2f}", fsize=8)
            node.add_face(support, column=0, position="branch-top")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_scale = True

# Render for publication
tree.render("figure.pdf", w=200, units="mm", tree_style=ts)
tree.render("figure.svg", tree_style=ts)  # Editable vector
```

### Caso de uso 4: Análise automatizada de árvores

Processe múltiplas árvores sistematicamente:

```python
from ete3 import Tree
import os

input_dir = "trees"
output_dir = "processed"

for filename in os.listdir(input_dir):
    if filename.endswith(".nw"):
        tree = Tree(os.path.join(input_dir, filename))

        # Standardize: midpoint root, resolve polytomies
        midpoint = tree.get_midpoint_outgroup()
        tree.set_outgroup(midpoint)
        tree.resolve_polytomy(recursive=True)

        # Filter low support branches
        for node in tree.traverse():
            if hasattr(node, 'support') and node.support < 0.5:
                if not node.is_leaf() and not node.is_root():
                    node.delete()

        # Save processed tree
        output_file = os.path.join(output_dir, f"processed_{filename}")
        tree.write(outfile=output_file)
```

## Documentação de referência

Para documentação completa de API, exemplos de código e guias detalhados, consulte os seguintes recursos no diretório `references/`:

- **`api_reference.md`**: Documentação completa de API para todas as classes e métodos ETE (Tree, PhyloTree, ClusterTree, NCBITaxa), incluindo parâmetros, tipos de retorno e exemplos de código
- **`workflows.md`**: Padrões de workflow comuns organizados por tarefa (operações de árvore, análise filogenética, comparação de árvores, integração de taxonomia, análise de agrupamento)
- **`visualization.md`**: Guia abrangente de visualização cobrindo TreeStyle, NodeStyle, Faces, funções de layout e técnicas avançadas de visualização

Carregue essas referências quando informações detalhadas forem necessárias:

```python
# To use API reference
# Read references/api_reference.md for complete method signatures and parameters

# To implement workflows
# Read references/workflows.md for step-by-step workflow examples

# To create visualizations
# Read references/visualization.md for styling and rendering options
```

## Solução de problemas

**Erros de import:**

```bash
# If "ModuleNotFoundError: No module named 'ete3'"
uv pip install ete3

# For GUI and rendering issues
uv pip install ete3[gui]
```

**Problemas de rendering:**

Se `tree.render()` ou `tree.show()` falhar com erros relacionados a Qt, instale as dependências de sistema:

```bash
# macOS
brew install qt@5

# Ubuntu/Debian
sudo apt-get install python3-pyqt5 python3-pyqt5.qtsvg
```

**Banco de dados de taxonomia NCBI:**

Se o download do banco de dados falhar ou for corrompido:

```python
from ete3 import NCBITaxa
ncbi = NCBITaxa()
ncbi.update_taxonomy_database()  # Redownload database
```

**Problemas de memória com árvores grandes:**

Para árvores muito grandes (>10.000 folhas), use iteradores em vez de list comprehensions:

```python
# Memory-efficient iteration
for leaf in tree.iter_leaves():
    process(leaf)

# Instead of
for leaf in tree.get_leaves():  # Loads all into memory
    process(leaf)
```

## Referência de formato Newick

ETE suporta múltiplas especificações de formato Newick (0-100):

- **Formato 0**: Flexível com comprimentos de ramo (padrão)
- **Formato 1**: Com nomes de nó interno
- **Formato 2**: Com valores de bootstrap/suporte
- **Formato 5**: Nomes de nó interno + comprimentos de ramo
- **Formato 8**: Todos os recursos (nomes, distâncias, suporte)
- **Formato 9**: Apenas nomes de folhas
- **Formato 100**: Apenas topologia

Especifique o formato ao ler/escrever:

```python
tree = Tree("tree.nw", format=1)
tree.write(outfile="output.nw", format=5)
```

Formato NHX (New Hampshire eXtended) preserva recursos customizados:

```python
tree.write(outfile="tree.nhx", features=["habitat", "temperature", "depth"])
```

## Melhores práticas

1. **Preserve comprimentos de ramo**: Use `preserve_branch_length=True` ao fazer poda para análise filogenética
2. **Cache de conteúdo**: Use `get_cached_content()` para acesso repetido ao conteúdo de nós em árvores grandes
3. **Use iteradores**: Empregue métodos `iter_*` para processamento memory-efficient de árvores grandes
4. **Escolha traversal apropriado**: Postorder para análise bottom-up, preorder para top-down
5. **Valide monofilia**: Sempre verifique o tipo de clade retornado (monofilético/parafilético/polifilético)
6. **Formatos vetor para publicação**: Use PDF ou SVG para figuras de publicação (escaláveis, editáveis)
7. **Teste interativo**: Use `tree.show()` para testar visualizações antes de renderizar para arquivo
8. **PhyloTree para filogenia**: Use classe PhyloTree para árvores gênicas e análise evolutiva
9. **Seleção de método copy**: "newick" para velocidade, "cpickle" para fidelidade total, "deepcopy" para objetos complexos
10. **Cache de queries NCBI**: Armazene resultados de queries de taxonomia NCBI para evitar acesso repetido ao banco de dados