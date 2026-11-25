---
name: handoff
description: >-
  Gera o documento de passagem de bastão de uma sessão ou projeto, para outro
  dev, agente ou você mesmo depois. Template fixo, destino
  durável em .context/docs/handoffs/, âncora de git real e marcação obrigatória
  do que foi verificado versus do que é só crença. Só dispara quando você
  chama: /kit-vamoo:handoff.
disable-model-invocation: true
---

# handoff

Só roda quando a pessoa chama `/kit-vamoo:handoff`: escrever um handoff é decisão de
quem está saindo, nunca do modelo.

## A regra que dá valor ao documento

**Toda afirmação de estado é marcada com como foi provada.**

```
- Ingestão de NF voltou a rodar  [verificado: select count(*) → 1.284 linhas hoje]
- O watchdog cobre esse caso     [acreditado: li o código, não rodei]
```

O motivo é mecânico: **o próximo agente trata o handoff como contrato e não
re-checa nada.** Uma crença escrita como fato vira premissa falsa para tudo que
vier depois — e o custo aparece semanas depois, longe da causa.

Na dúvida entre as duas marcas, use `[acreditado]`. É barato re-verificar; é caro
descobrir que a fundação era suposição.

## Antes de escrever

Colete a âncora com git — não de memória:

```bash
git rev-parse --abbrev-ref HEAD && git rev-parse --short HEAD
git log --oneline -12
git status --short
gh pr list --state open --json number,title,author,mergeable \
  --template '{{range .}}#{{.number}} {{.title}} ({{.author.login}}) {{.mergeable}}{{"\n"}}{{end}}' 2>/dev/null
git worktree list
```

Um handoff sem SHA é um handoff que não dá para conferir depois.

## Onde salvar

`<projeto>/.context/docs/handoffs/YYYY-MM-DD-<slug>.md`

Sem `.context/` no projeto → `docs/handoffs/`. **Nunca no diretório temporário do
sistema**: o handoff que some no reboot é o que você mais vai querer daqui a duas
semanas. Ao terminar, imprima o caminho absoluto — é o que a próxima sessão
recebe.

## Antes de fechar: a memória do projeto

O handoff conta a frente de trabalho. A **memória** guarda o que sobrevive a ela
— e é aqui que ela se publica, porque este é o único momento do fluxo em que
alguém está olhando para trás de propósito.

Quando o projeto tem `.context/memoria/` (a pasta que a skill `memoria-projeto`
liga), o passo é curto:

```bash
git status --short .context/memoria/
```

Numa sessão em worktree, rode o comando também no clone principal (`git -C
<clone-principal> status --short .context/memoria/`): a memória automática é por
repositório e compartilhada entre os worktrees, então o que a sessão registrou cai
no `.context/memoria/` do clone principal, não no do worktree.

O que aparecer aí foi escrito nesta sessão e ainda não está no repositório. Antes
de fechar, passe os olhos em cada arquivo tocado e faça três coisas:

1. **Apague o que se provou errado.** Memória errada é pior que memória faltando:
   ela é lida com confiança e ninguém re-checa. Se a sessão derrubou um fato
   antigo, o arquivo dele sai — não ganha um parágrafo de ressalva.
2. **Marque hipótese como hipótese.** A mesma regra do handoff vale aqui: o que
   foi medido e o que é inferência precisam estar escritos com essas palavras. A
   memória é lida por sessões que não viram nada do que você viu.
3. **Troque data relativa por absoluta.** "Semana passada" não sobrevive a três
   sessões.

Depois, o inverso: o que **este handoff** descobriu e vai valer daqui a um mês não
pode ficar só no handoff — handoff é de uma frente, memória é do projeto. Causa
raiz de incidente recorrente, decisão do cliente que parece bug, armadilha que
custou horas: isso vira arquivo na memória, com link para o handoff.

Publicar é a §4 da skill `memoria-projeto` (branch, conferência de PR de memória já
aberto, script do time se houver), apontando o clone principal. No handoff, cite o PR de
memória em que você commitou e todo PR `misto` que a conferência mostrar: quem assume
precisa saber que tem memória esperando merge.

Sem `.context/memoria/` no projeto, diga no handoff onde a memória mora (ou que
não existe) — a próxima sessão precisa saber se pode confiar em algo além do
documento.

## Política de conteúdo

- **Referencie, não copie.** Spec, plano, ADR, issue, commit e diff entram como
  caminho ou URL. O handoff carrega a linha viva do trabalho, não um arquivo
  morto de tudo.
- **Redija segredo e dado pessoal.** Chave, token, senha, telefone e e-mail de
  cliente não entram — nem "só o começo da chave".
