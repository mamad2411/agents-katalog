---
name: skill-developer
description: Criar e gerenciar skills de Claude Code seguindo as melhores práticas da Anthropic. Use ao criar novas skills, modificar skill-rules.json, entender padrões de ativação, trabalhar com hooks, debugar ativação de skills ou implementar divulgação progressiva. Abrange estrutura de skill, frontmatter YAML, tipos de trigger (palavras-chave, padrões de intenção, caminhos de arquivo, padrões de conteúdo), níveis de enforcement (block, suggest, warn), mecanismos de hook (UserPromptSubmit, PreToolUse), rastreamento de sessão e a regra de 500 linhas.
---

# Guia do Desenvolvedor de Skills

## Propósito

Guia completo para criar e gerenciar skills em Claude Code com sistema de auto-ativação, seguindo as melhores práticas oficiais da Anthropic, incluindo a regra de 500 linhas e padrão de divulgação progressiva.

## Quando Usar Esta Skill

Ativa automaticamente quando você menciona:
- Criar ou adicionar skills
- Modificar triggers ou regras de skill
- Entender como a ativação de skill funciona
- Debugar problemas de ativação de skill
- Trabalhar com skill-rules.json
- Mecânica do sistema de hooks
- Melhores práticas de Claude Code
- Divulgação progressiva
- Frontmatter YAML
- Regra de 500 linhas

---

## Visão Geral do Sistema

### Arquitetura de Dois Hooks

**1. Hook UserPromptSubmit** (Sugestões Proativas)
- **Arquivo**: `.claude/hooks/skill-activation-prompt.ts`
- **Ativação**: ANTES de Claude ver o prompt do usuário
- **Propósito**: Sugerir skills relevantes com base em palavras-chave + padrões de intenção
- **Método**: Injeta lembrança formatada como contexto (stdout → entrada de Claude)
- **Casos de uso**: Skills baseadas em tópico, detecção de trabalho implícito

**2. Stop Hook - Lembretes de Tratamento de Erros** (Lembretes Suaves)
- **Arquivo**: `.claude/hooks/error-handling-reminder.ts`
- **Ativação**: DEPOIS que Claude termina de responder
- **Propósito**: Lembrança suave para auto-avaliar tratamento de erros no código escrito
- **Método**: Analisa arquivos editados para padrões arriscados, exibe lembrança se necessário
- **Casos de uso**: Consciência de tratamento de erros sem bloquear fluxo de trabalho

**Mudança de Filosofia (2025-10-27):** Abandonamos o bloqueio PreToolUse para Sentry/tratamento de erros. Em vez disso, use lembretes suaves pós-resposta que não bloqueiam o fluxo de trabalho mas mantêm consciência de qualidade de código.

### Arquivo de Configuração

**Localização**: `.claude/skills/skill-rules.json`

Define:
- Todas as skills e suas condições de ativação
- Níveis de enforcement (block, suggest, warn)
- Padrões de caminho de arquivo (glob)
- Padrões de detecção de conteúdo (regex)
- Condições de skip (rastreamento de sessão, marcadores de arquivo, variáveis de ambiente)

---

## Tipos de Skill

### 1. Skills de Proteção (Guardrail)

**Propósito:** Enforçar melhores práticas críticas que previnem erros

**Características:**
- Tipo: `"guardrail"`
- Enforcement: `"block"`
- Prioridade: `"critical"` ou `"high"`
- Bloqueia edições de arquivo até a skill ser usada
- Previne erros comuns (nomes de coluna, erros críticos)
- Consciência de sessão (não repete nag na mesma sessão)

**Exemplos:**
- `database-verification` - Verificar nomes de tabela/coluna antes de queries Prisma
- `frontend-dev-guidelines` - Enforçar padrões React/TypeScript

**Quando Usar:**
- Erros que causam falhas em runtime
- Problemas de integridade de dados
- Problemas críticos de compatibilidade

### 2. Skills de Domínio

**Propósito:** Fornecer orientação abrangente para áreas específicas

**Características:**
- Tipo: `"domain"`
- Enforcement: `"suggest"`
- Prioridade: `"high"` ou `"medium"`
- Advisory, não obrigatório
- Específico de tópico ou domínio
- Documentação abrangente

**Exemplos:**
- `backend-dev-guidelines` - Padrões Node.js/Express/TypeScript
- `frontend-dev-guidelines` - Melhores práticas React/TypeScript
- `error-tracking` - Orientação de integração Sentry

**Quando Usar:**
- Sistemas complexos que exigem conhecimento profundo
- Documentação de melhores práticas
- Padrões arquiteturais
- Guias de como fazer

---

## Quick Start: Criando uma Nova Skill

### Passo 1: Criar Arquivo de Skill

**Localização:** `.claude/skills/{nome-skill}/SKILL.md`

**Template:**
```markdown
---
name: minha-nova-skill
description: Breve descrição incluindo palavras-chave que ativam esta skill. Mencione tópicos, tipos de arquivo e casos de uso. Seja explícito sobre termos de ativação.
---

# Minha Nova Skill

## Propósito
O que esta skill ajuda

## Quando Usar
Cenários e condições específicas

## Informações-Chave
A orientação real, documentação, padrões, exemplos
```

