---
name: benchling-integration
description: "Integração da plataforma Benchling R&D. Acesso ao registry (DNA, proteínas), inventário, entradas ELN, workflows via API, construção de Benchling Apps, consulta Data Warehouse, para automação de gerenciamento de dados de laboratório."
---

# Integração Benchling

## Visão Geral

Benchling é uma plataforma cloud para P&D em ciências da vida. Acesse entidades de registry (DNA, proteínas), inventário, notebooks eletrônicos de laboratório e workflows programaticamente via SDK Python e REST API.

## Quando Usar Esta Skill

Esta skill deve ser usada quando:
- Trabalhar com SDK Python ou REST API do Benchling
- Gerenciar sequências biológicas (DNA, RNA, proteínas) e entidades de registry
- Automatizar operações de inventário (amostras, containers, locais, transferências)
- Criar ou consultar entradas de notebooks eletrônicos de laboratório
- Construir automações de workflow ou Benchling Apps
- Sincronizar dados entre Benchling e sistemas externos
- Consultar o Data Warehouse do Benchling para análises
- Configurar integrações orientadas por eventos com AWS EventBridge

## Capacidades Principais

### 1. Autenticação & Configuração

**Instalação do SDK Python:**
```python
# Versão estável
uv pip install benchling-sdk
# ou com Poetry
poetry add benchling-sdk
```

**Métodos de Autenticação:**

Autenticação com Chave de API (recomendada para scripts):
```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

benchling = Benchling(
    url="https://seu-tenant.benchling.com",
    auth_method=ApiKeyAuth("sua_chave_api")
)
```

OAuth Client Credentials (para apps):
```python
from benchling_sdk.auth.client_credentials_oauth2 import ClientCredentialsOAuth2

auth_method = ClientCredentialsOAuth2(
    client_id="seu_client_id",
    client_secret="seu_client_secret"
)
benchling = Benchling(
    url="https://seu-tenant.benchling.com",
    auth_method=auth_method
)
```

**Pontos-Chave:**
- As chaves de API são obtidas nas Configurações de Perfil no Benchling
- Armazene credenciais com segurança (use variáveis de ambiente ou gerenciadores de senhas)
- Todas as requisições de API requerem HTTPS
- As permissões de autenticação refletem as permissões do usuário na UI

Para informações detalhadas sobre autenticação, incluindo OIDC e boas práticas de segurança, consulte `references/authentication.md`.

### 2. Gerenciamento de Registry & Entidades

As entidades de registry incluem sequências de DNA, sequências de RNA, sequências de AA, entidades customizadas e misturas. O SDK fornece classes tipadas para criar e gerenciar essas entidades.

**Criando Sequências de DNA:**
```python
from benchling_sdk.models import DnaSequenceCreate

sequence = benchling.dna_sequences.create(
    DnaSequenceCreate(
        name="Meu Plasmídeo",
        bases="ATCGATCG",
        is_circular=True,
        folder_id="fld_abc123",
        schema_id="ts_abc123",  # opcional
        fields=benchling.models.fields({"gene_name": "GFP"})
    )
)
```

**Registro no Registry:**

Para registrar uma entidade diretamente ao criar:
```python
sequence = benchling.dna_sequences.create(
    DnaSequenceCreate(
        name="Meu Plasmídeo",
        bases="ATCGATCG",
        is_circular=True,
        folder_id="fld_abc123",
        entity_registry_id="src_abc123",  # Registry para registrar
        naming_strategy="NEW_IDS"  # ou "IDS_FROM_NAMES"
    )
)
```

**Importante:** Use `entity_registry_id` OU `naming_strategy`, nunca ambos.

**Atualizando Entidades:**
```python
from benchling_sdk.models import DnaSequenceUpdate

updated = benchling.dna_sequences.update(
    sequence_id="seq_abc123",
    dna_sequence=DnaSequenceUpdate(
        name="Nome do Plasmídeo Atualizado",
        fields=benchling.models.fields({"gene_name": "mCherry"})
    )
)
```

Campos não especificados permanecem inalterados, permitindo atualizações parciais.

**Listagem e Paginação:**
```python
# Listar todas as sequências de DNA (retorna um gerador)
sequences = benchling.dna_sequences.list()
for page in sequences:
    for seq in page:
        print(f"{seq.name} ({seq.id})")

# Verificar contagem total
total = sequences.estimated_count()
```

**Operações-Chave:**
- Criar: `benchling.<entity_type>.create()`
- Ler: `benchling.<entity_type>.get(id)` ou `.list()`
- Atualizar: `benchling.<entity_type>.update(id, update_object)`
- Arquivar: `benchling.<entity_type>.archive(id)`

Tipos de entidade: `dna_sequences`, `rna_sequences`, `aa_sequences`, `custom_entities`, `mixtures`

