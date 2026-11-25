---
name: clean-code
description: Padrões pragmáticos de codificação - conciso, direto, sem over-engineering, sem comentários desnecessários
allowed-tools: Read, Write, Edit
version: 2.0
priority: CRITICAL
---

# Clean Code - Padrões Pragmáticos de Codificação com IA

> **HABILIDADE CRÍTICA** - Seja **conciso, direto e focado em solução**.

---

## Princípios Essenciais

| Princípio | Regra |
|-----------|-------|
| **SRP** | Responsabilidade Única - cada função/classe faz UMA coisa |
| **DRY** | Don't Repeat Yourself - extraia duplicatas, reutilize |
| **KISS** | Keep It Simple - a solução mais simples que funciona |
| **YAGNI** | You Aren't Gonna Need It - não construa recursos não usados |
| **Boy Scout** | Deixe o código mais limpo do que encontrou |

---

## Regras de Nomenclatura

| Elemento | Convenção |
|----------|-----------|
| **Variáveis** | Revele intenção: `userCount` não `n` |
| **Funções** | Verbo + substantivo: `getUserById()` não `user()` |
| **Booleanos** | Forma de pergunta: `isActive`, `hasPermission`, `canEdit` |
| **Constantes** | SCREAMING_SNAKE: `MAX_RETRY_COUNT` |

> **Regra:** Se você precisa de um comentário para explicar um nome, renomeie.

---

## Regras de Função

| Regra | Descrição |
|-------|-----------|
| **Pequena** | Máx 20 linhas, idealmente 5-10 |
| **Uma Coisa** | Faz uma coisa, faz bem |
| **Um Nível** | Um nível de abstração por função |
| **Poucos Args** | Máx 3 argumentos, prefira 0-2 |
| **Sem Efeitos Colaterais** | Não mute inputs inesperadamente |

---

## Estrutura de Código

| Padrão | Aplique |
|--------|---------|
| **Guard Clauses** | Early returns para casos extremos |
| **Flat > Nested** | Evite aninhamento profundo (máx 2 níveis) |
| **Composição** | Funções pequenas compostas juntas |
| **Colocalização** | Mantenha código relacionado perto |

---

## Estilo de Codificação com IA

| Situação | Ação |
|----------|------|
| Usuário pede feature | Escreva diretamente |
| Usuário relata bug | Corrija, não explique |
| Requisito não claro | Pergunte, não assuma |

---

## Anti-Padrões (NÃO FAÇA)

| ❌ Padrão | ✅ Solução |
|-----------|-----------|
| Comente cada linha | Delete comentários óbvios |
| Helper para one-liner | Inline do código |
| Factory para 2 objetos | Instanciação direta |
| utils.ts com 1 função | Coloque código onde é usado |
| "Primeiro importamos..." | Apenas escreva código |
| Aninhamento profundo | Guard clauses |
| Números mágicos | Constantes nomeadas |
| God functions | Divida por responsabilidade |

---

## 🔴 Antes de Editar QUALQUER Arquivo (PENSE PRIMEIRO!)

**Antes de alterar um arquivo, pergunte-se:**

| Pergunta | Por Quê |
|----------|---------|
| **O que importa este arquivo?** | Pode quebrar |
| **O que este arquivo importa?** | Mudanças de interface |
| **Quais testes cobrem isto?** | Testes podem falhar |
| **É um componente compartilhado?** | Múltiplos lugares afetados |

**Verificação Rápida:**
```
Arquivo a editar: UserService.ts
└── Quem importa isto? → UserController.ts, AuthController.ts
└── Precisam de mudanças também? → Verifique assinaturas de função
```

> 🔴 **Regra:** Edite o arquivo + todos os arquivos dependentes na MESMA tarefa.
> 🔴 **Nunca deixe imports quebrados ou atualizações faltando.**

---

## Resumo

| Faça | Não Faça |
|-----|----------|
| Escreva código diretamente | Escreva tutoriais |
| Deixe o código se auto-documentar | Adicione comentários óbvios |
| Corrija bugs imediatamente | Explique a correção primeiro |
| Inline coisas pequenas | Crie arquivos desnecessários |
| Nomeie as coisas claramente | Use abreviações |
| Mantenha funções pequenas | Escreva funções com 100+ linhas |

