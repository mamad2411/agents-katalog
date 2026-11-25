---
name: kaizen
description: Guia para melhoria contínua, à prova de erros e padronização. Use esta skill quando o usuário quiser melhorar a qualidade do código, refatorar ou discutir melhorias de processo.
---

# Kaizen: Melhoria Contínua

## Visão Geral

Pequenas melhorias, continuamente. À prova de erros por design. Siga o que funciona. Construa apenas o necessário.

**Princípio central:** Muitas pequenas melhorias superam uma grande mudança. Previna erros no tempo de design, não com correções.

## Quando Usar

**Sempre aplicado para:**

- Implementação e refatoração de código
- Decisões de arquitetura e design
- Melhorias de processo e workflow
- Tratamento de erros e validação

**Filosofia:** Qualidade através de progresso incremental e prevenção, não perfeição através de esforço massivo.

## Os Quatro Pilares

### 1. Melhoria Contínua (Kaizen)

Pequenas melhorias frequentes se acumulam em ganhos significativos.

#### Princípios

**Incremental sobre revolucionário:**

- Faça a menor mudança viável que melhora a qualidade
- Uma melhoria por vez
- Verifique cada mudança antes da próxima
- Construa momentum através de pequenas vitórias

**Sempre deixe o código melhor:**

- Corrija pequenos problemas conforme encontrar
- Refatore enquanto trabalha (dentro do escopo)
- Atualize comentários desatualizados
- Remova código morto quando vir

**Refinamento iterativo:**

- Primeira versão: faça funcionar
- Segunda passagem: torne claro
- Terceira passagem: torne eficiente
- Não tente fazer os três de uma vez

<Good>
```typescript
// Iteração 1: Faça funcionar
const calculateTotal = (items: Item[]) => {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total += items[i].price * items[i].quantity;
  }
  return total;
};

// Iteração 2: Torne claro (refatore)
const calculateTotal = (items: Item[]): number => {
  return items.reduce((total, item) => {
    return total + (item.price * item.quantity);
  }, 0);
};

// Iteração 3: Torne robusto (adicione validação)
const calculateTotal = (items: Item[]): number => {
  if (!items?.length) return 0;

  return items.reduce((total, item) => {
    if (item.price < 0 || item.quantity < 0) {
      throw new Error('Price and quantity must be non-negative');
    }
    return total + (item.price * item.quantity);
  }, 0);
};
```
Cada passo está completo, testado e funcionando
</Good>

<Bad>
```typescript
// Tentando fazer tudo de uma vez
const calculateTotal = (items: Item[]): number => {
  // Valide, otimize, adicione recursos, trate casos extremos tudo junto
  if (!items?.length) return 0;
  const validItems = items.filter(item => {
    if (item.price < 0) throw new Error('Negative price');
    if (item.quantity < 0) throw new Error('Negative quantity');
    return item.quantity > 0; // Também filtrando quantidades zero
  });
  // Mais caching, mais logging, mais conversão de moeda...
  return validItems.reduce(...); // Muitas responsabilidades de uma vez
};
```
Avassalador, propenso a erros, difícil de verificar
</Bad>

#### Na Prática

**Ao implementar recursos:**

1. Comece com a versão mais simples que funciona
2. Adicione uma melhoria (tratamento de erros, validação, etc.)
3. Teste e verifique
4. Repita se tempo permitir
5. Não tente tornar perfeito imediatamente

**Ao refatorar:**

- Corrija um smell de cada vez
- Faça commit após cada melhoria
- Mantenha testes passando o tempo todo
- Pare quando "bom o suficiente" (retornos decrescentes)

**Ao revisar código:**

- Sugira melhorias incrementais (não reescritas)
- Priorize: crítico → importante → bom ter
- Foque nas mudanças de maior impacto primeiro
- Aceite "melhor que antes" mesmo que não perfeito

### 2. Poka-Yoke (À Prova de Erros)

