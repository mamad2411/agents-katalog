---
name: database-schema-designer
description: Projete esquemas de banco de dados robustos e escaláveis para SQL e NoSQL. Fornece diretrizes de normalização, estratégias de indexação, padrões de migração, design de restrições e otimização de desempenho. Garante integridade de dados, desempenho de consultas e modelos de dados mantíveis.
license: MIT
---

# Designer de Esquema de Banco de Dados

Projete esquemas de banco de dados prontos para produção com boas práticas integradas.

---

## Início Rápido

Apenas descreva seu modelo de dados:

```
design a schema for an e-commerce platform with users, products, orders
```

Você receberá um esquema SQL completo como:

```sql
CREATE TABLE users (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id),
  total DECIMAL(10,2) NOT NULL,
  INDEX idx_orders_user (user_id)
);
```

**O que incluir em sua solicitação:**
- Entidades (usuários, produtos, pedidos)
- Relacionamentos-chave (usuários têm pedidos, pedidos têm itens)
- Dicas de escala (alto tráfego, milhões de registros)
- Preferência de banco de dados (SQL/NoSQL) - padrão é SQL se não especificado

---

## Gatilhos

| Gatilho | Exemplo |
|---------|---------|
| `design schema` | "design a schema for user authentication" |
| `database design` | "database design for multi-tenant SaaS" |
| `create tables` | "create tables for a blog system" |
| `schema for` | "schema for inventory management" |
| `model data` | "model data for real-time analytics" |
| `I need a database` | "I need a database for tracking orders" |
| `design NoSQL` | "design NoSQL schema for product catalog" |

---

## Termos-Chave

| Termo | Definição |
|------|-----------|
| **Normalização** | Organizar dados para reduzir redundância (1FN → 2FN → 3FN) |
| **3FN** | Terceira Forma Normal - sem dependências transitivas entre colunas |
| **OLTP** | Online Transaction Processing - muitas escritas, precisa normalização |
| **OLAP** | Online Analytical Processing - muitas leituras, beneficia-se de desnormalização |
| **Chave Estrangeira (FK)** | Coluna que referencia a chave primária de outra tabela |
| **Índice** | Estrutura de dados que acelera consultas (ao custo de escritas mais lentas) |
| **Padrão de Acesso** | Como sua aplicação lê/escreve dados (consultas, joins, filtros) |
| **Desnormalização** | Duplicar dados intencionalmente para acelerar leituras |

---

## Referência Rápida

| Tarefa | Abordagem | Consideração-Chave |
|--------|-----------|-------------------|
| Novo esquema | Normalize para 3FN primeiro | Modelagem de domínio sobre UI |
| SQL vs NoSQL | Padrões de acesso decidem | Razão leitura/escrita importa |
| Chaves primárias | INT ou UUID | UUID para sistemas distribuídos |
| Chaves estrangeiras | Sempre restringir | Estratégia ON DELETE crítica |
| Índices | FKs + colunas WHERE | Ordem das colunas importa |
| Migrações | Sempre reversíveis | Compatível com versão anterior primeiro |

---

## Visão Geral do Processo

```
Seus Requisitos de Dados
    |
    v
+-----------------------------------------------------+
| Fase 1: ANÁLISE                                     |
| * Identificar entidades e relacionamentos           |
| * Determinar padrões de acesso (leitura vs escrita) |
| * Escolher SQL ou NoSQL baseado em requisitos      |
+-----------------------------------------------------+
    |
    v
+-----------------------------------------------------+
| Fase 2: DESIGN                                      |
| * Normalizar para 3FN (SQL) ou embed/reference      |
| * Definir chaves primárias e estrangeiras           |
| * Escolher tipos de dados apropriados               |
| * Adicionar restrições (UNIQUE, CHECK, NOT NULL)    |
+-----------------------------------------------------+
    |
    v
+-----------------------------------------------------+
| Fase 3: OTIMIZAR                                    |
| * Planejar estratégia de indexação                  |
| * Considerar desnormalização para consultas pesadas |
| * Adicionar timestamps (created_at, updated_at)     |
+-----------------------------------------------------+
    |
    v
+-----------------------------------------------------+
| Fase 4: MIGRAR                                      |
| * Gerar scripts de migração (up + down)             |
| * Garantir compatibilidade com versão anterior      |
| * Planejar deployment sem tempo de inatividade      |
+-----------------------------------------------------+
    |
    v
Esquema Pronto para Produção
```

