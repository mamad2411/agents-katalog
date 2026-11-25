---
name: task-governance
description: Configure task ownership, review, monitoring, and approval according to the ControleOnline agent hierarchy.
---

# Governança de tasks

Use esta skill em toda criação, encaminhamento ou reabertura de task. Resolva a
hierarquia atual pelos agentes e pelo campo `reportsTo`; não presuma nomes ou
IDs se o cadastro tiver mudado.

## Papéis obrigatórios

Para cada task, configure os papéis disponíveis na plataforma nesta ordem:

1. **Revisor:** o superior imediato do agente responsável pela task.
2. **Monitor:** o CTO sempre que o responsável estiver abaixo do CTO na
   hierarquia, independentemente da profundidade da cadeia.
3. **Aprovador:** QA para task de Developer; Manager para task de qualquer
   outro agente que esteja abaixo do Manager.

Task de Developer é a task criada ou encaminhada para o agente cujo papel é
`Developer`; quando houver dúvida, use o agente responsável como critério
canônico. Task de outro papel segue a regra do segundo caso acima.

O agente no topo da hierarquia não recebe revisor automático. Para tasks do
próprio Manager ou do próprio CTO, use o superior existente na cadeia como
revisor; não invente um aprovador quando a regra de aprovação não se aplicar.

## Manager: encaminhar antes de executar

O Manager coordena, prioriza e distribui. Depois de identificar a primeira
prioridade elegível e executável:

- procure primeiro o agente subordinado adequado;
- se puder atribuir, atribua a task, configure revisor, monitor e aprovador, e
  registre o encaminhamento;
- não implemente a task como se fosse Developer, QA, Security, Design, UX ou
  DevOps quando houver subordinado elegível;
- se não puder atribuir por falta de permissão, agente elegível ou mecanismo de
  atribuição disponível, execute a ação necessária sob o papel de Manager e
  registre a razão objetiva;
- atribuir não encerra a task: confirme a atribuição e mantenha o estado da
  task coerente com o trabalho realmente iniciado.

A prioridade continua sendo definida pelo fluxo canônico: resolver trabalho
pendente e bloqueios reais antes de capturar uma nova task. Não crie estados ou
labels de bloqueio apenas para representar uma falha de encaminhamento.

## Verificação antes da conclusão

Antes de concluir a criação ou o encaminhamento, releia a task e confirme:

- responsável correto;
- revisor igual ao superior imediato;
- CTO como monitor quando o responsável estiver abaixo dele;
- QA como aprovador para Developer;
- Manager como aprovador para os demais agentes abaixo dele;
- nenhuma atribuição ou aprovação foi declarada sem leitura de retorno da
  plataforma.

Se a plataforma não oferecer um campo específico, registre o papel exigido no
handoff ou metadado operacional disponível, sem substituir a regra por texto
solto em instruções da task.
