# Master Publication

## Overview

Produção publica uma **Release Candidate congelada e previamente homologada em staging**. A RC é artefato técnico, nunca issue/task agregadora, e contém de 1 a 5 tasks.

Leia antes: `shared-github-github-flow/SKILL.md`, `shared-github-release-candidate/SKILL.md` e `shared-github-conflict-resolution/SKILL.md`.

## Pré-requisitos

1. Branch `rc/X.Y.Z-rc.N` existente.
2. `.release/rc-manifest.json` válido, `frozen: true`, com 1..5 tasks e SHAs completos.
3. A mesma RC foi homologada em staging com build/smokes aplicáveis.
4. Todas as tasks da RC foram autorizadas pelo humano em `Deploy`.
5. HEAD, SHAs e gitlinks continuam idênticos aos homologados.
6. Nenhum commit entrou na RC depois do snapshot homologado.

## Publicação

1. Releia o manifesto homologado e compare com a RC atual.
2. Confirme `baseMaster`. Se master mudou desde a montagem e a divergência puder alterar a composição, gere nova RC sobre master atual e re-homologue.
3. Confirme que cada repositório/submódulo aponta para o SHA homologado.
4. Confirme ausência de downgrade silencioso de gitlink.
5. Confirme build, browser/smoke, API/Postman e regressão exigidos para a RC.
6. Promova `rc/X.Y.Z-rc.N` diretamente para `master` por merge/PR conforme a proteção. **Nunca use `staging` como origem.**
7. O resultado em master deve representar o mesmo snapshot homologado; composição diferente falha fechado.
8. Gere a tag estável `vX.Y.Z` somente depois da promoção verde.
9. Rode smokes pós-deploy e registre o SHA anterior para rollback determinístico.
10. Manager decide o estado final de cada task individual.

## Dependencias de pacotes

Dependencias ControleOnline em composer.json e package.json devem usar uma
versao numerica exata X.Y.Z ja publicada no Packagist ou no registry npm.
Referencias de branch, aliases, Git URLs e repositories Composer customizados
para pacotes ControleOnline bloqueiam a publicacao. Publique as versoes dos
pacotes primeiro; nunca substitua versoes por branches durante dev, staging ou
master.

## Versão

- `package.json` / `app.json`: `X.Y.Z`.
- Branch técnica: `rc/X.Y.Z-rc.N`.
- Uma RC pode conter até 5 tasks; a versão estável representa o lote homologado.
- Alteração depois do freeze gera `rc.N+1`.

## Fail closed

Bloqueie quando houver manifesto inválido, mais de 5 tasks, task sem autorização Deploy, SHA/gitlink diferente do homologado, teste obrigatório falho, divergência de master que mude a composição, ou origem `staging`, `dev`, `release/*`/agregadora manual.

## Rollback

Antes do merge grave o SHA anterior de cada repositório publicado. Se smoke de produção falhar, reverta para esses SHAs e devolva as tasks ao fluxo de correção/revalidação. Não monte uma nova combinação diretamente em produção.