> **Lembre-se: O usuário quer código funcionando, não uma aula de programação.**

---

## 🔴 Auto-verificação Antes de Completar (OBRIGATÓRIO)

**Antes de dizer "tarefa concluída", verifique:**

| Verificação | Pergunta |
|-------------|----------|
| ✅ **Meta atingida?** | Fiz exatamente o que o usuário pediu? |
| ✅ **Arquivos editados?** | Modifiquei todos os arquivos necessários? |
| ✅ **Código funciona?** | Testei/verifiquei a mudança? |
| ✅ **Sem erros?** | Lint e TypeScript passam? |
| ✅ **Nada esquecido?** | Casos extremos faltando? |

> 🔴 **Regra:** Se QUALQUER verificação falhar, corrija antes de completar.

---

## Scripts de Verificação (OBRIGATÓRIO)

> 🔴 **CRÍTICO:** Cada agente executa APENAS os scripts de sua própria habilidade após concluir o trabalho.

### Mapeamento Agente → Script

| Agente | Script | Comando |
|--------|--------|---------|
| **frontend-specialist** | UX Audit | `python ~/.claude/skills/frontend-design/scripts/ux_audit.py .` |
| **frontend-specialist** | A11y Check | `python ~/.claude/skills/frontend-design/scripts/accessibility_checker.py .` |
| **backend-specialist** | API Validator | `python ~/.claude/skills/api-patterns/scripts/api_validator.py .` |
| **mobile-developer** | Mobile Audit | `python ~/.claude/skills/mobile-design/scripts/mobile_audit.py .` |
| **database-architect** | Schema Validate | `python ~/.claude/skills/database-design/scripts/schema_validator.py .` |
| **security-auditor** | Security Scan | `python ~/.claude/skills/vulnerability-scanner/scripts/security_scan.py .` |
| **seo-specialist** | SEO Check | `python ~/.claude/skills/seo-fundamentals/scripts/seo_checker.py .` |
| **seo-specialist** | GEO Check | `python ~/.claude/skills/geo-fundamentals/scripts/geo_checker.py .` |
| **performance-optimizer** | Lighthouse | `python ~/.claude/skills/performance-profiling/scripts/lighthouse_audit.py <url>` |
| **test-engineer** | Test Runner | `python ~/.claude/skills/testing-patterns/scripts/test_runner.py .` |
| **test-engineer** | Playwright | `python ~/.claude/skills/webapp-testing/scripts/playwright_runner.py <url>` |
| **Any agent** | Lint Check | `python ~/.claude/skills/lint-and-validate/scripts/lint_runner.py .` |
| **Any agent** | Type Coverage | `python ~/.claude/skills/lint-and-validate/scripts/type_coverage.py .` |
| **Any agent** | i18n Check | `python ~/.claude/skills/i18n-localization/scripts/i18n_checker.py .` |

> ❌ **ERRADO:** `test-engineer` executando `ux_audit.py`
> ✅ **CORRETO:** `frontend-specialist` executando `ux_audit.py`

---

### 🔴 Manipulação de Output de Script (LER → RESUMIR → PERGUNTAR)

**Quando executar um script de validação, você DEVE:**

1. **Executar o script** e capturar TODO o output
2. **Analisar o output** - identificar erros, avisos e aprovações
3. **Resumir para o usuário** neste formato:

```markdown
## Resultados do Script: [script_name.py]

### ❌ Erros Encontrados (X itens)
- [Arquivo:Linha] Descrição do erro 1
- [Arquivo:Linha] Descrição do erro 2

### ⚠️ Avisos (Y itens)
- [Arquivo:Linha] Descrição do aviso

### ✅ Aprovado (Z itens)
- Verificação 1 aprovada
- Verificação 2 aprovada

**Devo corrigir os X erros?**
```

4. **Aguarde confirmação do usuário** antes de corrigir
5. **Após corrigir** → Re-execute o script para confirmar

> 🔴 **VIOLAÇÃO:** Executar script e ignorar output = TAREFA FALHA.
> 🔴 **VIOLAÇÃO:** Auto-corrigir sem perguntar = Não permitido.
> 🔴 **Regra:** Sempre LER output → RESUMIR → PERGUNTAR → depois corrigir.