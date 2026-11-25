---
name: loop-de-design
description: >-
  Melhora uma peça a partir de uma referência concreta, com um construtor e
  três críticos independentes até cumprir o pedido, seguir o sistema e vencer
  a comparação visual. Use ao pedir loop de design, ciclo crítico ou iteração
  até atingir o nível de uma referência. Não é uma revisão pontual de acabamento.
license: MIT
metadata:
  author: Felipe Borges
  version: "3.1"
---

# Loop de Design

Quatro fases: entrevista, pré-verificação, desmontagem, ciclo. Não comece a
construir antes de entender o objetivo, abrir a referência e escrever a barra.
Aproveite respostas e autorizações que já estejam na conversa.

## 1. Entrevista

Resolva estas três perguntas juntas. Pergunte somente o que ainda falta; espere
as respostas necessárias antes de seguir.

1. O que você está construindo, e qual o tamanho ou a duração?
2. O que já faz isso muito bem? Uma página, vídeo ou arquivo que eu possa abrir.
   Se não tiver referência, diga “pular”.
3. Há arquivos de base? Sistema de design, marca, roteiro ou versão existente.

Se a referência for vaga (“o site da Apple”, “um bom SaaS”), peça uma vez a
página ou o arquivo específico. Sem referência concreta, o crítico inventa a
comparação e aprova cedo demais.

Se a pessoa disser “pular”, proponha três referências com uma frase de motivo
para cada uma. Dê oportunidade de escolha; sem preferência, use a mais exigente
que seja adequada ao objetivo e informe a escolha.

Escolha de modelos é opcional. Preserve preferências já combinadas; na ausência
delas, use a configuração disponível. Não acrescente um questionário de modelos
ou uma cota padrão de rodadas.

## 2. Pré-verificação

É uma checagem, não outra entrevista. Confirme e relate em um bloco:

- Abra a referência agora: capture ou leia o material real. Se estiver
  inacessível, avise e obtenha uma referência acessível, sem substituir por memória.
- Confirme que consegue renderizar o resultado: capturas de tela para um site,
  uma sequência de frames para animação, páginas renderizadas para um documento.
  Sem renderização, não há avaliação visual.
- Identifique as ferramentas de geração necessárias e confira sua disponibilidade.
- Confira os arquivos de entrada, incluindo o sistema de design.

Diga o que funciona, o que falta e **qual crítico fica sem condição de julgar**.
Não prossiga silenciosamente com um crítico sem condições de observar o resultado.

## 3. Desmontagem

Estude a referência e escreva **5 a 7 mecanismos observáveis** em `bar.md`.
Em projeto existente, reutilize `criterios-de-qualidade.md` se ele já tiver esse
papel: mantenha uma única barra vigente.

Mecanismos, não adjetivos. “Parece premium” não diz o que construir. Exemplos:

- o título tem cinco vezes o tamanho do corpo;
- há uma cor de destaque, restrita às ações;
- o movimento termina sempre na mesma direção;
- nenhuma animação dura menos de 400 ms.

São exemplos de mecanismos a extrair da referência, não regras universais.
Cada linha precisa ser verificável observando o resultado.

Mostre a barra antes de construir. Siga com o escopo já autorizado; só espere
nova resposta se houver uma decisão essencial ainda em aberto.

## 4. Ciclo

Divida o objetivo nas menores partes que possam ser melhoradas e julgadas por
conta própria. Prefira três ou quatro; cada parte adicional multiplica o trabalho.

Para cada parte: delegue a construção a **um agente construtor**; depois abra
**três críticos independentes**, cada um com contexto novo e sem conhecimento
de como o construtor trabalhou.

- **Briefing:** julga somente o pedido. Faz o que foi solicitado? Ignore estética.
- **Sistema:** julga somente `design-system.md`. Verifique aderência objetiva.
- **Visual:** julga somente `bar.md` (ou o equivalente já definido) e o resultado
  renderizado. Coloque nosso resultado ao lado da referência, às cegas e sem
  rótulos de procedência; diga qual é melhor e aponte a maior lacuna.

Escreva as instruções de cada crítico para este objetivo. Não reutilize
instruções genéricas entre objetivos diferentes.

### Regras

- Críticos são duros. Elogios não são úteis.
- Críticos julgam o resultado renderizado, nunca o código. Ler a implementação
  faz o crítico avaliar a intenção em vez do resultado.
- Vereditos binários, **APROVADO ou REPROVADO**, nunca notas. Notas tendem a
  subir a cada rodada.
- Os três precisam aprovar. Qualquer reprovação volta ao construtor com
  **a maior lacuna**, uma só.
- Não há número fixo de rodadas. A saída é vencer ou a pessoa interromper o ciclo.

Mantenha `progresso.md` atualizado: estado de cada parte, veredito de cada
crítico, histórico das lacunas e contagem de rodadas.

## Custo e limites

Não invente custo em tokens. Mostre rodadas executadas e partes concluídas.
Uma rodada global é uma passagem de construção e julgamento das partes pendentes;
não reinicie o contador ao trocar de parte.
Informe no início que o ciclo segue até aprovação e pode ser interrompido.

Se a pessoa definir um teto, respeite-o como ponto de parada: ao atingi-lo,
mostre o que ainda reprova, a maior lacuna e o total executado; peça autorização
antes de ultrapassá-lo. Não multiplique um teto global pelo número de partes.
Limite atingido não transforma reprovação em aprovação. O ciclo não amplia o
escopo nem autoriza gastos ou ações externas além do que foi combinado.

## O que faz o método falhar

- Referência vaga ou examinada superficialmente.
- Construtor julgando o próprio trabalho, ou críticos com contexto contaminado.
- Crítico permissivo, evidência inadequada ou nota subindo sozinha a cada rodada.
- Tratar uma cota como objetivo, ou enfraquecer a barra para caber nela.
- Especificar demais: cada instrução desnecessária tira espaço do julgamento.

## Apoio, somente quando necessário

- Agentes e modelos: [Codex](references/codex.md) ou [Claude Code](references/claude-code.md).
- Extração da barra: [Mecanismos](references/mecanismos.md).
- Captura e comparação: [Renderização](references/renderizacao.md).
- Origem: [Créditos](ATTRIBUTION.md).
