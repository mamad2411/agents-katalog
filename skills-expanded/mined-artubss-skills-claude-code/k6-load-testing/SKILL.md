---
name: k6-load-testing
description: "Habilidade abrangente de teste de carga k6 para API, browser e testes de escalabilidade. Escreva cenários de carga realistas, analise resultados e integre com CI/CD."
category: testing
risk: safe
source: community
date_added: "2026-03-13"
author: Kairo Official
tags: [k6, load-testing, performance, api-testing, ci-cd]
tools: [claude, cursor, gemini]
---

# Teste de Carga com k6

## Visão Geral

k6 é uma ferramenta moderna de teste de carga focada no desenvolvedor que ajuda você a escrever e executar testes de desempenho para APIs HTTP, endpoints WebSocket e cenários de browser. Esta habilidade fornece orientação abrangente sobre como escrever testes de carga realistas, configurar cenários de teste (smoke, load, stress, spike, soak), analisar resultados e integrar com pipelines CI/CD.

Use esta habilidade quando você precisar validar o desempenho do sistema, identificar gargalos, garantir conformidade com SLA ou detectar regressões de desempenho antes do deployment.

---

## Quando Usar Esta Habilidade

- Use quando precisar fazer teste de carga em APIs HTTP, endpoints WebSocket ou cenários de browser
- Use ao configurar testes de regressão de desempenho em CI/CD
- Use ao analisar o comportamento do sistema sob várias condições de carga
- Use ao comparar desempenho entre mudanças de código
- Use ao validar requisitos de SLA e orçamentos de desempenho

---

## Noções Básicas de k6

### Instalação

```bash
# macOS
brew install k6

# Windows
choco install k6

# Linux
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

### Início Rápido

```javascript
// simple-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
};

export default function () {
  const res = http.get('https://httpbin.test.k6.io/get');
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  sleep(1);
}
```

Execute com: `k6 run simple-test.js`

---

## Configuração de Teste

### Opções Comuns

```javascript
export const options = {
  // Usuários Virtuais (usuários simultâneos)
  vus: 100,
  
  // Duração do teste
  duration: '5m',
  
  // Ou use stages para ramp-up/ramp-down
  stages: [
    { duration: '30s', target: 20 },   // Aumento gradual
    { duration: '1m', target: 100 },  // Mantenha em 100
    { duration: '30s', target: 0 },    // Diminuição gradual
  ],
  
  // Thresholds (SLA)
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% das requisições < 500ms
    http_req_failed: ['rate<0.01'],     // Taxa de erro < 1%
  },
  
  // Zonas de carga (teste distribuído)
  ext: {
    loadimpact: {
      name: 'Meu Teste de Carga',
      distribution: {
        'amazon:us:ashburn': { weight: 50 },
        'amazon:eu:Dublin': { weight: 50 },
      },
    },
  },
};
```

### Tipos de Teste

| Tipo | Caso de Uso | Configuração |
|------|----------|---------------|
| Smoke Test | Verificar funcionalidade básica | Poucos VUs (1-5), duração curta |
| Load Test | Carga esperada normal | VUs alvo baseado em tráfego |
| Stress Test | Encontrar ponto de ruptura | Aumento além da capacidade |
| Spike Test | Picos súbitos de tráfego | Aumento/diminuição rápida |
| Soak Test | Estabilidade de longo prazo | Duração estendida |

---

## Teste HTTP

### Requisições Básicas

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export default function () {
  // Requisição GET
  const getRes = http.get('https://api.example.com/users');
  
  check(getRes, {
    'GET succeeded': (r) => r.status === 200,
    'has users': (r) => r.json('data.length') > 0,
  });

  // Requisição POST com corpo JSON
  const postRes = http.post('https://api.example.com/users', 
    JSON.stringify({ name: 'Test User', email: 'test@example.com' }),
    {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + __ENV.API_TOKEN,
      },
    }
  );
  
  check(postRes, {
    'POST succeeded': (r) => r.status === 201,
    'user created': (r) => r.json('id') !== undefined,
  });

  sleep(1);
}
```

### Encadeamento de Requisições

```javascript
import http from 'k6/http';
import { check } from 'k6';

export default function () {
  // Login e extrair token
  const loginRes = http.post('https://api.example.com/login', 
    JSON.stringify({ email: 'test@example.com', password: 'password123' })
  );
  
  const token = loginRes.json('access_token');
  
  // Usar token em requisições subsequentes
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
  
  const profileRes = http.get('https://api.example.com/profile', {
    headers: headers,
  });
  
  check(profileRes, {
    'profile loaded': (r) => r.status === 200,
  });
}
```

### Teste Parametrizado

