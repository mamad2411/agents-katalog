---
name: criar-post-instagram
description: Monta post completo de Instagram (imagem + legenda + hashtags + CTA + primeiro comentário) pronto para aprovação e publicação. Usa identidade de memory/empresa.md e tom de voz de config/tone-of-voice.md.
visibility: global
---

# Criar post de Instagram

## Quando usar
- Após gerar imagem com `gerar-imagem-post`.
- Quando data comemorativa ou campanha aparecer em `memory/marketing.md`.
- Quando Lia quiser propor conteúdo proativo para feed, story, reel ou carrossel.

> **Antes de escrever qualquer copy**, consultar `marketing/design-instagram`:
> - Seção 2 para identificar o tipo de post
> - Seção 3 para a fórmula de copy do tipo
> - Seção 4 para o gancho correto
> - Seção 9 para hashtags por segmento

## Estrutura da legenda
1. **Gancho** — 1ª linha, deve fazer parar de rolar.
2. **Contexto** — 2 a 4 linhas explicando o tema.
3. **Valor / oferta / ensinamento**.
4. **CTA claro** — comentar, salvar, mandar DM ou clicar no link da bio.
5. **Encerramento humano** — seguir `config/tone-of-voice.md`, sem robótico.

## Hashtags
- 5 a 12 no total:
  - 2-3 de nicho amplo
  - 3-5 de nicho específico
  - 1-2 locais (cidade / estado)
  - 1 de marca própria (se houver)
- Nunca usar hashtags spam ou irrelevantes.

## Primeiro comentário
- Repetir CTA ou colocar link (link não é clicável na legenda do feed).

## Saída entregue a Lia

```
[IMAGEM] workspace/output/marketing/...png
[FORMATO] feed | story | reel | carrossel

[LEGENDA]
...texto completo...

[HASHTAGS]
#tag1 #tag2 ...

[PRIMEIRO COMENTÁRIO]
...

[CTA]
...

[STATUS] rascunho — aguardando aprovação
[MEMÓRIA] registrado em memory/marketing.md id: cmp-YYYY-MM-DD-<slug>
```

## Não pode
- Publicar sem aprovação humana.
- Prometer preço, prazo, garantia ou desconto não validados.
- Usar frase proibida em `config/tone-of-voice.md`.
- Usar claim médico, financeiro ou jurídico sem fonte validada.
