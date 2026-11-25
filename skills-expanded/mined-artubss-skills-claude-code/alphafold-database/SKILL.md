---
name: alphafold-database
description: "Acesse mais de 200 milhões de estruturas de proteínas previstas por IA do AlphaFold. Recupere estruturas por ID do UniProt, baixe arquivos PDB/mmCIF, analise métricas de confiança (pLDDT, PAE) para descoberta de fármacos e biologia estrutural."
---

# AlphaFold Database

## Visão Geral

AlphaFold DB é um repositório público de estruturas 3D de proteínas previstas por IA para mais de 200 milhões de proteínas, mantido pela DeepMind e EMBL-EBI. Acesse previsões de estruturas com métricas de confiança, baixe arquivos de coordenadas, recupere conjuntos de dados em massa e integre previsões em workflows computacionais.

## Quando Usar Esta Skill

Esta skill deve ser usada ao trabalhar com estruturas de proteínas previstas por IA em cenários como:

- Recuperar previsões de estrutura de proteína por ID do UniProt ou nome da proteína
- Baixar arquivos de coordenadas PDB/mmCIF para análise estrutural
- Analisar métricas de confiança de previsão (pLDDT, PAE) para avaliar confiabilidade
- Acessar conjuntos de dados de proteoma em massa via Google Cloud Platform
- Comparar estruturas previstas com dados experimentais
- Executar descoberta de fármacos baseada em estrutura ou engenharia de proteínas
- Construir modelos estruturais para proteínas sem estruturas experimentais
- Integrar previsões do AlphaFold em pipelines computacionais

## Capacidades Principais

### 1. Buscando e Recuperando Previsões

**Usando Biopython (Recomendado):**

A biblioteca Biopython fornece a interface mais simples para recuperar estruturas do AlphaFold:

```python
from Bio.PDB import alphafold_db

# Get all predictions for a UniProt accession
predictions = list(alphafold_db.get_predictions("P00520"))

# Download structure file (mmCIF format)
for prediction in predictions:
    cif_file = alphafold_db.download_cif_for(prediction, directory="./structures")
    print(f"Downloaded: {cif_file}")

# Get Structure objects directly
from Bio.PDB import MMCIFParser
structures = list(alphafold_db.get_structural_models_for("P00520"))
```

**Acesso Direto à API:**

Consulte previsões usando endpoints REST:

```python
import requests

# Get prediction metadata for a UniProt accession
uniprot_id = "P00520"
api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
response = requests.get(api_url)
prediction_data = response.json()

# Extract AlphaFold ID
alphafold_id = prediction_data[0]['entryId']
print(f"AlphaFold ID: {alphafold_id}")
```

**Usando UniProt para Encontrar Acessos:**

Busque no UniProt para encontrar acessos de proteína primeiro:

```python
import urllib.parse, urllib.request

def get_uniprot_ids(query, query_type='PDB_ID'):
    """Query UniProt to get accession IDs"""
    url = 'https://www.uniprot.org/uploadlists/'
    params = {
        'from': query_type,
        'to': 'ACC',
        'format': 'txt',
        'query': query
    }
    data = urllib.parse.urlencode(params).encode('ascii')
    with urllib.request.urlopen(urllib.request.Request(url, data)) as response:
        return response.read().decode('utf-8').splitlines()

# Example: Find UniProt IDs for a protein name
protein_ids = get_uniprot_ids("hemoglobin", query_type="GENE_NAME")
```

### 2. Baixando Arquivos de Estrutura

AlphaFold fornece múltiplos formatos de arquivo para cada previsão:

**Tipos de Arquivo Disponíveis:**

- **Coordenadas do modelo** (`model_v4.cif`): Coordenadas atômicas em formato mmCIF/PDBx
- **Scores de confiança** (`confidence_v4.json`): Scores pLDDT por resíduo (0-100)
- **Erro Alinhado Previsto** (`predicted_aligned_error_v4.json`): Matriz PAE para confiança de pares de resíduos

**URLs de Download:**

