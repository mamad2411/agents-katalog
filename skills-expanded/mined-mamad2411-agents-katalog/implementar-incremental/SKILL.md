---
name: implementar-incremental
description: "Implementa em thin vertical slices — uma fatia funcional por vez, ciclo TDD por fatia, limite de cerca de 100 linhas antes de testar e feature flags para trabalho incompleto. Use quando qualquer dev vai construir uma feature de forma incremental."
author: "Pedro Andriow (https://github.com/Andriow)"
---

# Skill: implementar-incremental

Implementar features em fatias verticais completas e funcionais — uma de cada vez, testada, verificada e commitada antes de iniciar a próxima. Nunca implementar tudo de uma vez e testar no final.

**Agente:** `dev-backend`, `dev-bff`, `dev-frontend`, `dev-mobile`  

---

## Quando usar

- Ao iniciar implementação de qualquer feature
- Quando a tarefa envolve mais de 3 arquivos
- Sempre que houver risco de "implementação em bloco com testes no final"

---

## Processo

### Passo 1 — Definir a fatia
Identificar o menor incremento de valor testável. Uma fatia válida é exatamente uma das seguintes:
- Um endpoint funcionando de ponta a ponta
- Um componente renderizando com dados reais
- Uma query retornando dado real do banco

Fatias do tipo L (grande: mais de 5 arquivos, mais de uma feature) não são válidas e devem ser quebradas em fatias menores antes de continuar.

| Tamanho | Critério | Válida? |
|---|---|---|
| S | 1–2 arquivos, 1 endpoint ou 1 componente | Sim |
| M | 3–5 arquivos, 1 feature completa com validação | Sim |
| L | Mais de 5 arquivos, mais de uma feature | Não — quebrar antes de continuar |

### Passo 2 — Escrever o teste que define "concluído" (TDD)
Antes de escrever qualquer código de implementação, escrever o teste que define o critério de aceite da fatia. O teste deve falhar agora e passar ao final do passo 3. Isso força clareza sobre o que "pronto" significa.

### Passo 3 — Implementar apenas o necessário
Escrever somente o código que faz o teste do passo 2 passar — nada além. Sem antecipar próximas fatias, sem scaffolding para o futuro, sem abstrações não utilizadas agora.

Limite operacional: se chegou em 100 linhas sem conseguir rodar os testes, parar imediatamente e testar o que existe. Se os testes não passam com 100 linhas, a fatia está grande demais — quebrar.

### Passo 4 — Verificar
Antes de commitar, confirmar todos os itens:
- Testes da fatia atual passam
- Build está limpo (sem erros de compilação)
- Nenhuma regressão nos testes existentes
- O projeto compila e roda localmente

Nunca deixar o projeto em estado que não compila entre fatias.

### Passo 5 — Commitar
Commitar com mensagem descritiva da fatia concluída. O commit deve ser revertível de forma independente sem quebrar outras fatias. Se o trabalho ainda está incompleto mas precisa ser integrado, usar feature flag para proteger o código incompleto.

Formato de mensagem sugerido: `feat: <o que a fatia entrega>` — ex: `feat: endpoint GET /pedidos retorna lista paginada`

### Passo 6 — Iniciar a próxima fatia
Voltar ao passo 1 com a próxima fatia. Repetir o ciclo completo. Não iniciar a próxima fatia sem o commit da anterior.

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "Vou implementar tudo e testar no final, é mais rápido" | Não é. Bugs encontrados no final custam 10x mais para corrigir do que bugs encontrados na fatia. E o build quebrado bloqueia todos. |
| "Essa fatia é muito pequena para commitar" | Não existe fatia pequena demais. Commits pequenos tornam bisect trivial e rollback seguro. |
| "Preciso do scaffolding inteiro antes de testar qualquer coisa" | Se você não consegue testar nada sem o scaffolding inteiro, a arquitetura está acoplada demais — esse é o sinal do problema real. |
| "Feature flags são overhead" | Feature flag leva 10 linhas. Deploy de código incompleto que quebra produção leva horas de rollback. |
| "Vou refatorar depois, agora vou só colocar tudo junto" | Refatorar código sem testes é reescrever sem rede de segurança. A fatia inclui escrever o teste antes. |

---

## Anti-padrões bloqueados

- Commitar código que não compila — nunca, mesmo que seja "temporário"
- Abrir PR com múltiplas fatias não relacionadas num único commit
- Escrever testes depois da implementação como formalidade (mock que apenas confirma o que o código já faz)
- Implementar camadas inteiras (toda a camada de repositório) antes de qualquer camada superior funcionar
- Usar "vou testar manualmente" como substituto para teste automatizado da fatia
- Deixar o branch em estado quebrado no final do dia com intenção de "arrumar amanhã"

---

## Checklist de conclusão

- [ ] A fatia foi definida com critério claro de "pronto" antes de qualquer código
- [ ] O teste da fatia foi escrito antes da implementação
- [ ] O teste falha antes da implementação e passa após
- [ ] Nenhum código foi escrito além do necessário para o teste passar
- [ ] O build está limpo e sem erros de compilação
- [ ] Nenhuma regressão nos testes existentes
- [ ] A fatia foi commitada com mensagem descritiva
- [ ] Código incompleto que foi integrado está protegido por feature flag
- [ ] A próxima fatia só foi iniciada após o commit da anterior
