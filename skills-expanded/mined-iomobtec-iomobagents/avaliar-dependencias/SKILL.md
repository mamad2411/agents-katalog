---
name: avaliar-dependencias
description: "Analisa viabilidade, risco, manutenção e licenciamento de uma dependência externa antes de adotá-la. Use quando o arquiteto avalia incluir uma nova biblioteca ou serviço de terceiro."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: avaliar-dependencias

Analisa a **viabilidade e o risco de adicionar ou atualizar uma dependência externa** ao projeto. Avalia licença, manutenção, segurança, tamanho e compatibilidade antes de recomendar adoção ou rejeição.

**Agente:** arquiteto  
**Guardrails aplicáveis:** `00-core.md`, `backend.md`

---

## Quando usar

- Antes de executar `npm install <pacote>` em qualquer serviço
- Ao avaliar major version upgrade de dependência existente
- Quando um pacote existente se torna inseguro (CVE publicado) e precisa de substituto
- Para comparar alternativas antes de escolher uma biblioteca

---

## Entrada esperada

- Nome do pacote (ou lista de candidatos)
- Finalidade: o que o pacote resolve no projeto
- Camada onde será usado (backend Node.js, frontend React, ambos)
- Alternativas conhecidas (opcional)

---

## Processo de execução

### Passo 1 — Verificar se já existe solução interna ou nativa

Antes de avaliar pacote externo:
- A funcionalidade existe nativamente no Node.js ou no browser?
- O projeto já tem outro pacote que resolve o mesmo problema?
- Uma função utilitária simples resolveria sem dependência nova?

Se sim a qualquer um, recomendar a solução interna e encerrar.

### Passo 2 — Levantar dados do pacote

Para cada candidato avaliar:

| Critério | Onde verificar | Peso |
|---|---|---|
| Downloads semanais | npmjs.com | Alto |
| Data do último release | npmjs.com / GitHub | Alto |
| Issues abertas vs fechadas | GitHub | Médio |
| Número de mantenedores ativos | GitHub | Alto |
| Versão atual vs última | npmjs.com | Alto |
| Vulnerabilidades conhecidas | `npm audit` / Snyk / GitHub Security | Crítico |
| Tipo de licença | `package.json` / npmjs.com | Alto |
| Tamanho do bundle (frontend) | bundlephobia.com | Médio |
| TypeScript support | `@types/` ou tipos embutidos | Médio |
| Dependências transitivas | npmjs.com | Médio |

### Passo 3 — Avaliar licença

| Licença | Uso em software proprietário | Ação |
|---|---|---|
| MIT, ISC, BSD-2, BSD-3, Apache-2.0 | Permitido | Pode adotar |
| LGPL-2.1, LGPL-3.0 | Permitido com restrições de linking | Verificar com equipe |
| GPL-2.0, GPL-3.0, AGPL | Pode contaminar código proprietário | Bloquear — escalar para arquiteto |
| Unlicensed / sem licença | Sem permissão de uso | Bloquear |
| Licença comercial | Pode exigir pagamento | Verificar antes de adotar |

### Passo 4 — Avaliar saúde do projeto

Sinais de projeto abandonado (qualquer um = risco alto):
- Último commit há mais de 12 meses sem release
- Issues críticas abertas há mais de 6 meses sem resposta
- Mantenedor único sem backup declarado
- Repositório arquivado

### Passo 5 — Avaliar risco de breaking change futuro

- O pacote segue semver rigoroso?
- Há histórico de breaking changes em minor versions?
- O pacote está em versão `0.x` (sem estabilidade garantida)?

### Passo 6 — Recomendar

Baseado nos critérios, emitir recomendação:
- **Adotar** — baixo risco, boa saúde, licença ok
- **Adotar com ressalvas** — boa funcionalidade mas ponto de atenção declarado
- **Avaliar alternativa** — existe opção melhor que deve ser considerada primeiro
- **Rejeitar** — licença, segurança ou abandono tornam inaceitável

---

## Saída produzida

```markdown
## Avaliação de Dependência: <nome-do-pacote>

**Versão avaliada:** x.y.z  
**Finalidade:** <o que resolve>  
**Camada:** backend | frontend | ambos  
**Recomendação:** ✅ Adotar | ⚠️ Adotar com ressalvas | 🔄 Avaliar alternativa | ⛔ Rejeitar

---

### Dados do pacote

| Critério | Resultado | Avaliação |
|---|---|---|
| Downloads semanais | N | ✅ / ⚠️ / ⛔ |
| Último release | YYYY-MM-DD | ✅ / ⚠️ / ⛔ |
| Vulnerabilidades | N abertas | ✅ / ⚠️ / ⛔ |
| Licença | MIT | ✅ / ⚠️ / ⛔ |
| TypeScript support | Embutido | ✅ / ⚠️ / ⛔ |
| Bundle size (gzip) | N KB | ✅ / ⚠️ / ⛔ |

---

### Justificativa

<Por que adotar ou rejeitar — pontos principais>

### Riscos declarados

- <risco 1 e como mitigar>
- <risco 2 e como mitigar>

### Alternativas consideradas

| Alternativa | Por que não foi escolhida |
|---|---|
| <pacote-b> | <motivo> |

### Instrução de instalação (se aprovado)

```bash
npm install <pacote>@<versão-exata>
```

Fixar versão exata no `package.json` — não usar `^` ou `~` para dependências críticas.
```
