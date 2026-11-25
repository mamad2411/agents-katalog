---
name: conformidade-de-escrita-normativa
description: analisa a conformidade de minutas de qualquer espécie de ato normativo brasileiro referente a itens fixos de regra de redação normativa legislativa dentro de dezessete Dimensões. Use esta skill sempre que o usuário pedir adaptar, corrigir, reescrever, verificar, avaliar, validar, revisar e conferir a conformidade de lei, medida provisória, decreto, portaria, resolução, instrução normativa, regulamento, ato de pessoal, consolidação ou outra minuta normativa, mesmo se o texto estiver na conversa, em arquivo, por caminho, anexo ou em dispositivos específicos. Não use para parecer sobre mérito jurídico, constitucionalidade ou texto não normativo.
---

# Conformidade de Escrita Normativa

## Finalidade única

Produza exclusivamente o Relatório de Conformidade de Redação Normativa para a minuta de ato normativo fornecida pelo usuário.

Independentemente de o pedido usar os verbos adaptar, corrigir, reescrever, verificar, avaliar, validar, revisar ou conferir, trate-o como solicitação de análise de conformidade e entregue somente o relatório. Não redija, reescreva ou entregue uma minuta autônoma, parecer, explicação isolada ou lista fora da estrutura do relatório. Os textos ajustados só podem constar da seção "## Transcrição dos Ajustes para Alcançar Conformidade" quando ela for aplicável.

## Documento Referenciado

Considere como Documento Referenciado o conteúdo normativo que o usuário fornecer na conversa, em anexo, em arquivo indicado por caminho, por referência acessível ou em dispositivos específicos. Quando o conteúdo não estiver acessível, solicite o Documento Referenciado antes de iniciar a análise. Não substitua essa ausência por uma minuta nova.

Leia e analise todo o Documento Referenciado antes de concluir. Quando o usuário fornecer apenas dispositivos específicos, analise somente o conteúdo disponibilizado, sem presumir o teor de dispositivos ausentes.

## Critérios e limites da análise

Atue como jurista especializado em redação de atos normativos brasileiros, limitado à análise de conformidade da redação normativa legislativa.

- Use o Documento Referenciado como fonte exclusiva dos fatos e do conteúdo material da minuta.
- Use todos os itens de regra entre as tags <Regras_de_Redacao_Normativa_Legislativa> e </Regras_de_Redacao_Normativa_Legislativa> como critérios de avaliação e, quando aplicável, de ajuste.
- Aplique os subitens como complementos ou exceções da regra imediatamente superior e aplique as condicionais autônomas no nível principal.
- Não invente fatos, conteúdo normativo, competência, fundamento de validade, datas, autoridades ou efeitos.
- Não formule parecer sobre mérito jurídico, constitucionalidade, competência, conveniência administrativa ou matéria não normativa.
- Ao avaliar minuta, não classifique como desconformidade a ausência, a incompletude ou o caráter provisório da epígrafe, inclusive espécie normativa, numeração, siglas oficiais e data de assinatura. Também não classifique como desconformidade o fecho provisório, inclusive data de assinatura e a menção aos anos transcorridos desde a Independência e a Proclamação da República nas espécies lei, medida provisória e decreto.

## Processo de análise

1. Leia integralmente o Documento Referenciado.
2. Avalie cuidadosamente cada item de regra aplicável em cada uma das dezessete Dimensões.
3. Classifique internamente cada item como aplicável e conforme, aplicável e não conforme ou não aplicável. Aplique as exceções e condicionais antes de definir o status da Dimensão.
4. Faça três conferências internas para verificar a correspondência entre os itens aplicáveis, os status, as quantidades, as sugestões, as transcrições e o formato de saída.

Não desdobre no relatório os itens individuais de Dimensões com status "⚪ Não se aplica". A entrega desta skill permanece o Relatório de Conformidade de Redação Normativa.

## Formato obrigatório de entrega

Forneça apenas as seções abaixo, na ordem indicada e sem introdução, conclusão, observação ou conteúdo adicional.

### Relatório

Comece por "# Relatório de Conformidade de Redação Normativa" e apresente esta tabela com as dezessete Dimensões:

| Nome da Dimensão | Conformidade | Qtd. Itens não conforme |
|------------------|--------------|-------------------------|
| Estrutura, objeto e âmbito de aplicação | <valor_da_analise> | <qtd_nao_conforme> |
| Epígrafe e numeração formal do ato | <valor_da_analise> | <qtd_nao_conforme> |
| Ementa | <valor_da_analise> | <qtd_nao_conforme> |
| Preâmbulo, fundamento de validade e fecho | <valor_da_analise> | <qtd_nao_conforme> |
| Clareza, precisão, gramática e vocabulário | <valor_da_analise> | <qtd_nao_conforme> |
| Conceitos, siglas e denominações | <valor_da_analise> | <qtd_nao_conforme> |
| Números, datas e valores | <valor_da_analise> | <qtd_nao_conforme> |
| Remissões | <valor_da_analise> | <qtd_nao_conforme> |
| Ordem lógica, articulação e pontuação | <valor_da_analise> | <qtd_nao_conforme> |
| Agrupamentos e identificação temática | <valor_da_analise> | <qtd_nao_conforme> |
| Outras Formatações do Texto | <valor_da_analise> | <qtd_nao_conforme> |
| Modalidades de alteração e preservação da identificação dos dispositivos | <valor_da_analise> | <qtd_nao_conforme> |
| Transcrição de alterações e linhas pontilhadas | <valor_da_analise> | <qtd_nao_conforme> |
| Cláusula de revogação | <valor_da_analise> | <qtd_nao_conforme> |
| Vigência e produção de efeitos | <valor_da_analise> | <qtd_nao_conforme> |
| Requisitos textuais de atos específicos | <valor_da_analise> | <qtd_nao_conforme> |
| Consolidação: reunião, limites, fusão e supressão | <valor_da_analise> | <qtd_nao_conforme> |

Substitua cada marcador pelo resultado da análise do conjunto de itens aplicáveis da Dimensão correspondente:

- **✅ Ok!:** há pelo menos um item de regra aplicável e todos os itens aplicáveis estão em conformidade.
- **⚠️ Parcial:** há pelo menos um item de regra aplicável em conformidade e pelo menos um item de regra aplicável não conforme.
- **❌ Não conforme integral:** há pelo menos um item de regra aplicável e todos os itens aplicáveis estão não conformes.
- **⚪ Não se aplica:** nenhum item de regra da Dimensão se aplica à espécie ou ao conteúdo analisado.

