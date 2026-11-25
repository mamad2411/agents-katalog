---
name: cocoindex
description: Kit de ferramentas abrangente para desenvolvimento com a biblioteca CocoIndex. Use quando os usuários precisarem criar pipelines de transformação de dados (flows), escrever funções personalizadas ou operar flows via CLI ou API. Abrange a construção de workflows ETL para processamento de dados de IA, incluindo incorporação de documentos em bancos de dados vetoriais, construção de grafos de conhecimento, criação de índices de busca ou processamento de fluxos de dados com atualizações incrementais.
---

# CocoIndex

## Visão Geral

CocoIndex é um framework de transformação de dados em tempo real ultra-performático para IA com processamento incremental. Essa habilidade permite construir **flows de indexação** que extraem dados de fontes, aplicam transformações (chunking, embedding, extração via LLM) e exportam para destinos (bancos de dados vetoriais, grafos de conhecimento, bancos de dados relacionais).

**Capacidades principais:**

1. **Escrever flows de indexação** - Definir pipelines ETL usando Python
2. **Criar funções personalizadas** - Construir lógica de transformação reutilizável
3. **Operar flows** - Executar e gerenciar flows usando CLI ou API Python

**Recursos principais:**

- Processamento incremental (processa apenas dados alterados)
- Atualizações em tempo real (sincroniza continuamente mudanças da fonte para destinos)
- Funções integradas (chunking de texto, embeddings, extração via LLM)
- Múltiplas fontes de dados (arquivos locais, S3, Azure Blob, Google Drive, Postgres)
- Múltiplos destinos (Postgres+pgvector, Qdrant, LanceDB, Neo4j, Kuzu)

**Para documentação detalhada:** <https://cocoindex.io/docs/>
**Buscar na documentação:** <https://cocoindex.io/docs/search?q=url%20encoded%20keyword>

## Quando Usar Essa Habilidade

Use quando os usuários solicitarem:

- "Construir um índice de busca vetorial para meus documentos"
- "Criar um pipeline de embeddings para código/PDFs/imagens"
- "Extrair informações estruturadas usando LLMs"
- "Construir um grafo de conhecimento a partir de documentos"
- "Configurar indexação de documentos em tempo real"
- "Criar funções de transformação personalizadas"
- "Executar/atualizar meu flow CocoIndex"

## Workflow de Escrita de Flow

### Passo 1: Entender os Requisitos

Faça perguntas esclarecedoras para compreender:

**Fonte de dados:**

- Onde estão os dados? (arquivos locais, S3, banco de dados, etc.)
- Quais tipos de arquivo? (texto, PDF, JSON, imagens, código, etc.)
- Com que frequência mudam? (uma vez, periódico, contínuo)

**Transformações:**

- Qual processamento é necessário? (chunking, embedding, extração, etc.)
- Qual modelo de embedding? (SentenceTransformer, OpenAI, customizado)
- Alguma lógica customizada? (filtragem, parsing, enriquecimento)

**Destino:**

- Para onde devem ir os resultados? (Postgres, Qdrant, Neo4j, etc.)
- Qual schema? (campos, chaves primárias, índices)
- Busca vetorial necessária? (especificar métrica de similaridade)

### Passo 2: Configurar Dependências

Oriente o usuário a adicionar CocoIndex com extras apropriados ao seu projeto com base em suas necessidades:

**Dependência obrigatória:**

- `cocoindex` - Funcionalidade principal, CLI e a maioria das funções integradas

**Extras opcionais (adicione conforme necessário):**

- `cocoindex[embeddings]` - Para embeddings SentenceTransformer (ao usar `SentenceTransformerEmbed`)
- `cocoindex[colpali]` - Para embeddings ColPali de imagens/documentos (ao usar `ColPaliEmbedImage` ou `ColPaliEmbedQuery`)
- `cocoindex[lancedb]` - Para destino LanceDB (ao exportar para LanceDB)
- `cocoindex[embeddings,lancedb]` - Múltiplos extras podem ser combinados

**O que está incluído:**

- Pacote base: Funcionalidade principal, CLI, a maioria das funções integradas, destinos Postgres/Qdrant/Neo4j/Kuzu
- Extra `embeddings`: Biblioteca SentenceTransformers para modelos de embedding locais
- Extra `colpali`: Engine ColPali para embeddings de documentos/imagens multimodais
- Extra `lancedb`: Biblioteca cliente LanceDB para suporte a banco de dados vetorial LanceDB

