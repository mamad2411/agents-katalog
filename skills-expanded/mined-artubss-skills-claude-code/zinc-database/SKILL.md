---
name: zinc-database
description: "Acesse ZINC (230M+ compostos compráveis). Busque por ZINC ID/SMILES, realize buscas por similaridade, estruturas 3D prontas para docking, descoberta de análogos, para triagem virtual e descoberta de fármacos."
---

# ZINC Database

## Visão Geral

ZINC é um repositório livremente acessível de 230M+ compostos compráveis mantido pela UCSF. Busque por ZINC ID ou SMILES, realize buscas por similaridade, baixe estruturas 3D prontas para docking, descubra análogos para triagem virtual e descoberta de fármacos.

## Quando Usar Este Skill

Este skill deve ser usado quando:

- **Triagem virtual**: Encontrar compostos para estudos de docking molecular
- **Descoberta de leads**: Identificar compostos comercialmente disponíveis para desenvolvimento de fármacos
- **Buscas de estruturas**: Realizar buscas por similaridade ou análogos por SMILES
- **Recuperação de compostos**: Procurar moléculas por ZINC IDs ou códigos de fornecedores
- **Exploração do espaço químico**: Explorar a diversidade química de compostos compráveis
- **Estudos de docking**: Acessar estruturas moleculares 3D prontas
- **Buscas de análogos**: Encontrar compostos semelhantes com base em similaridade estrutural
- **Consultas de fornecedores**: Identificar compostos de fornecedores químicos específicos
- **Amostragem aleatória**: Obter conjuntos aleatórios de compostos para triagem

## Versões do Banco de Dados

ZINC evoluiu por múltiplas versões:

- **ZINC22** (Atual): Versão maior com 230+ milhões de compostos compráveis e compostos sob demanda em escala multi-bilionária
- **ZINC20**: Ainda mantido, focado em compostos do tipo lead e drug-like
- **ZINC15**: Versão anterior, legado mas ainda documentado

Este skill se concentra principalmente em ZINC22, a versão mais atual e abrangente.

## Métodos de Acesso

### Interface Web

Ponto de acesso principal: https://zinc.docking.org/
Busca interativa: https://cartblanche22.docking.org/

### Acesso via API

Todas as buscas ZINC22 podem ser realizadas programaticamente via API CartBlanche22:

**URL Base**: `https://cartblanche22.docking.org/`

Todos os endpoints da API retornam dados em formato texto ou JSON com campos customizáveis.

## Capacidades Principais

### 1. Busca por ZINC ID

Recuperar compostos específicos usando seus identificadores ZINC.

**Interface web**: https://cartblanche22.docking.org/search/zincid

**Endpoint da API**:
```bash
curl "https://cartblanche22.docking.org/[email protected]_fields=smiles,zinc_id"
```

**IDs múltiplos**:
```bash
curl "https://cartblanche22.docking.org/substances.txt:zinc_id=ZINC000000000001,ZINC000000000002&output_fields=smiles,zinc_id,tranche"
```

**Campos de resposta**: `zinc_id`, `smiles`, `sub_id`, `supplier_code`, `catalogs`, `tranche` (inclui contagem de H, LogP, MW, fase)

### 2. Busca por SMILES

Encontrar compostos pela estrutura química usando notação SMILES, com parâmetros de distância opcionais para busca de análogos.

**Interface web**: https://cartblanche22.docking.org/search/smiles

**Endpoint da API**:
```bash
curl "https://cartblanche22.docking.org/[email protected]=4-Fadist=4"
```

**Parâmetros**:
- `smiles`: String SMILES de consulta (URL-encoded se necessário)
- `dist`: Limiar de distância Tanimoto (padrão: 0 para correspondência exata)
- `adist`: Parâmetro de distância alternativa para buscas mais amplas (padrão: 0)
- `output_fields`: Lista separada por vírgulas dos campos de saída desejados

**Exemplo - Correspondência exata**:
```bash
curl "https://cartblanche22.docking.org/smiles.txt:smiles=c1ccccc1"
```

**Exemplo - Busca por similaridade**:
```bash
curl "https://cartblanche22.docking.org/smiles.txt:smiles=c1ccccc1&dist=3&output_fields=zinc_id,smiles,tranche"
```