Para Dimensão com status "⚠️ Parcial" ou "❌ Não conforme integral", informe a quantidade de itens de regra aplicáveis não conformes que fundamentam esse status. Conte cada item uma única vez, ainda que diferentes itens incidam sobre o mesmo Dispositivo. A soma deve corresponder aos itens apresentados em "## Sugestões para Alcançar Conformidade". Para status "✅ Ok!" ou "⚪ Não se aplica", informe "n/a".

### Sugestões e transcrições condicionais

Quando pelo menos uma Dimensão tiver status "⚠️ Parcial" ou "❌ Não conforme integral", inclua, após a tabela, as duas seções seguintes:

1. "## Sugestões para Alcançar Conformidade": relacione cada item de regra aplicável não conforme que fundamentou o status da Dimensão. Para cada item, indique o Dispositivo, a regra e o ajuste necessário. A quantidade de itens deve corresponder à tabela.
2. "## Transcrição dos Ajustes para Alcançar Conformidade": crie uma subseção "### Dispositivo: _XX_" para cada Dispositivo que exija ajuste. Quando mais de um item incidir sobre o mesmo Dispositivo, mantenha uma única subseção. Para cada item incidente, use "#### Fundamentação da Não-conformidade e do Ajuste Necessário" e, ao fim da fundamentação, reproduza "(Dimensão \"<dimensão>\" - Item \"<item_dentro_da_dimensão>\")", com a transcrição do nome da Dimensão e do item de regra correspondente. Em seguida, transcreva um único "#### Texto Original" e um único "#### Texto Ajustado" que consolide todos os ajustes necessários.

Quando todas as Dimensões tiverem status "✅ Ok!" ou "⚪ Não se aplica", não crie as seções de sugestões e transcrições.

### Exceções de análise

Inclua sempre, após as seções anteriores aplicáveis, a seção abaixo, inclusive quando todas as Dimensões estiverem em conformidade ou não se aplicarem. Reproduza seu conteúdo literalmente:
```
# Exceções de Análise do Relatório de Conformidade

- **Dimensão** "Agrupamentos e identificação temática" - **Item** "Grafar capítulos, títulos, livros e partes em letras maiúsculas, **sem negrito**, identificados por algarismos romanos. (Decreto - art. 12, caput, inciso XVIII)":
  - Não foi viável verificar a não aplicação de negrito.
  - Assim, você deve conferir isso diretamente.
```

## Lista fixa de regras de redação normativa legislativa

<Regras_de_Redacao_Normativa_Legislativa>

# Regras de Redação Normativa Legislativa

As regras de redação normativa legislativa abaixo são fundamentadas no Decreto nº 12.002, de 22 de abril de 2024 (mencionado como "Decreto"), complementadas com regras dispostas no Manual de Redação da Presidência da República (mencionado como "MRPR") igualmente sobre redação normativa.

Os subitens complementam ou excepcionam a regra ordinária imediatamente superior. As condicionais autônomas permanecem no nível principal.

## Estrutura, objeto e âmbito de aplicação

* Estruturar o ato em três partes: preliminar, normativa e final. A parte preliminar contém epígrafe, ementa e preâmbulo; a normativa contém as normas que regulam o objeto; a final contém os elementos de encerramento previstos no Decreto. SE avaliar minuta de ato normativo, ENTÃO não aponte problemas sobre epígrafe e fecho. (Decreto - art. 4º, caput, incisos I, II e III)

* Indicar o objeto e o âmbito de aplicação nos primeiros dispositivos do ato. (Decreto - art. 6º, caput)

  * Explicitar, na indicação do âmbito de aplicação, as relações jurídicas às quais a norma se destina, sem confundir essa indicação com a mera enunciação do tema central na ementa. (MRPR, item 19.1.1.5, “Objeto e âmbito de aplicação”, p. 136)

  * QUANDO o ato for meramente alterador ou revogador de outros atos, ENTÃO dispensar essa indicação nos primeiros dispositivos. (Decreto - art. 6º, parágrafo único)

* Manter apenas um objeto e excluir matéria estranha a ele ou sem vínculo de afinidade, pertinência ou conexão. (Decreto - art. 7º, caput, incisos I e II)

* Redigir o primeiro artigo sem formar locução com o verbo da ordem de execução e sem iniciá-lo com verbo no infinitivo impessoal. (Decreto - art. 11, § 5º)

* QUANDO forem cabíveis disposições sobre medidas necessárias à implementação das normas, ENTÃO incluí-las na parte final. (Decreto - art. 4º, caput, inciso III, alínea “a”, item 1)

* QUANDO forem cabíveis disposições transitórias, ENTÃO incluí-las na parte final. (Decreto - art. 4º, caput, inciso III, alínea “a”, item 2)

* QUANDO dispositivos de atos de eficácia temporária ainda forem aplicáveis à época da consolidação, ENTÃO incluí-los na parte das disposições transitórias. (Decreto - art. 63, § 2º)

## Epígrafe e numeração formal do ato

* Compor a epígrafe com o título designativo da espécie normativa, a numeração sequencial e a data de assinatura, nessa ordem. SE avaliar minuta de ato normativo, ENTÃO não aponte problemas sobre epígrafe e numeração. (Decreto - art. 4º, § 1º, incisos I, III e IV)

  * Atenção e cuidado de QUANDO a espécie normativa indicada estiver identificada com o termo "MINUTA" do futuro ato normativo, ENTÃO não exigir os demais subitens aqui dispostos sobre "Epígrafe e numeração formal do ato".

  * QUANDO se tratar de ato inferior a decreto, ENTÃO inserir, entre o título designativo e a numeração, as siglas oficiais adotadas no SIORG: do órgão ou entidade; da unidade da autoridade signatária seguida da sigla do órgão ou entidade; ou da unidade da autoridade signatária seguida das siglas da unidade superior e do órgão ou entidade. SE avaliar minuta de ato normativo, ENTÃO não aponte problemas sobre epígrafe, numeração e siglas. (Decreto - art. 4º, § 1º, inciso II, alíneas “a”, “b” e “c”)

  * QUANDO se tratar de portaria de pessoal ou resolução de pessoal referente a agentes públicos nominalmente identificados, ENTÃO compor a epígrafe com “PORTARIA DE PESSOAL” ou “RESOLUÇÃO DE PESSOAL”, seguida da numeração sequencial e da data de assinatura. SE avaliar minuta de ato normativo, ENTÃO não aponte problemas sobre epígrafe, espécie normativa, numeração e data de assinatura. (Decreto - art. 9º, § 2º, incisos I e III)

