# CLAUDE.md - Legal Workbench Frontend

Este modulo e o frontend React do Legal Workbench.

---

## Regras Especificas

### Stack
- React 18.2 + TypeScript 5.2
- Vite 5.0 como bundler
- React Router 7.11 para rotas
- Zustand 4.4 para estado global
- TipTap 3.15 para rich text editor (Doc Assembler)
- Tailwind CSS 3.3 para styling
- Lucide React para icones
- Sentry 2.0 para error tracking

### Comandos Locais
```bash
cd legal-workbench/frontend
bun install
bun run dev      # Dev server
bun run build    # Build producao
bun run lint     # ESLint
```

### Antes de Modificar
1. Verificar se build passa: `bun run build`
2. Verificar lint: `bun run lint`
3. Testar no browser

### NUNCA (Especifico do Frontend)
- Usar `npm` ou `yarn` (apenas `bun`)
- Importar de `ccui-assistant/` (removido)
- Criar arquivos `.jsx` (usar `.tsx`)
- Hardcodar URLs de API (usar env vars)
- Modificar arquivos em `ferramentas/` durante tarefas de frontend

### Padrao de Componentes
```typescript
// Preferir: functional components com hooks
const Component: React.FC<Props> = ({ prop }) => {
  // hooks primeiro
  // handlers depois
  // return por ultimo
};
```

### Estrutura de Pastas
```
frontend/
├── src/
│   ├── components/       # Componentes React
│   │   ├── document/     # TipTapDocumentViewer, FieldList, FieldEditorPanel
│   │   ├── templates/    # TemplateList, AssemblePanel
│   │   ├── upload/       # DropZone (full e compact)
│   │   └── ui/           # Button, Modal, Input, CollapsibleSection
│   ├── extensions/       # TipTap extensions
│   │   └── FieldAnnotationMark.ts  # Mark para anotacoes de campo
│   ├── pages/            # Paginas/rotas (DocAssemblerModule, STJModule, etc)
│   ├── services/         # API clients (api.ts)
│   ├── store/            # Zustand stores (documentStore.ts)
│   └── types/            # TypeScript types (index.ts)
├── public/
├── Dockerfile            # Multi-stage: bun build + nginx
├── nginx.conf            # Config nginx para SPA
└── index.html
```

### Modulos Principais

| Modulo | Rota | Descricao |
|--------|------|-----------|
| HubHome | `/` | Dashboard principal |
| DocAssembler | `/doc-assembler` | Editor de templates com TipTap |
| STJ | `/stj` | Consulta dados STJ |
| TrelloModule | `/trello` | Command center Trello |
| TextExtractor | `/text-extractor` | OCR + AI extraction |
| LedesConverter | `/ledes` | Conversor LEDES |

---

## Verificacao Obrigatoria

Antes de considerar qualquer tarefa de frontend concluida:

### 1. Build e Lint
```bash
cd legal-workbench/frontend
bun run build   # Deve passar sem erros
bun run lint    # Zero warnings idealmente
```

### 2. Testes Unitarios
```bash
bun run test              # Vitest - todos os testes
bun run test ComponentX   # Teste especifico
```

### 3. Verificacao Visual (quando UI mudou)
Usar Chrome MCP ou Playwright para verificar:
- Componente renderiza corretamente
- Estados de loading/error funcionam
- Responsividade (se aplicavel)

### 4. Checklist Pre-Commit
- [ ] Build passa
- [ ] Lint passa
- [ ] Testes passam (se existirem para o componente)
- [ ] Verificacao visual feita (para mudancas de UI)

> **Regra**: NAO commitar sem verificar. Erros descobertos no CI sao evitaveis.

---

## TipTap (Doc Assembler)

### Extensoes Customizadas
- `FieldAnnotationMark`: Mark para destacar campos de anotacao com cores

### Padroes de Posicionamento
```typescript
// Calculo de posicao global a partir de paragrafo + offset local
let globalStart = 0;
for (let i = 0; i < paragraphIndex; i++) {
  globalStart += paragraphs[i].length + 2; // +2 para "\n\n"
}
globalStart += localOffset;
```

### Estrutura do Document
- Documento = array de paragrafos
- Paragrafos unidos com `\n\n` no textContent
- Posicoes sao relativas ao paragrafo (paragraphIndex + localOffset)

---

## Deploy

### Build Docker
```bash
# Multi-stage build
bun install && bun run build  # Stage 1: build
nginx                          # Stage 2: serve
```

---

*Herdado de: legal-workbench/CLAUDE.md*
*Ultima atualizacao: 2026-01-17*
