---
name: brenda-database
description: "Acesse o banco de dados de enzimas BRENDA via API SOAP. Recupere parâmetros cinéticos (Km, kcat), equações de reação, dados de organismos e informações de enzimas específicas de substrato para pesquisa bioquímica e análise de vias metabólicas."
---

# Banco de Dados BRENDA

## Visão Geral

BRENDA (BRaunschweig ENzyme DAtabase) é o sistema de informações de enzimas mais abrangente do mundo, contendo dados detalhados de enzimas da literatura científica. Consulte parâmetros cinéticos (Km, kcat), equações de reação, especificidades de substrato, informações de organismos e condições ótimas para enzimas usando a API SOAP oficial. Acesse mais de 45.000 enzimas com milhões de pontos de dados cinéticos para pesquisa bioquímica, engenharia metabólica e descoberta de enzimas.

## Quando Usar Esta Skill

Esta skill deve ser usada quando:
- Procurar por parâmetros cinéticos de enzimas (Km, kcat, Vmax)
- Recuperar equações de reação e estequiometria
- Encontrar enzimas para substratos ou reações específicos
- Comparar propriedades de enzimas em diferentes organismos
- Investigar pH, temperatura e condições ótimas
- Acessar dados de inibição e ativação de enzimas
- Apoiar reconstrução de vias metabólicas e retrossíntese
- Realizar estudos de engenharia e otimização de enzimas
- Analisar especificidade de substrato e requisitos de cofator

## Capacidades Principais

### 1. Recuperação de Parâmetros Cinéticos

Acesse dados cinéticos abrangentes para enzimas:

**Obter Valores de Km por Número EC**:
```python
from brenda_client import get_km_values

# Obter valores de Km para todos os organismos
km_data = get_km_values("1.1.1.1")  # Álcool desidrogenase

# Obter valores de Km para organismo específico
km_data = get_km_values("1.1.1.1", organism="Saccharomyces cerevisiae")

# Obter valores de Km para substrato específico
km_data = get_km_values("1.1.1.1", substrate="ethanol")
```

**Analisar Resultados de Km**:
```python
for entry in km_data:
    print(f"Km: {entry}")
    # Exemplo de saída: "organism*Homo sapiens#substrate*ethanol#kmValue*1.2#commentary*"
```

**Extrair Informações Específicas**:
```python
from scripts.brenda_queries import parse_km_entry, extract_organism_data

for entry in km_data:
    parsed = parse_km_entry(entry)
    organism = extract_organism_data(entry)
    print(f"Organismo: {parsed['organism']}")
    print(f"Substrato: {parsed['substrate']}")
    print(f"Valor Km: {parsed['km_value']}")
    print(f"pH: {parsed.get('ph', 'N/A')}")
    print(f"Temperatura: {parsed.get('temperature', 'N/A')}")
```

### 2. Informações de Reação

Recupere equações de reação e detalhes:

**Obter Reações por Número EC**:
```python
from brenda_client import get_reactions

# Obter todas as reações para número EC
reactions = get_reactions("1.1.1.1")

# Filtrar por organismo
reactions = get_reactions("1.1.1.1", organism="Escherichia coli")

# Pesquisar reação específica
reactions = get_reactions("1.1.1.1", reaction="ethanol + NAD+")
```

**Processar Dados de Reação**:
```python
from scripts.brenda_queries import parse_reaction_entry, extract_substrate_products

for reaction in reactions:
    parsed = parse_reaction_entry(reaction)
    substrates, products = extract_substrate_products(reaction)

    print(f"Reação: {parsed['reaction']}")
    print(f"Organismo: {parsed['organism']}")
    print(f"Substratos: {substrates}")
    print(f"Produtos: {products}")
```

### 3. Descoberta de Enzimas

Encontre enzimas para transformações bioquímicas específicas:

**Encontrar Enzimas por Substrato**:
```python
from scripts.brenda_queries import search_enzymes_by_substrate

# Encontrar enzimas que atuam em glicose
enzymes = search_enzymes_by_substrate("glucose", limit=20)

for enzyme in enzymes:
    print(f"EC: {enzyme['ec_number']}")
    print(f"Nome: {enzyme['enzyme_name']}")
    print(f"Reação: {enzyme['reaction']}")
```

