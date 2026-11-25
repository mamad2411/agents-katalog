---
name: corno-revisa
description: Revisão de código pesada e direta sobre estrutura e manutenção de um PR ou branch - arquivo gigante, if espalhado, abstração que não paga o custo, código mágico. Separa o que o PR introduziu do que já era problema antes (que vira só observação), confere o impacto da mudança em quem usa o código mexido e termina com decisões - se o PR é da pessoa, pergunta quais achados corrigir; para qualquer PR, oferece um comentário escrito como gente e publicado pela conta dela. Use quando pedirem "corno revisa", "/corno-revisa", revisão pesada de PR, auditoria de qualidade ou revisão sem dó das mudanças da branch.
disable-model-invocation: true
---

# Corno revisa

Revisão sem dó de um PR ou da branch atual. A pergunta é uma só: a mudança deixou o código mais simples de entender e de mexer, ou só funciona? Seja direto: veredito primeiro, poucos apontamentos com convicção, nenhum enfeite.

## 1. Ache o alvo e o dono

- **PR dito** (número ou link): `gh pr view <n> --json number,title,url,author,baseRefName,headRefName,files` e `gh pr diff <n>`.
- **Sem alvo**: o PR da branch atual (`gh pr view`); sem PR, `git diff $(git merge-base HEAD origin/HEAD)...HEAD` mais o que não foi commitado.
- **De quem é**: compare `author.login` com `gh api user --jq .login`. Sem PR ou sem `gh`, a branch é da pessoa se os commits dela são do `git config user.email`. Isso decide o passo 6.

## 2. Leia o diff e o que ele toca

Leia o diff inteiro e o código em volta. Antes de qualquer ajuste pequeno, procure o movimento grande: uma reorganização que mantém o comportamento e faz partes inteiras sumirem. A melhor solução é a que parece óbvia depois de pronta.

**Regressão.** Para cada função, componente, tipo, rota, query, config ou contrato que o diff mudou, ache quem usa (busca pelo nome, imports, chamadas, testes) e veja se o comportamento muda para eles. Rode os testes desses usuários quando for barato. Anote o resultado nos dois sentidos: o que é afetado (com `arquivo:linha`) e o que você conferiu e não é.

## 3. Revise sem dó

1. **Ambição na simplificação.** Se dá para apagar complexidade em vez de mudar ela de lugar, insista nisso.
2. **Arquivo passando de mil linhas** por causa do PR é problema por padrão. Pergunte se não é hora de separar antes.
3. **If espalhado é defeito de desenho.** Caso especial enfiado num fluxo que não tem nada a ver piora o código mesmo funcionando.
4. **Código direto e sem graça vence código esperto.** Desconfie de mecanismo genérico que esconde uma suposição simples, de embrulho que só repassa, de fallback silencioso que cobre um caso que ninguém entendeu.
5. **Fronteiras claras.** Opcional sem motivo, `any`, cast em cascata e objeto montado na mão onde caberia um tipo de verdade são custo de manutenção.
6. **Lógica na camada certa**, usando o helper que o projeto já tem em vez de um quase igual.
7. **Estado atualizado em partes** que pode ficar pela metade, e trabalho independente feito em fila sem motivo, são defeito de desenho quando a estrutura limpa é óbvia.
8. **Não carimbe "funciona".** Se o comportamento pode ficar igual com estrutura bem melhor, peça a versão melhor.
9. **Meça duas vezes.** Todo apontamento diz o que mudar, onde e por que fica mais simples. Apontamento vago não entra.

Remédios preferidos: apagar uma camada inteira em vez de polir; remodelar o estado para os `if` sumirem; mudar quem é dono do conceito para a funcionalidade virar extensão natural; trocar caso especial por um fluxo padrão; separar orquestração de regra de negócio; usar o helper que já existe. "Renomeia isso" não resolve problema de estrutura.

## 4. Separe o que é do PR do que não é

- **Do PR**: o que as linhas do diff introduziram ou pioraram. Isso pede ajuste ou bloqueia.
- **Observação**: problema que já existia, mudança de arquitetura maior do que o PR, ou coisa de outro lugar. Não bloqueia o PR. Fica anotado com onde está e o que fazer, para outra tarefa.

Se o PR depende de um problema antigo para funcionar, ou o piora, ele passa a ser do PR.

## 5. Responda

```
Veredito: entra | entra com ajustes | precisa repensar, e por quê em uma frase.

Do PR
1. arquivo:linha: o problema. A correção.
2. ...

Impacto
- Afeta: <quem usa o código mexido>, <arquivo:linha>, <o que muda para ele>.
- Conferido sem impacto: <o que você checou e está igual>.

Observações (fora deste PR)
- <onde>: <o problema>. <o que fazer, em outra tarefa>.
```

Movimento grande de simplificação vem primeiro na lista "Do PR", com o código de como ficaria. Do mais grave para o menos grave. Estilo e formatação ficam com o formatador do projeto; bug fino, segurança e desempenho só entram se aparecerem no caminho.

**Barra para aprovar.** Bloqueia até o autor justificar: regressão estrutural, chance óbvia de simplificar muito ignorada, arquivo passando de mil linhas, `if` espalhado, abstração mágica ou embrulho sem função, lógica na camada errada ou helper duplicado.

## 6. Decisões

Use a ferramenta de pergunta com opções do seu agente (no Claude Code, a janela de perguntas); sem ela, uma lista numerada para a pessoa responder.

- **PR da pessoa**: pergunte quais achados "Do PR" ela quer que você corrija, um por opção, com várias escolhas possíveis. Observações não entram como correção aqui. Corrija só o que ela marcar, rode os testes e confira com a `corno-confere` se ela estiver instalada.
- **PR de outra pessoa**: não ofereça mexer no código dela.
- **Comentário no PR, nos dois casos**: pergunte se ela quer um. Se a skill `corno-humano` estiver instalada, use-a para o texto soar como gente. Mostre o texto e onde ele vai (comentário geral ou em linhas específicas) antes de publicar.

**Publicar só com um sim explícito.** O comentário sai pela conta da pessoa no `gh`; diga isso antes. Geral: `gh pr comment <n> --body-file <arquivo>`. Em linhas: `gh api repos/{owner}/{repo}/pulls/<n>/reviews` com `event: COMMENT` e os comentários com `path` e `line`. Nunca aprove nem peça mudanças (`--approve`, `--request-changes`) sem ela pedir isso com essas palavras. Depois de publicar, mande o link.

## Pronto quando

O veredito, os achados do PR com `arquivo:linha`, o impacto conferido e as observações estão na resposta; a pessoa decidiu o que corrigir e se comenta; e o que ela escolheu foi feito e conferido, com o link do comentário quando houver.
