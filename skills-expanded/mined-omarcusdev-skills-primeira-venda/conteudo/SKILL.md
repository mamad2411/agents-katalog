---
name: conteudo
description: Produz o conteúdo de um negócio local a partir de fotos e vídeos reais do produto ou serviço, com inventário das mídias, lista de tomadas para gravar no celular, edição simples, posts de feed, carrosséis, stories, capas de destaque, reels, criativos de anúncio, imagens de catálogo e legendas, e com revisão de privacidade, autorização de imagem, preço e área segura antes de publicar. Use quando o usuário pedir post, story, reel, carrossel, legenda, criativo, imagem de catálogo, calendário de conteúdo, quiser melhorar as fotos e vídeos do produto ou revisar peças já prontas antes de publicar. Publicar a peça é da skill presenca-nas-redes.
---

# Conteúdo

Foto e vídeo reais do negócio, legendas no tom dele e uma revisão antes de sair. Esta skill prepara as peças. Publicar é com `presenca-nas-redes`, e gastar em anúncio é com `anuncios`.

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

1. **Sem a ficha.** Se `negocio/ficha.md` não existe, pergunte o que o negócio vende, os preços e o tom de voz, e grave a ficha antes de seguir. Se existir `marca/marca.json`, use as cores, as fontes e o `{telefone}` de lá.
2. **Inventário primeiro.** Abra cada foto e vídeo e grave `midia/inventario.md`: o que mostra, a qualidade, o uso possível, dado pessoal visível e se há autorização de imagem. Termine com "melhores tomadas", "não usar" e "pedir ao dono". Modelo em `references/inventario-de-midias.md`.
3. **Originais intocados.** Copie tudo para `midia/originais/` e trabalhe só em cópias (`midia/tratadas/`).
4. **Escolha o caminho.** O padrão não instala nada: lista de tomadas para o celular, edição no editor do celular e legendas. Reel sempre sai com a lista de tomadas e o roteiro para gravar no celular (`references/lista-de-tomadas.md`), na mesma entrega. O reel feito de fotos é só a opção rápida, oferecida ao lado, nunca no lugar. O caminho com código é opcional e só entra se o usuário já tem as ferramentas ou aceita instalar. Antes de instalar qualquer coisa, mostre o comando e peça o ok. Python vai num ambiente isolado em `ferramentas/`.
5. **Peça material novo quando faltar.** Dê a lista de tomadas (`references/lista-de-tomadas.md`). Foto de WhatsApp comprimida ou print ampliado fica borrado em tela cheia: peça a original da câmera, enviada como documento.
6. **Trate e monte.** Fotos: `references/tratamento-de-fotos.md`. Vídeo: `references/video-do-celular.md`. Peças com texto e preço: `references/pecas-por-codigo.md`, no tamanho certo (`references/formatos-e-area-segura.md`). O produto na peça é o produto que se entrega.
7. **IA de imagem ou de voz, só com chave paga do usuário e pedido dele.** Diga antes quantas imagens, o custo estimado e o limite de gasto. Regras em `references/ia-de-imagem.md`. Nunca para consertar foto ruim nem para criar pessoa ou produto.
8. **Legendas.** No tom da ficha, com a forma de pedir (link do WhatsApp com um código por peça). Enquanto o canal não existe, o convite fica como `{como falar com a gente}`. Sem escassez falsa, sem desconto que o dono não aprovou, sem preço fora da ficha. Veja `references/legendas-e-tom.md`.
9. **Revisão.** Um segundo agente, ou o checklist em sequência se não houver subagentes: `references/revisao-antes-de-publicar.md`. Grave `conteudo/<semana>/revisao.md`, também para roteiro (a revisão do texto; a do vídeo vem depois de montado), e também quando o dono traz peças já prontas. Antes do passo 10, confira que o arquivo existe. Para vídeo, extraia quadros e olhe. O revisor não ouve áudio: a voz fica para você ouvir.
10. **Entrega.** Mostre o lote como lista numerada, com a peça, a legenda e o resultado da revisão. O dono responde item por item ("sim 1, 3, 4"). Item sem "sim" não segue. Cada ok vai para `negocio/decisoes.md`. Arquivo prometido (autorização de imagem, roteiro) é gravado na mesma resposta, ou não é prometido.