**Encontrar Enzimas por Produto**:
```python
from scripts.brenda_queries import search_enzymes_by_product

# Encontrar enzimas que produzem lactato
enzymes = search_enzymes_by_product("lactate", limit=10)
```

**Pesquisar por Padrão de Reação**:
```python
from scripts.brenda_queries import search_by_pattern

# Encontrar reações de oxidação
enzymes = search_by_pattern("oxidation", limit=15)
```

### 4. Dados de Enzimas Específicos de Organismos

Compare propriedades de enzimas em diferentes organismos:

**Obter Dados de Enzimas para Múltiplos Organismos**:
```python
from scripts.brenda_queries import compare_across_organisms

organisms = ["Escherichia coli", "Saccharomyces cerevisiae", "Homo sapiens"]
comparison = compare_across_organisms("1.1.1.1", organisms)

for org_data in comparison:
    print(f"Organismo: {org_data['organism']}")
    print(f"Km médio: {org_data['average_km']}")
    print(f"pH ótimo: {org_data['optimal_ph']}")
    print(f"Intervalo de temperatura: {org_data['temperature_range']}")
```

**Encontrar Organismos com Enzima Específica**:
```python
from scripts.brenda_queries import get_organisms_for_enzyme

organisms = get_organisms_for_enzyme("6.3.5.5")  # Glutamina sintetase
print(f"Encontrados {len(organisms)} organismos com esta enzima")
```

### 5. Parâmetros Ambientais

Acesse condições ótimas e parâmetros ambientais:

**Obter Dados de pH e Temperatura**:
```python
from scripts.brenda_queries import get_environmental_parameters

params = get_environmental_parameters("1.1.1.1")

print(f"Intervalo de pH ótimo: {params['ph_range']}")
print(f"Temperatura ótima: {params['optimal_temperature']}")
print(f"pH de estabilidade: {params['stability_ph']}")
print(f"Estabilidade de temperatura: {params['temperature_stability']}")
```

**Requisitos de Cofator**:
```python
from scripts.brenda_queries import get_cofactor_requirements

cofactors = get_cofactor_requirements("1.1.1.1")
for cofactor in cofactors:
    print(f"Cofator: {cofactor['name']}")
    print(f"Tipo: {cofactor['type']}")
    print(f"Concentração: {cofactor['concentration']}")
```

### 6. Especificidade de Substrato

Analise as preferências de substrato da enzima:

**Obter Dados de Especificidade de Substrato**:
```python
from scripts.brenda_queries import get_substrate_specificity

specificity = get_substrate_specificity("1.1.1.1")

for substrate in specificity:
    print(f"Substrato: {substrate['name']}")
    print(f"Km: {substrate['km']}")
    print(f"Vmax: {substrate['vmax']}")
    print(f"kcat: {substrate['kcat']}")
    print(f"Constante de especificidade: {substrate['kcat_km_ratio']}")
```

**Comparar Preferências de Substrato**:
```python
from scripts.brenda_queries import compare_substrate_affinity

comparison = compare_substrate_affinity("1.1.1.1")
sorted_by_km = sorted(comparison, key=lambda x: x['km'])

for substrate in sorted_by_km[:5]:  # Top 5 menores Km
    print(f"{substrate['name']}: Km = {substrate['km']}")
```

### 7. Inibição e Ativação

Acesse dados de regulação de enzimas:

**Obter Informações de Inibidor**:
```python
from scripts.brenda_queries import get_inhibitors

inhibitors = get_inhibitors("1.1.1.1")

for inhibitor in inhibitors:
    print(f"Inibidor: {inhibitor['name']}")
    print(f"Tipo: {inhibitor['type']}")
    print(f"Ki: {inhibitor['ki']}")
    print(f"IC50: {inhibitor['ic50']}")
```

**Obter Informações de Ativador**:
```python
from scripts.brenda_queries import get_activators

activators = get_activators("1.1.1.1")

for activator in activators:
    print(f"Ativador: {activator['name']}")
    print(f"Efeito: {activator['effect']}")
    print(f"Mecanismo: {activator['mechanism']}")
```

### 8. Suporte a Engenharia de Enzimas

Encontre alvo de engenharia e alternativas:

**Encontrar Homólogos Termófilos**:
```python
from scripts.brenda_queries import find_thermophilic_homologs

thermophilic = find_thermophilic_homologs("1.1.1.1", min_temp=50)

for enzyme in thermophilic:
    print(f"Organismo: {enzyme['organism']}")
    print(f"Temp ótima: {enzyme['optimal_temperature']}")
    print(f"Km: {enzyme['km']}")
```

