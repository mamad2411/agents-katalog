---
name: datacommons-client
description: Trabalhe com Data Commons, uma plataforma que fornece acesso programático a dados estatísticos públicos de fontes globais. Use essa skill ao trabalhar com dados demográficos, indicadores econômicos, estatísticas de saúde, dados ambientais ou qualquer conjunto de dados público disponível através de Data Commons. Aplicável para consultar estatísticas populacionais, números de PIB, taxas de desemprego, prevalência de doenças, resolução de entidades geográficas e explorar relacionamentos entre entidades estatísticas.
---

# Data Commons Client

## Visão Geral

Fornece acesso abrangente à API Python v2 do Data Commons para consultar observações estatísticas, explorar o grafo de conhecimento e resolver identificadores de entidades. Data Commons agrega dados de órgãos de censo, organizações de saúde, agências ambientais e outras fontes autoritárias em um grafo de conhecimento unificado.

## Instalação

Instale o cliente Python Data Commons com suporte a Pandas:

```bash
uv pip install "datacommons-client[Pandas]"
```

Para uso básico sem Pandas:
```bash
uv pip install datacommons-client
```

## Capacidades Principais

A API do Data Commons consiste em três endpoints principais, cada um detalhado em arquivos de referência dedicados:

### 1. Endpoint de Observação - Consultas de Dados Estatísticos

Consulte dados estatísticos de série temporal para entidades. Veja `references/observation.md` para documentação abrangente.

**Casos de uso primários:**
- Recuperar estatísticas de população, economia, saúde ou meio ambiente
- Acessar dados de série temporal histórica para análise de tendências
- Consultar dados para hierarquias (todos os condados em um estado, todos os países em uma região)
- Comparar estatísticas entre múltiplas entidades
- Filtrar por fonte de dados para consistência

**Padrões comuns:**
```python
from datacommons_client import DataCommonsClient

client = DataCommonsClient()

# Obter dados de população mais recentes
response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=["geoId/06"],  # California
    date="latest"
)

# Obter série temporal
response = client.observation.fetch(
    variable_dcids=["UnemploymentRate_Person"],
    entity_dcids=["country/USA"],
    date="all"
)

# Consultar por hierarquia
response = client.observation.fetch(
    variable_dcids=["MedianIncome_Household"],
    entity_expression="geoId/06<-containedInPlace+{typeOf:County}",
    date="2020"
)
```

### 2. Endpoint de Node - Exploração de Grafo de Conhecimento

Explore relacionamentos de entidades e propriedades dentro do grafo de conhecimento. Veja `references/node.md` para documentação abrangente.

**Casos de uso primários:**
- Descobrir propriedades disponíveis para entidades
- Navegar hierarquias geográficas (relacionamentos pai/filho)
- Recuperar nomes e metadados de entidades
- Explorar conexões entre entidades
- Listar todos os tipos de entidades no grafo

**Padrões comuns:**
```python
# Descobrir propriedades
labels = client.node.fetch_property_labels(
    node_dcids=["geoId/06"],
    out=True
)

# Navegar hierarquia
children = client.node.fetch_place_children(
    node_dcids=["country/USA"]
)

# Obter nomes de entidades
names = client.node.fetch_entity_names(
    node_dcids=["geoId/06", "geoId/48"]
)
```

### 3. Endpoint de Resolve - Identificação de Entidades

Traduza nomes de entidades, coordenadas ou IDs externos para IDs do Data Commons (DCIDs). Veja `references/resolve.md` para documentação abrangente.

**Casos de uso primários:**
- Converter nomes de lugares em DCIDs para consultas
- Resolver coordenadas para lugares
- Mapear IDs do Wikidata para entidades do Data Commons
- Lidar com nomes de entidades ambíguos

**Padrões comuns:**
```python
# Resolver por nome
response = client.resolve.fetch_dcids_by_name(
    names=["California", "Texas"],
    entity_type="State"
)

# Resolver por coordenadas
dcid = client.resolve.fetch_dcid_by_coordinates(
    latitude=37.7749,
    longitude=-122.4194
)

# Resolver IDs do Wikidata
response = client.resolve.fetch_dcids_by_wikidata_id(
    wikidata_ids=["Q30", "Q99"]
)
```

## Fluxo de Trabalho Típico