### 3. Busca por Códigos de Fornecedores

Consultar compostos de fornecedores químicos específicos ou recuperar todas as moléculas de catálogos particulares.

**Interface web**: https://cartblanche22.docking.org/search/catitems

**Endpoint da API**:
```bash
curl "https://cartblanche22.docking.org/catitems.txt:catitem_id=SUPPLIER-CODE-123"
```

**Casos de uso**:
- Verificar disponibilidade de compostos de fornecedores específicos
- Recuperar todos os compostos de um catálogo
- Correlacionar códigos de fornecedores com ZINC IDs

### 4. Amostragem Aleatória de Compostos

Gerar conjuntos aleatórios de compostos para triagem ou fins de benchmarking.

**Interface web**: https://cartblanche22.docking.org/search/random

**Endpoint da API**:
```bash
curl "https://cartblanche22.docking.org/substance/random.txt:count=100"
```

**Parâmetros**:
- `count`: Número de compostos aleatórios a recuperar (padrão: 100)
- `subset`: Filtrar por subset (ex: 'lead-like', 'drug-like', 'fragment')
- `output_fields`: Customizar campos de dados retornados

**Exemplo - Moléculas aleatórias do tipo lead**:
```bash
curl "https://cartblanche22.docking.org/substance/random.txt:count=1000&subset=lead-like&output_fields=zinc_id,smiles,tranche"
```

## Fluxos de Trabalho Comuns

### Fluxo de Trabalho 1: Preparando uma Biblioteca de Docking

1. **Definir critérios de busca** com base em propriedades alvo ou espaço químico desejado

2. **Consultar ZINC22** usando método apropriado:
   ```bash
   # Exemplo: Obter compostos drug-like com LogP e MW específicos
   curl "https://cartblanche22.docking.org/substance/random.txt:count=10000&subset=drug-like&output_fields=zinc_id,smiles,tranche" > docking_library.txt
   ```

3. **Analisar resultados** para extrair ZINC IDs e SMILES:
   ```python
   import pandas as pd

   # Carregar resultados
   df = pd.read_csv('docking_library.txt', sep='\t')

   # Filtrar por propriedades nos dados de tranche
   # Formato de tranche: H##P###M###-phase
   # H = doadores de ligação H, P = LogP*10, M = MW
   ```

4. **Baixar estruturas 3D** para docking usando ZINC ID ou baixar de repositórios de arquivos

### Fluxo de Trabalho 2: Encontrando Análogos de um Composto Ativo

1. **Obter SMILES** do composto ativo:
   ```python
   hit_smiles = "CC(C)Cc1ccc(cc1)C(C)C(=O)O"  # Exemplo: Ibuprofeno
   ```

2. **Realizar busca por similaridade** com limiar de distância:
   ```bash
   curl "https://cartblanche22.docking.org/smiles.txt:smiles=CC(C)Cc1ccc(cc1)C(C)C(=O)O&dist=5&output_fields=zinc_id,smiles,catalogs" > analogs.txt
   ```

3. **Analisar resultados** para identificar análogos compráveis:
   ```python
   import pandas as pd

   analogs = pd.read_csv('analogs.txt', sep='\t')
   print(f"Encontrados {len(analogs)} análogos")
   print(analogs[['zinc_id', 'smiles', 'catalogs']].head(10))
   ```

4. **Recuperar estruturas 3D** dos análogos mais promissores

### Fluxo de Trabalho 3: Recuperação em Lote de Compostos

1. **Compilar lista de ZINC IDs** da literatura, bancos de dados ou triagens anteriores:
   ```python
   zinc_ids = [
       "ZINC000000000001",
       "ZINC000000000002",
       "ZINC000000000003"
   ]
   zinc_ids_str = ",".join(zinc_ids)
   ```

2. **Consultar API ZINC22**:
   ```bash
   curl "https://cartblanche22.docking.org/substances.txt:zinc_id=ZINC000000000001,ZINC000000000002&output_fields=zinc_id,smiles,supplier_code,catalogs"
   ```

3. **Processar resultados** para análise downstream ou compra