Projete sistemas que previnem erros no tempo de compilação/design, não em tempo de execução.

#### Princípios

**Torne erros impossíveis:**

- Sistema de tipos captura erros
- Compilador executa contratos
- Estados inválidos irrepresentáveis
- Erros capturados cedo (esquerda da produção)

**Projete para segurança:**

- Falhe rápido e alto
- Forneça mensagens de erro úteis
- Torne o caminho correto óbvio
- Torne o caminho incorreto difícil

**Defesa em camadas:**

1. Sistema de tipos (tempo de compilação)
2. Validação (tempo de execução, cedo)
3. Guards (pré-condições)
4. Error boundaries (degradação graciosa)

#### À Prova de Erros com Sistema de Tipos

<Good>
```typescript
// Erro: status string pode ser qualquer valor
type OrderBad = {
  status: string; // Pode ser "pending", "PENDING", "pnding", qualquer coisa!
  total: number;
};

// Bom: Apenas estados válidos possíveis
type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered';
type Order = {
  status: OrderStatus;
  total: number;
};

// Melhor: Estados com dados associados
type Order =
  | { status: 'pending'; createdAt: Date }
  | { status: 'processing'; startedAt: Date; estimatedCompletion: Date }
  | { status: 'shipped'; trackingNumber: string; shippedAt: Date }
  | { status: 'delivered'; deliveredAt: Date; signature: string };

// Agora é impossível ter shipped sem trackingNumber
```
Sistema de tipos previne classes inteiras de erros
</Good>

<Good>
```typescript
// Torne estados inválidos irrepresentáveis
type NonEmptyArray<T> = [T, ...T[]];

const firstItem = <T>(items: NonEmptyArray<T>): T => {
  return items[0]; // Sempre seguro, nunca undefined!
};

// Chamador deve provar que array não está vazio
const items: number[] = [1, 2, 3];
if (items.length > 0) {
  firstItem(items as NonEmptyArray<number>); // Seguro
}
```
Assinatura de função garante segurança
</Good>

#### À Prova de Erros com Validação

<Good>
```typescript
// Erro: Validação após uso
const processPayment = (amount: number) => {
  const fee = amount * 0.03; // Usado antes de validação!
  if (amount <= 0) throw new Error('Invalid amount');
  // ...
};

// Bom: Valide imediatamente
const processPayment = (amount: number) => {
  if (amount <= 0) {
    throw new Error('Payment amount must be positive');
  }
  if (amount > 10000) {
    throw new Error('Payment exceeds maximum allowed');
  }

  const fee = amount * 0.03;
  // ... agora seguro usar
};

// Melhor: Validação no boundary com tipo marcado
type PositiveNumber = number & { readonly __brand: 'PositiveNumber' };

const validatePositive = (n: number): PositiveNumber => {
  if (n <= 0) throw new Error('Must be positive');
  return n as PositiveNumber;
};

const processPayment = (amount: PositiveNumber) => {
  // amount é garantido positivo, não precisa verificar
  const fee = amount * 0.03;
};

// Valide no boundary do sistema
const handlePaymentRequest = (req: Request) => {
  const amount = validatePositive(req.body.amount); // Valide uma vez
  processPayment(amount); // Use em todo lugar com segurança
};
```
Valide uma vez no boundary, seguro em todo lugar
</Good>

#### Guards e Pré-condições

<Good>
```typescript
// Early returns evitam código profundamente aninhado
const processUser = (user: User | null) => {
  if (!user) {
    logger.error('User not found');
    return;
  }

  if (!user.email) {
    logger.error('User email missing');
    return;
  }

  if (!user.isActive) {
    logger.info('User inactive, skipping');
    return;
  }

  // Lógica principal aqui, user garantido válido e ativo
  sendEmail(user.email, 'Welcome!');
};
```
Guards tornam suposições explícitas e enforçadas
</Good>

