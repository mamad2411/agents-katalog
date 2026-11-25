---
name: req-fault-tolerance
version: 1.0.0
description: >
  Analisa requisitos de software e injeta resiliência em código — do recebimento
  da tarefa (input) até a geração do artefato (build). Focado em mapear
  criticidade, exceções e fallbacks em cada etapa da execução.
triggers:
  - "analisar criticidade"
  - "tolerância a falhas"
  - "casos de exceção do requisito"
  - "resiliência no build"
  - "edge cases de geração"
  - "o que fazer se falhar"
---

# REQ FAULT TOLERANCE — Resiliência de código do requisito ao build

> **Propósito**: Transformar requisitos brutos em código defensivo, garantindo que
> falhas em qualquer etapa do pipeline (input, processamento, geração de artefato)
> resultem em degradação elegante e nunca em corrupção silenciosa.

## Filosofia Central

1. **Fail-Fast no Input, Graceful no Output** — Rejeite dados inválidos imediatamente na fronteira do sistema. Na prática: valide schemas antes de qualquer lógica de negócio; na saída, retorne o melhor estado possível (cache/fallback) em vez de crashar.
2. **Criticidade Dita Arquitetura** — Nem todo erro precisa de retry, nem todo retry precisa de Circuit Breaker. Na prática: classifique o requisito (P0 a P2) no passo 1 e use isso para limitar o custo computacional do tratamento de erro.
3. **Build Atômico** — Um processo de geração de artefato nunca deve deixar lixo para trás se falhar na metade. Na prática: escreva em diretório temporário e faça rename atômico apenas após validação final.
4. **Exceção é Fluxo, não Acidente** — `try/catch` não é um adendo, é o desenho do caminho alternativo. Na prática: erros esperados (ex: API fora) devem retornar um tipo de sucesso diferente (ex: `Result.Err`), não lançar exceção não-tratada.

## Quando Ativar

### ✅ Ativar para:
- Receber um requisito que implica geração de arquivo, chamada de API ou transformação de dados.
- Projetar a pipeline de execução de uma task complexa (ex: gerar relatório PDF a partir de 3 fontes).
- Refatorar código que falha de forma abrupta ou deixa o sistema em estado inconsistente.

### ❌ NÃO ativar para:
- Correção de bug de lógica de negócio pura (ex: cálculo de imposto errado) → corrija a matemática diretamente.
- Configuração de infraestrutura de CI/CD → use `ci-cd-setup`.
- Tratamento de erros genérico de UI (toast de erro) → use `frontend-ux-patterns`.

## Escopo e Limites

**Esta skill cobre:**
- Mapeamento de vetores de falha a partir da leitura de um requisito.
- Escrita de código defensivo na camada de aplicação/serviço.
- Garantia de atomicidade na geração de artefatos (build).

**Esta skill delega:**
- Padrões de resiliência de microsserviços (Saga, Outbox) → `architect-decisions`.
- Estrutura de logs e métricas de erro → `observability-patterns`.

## Protocolo de Execução

1. **Classificar Criticidade** — Leia o requisito e atribua um nível (P0: bloqueia usuário, P1: degrada experiência, P2: visual/cosmético). *Critério de conclusão: Nível anotado no topo do código.*
2. **Mapear Vetores de Falha** — Liste os 3 pontos mais prováveis de quebra: Entrada (input malformado), Processamento (dependência externa/timeout), Saída (falha de I/O no build). *Critério: Lista numerada escrita.*
3. **Definir Contratos de Falha** — Para cada vetor, defina o que o sistema retorna (ex: "Se API falhar, retornar últimos dados em cache com flag `stale: true`"). *Critério: Tipo de retorno definido.*
4. **Codificar Defesas** — Implemente validação de entrada estrita, limites de timeout e blocos de recuperação. *Critério: Código cobre os 3 vetores.*
5. **Isolar Pipeline de Build** — Se o requisito envolver criar um artefato, separe a lógica de "construir" da lógica de "salvar", garantindo write-atômico. *Critério: Ausência de writes parciais em disco.*
6. **Simular Falhas** — Forneça um exemplo de como testar cada ponto de falha (ex: "Para testar, injete um mock que lance `TimeoutError`"). *Critério: Comandos ou snippets de teste fornecidos.*

## Padrões Específicos

### 1. Validação de Fronteira (Input Gate)

**Regra**: O corpo da função principal nunca deve confiar que os tipos do TypeScript/Python garantem a regra de negócio. Valide explicitamente.

```typescript
// ✅ PASS — Rejeição imediata com contexto rico
function processReport(req: ReportRequest): Report {
  if (!req.dateRange || req.dateRange.start > req.dateRange.end) {
    throw new ValidationError('dateRange.invalid', { start: req.dateRange?.start, end: req.dateRange?.end });
  }
  // ... lógica segura
}

// ❌ FAIL — Confia no tipo, quebra com undefined inesperado
function processReport(req: ReportRequest): Report {
  const days = req.dateRange.end.getTime() - req.dateRange.start.getTime(); // Throw genérico se undefined
}
```

**Por que importa**: Erros de validação precoces evitam rastreamento de stack traces longos e permitem retornar HTTP 400 exato para o cliente.

### 2. Degradação Graceful em Dependências

**Regra**: Chamadas externas devem ter timeout rígido e fallback determinístico baseado na criticidade.

