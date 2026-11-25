---
name: feature-design-assistant
description: "Transforme ideias em designs e especificações totalmente formados através de diálogo colaborativo natural. Use ao planejar novos recursos, projetar arquitetura ou fazer mudanças significativas na codebase."
---

# Assistente de Design de Recursos

Ajude a transformar ideias em designs e especificações totalmente formados através de coleta de informações estruturada e validação colaborativa.

**Anuncie no início:** "Estou usando a skill feature-design-assistant para projetar este recurso."

## Fase 1: Descoberta de Contexto

Primeiro, explore a codebase para entender:
- Estrutura do projeto e tech stack
- Padrões e convenções existentes
- Recursos ou módulos relacionados
- Mudanças recentes em áreas relevantes

## Fase 2: Coleta Estruturada de Informações

Use **AskUserQuestion** para coletar informações de forma eficiente em lote. Cada chamada pode fazer até 4 perguntas.

### Rodada 1: Requisitos Principais (4 perguntas)

```json
{
  "questions": [
    {
      "question": "Qual é o objetivo principal deste recurso?",
      "header": "Objetivo",
      "multiSelect": false,
      "options": [
        { "label": "Nova Funcionalidade", "description": "Adicionar capacidade totalmente nova ao sistema" },
        { "label": "Melhoria", "description": "Melhorar ou estender recurso existente" },
        { "label": "Correção de Bug", "description": "Corrigir comportamento incorreto ou problema" },
        { "label": "Refatoração", "description": "Melhorar qualidade do código sem alterar comportamento" }
      ]
    },
    {
      "question": "Quem são os usuários primários deste recurso?",
      "header": "Usuários",
      "multiSelect": true,
      "options": [
        { "label": "Usuários Finais", "description": "Clientes externos usando o produto" },
        { "label": "Admins", "description": "Administradores internos ou operadores" },
        { "label": "Desenvolvedores", "description": "Outros desenvolvedores usando APIs ou SDKs" },
        { "label": "Sistema", "description": "Processos automatizados ou jobs em background" }
      ]
    },
    {
      "question": "Qual é o escopo esperado deste recurso?",
      "header": "Escopo",
      "multiSelect": false,
      "options": [
        { "label": "Pequeno (1-2 dias)", "description": "Componente único, mudanças limitadas" },
        { "label": "Médio (3-5 dias)", "description": "Múltiplos componentes, complexidade moderada" },
        { "label": "Grande (1-2 semanas)", "description": "Preocupações transversais, mudanças significativas" },
        { "label": "Incerto", "description": "Precisa explorar mais para estimar" }
      ]
    },
    {
      "question": "Há prazos ou restrições difíceis?",
      "header": "Cronograma",
      "multiSelect": false,
      "options": [
        { "label": "Urgente", "description": "Precisa disso ASAP, em dias" },
        { "label": "Esta Sprint", "description": "Deve ser feito dentro da sprint atual" },
        { "label": "Flexível", "description": "Sem prazo duro, qualidade sobre velocidade" },
        { "label": "Apenas Planejamento", "description": "Apenas projetando agora, implementando depois" }
      ]
    }
  ]
}
```

### Rodada 2: Requisitos Técnicos (4 perguntas)

```json
{
  "questions": [
    {
      "question": "Quais camadas do sistema este recurso irá tocar?",
      "header": "Camadas",
      "multiSelect": true,
      "options": [
        { "label": "Modelo de Dados", "description": "Schema de banco de dados, modelos, migrations" },
        { "label": "Lógica de Negócio", "description": "Services, lógica de domínio, regras" },
        { "label": "API", "description": "Endpoints REST/GraphQL, contratos" },
        { "label": "UI", "description": "Componentes frontend, interface do usuário" }
      ]
    },
    {
      "question": "Quais são os requisitos-chave de qualidade?",
      "header": "Qualidade",
      "multiSelect": true,
      "options": [
        { "label": "Alto Desempenho", "description": "Deve lidar com alto volume ou ser muito rápido" },
        { "label": "Segurança Forte", "description": "Dados sensíveis, autenticação, controle de acesso" },
        { "label": "Alta Confiabilidade", "description": "Não pode falhar, precisa de redundância" },
        { "label": "Fácil Manutenção", "description": "Precisa ser facilmente entendido e modificado" }
      ]
    },
    {
      "question": "Como os erros devem ser tratados?",
      "header": "Erros",
      "multiSelect": false,
      "options": [
        { "label": "Falhar Rápido", "description": "Parar imediatamente em qualquer erro" },
        { "label": "Degradação Graciosa", "description": "Continuar com funcionalidade reduzida" },
        { "label": "Retry & Recuperação", "description": "Retry automático com lógica de recuperação" },
        { "label": "Dependente do Contexto", "description": "Estratégias diferentes para casos diferentes" }
      ]
    },
    {
      "question": "Qual abordagem de teste é preferida?",
      "header": "Testes",
      "multiSelect": false,
      "options": [
        { "label": "TDD (Recomendado)", "description": "Escrever testes primeiro, depois implementação" },
        { "label": "Teste Depois", "description": "Implementar primeiro, adicionar testes depois" },
        { "label": "Testes Mínimos", "description": "Apenas testes de caminho crítico" },
        { "label": "Sem Testes", "description": "Pular testes para este recurso" }
      ]
    }
  ]
}
```

