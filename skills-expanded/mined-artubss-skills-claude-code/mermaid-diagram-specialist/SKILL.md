---
name: mermaid-diagram-specialist
category: tech
description:
  Especialista em diagramas Mermaid para criar fluxogramas, diagramas de sequência, DERs
  e visualizações de arquitetura
usage:
  Use ao criar documentação técnica, visualizar workflows, documentar
  arquitetura ou explicar design de sistemas
input:
  Descrição de processo, modelo de dados, requisitos de arquitetura, etapas de workflow
output: Diagramas Mermaid (flowchart, sequence, ERD, C4, state, etc.) em markdown
---

# Especialista em Diagramas Mermaid

## Visão Geral

**Propósito**: Especialista em criar diagramas Mermaid abrangentes para
documentação, visualização de arquitetura e mapeamento de processos

**Categoria**: Tech **Usuários Principais**: tech-writer, architecture-validator,
product-technical, tech-lead

## Quando Usar Esta Habilidade

- Criando documentação de arquitetura
- Visualizando workflows e processos
- Documentando modelos de dados (DERs)
- Explicando fluxos de sequência
- Criando máquinas de estado
- Documentando relacionamentos entre componentes
- Criando árvores de decisão
- Visualizando jornadas de usuários

## Pré-requisitos

**Obrigatório:**

- Entendimento do sistema/processo a documentar
- Acesso às especificações técnicas
- Conhecimento do tipo de diagrama necessário

**Opcional:**

- Cores do design system para consistência
- Documentação existente como referência

## Input

**O que a habilidade precisa:**

- Descrição de processo/sistema
- Entidades e relacionamentos (para DERs)
- Interações entre componentes (para diagramas de sequência)
- Camadas de arquitetura (para diagramas C4)
- Estados e transições (para diagramas de estado)

## Workflow

### Etapa 1: Seleção do Tipo de Diagrama

**Objetivo**: Escolher o tipo de diagrama apropriado para os requisitos

**Tipos de Diagramas Disponíveis:**

1. **Flowchart**: Fluxos de decisão, algoritmos, processos
2. **Sequence Diagram**: Interações de API, fluxos de mensagens
3. **ERD**: Schemas de banco de dados, relacionamentos de entidades
4. **Class Diagram**: Design orientado a objetos
5. **State Diagram**: Máquinas de estado, ciclo de vida
6. **Gantt Chart**: Cronogramas de projetos, agendas
7. **C4 Diagram**: Arquitetura em diferentes níveis
8. **Pie/Bar Charts**: Visualização de dados
9. **Git Graph**: Fluxos de controle de versão
10. **User Journey**: Fluxos de experiência do usuário

**Matriz de Decisão:**

- Processo com decisões → **Flowchart**
- Interações de API/sistema → **Sequence Diagram**
- Estrutura de banco de dados → **ERD**
- Arquitetura de sistema → **C4 Diagram**
- Relacionamentos de objetos → **Class Diagram**
- Transições de estado → **State Diagram**
- Cronograma de projeto → **Gantt Chart**

**Validação:**

- [ ] Tipo de diagrama corresponde ao conteúdo
- [ ] Complexidade apropriada
- [ ] Audiência considerada
- [ ] Objetivo claro

**Output**: Tipo de diagrama selecionado

### Etapa 2: Criação de Fluxogramas

**Objetivo**: Criar diagramas de fluxo de processo e decisão

**Sintaxe:**

```mermaid
flowchart TD
    Start([Start]) --> Input[/User Input/]
    Input --> Validate{Valid?}
    Validate -->|Yes| Process[Process Data]
    Validate -->|No| Error[Show Error]
    Error --> Input
    Process --> Save[(Save to DB)]
    Save --> Success[/Success Response/]
    Success --> End([End])
```

**Formatos de Nós:**

- `[Rectangle]` - Etapa de processo
- `([Rounded])` - Início/Fim
- `{Diamond}` - Decisão
- `[/Parallelogram/]` - Input/Output
- `[(Database)]` - Armazenamento de dados
- `((Circle))` - Conector

**Opções de Direção:**

- `TD` - De cima para baixo
- `LR` - Esquerda para direita
- `BT` - De baixo para cima
- `RL` - Direita para esquerda

**Exemplo - Fluxo de Reserva:**