**Encontrar Variantes Estáveis em pH Alcalino/Ácido**:
```python
from scripts.brenda_queries import find_ph_stable_variants

alkaline = find_ph_stable_variants("1.1.1.1", min_ph=8.0)
acidic = find_ph_stable_variants("1.1.1.1", max_ph=6.0)
```

### 9. Modelagem Cinética

Prepare dados para modelagem cinética:

**Obter Parâmetros Cinéticos para Modelagem**:
```python
from scripts.brenda_queries import get_modeling_parameters

model_data = get_modeling_parameters("1.1.1.1", substrate="ethanol")

print(f"Km: {model_data['km']}")
print(f"Vmax: {model_data['vmax']}")
print(f"kcat: {model_data['kcat']}")
print(f"Concentração de enzima: {model_data['enzyme_conc']}")
print(f"Temperatura: {model_data['temperature']}")
print(f"pH: {model_data['ph']}")
```

**Gerar Gráficos de Michaelis-Menten**:
```python
from scripts.brenda_visualization import plot_michaelis_menten

# Gerar gráficos cinéticos
plot_michaelis_menten("1.1.1.1", substrate="ethanol")
```

## Requisitos de Instalação

```bash
uv pip install zeep requests pandas matplotlib seaborn
```

## Configuração de Autenticação

BRENDA requer credenciais de autenticação:

1. **Criar arquivo .env**:
```
BRENDA_EMAIL=seu.email@exemplo.com
BRENDA_PASSWORD=sua_senha_brenda
```

2. **Ou definir variáveis de ambiente**:
```bash
export BRENDA_EMAIL="seu.email@exemplo.com"
export BRENDA_PASSWORD="sua_senha_brenda"
```

3. **Registre-se para acesso BRENDA**:
   - Visite https://www.brenda-enzymes.org/
   - Crie uma conta
   - Verifique seu email para credenciais
   - Nota: Há também `BRENDA_EMIAL` (note o typo) para suporte legado

## Scripts Auxiliares

Esta skill inclui scripts Python abrangentes para consultas ao banco de dados BRENDA:

### scripts/brenda_queries.py

Fornece funções de alto nível para análise de dados de enzimas:

**Funções Principais**:
- `parse_km_entry(entry)`: Analisar entradas de dados Km de BRENDA
- `parse_reaction_entry(entry)`: Analisar entradas de dados de reação
- `extract_organism_data(entry)`: Extrair informações específicas de organismos
- `search_enzymes_by_substrate(substrate, limit)`: Encontrar enzimas para substratos
- `search_enzymes_by_product(product, limit)`: Encontrar enzimas que produzem produtos
- `compare_across_organisms(ec_number, organisms)`: Comparar propriedades de enzimas
- `get_environmental_parameters(ec_number)`: Obter dados de pH e temperatura
- `get_cofactor_requirements(ec_number)`: Obter informações de cofator
- `get_substrate_specificity(ec_number)`: Analisar preferências de substrato
- `get_inhibitors(ec_number)`: Obter dados de inibição de enzimas
- `get_activators(ec_number)`: Obter dados de ativação de enzimas
- `find_thermophilic_homologs(ec_number, min_temp)`: Encontrar variantes resistentes ao calor
- `get_modeling_parameters(ec_number, substrate)`: Obter parâmetros para modelagem cinética
- `export_kinetic_data(ec_number, format, filename)`: Exportar dados para arquivo

**Uso**:
```python
from scripts.brenda_queries import search_enzymes_by_substrate, compare_across_organisms

# Pesquisar enzimas
enzymes = search_enzymes_by_substrate("glucose", limit=20)

# Comparar entre organismos
comparison = compare_across_organisms("1.1.1.1", ["E. coli", "S. cerevisiae"])
```

### scripts/brenda_visualization.py

Fornece funções de visualização para dados de enzimas:

**Funções Principais**:
- `plot_kinetic_parameters(ec_number)`: Plotar distribuições de Km e kcat
- `plot_organism_comparison(ec_number, organisms)`: Comparar organismos
- `plot_pH_profiles(ec_number)`: Plotar perfis de atividade de pH
- `plot_temperature_profiles(ec_number)`: Plotar perfis de atividade de temperatura
- `plot_substrate_specificity(ec_number)`: Visualizar preferências de substrato
- `plot_michaelis_menten(ec_number, substrate)`: Gerar curvas cinéticas
- `create_heatmap_data(enzymes, parameters)`: Criar dados para mapas de calor
- `generate_summary_plots(ec_number)`: Criar visão geral abrangente de enzima