---

## Comandos

| Comando | Quando Usar | Ação |
|---------|-------------|------|
| `design schema for {domain}` | Começando do zero | Geração completa de esquema |
| `normalize {table}` | Corrigindo tabela existente | Aplicar regras de normalização |
| `add indexes for {table}` | Problemas de desempenho | Gerar estratégia de indexação |
| `migration for {change}` | Evolução de esquema | Criar migração reversível |
| `review schema` | Code review | Auditar esquema existente |

**Workflow:** Comece com `design schema` → itere com `normalize` → otimize com `add indexes` → evolua com `migration`

---

## Princípios Centrais

| Princípio | POR QUÊ | Implementação |
|-----------|--------|----------------|
| Modelar o Domínio | UI muda, domínio não | Nomes de entidades refletem conceitos do negócio |
| Integridade de Dados Primeiro | Corrupção é custosa de corrigir | Restrições no nível de banco de dados |
| Otimizar para Padrão de Acesso | Não dá para otimizar para ambos | OLTP: normalizado, OLAP: desnormalizado |
| Planejar para Escala | Retrofit é doloroso | Estratégia de índice + plano de particionamento |

---

## Anti-Padrões

| Evitar | Por Quê | Instead |
|--------|---------|---------|
| VARCHAR(255) em tudo | Desperdiça armazenamento, esconde intenção | Dimensionar apropriadamente por campo |
| FLOAT para dinheiro | Erros de arredondamento | DECIMAL(10,2) |
| Sem restrições de FK | Dados órfãos | Sempre definir chaves estrangeiras |
| Sem índices em FKs | JOINs lentos | Indexar toda chave estrangeira |
| Armazenar datas como strings | Não consegue comparar/ordenar | Tipos DATE, TIMESTAMP |
| SELECT * em consultas | Busca dados desnecessários | Listas de coluna explícitas |
| Migrações não reversíveis | Não consegue reverter | Sempre escrever migração DOWN |
| Adicionar NOT NULL sem default | Quebra linhas existentes | Adicionar nullable, backfill, depois restringir |

---

## Checklist de Verificação

Após projetar um esquema:

- [ ] Toda tabela tem chave primária
- [ ] Todos os relacionamentos têm restrições de chave estrangeira
- [ ] Estratégia ON DELETE definida para cada FK
- [ ] Índices existem em todas as chaves estrangeiras
- [ ] Índices existem em colunas consultadas frequentemente
- [ ] Tipos de dados apropriados (DECIMAL para dinheiro, etc.)
- [ ] NOT NULL em campos obrigatórios
- [ ] Restrições UNIQUE onde necessário
- [ ] Restrições CHECK para validação
- [ ] Timestamps created_at e updated_at
- [ ] Scripts de migração são reversíveis
- [ ] Testado em staging com dados de produção

---

<details>
<summary><strong>Aprofundamento: Normalização (SQL)</strong></summary>

### Formas Normais

| Forma | Regra | Exemplo de Violação |
|-------|-------|---------------------|
| **1FN** | Valores atômicos, sem grupos repetidos | `product_ids = '1,2,3'` |
| **2FN** | 1FN + sem dependências parciais | customer_name em order_items |
| **3FN** | 2FN + sem dependências transitivas | country derivado de postal_code |

### Primeira Forma Normal (1FN)

```sql
-- RUIM: Múltiplos valores em coluna
CREATE TABLE orders (
  id INT PRIMARY KEY,
  product_ids VARCHAR(255)  -- '101,102,103'
);

-- BOM: Tabela separada para itens
CREATE TABLE orders (
  id INT PRIMARY KEY,
  customer_id INT
);

CREATE TABLE order_items (
  id INT PRIMARY KEY,
  order_id INT REFERENCES orders(id),
  product_id INT
);
```

### Segunda Forma Normal (2FN)

