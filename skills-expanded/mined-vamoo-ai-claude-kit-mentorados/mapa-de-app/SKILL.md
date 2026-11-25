---
name: mapa-de-app
description: >-
  Mapeia um app existente (telas, fluxos, dados) antes de orçar. Use em "quero um sistema igual
  ao X".
---

# mapa-de-app

Quando o cliente diz "quero um sistema igual ao X", ninguém sabe ainda o que é "igual". O
mapa responde antes da proposta e antes do plano: o que o X faz, por onde o usuário anda,
que dados ele guarda e o que dá para construir. Proposta sem mapa promete o app inteiro;
com mapa, promete a fatia que o cliente usa.

Reporte em PT-BR, sem travessão. Dado sem fonte não entra.

## Regras antes de tudo

O mapa estuda o que o app faz e como a pessoa usa. Não leva nada que é do app.

- **Só fonte pública e a conta do próprio cliente.** Nunca entre em conta de terceiro,
  nunca peça senha, nunca passe de paywall ou login por atalho.
- **Ler, não raspar.** Nada de crawler, download em massa ou loop. No navegador, uma
  página por vez, no ritmo de uma pessoa, com o cliente presente quando for a conta dele.
- **Sem código e sem API privada.** Não leia nem salve o JavaScript do app, não
  descompile, não registre chamadas de rede para copiar endpoint. Documentação pública de
  API pode.
- **Termos de uso.** Alguns proíbem usar a conta para construir concorrente. Se a conta
  do cliente está nesses termos, diga e trabalhe só com o público.
- **Print é referência.** Fica na pasta do mapa para comparar layout e nunca vai para o
  produto. Logo, ícone, ilustração, fonte paga e texto do app também não.

## Passo 1: recorte

Proponha e peça o sim em três pontos:

1. **Qual app e qual plataforma:** web, iOS, Android, desktop.
2. **Qual fatia.** "O X inteiro" não é projeto. Recomendado: o fluxo pelo qual o usuário
   paga. Pergunte ao cliente o que a equipe dele faz no X todo dia.
3. **Para quem.** A operação do próprio cliente, um nicho, ou produto para vender.

## Passo 2: fontes

Tabela de fontes primeiro, com link em cada linha, nesta ordem de valor:

| Fonte | O que dá |
|---|---|
| Central de ajuda | A lista de funcionalidades mais completa que existe, e as configurações |
| Página de preço | O que importa: o que eles cobram para liberar |
| Changelog | O que entrou há pouco e o que o time deles acha importante |
| Loja de apps | Print das telas principais, o discurso e as notas |
| Vídeo público de uso | Fluxo real, clique a clique |
| Site | Posicionamento e o fluxo principal nas palavras deles |
| Conta do cliente | O app de verdade, com todos os estados, com o cliente conduzindo |
| Documentação pública de API | O modelo de dados quase de graça |

## Passo 3: telas

Uma linha por tela, com ID fixo (T01, T02...), que todo o resto cita:
`ID | tela | rota ou como chega | para que serve | componentes | estados vistos`.
Estados contam: vazio, carregando, preenchido, erro, sem permissão, celular. Estado vazio
que não entrou no mapa é estado vazio que ninguém vai construir.

## Passo 4: fluxos

F01, F02...: o objetivo e as telas por onde passa, com os desvios. Conte os cliques do
caminho feliz: é o número a bater.

```
F01 Cliente agenda uma visita
    T07 agenda -> T08 escolhe horário -> T09 dados -> T10 confirmado
    cliques: 6
    desvios: sem horário na semana, fuso diferente, horário tomado no meio do preenchimento
```

## Passo 5: componentes

Toda peça que se repete: botão, campo, seletor de data, modal, tabela, aviso, menu. Nome,
variações, estados e em que telas aparece.

## Passo 6: modelo de dados inferido

Entidades, campos e relações, cada uma com a evidência e a confiança (alta, média,
palpite). Palpite fica escrito como palpite. Daqui sai o esquema do Supabase no plano.

```
Agendamento  id, tipo_id, inicio, fim, nome, email, status (confirmado | cancelado), respostas (json)
             evidência: T09 campos do formulário, T10 confirmação, artigo de ajuda "Cancelar"
             confiança: alta
```

## Passo 7: matriz de funcionalidades

`funcionalidades.csv`, colunas `funcionalidade,area,prioridade,no_original,no_nosso,notas`.
Prioridade: deve, deveria, poderia, fora. `no_nosso` nasce `nao` em toda linha e vira `sim`
durante a construção: é a régua de "falta quanto". Modelo em
`references/funcionalidades.modelo.csv`.

## Passo 8: o que não se copia

Linhas `fora`, cada uma com o motivo: conteúdo licenciado, a rede de usuários, dado que é
do app, parceria comercial, hardware, licença regulada (banco, saúde). "Igual ao X" quer
dizer as funcionalidades e o fluxo, não o que o X é dono.

## Passo 9: tamanho

Telas, fluxos, entidades e as partes difíceis (tempo real, sincronização, pagamento,
integração de agenda ou e-mail, offline). Tamanho: P (dias), M (semanas), G (um trimestre),
GG (recorte de novo). Nunca prometa cópia perfeita.

## Saída

Na pasta do projeto do cliente, em `.context/docs/mapa-<app>/` (sem repositório, na pasta de
trabalho): `mapa.md` pelo modelo de `references/modelo-mapa.md`, `funcionalidades.csv` e
`prints/`. No chat, cinco linhas: o fluxo principal, quantas telas e fluxos, as três partes
mais difíceis, o que ficou fora e o próximo passo.

Próximo passo, conforme o caso: a proposta para o cliente (o mapa vira o escopo, com as
linhas `deve` como entrega e o resto como fase seguinte) ou `kit-vamoo:grilling` antes do
plano de construção.