**Melhores Práticas:**
- ✅ **Nome**: Minúsculas, hífens, forma gerúndio preferida (verbo + -ing)
- ✅ **Descrição**: Incluir TODAS as palavras-chave/frases de ativação (máx. 1024 caracteres)
- ✅ **Conteúdo**: Menos de 500 linhas - use arquivos de referência para detalhes
- ✅ **Exemplos**: Exemplos de código real
- ✅ **Estrutura**: Headings claros, listas, blocos de código

### Passo 2: Adicionar a skill-rules.json

Veja [SKILL_RULES_REFERENCE.md](SKILL_RULES_REFERENCE.md) para schema completo.

**Template Básico:**
```json
{
  "minha-nova-skill": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "medium",
    "promptTriggers": {
      "keywords": ["palavra-chave1", "palavra-chave2"],
      "intentPatterns": ["(criar|adicionar).*?algo"]
    }
  }
}
```

### Passo 3: Testar Triggers

**Testar UserPromptSubmit:**
```bash
echo '{"session_id":"test","prompt":"seu prompt de teste"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

**Testar PreToolUse:**
```bash
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"session_id":"test","tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
```

### Passo 4: Refinar Padrões

Com base nos testes:
- Adicionar palavras-chave faltantes
- Refinar padrões de intenção para reduzir falsos positivos
- Ajustar padrões de caminho de arquivo
- Testar padrões de conteúdo contra arquivos reais

### Passo 5: Seguir Melhores Práticas da Anthropic

✅ Manter SKILL.md menor que 500 linhas
✅ Usar divulgação progressiva com arquivos de referência
✅ Adicionar índice a arquivos de referência > 100 linhas
✅ Escrever descrição detalhada com palavras-chave de ativação
✅ Testar com 3+ cenários reais antes de documentar
✅ Iterar com base no uso real

---

## Níveis de Enforcement

### BLOCK (Proteções Críticas)

- Previne fisicamente execução da ferramenta Edit/Write
- Código de saída 2 do hook, stderr → Claude
- Claude vê mensagem e deve usar a skill para prosseguir
- **Use Para**: Erros críticos, integridade de dados, problemas de segurança

**Exemplo:** Verificação de nome de coluna de banco de dados

### SUGGEST (Recomendado)

- Lembrança injetada antes de Claude ver o prompt
- Claude está ciente de skills relevantes
- Não enforçado, apenas advisory
- **Use Para**: Orientação de domínio, melhores práticas, guias de como fazer

**Exemplo:** Diretrizes de desenvolvimento frontend

### WARN (Opcional)

- Sugestões de baixa prioridade
- Apenas advisory, enforcement mínimo
- **Use Para**: Sugestões úteis, lembretes informativos

**Raramente usado** - a maioria das skills são BLOCK ou SUGGEST.

---

## Condições de Skip & Controle do Usuário

### 1. Rastreamento de Sessão

**Propósito:** Não incomodar repetidamente na mesma sessão

**Como funciona:**
- Primeira edição → Hook bloqueia, atualiza estado de sessão
- Segunda edição (mesma sessão) → Hook permite
- Sessão diferente → Bloqueia novamente

**Arquivo de Estado:** `.claude/hooks/state/skills-used-{session_id}.json`

### 2. Marcadores de Arquivo

**Propósito:** Skip permanente para arquivos verificados

**Marcador:** `// @skip-validation`

**Uso:**
```typescript
// @skip-validation
import { PrismaService } from './prisma';
// Este arquivo foi verificado manualmente
```

**NOTA:** Use com moderação - derrota o propósito se usado em excesso

### 3. Variáveis de Ambiente

**Propósito:** Desabilitar de emergência, override temporário

**Desabilitar globalmente:**
```bash
export SKIP_SKILL_GUARDRAILS=true  # Desabilita TODOS os blocos PreToolUse
```

**Específico de skill:**
```bash
export SKIP_DB_VERIFICATION=true
export SKIP_ERROR_REMINDER=true
```

---

## Checklist de Teste

Ao criar uma nova skill, verifique:

- [ ] Arquivo de skill criado em `.claude/skills/{nome}/SKILL.md`
- [ ] Frontmatter apropriado com name e description
- [ ] Entrada adicionada a `skill-rules.json`
- [ ] Palavras-chave testadas com prompts reais
- [ ] Padrões de intenção testados com variações
- [ ] Padrões de caminho de arquivo testados com arquivos reais
- [ ] Padrões de conteúdo testados contra conteúdo de arquivo
- [ ] Mensagem de bloqueio é clara e acionável (se guardrail)
- [ ] Condições de skip configuradas apropriadamente
- [ ] Nível de prioridade corresponde à importância
- [ ] Sem falsos positivos nos testes
- [ ] Sem falsos negativos nos testes
- [ ] Performance aceitável (<100ms ou <200ms)
- [ ] Sintaxe JSON validada: `jq . skill-rules.json`
- [ ] **SKILL.md menor que 500 linhas** ⭐
- [ ] Arquivos de referência criados se necessário
- [ ] Índice adicionado a arquivos > 100 linhas