Usuários podem instalar usando seu gerenciador de pacotes preferido (pip, uv, poetry, etc.) ou adicionar ao `pyproject.toml`.

**Para detalhes de instalação:** <https://cocoindex.io/docs/getting_started/installation>

### Passo 3: Configurar o Ambiente

**Verificar ambiente existente primeiro:**

1. Verificar se `COCOINDEX_DATABASE_URL` existe nas variáveis de ambiente
   - Se não encontrada, usar padrão: `postgres://cocoindex:cocoindex@localhost/cocoindex`

2. **Para flows que requerem APIs LLM** (embeddings, extração):
   - Perguntar ao usuário qual provedor LLM quer usar:
     - **OpenAI** - Geração e embeddings
     - **Anthropic** - Apenas geração
     - **Gemini** - Geração e embeddings
     - **Voyage** - Apenas embeddings
     - **Ollama** - Modelos locais (geração e embeddings)
   - Verificar se a chave de API correspondente existe nas variáveis de ambiente
   - Se não encontrada, **pedir ao usuário para fornecer o valor da chave de API**
   - **Nunca criar exemplos simplificados sem LLM** - sempre obter a chave de API apropriada e usar as funções LLM reais

**Oriente o usuário a criar arquivo `.env`:**

```bash
# Conexão com banco de dados (obrigatória - armazenamento interno)
COCOINDEX_DATABASE_URL=postgres://cocoindex:cocoindex@localhost/cocoindex

# Chaves de API LLM (adicione as que você precisa)
OPENAI_API_KEY=sk-...          # Para OpenAI (geração + embeddings)
ANTHROPIC_API_KEY=sk-ant-...   # Para Anthropic (apenas geração)
GOOGLE_API_KEY=...             # Para Gemini (geração + embeddings)
VOYAGE_API_KEY=pa-...          # Para Voyage (apenas embeddings)
# Ollama não requer chave de API (local)
```

**Para mais opções LLM:** <https://cocoindex.io/docs/ai/llm>

Criar estrutura básica do projeto:

```python
# main.py
from dotenv import load_dotenv
import cocoindex

@cocoindex.flow_def(name="FlowName")
def my_flow(flow_builder: cocoindex.FlowBuilder, data_scope: cocoindex.DataScope):
    # Definição do flow aqui
    pass

if __name__ == "__main__":
    load_dotenv()
    cocoindex.init()
    my_flow.update()
```

### Passo 4: Escrever o Flow

Seguir esta estrutura:

```python
@cocoindex.flow_def(name="DescriptiveName")
def flow_name(flow_builder: cocoindex.FlowBuilder, data_scope: cocoindex.DataScope):
    # 1. Importar dados da fonte
    data_scope["source_name"] = flow_builder.add_source(
        cocoindex.sources.SourceType(...)
    )

    # 2. Criar coletor(es) para saídas
    collector = data_scope.add_collector()

    # 3. Transformar dados (iterar por linhas)
    with data_scope["source_name"].row() as item:
        # Aplicar transformações
        item["new_field"] = item["existing_field"].transform(
            cocoindex.functions.FunctionName(...)
        )

        ...

        # Iteração aninhada (ex: chunks dentro de documentos)
        with item["nested_table"].row() as nested_item:
            # Mais transformações
            nested_item["embedding"] = nested_item["text"].transform(...)

            # Coletar dados para exportação
            collector.collect(
                field1=nested_item["field1"],
                field2=item["field2"],
                generated_id=cocoindex.GeneratedField.UUID
            )

    # 4. Exportar para destino
    collector.export(
        "target_name",
        cocoindex.targets.TargetType(...),
        primary_key_fields=["field1"],
        vector_indexes=[...]  # Se necessário
    )
```

**Princípios-chave:**

- Cada fonte cria um campo no escopo de dados de nível superior
- Usar `.row()` para iterar pelos dados da tabela
- **CRÍTICO: Sempre atribuir dados transformados aos campos de linha** - Use `item["new_field"] = item["existing_field"].transform(...)`, NÃO variáveis locais como `new_field = item["existing_field"].transform(...)`
- Transformações criam novos campos sem mutar dados existentes
- Coletores reúnem dados de qualquer nível de escopo
- Exportação deve acontecer no nível superior (não dentro de iterações de linha)

**Erros comuns a evitar:**

❌ **Errado:** Usar variáveis locais para transformações

```python
with data_scope["files"].row() as file:
    summary = file["content"].transform(...)  # ❌ Variável local
    summaries_collector.collect(filename=file["filename"], summary=summary)
```