**Uso**:
```python
from scripts.brenda_visualization import plot_kinetic_parameters, plot_michaelis_menten

# Plotar parâmetros cinéticos
plot_kinetic_parameters("1.1.1.1")

# Gerar curva de Michaelis-Menten
plot_michaelis_menten("1.1.1.1", substrate="ethanol")
```

### scripts/enzyme_pathway_builder.py

Construa vias enzimáticas e rotas retrossintéticas:

**Funções Principais**:
- `find_pathway_for_product(product, max_steps)`: Encontrar vias enzimáticas
- `build_retrosynthetic_tree(target, depth)`: Construir árvore retrossintética
- `suggest_enzyme_substitutions(ec_number, criteria)`: Sugerir alternativas de enzimas
- `calculate_pathway_feasibility(pathway)`: Avaliar viabilidade de via
- `optimize_pathway_conditions(pathway)`: Sugerir condições ótimas
- `generate_pathway_report(pathway, filename)`: Criar relatório detalhado de via

**Uso**:
```python
from scripts.enzyme_pathway_builder import find_pathway_for_product, build_retrosynthetic_tree

# Encontrar via para produto
pathway = find_pathway_for_product("lactate", max_steps=3)

# Construir árvore retrossintética
tree = build_retrosynthetic_tree("lactate", depth=2)
```

## Limites de Taxa de API e Boas Práticas

**Limites de Taxa**:
- A API BRENDA tem limite de taxa moderado
- Recomendado: 1 requisição por segundo para uso sustentado
- Máximo: 5 requisições a cada 10 segundos

**Boas Práticas**:
1. **Cache de resultados**: Armazene dados de enzimas frequentemente acessados localmente
2. **Consultas em lote**: Combine requisições relacionadas quando possível
3. **Use buscas específicas**: Reduza por organismo, substrato quando possível
4. **Manipule dados ausentes**: Nem todas as enzimas têm dados completos
5. **Valide números EC**: Garanta que números EC estejam em formato correto
6. **Implemente atrasos**: Adicione atrasos entre requisições consecutivas
7. **Use wildcards com sabedoria**: Use '*' para buscas mais amplas quando apropriado
8. **Monitore cota**: Rastreie seu uso de API

**Tratamento de Erros**:
```python
from brenda_client import get_km_values, get_reactions
from zeep.exceptions import Fault, TransportError

try:
    km_data = get_km_values("1.1.1.1")
except RuntimeError as e:
    print(f"Erro de autenticação: {e}")
except Fault as e:
    print(f"Erro de API BRENDA: {e}")
except TransportError as e:
    print(f"Erro de rede: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
```

## Fluxos de Trabalho Comuns

### Fluxo de Trabalho 1: Descoberta de Enzimas para Novo Substrato

Encontre enzimas adequadas para um substrato específico:

```python
from brenda_client import get_km_values
from scripts.brenda_queries import search_enzymes_by_substrate, compare_substrate_affinity

# Pesquisar enzimas que atuam em substrato
substrate = "2-phenylethanol"
enzymes = search_enzymes_by_substrate(substrate, limit=15)

print(f"Encontradas {len(enzymes)} enzimas para {substrate}")
for enzyme in enzymes:
    print(f"EC {enzyme['ec_number']}: {enzyme['enzyme_name']}")

# Obter dados cinéticos para melhores candidatos
if enzymes:
    best_ec = enzymes[0]['ec_number']
    km_data = get_km_values(best_ec, substrate=substrate)

    if km_data:
        print(f"Dados cinéticos para {best_ec}:")
        for entry in km_data[:3]:  # Primeiras 3 entradas
            print(f"  {entry}")
```

### Fluxo de Trabalho 2: Comparação de Enzimas Entre Organismos

Compare propriedades de enzimas em diferentes organismos:

