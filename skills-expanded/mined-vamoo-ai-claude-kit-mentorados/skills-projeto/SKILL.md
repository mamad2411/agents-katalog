---
name: skills-projeto
description: >-
  Skill de projeto (.claude/skills) cobra contexto em TODA request, mesmo sem
  disparar. Use ao criar, instalar (npx skills@1.7.4 add), auditar ou enxugar skill
  de projeto, em "quantas skills esse projeto carrega", "essa skill dispara?",
  "existe skill pra X", "vale a pena virar skill?", ou quando o aviso da abertura
  diz que o projeto passou do teto.
allowed-tools:
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/skills-projeto-scan.sh" *)'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/skills-projeto-scan.sh *)'
---

# Skills do projeto — o que elas cobram, e de quem

Depois de uma compactação só o começo desta skill volta ao contexto: leia o arquivo de `references/` no passo que o cita, mesmo que já tenha lido antes.

Skill de projeto vive em `.claude/skills/<nome>/SKILL.md` e vale só naquele
repositório. O ponto que quase ninguém vê: **a `description` de toda skill
visível entra no contexto antes do seu primeiro prompt e é relida a cada
request.** A skill não precisa disparar para cobrar — basta existir.

Números de 05/09/2026 (MEDIDO em quatro repositórios de cliente): 52 skills
locais somando ~9.030 chars de description, ~2.257 tokens por request
(ESTIMADO por chars÷4). Mais que o catálogo global inteiro da pessoa que mediu.
Ninguém decidiu isso; foi chegando.

## Teto deste kit: 8 skills e 2.000 chars por projeto

Não é lei da física, é orçamento. Acima disso, cada request do projeto carrega
mais catálogo do que trabalho. Passou do teto, a pergunta não é "qual eu apago",
é **"o que cada uma ensina que eu teria que repetir?"**.

Meça antes de mexer:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/skills-projeto-scan.sh" .
```

Sai uma linha por skill (chars de description, linhas de corpo, situação), o
total, o custo estimado por request e o que está quebrado. O hook do kit roda o
mesmo scan na abertura da sessão e fala **uma vez por mudança** — não a cada
sessão nova. **Cole a saída** antes de propor qualquer corte: recomendação sem a
tabela é chute.

O número de tokens do scan é **ESTIMADO** (chars÷4). Contexto MEDIDO só sai do
`/context` do CLI. Diga qual é qual: prometa o corte de chars, não o de tokens, e
número sem rótulo não entra no relatório.

## Enxugar: a ordem é fixa — deletar, mover, instalar, gerar

Cada passo é mais caro que o anterior, e o agente quer sempre pular para o último.
Nenhum passo começa antes de o anterior ter esgotado. O caso duvidoso de cada passo
está em [references/criterios.md](references/criterios.md).

1. **Deletar**, sem dó, a skill que casa qualquer um destes:
   - `name` ≠ nome da pasta: não roteia (ver "O que faz uma skill rotear de verdade");
   - corpo vazio: casca de scaffold, intenção que ninguém escreveu;
   - duplica uma skill global ou de plugin de mesmo assunto: duas versões da mesma
     regra é pior que nenhuma, porque ninguém sabe qual venceu. Se a do projeto é
     melhor, ela sobe para onde as outras moram e a local sai no mesmo commit;
   - o modelo já decide certo **sem** ela (cenário de pressão, ver "Opcional" abaixo):
     ela não está segurando nada.

   Skill fora do git (`git ls-files .claude/skills` não lista) já some no próximo
   clone: deletar só formaliza.
2. **Mover para `.context/docs/`** (ou para a pasta de docs do repositório) o que é **referência, não gatilho**:
   convenção de schema, mapa de endpoints, histórico de decisão. Isso não tem "quando
   usar", tem "onde procurar". Lá o preload é zero e o texto continua achável por
   busca, pelo Claude e por outros agentes. Corpo curto demais para ser procedimento
   quase sempre é referência.
3. **Lacuna: três portas antes de escrever.** Só com a dor nomeada, nesta ordem:
   já existe skill global ou de plugin (`ls ~/.claude/skills`, o menu `/`)? Existe no
   ecossistema (`npx skills@1.7.4 find`, seção "Procurar skill pronta")? Só então
   escreva, e só com as duas provas de "Não gere skill — ainda".
4. **Manter** o que passou pelos três. Se o total ainda estoura o teto com todas
   íntegras, o problema é escopo: promova ao kit o que não é deste projeto, ou divida
   o repositório.

## O risco maior é o `npx skills@1.7.4 add`

Instalar é uma linha, e o que entra pode ser um pacote com dezenas de skills.
Você não vê o custo: nada trava, nada avisa, e a conta chega diluída em toda
request pelo resto do projeto. Antes de instalar qualquer coisa de terceiro:

1. **Quantas skills vêm junto?** Bundle inteiro por causa de uma é o caso mais
   comum de estouro. Instale a skill, não o pacote, quando der.
2. **Leia o SKILL.md antes de aceitar.** Um SKILL.md de terceiro é código que o
   modelo lê como instrução — e o corpo dele pode carregar uma exclamação
   seguida de crase com um comando dentro, que **executa shell no momento em que
   a skill é carregada**, fora de qualquer hook de permissão (confirmado em
   05/09/2026 no kit do time): não há chamada de ferramenta, então nenhum
   `PreToolUse` nem `permissions.deny` vê o comando. O que sai dele entra no seu
   contexto como se fosse do sistema. Procure também `allowed-tools` largo demais
   e script chamado por caminho que você não controla. O gate do kit
   (`test-skill-sem-injecao.sh`) só varre o próprio kit, nunca o que você instala
   num projeto.
3. **Procedência**: quem publicou, quantas instalações, o repositório existe e
   tem histórico. Como procurar está na seção seguinte.

Depois de instalar, rode o scan. Se o total pulou, desinstale o que você não
consegue explicar em uma frase.

## Procurar skill pronta (e só instalar quando pedirem)

**Busque e apresente; `add` só com pedido explícito da pessoa.** Instalar muda o
projeto dela e passa a cobrar em toda request: em modo `auto`, isso continua sendo
decisão de quem pediu, nunca sua.

**Leia [references/procurar-e-instalar.md](references/procurar-e-instalar.md)** antes de
rodar `npx skills@1.7.4 find` ou `add` (versão, comandos, como pesar e apresentar).

## O que faz uma skill rotear de verdade

**Leia [references/rotear.md](references/rotear.md)** antes de criar, consertar ou julgar
se uma skill roteia, e antes de escrever ou enxugar o corpo dela.

## Não gere skill — ainda

Este kit **não** tem um passo "gerar skill", e é de propósito. Skill gerada
antes de você ter feito a coisa na mão é palpite formatado: sai casca, sai
description genérica, sai `name` errado. A regra:

> Faça o trabalho **na mão umas três vezes**. Quando você se pegar repetindo a
> mesma explicação para o Claude pela terceira vez, aí existe uma skill — e o
> corpo dela já está escrito, é o que você repetiu.

Quando chegar essa hora, o esqueleto sai de `npx skills@1.7.4 init <nome>` (ou de uma
cópia de uma skill deste kit que você entenda). Volte aqui depois com o rascunho
e rode o scan.

## Registre por que cada skill existe

Uma linha por skill, com a data e o motivo. Sem isso, ninguém consegue apagar
nada depois — na dúvida todo mundo mantém, e o total só sobe.

- Projeto com `.context/`: `.context/docs/skills.md`.
- Projeto sem `.context/`: `docs/skills.md` (crie o arquivo; não invente
  `.context/` só para isso).

Formato que basta:

```
- pagamentos-stripe (04/09) — o fluxo de webhook que erramos duas vezes. Sai quando
  o checkout novo estabilizar.