A maioria das consultas do Data Commons segue este padrão:

1. **Resolver entidades** (se começar com nomes):
   ```python
   resolve_response = client.resolve.fetch_dcids_by_name(
       names=["California", "Texas"]
   )
   dcids = [r["candidates"][0]["dcid"]
            for r in resolve_response.to_dict().values()
            if r["candidates"]]
   ```

2. **Descobrir variáveis disponíveis** (opcional):
   ```python
   variables = client.observation.fetch_available_statistical_variables(
       entity_dcids=dcids
   )
   ```

3. **Consultar dados estatísticos**:
   ```python
   response = client.observation.fetch(
       variable_dcids=["Count_Person", "UnemploymentRate_Person"],
       entity_dcids=dcids,
       date="latest"
   )
   ```

4. **Processar resultados**:
   ```python
   # Como dicionário
   data = response.to_dict()

   # Como DataFrame do Pandas
   df = response.to_observations_as_records()
   ```

## Encontrando Variáveis Estatísticas

Variáveis estatísticas usam padrões de nomenclatura específicos no Data Commons:

**Padrões de variáveis comuns:**
- `Count_Person` - População total
- `Count_Person_Female` - População feminina
- `UnemploymentRate_Person` - Taxa de desemprego
- `Median_Income_Household` - Renda mediana de domicílios
- `Count_Death` - Contagem de mortes
- `Median_Age_Person` - Idade mediana

**Métodos de descoberta:**
```python
# Verificar quais variáveis estão disponíveis para uma entidade
available = client.observation.fetch_available_statistical_variables(
    entity_dcids=["geoId/06"]
)

# Ou explore através da interface web
# https://datacommons.org/tools/statvar
```

## Trabalhando com Pandas

Todas as respostas de observação se integram com Pandas:

```python
response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=["geoId/06", "geoId/48"],
    date="all"
)

# Converter para DataFrame
df = response.to_observations_as_records()
# Colunas: date, entity, variable, value

# Remodelar para análise
pivot = df.pivot_table(
    values='value',
    index='date',
    columns='entity'
)
```

## Autenticação da API

**Para datacommons.org (padrão):**
- Uma chave de API é necessária
- Defina através de variável de ambiente: `export DC_API_KEY="sua_chave"`
- Ou passe ao inicializar: `client = DataCommonsClient(api_key="sua_chave")`
- Solicite chaves em: https://apikeys.datacommons.org/

**Para instâncias personalizadas de Data Commons:**
- Nenhuma chave de API necessária
- Especifique endpoint personalizado: `client = DataCommonsClient(url="https://custom.datacommons.org")`

## Documentação de Referência

Documentação abrangente para cada endpoint está disponível no diretório `references/`:

- **`references/observation.md`**: Documentação completa da API de Observação com todos os métodos, parâmetros, formatos de resposta e casos de uso comuns
- **`references/node.md`**: Documentação completa da API de Node para exploração de grafos, consultas de propriedades e navegação de hierarquias
- **`references/resolve.md`**: Documentação completa da API de Resolve para identificação de entidades e resolução de DCID
- **`references/getting_started.md`**: Guia de início rápido com exemplos completos e padrões comuns

## Recursos Adicionais

- **Documentação Oficial**: https://docs.datacommons.org/api/python/v2/
- **Explorador de Variáveis Estatísticas**: https://datacommons.org/tools/statvar
- **Navegador Data Commons**: https://datacommons.org/browser/
- **Repositório GitHub**: https://github.com/datacommonsorg/api-python

## Dicas para Uso Efetivo

1. **Sempre comece com resolução**: Converta nomes em DCIDs antes de consultar dados
2. **Use expressões de relação para hierarquias**: Consulte todos os filhos de uma vez em vez de consultas individuais
3. **Verifique a disponibilidade de dados primeiro**: Use `fetch_available_statistical_variables()` para ver o que é consultável
4. **Aproveite a integração com Pandas**: Converta respostas em DataFrames para análise
5. **Armazene resoluções em cache**: Se consultar as mesmas entidades repetidamente, guarde os mapeamentos nome→DCID
6. **Filtre por faceta para consistência**: Use `filter_facet_domains` para garantir dados da mesma fonte
7. **Leia os docs de referência**: Cada endpoint tem documentação extensa no diretório `references/`