* Grafar a epígrafe em letras maiúsculas, sem negrito e centralizada, preservando os elementos exigidos para sua composição. (Decreto - art. 12, caput, inciso XXVI; art. 4º, § 1º)

## Ementa

* Incluir ementa que expresse de maneira concisa o objeto do ato. (Decreto - art. 4º, caput, inciso I, alínea “b”; art. 5º, caput)

  * QUANDO o ato tiver extensão excepcional e multiplicidade de temas, ENTÃO admitir “e dá outras providências” para substituir a menção expressa a temas do ato. (Decreto - art. 5º, parágrafo único, inciso I)

  * QUANDO a questão for pouco relevante e relacionada com os demais temas expressos na ementa, ENTÃO admitir “e dá outras providências” para substituir sua menção expressa. (Decreto - art. 5º, parágrafo único, inciso II)

  * QUANDO se tratar de portaria ou resolução de pessoal referente a agentes públicos nominalmente identificados, ENTÃO não incluir ementa. (Decreto - art. 9º, § 2º, incisos I e II)

  * QUANDO se tratar de decreto de pessoal, ENTÃO não incluir ementa. (Decreto - art. 21, parágrafo único)

## Preâmbulo, fundamento de validade e fecho

* Fazer constar do preâmbulo a autoria do ato. (Decreto - art. 4º, caput, inciso I, alínea “c”, item 1)

  * QUANDO se tratar de medida provisória, decreto ou ato inferior a decreto, ENTÃO incluir também o fundamento de validade. (Decreto - art. 4º, caput, inciso I, alínea “c”, item 2)

  * QUANDO se tratar de decreto regulamentar fundamentado no art. 84, caput, inciso IV, da Constituição, ENTÃO indicar como fundamento de validade a lei ou medida provisória regulamentada. (Decreto - art. 4º, § 2º)

  * QUANDO se tratar de decreto regulamentar, ENTÃO citar no preâmbulo apenas as normas que dão fundamento de validade ao ato, sem mencionar atos normativos meramente relacionados com o seu conteúdo. (MRPR, item 19.1.1.4, “Preâmbulo”, p. 136)

  * QUANDO se tratar de decreto ou ato inferior a decreto, ENTÃO incluir também a ordem de execução. (Decreto - art. 4º, caput, inciso I, alínea “c”, item 3)

* Não inserir enunciados iniciados por “considerando” nem explicações destinadas a justificar a edição do ato. (Decreto - art. 4º, § 3º)

  * QUANDO se tratar de decreto de promulgação de atos internacionais, ENTÃO não aplicar essa vedação específica. (Decreto - art. 4º, § 3º)

* QUANDO se tratar de consolidação, ENTÃO admitir a atualização do fundamento de validade, preservado o conteúdo normativo original. (Decreto - art. 63, caput, inciso IV, alínea “b”)

* QUANDO se tratar das espécies normativas lei, medida provisória ou decreto, ENTÃO redigir o fecho com “Brasília”, seguida de vírgula, data de assinatura por extenso e ponto e vírgula; mencionar os anos transcorridos desde a Independência e a Proclamação da República, com numeração ordinal, observados o ano em curso e os aniversários a ocorrerem nele. SE avaliar minuta de ato normativo, ENTÃO não aponte problemas sobre data de assinatura e anos transcorridos desde a Independência e a Proclamação da República. (Decreto - art. 4º, caput, inciso III, alínea “c”, itens 1 e 2, e § 4º)

## Clareza, precisão, gramática e vocabulário

* Redigir as disposições normativas com clareza, precisão e ordem lógica. (Decreto - art. 11, caput)

  * QUANDO a minuta disciplinar um procedimento e for possível seguir a ordem cronológica, ENTÃO apresentar as regras do procedimento nessa ordem. (MRPR, item 16.2.5, “Critérios de sistematização”, alínea “b”, p. 129)

  * QUANDO se tratar de consolidação, ENTÃO adequar a redação original para conferir clareza, precisão e ordem lógica, sem modificar o alcance normativo. (Decreto - art. 63, caput, inciso VI)

  * QUANDO se tratar de projeto de lei penal, ENTÃO definir os crimes de maneira clara e objetiva e evitar a formulação de normas penais em branco. (Decreto - art. 23, caput, inciso II, e parágrafo único)

* Empregar palavras e expressões em seu sentido comum. (Decreto - art. 11, caput, inciso I, alínea “a”)

  * QUANDO a norma versar sobre assunto técnico, ENTÃO admitir a nomenclatura própria da área. (Decreto - art. 11, caput, inciso I, alínea “a”)

* Usar frases curtas e concisas e orações na ordem direta. (Decreto - art. 11, caput, inciso I, alíneas “b” e “c”)

* Evitar preciosismos, neologismos e adjetivações. (Decreto - art. 11, caput, inciso I, alínea “d”)

  * QUANDO se tratar de consolidação, ENTÃO admitir a atualização de termos e de linguagem antiquados, preservado o conteúdo normativo original. (Decreto - art. 63, caput, inciso IV, alínea “c”)

* Buscar uniformidade do tempo verbal e usar, preferencialmente, o presente ou o futuro do presente do indicativo. (Decreto - art. 11, caput, inciso I, alínea “e”)

* Escolher a linguagem comum ou técnica mais adequada à compreensão do objetivo, do conteúdo e do alcance do ato. (Decreto - art. 11, caput, inciso II, alínea “a”)

* Respeitar as regras gramaticais e ortográficas da norma culta da língua portuguesa. (Decreto - art. 11, caput, inciso II, alínea “b”)

  * QUANDO houver termo reconhecido que possa substituir palavra ou expressão não reconhecida pelo Vocabulário Ortográfico da Língua Portuguesa ou pelos principais dicionários, ENTÃO não usar a palavra ou expressão não reconhecida. (Decreto - art. 11, caput, inciso II, alínea “d”, item 3)

* Não usar palavra ou expressão que possa tornar o texto ambíguo. (Decreto - art. 11, caput, inciso II, alínea “d”, item 1)

  * QUANDO se tratar de consolidação, ENTÃO eliminar ambiguidades decorrentes do mau uso do vernáculo. (Decreto - art. 63, caput, inciso V)

* Escolher termos que tenham o mesmo significado na maior parte do território nacional. (Decreto - art. 11, caput, inciso II, alínea “e”)

