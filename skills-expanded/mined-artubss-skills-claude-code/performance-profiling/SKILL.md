---
name: performance-profiling
description: Princípios de análise de desempenho. Técnicas de medição, análise e otimização.
allowed-tools: Read, Glob, Grep, Bash
---

# Análise de Desempenho

> Meça, analise, otimize — nessa ordem.

## 🔧 Scripts de Execução

**Execute estes para análise de desempenho automatizada:**

| Script | Propósito | Uso |
|--------|-----------|-----|
| `scripts/lighthouse_audit.py` | Auditoria de desempenho Lighthouse | `python scripts/lighthouse_audit.py https://example.com` |

---

## 1. Core Web Vitals

### Alvos

| Métrica | Bom | Ruim | Mede |
|---------|-----|------|------|
| **LCP** | < 2,5s | > 4,0s | Carregamento |
| **INP** | < 200ms | > 500ms | Interatividade |
| **CLS** | < 0,1 | > 0,25 | Estabilidade |

### Quando Medir

| Estágio | Ferramenta |
|---------|-----------|
| Desenvolvimento | Lighthouse local |
| CI/CD | Lighthouse CI |
| Produção | RUM (Real User Monitoring) |

---

## 2. Workflow de Análise

### Processo em 4 Etapas

```
1. BASELINE → Meça o estado atual
2. IDENTIFIQUE → Encontre o gargalo
3. CORRIJA → Faça a mudança direcionada
4. VALIDE → Confirme a melhoria
```

### Seleção de Ferramenta de Análise

| Problema | Ferramenta |
|----------|-----------|
| Carregamento de página | Lighthouse |
| Tamanho do bundle | Bundle analyzer |
| Runtime | DevTools Performance |
| Memória | DevTools Memory |
| Rede | DevTools Network |

---

## 3. Análise de Bundle

### O Que Procurar

| Problema | Indicador |
|----------|-----------|
| Dependências grandes | Topo do bundle |
| Código duplicado | Múltiplos chunks |
| Código não utilizado | Cobertura baixa |
| Divisões ausentes | Chunk único grande |

### Ações de Otimização

| Descoberta | Ação |
|-----------|------|
| Biblioteca grande | Importe módulos específicos |
| Deps duplicadas | Deduque, atualize versões |
| Rota no principal | Divida o código |
| Exports não utilizados | Tree shake |

---

## 4. Análise de Runtime

### Análise da Aba Performance

| Padrão | Significado |
|--------|------------|
| Tarefas longas (>50ms) | UI bloqueada |
| Muitas tarefas pequenas | Oportunidade de batching possível |
| Layout/paint | Gargalo de renderização |
| Script | Execução de JavaScript |

### Análise da Aba Memory

| Padrão | Significado |
|--------|------------|
| Heap crescente | Vazamento possível |
| Retenção grande | Verifique referências |
| DOM desanexado | Não foi limpo |

---

## 5. Gargalos Comuns

### Por Sintoma

| Sintoma | Causa Provável |
|--------|---------------|
| Carregamento inicial lento | JS grande, render blocking |
| Interações lentas | Handlers de eventos pesados |
| Jank durante scroll | Layout thrashing |
| Memória crescente | Vazamentos, refs retidas |

---

## 6. Prioridades de Ganhos Rápidos

| Prioridade | Ação | Impacto |
|-----------|------|--------|
| 1 | Ative compressão | Alto |
| 2 | Lazy load de imagens | Alto |
| 3 | Divida código por rotas | Alto |
| 4 | Cache de ativos estáticos | Médio |
| 5 | Otimize imagens | Médio |

---

## 7. Anti-padrões

| ❌ Não faça | ✅ Faça |
|-----------|---------|
| Adivinhe os problemas | Analise primeiro |
| Micro-otimize | Corrija o maior problema |
| Otimize cedo | Otimize quando necessário |
| Ignore usuários reais | Use dados RUM |

---

> **Lembre-se:** O código mais rápido é o código que não executa. Remova antes de otimizar.