✅ **Correto:** Atribuir aos campos de linha

```python
with data_scope["files"].row() as file:
    file["summary"] = file["content"].transform(...)  # ✅ Atribuição de campo
    summaries_collector.collect(filename=file["filename"], summary=file["summary"])
```

❌ **Errado:** Criar dataclasses desnecessárias para espelhar campos do flow

```python
from dataclasses import dataclass

@dataclass
class FileSummary:  # ❌ Desnecessário - CocoIndex gerencia campos automaticamente
    filename: str
    summary: str
    embedding: list[float]

# Essa dataclass nunca é usada no flow!
```

### Passo 5: Desenhar a Solução do Flow

**IMPORTANTE:** Os padrões listados abaixo são pontos de partida comuns, mas **você não pode enumerar exaustivamente todos os cenários possíveis**. Quando os requisitos do usuário não correspondem aos padrões existentes:

1. **Combinar elementos de múltiplos padrões** - Misturar e combinar criatividade de fontes, transformações e destinos
2. **Revisar exemplos adicionais** - Ver <https://github.com/cocoindex-io/cocoindex?tab=readme-ov-file#-examples-and-demo> para casos de uso diversos do mundo real (reconhecimento facial, busca multimodal, recomendações de produtos, extração de formulários de pacientes, etc.)
3. **Pensar a partir de primeiros princípios** - Usar as APIs principais (fontes, transformações, coletores, exportações) e aplicar senso comum para resolver problemas novos
4. **Ser criativo** - CocoIndex é flexível; combinações únicas de componentes podem resolver problemas únicos

**Padrões de início comuns (use referências para exemplos detalhados):**

**Para embedding de texto:** Carregar `references/flow_patterns.md` e consultar "Padrão 1: Embedding de Texto Simples"

**Para embedding de código:** Carregar `references/flow_patterns.md` e consultar "Padrão 2: Embedding de Código com Detecção de Linguagem"

**Para extração via LLM + grafo de conhecimento:** Carregar `references/flow_patterns.md` e consultar "Padrão 3: Extração Baseada em LLM para Grafo de Conhecimento"

**Para atualizações em tempo real:** Carregar `references/flow_patterns.md` e consultar "Padrão 4: Atualizações em Tempo Real com Intervalo de Atualização"

**Para funções personalizadas:** Carregar `references/flow_patterns.md` e consultar "Padrão 5: Função de Transformação Personalizada"

**Para lógica de consulta reutilizável:** Carregar `references/flow_patterns.md` e consultar "Padrão 6: Transform Flow para Lógica Reutilizável"

**Para controle de concorrência:** Carregar `references/flow_patterns.md` e consultar "Padrão 7: Controle de Concorrência"

**Exemplo de composição de padrão:**

Se um usuário solicitar "indexar imagens de S3, gerar legendas com uma API de visão e armazenar em Qdrant", combine:

- Fonte AmazonS3 (de exemplos S3)
- Função personalizada para chamadas de API de visão (do padrão de funções personalizadas)
- EmbedText para incorporar as legendas (de padrões de embedding)
- Destino Qdrant (de exemplos de destino)

Nenhum padrão único cobre este cenário exato, mas os blocos de construção são compostos.

### Passo 6: Testar e Executar

Orientar o usuário pelo teste:

```bash
# 1. Executar com setup
cocoindex update --setup -f main   # -f força setup sem prompts de confirmação


# 2. Iniciar um servidor e redirecionar usuários para CocoInsight
cocoindex server -ci main
# Depois abrir CocoInsight em https://cocoindex.io/cocoinsight

```

## Tipos de Dados

CocoIndex possui um sistema de tipos independente de linguagens de programação. Todos os tipos de dados são determinados no momento da definição do flow, deixando schemas claros e previsíveis.

**IMPORTANTE: Quando definir tipos:**

- **Funções personalizadas**: Anotações de tipo são **obrigatórias** para valores de retorno (estas são a fonte de verdade para inferência de tipo)
- **Campos de flow**: Anotações de tipo **NÃO são necessárias** - CocoIndex infere automaticamente tipos de fontes, funções e transformações
- **Dataclasses/Modelos Pydantic**: Criar apenas quando **realmente usados** (como parâmetros/retornos de função ou output_type de ExtractByLlm), NÃO para espelhar schemas de campos de flow

**Requisitos de anotação de tipo:**