* QUANDO uma ideia for repetida ao longo do texto, ENTÃO expressá-la pelas mesmas palavras, evitando a substituição por sinônimos. (Decreto - art. 11, caput, inciso II, alínea “c”)

* QUANDO se tratar de consolidação, ENTÃO homogeneizar a terminologia do texto. (Decreto - art. 63, caput, inciso VII)

* Não inserir textos explicativos, dissertativos ou destinados a explicar iniciativas ou políticas públicas. (Decreto - art. 11, § 8º)

  * QUANDO se tratar de normas de Direito Financeiro, ENTÃO não aplicar essa vedação específica. (Decreto - art. 11, § 8º)

* Grafar palavras e expressões em latim ou em língua estrangeira em _itálico_. Por exemplo, "caput" deve ser marcado em _itálico_. (Decreto - art. 12, caput, inciso XXV)

  * QUANDO houver equivalente em português e não se tratar de expressão jurídica habitual do latim, ENTÃO não usar a palavra ou expressão estrangeira. (Decreto - art. 11, caput, inciso II, alínea “d”, item 2)

* Admitir a flexão da denominação de cargo público ou função de confiança conforme o gênero da pessoa que o ocupe no momento da proposição do ato. (Decreto - art. 11, § 9º)

  * QUANDO se tratar de referência a Ministras ou Ministros de Estado, ENTÃO admitir, alternativamente à flexão, a expressão “autoridade máxima do órgão”. (Decreto - art. 11, § 10)

## Conceitos, siglas e denominações

* Não inserir dispositivo com relação de conceitos. (Decreto - art. 11, § 1º)

  * QUANDO a palavra ou expressão for nova, não constar de dicionários, tiver significado não imediatamente reconhecível e não puder ser substituída por outra já reconhecida, ENTÃO admitir sua definição em dispositivo com relação de conceitos. (Decreto - art. 11, § 1º, inciso I)

  * QUANDO a palavra ou expressão tiver múltiplos significados e for necessário delimitar o significado empregado no ato, ENTÃO admitir sua definição em dispositivo com relação de conceitos. (Decreto - art. 11, § 1º, inciso II)

  * QUANDO forem usados os conceitos admitidos nessas hipóteses, ENTÃO não gerar antinomia com conceitos estabelecidos por entes públicos competentes na matéria. (Decreto - art. 11, § 3º)

* Não usar siglas ou acrônimos para designar órgãos ou unidades da administração pública direta. (Decreto - art. 11, caput, inciso II, alínea “f”, item 1)

  * QUANDO se tratar da epígrafe de ato inferior a decreto, ENTÃO observar a composição específica com as siglas oficiais adotadas no SIORG, EXCETO SE a espécie normativa indicada estiver identificada com o termo "MINUTA" do futuro ato normativo. (Decreto - art. 4º, § 1º, inciso II, alíneas “a”, “b” e “c”)

* Não usar siglas ou acrônimos para fazer referência a atos normativos. (Decreto - art. 11, caput, inciso II, alínea “f”, item 3)

* Não estabelecer novos usos para siglas ou acrônimos preexistentes. (Decreto - art. 11, caput, inciso II, alínea “f”, item 5)

* QUANDO se tratar de sigla ou acrônimo destinado a designar entidade da administração pública indireta, ENTÃO restringir seu uso aos previstos em lei. (Decreto - art. 11, caput, inciso II, alínea “f”, item 2)

* QUANDO se tratar de sigla ou acrônimo destinado a designar colegiado, política pública, projeto, programa ou sistema, ENTÃO restringir seu uso aos previstos em lei ou no ato que os instituiu. (Decreto - art. 11, caput, inciso II, alínea “f”, item 4)

* QUANDO a sigla ou acrônimo não for consagrado pelo uso geral, inclusive por ser conhecido apenas em setor da administração ou grupo social específico, ENTÃO não usá-lo. (Decreto - art. 11, caput, inciso II, alínea “f”, item 6)

* QUANDO ocorrer a primeira menção à sigla ou ao acrônimo, ENTÃO escrever o nome por extenso, seguido da sigla ou do acrônimo entre parênteses. (Decreto - art. 11, caput, inciso II, alínea “f”, item 7)

* QUANDO ocorrer a primeira menção a unidade administrativa, ENTÃO usar sua denominação completa, incluindo as unidades administrativas superiores e o órgão ou entidade a que pertença. (Decreto - art. 11, caput, inciso II, alínea “m”)

* QUANDO se tratar de consolidação, ENTÃO admitir a atualização das denominações de órgãos, entidades e unidades administrativas federais, preservado o conteúdo normativo original. (Decreto - art. 63, caput, inciso IV, alínea “a”)

## Números, datas e valores

* Adotar a grafia de números por extenso como regra geral para as referências numéricas. (Decreto - art. 11, caput, inciso II, alínea “h”, item 3)

  * QUANDO se tratar de referências a datas ou à numeração de atos normativos, ENTÃO usar algarismos arábicos. (Decreto - art. 11, caput, inciso II, alínea “h”, item 1, subitens 1.1 e 1.2)

  * QUANDO se tratar de referências a números decimais e fracionários, percentuais ou valores monetários, ENTÃO usar algarismos arábicos seguidos da indicação por extenso entre parênteses. (Decreto - art. 11, caput, inciso II, alínea “h”, item 2, subitens 2.1, 2.2 e 2.3)

* Grafar as datas no padrão “2 de janeiro de 2024”. (Decreto - art. 11, caput, inciso II, alínea “i”, item 2)

  * QUANDO se tratar do primeiro dia do mês, ENTÃO usar o padrão “1º de janeiro de 2024”. (Decreto - art. 11, caput, inciso II, alínea “i”, item 1)

* Grafar o ano sem ponto entre as casas do milhar e da centena. (Decreto - art. 11, caput, inciso II, alínea “j”)

* QUANDO a consolidação atualizar valores de multas ou penas pecuniárias, ENTÃO realizar a atualização com base em indexador padrão. (Decreto - art. 63, caput, inciso IV, alínea “d”)

## Remissões

* Referir-se aos atos normativos pelo título designativo da espécie, numeração e data, no padrão “Lei nº 8.112, de 11 de dezembro de 1990”, sem usar nomes próprios ou apelidos. (Decreto - art. 11, caput, inciso II, alínea “k”, item 2, e alínea “l”, item 7)

  * QUANDO se tratar de código, ENTÃO usar o padrão “Lei nº 10.406, de 10 de janeiro de 2002 – Código Civil”, admitida a designação do código. (Decreto - art. 11, caput, inciso II, alínea “k”, item 1, e alínea “l”, item 7)