#### À Prova de Erros com Configuração

<Good>
```typescript
// Erro: Config opcional com padrões inseguros
type ConfigBad = {
  apiKey?: string;
  timeout?: number;
};

const client = new APIClient({ timeout: 5000 }); // apiKey faltando!

// Bom: Config requerida, falha cedo
type Config = {
  apiKey: string;
  timeout: number;
};

const loadConfig = (): Config => {
  const apiKey = process.env.API_KEY;
  if (!apiKey) {
    throw new Error('API_KEY environment variable required');
  }

  return {
    apiKey,
    timeout: 5000,
  };
};

// App falha ao iniciar se config inválida, não durante request
const config = loadConfig();
const client = new APIClient(config);
```
Falhe ao iniciar, não em produção
</Good>

#### Na Prática

**Ao projetar APIs:**
- Use tipos para restringir inputs
- Torne estados inválidos irrepresentáveis
- Retorne Result<T, E> em vez de jogar exceção
- Documente pré-condições em tipos

**Ao tratar erros:**
- Valide em boundaries do sistema
- Use guards para pré-condições
- Falhe rápido com mensagens claras
- Registre contexto para debugging

**Ao configurar:**
- Requerido sobre opcional com padrões
- Valide toda config ao iniciar
- Falhe no deployment se config inválida
- Não permita configurações parciais

### 3. Trabalho Padronizado

Siga padrões estabelecidos. Documente o que funciona. Torne boas práticas fáceis de seguir.

#### Princípios

**Consistência sobre criatividade:**
- Siga padrões de codebase existentes
- Não reinvente problemas resolvidos
- Novo padrão apenas se significativamente melhor
- Acordo em equipe sobre novos padrões

**Documentação vive com código:**
- README para setup e arquitetura
- CLAUDE.md para convenções de codificação IA
- Comentários para "por quê", não "o quê"
- Exemplos para padrões complexos

**Automatize padrões:**
- Linters enforcement de estilo
- Type checks enforcement de contratos
- Testes verificam comportamento
- CI/CD enforcement de quality gates

#### Seguindo Padrões

<Good>
```typescript
// Padrão de codebase existente para API clients
class UserAPIClient {
  async getUser(id: string): Promise<User> {
    return this.fetch(`/users/${id}`);
  }
}

// Novo código segue o mesmo padrão
class OrderAPIClient {
  async getOrder(id: string): Promise<Order> {
    return this.fetch(`/orders/${id}`);
  }
}
```
Consistência torna codebase previsível
</Good>

<Bad>
```typescript
// Padrão existente usa classes
class UserAPIClient { /* ... */ }

// Novo código introduz padrão diferente sem discussão
const getOrder = async (id: string): Promise<Order> => {
  // Quebrando consistência "porque prefiro funções"
};
```
Inconsistência cria confusão
</Bad>

#### Padrões de Tratamento de Erros

<Good>
```typescript
// Padrão do projeto: Tipo Result para erros recuperáveis
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

// Todos os serviços seguem este padrão
const fetchUser = async (id: string): Promise<Result<User, Error>> => {
  try {
    const user = await db.users.findById(id);
    if (!user) {
      return { ok: false, error: new Error('User not found') };
    }
    return { ok: true, value: user };
  } catch (err) {
    return { ok: false, error: err as Error };
  }
};

// Chamadores usam padrão consistente
const result = await fetchUser('123');
if (!result.ok) {
  logger.error('Failed to fetch user', result.error);
  return;
}
const user = result.value; // Type-safe!
```
Padrão padrão através de codebase
</Good>

#### Padrões de Documentação