### Rodada 3: Integração & Dependências (4 perguntas)

```json
{
  "questions": [
    {
      "question": "Este recurso precisa de integrações externas?",
      "header": "Integrações",
      "multiSelect": true,
      "options": [
        { "label": "Banco de Dados", "description": "Novas tabelas, queries ou migrations" },
        { "label": "APIs Externas", "description": "Chamadas de serviços de terceiros" },
        { "label": "Message Queue", "description": "Processamento assíncrono, eventos" },
        { "label": "Nenhuma", "description": "Nenhuma integração externa necessária" }
      ]
    },
    {
      "question": "Há dependências de outros recursos ou times?",
      "header": "Dependências",
      "multiSelect": true,
      "options": [
        { "label": "Sistema de Autenticação", "description": "Autenticação ou autorização de usuário" },
        { "label": "Outros Recursos", "description": "Depende de recursos em desenvolvimento" },
        { "label": "Time Externo", "description": "Precisa de input de outro time" },
        { "label": "Nenhuma", "description": "Recurso totalmente independente" }
      ]
    },
    {
      "question": "Como devemos lidar com compatibilidade retroativa?",
      "header": "Compat",
      "multiSelect": false,
      "options": [
        { "label": "Deve Manter", "description": "Não pode quebrar clientes existentes" },
        { "label": "Versionar API", "description": "Criar nova versão, deprecate a antiga" },
        { "label": "Breaking OK", "description": "Pode fazer mudanças incompatíveis" },
        { "label": "Não Aplicável", "description": "Novo recurso, sem usuários existentes" }
      ]
    },
    {
      "question": "Que documentação é necessária?",
      "header": "Docs",
      "multiSelect": true,
      "options": [
        { "label": "Docs de API", "description": "Documentação de endpoint" },
        { "label": "Guia do Usuário", "description": "How-to para usuários finais" },
        { "label": "Guia de Dev", "description": "Detalhes de implementação técnica" },
        { "label": "Nenhuma", "description": "Nenhuma documentação necessária" }
      ]
    }
  ]
}
```

### Rodada 4: Perguntas Esclarecedoras (Dependente do Contexto)

Com base em respostas anteriores, faça perguntas de acompanhamento. Exemplos:

**Se camada UI selecionada:**
```json
{
  "questions": [
    {
      "question": "Qual framework/abordagem UI devemos usar?",
      "header": "Tech UI",
      "multiSelect": false,
      "options": [
        { "label": "React", "description": "Componentes React com hooks" },
        { "label": "Vue", "description": "Componentes Vue.js" },
        { "label": "Server-Side", "description": "Templates HTML renderizados no servidor" },
        { "label": "Padrão Existente", "description": "Seguir convenções do projeto atual" }
      ]
    }
  ]
}
```

**Se Segurança Forte selecionada:**
```json
{
  "questions": [
    {
      "question": "Que medidas de segurança são necessárias?",
      "header": "Segurança",
      "multiSelect": true,
      "options": [
        { "label": "Validação de Entrada", "description": "Sanitização rigorosa de entrada" },
        { "label": "Rate Limiting", "description": "Prevenir abuso e DoS" },
        { "label": "Audit Logging", "description": "Rastrear todas as ações sensíveis" },
        { "label": "Criptografia", "description": "Criptografar dados em repouso/trânsito" }
      ]
    }
  ]
}
```

## Fase 3: Exploração de Abordagens