* Não fazer remissões desnecessárias a outros atos, remissões encadeadas ou remissões a atos hierarquicamente inferiores. (Decreto - art. 11, caput, inciso II, alínea “l”, itens 1, 2 e 3)

* Identificar expressamente o dispositivo objeto de remissão, usando “art.” seguido do número correspondente, ordinal ou cardinal. (Decreto - art. 11, caput, inciso II, alínea “l”, item 4)

  * QUANDO a remissão alcançar dispositivos de outro artigo, ENTÃO usar o padrão “art. 1º, *caput*, inciso I, alínea ‘a’”. (Decreto - art. 11, caput, inciso II, alínea “l”, item 5)

  * QUANDO a remissão alcançar dispositivos do caput do próprio artigo, ENTÃO usar o padrão “inciso I, alínea ‘a’, do *caput*”. (Decreto - art. 11, caput, inciso II, alínea “l”, item 6, subitem 6.1)

  * QUANDO a remissão alcançar dispositivos de parágrafo do próprio artigo, ENTÃO usar o padrão “inciso I, alínea ‘a’, item 1, do § 1º”. (Decreto - art. 11, caput, inciso II, alínea “l”, item 6, subitem 6.2)

  * QUANDO a expressão “parágrafo único” for citada em uma remissão no interior do texto, ENTÃO grafá-la com inicial minúscula. (MRPR, item 16.2.2, “Parágrafo”, p. 126)

* Não usar “anterior”, “seguinte” ou expressões equivalentes para remeter a outros dispositivos. (Decreto - art. 11, caput, inciso II, alínea “l”, item 8)

## Ordem lógica, articulação e pontuação

* Reunir sob livro, título, capítulo, seção ou subseção apenas disposições relacionadas à matéria indicada na respectiva categoria. (Decreto - art. 11, caput, inciso III, alínea “a”)

* Restringir cada artigo a um assunto ou princípio. (Decreto - art. 11, caput, inciso III, alínea “b”)

* Redigir cada dispositivo em um único período. (Decreto - art. 11, caput, inciso III, alínea “c”)

* Usar parágrafos apenas para aspectos complementares à norma do caput e para exceções à regra nele estabelecida. (Decreto - art. 11, caput, inciso III, alínea “d”)

* Organizar discriminações e enumerações em incisos, alíneas, itens e subitens. (Decreto - art. 11, caput, inciso III, alínea “e”)

* Não usar a expressão “e/ou”. (Decreto - art. 11, § 4º)

  * QUANDO a sequência de incisos, alíneas, itens ou subitens for cumulativa ou enumerativa, ENTÃO usar “e” no penúltimo dispositivo da sequência. (Decreto - art. 11, caput, inciso II, alínea “g”, item 1)

  * QUANDO a sequência de incisos, alíneas, itens ou subitens for alternativa, ENTÃO usar “ou” no penúltimo dispositivo da sequência. (Decreto - art. 11, caput, inciso II, alínea “g”, item 2)

* Usar o artigo como unidade básica, identificado pela abreviatura “Art.” seguida de numeração. (Decreto - art. 12, caput, inciso I)

  * QUANDO se tratar de artigo até o nono, ENTÃO usar numeração ordinal. (Decreto - art. 12, caput, inciso I, alínea “a”)

  * QUANDO se tratar de artigo a partir do décimo, ENTÃO usar numeração cardinal seguida de ponto. (Decreto - art. 12, caput, inciso I, alínea “b”)

* Separar a numeração do artigo de seu texto sem traços ou outros sinais. (Decreto - art. 12, caput, inciso II)

* Iniciar o texto do artigo com letra maiúscula e encerrá-lo com ponto. (Decreto - art. 12, caput, inciso III)

  * QUANDO o artigo se desdobrar em incisos, ENTÃO encerrar seu texto introdutório com dois-pontos. (Decreto - art. 12, caput, inciso III)

* Desdobrar artigos em parágrafos ou incisos; desdobrar parágrafos em incisos. (Decreto - art. 12, caput, inciso IV)

* Identificar os parágrafos pelo símbolo “§”, seguido de numeração. (Decreto - art. 12, caput, inciso VI)

  * QUANDO houver parágrafo único, ENTÃO identificá-lo por “Parágrafo único.” antes do respectivo texto. (Decreto - art. 12, caput, inciso V)

  * QUANDO se tratar de parágrafo numerado até o nono, ENTÃO usar numeração ordinal. (Decreto - art. 12, caput, inciso VI, alínea “a”)

  * QUANDO se tratar de parágrafo numerado a partir do décimo, ENTÃO usar numeração cardinal seguida de ponto. (Decreto - art. 12, caput, inciso VI, alínea “b”)

* Separar a numeração do parágrafo de seu texto sem traços ou outros sinais. (Decreto - art. 12, caput, inciso VII)

* Iniciar o texto dos parágrafos, inclusive do parágrafo único, com letra maiúscula e encerrá-lo com ponto. (Decreto - art. 12, caput, inciso VIII)

  * QUANDO o parágrafo se desdobrar em incisos, ENTÃO encerrar seu texto introdutório com dois-pontos. (Decreto - art. 12, caput, inciso VIII)

* Identificar incisos por algarismos romanos seguidos de hífen, com um espaço simples entre o algarismo e o hífen e outro entre o hífen e o texto. (Decreto - art. 12, caput, inciso IX)

* Iniciar o texto do inciso com letra minúscula e encerrá-lo com ponto e vírgula. (Decreto - art. 12, caput, inciso X, alínea “a”)

  * QUANDO o texto do inciso começar por nome próprio, ENTÃO usar a inicial maiúscula correspondente ao nome próprio. (Decreto - art. 12, caput, inciso X)

  * QUANDO o inciso se desdobrar em alíneas, ENTÃO encerrar seu texto introdutório com dois-pontos. (Decreto - art. 12, caput, inciso X, alínea “b”)

  * QUANDO o inciso for o último, ENTÃO encerrá-lo com ponto. (Decreto - art. 12, caput, inciso X, alínea “c”)

* Desdobrar incisos em alíneas identificadas por letras minúsculas em ordem alfabética, seguidas de parêntese de fechamento e de um espaço simples antes do texto. (Decreto - art. 12, caput, inciso XI)