```mermaid
flowchart TD
    Start([Usuário Inicia Reserva]) --> CheckDates[Verificar Disponibilidade de Datas]
    CheckDates --> Available{Datas Disponíveis?}
    Available -->|Não| ShowError[/Mostrar Mensagem Indisponível/]
    ShowError --> End([Fim])
    Available -->|Sim| CreateBooking[Criar Reserva Pendente]
    CreateBooking --> Payment[Processar Pagamento]
    Payment --> PaymentSuccess{Pagamento Bem-sucedido?}
    PaymentSuccess -->|Não| CancelBooking[Cancelar Reserva]
    CancelBooking --> ShowError
    PaymentSuccess -->|Sim| ConfirmBooking[Confirmar Reserva]
    ConfirmBooking --> SendEmail[/Enviar Email de Confirmação/]
    SendEmail --> SaveDB[(Salvar no Banco de Dados)]
    SaveDB --> Success[/Mostrar Sucesso/]
    Success --> End
```

**Validação:**

- [ ] Todos os caminhos cobertos
- [ ] Pontos de decisão claros
- [ ] Início e fim definidos
- [ ] Direção de fluxo lógica

**Output**: Fluxograma de processo

### Etapa 3: Criação de Diagramas de Sequência

**Objetivo**: Documentar interações de API e fluxos de mensagens

**Sintaxe:**

```mermaid
sequenceDiagram
    actor User
    participant Frontend
    participant API
    participant DB
    participant Payment

    User->>Frontend: Click "Book"
    Frontend->>API: POST /api/bookings
    API->>DB: Check availability
    DB-->>API: Available
    API->>Payment: Process payment
    Payment-->>API: Payment successful
    API->>DB: Create booking
    DB-->>API: Booking created
    API-->>Frontend: 201 Created
    Frontend-->>User: Show confirmation
```

**Tipos de Participantes:**

- `actor` - Usuário humano
- `participant` - Sistema/Serviço
- `database` - Banco de dados

**Tipos de Seta:**

- `->` - Linha sólida (síncrona)
- `-->` - Linha pontilhada (resposta)
- `->>` - Seta sólida (mensagem assíncrona)
- `-->>` - Seta pontilhada (resposta assíncrona)

**Exemplo - Fluxo de Autenticação:**

```mermaid
sequenceDiagram
    actor User
    participant Frontend
    participant API
    participant Clerk
    participant DB

    User->>Frontend: Insira credenciais
    Frontend->>Clerk: Solicitação de login
    Clerk->>Clerk: Validar credenciais
    alt Credenciais válidas
        Clerk-->>Frontend: Token JWT
        Frontend->>API: Solicitar com token
        API->>Clerk: Verificar token
        Clerk-->>API: Token válido
        API->>DB: Buscar dados do usuário
        DB-->>API: Dados do usuário
        API-->>Frontend: Sessão do usuário
        Frontend-->>User: Usuário conectado
    else Credenciais inválidas
        Clerk-->>Frontend: Erro de autenticação
        Frontend-->>User: Mostrar erro
    end
```

**Validação:**

- [ ] Todos os participantes identificados
- [ ] Fluxo de mensagens lógico
- [ ] Mensagens de retorno mostradas
- [ ] Blocos alt/loop usados corretamente

**Output**: Diagrama de sequência

### Etapa 4: Criação de DER

**Objetivo**: Documentar schema de banco de dados e relacionamentos

**Sintaxe:**

```mermaid
erDiagram
    USER ||--o{ BOOKING : creates
    ACCOMMODATION ||--o{ BOOKING : "booked for"
    USER {
        uuid id PK
        string email UK
        string name
        timestamp created_at
    }
    BOOKING {
        uuid id PK
        uuid user_id FK
        uuid accommodation_id FK
        date check_in
        date check_out
        enum status
    }
    ACCOMMODATION {
        uuid id PK
        string name
        text description
        decimal price_per_night
    }
```

**Tipos de Relacionamento:**

- `||--||` - Um para um
- `||--o{` - Um para muitos
- `}o--o{` - Muitos para muitos
- `||--o|` - Um para zero ou um

**Símbolos de Cardinalidade:**

- `||` - Exatamente um
- `o|` - Zero ou um
- `}o` - Zero ou mais
- `}|` - Um ou mais

**Exemplo - DER Completo de Hospeda:**

```mermaid
erDiagram
    USER ||--o{ BOOKING : creates
    USER ||--o{ REVIEW : writes
    USER ||--o{ ACCOMMODATION : owns
    ACCOMMODATION ||--o{ BOOKING : "has bookings"
    ACCOMMODATION ||--o{ REVIEW : "has reviews"
    ACCOMMODATION }o--o{ AMENITY : includes
    BOOKING ||--|| PAYMENT : "has payment"

    USER {
        uuid id PK
        string clerk_id UK
        string email UK
        string name
        enum role
        timestamp created_at
    }

    ACCOMMODATION {
        uuid id PK
        uuid owner_id FK
        string name
        text description
        decimal price_per_night
        int max_guests
        enum status
    }

    BOOKING {
        uuid id PK
        uuid user_id FK
        uuid accommodation_id FK
        date check_in
        date check_out
        int guests
        enum status
        decimal total_price
    }

    REVIEW {
        uuid id PK
        uuid user_id FK
        uuid accommodation_id FK
        int rating
        text comment
        timestamp created_at
    }

    PAYMENT {
        uuid id PK
        uuid booking_id FK
        string mercadopago_id UK
        decimal amount
        enum status
        timestamp processed_at
    }

    AMENITY {
        uuid id PK
        string name
        string icon
    }
```