```javascript
import http from 'k6/http';
import { check } from 'k6';

const usernames = ['user1', 'user2', 'user3', 'user4', 'user5'];

export default function () {
  // Use array compartilhado com índice específico do VU
  const username = usernames[__VU % usernames.length];
  
  const res = http.get(`https://api.example.com/users/${username}`);
  
  check(res, {
    'user found': (r) => r.status === 200,
  });
}
```

---

## Teste de Browser (k6 Browser)

```javascript
import { browser } from 'k6/browser';

export const options = {
  scenarios: {
    browser_test: {
      executor: 'constant-vus',
      vus: 5,
      duration: '30s',
      browser: {
        type: 'chromium',
      },
    },
  },
};

export default async function () {
  const page = await browser.newPage();
  
  try {
    await page.goto('https://example.com');
    
    const title = await page.title();
    console.log(`Page title: ${title}`);
    
    // Clicar e interagir
    await page.click('button[data-testid="submit"]');
    
    // Aguardar resposta
    await page.waitForSelector('.success-message');
    
  } finally {
    await page.close();
  }
}
```

Instale o suporte a browser: `k6 install chromium`

---

## Teste WebSocket

```javascript
import ws from 'k6/ws';
import { check } from 'k6';

export default function () {
  const url = 'wss://echo.websocket.org';
  
  ws.connect(url, {}, function (socket) {
    socket.on('open', () => {
      console.log('WebSocket connected');
      socket.send('Hello WebSocket');
    });
    
    socket.on('message', (data) => {
      console.log(`Received: ${data}`);
      check(data, {
        'echo received': (d) => d.includes('Hello'),
      });
    });
    
    socket.on('close', () => {
      console.log('WebSocket closed');
    });
    
    // Enviar mensagens periódicas
    socket.setInterval(function () {
      socket.send('ping');
    }, 1000);
    
    // Fechar após 5 segundos
    socket.setTimeout(function () {
      socket.close();
    }, 5000);
  });
}
```

---

## Manipulação de Dados

### Fonte de Dados CSV

```javascript
import http from 'k6/http';
import { check } from 'k6';
import { SharedArray } from 'k6/data';

// Opção 1: Carregar uma vez, compartilhar entre VUs
const users = new SharedArray('users', function () {
  return open('./users.csv').split('\n').slice(1).map(line => {
    const [email, password] = line.split(',');
    return { email, password };
  });
});

export default function () {
  const user = users[__VU % users.length];
  
  const res = http.post('https://api.example.com/login',
    JSON.stringify({ email: user.email, password: user.password })
  );
  
  check(res, { 'login successful': (r) => r.status === 200 });
}
```

### Fonte de Dados JSON

```javascript
import http from 'k6/http';
import { check } from 'k6';
import { SharedArray } from 'k6/data';

const products = new SharedArray('products', function () {
  return JSON.parse(open('./products.json'));
});

export default function () {
  const product = products[Math.floor(Math.random() * products.length)];
  
  const res = http.get(`https://api.example.com/products/${product.id}`);
  
  check(res, { 'product found': (r) => r.status === 200 });
}
```

---

## Thresholds e SLA

### Thresholds Básicos

```javascript
export const options = {
  vus: 50,
  duration: '2m',
  
  thresholds: {
    // Thresholds de tempo de resposta
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    
    // Threshold de taxa de erro
    http_req_failed: ['rate<0.01'],
    
    // Threshold de throughput
    http_reqs: ['rate>100'],
  },
};
```

### Thresholds Avançados

```javascript
export const options = {
  thresholds: {
    // Múltiplos thresholds na mesma métrica
    http_req_duration: [
      'p(90)<300',   // 90º percentil < 300ms
      'p(95)<500',  // 95º percentil < 500ms
      'p(99)<1000', // 99º percentil < 1s
      'avg<200',    // média < 200ms
    ],
    
    // Métricas customizadas
    my_custom_metric: ['avg<100'],
    
    // Abortar em falha de threshold
    'http_req_duration{method:GET}': ['p(95)<300'],
  },
};
```

---

## Métricas Customizadas

### Counters

```javascript
import http from 'k6/http';
import { Counter, Trend, Rate, Gauge } from 'k6/metrics';

// Definir métricas customizadas
const myCounter = new Counter('api_calls_total');
const responseTime = new Trend('response_time');
const errorRate = new Rate('error_rate');
const activeUsers = new Gauge('active_users');