Para referência SDK abrangente e padrões avançados, consulte `references/sdk_reference.md`.

### 3. Gerenciamento de Inventário

Gerencie amostras físicas, containers, caixas e locais dentro do sistema de inventário do Benchling.

**Criando Containers:**
```python
from benchling_sdk.models import ContainerCreate

container = benchling.containers.create(
    ContainerCreate(
        name="Tubo de Amostra 001",
        schema_id="cont_schema_abc123",
        parent_storage_id="box_abc123",  # opcional
        fields=benchling.models.fields({"concentration": "100 ng/μL"})
    )
)
```

**Gerenciando Caixas:**
```python
from benchling_sdk.models import BoxCreate

box = benchling.boxes.create(
    BoxCreate(
        name="Caixa de Freezer A1",
        schema_id="box_schema_abc123",
        parent_storage_id="loc_abc123"
    )
)
```

**Transferindo Itens:**
```python
# Transferir um container para um novo local
transfer = benchling.containers.transfer(
    container_id="cont_abc123",
    destination_id="box_xyz789"
)
```

**Operações-Chave de Inventário:**
- Criar containers, caixas, locais, placas
- Atualizar propriedades de itens de inventário
- Transferir itens entre locais
- Registrar entrada/saída de itens
- Operações em lote para transferências em massa

### 4. Notebook & Documentação

Interaja com entradas de notebooks eletrônicos de laboratório (ELN), protocolos e templates.

**Criando Entradas de Notebook:**
```python
from benchling_sdk.models import EntryCreate

entry = benchling.entries.create(
    EntryCreate(
        name="Experimento 2025-10-20",
        folder_id="fld_abc123",
        schema_id="entry_schema_abc123",
        fields=benchling.models.fields({"objective": "Testar expressão gênica"})
    )
)
```

**Vinculando Entidades a Entradas:**
```python
# Adicionar referências a entidades em uma entrada
entry_link = benchling.entry_links.create(
    entry_id="entry_abc123",
    entity_id="seq_xyz789"
)
```

**Operações-Chave de Notebook:**
- Criar e atualizar entradas de notebooks de laboratório
- Gerenciar templates de entrada
- Vincular entidades e resultados a entradas
- Exportar entradas para documentação

### 5. Workflows & Automação

Automatize processos de laboratório usando o sistema de workflow do Benchling.

**Criando Tarefas de Workflow:**
```python
from benchling_sdk.models import WorkflowTaskCreate

task = benchling.workflow_tasks.create(
    WorkflowTaskCreate(
        name="Amplificação por PCR",
        workflow_id="wf_abc123",
        assignee_id="user_abc123",
        fields=benchling.models.fields({"template": "seq_abc123"})
    )
)
```

**Atualizando Status da Tarefa:**
```python
from benchling_sdk.models import WorkflowTaskUpdate

updated_task = benchling.workflow_tasks.update(
    task_id="task_abc123",
    workflow_task=WorkflowTaskUpdate(
        status_id="status_complete_abc123"
    )
)
```

**Operações Assíncronas:**

Algumas operações são assíncronas e retornam tarefas:
```python
# Aguardar conclusão da tarefa
from benchling_sdk.helpers.tasks import wait_for_task

result = wait_for_task(
    benchling,
    task_id="task_abc123",
    interval_wait_seconds=2,
    max_wait_seconds=300
)
```

**Operações-Chave de Workflow:**
- Criar e gerenciar tarefas de workflow
- Atualizar status e atribuições de tarefas
- Executar operações em lote de forma assíncrona
- Monitorar progresso de tarefas

### 6. Eventos & Integração

Inscreva-se em eventos do Benchling para integrações em tempo real usando AWS EventBridge.

**Tipos de Evento:**
- Criação, atualização, arquivo de entidades
- Transferências de inventário
- Mudanças no status de tarefas de workflow
- Criação e atualizações de entradas
- Registro de resultados

**Padrão de Integração:**
1. Configure roteamento de eventos para AWS EventBridge nas configurações do Benchling
2. Crie regras do EventBridge para filtrar eventos
3. Roteie eventos para funções Lambda ou outros destinos
4. Processe eventos e atualize sistemas externos

**Casos de Uso:**
- Sincronizar dados do Benchling com bancos de dados externos
- Disparar processos downstream na conclusão de workflow
- Enviar notificações sobre mudanças de entidades
- Registro de trilha de auditoria

Consulte a documentação de eventos do Benchling para schemas de eventos e configuração.

### 7. Data Warehouse & Análises

Consulte dados históricos do Benchling usando SQL através do Data Warehouse.

**Método de Acesso:**
O Data Warehouse do Benchling fornece acesso SQL aos dados do Benchling para análises e relatórios. Conecte-se usando clientes SQL padrão com credenciais fornecidas.