### Fluxo de Trabalho 4: Amostragem do Espaço Químico

1. **Selecionar parâmetros de subset** com base em objetivos de triagem:
   - Fragment: MW < 250, bom para descoberta de fármacos baseada em fragmentos
   - Lead-like: MW 250-350, LogP ≤ 3.5
   - Drug-like: MW 350-500, segue a Regra dos Cinco de Lipinski

2. **Gerar amostra aleatória**:
   ```bash
   curl "https://cartblanche22.docking.org/substance/random.txt:count=5000&subset=lead-like&output_fields=zinc_id,smiles,tranche" > chemical_space_sample.txt
   ```

3. **Analisar diversidade química** e preparar para triagem virtual

## Campos de Saída

Customize respostas da API com o parâmetro `output_fields`:

**Campos disponíveis**:
- `zinc_id`: Identificador ZINC
- `smiles`: Representação string SMILES
- `sub_id`: ID de substância interno
- `supplier_code`: Número de catálogo do fornecedor
- `catalogs`: Lista de fornecedores oferecendo o composto
- `tranche`: Propriedades moleculares codificadas (contagem de H, LogP, MW, fase de reatividade)

**Exemplo**:
```bash
curl "https://cartblanche22.docking.org/substances.txt:zinc_id=ZINC000000000001&output_fields=zinc_id,smiles,catalogs,tranche"
```

## Sistema de Tranche

ZINC organiza compostos em "tranches" com base em propriedades moleculares:

**Formato**: `H##P###M###-phase`

- **H##**: Número de doadores de ligação de hidrogênio (00-99)
- **P###**: LogP × 10 (ex: P035 = LogP 3.5)
- **M###**: Peso molecular em Daltons (ex: M400 = 400 Da)
- **phase**: Classificação de reatividade

**Exemplo de tranche**: `H05P035M400-0`
- 5 doadores de ligação de H
- LogP = 3.5
- MW = 400 Da
- Fase de reatividade 0

Use dados de tranche para filtrar compostos por critérios de drug-likeness.

## Baixando Estruturas 3D

Para docking molecular, estruturas 3D estão disponíveis via repositórios de arquivos:

**Repositório de arquivos**: https://files.docking.org/zinc22/

Estruturas são organizadas por tranches e disponíveis em múltiplos formatos:
- MOL2: Formato multi-molécula com coordenadas 3D
- SDF: Formato de arquivo de estrutura-dados
- DB2.GZ: Formato de banco de dados comprimido para DOCK

Consulte a documentação ZINC em https://wiki.docking.org para protocolos de download e métodos de acesso em lote.

## Integração com Python

### Usando curl com Python

```python
import subprocess
import json

def query_zinc_by_id(zinc_id, output_fields="zinc_id,smiles,catalogs"):
    """Consulta ZINC22 por ZINC ID."""
    url = f"https://cartblanche22.docking.org/[email protected]_id={zinc_id}&output_fields={output_fields}"
    result = subprocess.run(['curl', url], capture_output=True, text=True)
    return result.stdout

def search_by_smiles(smiles, dist=0, adist=0, output_fields="zinc_id,smiles"):
    """Busca ZINC22 por SMILES com parâmetros de distância opcionais."""
    url = f"https://cartblanche22.docking.org/smiles.txt:smiles={smiles}&dist={dist}&adist={adist}&output_fields={output_fields}"
    result = subprocess.run(['curl', url], capture_output=True, text=True)
    return result.stdout

def get_random_compounds(count=100, subset=None, output_fields="zinc_id,smiles,tranche"):
    """Obter compostos aleatórios de ZINC22."""
    url = f"https://cartblanche22.docking.org/substance/random.txt:count={count}&output_fields={output_fields}"
    if subset:
        url += f"&subset={subset}"
    result = subprocess.run(['curl', url], capture_output=True, text=True)
    return result.stdout
```

### Analisando Resultados

