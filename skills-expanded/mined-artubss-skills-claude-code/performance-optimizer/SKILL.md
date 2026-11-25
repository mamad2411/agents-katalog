---
name: performance-optimizer
description: "Identifica e corrige gargalos de desempenho em código, bancos de dados e APIs. Mede antes e depois para comprovar as melhorias."
category: development
risk: safe
source: community
date_added: "2026-03-05"
---

# Performance Optimizer

Encontre e corrija gargalos de desempenho. Meça, otimize, verifique. Deixe rápido.

## Quando Usar Esta Skill

- App está lento ou travando
- Usuário reclama de desempenho
- Tempo de carregamento de página é alto
- Respostas de API são lentas
- Queries de banco de dados demoram muito
- Usuário menciona "lento", "travamento", "desempenho" ou "otimizar"

## O Processo de Otimização

### 1. Meça Primeiro

Nunca otimize sem medir:

```javascript
// Meça tempo de execução
console.time('operation');
await slowOperation();
console.timeEnd('operation'); // operation: 2341ms
```

**O que medir:**
- Tempo de carregamento de página
- Tempo de resposta de API
- Tempo de query do banco de dados
- Tempo de execução de função
- Uso de memória
- Requisições de rede

### 2. Encontre o Gargalo

Use ferramentas de profiling para encontrar as partes lentas:

**Navegador:**
```
DevTools → Performance tab → Record → Stop
Procure por long tasks (barras vermelhas)
```

**Node.js:**
```bash
node --prof app.js
node --prof-process isolate-*.log > profile.txt
```

**Banco de Dados:**
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

### 3. Otimize

Corrija a coisa mais lenta primeiro (maior impacto).

## Otimizações Comuns

### Queries de Banco de Dados

**Problema: N+1 Queries**
```javascript
// Ruim: N+1 queries
const users = await db.users.find();
for (const user of users) {
  user.posts = await db.posts.find({ userId: user.id }); // N queries
}

// Bom: Query única com JOIN
const users = await db.users.find()
  .populate('posts'); // 1 query
```

**Problema: Índice Ausente**
```sql
-- Verifique query lenta
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
-- Mostra: Seq Scan (ruim)

-- Adicione índice
CREATE INDEX idx_users_email ON users(email);

-- Verifique novamente
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
-- Mostra: Index Scan (bom)
```

**Problema: SELECT ***
```javascript
// Ruim: Obtém todas as colunas
const users = await db.query('SELECT * FROM users');

// Bom: Apenas colunas necessárias
const users = await db.query('SELECT id, name, email FROM users');
```

**Problema: Sem Paginação**
```javascript
// Ruim: Retorna todos os registros
const users = await db.users.find();

// Bom: Paginado
const users = await db.users.find()
  .limit(20)
  .skip((page - 1) * 20);
```

### Performance de API

**Problema: Sem Cache**
```javascript
// Ruim: Acessa banco de dados toda vez
app.get('/api/stats', async (req, res) => {
  const stats = await db.stats.calculate(); // Lento
  res.json(stats);
});

// Bom: Cache por 5 minutos
const cache = new Map();
app.get('/api/stats', async (req, res) => {
  const cached = cache.get('stats');
  if (cached && Date.now() - cached.time < 300000) {
    return res.json(cached.data);
  }
  
  const stats = await db.stats.calculate();
  cache.set('stats', { data: stats, time: Date.now() });
  res.json(stats);
});
```

**Problema: Operações Sequenciais**
```javascript
// Ruim: Sequencial (lento)
const user = await getUser(id);
const posts = await getPosts(id);
const comments = await getComments(id);
// Total: 300ms + 200ms + 150ms = 650ms

// Bom: Paralelo (rápido)
const [user, posts, comments] = await Promise.all([
  getUser(id),
  getPosts(id),
  getComments(id)
]);
// Total: max(300ms, 200ms, 150ms) = 300ms
```

**Problema: Payloads Grandes**
```javascript
// Ruim: Retorna tudo
res.json(users); // 5MB response

// Bom: Apenas campos necessários
res.json(users.map(u => ({
  id: u.id,
  name: u.name,
  email: u.email
}))); // 500KB response
```

### Performance de Frontend

**Problema: Re-renders Desnecessários**
```javascript
// Ruim: Re-renderiza em toda atualização do pai
function UserList({ users }) {
  return users.map(user => <UserCard user={user} />);
}

// Bom: Memoizado
const UserCard = React.memo(({ user }) => {
  return <div>{user.name}</div>;
});
```

**Problema: Bundle Grande**
```javascript
// Ruim: Importa biblioteca inteira
import _ from 'lodash'; // 70KB

// Bom: Importa apenas o necessário
import debounce from 'lodash/debounce'; // 2KB
```

