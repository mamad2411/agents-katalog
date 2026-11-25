---
name: vies-de-plausibilidade
description: Contramedidas para o erro que um LLM produz por construção — gerar a saída mais PLAUSÍVEL e tratá-la como verificada. Cobre edição destrutiva de arquivo, documento tratado como verdade sobre o código, primeiro diagnóstico convincente, filtro de saída que mascara falha, correção que piora, e ausência de sinal lida como prova. Carregar antes de reescrever trecho de arquivo longo, antes de afirmar causa raiz, antes de confiar num comando que resume saída de teste/build, e antes de declarar qualquer coisa verificada.
---

# Plausível não é verificado

Um modelo de linguagem produz a continuação mais provável. A saída errada mais provável é, por construção, a que mais parece certa. Esta skill trata do mecanismo que atravessa todos os domínios: nada estoura, o diff parece bom, o log diz o que você esperava, e está errado.

Cada classe abaixo tem origem num incidente real do projeto que deu origem a este método.

## 1. Edição por intervalo apaga o que está no meio

Nunca reescreva com `s[:ini] + novo + s[fim:]` usando duas âncoras: tudo entre elas some, inclusive seções que você não sabia que existiam. Caso de origem: a reescrita de uma seção do roadmap engoliu outra seção inteira que vivia entre as âncoras; só apareceu horas depois.

- Use `replace(antigo, novo, 1)` com `assert antigo in s` — falha alto se o alvo mudou.
- Confira a contagem de TODAS as âncoras antes de aplicar qualquer uma.
- Depois de reescrita estrutural, compare a lista de títulos (ou de funções) com o git:
  `diff <(git show HEAD:arq.md | grep -E '^#{2,3} ') <(grep -E '^#{2,3} ' arq.md)`.
- `replace(a, b, 1)` pega a PRIMEIRA ocorrência — use âncora com 2-3 linhas de contexto.

## 2. Comentário e documento não são fonte de verdade sobre o código

O texto ao lado do código envelhece sem avisar, e a generalização ("todos os N fazem X") é a forma mais plausível de escrever uma decisão. Caso de origem: um registro dizia "3 papéis"; o `grep` devolveu 21 call sites. Uma ADR afirmava uma política única; a contagem mostrou três, cada uma com motivo.

- Antes de agir sobre o que um comentário/roadmap afirma, confirme no código.
- Nunca escreva "todos", "sempre", "os N" sem ter rodado a contagem — e cole o comando na decisão.
- Se o texto estava errado, corrija-o no mesmo commit e diga que estava errado.

## 3. O primeiro diagnóstico convincente é o mais perigoso

Caso de origem: suíte E2E instável, diagnóstico óbvio "paralelismo". Testado: `workers: 1` piorou. A causa real era o serviço degradando após horas de carga.

- Formule a hipótese E o teste que a refutaria antes de implementar. Sem teste barato, é palpite.
- Correção que não resolve: suspeite do diagnóstico antes de reforçar a correção.
- Registre a hipótese refutada no código/doc, ou a próxima sessão repete o caminho.

## 4. O filtro que você escreveu para ler a saída pode esconder a falha

Caso de origem: um strip de ANSI que removia só cores leu uma execução com 15 falhas como "80 passed". O certo era `\x1b\[[0-9;]*[A-Za-z]`.

- Cruze dois sinais independentes (sumário textual E contagem de marcadores; exit code E conteúdo).
- `cmd | tail` mascara o exit code: use `${PIPESTATUS[0]}`.
- Resultado bom demais para o que você mudou é motivo para desconfiar do instrumento.
- Antes de declarar verde, rode uma vez sem filtro nenhum e olhe.
- Saída grande de CLI vai para arquivo, não para pipe: há ferramenta que sai antes de esvaziar o buffer e entrega exatamente 65.536 bytes. Caso de origem: um "0 de 24" falso que dependia só de a saída passar por `| sed`.
- O filtro pode estar no próprio gate. Sob `set -o pipefail`, `produtor | grep -q` falha ao acaso: o `grep -q` sai no primeiro acerto, o produtor leva SIGPIPE e o pipeline conta como falha. Caso de origem: num `pre-commit`, `env | grep -q` ignorava a exceção nomeada em 152 de 300 execuções, e `printf "$lista_grande" | grep -q` errou 200 em 200 — um merge grande pularia o gate. O sintoma era um teste "intermitente", e a primeira explicação plausível (disco temporário cheio por outra sessão) chegou a ser registrada. **Ressalva de medição (2026-10-25)**: as taxas são de corrida, não constantes — o mesmo pipeline revalidado deu 0–52/300 e 0–1/30, variando entre execuções; só o caso de lista grande foi determinístico (94 KB com o match na 1ª linha: 50/50). Cite o mecanismo, e cada número como "uma rodada observada". Use here-string (`grep -q padrão <<<"$var"`) ou `case` sobre a variável.