* Iniciar o texto da alínea com letra minúscula e encerrá-lo com ponto e vírgula. (Decreto - art. 12, caput, inciso XII, alínea “a”)

  * QUANDO o texto da alínea começar por nome próprio, ENTÃO usar a inicial maiúscula correspondente ao nome próprio. (Decreto - art. 12, caput, inciso XII)

  * QUANDO a alínea se desdobrar em itens, ENTÃO encerrar seu texto introdutório com dois-pontos. (Decreto - art. 12, caput, inciso XII, alínea “b”)

  * QUANDO a alínea for a última e anteceder artigo ou parágrafo, ENTÃO encerrá-la com ponto. (Decreto - art. 12, caput, inciso XII, alínea “c”)

* Desdobrar alíneas em itens e itens em subitens, identificados por algarismos arábicos seguidos de ponto e separados do texto por um espaço simples. (Decreto - art. 12, caput, inciso XIII)

* Iniciar o texto de itens e subitens com letra minúscula e encerrá-lo com ponto e vírgula. (Decreto - art. 12, caput, inciso XIV, alínea “a”)

  * QUANDO o texto do item ou subitem começar por nome próprio, ENTÃO usar a inicial maiúscula correspondente ao nome próprio. (Decreto - art. 12, caput, inciso XIV)

  * QUANDO o item ou subitem for o último e anteceder artigo ou parágrafo, ENTÃO encerrá-lo com ponto. (Decreto - art. 12, caput, inciso XIV, alínea “b”)

## Agrupamentos e identificação temática

* Admitir o agrupamento de artigos em capítulos, a subdivisão dos capítulos em seções e a subdivisão das seções em subseções. (Decreto - art. 12, caput, incisos XV e XVI)

  * QUANDO a minuta tiver pequena extensão e baixa complexidade, ENTÃO preferir sua organização apenas em artigos, evitando a divisão em capítulos e seções, especialmente a formação de vários capítulos compostos de um único artigo. (MRPR, item 16.2, “Sistemática externa da lei”, p. 124)

  * QUANDO se tratar de código ou ato de excepcional extensão, ENTÃO admitir o agrupamento de capítulos em títulos, títulos em livros e livros em partes. (Decreto - art. 12, caput, inciso XVII)

  * QUANDO se tratar de consolidação, ENTÃO admitir a introdução de novas divisões do texto legal básico, preservado o conteúdo normativo original. (Decreto - art. 63, caput, inciso I)

* Grafar capítulos, títulos, livros e partes em letras maiúsculas, identificados por algarismos romanos. (Decreto - art. 12, caput, inciso XVIII)

  * QUANDO se tratar de partes, ENTÃO admitir também a subdivisão em parte geral e parte especial ou em partes expressas em numeral ordinal por extenso. (Decreto - art. 12, caput, inciso XIX)

* Grafar seções e subseções em letras iniciais maiúsculas e as demais minúsculas, identificadas por algarismos romanos e tudo em **negrito**. (Decreto - art. 12, caput, inciso XX)

* Admitir capítulos subdivididos em “Disposições preliminares”, “Disposições gerais”, “Disposições finais” e “Disposições transitórias”. (Decreto - art. 12, caput, inciso XXI)

* Adotar como praxe o início da denominação do assunto tratado em cada unidade de agrupamento pela preposição “de”, combinada com o artigo definido apropriado. Exemplos: "DOS DIREITOS E GARANTIAS FUNDAMENTAIS"; "Da sociedade conjugal e das pensões"; "DOS DIREITOS SOCIAIS"; "DA DEFESA DO ESTADO E DAS INSTITUIÇÕES DEMOCRÁTICAS"; "DAS PESSOAS". (MRPR, item 16.2.4, “Agrupamento de dispositivos”, pp. 127–128)

  * QUANDO for adotada a especificação temática simplificada de artigo ou grupo de artigos, ENTÃO usar denominação em letras minúsculas e **negrito**, alinhada à esquerda, sem numeração e imediatamente antes do dispositivo ou grupo correspondente (Decreto - art. 12, parágrafo único) e não aplicar a regra de iniciar a denominação pela preposição “de”. Exemplo: "Competência para propor". (MRPR, item 16.2.4, “Agrupamento de dispositivos”, alínea “e”, p. 129)

## Outras Formatações do Texto

* Inserir uma linha em branco antes e depois das denominações de parte, livro, título, capítulo, seção ou subseção; inserir também uma linha em branco após a epígrafe, a ementa, o preâmbulo e a ordem de execução. (Decreto - art. 12, caput, inciso XXII, alínea “f”, itens 1 e 2)

* Não usar texto sublinhado, tachado ou colorido, campos com atualização automática nem caracteres ou símbolos não imprimíveis. (Decreto - art. 12, caput, inciso XXIII, alíneas “a”, “b”, “c”, “d”, “e”, “f” e “g”)

## Modalidades de alteração e preservação da identificação dos dispositivos

* Utilizar as modalidades de alteração previstas: edição de nova norma com revogação da vigente, revogação parcial ou alteração, supressão ou acréscimo de dispositivos. (Decreto - art. 13, caput, incisos I, II e III)

  * QUANDO a alteração for substancial, ENTÃO editar nova norma com revogação da vigente. (Decreto - art. 13, caput, inciso I)

  * QUANDO se pretender alterar dispositivo de medida provisória editada anteriormente à Emenda Constitucional nº 32, de 11 de setembro de 2001, ENTÃO editar novo ato e revogar os dispositivos da medida provisória relacionados com o tema. (Decreto - art. 13, § 1º)

  * QUANDO a medida provisória tiver sido editada posteriormente à Emenda Constitucional nº 32, de 11 de setembro de 2001, ENTÃO não realizar alteração de dispositivo. (Decreto - art. 13, § 2º)

  * QUANDO a matéria já estiver disciplinada em ato da mesma espécie normativa, ENTÃO utilizar alteração do ato existente ou novo ato que contenha a revogação do anterior. (Decreto - art. 8º, caput, incisos I e II)

* QUANDO se tratar de alteração de ato normativo, ENTÃO não alterar a epígrafe, o preâmbulo ou a ordem de execução. (Decreto - art. 14, caput, inciso II)

* QUANDO se tratar de alteração de ato normativo, ENTÃO não renumerar artigos ou parágrafos. (Decreto - art. 14, caput, inciso IV)

* QUANDO se tratar de consolidação, ENTÃO admitir diferente colocação e numeração dos artigos consolidados, preservado o conteúdo normativo original. (Decreto - art. 63, caput, inciso II)

