---
name: ciclo-de-pesquisa
description: Conduz pesquisa com embasamento verificável, do levantamento de fonte primária até o relatório auditável em markdown. Use quando o usuário pedir para pesquisar um tema, levantar evidência, checar um dado, comparar fontes, escrever relatório com citação, ou disser variações como "pesquisa isso pra mim", "de onde vem esse número", "isso é verdade", "monta um relatório sobre", "levanta os papers de". Também use antes de publicar qualquer número, afirmação quantitativa ou superlativo.
---

# Ciclo de pesquisa

Conduza a pesquisa em estações, na ordem. Não pule a ingestão nem a memória.

## As quatro regras inegociáveis

Aplique em toda pesquisa, sem exceção e sem esperar o usuário pedir.

1. **Fonte primária na frente.** Ordem de confiança: documentação oficial e repositório do projeto, depois publicação primária ou paper, depois análise de terceiro, e por último blog agregador, que serve apenas como pista para confirmar em outro lugar. Nunca encerre em blog agregador.
2. **Divergência é reportada, nunca resolvida em silêncio.** Quando duas fontes discordam, apresente as duas com a data de cada uma e diga qual é a primária. Escolher a mais conveniente sem avisar é falha grave.
3. **Amostra fraca é marcada.** Padrão observado em menos de cinco casos entra como "amostra fraca", jamais como conclusão.
4. **Saída auditável.** Todo número, valor monetário ou superlativo carrega a URL e a data de acesso ao lado. Sem isso, o dado não sai do rascunho.

## Estação 1: fonte primária

Use o MCP `paper-search` para localizar literatura em arXiv, PubMed, bioRxiv, Semantic Scholar, Crossref, OpenAlex e Unpaywall.

Peça sempre o DOI junto do título, porque o DOI sobrevive a link quebrado. Baixe os PDFs numa pasta `./fontes` do projeto.

Quando o tema for tecnologia ou produto em vez de ciência, a fonte primária é o repositório, a documentação oficial e o changelog. Contagem de stars, versão e data de release devem ser lidas na página do projeto, nunca em artigo que cita o projeto.

## Estação 2: ingestão legível

Antes de ler qualquer documento, converta. Delegue para a skill `ingestao`, que roteia cada tipo de arquivo para o conversor certo.

Nunca analise um PDF de duas colunas sem converter antes. Ordem de leitura embaralhada gera conclusão embaralhada.

## Estação 3: protocolo

Antes de investigar, escreva no arquivo de saída:

- a pergunta exata, em uma frase
- o critério que decide a resposta, fixado agora e não depois
- o que falsificaria a hipótese

Se o usuário instalou o RigorPilot, delegue a execução para ele quando o trabalho for reprodução de experimento.

## Estação 4: investigação

Cruze as fontes convertidas. Ao usar as skills de terceiros instaladas pelo bootstrap, mantenha as quatro regras acima delas: elas definem o método, as regras definem o padrão de prova.

Registre no arquivo cada afirmação com a fonte correspondente enquanto pesquisa, não no final. Reconstruir a origem depois é onde o rastro se perde.

## Estação 5: memória

Salve o resultado em markdown. Estrutura padrão:

- pergunta e critério
- achados, cada um com fonte e data
- divergências encontradas, com as duas versões
- o que ficou em aberto
- fontes consultadas, com URL e data de acesso

Se o usuário mantém um vault de Obsidian, salve lá, respeitando a estrutura de pastas que já existe. Vault de Obsidian é uma pasta de markdown comum, então escreva direto no sistema de arquivos, sem MCP.

Se o MCP `zotero` estiver disponível, registre as referências formais lá com `zotero_add_by_doi`.

## Estação 6: prova de fogo

Ao terminar, liste explicitamente para o usuário:

- quais afirmações vieram de fonte primária
- quais ficaram apoiadas apenas em fonte secundária
- quais números merecem reconfirmação por serem voláteis, como contagem de stars, preço e cargo

Sugira subir o mesmo conjunto de fontes no Gemini Notebook como segunda leitura quando a decisão for de alto risco.

## Anti-padrões

- responder de memória sem abrir fonte, mesmo quando a resposta parece óbvia
- citar número redondo sem data
- apresentar consenso quando as fontes divergem
- deixar o achado morrer no chat sem virar arquivo
