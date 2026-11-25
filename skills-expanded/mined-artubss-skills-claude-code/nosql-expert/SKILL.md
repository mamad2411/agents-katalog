---
name: nosql-expert
description: "Orientação especializada em bancos de dados NoSQL distribuídos (Cassandra, DynamoDB). Foca em modelos mentais, modelagem query-first, design single-table e evitar partições quentes em sistemas de alta escala."
---

# Padrões NoSQL Expert (Cassandra & DynamoDB)

## Visão Geral

Esta habilidade fornece modelos mentais profissionais e padrões de design para **armazenamentos distribuídos wide-column e key-value** (especificamente Apache Cassandra e Amazon DynamoDB).

Diferente de SQL (onde você modela entidades de dados) ou armazenamentos de documentos (como MongoDB), estes sistemas distribuídos exigem que você **modele suas queries primeiro**.

## Quando Usar

- **Design para Escala**: Saindo de bancos de dados simples single-node para clusters distribuídos.
- **Seleção de Tecnologia**: Avaliando ou utilizando **Cassandra**, **ScyllaDB** ou **DynamoDB**.
- **Ajuste de Performance**: Solucionando problemas de "partições quentes" ou alta latência em sistemas NoSQL existentes.
- **Microsserviços**: Implementando padrões "database-per-service" onde leituras altamente otimizadas são necessárias.

## A Mudança Mental: SQL vs. NoSQL Distribuído

| Característica | SQL (Relacional) | NoSQL Distribuído (Cassandra/DynamoDB) |
| :--- | :--- | :--- |
| **Modelagem de dados** | Modela Entidades + Relacionamentos | Modela **Queries** (Padrões de Acesso) |
| **Joins** | Intensivo em CPU, em tempo de leitura | **Pré-computado** (Desnormalizado) em tempo de escrita |
| **Custo de armazenamento** | Caro (minimizar duplicação) | Barato (duplicar dados para velocidade de leitura) |
| **Consistência** | ACID (Forte) | **BASE (Eventual)** / Ajustável |
| **Escalabilidade** | Vertical (Máquina maior) | **Horizontal** (Mais nós/shards) |

> **A Regra de Ouro:** Em SQL, você projeta o modelo de dados para responder *qualquer* query. Em NoSQL, você projeta o modelo de dados para responder *queries específicas* eficientemente.

## Padrões de Design Core

### 1. Modelagem Query-First (Padrões de Acesso)

Você tipicamente não pode "adicionar uma query depois" sem migração ou criar uma nova tabela/índice.

**Processo:**
1.  **Liste todas as Entidades** (User, Order, Product).
2.  **Liste todos os Padrões de Acesso** ("Obter User por Email", "Obter Orders do User ordenadas por Data").
3.  **Projete a Tabela(s)** especificamente para servir esses padrões com um único lookup.

### 2. A Partition Key é Rainha

Os dados são distribuídos entre nós físicos baseado na **Partition Key (PK)**.
-   **Objetivo:** Distribuição uniforme de dados e tráfego.
-   **Anti-Pattern:** Usar uma PK de baixa cardinalidade (ex: `status="active"` ou `gender="m"`) cria **Partições Quentes**, limitando a throughput à capacidade de um único nó.
-   **Melhor Prática:** Use chaves de alta cardinalidade (User IDs, Device IDs, Chaves Compostas).

### 3. Clustering / Sort Keys

Dentro de uma partição, os dados são ordenados no disco pela **Clustering Key (Cassandra)** ou **Sort Key (DynamoDB)**.
-   Isso permite **Range Queries** eficientes (ex: `WHERE user_id=X AND date > Y`).
-   Efetivamente pré-ordena seus dados para requisitos específicos de recuperação.

### 4. Design Single-Table (Adjacency Lists)

*Uso primário: DynamoDB (mas conceitos se aplicam em outros lugares)*

Armazenar múltiplos tipos de entidade em uma tabela para habilitar leituras pré-joined.

| PK (Partition) | SK (Sort) | Campos de Dados... |
| :--- | :--- | :--- |
| `USER#123` | `PROFILE` | `{ name: "Ian", email: "..." }` |
| `USER#123` | `ORDER#998` | `{ total: 50.00, status: "shipped" }` |
| `USER#123` | `ORDER#999` | `{ total: 12.00, status: "pending" }` |

-   **Query:** `PK="USER#123"`
-   **Resultado:** Busca User Profile E todas as Orders em **uma única requisição de rede**.

### 5. Desnormalização & Duplicação

Não tenha medo de armazenar os mesmos dados em múltiplas tabelas para servir padrões de query diferentes.
-   **Tabela A:** `users_by_id` (PK: uuid)
-   **Tabela B:** `users_by_email` (PK: email)

*Trade-off: Você deve gerenciar consistência de dados entre tabelas (frequentemente usando eventual consistency ou batch writes).*

## Orientação Específica

### Apache Cassandra / ScyllaDB

-   **Estrutura de Primary Key:** `((Partition Key), Clustering Columns)`
-   **Sem Joins, Sem Agregates:** Não tente fazer `JOIN` ou `GROUP BY`. Pré-calcule agregates em uma tabela de contador separada.
-   **Evite `ALLOW FILTERING`:** Se você ver isso em produção, seu modelo de dados está errado. Isso implica um full cluster scan.
-   **Escritas são Baratas:** Inserts e Updates são apenas appends para a LSM tree. Não se preocupe com volume de escrita tanto quanto com eficiência de leitura.
-   **Tombstones:** Deletes são marcadores custosos. Evite padrões de delete de alta velocidade (como filas) em tabelas padrão.

### AWS DynamoDB

-   **GSI (Global Secondary Index):** Use GSIs para criar visualizações alternativas de seus dados (ex: "Pesquisar Orders por Data" em vez de por User).
    -   *Nota:* GSIs são eventually consistent.
-   **LSI (Local Secondary Index):** Ordena dados diferentemente *dentro* da mesma partição. Deve ser criado no tempo de criação da tabela.
-   **WCU / RCU:** Entenda os modos de capacidade. Design single-table ajuda a otimizar unidades de capacidade consumidas.
-   **TTL:** Use atributos Time-To-Live para expirar automaticamente dados antigos (delete gratuito) sem criar tombstones.

## Checklist Expert

Antes de finalizar seu schema NoSQL:

-   [ ] **Cobertura de Padrões de Acesso:** Cada padrão de query mapeia para uma tabela ou índice específico?
-   [ ] **Verificação de Cardinalidade:** A Partition Key tem valores únicos suficientes para distribuir tráfego uniformemente?
-   [ ] **Risco de Split de Partição:** Para qualquer partição única (ex: orders de um único usuário), ela crescerá indefinidamente? (Se > 10GB, você precisa "shardear" a partição, ex: `USER#123#2024-01`).
-   [ ] **Requisito de Consistência:** A aplicação pode tolerar eventual consistency para este padrão de leitura?

## Anti-Patterns Comuns

❌ **Scatter-Gather:** Consultar *todas* as partições para encontrar um item (Scan).
❌ **Hot Keys:** Colocar todos os dados de "segunda-feira" em uma partição.
❌ **Modelagem Relacional:** Criar tabelas `Author` e `Book` e tentar juntá-las em código. (Em vez disso, incorpore resumos de Book em Author, ou duplique info de Author em Books).