- **Valores de retorno de funções personalizadas**: Devem usar **anotações de tipo específicas** - estas são a fonte de verdade para inferência de tipo
- **Argumentos de funções personalizadas**: Relaxados - podem usar `Any`, `dict[str, Any]` ou omitir anotações; o engine já conhece os tipos
- **Definições de flow**: Sem anotações de tipo explícitas necessárias - CocoIndex infere automaticamente tipos de fontes e funções

**Por que tipos de retorno específicos importam:** Tipos de retorno de funções personalizadas permitem que CocoIndex infira tipos de campo em todo o flow sem processar dados reais. Isso permite criar schemas de destino apropriados (ex: índices vetoriais com dimensões fixas).

**Categorias de tipo comuns:**

1. **Tipos primitivos**: `str`, `int`, `float`, `bool`, `bytes`, `datetime.date`, `datetime.datetime`, `uuid.UUID`

2. **Tipos vetoriais** (embeddings): Especificar dimensão no tipo de retorno se você planeja exportar como vetores para destinos, pois a maioria dos destinos requer uma dimensão vetorial fixa
   - `cocoindex.Vector[cocoindex.Float32, typing.Literal[768]]` - vetor float32 de 768 dimensões (recomendado)
   - `list[float]` sem dimensão também funciona

3. **Tipos struct**: Dataclass, NamedTuple ou modelo Pydantic
   - Tipo de retorno: Deve usar classe específica (ex: `Person`)
   - Argumento: Pode usar `dict[str, Any]` ou `Any`

4. **Tipos de tabela**:
   - **KTable** (com chave): `dict[K, V]` onde K = tipo de chave (primitivo ou struct congelado), V = tipo Struct
   - **LTable** (ordenada): `list[R]` onde R = tipo Struct
   - Argumentos: Podem usar `dict[Any, Any]` ou `list[Any]`

5. **Tipo Json**: `cocoindex.Json` para dados não estruturados/dinâmicos

6. **Tipos opcionais**: `T | None` para valores anuláveis

**Exemplos:**

```python
from dataclasses import dataclass
from typing import Literal
import cocoindex

@dataclass
class Person:
    name: str
    age: int

# ✅ Vetor com dimensão (recomendado para busca vetorial)
@cocoindex.op.function(behavior_version=1)
def embed_text(text: str) -> cocoindex.Vector[cocoindex.Float32, Literal[768]]:
    """Gerar embedding de 768 dimensões - dimensão necessária para índice vetorial."""
    # ... lógica de embedding ...
    return embedding  # array numpy ou lista de 768 floats

# ✅ Tipo de retorno Struct, argumento relaxado
@cocoindex.op.function(behavior_version=1)
def process_person(person: dict[str, Any]) -> Person:
    """Argumento pode ser dict[str, Any], retorno deve ser Struct específico."""
    return Person(name=person["name"], age=person["age"])

# ✅ Tipo de retorno LTable
@cocoindex.op.function(behavior_version=1)
def filter_people(people: list[Any]) -> list[Person]:
    """Tipo de retorno especifica lista de Struct específico."""
    return [p for p in people if p.age >= 18]

# ❌ Errado: dict[str, str] não é um tipo CocoIndex válido e específico
# @cocoindex.op.function(...)
# def bad_example(person: Person) -> dict[str, str]:
#     return {"name": person.name}
```

**Para documentação abrangente de tipos de dados:** <https://cocoindex.io/docs/core/data_types>

## Funções Personalizadas

Quando os usuários precisarem de lógica de transformação customizada, criar funções personalizadas.

### Decisão: Função Isolada vs Spec+Executor

**Usar função isolada quando:**

- Transformação simples
- Sem configuração necessária
- Sem setup/inicialização necessária

**Usar spec+executor quando:**

- Precisa de configuração (nomes de modelo, endpoints de API, parâmetros)
- Requer setup (carregar modelos, estabelecer conexões)
- Processamento complexo multi-etapa

### Criar Funções Isoladas

```python
@cocoindex.op.function(behavior_version=1)
def my_function(input_arg: str, optional_arg: int | None = None) -> dict:
    """
    Descrição da função.

    Args:
        input_arg: Descrição
        optional_arg: Descrição opcional
    """
    # Lógica de transformação
    return {"result": f"processed-{input_arg}"}
```

**Requisitos:**

- Decorador: `@cocoindex.op.function()`
- Anotações de tipo em todos os argumentos e valor de retorno
- Parâmetros opcionais: `cache=True` para operações custosas, `behavior_version` (obrigatório com cache)