## 5. A correção plausível que piora

Se o sintoma mudou mas não sumiu, reverta o seu próprio fix antes de empilhar o segundo. Fix sobre diagnóstico errado transforma sintoma simples em insolúvel.

Variante pior: a correção escrita com convicção, citando `grep` e linha de arquivo, também errada. As evidências eram compatíveis com a hipótese E com a contrária. Pergunte: **este comando daria este resultado se eu estivesse errado?** Prefira medição comparativa ("0 aqui, 33 ali") a absoluta ("existe X").

## 6. Verifique o efeito, não a aparência do efeito

Caso de origem: um parser de cabeçalho binário parecia certo, os valores batiam com a especificação — e parava um campo cedo, superestimando um cálculo em 7×. Só um arquivo real impresso mostrou. Outro: um `DELETE` respondia `{"status":"deleted"}` sem apagar nada.

- Teste sintético prova borda; dado real prova que você entendeu o formato. Faça os dois.
- Asserte o efeito no disco/servidor, não a tela.

## 7. O script de edição abortou, e o commit foi feito assim mesmo

O `&&` liga o `git add` ao `git commit`, não ao script. Se o script aborta num `assert`, o commit sai com mensagem completa e diff pela metade.

- Nunca encadeie o commit ao script de edição. Rode, olhe, commite.
- Depois de commitar documento: `git show --stat` — o tamanho tem de ser compatível com a mensagem.
- Delimitador de heredoc que não possa aparecer no conteúdo (`FIM_UNICO_XYZ`, não `EOF`).
- `git checkout -- arquivo` para "desfazer o engano" apaga trabalho sem pergunta. Antes: `cp` ou commit WIP.

## 8. O nome plausível dispensou a consulta ao documento que já respondia

Inverso da classe 2: o nome era tão óbvio que ninguém procurou o runbook que já documentava a armadilha. Caso de origem: o binário de um pacote não tinha o nome do pacote; o build morreu depois de compilar tudo — e o runbook descrevia exatamente isso.

- Antes de escrever procedimento para ambiente que você não executa, leia o runbook dele.
- Nome de pacote ≠ nome de binário ≠ nome de serviço. Confirme.
- Script que roda longe de você: verifique todos os pré-requisitos no começo, falhe em segundos.
- Aparência visual: verde em teste não cobre. Diga isso explicitamente.

## 9. A ausência de sinal só vale no contexto que a produziria

Não ver um prompt/erro/log prova que naquele contexto ele não apareceu. Caso de origem: "o app não pede permissão" — testado no mesmo build que já tinha a permissão concedida. Um build novo pediu na hora. Pergunte: o que eu testei geraria o sinal se ele fosse necessário?

## 10. A reprodução "não reproduziu" porque a tentativa anterior mudou o estado

Antes de cada nova tentativa, reconstrua o estado de partida inteiro (processo, arquivo de PID, porta, banco) e confira cada peça. E texto de entrega escrito antes da medição sai no pretérito com a mesma naturalidade de um resultado: releia toda frase "medido/validado" contra o que já rodou.

## Checklist antes de declarar pronto

1. O que afirmo foi medido? Com que comando — e o filtro dele pode mentir?
2. Reescrevi arquivo? Auditei títulos/funções contra o git?
3. Afirmei causa raiz? Qual teste a refutaria, e ele rodou?
4. Algum comentário/doc lido como verdade foi conferido no código?
5. Empilhei fix sobre fix? Reverti o primeiro?
6. Hipótese refutada está registrada?
7. Escrevi procedimento para ambiente que não executo? Li o runbook?
8. A prova daria o mesmo resultado se eu estivesse errado?
9. Repeti uma reprodução? Reconstruí o estado de partida?