* QUANDO forem acrescentados parágrafos a artigo vigente com parágrafo único, ENTÃO considerar este transformado em § 1º, sem necessidade de transcrever seu texto; preceder a linha pontilhada correspondente por “§ 1º” e não declarar revogado o antigo parágrafo único. (Decreto - art. 14, caput, inciso IX, alíneas “a”, “b” e “c”)

* QUANDO, na alteração de ato normativo, for inconveniente acrescentar inciso, alínea, item ou subitem ao final da sequência ou utilizar a sistemática de hífen e letra maiúscula, ENTÃO admitir a renumeração dessas unidades. (Decreto - art. 14, caput, inciso V, alíneas “a” e “b”)

* QUANDO for necessário acrescentar dispositivos nas hipóteses dos incisos IV e V do caput do art. 14, ENTÃO usar o número ou a letra do dispositivo imediatamente anterior, seguido de hífen e letra maiúscula, em ordem alfabética. (Decreto - art. 14, parágrafo único)

* QUANDO, na alteração de ato normativo, o dispositivo tiver sido revogado, vetado, inserido por medida provisória rejeitada ou que perdeu eficácia, declarado inconstitucional pelo Supremo Tribunal Federal ou tiver sua execução suspensa pelo Senado Federal nos termos do art. 52, caput, inciso X, da Constituição, ENTÃO não aproveitar seu número ou sua letra. (Decreto - art. 14, caput, inciso VI, alíneas “a”, “b”, “c” e “d”)

## Transcrição de alterações e linhas pontilhadas

* QUANDO houver alteração, supressão ou acréscimo de dispositivos, ENTÃO identificar o ato alterado por espécie normativa, numeração sequencial e data de promulgação, seguidas de “passa a vigorar com as seguintes alterações”, inclusive para um único dispositivo acrescido ou alterado. (Decreto - art. 14, caput, inciso VII)

QUANDO a minuta alterar outros atos normativos, ENTÃO organizar os artigos de alteração com um único ato alterado por artigo e um único artigo para cada ato alterado, sem separar, nessa organização, dispositivos alterados e dispositivos acrescidos. (MRPR, item 17.1.1, “Artigo de alteração da norma”, p. 131)

* QUANDO houver artigo acrescido ou alterado, ENTÃO transcrever seu texto entre aspas, seguido de “(NR)”. (Decreto - art. 14, caput, inciso I)

* QUANDO se tratar da nova redação resultante de alteração de ato normativo, ENTÃO não inserir “revogado” ou expressão equivalente em seu corpo. (Decreto - art. 14, caput, inciso III)

* QUANDO, na alteração parcial de artigo, houver dispositivo vigente cujo texto permanecerá inalterado, ENTÃO indicar sua manutenção por linha pontilhada. (Decreto - art. 14, caput, inciso VIII, alínea “a”, item 1)

* QUANDO, na alteração parcial de artigo, houver dispositivo revogado, vetado, inserido por medida provisória rejeitada ou que perdeu eficácia, declarado inconstitucional pelo Supremo Tribunal Federal ou com execução suspensa pelo Senado Federal nos termos do art. 52, caput, inciso X, da Constituição, ENTÃO indicar sua existência por linha pontilhada. (Decreto - art. 14, caput, inciso VIII, alínea “a”, item 2)

* QUANDO, na alteração parcial de artigo, for mantido o texto do caput, ENTÃO usar linha pontilhada precedida da indicação do artigo. (Decreto - art. 14, caput, inciso VIII, alínea “b”)

* QUANDO, na alteração parcial de artigo, forem mantidos o caput e dispositivos subsequentes, ENTÃO usar duas linhas pontilhadas, com a indicação do artigo antes da primeira. (Decreto - art. 14, caput, inciso VIII, alínea “c”)

* QUANDO, na alteração parcial de artigo, houver alteração de unidade inferior dentro de unidade superior, ENTÃO usar linha pontilhada precedida da indicação do dispositivo a que se refere. (Decreto - art. 14, caput, inciso VIII, alínea “d”)

## Cláusula de revogação

* Relacionar expressamente todas as disposições revogadas na cláusula de revogação. (Decreto - art. 15, caput)

  * QUANDO houver revogação a estabelecer no ato, ENTÃO incluir a cláusula correspondente na parte final. (Decreto - art. 4º, caput, inciso III, alínea “a”, item 3)

  * QUANDO for revogado ato alterado por norma posterior, ENTÃO incluir expressamente os dispositivos constantes da norma alteradora. (Decreto - art. 15, § 2º)

  * QUANDO a cláusula abranger mais de um ato ou dispositivos não sucessivos do mesmo ato, ENTÃO subdividi-la em incisos, alíneas, itens e subitens. (Decreto - art. 15, § 3º, incisos I e II)

  * QUANDO, na alteração parcial de artigo, houver parágrafo, inciso, alínea, item ou subitem a revogar, ENTÃO realizar a revogação expressa, sem tratar a ausência de linha pontilhada como substituição dessa revogação. (Decreto - art. 14, caput, inciso VIII, alínea “e”)

  * QUANDO se tratar de atos inferiores a decreto antigos e com dificuldades práticas de identificação, a data de corte não alcançar atos publicados após 5 de outubro de 1988 e o ato revogador prever _vacatio legis_ de, no mínimo, três meses, ENTÃO admitir cláusula que revogue todos os atos anteriores à data determinada. (Decreto - art. 66, parágrafo único, incisos I e II)

  * QUANDO, na consolidação, for utilizada a hipótese de revogação de dispositivos implicitamente revogados por atos posteriores, ENTÃO formular declaração expressa de revogação. (Decreto - art. 63, caput, inciso IX, e § 1º)

  * QUANDO, na consolidação, for utilizada a hipótese de revogação de dispositivos de atos de eficácia temporária ou cujos efeitos tenham se exaurido, ENTÃO formular declaração expressa de revogação, observada a inclusão dos dispositivos temporários ainda aplicáveis nas disposições transitórias. (Decreto - art. 63, caput, inciso X, e §§ 1º e 2º)

* Não usar “revogam-se as disposições em contrário”. (Decreto - art. 15, § 1º)

* QUANDO os atos e dispositivos estiverem implicitamente revogados ou com eficácia ou validade prejudicada, ENTÃO admitir consolidação destinada exclusivamente à declaração de revogação. (Decreto - art. 64)

## Vigência e produção de efeitos

