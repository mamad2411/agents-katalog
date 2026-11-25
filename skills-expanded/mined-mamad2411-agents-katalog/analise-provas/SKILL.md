---
name: analise-provas
description: "Use somente quando invocada explicitamente para analise probatoria estruturada: documentos, autenticidade aparente, admissibilidade, lacunas, prova faltante e risco adversarial. Nao autoacionar por mencoes genericas a provas."
---

# Analise de Provas

Usar esta skill apenas por selecao explicita do usuario.

Executar leitura juridica dos documentos antes de redigir a peca. Tratar prova como estrutura do caso, nao como anexo decorativo.

## Coordenacao com o stack atual

- Se os arquivos estiverem em `.pdf`, usar ferramentas locais de leitura, OCR ou extracao quando necessario.
- Se os arquivos estiverem em `.docx`, usar tambem a skill `doc` para leitura estruturada.
- Se a analise probatoria precisar ser convertida em peca, migrar depois para `peticao-final`.

## Objetivo

Entregar parecer probatorio que responda:

- o que cada documento prova;
- qual a forca probatoria de cada item;
- quais fatos estao cobertos, fracos ou sem prova;
- quais pontos sao vulneraveis a impugnacao;
- como organizar a prova na futura peticao.

## Criterios de sucesso

- Inventario objetivo dos documentos relevantes.
- Matriz `documento -> fato que prova -> forca -> tipo`.
- Distincao clara entre fato alegado, fato documentalmente demonstrado e inferencia.
- Lacunas ligadas a fatos essenciais, nao a observacoes genericas.
- Risco adversarial apontado sem presumir autenticidade tecnica, autoria ou licitude.

## Fluxo essencial

1. Inventariar documentos por funcao: relacao juridica, fato gerador/descumprimento, dano/consequencia e corroboracao.
2. Para cada documento, identificar tipo, origem, data relevante, destinatario, formato e integridade aparente.
3. Relacionar cada documento a fato juridico concreto. Evitar conclusoes vagas como "ajuda o caso".
4. Classificar forca:

- `5`: prova direta e dificil de contestar
- `4`: prova forte, mas com algum ponto de ataque
- `3`: prova indireta relevante ou conjunto indicativo
- `2`: indicio fraco ou dependente de complemento
- `1`: nao sustenta o fato sozinha

5. Avaliar autenticidade aparente, licitude de obtencao, necessidade de traducao/autenticacao/cadeia de custodia/complemento tecnico e coerencia com a narrativa.
6. Mapear lacunas em tabela `fato essencial -> prova disponivel -> status`.
7. Antecipar ataques: conversa parcial, print isolado, copia simples, documento editavel, e-mail sem cabecalho, audio/video sem origem minima, contradicao documental.
8. Recomendar ordem de apresentacao da prova e cautelas de redacao.

## Regras de parada

Parar e pedir complemento quando arquivos estiverem inacessiveis, ilegiveis ou insuficientes para inventario minimo. Se a prova contradisser a narrativa do cliente, tratar como risco critico antes de sugerir peca.

## Restrições

- Nao inventar prova inexistente.
- Nao presumir autenticidade tecnica, data, autoria ou licitude sem base.
- Se a prova for fraca, dizer que e fraca.
- Se faltar base para fato central, tratar como lacuna.
- Nao redigir peticao completa dentro desta skill.

## Formato de saida

```text
PARECER PROBATORIO

1. INVENTARIO
2. MATRIZ PROBATORIA
- documento -> fato que prova -> forca -> tipo

3. PONTOS FORTES
- [provas com melhor lastro e o fato que sustentam]

4. PONTOS DE ATENCAO
- [problemas de admissibilidade, autenticidade ou contexto]

5. LACUNAS
- [fatos sem prova suficiente e como suprir]

6. RISCO ADVERSARIAL
- [contra-ataques previsiveis]

7. ESTRATEGIA DE APRESENTACAO
- [ordem recomendada e forma de ancoragem na peca]
```

Se o usuario pedir proxima etapa, encaminhar para `peticao-final` ou ferramenta documental adequada, conforme o caso.