<Good>
```typescript
/**
 * Retenta uma operação assíncrona com backoff exponencial.
 *
 * Por quê: Requests de rede falham temporariamente; retentativas melhoram confiabilidade
 * Quando usar: Chamadas de API externa, operações de banco de dados
 * Quando não usar: Validação de entrada de usuário, chamadas de função interna
 *
 * @example
 * const result = await retry(
 *   () => fetch('https://api.example.com/data'),
 *   { maxAttempts: 3, baseDelay: 1000 }
 * );
 */
const retry = async <T>(
  operation: () => Promise<T>,
  options: RetryOptions
): Promise<T> => {
  // Implementação...
};
```
Documenta por quê, quando e como
</Good>

#### Na Prática

**Antes de adicionar novos padrões:**

- Procure no codebase por problemas similares resolvidos
- Verifique CLAUDE.md para convenções do projeto
- Discuta com a equipe se quebrando padrão
- Atualize docs ao introduzir novo padrão

**Ao escrever código:**

- Combine estrutura de arquivo existente
- Use mesmas convenções de nomenclatura
- Siga mesma abordagem de tratamento de erros
- Importe de mesmos locais

**Ao revisar:**

- Verifique consistência com código existente
- Aponte para exemplos no codebase
- Sugira alinhar com padrões
- Atualize CLAUDE.md se novo padrão emergir

### 4. Just-In-Time (JIT)

Construa o que é necessário agora. Nem mais, nem menos. Evite otimização prematura e over-engineering.

#### Princípios

**YAGNI (Você Não Vai Precisar Disso):**

- Implemente apenas requisitos atuais
- Sem recursos "só em caso"
- Sem código "podemos precisar depois"
- Delete especulação

**Coisa mais simples que funciona:**

- Comece com solução direta
- Adicione complexidade apenas quando necessário
- Refatore quando requisitos mudam
- Não antecipe necessidades futuras

**Otimize quando mensurado:**

- Sem otimização prematura
- Profile antes de otimizar
- Meça impacto de mudanças
- Aceite performance "bom o suficiente"

#### YAGNI em Ação

<Good>
```typescript
// Requisito atual: Registre erros no console
const logError = (error: Error) => {
  console.error(error.message);
};
```
Simples, atende necessidade atual
</Good>

<Bad>
```typescript
// Over-engineered para "necessidades futuras"
interface LogTransport {
  write(level: LogLevel, message: string, meta?: LogMetadata): Promise<void>;
}

class ConsoleTransport implements LogTransport { /* ... */ }
class FileTransport implements LogTransport { /* ... */ }
class RemoteTransport implements LogTransport { /* ... */ }

class Logger {
  private transports: LogTransport[] = [];
  private queue: LogEntry[] = [];
  private rateLimiter: RateLimiter;
  private formatter: LogFormatter;

  // 200 linhas de código para "talvez precisemos"
}

const logError = (error: Error) => {
  Logger.getInstance().log('error', error.message);
};
```
Construindo para requisitos imaginários
</Bad>

**Quando adicionar complexidade:**
- Requisito atual exige
- Pontos de dor identificados através de uso
- Problemas de performance mensurados
- Múltiplos casos de uso emergiram

<Good>
```typescript
// Comece simples
const formatCurrency = (amount: number): string => {
  return `$${amount.toFixed(2)}`;
};

// Requisito evolui: suporte múltiplas moedas
const formatCurrency = (amount: number, currency: string): string => {
  const symbols = { USD: '$', EUR: '€', GBP: '£' };
  return `${symbols[currency]}${amount.toFixed(2)}`;
};

// Requisito evolui: suporte localização
const formatCurrency = (amount: number, locale: string): string => {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: locale === 'en-US' ? 'USD' : 'EUR',
  }).format(amount);
};
```
Complexidade adicionada apenas quando necessária
</Good>

#### Abstração Prematura

<Bad>
```typescript
// Um caso de uso, mas construindo framework genérico
abstract class BaseCRUDService<T> {
  abstract getAll(): Promise<T[]>;
  abstract getById(id: string): Promise<T>;
  abstract create(data: Partial<T>): Promise<T>;
  abstract update(id: string, data: Partial<T>): Promise<T>;
  abstract delete(id: string): Promise<void>;
}

class GenericRepository<T> { /* 300 linhas */ }
class QueryBuilder<T> { /* 200 linhas */ }
// ... construindo ORM inteiro para uma tabela
```
Abstração massiva para futuro incerto
</Bad>