---

## Arquivos de Referência

Para informações detalhadas sobre tópicos específicos, veja:

### [TRIGGER_TYPES.md](TRIGGER_TYPES.md)
Guia completo para todos os tipos de trigger:
- Triggers de palavra-chave (correspondência explícita de tópico)
- Padrões de intenção (detecção implícita de ação)
- Triggers de caminho de arquivo (padrões glob)
- Padrões de conteúdo (regex em arquivos)
- Melhores práticas e exemplos para cada
- Armadilhas comuns e estratégias de teste

### [SKILL_RULES_REFERENCE.md](SKILL_RULES_REFERENCE.md)
Schema completo de skill-rules.json:
- Definições completas de interface TypeScript
- Explicações campo a campo
- Exemplo completo de skill guardrail
- Exemplo completo de skill de domínio
- Guia de validação e erros comuns

### [HOOK_MECHANISMS.md](HOOK_MECHANISMS.md)
Mergulho profundo nos internals de hooks:
- Fluxo UserPromptSubmit (detalhado)
- Fluxo PreToolUse (detalhado)
- Tabela de comportamento de código de saída (CRÍTICO)
- Gerenciamento de estado de sessão
- Considerações de performance

### [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
Guia abrangente de debugging:
- Skill não está ativando (UserPromptSubmit)
- PreToolUse não está bloqueando
- Falsos positivos (muitos triggers)
- Hook não está executando
- Problemas de performance

### [PATTERNS_LIBRARY.md](PATTERNS_LIBRARY.md)
Coleção de padrões prontos para usar:
- Biblioteca de padrões de intenção (regex)
- Biblioteca de padrões de caminho de arquivo (glob)
- Biblioteca de padrões de conteúdo (regex)
- Organizado por caso de uso
- Pronto para copiar e colar

### [ADVANCED.md](ADVANCED.md)
Aprimoramentos futuros e ideias:
- Atualizações de regras dinâmicas
- Dependências de skill
- Enforcement condicional
- Analytics de skill
- Versionamento de skill

---

## Resumo de Referência Rápida

### Criar Nova Skill (5 Passos)

1. Criar `.claude/skills/{nome}/SKILL.md` com frontmatter
2. Adicionar entrada a `.claude/skills/skill-rules.json`
3. Testar com comandos `npx tsx`
4. Refinar padrões com base em testes
5. Manter SKILL.md menor que 500 linhas

### Tipos de Trigger

- **Palavras-chave**: Menções explícitas de tópico
- **Intenção**: Detecção implícita de ação
- **Caminhos de Arquivo**: Ativação baseada em localização
- **Conteúdo**: Detecção específica de tecnologia

Veja [TRIGGER_TYPES.md](TRIGGER_TYPES.md) para detalhes completos.

### Enforcement

- **BLOCK**: Código de saída 2, apenas crítico
- **SUGGEST**: Injetar contexto, mais comum
- **WARN**: Advisory, raramente usado

### Condições de Skip

- **Rastreamento de sessão**: Automático (previne nags repetidos)
- **Marcadores de arquivo**: `// @skip-validation` (skip permanente)
- **Variáveis de env**: `SKIP_SKILL_GUARDRAILS` (desabilitar de emergência)

### Melhores Práticas da Anthropic

✅ **Regra de 500 linhas**: Manter SKILL.md menor que 500 linhas
✅ **Divulgação progressiva**: Usar arquivos de referência para detalhes
✅ **Índice**: Adicionar a arquivos de referência > 100 linhas
✅ **Um nível profundo**: Não aninhar referências profundamente
✅ **Descrições ricas**: Incluir todas as palavras-chave de ativação (máx. 1024 caracteres)
✅ **Testar primeiro**: Construir 3+ avaliações antes de documentação extensa
✅ **Naming em gerúndio**: Preferir verbo + -ing (ex: "processando-pdfs")

### Debugar

Testar hooks manualmente:
```bash
# UserPromptSubmit
echo '{"prompt":"teste"}' | npx tsx .claude/hooks/skill-activation-prompt.ts

# PreToolUse
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
```

Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para guia completo de debugging.

---

## Arquivos Relacionados

**Configuração:**
- `.claude/skills/skill-rules.json` - Configuração mestre
- `.claude/hooks/state/` - Rastreamento de sessão
- `.claude/settings.json` - Registro de hooks

**Hooks:**
- `.claude/hooks/skill-activation-prompt.ts` - UserPromptSubmit
- `.claude/hooks/error-handling-reminder.ts` - Evento Stop (lembretes suaves)

**Todas as Skills:**
- `.claude/skills/*/SKILL.md` - Arquivos de conteúdo de skill

---

**Status de Skill**: COMPLETO - Reestruturado seguindo melhores práticas da Anthropic ✅
**Contagem de Linhas**: < 500 (seguindo regra de 500 linhas) ✅
**Divulgação Progressiva**: Arquivos de referência para informações detalhadas ✅

**Próximo**: Criar mais skills, refinar padrões com base no uso