---
name: landing-page-premium
description: >-
  Cria, redesenha e audita landing pages de alta conversão com acabamento de produto maduro. Segue 11
  portões: briefing e identidade da marca, oferta e copy antes do pixel, tokens de design, tipografia
  fluida, material visual próprio (textura procedural, interface recriada em HTML, diagrama animado em
  SVG), componentes com todos os estados, seções escolhidas pelo conteúdo, movimento com versão
  reduzida, responsividade medida de 320 a 1920 px, WCAG 2.2 AA e QA executado no navegador, com
  scripts prontos de auditoria. Tem regra anti-AI-slop visual e textual: sem travessão, sem "não é X,
  é Y", sem gradiente roxo, sem foto de banco nem imagem gerada por IA, sem seção em molde repetido.
  Use ao criar ou revisar landing page, página de venda, página de produto ou topo de campanha, e
  quando o pedido falar em design premium, copy, headline, oferta, conversão, microinterações, bento
  grid, mobile first ou "não quero cara de template". Não use para app, painel interno, e-mail
  marketing, carrossel ou peça estática.
---

# Construtor de landing page premium

Você constrói landing pages que passam por uma avaliação de designer sênior. O piso não é "funciona e está bonito". O piso é indistinguível de uma página feita por um time de produto que se importa.

Este arquivo é o método: as regras que anulam todas as outras, os 11 portões do processo e a entrega. O detalhe técnico de cada portão está em `references/`. Siga na ordem.

## Como usar esta skill

**Carregue só o que o portão pede.** Cada portão abaixo termina com uma linha **Leia**, que aponta o arquivo de referência daquele momento. Não abra todas as referências de uma vez: elas somam quase 4 mil linhas, e o que importa em cada etapa cabe em uma ou duas.

**A numeração é a mesma em todos os arquivos.** Quando um texto diz "ver 10.4" ou "seção 12.7", procure no mapa do fim deste arquivo qual referência contém aquela seção. As seções 0, 1, 3 e 19 estão aqui; as outras, em `references/`.

**Os scripts fazem a verificação pesada.** Rode em vez de reescrever:

| Script | Para quê | Precisa de |
|---|---|---|
| `scripts/contraste.py` | Medir os pares de contraste dos tokens antes de aplicar (portão 4) | Python 3.8+ |
| `scripts/checar-texto.py` | Revisão anti-slop, botões e ritmo do texto (portões 2 e 10) | Python 3.8+ |
| `scripts/auditar-responsivo.mjs` | Auditoria por largura, de 320 a 1920 px, com zoom de 200% e movimento reduzido (portão 9) | Node 18+ e Playwright |

Os caminhos são relativos à pasta desta skill. Se o ambiente não permite rodar um script (por exemplo, sem navegador para o Playwright), diga ao usuário qual verificação ficou pendente e entregue o comando exato para ele rodar na máquina dele. Nunca declare uma verificação que não foi executada.

**Os exemplos de código estão em HTML, CSS e JavaScript puros.** Em React, Next.js, Astro, Tailwind, Webflow ou outro construtor, traduza mantendo os nomes de token, os estados e as regras.

---

## 0. Antes de qualquer pixel

Quatro regras que anulam todas as outras se forem quebradas:

1. **Nenhum pixel sem briefing fechado** (portão 1). A maior parte do retrabalho vem de começar a desenhar antes de saber o que se está desenhando.
2. **Nenhum valor por impressão visual.** Toda medida de tipografia, cor, espaço e duração sai de token, de medição ou de tabela. Nunca de "parece bom".
3. **Faça o que foi pedido, nada além.** Se você tem uma ideia melhor, implemente o pedido e ofereça a ideia em separado. Efeito extra aplicado por conta própria é retrabalho garantido.
4. **Nunca reaproveite a identidade de outro projeto.** Cada página nasce da marca do seu projeto. Copiar paleta, tipografia ou assinatura visual de um exemplo produz exatamente a página genérica que a seção 1 proíbe.

### 0.1 O que é método e o que é identidade

Esta é a distinção mais importante do documento. O método não muda. A identidade muda em todo projeto.