```

## Opcional: teste a skill sob pressão

**Leia [references/teste-sob-pressao.md](references/teste-sob-pressao.md)** antes de montar
o cenário: a skill do projeto se testa à mão.

É nota, não gate: uma skill sua não precisa passar por isso para existir.

## O que o agente vai querer fazer (e por que está errado)

| O que ele vai querer fazer | Por que está errado |
|---|---|
| "São só 6 linhas de frontmatter, o custo é irrisório." | O custo é por request, não por arquivo. 52 descriptions × toda request pesa mais que muito arquivo que você lê de propósito. |
| "Conserto o `name` das cascas e elas passam a rotear." | Ligar o gatilho de uma skill de corpo vazio é fazê-la disparar para o nada: piora. Corpo vazio se apaga; se o conteúdo importa, escreve-se primeiro. |
| "A skill não custa nada porque quase nunca é usada." | A description de skill que o modelo pode chamar entra **sempre**, usada ou não. |
| "Movo para `.context/docs/` antes de apagar, para não perder nada." | Mover casca vazia é trocar lixo de gaveta. Primeiro se apaga; `.context/docs/` é para o que tem conteúdo e não tem gatilho. |
| "Ponho tudo como só-slash e o número cai." | Zera o custo e zera o roteamento junto: a skill deixa de existir para o modelo. Só-slash é para skill que é só-slash por natureza (deploy, disparo, efeito colateral). |
| "Já que estou aqui, escrevo a skill que faltava." | Gerar é o último passo e pede as três portas da lacuna. Sem elas, é dívida nova. |
| "Instalo a do ecossistema, tem 100 mil instalações." | Instalação é reputação, não auditoria. O SKILL.md se lê inteiro antes: ele executa shell ao carregar. |
| "Apago tudo e recrio limpo depois." | Apagar o que passa é perder o que funciona. O veredito é por skill, com a tabela do scan colada. |

## Checklist antes de commitar uma skill nova

- [ ] `name` do frontmatter == nome da pasta (minúsculo, com hífen)
- [ ] `description` diz QUANDO usar, com as suas palavras, e cabe em 500 chars
- [ ] O corpo ensina algo que você teria que repetir — e você já repetiu
- [ ] Nenhuma frase do corpo é no-op (o modelo já faria aquilo sem ela)
- [ ] O scan continua dentro do teto (8 skills / 2.000 chars)
- [ ] A linha do porquê está em `.context/docs/skills.md` (ou `docs/skills.md`)