Criar ou arrumar perfil é da `presenca-nas-redes`. Se o dono não tem Instagram, diga em uma frase que o perfil só deve ser criado depois que o número do negócio existir, e passe a frase pronta para pedir isso: "arruma meu Instagram quando o número chegar".

Se o atendimento do negócio manda cardápio ou tabela de serviços por mensagem, a foto boa dela também serve lá. Veja `atendente-ia`.

## O que é com você

- Fotografar e filmar o produto ou o serviço (o Claude não cria foto de produto).
- Editar o vídeo no celular, se escolher o caminho padrão.
- Colher a autorização de imagem de cliente que aparecer na peça.
- Confirmar os detalhes do produto: tamanho, ingredientes, o que vai na caixa.
- Aprovar cada peça e cada legenda.
- Ouvir a voz sintética, se usar.
- Criar a chave de imagem ou voz, pôr o limite de gasto e pagar, se quiser usar.

## Regras

- Ação para fora (publicar, gastar, escrever a cliente) só com ok explícito, item por item. Esta skill não publica.
- Nada inventado: preço, prazo, ingrediente, estoque, "feito na hora". A peça só afirma o que a ficha sustenta.
- Nunca em peça pública: telefone ou e-mail pessoal, endereço da casa, nome de terceiro, marca vizinha, rosto ou pet de cliente sem autorização registrada. Sem autorização, recorte ou desfoque.
- Foto ou print de outra pessoa ou de outro negócio não entra. Só material próprio.
- Chave de provedor fica no `.env` do projeto, que o próprio usuário preenche. Nunca peça a chave no chat nem a imprima.
- Custos ditos antes: chaves pagas de imagem e voz, e a licença do Remotion para empresa maior.
- Regras completas: `../montar-negocio/references/regras-da-casa.md`.

## Lições de origem (para você, Claude; não narre ao dono)

Vêm do caso de origem do plugin, uma doceria pequena. Amostra pequena, um único caso. É lição, não promessa de resultado. Use como conselho em voz neutra; cite a origem só se o dono perguntar de onde vem o conselho.

- Um vídeo real gravado no celular teve cerca de 3 vezes menos custo por conversa do que as artes gráficas, que ficaram caras ou sem nenhuma conversa.
- Só 1 de 39 mídias novas tinha sido usada quando o inventário foi feito. Faça o inventário antes de criar.
- IA de imagem melhora fundo e enquadramento, mas amplifica foto ruim. Foto de partida borrada continua borrada.
- Exposição só clareia: escurecer deixou o chocolate com cor de barro. Vídeo HDR de iPhone precisa ir para SDR, senão fica lavado.
- Texto inventado ("feito na hora") foi cortado na revisão. Telefone pessoal visível num adesivo vazou em toda foto e recorte.
- Votação em página repetida irritou o dono. Lista numerada no chat resolve.

## Leia quando

- Montar o inventário: `references/inventario-de-midias.md`.
- Pedir material novo: `references/lista-de-tomadas.md`.
- Editar vídeo: `references/video-do-celular.md`.
- Tratar foto ou recortar fundo: `references/tratamento-de-fotos.md`.
- Usar IA de imagem ou voz: `references/ia-de-imagem.md` e, para voz, `references/legendas-e-tom.md`.
- Escolher tamanho e margem: `references/formatos-e-area-segura.md`.
- Gerar peças por código: `references/pecas-por-codigo.md`.
- Escrever legenda: `references/legendas-e-tom.md`.
- Aparece pessoa ou pet de cliente: `references/autorizacao-de-imagem.md`.
- Antes de mostrar o lote: `references/revisao-antes-de-publicar.md`.
