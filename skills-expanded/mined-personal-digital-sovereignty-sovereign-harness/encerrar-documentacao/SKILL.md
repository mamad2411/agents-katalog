---
name: encerrar-documentacao
description: Mantém o ciclo documental ao concluir, descartar ou reabrir uma entrega, fase, gap ou decisão. Sincroniza PENDING, ROADMAP, CONCLUSION e referências e publica a unidade encerrada na linha principal, provando que chegou lá, sem apagar evidências nem fechar escopo não validado.
---

# Encerrar a unidade realmente entregue

Leia a política documental do projeto. Identifique a unidade exata: uma fase pode
terminar enquanto o épico continua aberto; implementação não aceita ADR por si.

1. Confira evidências executadas e commits/PRs, limitações e trabalho remanescente.
2. Atualize o documento de origem com resultado, data e links; preserve contexto
   e decisões. Resolvido ou descartado continua na mesma categoria e com o mesmo ID.
3. Remova de PENDING somente o trabalho encerrado. Pendência residual mantém
   descrição concreta, responsável/dependência e próximo passo.
4. Registre o desfecho em CONCLUSION com evidência e commit/PR. Atualize ROADMAP
   apenas quando a entrega mudar sequência, prioridade ou dependência. Atualize
   CHANGELOG no escopo correspondente.
5. Confira os links épico ↔ ADR e gap → origem/resolução. Rejeição/substituição
   de decisão preserva motivo e autoridade segundo a política vigente. Documento
   já citado fora do repositório que muda de lugar ganha registro origem → destino;
   a referência histórica não se reescreve.
6. Rode os verificadores documentais, inclusive os que cruzam repositórios quando
   o projeto os tiver, e confira o diff antes de commitar.
7. Publique e prove. Commit em branch não é entrega: a unidade encerrada entra na
   linha principal no mesmo passo — o que está em curso fica na branch, o que
   fechou não espera o épico. Prove com `git merge-base --is-ancestor <commit> main`
   e confira o quadro (`quadro.sh saude`, quando o projeto o usa): branch já
   publicada é apagada com prova, entrada concluída sai de "Em andamento".

Reabertura é novo evento apontando para o histórico, com motivo e evidência;
nunca apagar conclusão antiga para fazer parecer que o item sempre esteve aberto.
Não inventar teste executado, aceite humano, prazo, versão ou suporte linguístico.
Antes de declarar encerrado, a pergunta não é "commitei?", é "está na main?".