```sql
-- RUIM: customer_name depende apenas de customer_id
CREATE TABLE order_items (
  order_id INT,
  product_id INT,
  customer_name VARCHAR(100),  -- Dependência parcial!
  PRIMARY KEY (order_id, product_id)
);

-- BOM: Dados do cliente em tabela separada
CREATE TABLE customers (
  id INT PRIMARY KEY,
  name VARCHAR(100)
);
```

### Terceira Forma Normal (3FN)

```sql
-- RUIM: country depende de postal_code
CREATE TABLE customers (
  id INT PRIMARY KEY,
  postal_code VARCHAR(10),
  country VARCHAR(50)  -- Dependência transitiva!
);

-- BOM: Tabela separada de postal_codes
CREATE TABLE postal_codes (
  code VARCHAR(10) PRIMARY KEY,
  country VARCHAR(50)
);
```

### Quando Desnormalizar

| Cenário | Estratégia de Desnormalização |
|---------|-------------------------------|
| Relatórios com muitas leituras | Agregados pré-calculados |
| JOINs caros | Colunas derivadas em cache |
| Dashboards de analytics | Visualizações materializadas |

```sql
-- Desnormalizado para desempenho
CREATE TABLE orders (
  id INT PRIMARY KEY,
  customer_id INT,
  total_amount DECIMAL(10,2),  -- Calculado
  item_count INT               -- Calculado
);
```

</details>

<details>
<summary><strong>Aprofundamento: Tipos de Dados</strong></summary>

### Tipos String

| Tipo | Caso de Uso | Exemplo |
|------|------------|---------|
| CHAR(n) | Comprimento fixo | Códigos de estado, datas ISO |
| VARCHAR(n) | Comprimento variável | Nomes, emails |
| TEXT | Conteúdo longo | Artigos, descrições |

```sql
-- Bom dimensionamento
email VARCHAR(255)
phone VARCHAR(20)
country_code CHAR(2)
```

### Tipos Numéricos

| Tipo | Intervalo | Caso de Uso |
|------|-----------|------------|
| TINYINT | -128 a 127 | Idade, códigos de status |
| SMALLINT | -32K a 32K | Quantidades |
| INT | -2.1B a 2.1B | IDs, contagens |
| BIGINT | Muito grande | IDs grandes, timestamps |
| DECIMAL(p,s) | Precisão exata | Dinheiro |
| FLOAT/DOUBLE | Aproximado | Dados científicos |

```sql
-- SEMPRE usar DECIMAL para dinheiro
price DECIMAL(10, 2)  -- R$99.999.999,99

-- NUNCA usar FLOAT para dinheiro
price FLOAT  -- Erros de arredondamento!
```

### Tipos Data/Hora

```sql
DATE        -- 2025-10-31
TIME        -- 14:30:00
DATETIME    -- 2025-10-31 14:30:00
TIMESTAMP   -- Conversão automática de timezone

-- Sempre armazenar em UTC
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

### Booleano

```sql
-- PostgreSQL
is_active BOOLEAN DEFAULT TRUE

-- MySQL
is_active TINYINT(1) DEFAULT 1
```

</details>

<details>
<summary><strong>Aprofundamento: Estratégia de Indexação</strong></summary>

### Quando Criar Índices

| Sempre Indexar | Razão |
|----------------|-------|
| Chaves estrangeiras | Acelera JOINs |
| Colunas em cláusula WHERE | Acelera filtragem |
| Colunas em ORDER BY | Acelera ordenação |
| Restrições únicas | Força unicidade |

```sql
-- Índice de chave estrangeira
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Índice de padrão de consulta
CREATE INDEX idx_orders_status_date ON orders(status, created_at);
```

### Tipos de Índice

| Tipo | Melhor Para | Exemplo |
|------|-------------|---------|
| B-Tree | Intervalos, igualdade | `price > 100` |
| Hash | Apenas correspondência exata | `email = 'x@y.com'` |
| Full-text | Busca de texto | `MATCH AGAINST` |
| Parcial | Subconjunto de linhas | `WHERE is_active = true` |

### Ordem de Índice Composto

```sql
CREATE INDEX idx_customer_status ON orders(customer_id, status);

-- Usa índice (customer_id primeiro)
SELECT * FROM orders WHERE customer_id = 123;
SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending';