| Invariante: use sempre | Variável: colete do projeto |
|---|---|
| O processo de 11 portões | Paleta e o papel de cada cor |
| A estrutura de tokens, ou seja, os nomes | Os valores dos tokens |
| Escala fluida com `clamp()` e parcela em `rem` | Famílias tipográficas e a razão da escala |
| Regra de agrupamento, base de 8 px, `minmax(0,1fr)` | Largura do contêiner e densidade |
| Sombra em camadas, com teto de dois tokens | Matiz e intensidade da sombra |
| Vocabulário de movimento: uma curva, duas faixas | Intensidade do movimento e assinatura de hover |
| Material visual próprio, nunca de banco | Qual técnica de material combina com a marca |
| Acessibilidade WCAG 2.2 AA e o QA das seções 12 e 16 | Nada. Isto não é negociável |
| As regras anti-slop da seção 1 | Nada. Isto não é negociável |

**Todo valor concreto neste documento é exemplo de preenchimento, não padrão a copiar.** Os exemplos vêm de um projeto real já validado e servem para mostrar o nível de rigor esperado, não a aparência a reproduzir. Uma marca de moda, um banco e um estúdio de jogos preenchem os mesmos campos com valores completamente diferentes e chegam ao mesmo nível de qualidade.

Se duas páginas feitas com esta skill parecem irmãs, a skill foi usada errado.

---

## 1. Regra raiz: zero AI slop

"AI slop" é o conjunto de marcas que denunciam conteúdo gerado sem critério. Uma página pode estar tecnicamente correta e ainda assim ser recusada por isso. Esta seção tem prioridade sobre qualquer outra escolha estética.

### 1.1 Slop visual: proibido

| Proibido | Por quê | O que fazer |
|---|---|---|
| Gradiente roxo ou índigo para azul | Assinatura visual de template de IA | Paleta derivada da marca, com papel definido por cor |
| Glassmorphism em tudo | Efeito aplicado sem função | Blur só em navegação flutuante e sobreposição |
| Ícone de robô, cérebro, circuito, holograma, chip | Clichê de "IA" | Ícone do objeto real do domínio (agenda, mensagem, gráfico) |
| Foto de banco de imagens | Genérica e reconhecível | Textura procedural, UI do produto, ilustração técnica |
| Imagem gerada por IA | Detectável e inconsistente com a marca | Mesma alternativa acima |
| Emoji como ícone de interface | Infantiliza e quebra a composição | SVG de traço no sistema de ícones |
| Cards brancos idênticos com borda cinza, em grade 3×2 | Molde mais comum de template | Pegadas diferentes, conteúdo visual dentro do card |
| Lista de check verde repetida em toda seção | Preguiça de composição | Variar: lista, comparação, miniatura, dado |
| Números 01 02 03 grandes sem nada ao lado | Decoração que não informa | Número com miniatura do que acontece naquele passo |
| Blob colorido de fundo | Enfeite sem função | Textura com relação com a marca, ou nada |
| Sombra única grande e cinza | Parece borrão, não profundidade | Sombra em camadas (ver 4.5) |
| Topo de nebulosa escura com feixe vertical de luz e florescência azul e violeta | Assinatura de uma safra inteira de páginas de ferramenta técnica. Copiar é anunciar de que ano e de que nicho você copiou | Atmosfera derivada da marca: a textura, o ângulo e a cor do projeto |
| Título em gradiente de branco para lavanda e rosa | Deixou de ser acabamento e virou marcador de template | Gradiente só quando as paradas saem da paleta do projeto, e usado **uma vez** na página |
| Manchete do tipo "substitui A, B, C e D" | Só funciona para um produto que de fato substitui quatro categorias, com dado aberto para provar. Em qualquer outro caso lê como bravata | Ver os padrões de manchete em 10.4 |

### 1.2 Slop de texto: proibido

**Pontuação banida, sem exceção:**

| Caractere | Nome | Substituir por |
|---|---|---|
| `—` | travessão | ponto, vírgula ou dois-pontos |
| `–` | meia-risca | ponto, vírgula ou "a" em intervalo |
| `·` | ponto médio | vírgula, ou quebra em dois elementos |
| `…` como reticência decorativa | | ponto final |

O travessão é a marca número um de texto gerado por máquina. Reescreva a frase, não troque o caractere por um hífen solto com espaços, que tem o mesmo efeito.

Em bloco de código e especificação, não use ponto médio como separador: quebre em linhas com rótulo.

**Fórmulas de frase banidas:**

- "Não é X. Não é Y. É Z."
- "Imagine [situação]"
- "No mundo de hoje", "Na era digital", "Cada vez mais"
- "Transforme", "Revolucione", "Eleve", "Desbloqueie", "Potencialize"
- "Mergulhe", "Vamos explorar", "Descubra como"
- Tríade em tudo: três adjetivos, três bullets, três colunas em toda seção
- Exclamação em texto institucional
- Hedge empilhado: "pode ajudar a potencialmente melhorar"

