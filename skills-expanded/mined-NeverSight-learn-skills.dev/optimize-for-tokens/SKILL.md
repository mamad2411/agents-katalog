---
name: optimize-for-tokens
description: >
  Analisa e refatora código para reduzir consumo de tokens em contextos de IA, dividindo arquivos grandes em módulos coesos e eliminando confusão de contexto. Use esta skill SEMPRE que o usuário mencionar: arquivos grandes demais, contexto confuso, token limit, refatorar para IA, dividir componentes, separar lógica de UI, extrair types, otimizar contexto para LLM, "arquivo com mais de 300 linhas", ou qualquer pedido de organização de codebase visando eficiência com IA. Acione também quando o usuário pedir para "limpar o código", "modularizar", "separar responsabilidades", ou simplesmente perguntar "como posso deixar meu código mais fácil para a IA entender".
---

# Optimize for Tokens

Skill para analisar e refatorar codebases com foco em **reduzir consumo de tokens** e **eliminar confusão de contexto** em sessões com LLMs.

---

## Fluxo de execução

### 1. Análise Inicial (sempre primeiro)

Antes de qualquer ação, execute a análise completa:

```bash
# Contar linhas de todos os arquivos relevantes
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) \
  ! -path "*/node_modules/*" ! -path "*/.next/*" ! -path "*/dist/*" \
  | xargs wc -l 2>/dev/null | sort -rn | head -30
```

Classifique cada arquivo:
- 🔴 **Crítico**: > 500 linhas — divisão obrigatória
- 🟡 **Atenção**: 300–500 linhas — divisão recomendada
- 🟢 **OK**: < 300 linhas — sem ação necessária

Mostre o resumo antes de qualquer refatoração. Sempre peça confirmação ao usuário antes de modificar arquivos.

---

### 2. Divisão de Arquivos > 300 Linhas

**Regra principal:** Nenhum arquivo enviado ao contexto de uma IA deve ter mais de 300 linhas.

**Identificar domínios no arquivo:**

```
ComponenteGrande.tsx (600 linhas)
├── Tipos e interfaces       → types/ComponenteGrande.types.ts
├── Hooks e estado           → hooks/useComponenteGrande.ts
├── Lógica de negócio        → utils/componenteGrandeHelpers.ts
│   └── Funções puras        → utils/componenteGrandeUtils.ts
├── Subcomponentes internos  → components/ComponenteGrandeParts.tsx
└── Componente principal     → ComponenteGrande.tsx  (~80 linhas)
```

**Estratégia de corte:**
1. Tipos e interfaces primeiro (zero side effects)
2. Funções puras e helpers (fácil de isolar)
3. Hooks customizados (estado + efeitos)
4. Subcomponentes (JSX reutilizável)
5. Componente raiz por último (apenas orquestração)

---

### 3. Isolamento: UI × Hooks × Lógica de Negócio

**Estrutura alvo para projetos React/Next:**

```
src/
├── components/          ← Apenas JSX + estilos (sem lógica complexa)
│   └── Button/
│       ├── Button.tsx           (< 80 linhas — só renderização)
│       └── Button.types.ts
├── hooks/               ← Estado, efeitos, subscriptions
│   ├── useAuth.ts
│   └── useCart.ts
├── services/            ← Chamadas de API, side effects externos
│   └── authService.ts
├── utils/               ← Funções puras, transformações, validações
│   └── formatters.ts
└── types/               ← Tipos globais e compartilhados
    └── index.ts
```

**Regras de isolamento:**

| Camada | Pode importar | Não pode importar |
|--------|--------------|-------------------|
| `components/` | `hooks/`, `types/`, `utils/` | `services/` diretamente |
| `hooks/` | `services/`, `utils/`, `types/` | `components/` |
| `services/` | `types/`, `utils/` | `hooks/`, `components/` |
| `utils/` | `types/` | qualquer outra camada |
| `types/` | nada | tudo |

---

### 4. Extração de Tipos para Arquivos Dedicados

**Quando extrair:**
- Interface ou type usado em mais de 1 arquivo → arquivo `types/` dedicado
- Enums compartilhados → `types/enums.ts`
- Tipos de resposta de API → `types/api.ts`
- Props de componentes → colocado junto ao componente (`Button.types.ts`)

