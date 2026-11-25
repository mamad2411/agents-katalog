---
name: corno-pesquisa
description: Pesquisa uma pergunta em fontes primárias confiáveis (documentação oficial, código, especificação) e salva o que achou num Markdown no repositório, com links. Use quando pedirem para pesquisar um assunto, "o que a doc diz sobre", "qual versão suporta", "isso ainda funciona assim?", levantar fatos de uma API ou documentação, comparar opções ou bibliotecas, ou "research this".
---

# Corno pesquisa

Responda com o que as fontes dizem, não com o que parece certo.

Se o ambiente permite agente em segundo plano, delegue a leitura a ele com a pergunta e o formato abaixo, e siga trabalhando enquanto ele lê.

## Como

1. **Escreva a pergunta** em uma frase e o que conta como resposta (um número de versão, um comportamento, uma decisão).
2. **Fontes primárias primeiro:** documentação oficial, código-fonte, changelog, especificação, issue do mantenedor. Blog e fórum só para achar a fonte primária.
3. **Confira a data.** Anote a versão e a data de cada fato; coisa velha muda.
4. **Separe fato de inferência.** Fato tem link. Inferência diz "pelo que o código mostra, …".
5. **Salve** na pasta de docs que o projeto já usa, ou em `docs/pesquisa/<assunto>.md` se não houver, neste formato:

   ```markdown
   # <pergunta>
   Pesquisado em <data>.

   **Resposta:** <uma ou duas frases>

   ## Achados
   - <fato> ([fonte](link), versão X, data)

   ## Em aberto
   - <o que não deu para confirmar>
   ```

## Resposta

Comece pela resposta em uma ou duas frases. Depois os detalhes e os links. Se as fontes discordam, mostre as duas e diga qual parece mais confiável e por quê. Se não achou, diga que não achou; não preencha o buraco com chute.
