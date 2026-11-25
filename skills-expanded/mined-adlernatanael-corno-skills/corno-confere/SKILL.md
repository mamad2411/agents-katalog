---
name: corno-confere
description: Agente de IA mente muito dizendo que está pronto. Esta skill é o chicote contra isso - antes de qualquer "pronto", põe lado a lado cada coisa pedida (entrada) e o que foi entregue (saída) e confere se foi feito e do jeito que foi pedido, inclusive o que chegou no meio do trabalho, com prova rodada agora. Confere em duas voltas, a segunda inteira de novo depois das correções, e diz o que falta em vez de "está tudo certo". Use sempre que o agente for dizer "pronto", "feito", "terminei", "corrigi", "funciona", "os testes passam", "done" ou "fixed"; quando a pessoa perguntar "veja se faltou coisa", "faltou algo?", "terminou?", "tá pronto?" ou "confere aí"; e antes de commit, PR, deploy ou de repassar o resultado de outro agente.
---

# Corno confere

**Lei única: nada de "pronto" sem prova de que tudo que foi pedido foi entregue, do jeito que foi pedido, e funciona agora.**

Agente de IA mente muito na hora de dizer que terminou: esquece metade do pedido, entrega parecido em vez de igual, e afirma que funciona sem ter rodado. O corno é o último a saber. Aqui você é o chicote: desconfia do próprio trabalho, confere cada item contra o pedido e só para quando a prova bate. Mudar as palavras para escapar da regra ("deve estar ok", "acho que foi") é quebrar a regra do mesmo jeito.

## 1. Junte tudo que foi pedido

Releia a conversa desde o último "pronto" aceito, ou desde o começo da tarefa. Não só a última mensagem:

- O pedido original e cada mudança de rumo depois dele.
- As mensagens que chegaram enquanto você trabalhava. São as que mais se perdem.
- Os detalhes ditos de passagem ("e tira aquela barra", "deixa preto e branco").
- O que a tarefa exige mesmo sem ser dito: testes que a mudança quebrou, telas que usam o componente mexido, docs e textos que ficaram desatualizados.

Escreva a lista, um item por linha, com as palavras da pessoa. Essa é a **entrada**: o que foi pedido, com os detalhes exatos (texto, nome, valor, cor, lugar, quantidade, formato).

## 2. Ponha entrada e saída lado a lado

Para cada item, escreva ao lado a **saída**: o que você entregou de fato, lido agora no arquivo, na tela ou na resposta, não lembrado. Depois compare:

- **Foi feito?** Existe a mudança.
- **Foi feito do jeito que foi pedido?** O texto é o texto pedido, letra por letra. O lugar é o lugar pedido. "Tira" foi tirado, não escondido. "Deixa preto e branco" não tem cinza azulado. "Pra Mac, Windows e Linux" tem os três. Parecido não é igual.
- **Fez só o que foi pedido?** Mudança que ninguém pediu e que muda o resultado entra na lista, para a pessoa saber.

## 3. Prove cada item, agora

Para cada item, o portão:

1. **Qual prova mostra que está feito e funcionando?** A que cobre o item inteiro, não uma parte.
2. **Rode agora**, depois da última mudança. Resultado de antes não conta.
3. **Leia a saída inteira**: código de saída, número de falhas, avisos novos.
4. **Ela confirma?** Marque **feito** (com a prova), **diferente do pedido** (o que diverge), **parcial** (o que falta) ou **não feito**.

| Tipo de item | Prova | Não basta |
|---|---|---|
| Mudança em código ou texto | O trecho no arquivo (`arquivo:linha`) ou o diff | "Mudei" |
| Lógica, função | A suíte do pacote com 0 falhas | Só o teste novo, rodada antiga |
| Build, tipos, lint | O comando completo terminando com código 0 | Lint verde provando o build |
| API, integração | Uma chamada real com a resposta | O código parece certo |
| Algo visual | Print do estado mudado no tamanho em que a pessoa usa | Build verde |
| Bug corrigido | O passo que reproduzia o bug, agora sem o bug | Código mudado |
| Algo removido | Busca mostrando que não sobrou nada | "Apaguei" |
| Algo publicado (push, deploy, envio) | Confirmação do outro lado: status remoto, CI, URL | O comando local não deu erro |
| Desempenho | Número antes e depois, medido do mesmo jeito | "Ficou mais rápido" |
| Trabalho de outro agente | O diff real e a sua conferência | O relatório dele dizendo "sucesso" |

## 4. Feche o que faltou

Item diferente do pedido, parcial ou não feito: faça agora, se está no escopo. Se não dá para fazer (falta acesso, decisão da pessoa, informação), diga exatamente qual e por quê.

## 5. Segunda volta, inteira

Corrigiu alguma coisa na primeira volta? Então a conferência de antes não vale mais: correção quebra o que estava certo. Refaça os passos 1 a 3 do zero, com a lista inteira, não só os itens corrigidos, e rode as provas de novo.

A segunda volta só confere, não edita. Se ela achar algo, corrija e faça outra volta inteira. Você para quando uma volta inteira passa sem mudar nada.

## 6. Só então responda

- "Pronto" só se todos os itens estiverem feitos e provados.
- Pedido com mais de uma parte: mostre a lista curta com o pedido, o entregue, o estado e a prova de cada item.
- O que não deu para verificar vai escrito: "não testei no Safari", "o deploy não foi feito".

## Sinais de que você está sendo corno

- Responder só à última mensagem e esquecer as anteriores.
- "Deve funcionar", "provavelmente", "parece que", "acho que resolve".
- Comemorar ("Perfeito!", "Tudo certo!") antes de conferir.
- Commit, push ou PR sem prova fresca.
- Conferir uma parte e afirmar o todo.
- Entregar parecido com o pedido e chamar de feito.
- Corrigir na conferência e responder sem conferir de novo.
- Confiar no relatório de outro agente.
- "Só desta vez", "é mudança pequena", "esse detalhe a pessoa nem vai notar".

## Desculpas e a resposta

| Desculpa | Resposta |
|---|---|
| "Agora deve funcionar" | Então rode. |
| "Tenho certeza" | Certeza não é saída de comando. |
| "Já fiz o principal" | A pessoa pediu tudo, não o principal. |
| "É só um ajuste pequeno" | Ajuste pequeno quebra build igual. |
| "O lint passou" | Lint não compila nem testa. |
| "O agente disse que deu certo" | Confira o diff e rode você. |
| "Conferir tudo demora" | Menos que desfazer um "pronto" errado. |
| "Ficou quase igual ao pedido" | Quase igual é diferente. Ajuste ou diga a diferença. |
| "Só corrigi um detalhe, não precisa conferir de novo" | A correção é a mudança mais nova e a menos conferida. Segunda volta. |

## Quando não usar

Conversa sem entrega (explicar um conceito, opinar): não há pedido para conferir nem nada para rodar.

## Pronto quando

Cada coisa pedida na conversa está ao lado do que foi entregue, igual ao pedido, com uma prova rodada depois da última mudança; uma volta inteira passou sem precisar mudar nada; o que não deu foi dito; e a palavra "pronto" só aparece se nada ficou para trás.
