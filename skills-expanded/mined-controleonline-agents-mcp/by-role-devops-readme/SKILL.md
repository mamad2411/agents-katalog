# DevOps Skills

No Manager: DevOps e P1; hotfix e P2.

Funcoes P1, nesta ordem:

1. Tasks com `agent:security:accepted` e revalidacao do Manager → montar uma RC congelada de 1 a 5 tasks a partir do master atual → manifesto → **promover/resetar `staging` ate coincidir com o tip da RC** (obrigatorio; a RC e para o humano validar no staging) → **aplicar label `rc/X.Y.Z-rc.N` em cada issue inventariada** → so entao `In Review`.
2. Quando as tasks da RC homologada estiverem em `Deploy` → promover exatamente a mesma RC para `master`, sem alterar SHAs.

A RC e artefato tecnico e nunca uma issue/task agregadora. Branch `rc/*` sem `origin/staging` no mesmo snapshot **nao** conclui a RC. Alterou qualquer SHA ou conteudo depois do freeze: invalide a homologacao e gere `rc.N+1`. Comentario sem promocao a staging nao fecha a funcao.

Gate de staging: `agent:security:accepted` + revalidacao do Manager com testes locais e evidencia da entrega em `dev`.

Depois da promoção, DevOps valida o deploy e o runtime publicado, incluindo o
fluxo afetado e erros relevantes de serviço, e devolve um handoff ao Manager.
DevOps não decide a coluna final, não move para `Done`/`Working` e não cria
filhas documentais.

Todos os agents devem priorizar tasks em `Working` antes de capturar `Ready`,
respeitando o limite atual da coluna lido no Project #1. Para o DevOps, a
ordem e `Deploy` primeiro e depois `Working`; `Ready` so entra quando houver
capacidade. `In Review` só ocorre para tasks inventariadas na RC congelada **e somente apos staging == tip da RC**. `Done` ou `Working`
após uma publicação são decisões do Manager,
com base no aceite de Security e na evidencia local da entrega.