**Problema: Sem Code Splitting**
```javascript
// Ruim: Tudo em um bundle
import HeavyComponent from './HeavyComponent';

// Bom: Carregamento preguiçoso
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));
```

**Problema: Imagens Não Otimizadas**
```html
<!-- Ruim: Imagem grande -->
<img src="photo.jpg" /> <!-- 5MB -->

<!-- Bom: Otimizada e responsiva -->
<img 
  src="photo-small.webp" 
  srcset="photo-small.webp 400w, photo-large.webp 800w"
  loading="lazy"
  width="400"
  height="300"
/> <!-- 50KB -->
```

### Otimização de Algoritmo

**Problema: Algoritmo Ineficiente**
```javascript
// Ruim: O(n²) - loops aninhados
function findDuplicates(arr) {
  const duplicates = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) duplicates.push(arr[i]);
    }
  }
  return duplicates;
}

// Bom: O(n) - passagem única com Set
function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();
  for (const item of arr) {
    if (seen.has(item)) duplicates.add(item);
    seen.add(item);
  }
  return Array.from(duplicates);
}
```

**Problema: Cálculos Repetidos**
```javascript
// Ruim: Calcula toda vez
function getTotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
// Chamado 100 vezes em render

// Bom: Memoizado
const getTotal = useMemo(() => {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}, [items]);
```

### Otimização de Memória

**Problema: Memory Leak**
```javascript
// Ruim: Event listener não removido
useEffect(() => {
  window.addEventListener('scroll', handleScroll);
  // Memory leak!
}, []);

// Bom: Limpeza
useEffect(() => {
  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
}, []);
```

**Problema: Dados Grandes em Memória**
```javascript
// Ruim: Carrega arquivo inteiro em memória
const data = fs.readFileSync('huge-file.txt'); // 1GB

// Bom: Faz streaming
const stream = fs.createReadStream('huge-file.txt');
stream.on('data', chunk => process(chunk));
```

## Medindo Impacto

Sempre meça antes e depois:

```javascript
// Antes da otimização
console.time('query');
const users = await db.users.find();
console.timeEnd('query');
// query: 2341ms

// Depois da otimização (índice adicionado)
console.time('query');
const users = await db.users.find();
console.timeEnd('query');
// query: 23ms

// Melhoria: 100x mais rápido!
```

## Performance Budgets

Estabeleça metas:

```
Carregamento de Página: < 2 segundos
Resposta de API: < 200ms
Query de Banco de Dados: < 50ms
Tamanho do Bundle: < 200KB
Time to Interactive: < 3 segundos
```

## Ferramentas

**Navegador:**
- Chrome DevTools Performance tab
- Lighthouse (audit)
- Network tab (waterfall)

**Node.js:**
- `node --prof` (profiling)
- `clinic` (diagnostics)
- `autocannon` (load testing)

**Banco de Dados:**
- `EXPLAIN ANALYZE` (query plans)
- Slow query log
- Database profiler

**Monitoramento:**
- New Relic
- Datadog
- Sentry Performance

## Quick Wins

Otimizações fáceis com grande impacto:

1. **Adicione índices de banco de dados** em colunas consultadas frequentemente
2. **Habilite compressão gzip** no servidor
3. **Adicione cache** para operações caras
4. **Lazy load** imagens e componentes pesados
5. **Use CDN** para assets estáticos
6. **Minifique e comprima** JavaScript/CSS
7. **Remova dependências não usadas**
8. **Use paginação** em vez de carregar todos os dados
9. **Otimize imagens** (WebP, dimensionamento apropriado)
10. **Habilite HTTP/2** no servidor

## Checklist de Otimização

- [ ] Mediu desempenho atual
- [ ] Identificou gargalo
- [ ] Aplicou otimização
- [ ] Mediu melhoria
- [ ] Verificou se funcionalidade ainda funciona
- [ ] Sem novos bugs introduzidos
- [ ] Mudança documentada

## Quando NÃO Otimizar

- Otimização prematura (otimize quando estiver realmente lento)
- Micro-otimizações (economizar 1ms quando página demora 5 segundos)
- Código legível é mais importante que ganhos minúsculos de velocidade
- Se já estiver rápido o suficiente

## Princípios-Chave

- Meça antes de otimizar
- Corrija o maior gargalo primeiro
- Meça depois para comprovar melhoria
- Não sacrifique legibilidade por ganhos minúsculos
- Faça profile em ambiente parecido com produção
- Considere a regra 80/20 (20% do código causa 80% da lentidão)

## Skills Relacionadas

- `@database-design` - Otimização de queries
- `@codebase-audit-pre-push` - Revisão de código
- `@bug-hunter` - Debugging