export default function () {
  const res = http.get('https://api.example.com/data');
  
  // Incrementar counter
  myCounter.add(1);
  
  // Adicionar a trend (para percentis)
  responseTime.add(res.timings.duration);
  
  // Rastrear taxa de erro
  errorRate.add(res.status !== 200);
  
  // Definir valor de gauge
  activeUsers.add(__VU);
  
  // Métricas com tags
  const taggedRes = http.get('https://api.example.com/users', {
    tags: { endpoint: 'users', env: 'prod' },
  });
}
```

---

## Integração com CI/CD

### GitHub Actions

```yaml
# .github/workflows/load-test.yml
name: Load Tests

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Diariamente às 2 AM

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup k6
        uses: grafana/k6-action@v0.2.0
        
      - name: Run load test
        env:
          API_TOKEN: ${{ secrets.API_TOKEN }}
        run: k6 run --out json=results.json load-test.js
        
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: k6-results
          path: results.json
          
      - name: Check thresholds
        if: failure()
        run: |
          echo "Load test failed thresholds!"
          exit 1
```

### GitLab CI

```yaml
# .gitlab-ci.yml
load_test:
  image: grafana/k6:latest
  script:
    - k6 run load-test.js
  artifacts:
    when: always
    paths:
      - results.json
    reports:
      junit: results.xml
```

---

## Análise de Resultados

### Relatórios Integrados

```bash
# Resumo em texto
k6 run load-test.js

# Saída JSON para parsing
k6 run --out json=results.json load-test.js

# InfluxDB + Grafana
k6 run --out influxdb=http://localhost:8086/k6 load-test.js

# Prometheus remote write
k6 run --out prometheus=localhost:9090/k6 load-test.js

# Resultados em cloud
k6 run --out cloud load-test.js
```

### Interpretando Resultados

| Métrica | Descrição | Bom | Aviso | Ruim |
|--------|----------|------|---------|-----|
| http_req_duration (p95) | Tempo de resposta 95% | < 300ms | 300-500ms | > 500ms |
| http_req_failed | Taxa de erro | < 0,1% | 0,1-1% | > 1% |
| http_reqs | Requisições/seg | Atendendo alvo | Próximo do limite | No limite |
| vus | Usuários virtuais | Estável | Aumento gradual | Pico inesperado |

---

## Exemplos

### Exemplo 1: Teste de Carga Básico de API

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 50,
  duration: '2m',
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  sleep(1);
}
```

### Exemplo 2: Teste com Autenticação e Parametrização de Dados

```javascript
import http from 'k6/http';
import { check } from 'k6';
import { SharedArray } from 'k6/data';

const users = new SharedArray('users', function () {
  return JSON.parse(open('./users.json'));
});

export default function () {
  const user = users[__VU % users.length];
  
  const loginRes = http.post('https://api.example.com/login',
    JSON.stringify({ email: user.email, password: user.password })
  );
  
  const token = loginRes.json('access_token');
  
  const headers = { 'Authorization': `Bearer ${token}` };
  const res = http.get('https://api.example.com/profile', { headers });
  
  check(res, { 'profile loaded': (r) => r.status === 200 });
}
```

---

## Melhores Práticas

- **Comece com smoke test**: Verifique se o teste funciona com 1-5 VUs antes de escalar
- **Use dados realistas**: Parametrize com dados reais de usuários e comportamentos
- **Defina thresholds significativos**: Corresponda ao seu SLA e requisitos de negócio
- **Aqueça sistemas**: Inclua tempo de ramp-up nos stages
- **Monitore dependências externas**: Rastreie não apenas suas APIs, mas serviços downstream
- **Use tags**: Marque requisições para análise granular (`tags: { endpoint: 'users' }`)
- **Mantenha testes focados**: Um arquivo de teste por cenário para clareza

---

## Armadilhas Comuns

- **Problema:** Testes passam localmente, mas falham em CI
  **Solução:** Garanta que o ambiente de CI tenha recursos similares e condições de rede

- **Problema:** Resultados inconsistentes entre execuções
  **Solução:** Verifique dependências externas, dados aleatórios ou poluição de dados de teste

- **Problema:** k6 fica sem memória
  **Solução:** Use `SharedArray` para dados grandes, reduza VUs ou use a flag `--max-memory`

- **Problema:** Thresholds muito rigorosos
  **Solução:** Comece com thresholds relaxados, aperte baseado em dados históricos

---

## Habilidades Relacionadas

- `@performance-engineer` - Para otimização de desempenho mais ampla
- `@api-testing-observability-api-mock` - Para mock de API durante testes
- `@application-performance-performance-optimization` - Para otimização de desempenho

---

## Recursos Adicionais

- [Documentação k6](https://k6.io/docs/)
- [Exemplos k6](https://github.com/grafana/k6/tree/master/examples)
- [Guias de Teste de Carga k6](https://k6.io/guides/)
- [k6 Cloud](https://k6.io/cloud/)