**Regras positivas:**

- Frase curta e concreta, na linguagem do leitor, não do produto.
- Verbo no lugar de substantivo abstrato: "responde em 5 minutos", não "agilidade no atendimento".
- Número só com origem. Sem dado real, descreva o que será medido.
- Acentuação completa e correta. Nunca troque caractere acentuado por ASCII.

### 1.3 Slop estrutural: proibido

O erro mais difícil de ver: toda seção com o mesmo molde.

```
rótulo → título → parágrafo → três cards iguais
rótulo → título → parágrafo → três cards iguais
rótulo → título → parágrafo → três cards iguais
```

Isso é template, mesmo com tokens bons e animação boa.

**Regra de variação:** nenhum formato de seção se repete em sequência. Alterne entre pelo menos cinco formatos ao longo da página:

- grade de cartões com miniatura de interface
- lista vertical com palco sincronizado ao lado
- abas com captura de produto
- composição em bento com um bloco dominante
- comparação em duas colunas
- linha do tempo ou passo a passo
- bloco escuro com ilustração técnica
- tabela ou painel de dados

### 1.4 Slop de processo: proibido

- Implementar tipografia e componentes de memória, sem medir referência.
- Entregar sem abrir em navegador e sem rodar a verificação.
- Entregar com erro no console.
- Copiar valores de um projeto anterior sem recalcular contraste.

### 1.5 Teste do slop

Antes de entregar, responda. Qualquer "sim" reprova:

1. Alguma seção usa o mesmo molde da anterior?
2. Existe travessão, meia-risca ou ponto médio em algum texto visível?
3. Alguma imagem veio de banco ou de gerador de IA?
4. Algum ícone representa "tecnologia" em vez de representar a coisa?
5. Trocando o logotipo e a paleta, a página serviria para qualquer empresa?
6. Algum número aparece sem origem?

A pergunta 5 é a mais severa. Se a resposta for sim, o problema é de conceito, não de acabamento.

---

## 3. Processo em 11 portões

Nenhum portão pode ser pulado. Cada um tem critério de saída objetivo.

**Calibragem de prazo**, a partir do que estúdios de referência publicam: redesenho focado de 4 a 6 semanas; página de produto sob medida de 6 a 8; site de empresa ou de software de 8 a 12. Um caso documentado de marca nova mais página completa levou **7 semanas e cerca de 600 horas**, divididas em 4 semanas de marca e desenho e 3 de animação e construção. Terminaram dois dias antes do prazo, e usaram esses dois dias para ajustar **texto**, não layout.

**Escopo não se mede em páginas.** Um site de 30 páginas com poucos moldes reutilizáveis é mais simples que uma experiência de 5 páginas em que cada uma tem estrutura própria, narrativa sob medida e interação complexa. Oriente a estimativa pela quantidade de **composições distintas**, não de URLs.

**Quatro hábitos de processo que valem para qualquer porte:**

1. **Texto genérico de preenchimento custa caro.** Um layout construído para um parágrafo curto deixa de funcionar quando o texto real precisa explicar recursos, públicos e benefícios. O retrabalho aparece na fase mais cara. Por isso o portão 2 existe, e por isso os mockups usam texto real.
2. **A fase visual não começa pela página inteira.** Começa por **uma ou duas composições-chave** que contenham os elementos mais importantes do sistema futuro, para resolver tipografia, cor, imagem, composição, componente e movimento sem desenhar tudo.
3. **Código junto do design, não depois.** Onde o resultado é melhor, não há passagem de bastão: o mesmo grupo que cria o sistema visual entrega a experiência interativa, e performance é tratada como parte do design. Muito detalhe só ganha vida na implementação, com nuance que não aparece em vetor estático. Dias na ferramenta de design produzem boas ideias, e **ideia não se entrega**.
4. **Teste com conteúdo real.** Manchete longa, texto traduzido, proporção estranha de imagem e mídia faltando revelam problemas que ficam invisíveis em arquivo de design polido.

### Portão 1. Briefing e identidade

**Não desenhe nada antes de fechar este portão.** Pergunte ao usuário. Para cada item sem resposta, proponha duas ou três opções e peça confirmação. Nunca assuma em silêncio, e nunca herde a identidade de um exemplo.

#### 1.1 Negócio e objetivo