```python
from scripts.brenda_queries import compare_across_organisms, get_environmental_parameters

# Definir organismos para comparação
organisms = [
    "Escherichia coli",
    "Saccharomyces cerevisiae",
    "Bacillus subtilis",
    "Thermus thermophilus"
]

# Comparar álcool desidrogenase
comparison = compare_across_organisms("1.1.1.1", organisms)

print("Comparação entre organismos:")
for org_data in comparison:
    print(f"\n{org_data['organism']}:")
    print(f"  Km médio: {org_data['average_km']}")
    print(f"  pH ótimo: {org_data['optimal_ph']}")
    print(f"  Temperatura: {org_data['optimal_temperature']}°C")

# Obter parâmetros ambientais detalhados
env_params = get_environmental_parameters("1.1.1.1")
print(f"\nIntervalo de pH ótimo geral: {env_params['ph_range']}")
```

### Fluxo de Trabalho 3: Identificação de Alvo de Engenharia de Enzimas

Encontre oportunidades de engenharia para melhoria de enzimas:

```python
from scripts.brenda_queries import (
    find_thermophilic_homologs,
    find_ph_stable_variants,
    compare_substrate_affinity
)

# Encontrar variantes termófilas para estabilidade térmica
thermophilic = find_thermophilic_homologs("1.1.1.1", min_temp=50)
print(f"Encontradas {len(thermophilic)} variantes termófilas")

# Encontrar variantes estáveis em pH alcalino
alkaline = find_ph_stable_variants("1.1.1.1", min_ph=8.0)
print(f"Encontradas {len(alkaline)} variantes estáveis em pH alcalino")

# Comparar especificidades de substrato para alvos de engenharia
specificity = compare_substrate_affinity("1.1.1.1")
print("Classificação de afinidade de substrato:")
for i, sub in enumerate(specificity[:5]):
    print(f"  {i+1}. {sub['name']}: Km = {sub['km']}")
```

### Fluxo de Trabalho 4: Construção de Via Enzimática

Construa vias de síntese enzimática:

```python
from scripts.enzyme_pathway_builder import (
    find_pathway_for_product,
    build_retrosynthetic_tree,
    calculate_pathway_feasibility
)

# Encontrar via para produto alvo
target = "lactate"
pathway = find_pathway_for_product(target, max_steps=3)

if pathway:
    print(f"Via encontrada para {target}:")
    for i, step in enumerate(pathway['steps']):
        print(f"  Etapa {i+1}: {step['reaction']}")
        print(f"    Enzima: EC {step['ec_number']}")
        print(f"    Organismo: {step['organism']}")

# Avaliar viabilidade de via
feasibility = calculate_pathway_feasibility(pathway)
print(f"\nPontuação de viabilidade de via: {feasibility['score']}/10")
print(f"Possíveis problemas: {feasibility['warnings']}")
```

### Fluxo de Trabalho 5: Análise de Parâmetros Cinéticos

Análise cinética abrangente para seleção de enzimas:

```python
from brenda_client import get_km_values
from scripts.brenda_queries import parse_km_entry, get_modeling_parameters
from scripts.brenda_visualization import plot_kinetic_parameters

# Obter dados cinéticos abrangentes
ec_number = "1.1.1.1"
km_data = get_km_values(ec_number)

# Analisar parâmetros cinéticos
all_entries = []
for entry in km_data:
    parsed = parse_km_entry(entry)
    if parsed['km_value']:
        all_entries.append(parsed)

print(f"Analisadas {len(all_entries)} entradas cinéticas")

# Encontrar melhor desempenho cinético
best_km = min(all_entries, key=lambda x: x['km_value'])
print(f"\nMelhor desempenho cinético:")
print(f"  Organismo: {best_km['organism']}")
print(f"  Substrato: {best_km['substrate']}")
print(f"  Km: {best_km['km_value']}")

# Obter parâmetros de modelagem
model_data = get_modeling_parameters(ec_number, substrate=best_km['substrate'])
print(f"\nParâmetros de modelagem:")
print(f"  Km: {model_data['km']}")
print(f"  kcat: {model_data['kcat']}")
print(f"  Vmax: {model_data['vmax']}")

# Gerar visualização
plot_kinetic_parameters(ec_number)
```

### Fluxo de Trabalho 6: Seleção de Enzima Industrial

Selecione enzimas para aplicações industriais:

```python
from scripts.brenda_queries import (
    find_thermophilic_homologs,
    get_environmental_parameters,
    get_inhibitors
)

# Critérios industriais: alta tolerância de temperatura, resistência a solventes orgânicos
target_enzyme = "1.1.1.1"

# Encontrar variantes termófilas
thermophilic = find_thermophilic_homologs(target_enzyme, min_temp=60)
print(f"Candidatos termófilos: {len(thermophilic)}")

# Verificar tolerância a solvente (dados de inibidor)
inhibitors = get_inhibitors(target_enzyme)
solvent_tolerant = [
    inv for inv in inhibitors
    if 'ethanol' not in inv['name'].lower() and
       'methanol' not in inv['name'].lower()
]

print(f"Candidatos tolerantes a solvente: {len(solvent_tolerant)}")

# Avaliar principais candidatos
for candidate in thermophilic[:3]:
    print(f"\nCandidato: {candidate['organism']}")
    print(f"  Temp ótima: {candidate['optimal_temperature']}°C")
    print(f"  Km: {candidate['km']}")
    print(f"  Intervalo de pH: {candidate.get('ph_range', 'N/A')}")
```

## Formatos de Dados e Análise

### Formato de Resposta BRENDA

BRENDA retorna dados em formatos específicos que precisam de análise:

**Formato de Valor Km**:
```
organism*Escherichia coli#substrate*ethanol#kmValue*1.2#kmValueMaximum*#commentary*pH 7.4, 25°C#ligandStructureId*#literature*
```

**Formato de Reação**:
```
ecNumber*1.1.1.1#organism*Saccharomyces cerevisiae#reaction*ethanol + NAD+ <=> acetaldehyde + NADH + H+#commentary*#literature*
```

### Padrões de Extração de Dados

```python
import re

def parse_brenda_field(data, field_name):
    """Extrair campo específico da entrada de dados BRENDA"""
    pattern = f"{field_name}\\*([^#]*)"
    match = re.search(pattern, data)
    return match.group(1) if match else None

def extract_multiple_values(data, field_name):
    """Extrair múltiplos valores para um campo"""
    pattern = f"{field_name}\\*([^#]*)"
    matches = re.findall(pattern, data)
    return [match for match in matches if match.strip()]
```

## Documentação de Referência

Para documentação detalhada de BRENDA, consulte `references/api_reference.md`. Isto inclui:
- Documentação completa do método API SOAP
- Listas completas de parâmetros e formatos
- Estrutura de números EC e validação
- Especificações de formato de resposta
- Códigos de erro e tratamento
- Definições de campos de dados
- Formatos de citação de literatura

## Solução de Problemas

**Erros de Autenticação**:
- Verifique BRENDA_EMAIL e BRENDA_PASSWORD no arquivo .env
- Verifique ortografia correta (note suporte legado BRENDA_EMIAL)
- Garanta que a conta BRENDA está ativa e tem acesso à API

**Nenhum Resultado Retornado**:
- Tente buscas mais amplas com wildcards (*)
- Verifique formato do número EC (ex: "1.1.1.1" não "1.1.1")
- Verifique ortografia e nomenclatura do substrato
- Algumas enzimas podem ter dados limitados em BRENDA

**Limitação de Taxa**:
- Adicione atrasos entre requisições (0,5-1 segundo)
- Cache de resultados localmente
- Use consultas mais específicas para reduzir volume de dados
- Considere operações em lote para múltiplas consultas

**Erros de Rede**:
- Verifique conexão de internet
- Servidor BRENDA pode estar temporariamente indisponível
- Tente novamente após alguns minutos
- Considere usar VPN se houver restrição geográfica

**Problemas de Formato de Dados**:
- Use funções de análise fornecidas em scripts
- Dados BRENDA podem ser inconsistentes em formatação
- Manipule campos ausentes com graça
- Valide dados analisados antes do uso

**Problemas de Desempenho**:
- Consultas grandes podem ser lentas; limite escopo de busca
- Use filtros específicos de organismo ou substrato
- Considere processamento assíncrono para operações em lote
- Monitore uso de memória com conjuntos de dados grandes

## Recursos Adicionais

- BRENDA Home: https://www.brenda-enzymes.org/
- Documentação API SOAP BRENDA: https://www.brenda-enzymes.org/soap.php
- Números de Comissão de Enzimas (EC): https://www.qmul.ac.uk/sbcs/iubmb/enzyme/
- Cliente SOAP Zeep: https://python-zeep.readthedocs.io/
- Nomenclatura de Enzimas: https://www.iubmb.org/enzyme/