### Criar Funções Spec+Executor

```python
# 1. Definir spec de configuração
class MyFunction(cocoindex.op.FunctionSpec):
    """Configuração para MyFunction."""
    model_name: str
    threshold: float = 0.5

# 2. Definir executor
@cocoindex.op.executor_class(cache=True, behavior_version=1)
class MyFunctionExecutor:
    spec: MyFunction  # Obrigatório: link para spec
    model = None      # Variáveis de instância para estado

    def prepare(self) -> None:
        """Opcional: executar uma vez antes da execução."""
        # Carregar modelo, estabelecer conexões, etc.
        self.model = load_model(self.spec.model_name)

    def __call__(self, text: str) -> dict:
        """Obrigatório: executar para cada linha de dados."""
        # Usar self.spec para configuração
        # Usar self.model para recursos carregados
        result = self.model.process(text)
        return {"result": result}
```

**Quando habilitar cache:**

- Chamadas de API LLM
- Inferência de modelo
- Chamadas de API externa
- Operações computacionalmente custosas

**Importante:** Incrementar `behavior_version` quando a lógica da função muda para invalidar o cache.

Para exemplos detalhados e padrões, carregar `references/custom_functions.md`.

**Para mais sobre funções personalizadas:** <https://cocoindex.io/docs/custom_ops/custom_functions>

## Operando Flows

### Operações CLI

**Setup flow (criar recursos):**

```bash
cocoindex setup main
```

**Atualização única:**

```bash
cocoindex update main

# Com auto-setup
cocoindex update --setup main

# Forçar reset de tudo antes de setup e atualização
cocoindex update --reset main
```

**Atualização em tempo real (monitoramento contínuo):**

```bash
cocoindex update main.py -L

# Requer refresh_interval na fonte ou captura de mudança específica da fonte
```

**Drop flow (remover todos os recursos):**

```bash
cocoindex drop main.py
```

**Inspecionar flow:**

```bash
cocoindex show main.py:FlowName
```

**Testar sem efeitos colaterais:**

```bash
cocoindex evaluate main.py:FlowName --output-dir ./test_output
```

Para referência completa da CLI, carregar `references/cli_operations.md`.

**Para documentação da CLI:** <https://cocoindex.io/docs/core/cli>

### Operações de API

**Setup básico:**

```python
from dotenv import load_dotenv
import cocoindex

load_dotenv()
cocoindex.init()

@cocoindex.flow_def(name="MyFlow")
def my_flow(flow_builder, data_scope):
    # ... definição do flow ...
    pass
```

**Atualização única:**

```python
stats = my_flow.update()
print(f"Processadas {stats.total_rows} linhas")

# Async
stats = await my_flow.update_async()
```

**Atualização em tempo real:**

```python
# Como context manager
with cocoindex.FlowLiveUpdater(my_flow) as updater:
    # Updater executa em background
    # Sua lógica de aplicação aqui
    pass

# Controle manual
updater = cocoindex.FlowLiveUpdater(
    my_flow,
    cocoindex.FlowLiveUpdaterOptions(
        live_mode=True,
        print_stats=True
    )
)
updater.start()
# ... lógica de aplicação ...
updater.wait()
```

**Setup/drop:**

```python
my_flow.setup(report_to_stdout=True)
my_flow.drop(report_to_stdout=True)
cocoindex.setup_all_flows()
cocoindex.drop_all_flows()
```

**Consultar com transform flows:**

```python
@cocoindex.transform_flow()
def text_to_embedding(text: cocoindex.DataSlice[str]) -> cocoindex.DataSlice[list[float]]:
    return text.transform(
        cocoindex.functions.SentenceTransformerEmbed(model="...")
    )

# Usar em flow para indexação
doc["embedding"] = text_to_embedding(doc["content"])

# Usar para consultas
query_embedding = text_to_embedding.eval("search query")
```

Para referência completa de API e padrões, carregar `references/api_operations.md`.

**Para documentação de API:** <https://cocoindex.io/docs/core/flow_methods>

## Funções Integradas

### Processamento de Texto

**SplitRecursively** - Chunking inteligente de texto

```python
doc["chunks"] = doc["content"].transform(
    cocoindex.functions.SplitRecursively(),
    language="markdown",  # ou "python", "javascript", etc.
    chunk_size=2000,
    chunk_overlap=500
)
```

**ParseJson** - Analisar strings JSON

```python
data = json_string.transform(cocoindex.functions.ParseJson())
```

