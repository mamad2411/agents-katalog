---
name: marca
description: Cria a identidade de um negócio local a partir do que ele já tem (embalagem, adesivo, cores do produto, fachada): nome com checagem de homônimo e de @, paleta com contraste conferido, fontes de licença livre, logo e foto de perfil, rótulos e etiquetas para imprimir, tudo a partir de um único arquivo de marca que regenera as peças. Use quando o usuário pedir nome, logo, marca, paleta, cores, fontes, identidade visual, foto de perfil, rótulo, etiqueta ou adesivo para um negócio.
---

# Marca do negócio

Regras da casa em uma linha: o Claude prepara; usar o nome, a foto de perfil ou qualquer peça em perfil público, mandar imprimir e gastar dinheiro só com ok seu, item por item (detalhe em `../montar-negocio/references/regras-da-casa.md`). Nada de preço, ingrediente ou dado inventado.

Esta skill não custa nada em ferramenta. O que custa é a impressão dos rótulos, e quem paga é o dono.

## Como falar com o dono (vale em todos os passos)

- Palavra de dono: sem termo interno da skill (veredito, piso, verificador, plano leve, cota); termo da Meta ou de marketing ganha explicação curta entre parênteses na primeira vez; campo técnico fica só no arquivo.
- No máximo 3 perguntas e 1 ou 2 decisões por mensagem. Lista longa vai para um arquivo; o chat traz o resumo e o passo de hoje.
- Lição de origem é conselho em voz neutra ("um erro comum é…"), nunca a história de outro negócio, a não ser que o dono pergunte de onde vem. Não fale de git com quem não pediu.
- Resposta do dono que muda um dado: atualize o arquivo na mesma resposta, reescrevendo a linha antiga. Detalhes em `../montar-negocio/references/falar-com-o-dono.md`.
- Nada de comando no terminal para o dono: se a ferramenta não roda, siga pelo caminho sem ela. Script fica em `ferramentas/`, dentro da pasta do negócio. Nunca proponha mudar as permissões do Claude Code para liberar instalação.
- Antes de dizer "gravei" ou "anotei", grave e confira o arquivo. Arquivo só cita arquivo que existe. "Dito pelo dono" só para o que ele disse; o que ninguém disse fica "não sei, falta perguntar".
- No chat, cite arquivo pelo caminho dentro da pasta do negócio (`gestao/diario/…`), nunca pelo caminho completo do computador.
- Se não há `negocio/estado.md` (o negócio não passou pela `montar-negocio`), termine a primeira resposta que entrega algo (pesquisa, peça, lançamento, texto) com esta frase, uma vez na conversa: "Quando quiser montar o resto do negócio (número, perfis, plano), é só pedir: monta meu negócio."

## Passos