```python
import requests

alphafold_id = "AF-P00520-F1"
version = "v4"

# Model coordinates (mmCIF)
model_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-model_{version}.cif"
response = requests.get(model_url)
with open(f"{alphafold_id}.cif", "w") as f:
    f.write(response.text)

# Confidence scores (JSON)
confidence_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-confidence_{version}.json"
response = requests.get(confidence_url)
confidence_data = response.json()

# Predicted Aligned Error (JSON)
pae_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-predicted_aligned_error_{version}.json"
response = requests.get(pae_url)
pae_data = response.json()
```

**Formato PDB (Alternativa):**

```python
# Download as PDB format instead of mmCIF
pdb_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-model_{version}.pdb"
response = requests.get(pdb_url)
with open(f"{alphafold_id}.pdb", "wb") as f:
    f.write(response.content)
```

### 3. Trabalhando com Métricas de Confiança

As previsões do AlphaFold incluem estimativas de confiança críticas para interpretação:

**pLDDT (confiança por resíduo):**

```python
import json
import requests

# Load confidence scores
alphafold_id = "AF-P00520-F1"
confidence_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-confidence_v4.json"
confidence = requests.get(confidence_url).json()

# Extract pLDDT scores
plddt_scores = confidence['confidenceScore']

# Interpret confidence levels
# pLDDT > 90: Very high confidence
# pLDDT 70-90: High confidence
# pLDDT 50-70: Low confidence
# pLDDT < 50: Very low confidence

high_confidence_residues = [i for i, score in enumerate(plddt_scores) if score > 90]
print(f"High confidence residues: {len(high_confidence_residues)}/{len(plddt_scores)}")
```

**PAE (Erro Alinhado Previsto):**

PAE indica confiança nas posições relativas de domínios:

```python
import numpy as np
import matplotlib.pyplot as plt

# Load PAE matrix
pae_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-predicted_aligned_error_v4.json"
pae = requests.get(pae_url).json()

# Visualize PAE matrix
pae_matrix = np.array(pae['distance'])
plt.figure(figsize=(10, 8))
plt.imshow(pae_matrix, cmap='viridis_r', vmin=0, vmax=30)
plt.colorbar(label='PAE (Å)')
plt.title(f'Predicted Aligned Error: {alphafold_id}')
plt.xlabel('Residue')
plt.ylabel('Residue')
plt.savefig(f'{alphafold_id}_pae.png', dpi=300, bbox_inches='tight')

# Low PAE values (<5 Å) indicate confident relative positioning
# High PAE values (>15 Å) suggest uncertain domain arrangements
```

### 4. Acesso a Dados em Massa via Google Cloud

Para análises em larga escala, use datasets do Google Cloud:

**Google Cloud Storage:**

```bash
# Install gsutil
uv pip install gsutil

# List available data
gsutil ls gs://public-datasets-deepmind-alphafold-v4/

# Download entire proteomes (by taxonomy ID)
gsutil -m cp gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-9606-*.tar .

# Download specific files
gsutil cp gs://public-datasets-deepmind-alphafold-v4/accession_ids.csv .
```

**Acesso a Metadados via BigQuery:**

```python
from google.cloud import bigquery

# Initialize client
client = bigquery.Client()

# Query metadata
query = """
SELECT
  entryId,
  uniprotAccession,
  organismScientificName,
  globalMetricValue,
  fractionPlddtVeryHigh
FROM `bigquery-public-data.deepmind_alphafold.metadata`
WHERE organismScientificName = 'Homo sapiens'
  AND fractionPlddtVeryHigh > 0.8
LIMIT 100
"""

results = client.query(query).to_dataframe()
print(f"Found {len(results)} high-confidence human proteins")
```

**Download por Espécie:**

```python
import subprocess

def download_proteome(taxonomy_id, output_dir="./proteomes"):
    """Download all AlphaFold predictions for a species"""
    pattern = f"gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-{taxonomy_id}-*_v4.tar"
    cmd = f"gsutil -m cp {pattern} {output_dir}/"
    subprocess.run(cmd, shell=True, check=True)

# Download E. coli proteome (tax ID: 83333)
download_proteome(83333)

# Download human proteome (tax ID: 9606)
download_proteome(9606)
```

### 5. Analisando e Interpretando Estruturas

Trabalhe com estruturas do AlphaFold baixadas usando BioPython:

```python
from Bio.PDB import MMCIFParser, PDBIO
import numpy as np

# Parse mmCIF file
parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("protein", "AF-P00520-F1-model_v4.cif")

# Extract coordinates
coords = []
for model in structure:
    for chain in model:
        for residue in chain:
            if 'CA' in residue:  # Alpha carbons only
                coords.append(residue['CA'].get_coord())

coords = np.array(coords)
print(f"Structure has {len(coords)} residues")

# Calculate distances
from scipy.spatial.distance import pdist, squareform
distance_matrix = squareform(pdist(coords))

# Identify contacts (< 8 Å)
contacts = np.where((distance_matrix > 0) & (distance_matrix < 8))
print(f"Number of contacts: {len(contacts[0]) // 2}")
```

**Extrair Fatores B (valores de pLDDT):**

AlphaFold armazena scores de pLDDT na coluna de fator B:

```python
from Bio.PDB import MMCIFParser

parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("protein", "AF-P00520-F1-model_v4.cif")

# Extract pLDDT from B-factors
plddt_scores = []
for model in structure:
    for chain in model:
        for residue in chain:
            if 'CA' in residue:
                plddt_scores.append(residue['CA'].get_bfactor())

# Identify high-confidence regions
high_conf_regions = [(i, score) for i, score in enumerate(plddt_scores, 1) if score > 90]
print(f"High confidence residues: {len(high_conf_regions)}")
```

### 6. Processamento em Lote de Múltiplas Proteínas

Processe múltiplas previsões com eficiência:

```python
from Bio.PDB import alphafold_db
import pandas as pd

uniprot_ids = ["P00520", "P12931", "P04637"]  # Multiple proteins
results = []

for uniprot_id in uniprot_ids:
    try:
        # Get prediction
        predictions = list(alphafold_db.get_predictions(uniprot_id))

        if predictions:
            pred = predictions[0]

            # Download structure
            cif_file = alphafold_db.download_cif_for(pred, directory="./batch_structures")

            # Get confidence data
            alphafold_id = pred['entryId']
            conf_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-confidence_v4.json"
            conf_data = requests.get(conf_url).json()

            # Calculate statistics
            plddt_scores = conf_data['confidenceScore']
            avg_plddt = np.mean(plddt_scores)
            high_conf_fraction = sum(1 for s in plddt_scores if s > 90) / len(plddt_scores)

            results.append({
                'uniprot_id': uniprot_id,
                'alphafold_id': alphafold_id,
                'avg_plddt': avg_plddt,
                'high_conf_fraction': high_conf_fraction,
                'length': len(plddt_scores)
            })
    except Exception as e:
        print(f"Error processing {uniprot_id}: {e}")

# Create summary DataFrame
df = pd.DataFrame(results)
print(df)
```

## Instalação e Configuração

### Bibliotecas Python

```bash
# Install Biopython for structure access
uv pip install biopython

# Install requests for API access
uv pip install requests

# For visualization and analysis
uv pip install numpy matplotlib pandas scipy

# For Google Cloud access (optional)
uv pip install google-cloud-bigquery gsutil
```

### Alternativa de API 3D-Beacons

AlphaFold também pode ser acessado via API federada 3D-Beacons:

```python
import requests

# Query via 3D-Beacons
uniprot_id = "P00520"
url = f"https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/uniprot/summary/{uniprot_id}.json"
response = requests.get(url)
data = response.json()

# Filter for AlphaFold structures
af_structures = [s for s in data['structures'] if s['provider'] == 'AlphaFold DB']
```

## Casos de Uso Comuns

### Proteômica Estrutural
- Baixar previsões de proteoma completo para análise
- Identificar regiões estruturais de alta confiança em proteínas
- Comparar estruturas previstas com dados experimentais
- Construir modelos estruturais para famílias de proteínas

### Descoberta de Fármacos
- Recuperar estruturas de proteína alvo para estudos de docking
- Analisar conformações de sítio de ligação
- Identificar bolsas drugatáveis em estruturas previstas
- Comparar estruturas entre homólogos

### Engenharia de Proteínas
- Identificar regiões estáveis/instáveis usando pLDDT
- Projetar mutações em regiões de alta confiança
- Analisar arquiteturas de domínio usando PAE
- Modelar variantes de proteína e mutações

### Estudos Evolutivos
- Comparar estruturas de ortólogos entre espécies
- Analisar conservação de características estruturais
- Estudar padrões de evolução de domínios
- Identificar regiões funcionalmente importantes