```typescript
// ✅ PASS — Timeout curto + Fallback explícito baseado em criticidade
async function fetchContextData(criticality: 'P0' | 'P1' | 'P2'): Promise<Context> {
  try {
    return await fetchWithTimeout('https://api.context.com/data', { timeout: 2000 });
  } catch (error) {
    if (criticality === 'P0') throw new CriticalDependencyError('Context API unavailable', { cause: error });
    log.warn('Using fallback context due to API failure');
    return FALLBACK_CONTEXT; // Objeto imutável em memória
  }
}

// ❌ FAIL — Sem timeout, sem fallback, lança erro não tratado
async function fetchContextData(): Promise<Context> {
  const res = await fetch('https://api.context.com/data'); // Pode travar a thread infinitamente
  return res.json();
}
```

**Por que importa**: Sem timeout, uma API travada congela seu processo de build. Sem fallback, um erro P2 derruba um usuário P0.

### 3. Build Atômico (Geração de Artefato)

**Regra**: Nunca escreva diretamente no caminho final do artefato. Escreva em `.tmp` e use rename/move síncrono do SO.

```python
import os
import shutil

# ✅ PASS — Escrita temporária + rename atômico
def generate_artifact(data: dict, final_path: str):
    temp_path = f"{final_path}.tmp.{os.getpid()}"
    try:
        with open(temp_path, 'w') as f:
            f.write(transform(data))
        
        # Validação pós-build (ex: verificar se arquivo não está corrompido/vazio)
        if os.path.getsize(temp_path) == 0:
            raise BuildError("Arquivo gerado está vazio.")
            
        os.replace(temp_path, final_path) # Operação atômica em sistemas POSIX/NTFS
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path) # Limpeza garantida
        raise BuildError("Falha na geração do artefato.", { cause: e })

# ❌ FAIL — Escrita direta, deixa arquivo corrompido pela metade se falhar
def generate_artifact(data: dict, final_path: str):
    with open(final_path, 'w') as f:
        f.write("Header...")
        f.write(transform(data)) # Se falhar aqui, o arquivo final está quebrado
```

**Por que importa**: Se o processo morrer na metade da escrita, o arquivo final existirá, mas estará corrompido, quebrando execuções subsequentes ou entregando lixo ao usuário.

### 4. Tratamento de Erro como Tipo (Result Pattern)

**Regra**: Para fluxos onde o erro é uma possibilidade esperada (não excepcional), retorne um objeto de resultado em vez de lançar exceção.

```typescript
// ✅ PASS — Erro tipado como parte do fluxo
type Result<T> = { ok: true; value: T } | { ok: false; error: ValidationError };

function parseConfig(raw: string): Result<Config> {
  const parsed = JSON.parse(raw); // Apenas lança se JSON for inválido (erro de sintaxe real)
  if (!parsed.apiUrl) {
    return { ok: false, error: new ValidationError('Missing apiUrl') };
  }
  return { ok: true, value: parsed as Config };
}

// ❌ FAIL — Mistura erro de sistema com erro de validação
function parseConfig(raw: string): Config {
  const parsed = JSON.parse(raw);
  if (!parsed.apiUrl) throw new Error("Missing apiUrl"); // Obriga o caller a usar try/catch para regra de negócio
}
```

**Por que importa**: Força o consumidor da função a lidar com o caso de falha no nível de tipo, evitando `try/catch` descontrolados espalhados pelo código.

## Anti-Padrões Críticos

| Anti-padrão | Consequência | Alternativa Correta |
| :--- | :--- | :--- |
| `catch (e) { console.log(e) }` e continua | Dados corrompidos silenciosamente processados | Abortar a etapa e acionar fallback ou rejeitar a request |
| Retry infinito ou sem Backoff | Sobrecarga no sistema dependente, esgotamento de conexões | Retry com limite (ex: 3x) e Exponential Backoff + Jitter |
| Deixar arquivo `.tmp` ao falhar | Leak de disco, confusão de estado em builds subsequentes | Bloco `finally` ou cleanup estruturado para remover temp |
| Usar exceções para controle de fluxo | Stack traces pesados, dificulta depuração real | Usar tipagem (`Result`, `Option`) para erros de negócio |

## Critérios de Qualidade

Antes de entregar o código gerado, confirme:

- [ ] Criticidade (P0/P1/P2) declarada no topo do arquivo ou comentário da função.
- [ ] Os 3 vetores de falha (Input, Process, Output) foram explicitamente listados antes do código.
- [ ] Tempo de timeout definido para qualquer operação I/O ou de rede.
- [ ] Geração de arquivo usa método atômico (tmp + rename).
- [ ] Nenhum bloco `catch` está vazio ou faz apenas `console.log`.
- [ ] Fornecido exemplo de como simular a falha (Mock/Stub) para validar a resiliência.
- [ ] Tipos de retorno de erro são específicos (ex: `BuildError`, `ValidationError`) e não genéricos (`Error`).

## Referências Cruzadas

| Precisa de... | Use a skill... |
| :--- | :--- |
| Criar o arquivo final após o processamento resiliente | `docx`, `xlsx`, `pptx`, `pdf` (conforme o formato) |
| Desenhar arquitetura de microsserviço com tolerância total | `architect-decisions` |
| Emitir logs estruturados das falhas capturadas | `observability-patterns` |
| Tratar erros específicos de UI no frontend | `frontend-ux-patterns` |