- **Escreva para quem não estava lá.** Quem lê não viu a conversa e não vai
  perguntar. Se depende de contexto que só existe na sessão, o contexto vai junto.
- **Diga o que ignorar.** Doc auto-gerado desatualizado e pasta congelada
  desperdiçam o dia de quem chega. Uma seção de "não use como fonte" costuma valer
  mais que uma de "leia isto".
- **Ordene pendência por custo × risco**, não por área. Quem assume precisa saber
  por onde começar, não como o trabalho é organizado.

## Template

```markdown
# Handoff — <frente ou pessoa>

**Data:** YYYY-MM-DD · **Base:** `<branch>` @ `<sha>` · **De:** <nome> · **Para:** <nome>

<Um parágrafo: o que é isto, e o enquadramento operacional que muda tudo —
"está em produção e é usado todo dia útil", "não existe staging", "o cliente
opera sozinho aos sábados". Se houver uma restrição assim, ela vem antes de
qualquer detalhe técnico.>

## 1. O que é

Tabela: módulo · o que faz · quem usa. Uma linha por módulo que quem assume vai tocar,
não o inventário do repo.

## 2. Acessos necessários

O que pedir, a quem, antes de qualquer coisa. Nunca o valor — só o nome e o dono.

## 3. Rodar local

Comandos exatos. E o que vai assustar e é normal (teste que falha por padrão,
warning conhecido, tsc não estrito). Se `.env.example` está incompleto, diga.

## 4. Como o código está organizado

Só o que não é óbvio pela árvore de diretórios.

## 5. Fluxo de trabalho

Branch, PR, CI, deploy, migrations. **Migrations em destaque se houver ordem
obrigatória** — é onde mais se quebra produção.

## 6. Integrações e por onde elas quebram

Uma linha por integração + o modo de falha já observado.

## 7. O que aconteceu recentemente

Últimas semanas, com PR/SHA. O que mudou e por quê.

## 8. Pendências, na ordem que eu faria

Ordenado por custo × risco:
- **Primeiro** — barato e fecha risco real
- **Depois** — precisa de janela ou decisão
- **Dívida** — produto e técnico
- **Não é código** — depende de gente

Cada item marcado `[verificado: ...]` ou `[acreditado]`.

## 9. Armadilhas conhecidas

Tabela sintoma → causa real. O que custou caro para descobrir.

## 10. Documentação: o que ler e o que ignorar

**Leia, nesta ordem:** ...
**Não use como fonte:** ... (e por quê — auto-gerado, congelado, superado)

## 11. Se der ruim

Cenário de incidente → primeiro comando → quem chamar. Deixe claro o que exige
autorização antes: rotação de segredo, acesso a servidor, decisão com o cliente.

## Skills sugeridas

Quais skills a próxima sessão deve carregar, e para quê.
Ex.: `baseline` (auditar antes de mexer) · `ship` (deploy) ·
`secscan` (revisão de segurança).
```

## Está bom quando

- Cabe em uma fração da conversa que o originou; spec e diff aparecem como
  caminho, não como texto colado.
- Alguém lê **frio**, sem a sessão original, e sabe o que fazer.
- A pessoa que assume começa a trabalhar em vez de pedir para você re-explicar.
- Nenhuma linha afirma estado sem dizer como aquilo foi provado.
- Não tem chave, token, senha nem dado pessoal.
- A memória do projeto saiu junto: o que a sessão escreveu está publicado, o que
  ela derrubou está apagado, e o que ela descobriu de durável virou arquivo lá —
  não só um parágrafo aqui.

## Armadilhas

| Sintoma | Causa real |
|---|---|
| Próximo agente construiu em cima de premissa errada | Crença escrita como fato. A marcação `[verificado]`/`[acreditado]` existe exatamente para isto |
| Handoff sumiu | Foi salvo no diretório temporário. `.context/docs/handoffs/` é versionado |
| Ninguém lê porque tem 40 páginas | Copiou spec e diff em vez de referenciar |
| Doc envelheceu sem ninguém notar | Faltou a âncora `**Base:** <branch> @ <sha>`. Sem ela não há como saber a distância |
| Quem assumiu perdeu um dia em doc obsoleta | Faltou a seção "não use como fonte" |
| Segredo vazou junto | Redação não foi feita. É item de checklist, não de bom senso |
| Fato descoberto com esforço se perdeu depois do handoff | Ficou só no documento da frente. Handoff é de uma frente; memória é do projeto — o durável tem que sair dos dois lados |
| Memória ficou só na máquina de quem saiu | O agente escreve sozinho, mas publicar é passo de gente. Se não sai no handoff, não sai nunca |
| Dois PRs abertos com a mesma memória | O handoff publicou sem olhar o PR de memória que outra sessão já tinha aberto. O `gh pr list` antes de publicar evita |
