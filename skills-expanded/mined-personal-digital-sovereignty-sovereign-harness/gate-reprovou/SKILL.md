---
name: gate-reprovou
description: Como publicar trabalho sem contornar os gates locais (pre-commit, pre-push, merge gate) — e como distinguir gate que reprovou por defeito do CÓDIGO de gate que reprovou por defeito da PRÓPRIA FERRAMENTA. Carregar antes de qualquer git push, ao ver "PUSH BLOQUEADO" ou "MERGE RECUSADO", e antes de sequer considerar o escape nomeado.
---

# O gate também erra — distinguir isso é o trabalho

Regra do método: **se um gate reprovou, ou o código está errado, ou o gate está errado; as duas coisas se resolvem, não se contornam.** No projeto de origem, numa mesma semana, três reprovações seguidas foram do gate, não do código — e uma foi contornada por hábito antes de diagnosticada.

## Ativação (config local — não viaja no clone)

```bash
git config core.hooksPath .githooks
```

Sem a ativação, o hook fica versionado e inerte naquele clone — por isso ela é passo explícito da instalação. Desligar com `core.hooksPath=/dev/null` nunca é legítimo: é override silencioso, sem rastro.

## Defeitos de ferramenta já medidos (procure a mesma família)

1. **A ferramenta ignora a lista de arquivos.** `cargo fmt --check -- <arquivos>` enumera os targets do crate e checa tudo; o gate "dos arquivos do push" reprovava por dívida antiga. Correto: `rustfmt --edition 2021 --check --config skip_children=true <arquivos>`.
2. **A ferramenta expande a lista.** `rustfmt` atravessa declarações `mod` e checa arquivos fora do push.
3. **A ferramenta não sabe parsear o tipo.** `prettier` sem config que declare o plugin de Svelte acusa `No parser could be inferred` — e componentes nunca foram verificados.
4. **O comando estava errado, e o `|| true` escondia.** `tsc --noEmit` cru não conhece runas do Svelte 5; o certo era `svelte-check`.
5. **Supressão inline com sintaxe errada não suprime.** `# nosemgrep: justificativa` lê a justificativa como id de regra; use `# nosemgrep` puro e justifique na linha de cima.
6. **O resumo filtrado esconde a reprovação.** Confira com o binário que o gate usa, no arquivo específico.

Como provar que a culpa não é sua, antes de qualquer escape: rode a ferramenta do gate só nos seus arquivos. Saída limpa = o defeito é do gate — corrija o gate (e registre).

## Dívida pré-existente: commit separado

Arquivo que você toca já era não-conforme em `main`? Formatar é legítimo, mas em commit próprio (`style(...)`, mecânico, testes verdes) — nunca junto da mudança de comportamento.

## O escape nomeado: quando é legítimo, e o preço

Só depois de diagnosticar que o gate está errado e o código não, e sempre com:

1. registro no arquivo de pendências **no ato**;
2. menção no corpo do PR de qual gate foi pulado e por quê.

Exceção usada sem diagnóstico não é consciente, é hábito. O escape do guard do agente é por regra (nunca `all`).

## Ordem que funciona ao publicar

1. bateria local completa no repositório;
2. `git ls-remote origin main` — confirma autenticação sem escrever nada;
3. push (os gates rodam aqui);
4. PR com o corpo descrevendo validação e gates;
5. **merge gate** (valida o RESULTADO do merge), nunca o merge direto pela plataforma;
6. atualizar `main` local antes do próximo repositório da cadeia.

## Push que fica pendurado depois de "push autorizado"

O `git push` abre a conexão antes de chamar o hook. Gate longo (testes frios disputando CPU) faz o servidor derrubar a conexão ociosa, e o push espera para sempre. Encerre o `git push` e o `ssh` filho pelo PID (nunca `pkill -f`) e repita: o build já está em cache. Não rode dois gates pesados ao mesmo tempo.