**Consultas Comuns:**
- Agregar resultados experimentais
- Analisar tendências de inventário
- Gerar relatórios de conformidade
- Exportar dados para análise externa

**Integração com Ferramentas de Análise:**
- Jupyter notebooks para análise interativa
- Ferramentas de BI (Tableau, Looker, PowerBI)
- Dashboards customizados

## Melhores Práticas

### Tratamento de Erros

O SDK automaticamente tenta novamente requisições falhadas:
```python
# Tentativa automática para status 429, 502, 503, 504
# Até 5 tentativas com backoff exponencial
# Customize o comportamento de retry se necessário
from benchling_sdk.retry import RetryStrategy

benchling = Benchling(
    url="https://seu-tenant.benchling.com",
    auth_method=ApiKeyAuth("sua_chave_api"),
    retry_strategy=RetryStrategy(max_retries=3)
)
```

### Eficiência de Paginação

Use geradores para paginação eficiente em memória:
```python
# Iteração baseada em gerador
for page in benchling.dna_sequences.list():
    for sequence in page:
        process(sequence)

# Verificar contagem estimada sem carregar todas as páginas
total = benchling.dna_sequences.list().estimated_count()
```

### Auxiliar de Campos de Schema

Use o auxiliar `fields()` para campos de schema customizados:
```python
# Converter dict para objeto Fields
custom_fields = benchling.models.fields({
    "concentration": "100 ng/μL",
    "date_prepared": "2025-10-20",
    "notes": "Preparação de alta qualidade"
})
```

### Compatibilidade Futura

O SDK manipula valores de enum desconhecidos e tipos de forma elegante:
- Valores de enum desconhecidos são preservados
- Tipos polimórficos não reconhecidos retornam `UnknownType`
- Permite trabalhar com versões de API mais recentes

### Considerações de Segurança

- Nunca envie chaves de API para controle de versão
- Use variáveis de ambiente para credenciais
- Reveze chaves se comprometidas
- Conceda permissões mínimas necessárias para apps
- Use OAuth para cenários multi-usuário

## Recursos

### references/

Documentação de referência detalhada para informações aprofundadas:

- **authentication.md** - Guia abrangente de autenticação incluindo OIDC, boas práticas de segurança e gerenciamento de credenciais
- **sdk_reference.md** - Referência detalhada do SDK Python com padrões avançados, exemplos e todos os tipos de entidade
- **api_endpoints.md** - Referência de endpoints da REST API para chamadas HTTP diretas sem o SDK

Carregue essas referências conforme necessário para requisitos específicos de integração.

### scripts/

Esta skill atualmente inclui scripts de exemplo que podem ser removidos ou substituídos por scripts de automação customizados para seus workflows específicos do Benchling.

## Casos de Uso Comuns

**1. Importação em Lote de Entidades:**
```python
# Importar múltiplas sequências de arquivo FASTA
from Bio import SeqIO

for record in SeqIO.parse("sequences.fasta", "fasta"):
    benchling.dna_sequences.create(
        DnaSequenceCreate(
            name=record.id,
            bases=str(record.seq),
            is_circular=False,
            folder_id="fld_abc123"
        )
    )
```

**2. Auditoria de Inventário:**
```python
# Listar todos os containers em um local específico
containers = benchling.containers.list(
    parent_storage_id="box_abc123"
)

for page in containers:
    for container in page:
        print(f"{container.name}: {container.barcode}")
```

**3. Automação de Workflow:**
```python
# Atualizar todas as tarefas pendentes para um workflow
tasks = benchling.workflow_tasks.list(
    workflow_id="wf_abc123",
    status="pending"
)

for page in tasks:
    for task in page:
        # Executar verificações automatizadas
        if auto_validate(task):
            benchling.workflow_tasks.update(
                task_id=task.id,
                workflow_task=WorkflowTaskUpdate(
                    status_id="status_complete"
                )
            )
```

**4. Exportação de Dados:**
```python
# Exportar todas as sequências com propriedades específicas
sequences = benchling.dna_sequences.list()
export_data = []

for page in sequences:
    for seq in page:
        if seq.schema_id == "target_schema_id":
            export_data.append({
                "id": seq.id,
                "name": seq.name,
                "bases": seq.bases,
                "length": len(seq.bases)
            })

# Salvar em CSV ou banco de dados
import csv
with open("sequences.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=export_data[0].keys())
    writer.writeheader()
    writer.writerows(export_data)
```

## Recursos Adicionais

- **Documentação Oficial:** https://docs.benchling.com
- **Referência SDK Python:** https://benchling.com/sdk-docs/
- **Referência de API:** https://benchling.com/api/reference
- **Suporte:** [email protected]