**Validação:**

- [ ] Todas as entidades definidas
- [ ] Relacionamentos precisos
- [ ] Cardinalidade correta
- [ ] Chaves primárias/estrangeiras marcadas

**Output**: Diagrama DER

### Etapa 5: Diagramas de Arquitetura C4

**Objetivo**: Documentar arquitetura de sistema em diferentes níveis

**Nível de Contexto** (Sistema no ambiente):

```mermaid
C4Context
    title System Context - Plataforma Hospeda

    Person(guest, "Hóspede", "Turista procurando hospedagem")
    Person(owner, "Proprietário", "Proprietário de hospedagem")
    System(hospeda, "Plataforma Hospeda", "Plataforma de reservas de turismo")

    System_Ext(clerk, "Clerk", "Provedor de autenticação")
    System_Ext(mercadopago, "Mercado Pago", "Processador de pagamentos")
    System_Ext(email, "Serviço de Email", "Emails transacionais")

    Rel(guest, hospeda, "Busca e reserva", "HTTPS")
    Rel(owner, hospeda, "Gerencia listagens", "HTTPS")
    Rel(hospeda, clerk, "Autentica usuários", "API")
    Rel(hospeda, mercadopago, "Processa pagamentos", "API")
    Rel(hospeda, email, "Envia notificações", "SMTP")
```

**Nível de Container** (Aplicações e armazenamentos de dados):

```mermaid
C4Container
    title Container - Plataforma Hospeda

    Person(user, "Usuário")

    Container(web, "Aplicação Web", "Astro + React", "Site público")
    Container(admin, "Painel Admin", "TanStack Start", "Interface de gerenciamento")
    Container(api, "API", "Hono", "Serviços backend")
    ContainerDb(db, "Banco de Dados", "PostgreSQL", "Armazena todos os dados")

    Rel(user, web, "Usa", "HTTPS")
    Rel(user, admin, "Gerencia", "HTTPS")
    Rel(web, api, "Chama", "JSON/HTTPS")
    Rel(admin, api, "Chama", "JSON/HTTPS")
    Rel(api, db, "Lê/Escreve", "SQL")
```

**Nível de Componente** (Estrutura interna):

```mermaid
C4Component
    title Components - Aplicação API

    Container(api, "API", "Hono")

    Component(routes, "Routes", "Hono Router", "Endpoints HTTP")
    Component(services, "Services", "Business Logic", "Operações de domínio")
    Component(models, "Models", "Data Access", "Operações de BD")
    Component(middleware, "Middleware", "Cross-cutting", "Autenticação, logging, erros")

    Rel(routes, middleware, "Usa")
    Rel(routes, services, "Chama")
    Rel(services, models, "Usa")
    Rel(models, db, "Consulta")
```

**Validação:**

- [ ] Nível apropriado selecionado
- [ ] Todos os sistemas/containers mostrados
- [ ] Relacionamentos claros
- [ ] Sistemas externos identificados

**Output**: Diagramas de arquitetura C4

### Etapa 6: Criação de Diagramas de Estado

**Objetivo**: Documentar máquinas de estado e ciclos de vida

**Sintaxe:**

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> Confirmed : Payment Success
    Pending --> Cancelled : Payment Failed
    Pending --> Cancelled : User Cancels
    Confirmed --> CheckedIn : Check-in Date
    Confirmed --> Cancelled : Cancellation Request
    CheckedIn --> CheckedOut : Check-out Date
    CheckedOut --> Reviewed : User Submits Review
    CheckedOut --> [*] : 30 Days Elapsed
    Reviewed --> [*]
    Cancelled --> [*]