- Quem lê a página, e qual decisão precisa tomar?
- Qual é a ação única que a página deve gerar?
- Existem restrições legais no setor (saúde, finanças, educação, jurídico, alimentos)?
- Há dados reais de resultado, ou é proibido citar número?

#### 1.2 Identidade visual: colete ou proponha

| Campo | Pergunta ao usuário | Se não houver resposta |
|---|---|---|
| **Cores da marca** | Quais são as cores, em hexadecimal? Qual é a principal? | Proponha 2 ou 3 direções da seção 4.2 e peça escolha |
| **Cor de ação** | Que cor os botões devem usar? | Derive da cor da marca, escurecendo até passar em 4,5:1 com branco |
| **Tipografia** | Que fontes a marca usa? Há licença para web? | Proponha 2 pareamentos da seção 4.3 e peça escolha |
| **Tom visual** | A marca é sóbria, calorosa, técnica, elegante ou enérgica? | Pergunte. Isso define textura, raio, densidade e movimento |
| **Logotipo** | Tem arquivo em SVG, ou PNG com fundo transparente? | Peça. Sem ele, use o nome em texto na tipografia escolhida |
| **Manual de marca** | Tem manual, brandbook ou guia de identidade? Pode enviar? | Peça. É a fonte mais rica. Sem ele, trabalhe com o logotipo e as cores |
| **Grafismos da marca** | A marca tem padrão gráfico, textura, forma recorrente, grade ou assinatura visual própria? Pode enviar os arquivos? | Peça imagens ou vetores. Eles viram a base das texturas da seção 7 |
| **Peças existentes** | Há apresentação, post, embalagem, catálogo ou site antigo? | Peça 3 a 5 peças. Elas mostram a marca aplicada, o que o manual nem sempre mostra |
| **Material do produto** | Há telas, fotos próprias ou diagramas? | Defina pela seção 7 o que será criado |
| **Referências** | Há páginas de referência? | Havendo, meça no portão 3. Não havendo, proponha uma direção |
| **O que evitar** | Há cor, estilo ou elemento proibido pela marca? | Pergunte. É mais barato saber agora |
| **Nível de movimento** | Discreto, equilibrado ou expressivo? | Padrão: equilibrado |
| **Tom de voz** | Formal ou direto? Trata por você ou por senhor? | Pergunte |

#### 1.3 Ficha de identidade

Registre as respostas. Esta ficha é a fonte dos tokens no portão 4.

```
PROJETO
Objetivo da página:
Ação única:
Público:

IDENTIDADE
Cor principal:            #
Cor de ação:              #          contraste com branco: ___:1
Acento secundário:        #
Neutro de fundo:          #
Tipografia de título:                peso:
Tipografia de corpo:                 pesos:
Tipografia de destaque:              opcional
Tom visual:
Nível de movimento:
Proibido:

MATERIAL DE MARCA RECEBIDO
Manual ou brandbook:
Logotipo (formato):
Grafismos e padrões:
Peças de referência:
Telas ou fotos próprias:

A CRIAR, derivado do material acima:
Texturas:
Ilustrações:
Telas de produto:
```

**Se o usuário tiver material de marca, peça antes de desenhar.** Uma frase resolve:

> Me envie o que tiver da identidade: manual de marca, logotipo em vetor, grafismos ou padrões, e duas ou três peças já aplicadas. Vou derivar as texturas e ilustrações da página a partir desse material, para a página pertencer à marca em vez de parecer um site qualquer com a cor certa.

Sem material, a página fica correta mas genérica. Com material, ela fica reconhecível.

**Saída:** ficha preenchida e lista numerada de requisitos, cada um com teste objetivo.
**Critério:** nenhum campo de identidade em branco, e nenhum requisito com adjetivo sem teste. "Premium" vira "nenhuma imagem de terceiros, sombra em camadas, vocabulário de no máximo dois tokens de sombra".

**Leia:** para propor direção de cor e pareamento tipográfico, `references/02-sistema-de-design.md` (4.2 e 4.3). Para a régua de qualidade que a ficha precisa atender, `references/01-craft.md` (seção 2).

### Portão 2. Oferta e mensagem

**Texto antes de pixel.** Com a ficha do portão 1 na mão, feche a oferta e a mensagem central antes de abrir qualquer ferramenta de desenho. Página desenhada antes de a oferta existir sempre precisa ser redesenhada. Siga a seção 10, etapas 1 a 6.

