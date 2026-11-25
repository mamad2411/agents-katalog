---
name: session-handoff
description: "Cria documentos abrangentes de transferência para transições contínuas entre agentes IA. Acionado quando: (1) usuário solicita handoff/salvar memória/contexto, (2) janela de contexto se aproxima da capacidade, (3) marco importante de tarefa concluído, (4) sessão de trabalho terminando, (5) usuário diz 'salvar estado', 'criar handoff', 'preciso pausar', 'contexto está ficando cheio', (6) retomando trabalho com 'carregar handoff', 'retomar de', 'continuar de onde parei'. Sugere proativamente handoffs após trabalho substancial (múltiplas edições de arquivo, debugging complexo, decisões arquiteturais). Resolve exaustão de contexto de agente de longa duração habilitando agentes novos a continuar com zero ambiguidade."
---

# Handoff

Cria documentos abrangentes de transferência que permitem a agentes IA novos continuarem o trabalho com zero ambiguidade. Resolve o problema de exaustão de contexto de agentes de longa duração.

## Seleção de Modo

Determine qual modo se aplica:

**Criando um handoff?** Usuário quer salvar estado atual, pausar trabalho ou contexto está ficando cheio.
- Siga: Fluxo CREATE abaixo

**Retomando de um handoff?** Usuário quer continuar trabalho anterior, carregar contexto, ou menciona um handoff existente.
- Siga: Fluxo RESUME abaixo

**Sugestão proativa?** Após trabalho substancial (5+ edições de arquivo, debugging complexo, decisões maiores), sugira:
> "Fizemos progresso significativo. Considere criar um documento handoff para preservar este contexto em sessões futuras. Diga 'criar handoff' quando estiver pronto."

## Fluxo CREATE

### Passo 1: Gerar Scaffold

Execute o script de scaffold inteligente para criar um documento handoff pré-preenchido:

```bash
python scripts/create_handoff.py [task-slug]
```

Exemplo: `python scripts/create_handoff.py implementing-user-auth`

**Para handoffs de continuação** (vinculando a trabalho anterior):
```bash
python scripts/create_handoff.py "auth-part-2" --continues-from 2024-01-15-auth.md
```

O script irá:
- Criar diretório `.claude/handoffs/` se necessário
- Gerar nome de arquivo com timestamp
- Pré-preenchimento: timestamp, caminho do projeto, branch git, commits recentes, arquivos modificados
- Adicionar links de cadeia de handoff se continuando de trabalho anterior
- Exportar caminho do arquivo para edição

### Passo 2: Completar o Documento Handoff

Abra o arquivo gerado e preencha todas as seções `[TODO: ...]`. Priorize estas seções:

1. **Current State Summary** - O que está acontecendo agora
2. **Important Context** - Informações críticas que o próximo agente DEVE saber
3. **Immediate Next Steps** - Primeiros passos claros e acionáveis
4. **Decisions Made** - Escolhas com fundamentação (não apenas resultados)

Use a estrutura de template em [references/handoff-template.md](references/handoff-template.md) como orientação.

### Passo 3: Validar o Handoff

Execute o script de validação para verificar completude e segurança:

```bash
python scripts/validate_handoff.py <handoff-file>
```

O validador verifica:
- [ ] Sem placeholders `[TODO: ...]` remanescentes
- [ ] Seções obrigatórias presentes e preenchidas
- [ ] Nenhum potencial segredo detectado (chaves de API, senhas, tokens)
- [ ] Arquivos referenciados existem
- [ ] Escore de qualidade (0-100)

**Não finalize um handoff com segredos detectados ou escore abaixo de 70.**

### Passo 4: Confirmar Handoff

Relate ao usuário:
- Localização do arquivo handoff
- Escore de validação e avisos
- Resumo do contexto capturado
- Item de ação primeira para próxima sessão

## Fluxo RESUME

### Passo 1: Encontrar Handoffs Disponíveis

Liste handoffs no projeto atual:

```bash
python scripts/list_handoffs.py
```

Isso mostra todos os handoffs com datas, títulos e status de conclusão.

### Passo 2: Verificar Defasagem

Antes de carregar, verifique quão atual o handoff é:

```bash
python scripts/check_staleness.py <handoff-file>
```

Níveis de defasagem:
- **FRESH**: Seguro para retomar - mudanças mínimas desde handoff
- **SLIGHTLY_STALE**: Revise mudanças, depois retome
- **STALE**: Verifique contexto cuidadosamente antes de retomar
- **VERY_STALE**: Considere criar um handoff novo

O script verifica:
- Tempo desde criação do handoff
- Commits git desde handoff
- Arquivos mudados desde handoff
- Divergência de branch
- Arquivos referenciados faltando

### Passo 3: Carregar o Handoff

Leia o documento handoff relevante completamente antes de tomar qualquer ação.

Se o handoff faz parte de uma cadeia (tem link "Continues from"), também leia o handoff anterior vinculado para contexto completo.

### Passo 4: Verificar Contexto

Siga a checklist em [references/resume-checklist.md](references/resume-checklist.md):

1. Verifique se diretório do projeto e branch git combinam
2. Verifique se bloqueadores foram resolvidos
3. Valide que suposições ainda se mantêm
4. Revise arquivos modificados para conflitos
5. Verifique estado do ambiente

### Passo 5: Começar Trabalho

Inicie com o item "Immediate Next Steps" #1 do documento handoff.

Referencie estas seções conforme trabalhar:
- "Critical Files" para localizações importantes
- "Key Patterns Discovered" para convenções a seguir
- "Potential Gotchas" para evitar problemas conhecidos

### Passo 6: Atualizar ou Encadear Handoffs

Conforme trabalhar:
- Marque itens concluídos em "Pending Work"
- Adicione novas descobertas em seções relevantes
- Para sessões longas: crie um novo handoff com `--continues-from` para encadeá-los

## Encadeamento de Handoff

Para projetos de longa duração, encadeie handoffs juntos para manter linhagem de contexto:

```
handoff-1.md (trabalho inicial)
    ↓
handoff-2.md --continues-from handoff-1.md
    ↓
handoff-3.md --continues-from handoff-2.md
```

Cada handoff na cadeia:
- Vincula-se ao seu predecessor
- Pode marcar handoffs antigos como supersedidos
- Fornece migalhas de contexto para novos agentes

Ao retomar de uma cadeia, leia o handoff mais recente primeiro, depois referencie predecessores conforme necessário.

## Localização de Armazenamento

Handoffs são armazenados em: `.claude/handoffs/`

Convenção de nomenclatura: `YYYY-MM-DD-HHMMSS-[slug].md`

Exemplo: `2024-01-15-143022-implementing-auth.md`

## Recursos

### scripts/

| Script | Propósito |
|--------|-----------|
| `create_handoff.py [slug] [--continues-from <file>]` | Gera novo handoff com scaffold inteligente |
| `list_handoffs.py [path]` | Lista handoffs disponíveis em um projeto |
| `validate_handoff.py <file>` | Verifica completude, qualidade e segurança |
| `check_staleness.py <file>` | Avalia se contexto de handoff ainda é atual |

### references/

- [handoff-template.md](references/handoff-template.md) - Estrutura completa de template com orientação
- [resume-checklist.md](references/resume-checklist.md) - Checklist de verificação para agentes retomando