```

**Exemplo - Ciclo de Vida de Reserva:**

```mermaid
stateDiagram-v2
    [*] --> Draft : Criar Reserva

    state "Pagamento Pendente" as Pending
    state "Processando Pagamento" as Processing

    Draft --> Pending : Submeter Reserva
    Pending --> Processing : Iniciar Pagamento

    Processing --> Confirmed : Pagamento Aprovado
    Processing --> PaymentFailed : Pagamento Recusado

    PaymentFailed --> Pending : Tentar Novamente
    PaymentFailed --> Cancelled : Máximo de Tentativas

    Confirmed --> Active : Data de Check-in Atingida
    Active --> Completed : Data de Check-out Atingida

    Confirmed --> CancelRequested : Solicitação de Cancelamento
    CancelRequested --> RefundProcessing : Aprovar Cancelamento
    RefundProcessing --> Cancelled : Reembolso Concluído

    Completed --> [*]
    Cancelled --> [*]

    note right of Confirmed
        Proprietário notificado
        Calendário bloqueado
    end note

    note right of Completed
        Avaliação solicitada
        Pagamento liberado
    end note
```

**Validação:**

- [ ] Todos os estados definidos
- [ ] Transições lógicas
- [ ] Estados inicial/final marcados
- [ ] Notas explicam estados-chave

**Output**: Diagrama de estado

### Etapa 7: Styling e Customização

**Objetivo**: Aplicar styling consistente aos diagramas

**Aplicação de Tema:**

```mermaid
%%{init: {'theme':'base', 'themeVariables': {
  'primaryColor':'#3B82F6',
  'primaryTextColor':'#fff',
  'primaryBorderColor':'#2563EB',
  'lineColor':'#6B7280',
  'secondaryColor':'#10B981',
  'tertiaryColor':'#F59E0B'
}}}%%
flowchart TD
    A[Start] --> B[Process]
    B --> C[End]
```

**Styling de Classes:**

```mermaid
flowchart TD
    A[Normal] --> B[Success]
    B --> C[Error]

    classDef successClass fill:#10B981,stroke:#059669,color:#fff
    classDef errorClass fill:#EF4444,stroke:#DC2626,color:#fff

    class B successClass
    class C errorClass
```

**Validação:**

- [ ] Cores correspondem à marca
- [ ] Contraste suficiente
- [ ] Styling consistente
- [ ] Legível em ambos os temas

**Output**: Diagramas com styling

## Output

**Produz:**

- Código de diagrama Mermaid em markdown
- Múltiplos tipos de diagrama conforme necessário
- Diagramas com styling e tema
- Visualizações prontas para documentação

**Critérios de Sucesso:**

- Diagrama representa com precisão o sistema
- Todos os elementos adequadamente rotulados
- Relacionamentos claros e corretos
- Styling consistente com marca
- Renderiza corretamente em markdown

## Melhores Práticas

1. **Simplicidade**: Manter diagramas focados e sem poluição visual
2. **Labels**: Rótulos claros e descritivos para todos os elementos
3. **Direção**: Direção de fluxo consistente (geralmente de cima para baixo ou esquerda para direita)
4. **Agrupamento**: Usar subgráficos para agrupar elementos relacionados
5. **Cores**: Usar cores para destacar elementos importantes
6. **Notas**: Adicionar notas para explicar lógica complexa
7. **Níveis**: Usar nível de abstração apropriado para a audiência
8. **Atualizações**: Manter diagramas sincronizados com código
9. **Comentários**: Adicionar comentários no código Mermaid para manutenibilidade
10. **Testes**: Verificar que diagramas renderizam na plataforma de destino

## Padrões Comuns

### Fluxo de Solicitação de API

```mermaid
sequenceDiagram
    Client->>+API: GET /resource
    API->>+Service: fetchResource()
    Service->>+Model: findById()
    Model->>+DB: SELECT query
    DB-->>-Model: Row data
    Model-->>-Service: Entity
    Service-->>-API: DTO
    API-->>-Client: JSON response
```

### Fluxo de Tratamento de Erro

```mermaid
flowchart TD
    Request[Solicitação Recebida] --> Validate{Válido?}
    Validate -->|Não| ValidationError[Erro de Validação]
    ValidationError --> ErrorHandler[Manipulador de Erro]
    Validate -->|Sim| Process[Processar Solicitação]
    Process --> DB{Sucesso no BD?}
    DB -->|Não| DBError[Erro de Banco de Dados]
    DBError --> ErrorHandler
    DB -->|Sim| Success[Resposta de Sucesso]
    ErrorHandler --> LogError[Registrar Erro]
    LogError --> ErrorResponse[Resposta de Erro]
```

## Observações

- Mermaid renderiza no GitHub, GitLab, Notion e na maioria dos visualizadores de markdown
- Editor ao vivo disponível em mermaid.live
- Complexidade máxima: Manter abaixo de 20 nós para legibilidade
- Usar subgráficos para agrupar nós relacionados
- Testar renderização na plataforma de destino antes de commitar
- Manter fonte de diagrama em arquivos markdown, não em imagens
- Controlar versão de diagramas com código
- Atualizar diagramas durante revisão de código