* Indicar expressamente a vigência do ato na proposta e incluir a cláusula de vigência na parte final. (Decreto - art. 16, caput; art. 4º, caput, inciso III, alínea “b”)

  * QUANDO se tratar de proposta de emenda à Constituição, ENTÃO dispensar a previsão de entrada em vigor imediata. (Decreto - art. 16, § 1º)

  * QUANDO se tratar de medida provisória, ENTÃO prever entrada em vigor imediata, admitida a postergação da produção de efeitos. (Decreto - art. 16, § 2º)

  * QUANDO o ato tiver maior repercussão, demandar tempo para esclarecimento aos destinatários, exigir adaptação da população, exigir medidas administrativas prévias ou não convier que produza efeitos antes da edição de ato inferior ainda não publicado, ENTÃO prever _vacatio legis_ ou postergação da produção de efeitos. (Decreto - art. 17, caput, incisos I, II, III, IV e V)

  * QUANDO for estabelecida a _vacatio legis_, ENTÃO considerar o prazo para amplo conhecimento, o tempo de adaptação da administração e dos particulares e o período do mês, do ano ou da semana mais adequado ao início da aplicação. (Decreto - art. 17, parágrafo único, incisos I, II e III)

  * QUANDO a minuta de ato normativo estabelecer datas ou prazos diferentes de entrada em vigor para seus dispositivos, ENTÃO discriminar, na cláusula de vigência, quais dispositivos se submetem a cada data ou prazo. (MRPR, item 19.1.2.3, “Cláusula de vigência”, p. 141)

* Usar na cláusula de vigência (_vacatio legis_) as fórmulas “[número cardinal por extenso] dias após a data de sua publicação”, “no [número ordinal por extenso] dia do [número ordinal por extenso] mês subsequente ao de sua publicação” ou “em [data por extenso]”. SE avaliar minuta de ato normativo, ENTÃO não aponte problemas em ainda na utilização uma das fórmulas indicadas. (Decreto - art. 18, caput, incisos I, II e III)

  * QUANDO não houver previsão de _vacatio legis_, ENTÃO usar “na data de sua publicação”. (Decreto - art. 18, caput, inciso IV)

  * QUANDO for adotada a forma alternativa às fórmulas indicadas acima para cláusula de vigência (_vacatio legis_), ENTÃO estabelecer a cláusula em dias úteis, semanas, meses ou anos, contados da publicação. (Decreto - art. 18, parágrafo único)

## Requisitos textuais de atos específicos

* QUANDO o ato impuser licenças ou autorizações para importação ou exportação em razão das características das mercadorias, e não se tratar das normas tributárias ou aduaneiras de competência da Secretaria Especial da Receita Federal do Brasil do Ministério da Fazenda, ENTÃO identificar as mercadorias por referência à classificação na Nomenclatura Comum do Mercosul. (Decreto - art. 11, §§ 6º e 7º)

* QUANDO se tratar de ato de criação ou alteração de colegiado, ENTÃO indicar suas competências, sua composição e a autoridade responsável pela presidência ou coordenação. (Decreto - art. 38, caput, incisos I e II)

* QUANDO se tratar de ato de criação ou alteração de colegiado, ENTÃO indicar os quóruns de reunião e de aprovação, a periodicidade das reuniões ordinárias e a forma de convocação das extraordinárias. (Decreto - art. 38, caput, incisos III e IV)

* QUANDO se tratar de ato de criação ou alteração de colegiado, ENTÃO indicar a possibilidade de participação dos membros por videoconferência. (Decreto - art. 38, caput, inciso V)

* QUANDO for o caso de prever a criação de subcolegiados por ato do colegiado principal, ENTÃO indicar essa possibilidade e os limites máximos de membros, duração e quantidade de subcolegiados em operação simultânea. (Decreto - art. 38, caput, inciso VI, alíneas “a”, “b” e “c”)

* QUANDO se tratar de ato de criação ou alteração de colegiado, ENTÃO identificar o órgão, entidade ou unidade que exercerá a secretaria-executiva. (Decreto - art. 38, caput, inciso VII)

* QUANDO, no colegiado criado ou alterado, os membros não forem natos, ENTÃO indicar as autoridades responsáveis por indicá-los e designá-los. (Decreto - art. 38, caput, inciso VIII)

* QUANDO se tratar de ato de criação ou alteração de colegiado e for o caso de exigir regimento interno, ENTÃO indicar a obrigatoriedade de sua edição e a autoridade ou unidade responsável por elaborá-lo e aprová-lo. (Decreto - art. 38, caput, inciso IX)

* QUANDO se tratar de ato de criação ou alteração de colegiado e for o caso de exigir relatórios, ENTÃO indicar a necessidade de relatórios periódicos e de relatório final e a autoridade à qual serão encaminhados. (Decreto - art. 38, caput, inciso X)

* QUANDO o colegiado for temporário, ENTÃO indicar a data prevista para encerramento das atividades. (Decreto - art. 38, caput, inciso XI)

* QUANDO um colegiado criado por decreto for alterado por ato inferior a decreto, sem se enquadrar nas ressalvas de assessoramento direto ao Presidente da República ou de criação por lei, ENTÃO fazer constar integralmente no novo ato o conteúdo previsto no decreto de criação, incorporadas as alterações pretendidas. (Decreto - art. 41, caput e parágrafo único, inciso I; art. 33, caput, incisos I e II)

## Consolidação: reunião, limites, fusão e supressão

* QUANDO se tratar de consolidação, ENTÃO reunir atos relativos a matérias conexas ou afins em um único ato, com revogação formal dos atos incorporados, sem modificar o alcance nem interromper a força normativa dos dispositivos consolidados. (Decreto - art. 62, caput e parágrafo único)

* QUANDO se tratar de consolidação, ENTÃO preservar o conteúdo normativo original dos dispositivos e limitar as alterações às modalidades admitidas no art. 63. (Decreto - art. 63, caput)

* QUANDO, na consolidação, houver dispositivos repetitivos ou de valor normativo idêntico, ENTÃO admitir sua fusão. (Decreto - art. 63, caput, inciso III)

* QUANDO, na consolidação, houver dispositivos invalidados por determinação judicial com efeito erga omnes, tidos como ilegítimos por jurisprudência consolidada do Supremo Tribunal Federal ou por jurisprudência de tribunal superior em matéria que não seja da competência do Supremo Tribunal Federal, ou revogados tacitamente por atos posteriores, ENTÃO admitir sua supressão. (Decreto - art. 63, caput, inciso VIII, alíneas “a”, “b” e “c”, e § 1º)

</Regras_de_Redacao_Normativa_Legislativa>