```python
import pandas as pd
from io import StringIO

# Consultar ZINC e analisar como DataFrame
result = query_zinc_by_id("ZINC000000000001")
df = pd.read_csv(StringIO(result), sep='\t')

# Extrair propriedades de tranche
def parse_tranche(tranche_str):
    """Analisar código de tranche ZINC para extrair propriedades."""
    # Formato: H##P###M###-phase
    import re
    match = re.match(r'H(\d+)P(\d+)M(\d+)-(\d+)', tranche_str)
    if match:
        return {
            'h_donors': int(match.group(1)),
            'logP': int(match.group(2)) / 10.0,
            'mw': int(match.group(3)),
            'phase': int(match.group(4))
        }
    return None

df['tranche_props'] = df['tranche'].apply(parse_tranche)
```

## Melhores Práticas

### Otimização de Consultas

- **Comece específico**: Inicie com buscas exatas antes de expandir para buscas por similaridade
- **Use parâmetros de distância apropriados**: Valores pequenos de dist (1-3) para análogos próximos, maiores (5-10) para análogos diversos
- **Limite campos de saída**: Solicite apenas campos necessários para reduzir transferência de dados
- **Agrupe consultas**: Combine múltiplos ZINC IDs em uma única chamada da API quando possível

### Considerações de Performance

- **Rate limiting**: Respeite recursos do servidor; evite requisições consecutivas rápidas
- **Caching**: Armazene compostos acessados frequentemente localmente
- **Downloads paralelos**: Ao baixar estruturas 3D, use wget paralelo ou aria2c para repositórios de arquivos
- **Filtragem por subset**: Use subsets lead-like, drug-like ou fragment para reduzir espaço de busca

### Qualidade de Dados

- **Verifique disponibilidade**: Catálogos de fornecedores mudam; confirme disponibilidade de compostos antes de pedidos grandes
- **Verifique estereoquímica**: SMILES podem não especificar completamente estereoquímica; verifique estruturas 3D
- **Valide estruturas**: Use ferramentas de quimioinformática (RDKit, OpenBabel) para verificar validade de estrutura
- **Referência cruzada**: Quando possível, verifique com outros bancos de dados (PubChem, ChEMBL)

## Recursos

### references/api_reference.md

Documentação abrangente incluindo:

- Referência completa de endpoints da API
- Sintaxe de URL e especificações de parâmetros
- Padrões avançados de consulta e exemplos
- Organização e acesso do repositório de arquivos
- Métodos de download em massa
- Tratamento de erros e resolução de problemas
- Integração com software de docking molecular

Consulte este documento para informações técnicas detalhadas e padrões de uso avançado.

## Avisos Importantes

### Confiabilidade de Dados

ZINC declara explicitamente: **"Não garantimos a qualidade de qualquer molécula para qualquer propósito e não assumimos responsabilidade por erros decorrentes do uso deste banco de dados."**

- Disponibilidade de compostos pode mudar sem aviso
- Representações de estruturas podem conter erros
- Informações de fornecedores devem ser verificadas independentemente
- Use validação apropriada antes do trabalho experimental

### Uso Apropriado

- ZINC é destinado para fins acadêmicos e pesquisa em descoberta de fármacos
- Verifique termos de licença para uso comercial
- Respeite propriedade intelectual ao trabalhar com compostos patenteados
- Siga diretrizes da sua instituição para aquisição de compostos

## Recursos Adicionais

- **Website ZINC**: https://zinc.docking.org/
- **Interface CartBlanche22**: https://cartblanche22.docking.org/
- **Wiki ZINC**: https://wiki.docking.org/
- **Repositório de Arquivos**: https://files.docking.org/zinc22/
- **GitHub**: https://github.com/docking-org/
- **Publicação Primária**: Irwin et al., J. Chem. Inf. Model 2020 (ZINC15)
- **Publicação ZINC22**: Irwin et al., J. Chem. Inf. Model 2023

## Citações

Ao usar ZINC em publicações, cite a versão apropriada:

**ZINC22**:
Irwin, J. J., et al. "ZINC22—A Free Multi-Billion-Scale Database of Tangible Compounds for Ligand Discovery." *Journal of Chemical Information and Modeling* 2023.

**ZINC15**:
Irwin, J. J., et al. "ZINC15 – Ligand Discovery for Everyone." *Journal of Chemical Information and Modeling* 2020, 60, 6065–6073.