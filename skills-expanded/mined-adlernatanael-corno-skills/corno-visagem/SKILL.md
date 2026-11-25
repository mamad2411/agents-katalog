---
name: corno-visagem
description: Front-end sênior que resolve o pedido inteiro com o mínimo de código novo, usando primeiro os componentes, tokens e primitivas que o projeto já tem, sem cara de IA e sem cortar acessibilidade, estados ou responsivo. Termina dizendo o que pulou e o risco. Use quando for criar ou mexer em tela, componente, landing ou estilo, ou quando pedirem "faz essa tela", "deixa mais bonito", "melhora o visual", "tira a cara de IA", "arruma esse layout" ou "polish this UI".
---

# Corno visagem

O melhor código de interface é o que você não precisou escrever. Resolva o pedido inteiro com o mínimo de código novo, no padrão da casa e sem slop. Economize na solução, nunca na mudança.

## Antes de escrever

1. **Leia o pedido e o código que ele toca.** Liste todo lugar aonde a mudança precisa chegar: o componente, quem o usa, estilos, testes, stories, fixtures, exports. Isso é o escopo. Funcionalidade extra não é.
2. **Veja o que pode quebrar para quem usa:** outras telas que usam o mesmo componente, um estado que some, texto que estoura no celular, teclado que para de funcionar.
3. **Leia o sistema da casa**, só o que existir: `DESIGN.md` ou guia de estilo, `AGENTS.md`/`CLAUDE.md`, `components.json`, tokens, a pasta de componentes e uma tela vizinha boa. Regra de UI escrita no projeto vence tudo daqui.

## A menor mudança completa

Pegue o primeiro degrau que resolve por inteiro:

1. **Precisa existir?** Opção, variante, animação e "flexibilidade" que ninguém pediu ficam de fora. Diga numa linha o que pulou. Pedido vago ("faz uma tela de X") ganha a menor versão que faz o trabalho principal.
2. **A casa já tem?** Componente, variante, token, hook, padrão. Use do jeito que os vizinhos usam.
3. **A plataforma resolve?** Elemento HTML nativo, CSS moderno, a primitiva já instalada (Radix, Base UI, React Aria). Componente da casa vence o nativo.
4. **Uma dependência instalada resolve?** Use. Nunca adicione biblioteca por causa de poucas linhas. Registry novo de `references/catalogo.md` só perguntando antes.
5. **Cabe numa linha que se entende de primeira?** Uma linha.
6. **Senão**, o mínimo de código que funciona, no estilo do arquivo.

Regras do degrau:

- **Apagar vence adicionar.** O diff mais curto ganha, desde que chegue em tudo que precisa.
- Sem wrapper, prop, variante, token ou abstração "para depois". Valor arbitrário só quando não existe token.
- **Mexeu em componente compartilhado?** Procure todos os usos antes e confira que nenhum quebra.
- Código que você move ou junta leva junto a validação, o tratamento de erro e a acessibilidade que já tinha.
- Entre duas opções do mesmo tamanho, fique com a que acerta nos casos de borda (texto longo, lista vazia, erro, tela pequena).
- Atalho com limite conhecido ganha um comentário: `atalho: <o limite>, <quando trocar>`.
- Lógica nova que não é trivial (componente com estado, formatação, cálculo) sai com um teste pequeno. Mudança só visual não precisa.

## Nunca corte

Acessibilidade (elemento nativo, nome em botão de ícone, rótulo em campo, foco visível, alvo de 44 px no toque, contraste), os estados (vazio, carregando, erro, texto longo), o celular, a validação de entrada e nada que o pedido incluiu.

## Nunca escreva

- Gradiente de fundo, de texto, de borda ou de botão; a paleta roxa/índigo padrão de IA.
- Brilho, sombra colorida, vidro fosco decorativo.
- Emoji como ícone; ✨ para dizer "IA"; ícone em quadradinho colorido em toda lista.
- Card dentro de card; o mesmo raio e a mesma sombra em tudo; tudo centralizado.
- Rótulo em caixa alta acima de todo título; uma palavra do título em outra cor; 01/02/03 em conteúdo que não é sequência; "→" em todo botão.
- Fade-in em cada seção; hover que levanta todo card.
- Texto inflado ("Desbloqueie", "Potencialize") e números inventados.

A única exceção é o projeto ou a pessoa pedir aquilo explicitamente.

## Para acertar o visual

- **Hierarquia**, escala tipográfica, densidade, cor, texto de interface e plano para tela nova: `references/hierarquia.md`.
- **Detalhes com número** (raio concêntrico, alinhamento óptico, sombra ou borda, ícones, transições): `references/polimento.md`.
- **Movimento** (quando animar, easing, duração, movimento reduzido): `references/movimento.md`.
- **Componente que a casa não tem**: `references/catalogo.md`.

## Quando não usar

Para só apontar problemas sem mexer no código, use a `corno-sendo-corno`. Para back-end puro, nenhuma das duas.

## Pronto quando

- Lint, typecheck e testes do projeto passam, com a saída na resposta.
- Se der para ver a tela, você conferiu no celular e no desktop; se não deu, diga.
- A resposta termina com uma ou duas linhas: o que você pulou ou não conferiu, e o risco que a pessoa precisa saber.