Após coletar requisitos, proponha 2-3 abordagens:

```markdown
## Opções de Abordagem

### Opção A: [Nome] (Recomendada)
**Vantagens:** ...
**Desvantagens:** ...
**Melhor para:** ...

### Opção B: [Nome]
**Vantagens:** ...
**Desvantagens:** ...
**Melhor para:** ...

### Opção C: [Nome]
**Vantagens:** ...
**Desvantagens:** ...
**Melhor para:** ...
```

Use AskUserQuestion para confirmar abordagem:

```json
{
  "questions": [
    {
      "question": "Qual abordagem você gostaria de prosseguir?",
      "header": "Abordagem",
      "multiSelect": false,
      "options": [
        { "label": "Opção A (Recomendada)", "description": "Resumo breve da abordagem A" },
        { "label": "Opção B", "description": "Resumo breve da abordagem B" },
        { "label": "Opção C", "description": "Resumo breve da abordagem C" }
      ]
    }
  ]
}
```

## Fase 4: Apresentação do Design

Apresente o design em seções (300-500 palavras cada), valide após cada:

1. **Visão Geral da Arquitetura** - Estrutura de alto nível
2. **Modelo de Dados** - Entidades, relacionamentos, schema
3. **Design de API** - Endpoints, requisição/resposta
4. **Design de Componentes** - Módulos internos, interfaces
5. **Tratamento de Erros** - Casos de erro, estratégias de recuperação
6. **Estratégia de Testes** - O que e como testar

Após cada seção, use AskUserQuestion:

```json
{
  "questions": [
    {
      "question": "Esta seção parece correta?",
      "header": "Revisão",
      "multiSelect": false,
      "options": [
        { "label": "Parece Bom", "description": "Continuar para próxima seção" },
        { "label": "Pequenas Mudanças", "description": "Pequenos ajustes necessários" },
        { "label": "Revisão Grande", "description": "Mudanças significativas necessárias" },
        { "label": "Dúvidas", "description": "Preciso de esclarecimento antes de prosseguir" }
      ]
    }
  ]
}
```

## Fase 5: Documentação & Tarefas

### Salvar Documento de Design

Escreva em `docs/designs/AAAA-MM-DD-<topico>-design.md`:

```markdown
# Recurso: [Nome]

## Resumo
[Breve descrição]

## Requisitos
[Das respostas da Fase 2]

## Arquitetura
[Da Fase 4]

## Tarefas de Implementação
[Checklist de tarefas]
```

### Gerar Tarefas de Implementação

```markdown
## Tarefas de Implementação

- [ ] **Título da Tarefa** `priority:1` `phase:model` `time:15min`
  - files: src/file1.py, tests/test_file1.py
  - [ ] Escrever teste falhando para X
  - [ ] Rodar teste, verificar que falha
  - [ ] Implementar código mínimo
  - [ ] Rodar teste, verificar que passa
  - [ ] Commit

- [ ] **Outra Tarefa** `priority:2` `phase:api` `deps:Título da Tarefa` `time:10min`
  - files: src/api.py
  - [ ] Escrever teste falhando
  - [ ] Implementar e verificar
  - [ ] Commit
```

## Fase 6: Handoff de Execução

```json
{
  "questions": [
    {
      "question": "Como você gostaria de prosseguir com a implementação?",
      "header": "Próximo Passo",
      "multiSelect": false,
      "options": [
        { "label": "Executar Agora", "description": "Rodar /feature-pipeline nesta sessão" },
        { "label": "Nova Sessão", "description": "Iniciar sessão fresca para implementação" },
        { "label": "Depois", "description": "Salvar design, implementar manualmente depois" },
        { "label": "Revisar Design", "description": "Voltar e modificar o design" }
      ]
    }
  ]
}
```

## Princípios-Chave

- **Fazer lotes de perguntas eficientemente** - Use todos os 4 slots de perguntas quando apropriado
- **Usar multiSelect para opções não-exclusivas** - Camadas, recursos, requisitos
- **Usar seleção única para decisões** - Abordagem, cronograma, estratégia
- **Marcar recomendações** - Adicionar "(Recomendado)" às opções preferidas
- **Refinamento progressivo** - Perguntas gerais → Perguntas específicas
- **Validar incrementalmente** - Verificar compreensão em cada fase
- **YAGNI ruthlessly** - Remover recursos desnecessários dos designs