**Padrão de nomenclatura:**
```
types/
├── index.ts          ← Re-exporta tudo (barrel)
├── api.ts            ← Tipos de request/response
├── enums.ts          ← Enums da aplicação
├── models.ts         ← Entidades de domínio
└── [Componente].types.ts  ← Props e tipos locais
```

**Template do barrel (`types/index.ts`):**
```typescript
export * from './api';
export * from './enums';
export * from './models';
```

---

### 5. Análise de Economia de Tokens em Tempo Real

Após cada refatoração, calcule e exiba o relatório:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  💰 RELATÓRIO DE ECONOMIA DE TOKENS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ANTES DA REFATORAÇÃO
  ─────────────────────────────────────
  Arquivo único:    1.240 linhas
  Tokens estimados: ~18.600 tokens
  Custo contextual: alto (arquivo inteiro sempre carregado)

  DEPOIS DA REFATORAÇÃO
  ─────────────────────────────────────
  Módulos criados:  6 arquivos
  ┌─────────────────────────────┬───────┐
  │ Arquivo                     │ Linhas│
  ├─────────────────────────────┼───────│
  │ Component.tsx               │   78  │
  │ hooks/useComponent.ts       │   95  │
  │ types/Component.types.ts    │   42  │
  │ utils/componentHelpers.ts   │  110  │
  │ services/componentService.ts│   88  │
  │ components/ComponentParts   │   95  │
  └─────────────────────────────┴───────┘

  IMPACTO POR TAREFA TÍPICA
  ─────────────────────────────────────
  Corrigir bug no hook:
    Antes:  ~18.600 tokens (arquivo inteiro)
    Depois: ~1.425 tokens (só o hook)
    Economia: 92% (~17.175 tokens)

  Ajustar UI/estilo:
    Antes:  ~18.600 tokens
    Depois: ~1.170 tokens (componente + types)
    Economia: 94% (~17.430 tokens)

  Adicionar endpoint:
    Antes:  ~18.600 tokens
    Depois: ~1.320 tokens (service + types)
    Economia: 93% (~17.280 tokens)

  ECONOMIA TOTAL ESTIMADA (sessão típica)
  ─────────────────────────────────────
  ✅ 85-94% menos tokens por operação
  ✅ Contexto focado = menos alucinações
  ✅ Edições mais rápidas e precisas
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Fórmula de estimativa:**
- 1 linha de código TypeScript/TSX ≈ 15 tokens (média com imports, tipos, JSX)
- Tokens economizados = (linhas do arquivo original × 15) − (linhas do módulo relevante × 15)
- % economia = tokens economizados / tokens originais × 100

---

## Guia de Decisão Rápida

```
Arquivo recebido
      │
      ▼
 > 300 linhas? ──NÃO──→ Verificar apenas extração de tipos
      │
     SIM
      │
      ▼
 Tem JSX + Hooks + Lógica juntos?
      │
     SIM ──→ Separar em 3+ arquivos (UI / Hook / Service)
      │
     NÃO
      │
      ▼
 Tem tipos inline complexos (> 5 interfaces)?
      │
     SIM ──→ Extrair para .types.ts
      │
     NÃO
      │
      ▼
 Tem funções utilitárias puras (> 3 funções)?
      │
     SIM ──→ Extrair para utils/
      │
     NÃO
      │
      ▼
 Dividir por domínio lógico (menor coesão primeiro)
```

---

## Regras de Ouro

1. **Nunca quebre o que funciona** — sempre rode `tsc --noEmit` após refatoração
2. **Imports sempre relativos** — facilita movimentação futura
3. **Um conceito por arquivo** — se o nome tiver "e" ou "/", dividir mais
4. **Barrel exports** com moderação — use apenas em `types/` e `components/`
5. **Não otimize prematuramente** — só divida se o arquivo for > 300 linhas OU tiver múltiplas responsabilidades claras
6. **Preserve o histórico** — mencione ao usuário que o `git mv` preserva histórico melhor que deletar/criar

---

## Referências adicionais

- `references/patterns.md` — Padrões avançados de organização por stack (Next.js, Vite, NestJS)
- `references/token-math.md` — Tabela detalhada de estimativa de tokens por tipo de arquivo

Para stacks específicas (NestJS, Vite, monorepo), leia `references/patterns.md` antes de propor a estrutura.