**DetectProgrammingLanguage** - Detectar linguagem pelo nome de arquivo

```python
file["language"] = file["filename"].transform(
    cocoindex.functions.DetectProgrammingLanguage()
)
```

### Embeddings

**SentenceTransformerEmbed** - Modelo de embedding local

```python
# Requer: cocoindex[embeddings]
chunk["embedding"] = chunk["text"].transform(
    cocoindex.functions.SentenceTransformerEmbed(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
)
```

**EmbedText** - Embeddings via API LLM

Esta é a **forma recomendada** de gerar embeddings usando APIs LLM (OpenAI, Voyage, etc.).

```python
chunk["embedding"] = chunk["text"].transform(
    cocoindex.functions.EmbedText(
        api_type=cocoindex.LlmApiType.OPENAI,
        model="text-embedding-3-small",
    )
)
```

**ColPaliEmbedImage** - Embeddings de imagem multimodais

```python
# Requer: cocoindex[colpali]
image["embedding"] = image["img_bytes"].transform(
    cocoindex.functions.ColPaliEmbedImage(model="vidore/colpali-v1.2")
)
```

### Extração via LLM

**ExtractByLlm** - Extrair dados estruturados com LLM

Esta é a **forma recomendada** de usar LLMs para tarefas de extração e sumarização. Suporta saídas estruturadas (dataclasses, modelos Pydantic) e saídas de texto simples (str).

```python
import dataclasses

# Para extração estruturada
@dataclasses.dataclass
class ProductInfo:
    name: str
    price: float
    category: str

item["product_info"] = item["text"].transform(
    cocoindex.functions.ExtractByLlm(
        llm_spec=cocoindex.LlmSpec(
            api_type=cocoindex.LlmApiType.OPENAI,
            model="gpt-4o-mini"
        ),
        output_type=ProductInfo,
        instruction="Extrair informações do produto"
    )
)

# Para sumarização/geração de texto
file["summary"] = file["content"].transform(
    cocoindex.functions.ExtractByLlm(
        llm_spec=cocoindex.LlmSpec(
            api_type=cocoindex.LlmApiType.OPENAI,
            model="gpt-4o-mini"
        ),
        output_type=str,
        instruction="Resuma este documento em um parágrafo"
    )
)
```

## Fontes e Destinos Comuns

**Navegar por todas as fontes:** <https://cocoindex.io/docs/sources/>
**Navegar por todos os destinos:** <https://cocoindex.io/docs/targets/>

### Fontes

**LocalFile:**

```python
cocoindex.sources.LocalFile(
    path="documents",
    included_patterns=["*.md", "*.txt"],
    excluded_patterns=["**/.*", "node_modules"]
)
```

**AmazonS3:**

```python
cocoindex.sources.AmazonS3(
    bucket="my-bucket",
    prefix="documents/",
    aws_access_key_id=cocoindex.add_transient_auth_entry("..."),
    aws_secret_access_key=cocoindex.add_transient_auth_entry("...")
)
```

**Postgres:**

```python
cocoindex.sources.Postgres(
    connection=cocoindex.add_auth_entry("conn", cocoindex.sources.PostgresConnection(...)),
    query="SELECT id, content FROM documents"
)
```

### Destinos

**Postgres (com suporte vetorial):**

```python
collector.export(
    "target_name",
    cocoindex.targets.Postgres(),
    primary_key_fields=["id"],
    vector_indexes=[
        cocoindex.VectorIndexDef(
            field_name="embedding",
            metric=cocoindex.VectorSimilarityMetric.COSINE_SIMILARITY
        )
    ]
)
```

**Qdrant:**

```python
collector.export(
    "target_name",
    cocoindex.targets.Qdrant(collection_name="my_collection"),
    primary_key_fields=["id"]
)
```

**LanceDB:**

```python
# Requer: cocoindex[lancedb]
collector.export(
    "target_name",
    cocoindex.targets.LanceDB(uri="lancedb_data", table_name="my_table"),
    primary_key_fields=["id"]
)
```

**Neo4j (nós):**

```python
collector.export(
    "nodes",
    cocoindex.targets.Neo4j(
        connection=neo4j_conn,
        mapping=cocoindex.targets.Nodes(label="Entity")
    ),
    primary_key_fields=["id"]
)
```

**Neo4j (relacionamentos):**

```python
collector.export(
    "relationships",
    cocoindex.targets.Neo4j(
        connection=neo4j_conn,
        mapping=cocoindex.targets.Relationships(