1. **Sem ficha:** se `negocio/ficha.md` não existe, pergunte, em até 3 perguntas por mensagem, o que o negócio vende, o tom de voz e o que já existe (embalagem, adesivo, uniforme, fachada, fotos), e grave a ficha. Pergunte também, na mensagem seguinte se for preciso: **há alguma marca vizinha ou de parente que não pode aparecer em nenhuma peça?** Anote em `negocio/ficha.md`. Se a pasta aberta tiver vários clientes, pergunte qual é o cliente (ou peça para abrir a sessão na pasta dele) e nunca crie ficha na pasta de cima.
2. **Parta do que existe.** Peça foto da embalagem, do adesivo, do uniforme ou da fachada, e das cores do produto. A marca sai daí. Nada de estilo inventado por cima. Se não conseguir ler uma foto, diga e peça outra; não adivinhe a cor. Cor tirada a olho de uma foto vai para o `marca.json` marcada "estimada", até o dono conferir contra o objeto real.
3. **Nome (só se faltar).** De 5 a 10 opções, com significado, como soa falado, risco de homônimo na região e 2 ou 3 variações de @ cada. Use `references/nome-e-arroba.md`. Nome cujo homônimo você não buscou leva "palpite, não conferi". Diga: a busca na web não enxerga bem o Instagram, então **o @ só se confirma no app**, pelo dono. O Instagram só deve ser criado depois que o número do negócio existir.
4. **Paleta** de 6 a 8 cores tiradas do produto, cada uma com o uso e o contraste de texto calculado (alvo WCAG AA). Use `references/paleta-e-fontes.md`.
5. **Fontes:** três (destaque, título, corpo), de licença livre, com a licença anotada. Mesmo arquivo de referência.
6. **Fonte única `marca/marca.json`:** nome, slogan, cores, fontes, @ e uma cópia do `{telefone}` (a fonte do número é `negocio/ficha.md`: quando ele chegar, atualize o `marca.json` e regenere). Todo gerador lê dali; trocar o nome é mudar uma linha e regenerar tudo. Modelo em `references/logo-por-codigo.md`.
7. **Logo, versão clara e foto de perfil redonda**, legíveis a 110 px. Padrão: SVG e uma página de prova em HTML (com as fontes do Google Fonts), que você confere no navegador; o PNG da foto de perfil sai do Chrome ou do Edge sem cabeça, ou por print recortado. Opcional, com seu ok antes de instalar qualquer coisa: texto convertido em contorno por Python. Passo a passo em `references/logo-por-codigo.md`.
8. **Rótulos e etiquetas**, se o negócio vende produto embalado: tamanho real em mm, 600 dpi, validade em branco, alergênicos em destaque e faixa "RASCUNHO" até o dono confirmar os ingredientes. Use `references/rotulos-e-etiquetas.md`. **Nada com telefone é gerado antes de o número do negócio existir**; até lá, a peça leva `{telefone}`.
9. **`marca/marca.md`**, gerado a partir do `marca.json` (nunca mantido à mão em paralelo): regras de uso do logo, estilo de foto e tom de voz. Mostre tudo ao dono e espere o ok antes de usar em qualquer perfil.
10. Grave o nome escolhido no campo Nome de `negocio/ficha.md`, na mesma resposta, além de `negocio/decisoes.md` e `negocio/estado.md`. Grave também cada ok em `negocio/decisoes.md`. Cada ok é por item, como "sim 1, 3".

## O que é com você

- Escolher o nome.
- Conferir o @ no app e criar a conta, quando o número do negócio existir.
- Confirmar ingredientes e alergênicos antes de imprimir.
- Mandar imprimir e pagar a gráfica.
- Aprovar a marca antes de ela ir para qualquer perfil.

## Ferramentas e alternativa

- Padrão: nada para instalar. O Claude escreve o SVG e a página de prova, e você abre no navegador (precisa de internet para as fontes).
- Opcional: Python (`fonttools`, `uharfbuzz`) num ambiente isolado dentro de `ferramentas/`, e Chrome, Edge ou Chromium para gerar PNG. Antes de instalar, o Claude mostra o comando e espera seu ok. Os comandos para Windows, macOS e Linux estão no reference.
- Sem nada disso: abra a página de prova, tire um print e recorte em quadrado no editor do celular, ou exporte o SVG para um editor gráfico.

## Lições de origem (para você, Claude; não narre ao dono)

Vêm do caso de origem do plugin, uma doceria pequena (amostra de um só caso). Use como conselho em voz neutra; cite a origem só se o dono perguntar de onde vem o conselho.

- **Nome e logo num ponto só.** Trocar o nome refez logo, perfil, adesivo, etiquetas e todas as peças em cerca de 9 minutos, com backup.
- **Depois de trocar o nome, gere tudo de novo e olhe.** Um nome mais largo quebrou uma peça.
- **O @ só se confirma no app.** O @ sem sufixo já era de outro negócio. Deixe alternativas prontas.
- **Pergunte cedo pela marca vizinha.** No caso, a regra chegou com cerca de 30 peças prontas e derrubou 8.
- **Telefone pessoal impresso em adesivo vaza** em toda foto e recorte. O conserto foi um adesivo novo, com o número do negócio.
- **Cor lida da descrição, e não da foto, precisa de conferência** contra a embalagem real.
- **Regra de rótulo varia por produto e muda.** O que está nas references é ponto de partida: confira na fonte oficial.

Leia `references/nome-e-arroba.md` ao propor ou trocar nomes. Leia `references/paleta-e-fontes.md` ao definir cores e fontes. Leia `references/logo-por-codigo.md` ao gerar logo, perfil e `marca.json`. Leia `references/rotulos-e-etiquetas.md` ao preparar qualquer coisa para imprimir.