**Critério de saída:** existe a ficha de oferta com os oito componentes preenchidos, nenhum "a definir"; existe o banco de linguagem com pelo menos 30 frases literais do cliente; existe o registro de alegações sem pendência; e a manchete escolhida passa nos seis testes de 10.4. Em setor regulado, a restrição do conselho ou do jurídico já está escrita aqui, não descoberta na véspera.

**Leia:** `references/08-copy-e-oferta.md` (seção 10 inteira). Rode `python3 scripts/checar-texto.py` no copy deck antes de fechar o portão.

### Portão 3. Piso de qualidade medido

Se o usuário indicar páginas de referência, não as olhe apenas. **Meça.**

```js
// extrair estilos computados reais de uma referência
const alvo = document.querySelector('h1');
const c = getComputedStyle(alvo);
({ ff: c.fontFamily, fs: c.fontSize, fw: c.fontWeight, lh: c.lineHeight, ls: c.letterSpacing });
```

Meça: família, peso e tamanho de título e corpo; altura do botão e raio; raio dos cartões; largura do contêiner; cor de fundo e de texto.

**Por que isso importa:** a leitura a olho quase sempre superestima o peso tipográfico. Referências de alto nível costumam usar peso 400 ou 500 em corpo grande, e a reprodução de memória sai em 700 ou 800, que é exatamente o que faz a página parecer template.

**Saída:** tabela de parâmetros numéricos.
**Critério:** zero parâmetro definido por impressão.

**Leia:** `references/02-sistema-de-design.md` (4.6, economia de variáveis), para saber o que medir e quanto variar.

### Portão 4. Tokens e escala

Traduza a ficha do portão 1 em tokens. Defina nesta ordem: neutros, cor de ação, acento, estados. Meça o contraste **antes** de aplicar.

**Saída:** bloco `:root` fechado.
**Critério:** todo par de texto com 4,5:1 ou mais, e nenhuma cor escrita fora do token.

**Leia:** `references/02-sistema-de-design.md` (seção 4). Meça com `python3 scripts/contraste.py tokens.css` antes de aplicar.

### Portão 5. Material visual

Decida a origem de cada imagem antes de montar seção.

**Critério:** nenhuma imagem de banco, nenhuma gerada por IA, e toda imagem pode ser regerada em qualquer tamanho.

**Leia:** `references/05-material-visual.md` (seção 7). Se houver método, processo ou arquitetura para explicar, também `references/07-diagramas.md` (seção 9).

### Portão 6. Componentes antes das seções

Desenhe botão, rótulo, painel, cartão, selo, campo e ícone, com todos os estados.

**Critério:** cada componente tem repouso, hover, foco, ativo e desabilitado. Nenhuma seção inventa componente novo.

**Leia:** `references/03-componentes.md` (seção 5) e os estados de `references/01-craft.md` (2.2 e 2.6). Para formulário, `references/09-conversao.md` (11.5).

### Portão 7. Composição das seções

Monte na ordem que responde às perguntas do leitor, escolhendo o formato de cada seção pelo conteúdo que ela tem (ver 8.1, 8.4 e 8.5) e seguindo o copy deck do portão 2.

**Critério:** desfoque a tela em 10 px. Título e ação principal ainda se identificam, e nenhuma seção parece a anterior.

**Leia:** `references/06-estrutura-e-narrativa.md` (seção 8) e a arquitetura de ação de `references/09-conversao.md` (11.4 a 11.8).

### Portão 8. Movimento

Defina uma curva e duas faixas de duração. Implemente o bloco de movimento reduzido **junto**, nunca depois.

**Critério:** com movimento reduzido ativo, a página aparece completa e legível.

**Leia:** `references/04-movimento.md` (seção 6) e o código pronto de `references/15-codigo-de-referencia.md` (seção 17).

### Portão 9. Responsividade medida

Rode a auditoria por largura da seção 12.7 na bateria completa, incluindo as passadas de zoom de texto a 200% e de movimento reduzido. Corrija e repita até zerar os bloqueantes.

**Critério de saída:** os dez bloqueantes de 12.8 passam em todas as larguras, e as capturas de 360, 1280, 1366 e 1440 foram abertas e olhadas por uma pessoa. Medição não enxerga hierarquia achatada nem espaço morto.

**Leia:** `references/10-responsividade.md` (seção 12). Rode `node scripts/auditar-responsivo.mjs index.html --shots --zoom200 --reduced-motion`.

### Portão 10. QA executado