-- NÃO usa índice (status sozinho)
SELECT * FROM orders WHERE status = 'pending';
```

**Regra:** Coluna mais seletiva primeiro, ou coluna consultada sozinha com mais frequência.

### Armadilhas de Índice

| Armadilha | Problema | Solução |
|-----------|---------|---------|
| Sobre-indexação | Escritas lentas | Indexar apenas o que é consultado |
| Ordem de coluna errada | Índice não utilizado | Corresponder padrões de consulta |
| Índices FK faltantes | JOINs lentos | Sempre indexar FKs |

</details>

<details>
<summary><strong>Aprofundamento: Restrições</strong></summary>

### Chaves Primárias

```sql
-- Auto-increment (simples)
id INT AUTO_INCREMENT PRIMARY KEY

-- UUID (sistemas distribuídos)
id CHAR(36) PRIMARY KEY DEFAULT (UUID())

-- Composta (tabelas de junção)
PRIMARY KEY (student_id, course_id)
```

### Chaves Estrangeiras

```sql
FOREIGN KEY (customer_id) REFERENCES customers(id)
  ON DELETE CASCADE     -- Deletar filhos com pai
  ON DELETE RESTRICT    -- Prevenir deleção se referenciado
  ON DELETE SET NULL    -- Definir como NULL quando pai deletado
  ON UPDATE CASCADE     -- Atualizar filhos quando pai muda
```

| Estratégia | Usar Quando |
|-----------|-------------|
| CASCADE | Dados dependentes (order_items) |
| RESTRICT | Referências importantes (prevenir acidentes) |
| SET NULL | Relacionamentos opcionais |

### Outras Restrições

```sql
-- Único
email VARCHAR(255) UNIQUE NOT NULL

-- Único composto
UNIQUE (student_id, course_id)

-- Check
price DECIMAL(10,2) CHECK (price >= 0)
discount INT CHECK (discount BETWEEN 0 AND 100)

-- Not null
name VARCHAR(100) NOT NULL
```

</details>

<details>
<summary><strong>Aprofundamento: Padrões de Relacionamento</strong></summary>

### Um para Muitos

```sql
CREATE TABLE orders (
  id INT PRIMARY KEY,
  customer_id INT NOT NULL REFERENCES customers(id)
);

CREATE TABLE order_items (
  id INT PRIMARY KEY,
  order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id INT NOT NULL,
  quantity INT NOT NULL
);
```

### Muitos para Muitos

```sql
-- Tabela de junção
CREATE TABLE enrollments (
  student_id INT REFERENCES students(id) ON DELETE CASCADE,
  course_id INT REFERENCES courses(id) ON DELETE CASCADE,
  enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (student_id, course_id)
);
```

### Auto-Referenciado

```sql
CREATE TABLE employees (
  id INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  manager_id INT REFERENCES employees(id)
);
```

### Polimórfico

```sql
-- Abordagem 1: FKs separadas (integridade mais forte)
CREATE TABLE comments (
  id INT PRIMARY KEY,
  content TEXT NOT NULL,
  post_id INT REFERENCES posts(id),
  photo_id INT REFERENCES photos(id),
  CHECK (
    (post_id IS NOT NULL AND photo_id IS NULL) OR
    (post_id IS NULL AND photo_id IS NOT NULL)
  )
);

-- Abordagem 2: Tipo + ID (flexível, integridade mais fraca)
CREATE TABLE comments (
  id INT PRIMARY KEY,
  content TEXT NOT NULL,
  commentable_type VARCHAR(50) NOT NULL,
  commentable_id INT NOT NULL
);
```

</details>

<details>
<summary><strong>Aprofundamento: Design NoSQL (MongoDB)</strong></summary>

### Embedding vs Referencing

| Fator | Embed | Reference |
|-------|-------|-----------|
| Padrão de acesso | Ler junto | Ler separadamente |
| Relacionamento | 1:poucos | 1:muitos |
| Tamanho do documento | Pequeno | Próximo de 16MB |
| Frequência de atualização | Raramente | Frequentemente |

### Documento Embedido

```json
{
  "_id": "order_123",
  "customer": {
    "id": "cust_456",
    "name": "Jane Smith",
    "email": "jane@example.com"
  },
  "items": [
    { "product_id": "prod_789", "quantity": 2, "price": 29.99 }
  ],
  "total": 109.97
}
```

### Documento Referenciado

```json
{
  "_id": "order_123",
  "customer_id": "cust_456",
  "item_ids": ["item_1", "item_2"],
  "total": 109.97
}
```

### Índices MongoDB

```javascript
// Campo único
db.users.createIndex({ email: 1 }, { unique: true });