## Conceitos-Chave

**Acesso do UniProt:** Identificador primário para proteínas (ex: "P00520"). Necessário para consultar AlphaFold DB.

**ID do AlphaFold:** Formato de identificador interno: `AF-[acesso UniProt]-F[número do fragmento]` (ex: "AF-P00520-F1").

**pLDDT (Teste de Diferença de Distância Local Previsto):** Métrica de confiança por resíduo (0-100). Valores mais altos indicam previsões mais confiantes.

**PAE (Erro Alinhado Previsto):** Matriz indicando confiança nas posições relativas entre pares de resíduos. Valores baixos (<5 Å) sugerem posicionamento relativo confiante.

**Versão do Banco de Dados:** A versão atual é v4. As URLs de arquivo incluem sufixo de versão (ex: `model_v4.cif`).

**Número do Fragmento:** Proteínas grandes podem ser divididas em fragmentos. O número do fragmento aparece no ID do AlphaFold (ex: F1, F2).

## Diretrizes de Interpretação de Confiança

**Limites de pLDDT:**
- **>90**: Confiança muito alta — adequado para análise detalhada
- **70-90**: Confiança alta — estrutura de backbone geralmente confiável
- **50-70**: Confiança baixa — usar com cautela, regiões flexíveis
- **<50**: Confiança muito baixa — provavelmente desordenado ou não confiável

**Diretrizes de PAE:**
- **<5 Å**: Posicionamento relativo de domínios confiante
- **5-10 Å**: Confiança moderada no arranjo
- **>15 Å**: Posições relativas incertas, domínios podem ser móveis

## Recursos

### references/api_reference.md

Documentação abrangente da API cobrindo:
- Especificações completas de endpoints da API REST
- Detalhes de formato de arquivo e esquemas de dados
- Estrutura do dataset Google Cloud e padrões de acesso
- Exemplos avançados de query e estratégias de processamento em lote
- Limitação de taxa, cache e boas práticas
- Troubleshooting de problemas comuns

Consulte esta referência para informações detalhadas da API, estratégias de download em massa ou ao trabalhar com datasets em larga escala.

## Notas Importantes

### Uso de Dados e Atribuição

- AlphaFold DB está livremente disponível sob licença CC-BY-4.0
- Cite: Jumper et al. (2021) Nature e Varadi et al. (2022) Nucleic Acids Research
- Previsões são modelos computacionais, não estruturas experimentais
- Sempre avalie métricas de confiança antes da análise downstream

### Gerenciamento de Versão

- Versão atual do banco de dados: v4 (a partir de 2024-2025)
- URLs de arquivo incluem sufixo de versão (ex: `_v4.cif`)
- Verifique atualizações do banco de dados regularmente
- Versões mais antigas podem ser descontinuadas ao longo do tempo

### Considerações de Qualidade de Dados

- pLDDT alto não garante precisão funcional
- Regiões de baixa confiança podem estar desordenadas in vivo
- PAE indica confiança relativa de domínio, não posicionamento absoluto
- Previsões não incluem ligantes, modificações pós-traducionais e cofatores
- Complexos multi-cadeia não são previstos (apenas cadeias únicas)

### Dicas de Desempenho

- Use Biopython para acesso simples de proteína única
- Use Google Cloud para downloads em massa (muito mais rápido que arquivos individuais)
- Cache de arquivos baixados localmente para evitar downloads repetidos
- Tier gratuito BigQuery: 1 TB de dados processados por mês
- Considere largura de banda de rede para downloads em larga escala

## Recursos Adicionais

- **Site AlphaFold DB:** https://alphafold.ebi.ac.uk/
- **Documentação da API:** https://alphafold.ebi.ac.uk/api-docs
- **Dataset Google Cloud:** https://cloud.google.com/blog/products/ai-machine-learning/alphafold-protein-structure-database
- **API 3D-Beacons:** https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/
- **Artigos do AlphaFold:**
  - Nature (2021): https://doi.org/10.1038/s41586-021-03819-2
  - Nucleic Acids Research (2024): https://doi.org/10.1093/nar/gkad1011
- **Documentação Biopython:** https://biopython.org/docs/dev/api/Bio.PDB.alphafold_db.html
- **Repositório GitHub:** https://github.com/google-deepmind/alphafold