<Good>
```typescript
// Funções simples para necessidades atuais
const getUsers = async (): Promise<User[]> => {
  return db.query('SELECT * FROM users');
};

const getUserById = async (id: string): Promise<User | null> => {
  return db.query('SELECT * FROM users WHERE id = $1', [id]);
};

// Quando padrão emerge entre múltiplas entidades, então abstraia
```
Abstraia apenas quando padrão comprovado em 3+ casos
</Good>

#### Otimização de Performance

<Good>
```typescript
// Atual: Abordagem simples
const filterActiveUsers = (users: User[]): User[] => {
  return users.filter(user => user.isActive);
};

// Benchmark mostra: 50ms para 1000 usuários (aceitável)
// ✓ Entregue, nenhuma otimização necessária

// Depois: Após profiling mostra que isto é gargalo
// Então otimize com lookup indexado ou caching
```
Otimize baseado em medição, não suposições
</Good>

<Bad>
```typescript
// Otimização prematura
const filterActiveUsers = (users: User[]): User[] => {
  // "Isto pode ser lento, então vamos fazer cache e indexar"
  const cache = new WeakMap();
  const indexed = buildBTreeIndex(users, 'isActive');
  // 100 linhas de código de otimização
  // Adiciona complexidade, mais difícil de manter
  // Nenhuma evidência de que era necessário
};
```
Solução complexa para problema não-medido
</Bad>

#### Na Prática

**Ao implementar:**

- Resolva o problema imediato
- Use abordagem direta
- Resista pensamento "e se"
- Delete código especulativo

**Ao otimizar:**

- Profile primeiro, otimize segundo
- Meça antes e depois
- Documente por que otimização necessária
- Mantenha versão simples nos testes

**Ao abstrair:**

- Espere 3+ casos similares (Rule of Three)
- Torne abstração tão simples quanto possível
- Prefira duplicação sobre abstração errada
- Refatore quando padrão claro

## Integração com Comandos

A skill Kaizen guia como você trabalha. Os comandos fornecem análise estruturada:

- **`/why`**: Análise de causa raiz (5 Porquês)
- **`/cause-and-effect`**: Análise multifatorial (Espinha de Peixe)
- **`/plan-do-check-act`**: Ciclos de melhoria iterativos
- **`/analyse-problem`**: Documentação abrangente (A3)
- **`/analyse`**: Seleção inteligente de método (Gemba/VSM/Muda)

Use comandos para resolução estruturada de problemas. Aplique skill para desenvolvimento dia-a-dia.

## Bandeiras Vermelhas

**Violando Melhoria Contínua:**

- "Vou refatorar depois" (nunca acontece)
- Deixar código pior que encontrou
- Big bang rewrites em vez de incremental

**Violando Poka-Yoke:**

- "Usuários devem apenas ter cuidado"
- Validação após uso em vez de antes
- Config opcional sem validação

**Violando Trabalho Padronizado:**

- "Prefiro fazer à minha maneira"
- Não verificar padrões existentes
- Ignorar convenções do projeto

**Violando Just-In-Time:**

- "Podemos precisar disso algum dia"
- Construindo frameworks antes de usá-los
- Otimizando sem medir

## Lembre-se

**Kaizen é sobre:**

- Pequenas melhorias continuamente
- Prevenir erros por design
- Seguir padrões comprovados
- Construir apenas o necessário

**Não é sobre:**

- Perfeição na primeira tentativa
- Projetos de refatoração massivos
- Abstrações criativas
- Otimização prematura

**Mentalidade:** Bom o suficiente hoje, melhor amanhã. Repita.