// Composto
db.orders.createIndex({ customer_id: 1, created_at: -1 });

// Busca de texto
db.articles.createIndex({ title: "text", content: "text" });

// Geoespacial
db.stores.createIndex({ location: "2dsphere" });
```

</details>

<details>
<summary><strong>Aprofundamento: Migrações</strong></summary>

### Boas Práticas de Migração

| Prática | POR QUÊ |
|---------|---------|
| Sempre reversível | Precisa reverter |
| Compatível com versão anterior | Zero-downtime deploys |
| Schema antes dos dados | Separar responsabilidades |
| Testar em staging | Pegar problemas cedo |

### Adicionar Coluna (Zero-Downtime)

```sql
-- Passo 1: Adicionar coluna nullable
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Passo 2: Deploy de código que escreve na nova coluna

-- Passo 3: Backfill de linhas existentes
UPDATE users SET phone = '' WHERE phone IS NULL;

-- Passo 4: Fazer obrigatório (se necessário)
ALTER TABLE users MODIFY phone VARCHAR(20) NOT NULL;
```

### Renomear Coluna (Zero-Downtime)

```sql
-- Passo 1: Adicionar nova coluna
ALTER TABLE users ADD COLUMN email_address VARCHAR(255);

-- Passo 2: Copiar dados
UPDATE users SET email_address = email;

-- Passo 3: Deploy de código lendo da nova coluna
-- Passo 4: Deploy de código escrevendo na nova coluna

-- Passo 5: Dropar coluna antiga
ALTER TABLE users DROP COLUMN email;
```

### Template de Migração

```sql
-- Migration: YYYYMMDDHHMMSS_description.sql

-- UP
BEGIN;
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
CREATE INDEX idx_users_phone ON users(phone);
COMMIT;

-- DOWN
BEGIN;
DROP INDEX idx_users_phone ON users;
ALTER TABLE users DROP COLUMN phone;
COMMIT;
```

</details>

<details>
<summary><strong>Aprofundamento: Otimização de Desempenho</strong></summary>

### Análise de Consulta

```sql
EXPLAIN SELECT * FROM orders
WHERE customer_id = 123 AND status = 'pending';
```

| Procure Por | Significado |
|-------------|-------------|
| type: ALL | Full table scan (ruim) |
| type: ref | Índice usado (bom) |
| key: NULL | Nenhum índice usado |
| rows: alto | Muitas linhas escaneadas |

### Problema N+1 Queries

```python
# RUIM: N+1 queries
orders = db.query("SELECT * FROM orders")
for order in orders:
    customer = db.query(f"SELECT * FROM customers WHERE id = {order.customer_id}")

# BOM: Single JOIN
results = db.query("""
    SELECT orders.*, customers.name
    FROM orders
    JOIN customers ON orders.customer_id = customers.id
""")
```

### Técnicas de Otimização

| Técnica | Quando Usar |
|---------|-------------|
| Adicionar índices | WHERE/ORDER BY lentos |
| Desnormalizar | JOINs caros |
| Paginação | Grandes conjuntos de resultados |
| Caching | Consultas repetidas |
| Read replicas | Carga de leitura pesada |
| Particionamento | Tabelas muito grandes |

</details>

---

## Pontos de Extensão

1. **Padrões Específicos de Banco de Dados:** Adicionar variações MySQL vs PostgreSQL vs SQLite
2. **Padrões Avançados:** Time-series, event sourcing, CQRS, multi-tenancy
3. **Integração com ORM:** Padrões TypeORM, Prisma, SQLAlchemy
4. **Monitoramento:** Rastreamento de desempenho de consultas, alertas de consulta lenta