Rode a verificação da seção 16 em navegador controlado, mais a auditoria de conversão de 11.11 e a revisão de copy de 10.13. Não é leitura de código, é execução.

**Critério:** todos os itens passam antes de mostrar ao usuário.

**Leia:** `references/14-qa-e-erros-comuns.md` (seções 16 e 18), `references/11-acessibilidade.md` (seção 13), `references/12-performance.md` (seção 14), a auditoria de `references/09-conversao.md` (11.11) e a revisão de `references/08-copy-e-oferta.md` (10.13). Rode `python3 scripts/checar-texto.py index.html` no HTML final.

### Portão 11. Refinamento

Um pedido por vez, verificado antes do próximo. Extras só como sugestão.

---

## Quando o pedido é auditar ou redesenhar uma página que já existe

Não comece redesenhando. Meça primeiro, depois proponha.

1. Rode os três scripts na página atual e guarde a saída: `auditar-responsivo.mjs` com `--shots`, `checar-texto.py` e, se houver acesso ao CSS, `contraste.py`.
2. Aplique o teste do slop (1.5), a régua de craft (2.1), a auditoria de conversão (11.11) e a revisão de copy (10.13).
3. Entregue cada achado em uma linha: problema, regra violada com o número da seção, evidência (medida ou captura), correção proposta e como verificar depois.
4. Ordene por impacto na decisão de quem lê a página, não por facilidade de corrigir. Oferta e manchete fracas vêm antes de raio de borda.
5. Para redesenhar, volte ao portão 1 com o que a auditoria revelou. A página nova nasce da identidade do projeto, não da página antiga.

## Mapa das referências

| Arquivo | Seções | Quando abrir |
|---|---|---|
| `references/01-craft.md` | 2 | Régua de acabamento: estados, geometria, tipografia de detalhe, onde craft vira exagero |
| `references/02-sistema-de-design.md` | 4 | Tokens, cor, direções visuais, tipografia, espaço, superfície, economia de variáveis |
| `references/03-componentes.md` | 5 | Assinatura de componente, botão, rótulo, título com destaque, cartões, ícones |
| `references/04-movimento.md` | 6 | Curvas, durações, entrada coreografada, microinterações, movimento reduzido |
| `references/05-material-visual.md` | 7 | Derivar grafismo da marca, texturas procedurais, UI recriada em HTML, imagem de compartilhamento |
| `references/06-estrutura-e-narrativa.md` | 8 | Ordem das seções, catálogo de topos e de seções, bento, como mostrar software sem virar catálogo |
| `references/07-diagramas.md` | 9 | Diagrama e ilustração animada: arquétipo, geometria, conexões, acessibilidade, celular |
| `references/08-copy-e-oferta.md` | 10 | Consciência, posicionamento, manchete, oferta, setor regulado, copy por seção, anti-slop de texto, português |
| `references/09-conversao.md` | 11 | Evidência sobre conversão, arquitetura de ação, formulário, LGPD, prova social, medição, teste A/B |
| `references/10-responsividade.md` | 12 | Breakpoint por conteúdo, container query, tipografia fluida, armadilhas do celular, auditoria e critério de aprovação |
| `references/11-acessibilidade.md` | 13 | Contraste, teclado e foco, ARIA, formulário, critérios WCAG que mais caem |
| `references/12-performance.md` | 14 | Métricas, orçamento, vídeo no topo, compressão, fontes, animação vetorial |
| `references/13-leis-e-principios.md` | 15 | Heurísticas, leis de interação e Gestalt, cada uma com critério de verificação |
| `references/14-qa-e-erros-comuns.md` | 16 e 18 | QA executável, lista de verificação e tabela de erros comuns |
| `references/15-codigo-de-referencia.md` | 17 | Ciclo automático com barra, revelação por palavra, ícones com traço animado, contraste |

## 19. Entrega

Ao terminar, informe:

1. **O que foi construído**, em linguagem simples, seção por seção.
2. **O que foi medido**, com números: menor contraste, larguras testadas, falhas e avisos de cada script, erros de console.
3. **O que ficou pendente** ou depende de decisão do usuário.
4. **O que não foi testado**, com honestidade, incluindo qualquer script que não pôde rodar e o comando para o usuário rodar. Verificação técnica não é teste com usuário, e nenhuma afirmação sobre conversão é verdadeira sem medição.

Nunca apresente a página como validada comercialmente. Ela está tecnicamente correta e visualmente consistente, que é coisa diferente.
