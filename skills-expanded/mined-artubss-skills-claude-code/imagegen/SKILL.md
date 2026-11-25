---
name: "imagegen"
description: "Use when the user asks to generate or edit images via the OpenAI Image API (for example: generate image, edit/inpaint/mask, background removal or replacement, transparent background, product shots, concept art, covers, or batch variants); run the bundled CLI (`scripts/image_gen.py`) and require `OPENAI_API_KEY` for live calls."
author: openai
---


# Skill de Geração de Imagens

Gera ou edita imagens para o projeto atual (por exemplo, assets de website, assets de game, mockups de UI, mockups de produto, wireframes, design de logo, imagens fotorrealistas, infográficos). Usa como padrão `gpt-image-1.5` e a OpenAI Image API, e prefere o CLI agrupado para execuções determinísticas e reproduzíveis.

## Quando usar
- Gerar uma nova imagem (concept art, product shot, capa, hero de website)
- Editar uma imagem existente (inpainting, edições com máscara, transformações de iluminação ou clima, substituição de fundo, remoção de objetos, composição, fundo transparente)
- Execuções em lote (muitos prompts ou muitas variantes entre prompts)

## Árvore de decisão (gerar vs editar vs lote)
- Se o usuário fornece uma imagem de entrada (ou diz "edit/retouch/inpaint/mask/translate/localize/change only X") → **editar**
- Senão, se o usuário precisa de muitos prompts/assets diferentes → **generate-batch**
- Senão → **gerar**

## Fluxo de trabalho
1. Decida a intenção: gerar vs editar vs lote (veja a árvore de decisão acima).
2. Colete as entradas antecipadamente: prompt(s), texto exato (palavra por palavra), restrições/lista de evitar, e qualquer imagem(ns) de entrada/máscara(s). Para edições de múltiplas imagens, rotule cada entrada por índice e função; para edições, liste invariantes explicitamente.
3. Se lote: escreva um JSONL temporário em tmp/ (um trabalho por linha), execute uma vez e depois delete o JSONL.
4. Aumente o prompt em uma especificação curta rotulada (estrutura + restrições) sem inventar novos requisitos criativos.
5. Execute o CLI agrupado (`scripts/image_gen.py`) com padrões sensatos (veja references/cli.md).
6. Para edições/gerações complexas, inspecione as saídas (abra/visualize imagens) e valide: assunto, estilo, composição, precisão de texto e invariantes/itens a evitar.
7. Itere: faça uma única mudança direcionada (prompt ou máscara), execute novamente, verifique novamente.
8. Salve/retorne as saídas finais e anote o prompt final + flags utilizados.

## Convenções de temp e saída
- Use `tmp/imagegen/` para arquivos intermediários (por exemplo, lotes JSONL); delete quando terminar.
- Escreva artefatos finais em `output/imagegen/` ao trabalhar neste repositório.
- Use `--out` ou `--out-dir` para controlar caminhos de saída; mantenha nomes de arquivo estáveis e descritivos.

## Dependências (instale se ausentes)
Prefira `uv` para gerenciamento de dependências.

Pacotes Python:
```
uv pip install openai pillow
```
Se `uv` não estiver disponível:
```
python3 -m pip install openai pillow
```

## Ambiente
- `OPENAI_API_KEY` deve estar definida para chamadas de API ao vivo.

Se a chave estiver ausente, forneça ao usuário estas etapas:
1. Crie uma chave de API na interface da plataforma OpenAI: https://platform.openai.com/api-keys
2. Defina `OPENAI_API_KEY` como uma variável de ambiente no seu sistema.
3. Ofereça-se para guiá-lo na configuração da variável de ambiente para seu SO/shell, se necessário.
- Nunca peça ao usuário que cole a chave completa no chat. Peça para defini-la localmente e confirme quando estiver pronto.

Se a instalação não for possível neste ambiente, diga ao usuário qual dependência está ausente e como instalá-la localmente.

## Padrões e regras
- Use `gpt-image-1.5` a menos que o usuário explicitamente solicite `gpt-image-1-mini` ou explicitamente prefira um modelo mais barato/rápido.
- Assuma que o usuário quer uma nova imagem a menos que explicitamente solicite uma edição.
- Exija `OPENAI_API_KEY` antes de qualquer chamada de API ao vivo.
- Use o SDK Python da OpenAI (pacote `openai`) para todas as chamadas de API; não use HTTP bruto.
- Se o usuário solicitar edições, use `client.images.edit(...)` e inclua imagens de entrada (e máscara se fornecida).
- Prefira o CLI agrupado (`scripts/image_gen.py`) em vez de escrever novos scripts pontuais.
- Nunca modifique `scripts/image_gen.py`. Se algo estiver faltando, pergunte ao usuário antes de fazer qualquer coisa.
- Se o resultado não for claramente relevante ou não satisfizer as restrições, itere com pequenas mudanças de prompt direcionadas; apenas faça uma pergunta se um detalhe ausente bloquear o sucesso.

## Aumento de prompt
Reformate prompts do usuário em uma especificação estruturada e orientada para produção. Apenas torne explícitos os detalhes implícitos; não invente novos requisitos.

## Taxonomia de casos de uso (slugs exatos)
Classifique cada solicitação em um destes buckets e mantenha o slug consistente entre prompts e referências.

Gerar:
- photorealistic-natural — cenas de estilo de vida candid/editorial com textura real e iluminação natural.
- product-mockup — shots de produto/embalagem, imagens de catálogo, conceitos de merch.
- ui-mockup — mockups de interface de app/web que parecem enviáveis.
- infographic-diagram — diagramas/infográficos com layout estruturado e texto.
- logo-brand — exploração de logo/marca, amigável a vetor.
- illustration-story — quadrinhos, arte de livros infantis, cenas narrativas.
- stylized-concept — concept art orientado ao estilo, renders 3D/estilizados.
- historical-scene — cenas com precisão de período/conhecimento de mundo.

Editar:
- text-localization — traduzir/substituir texto em imagem, preservar layout.
- identity-preserve — prova virtual, pessoa em cena; bloquear rosto/corpo/pose.
- precise-object-edit — remover/substituir um elemento específico (incl. trocas interiores).
- lighting-weather — mudanças apenas de hora do dia/estação/atmosfera.
- background-extraction — fundo transparente / recorte limpo.
- style-transfer — aplicar estilo de referência enquanto muda assunto/cena.
- compositing — inserção/fusão de múltiplas imagens com iluminação/perspectiva combinadas.
- sketch-to-render — desenho/arte linear para render fotorrealista.

Esclarecimento rápido (aumento vs invenção):
- Se o usuário diz "uma imagem hero para uma landing page", você pode adicionar *restrições de layout/composição* que são implícitas nesse uso (por exemplo, "espaço negativo generoso à direita para texto de headline").
- Não introduza novos elementos criativos que o usuário não pediu (por exemplo, adicionar mascote, mudar o assunto, inventar nomes de marca/logos).

Modelo (inclua apenas linhas relevantes):
```
Caso de uso: <slug de taxonomia>
Tipo de asset: <onde o asset será usado>
Solicitação principal: <prompt principal do usuário>
Cena/fundo: <ambiente>
Assunto: <assunto principal>
Estilo/meio: <foto/ilustração/3D/etc>
Composição/enquadramento: <amplo/close/top-down; posicionamento>
Iluminação/mood: <iluminação + mood>
Paleta de cores: <notas da paleta>
Materiais/texturas: <detalhes de superfícies>
Qualidade: <baixa/média/alta/automática>
Fidelidade de entrada (edições): <baixa/alta>
Texto (palavra por palavra): "<texto exato>"
Restrições: <deve manter/deve evitar>
Evitar: <restrições negativas>
```

Regras de aumento:
- Mantenha breve; adicione apenas detalhes que o usuário já implícita ou explicitamente forneceu.
- Sempre classifique a solicitação em um slug de taxonomia acima e adeque restrições/composição/qualidade a esse bucket. Use o slug para encontrar o exemplo correspondente em `references/sample-prompts.md`.
- Se o usuário fizer uma solicitação ampla (por exemplo, "Gere imagens para este website"), use bom senso para propor assets saborosos e apropriados ao contexto e mapeie cada um para um slug de taxonomia.
- Para edições, liste explicitamente invariantes ("mude apenas X; mantenha Y inalterado").
- Se algum detalhe crítico estiver ausente e bloquear o sucesso, faça uma pergunta; senão, prossiga.

## Exemplos

### Exemplo de geração (imagem hero)
```
Caso de uso: stylized-concept
Tipo de asset: hero de landing page
Solicitação principal: uma imagem hero minimalista de uma xícara de café de cerâmica
Estilo/meio: fotografia de produto limpa
Composição/enquadramento: produto centralizado, espaço negativo generoso à direita
Iluminação/mood: iluminação de estúdio suave
Restrições: sem logos, sem texto, sem watermark
```

### Exemplo de edição (invariantes)
```
Caso de uso: precise-object-edit
Tipo de asset: substituição de fundo em foto de produto
Solicitação principal: substituir o fundo por um gradiente de pôr do sol caloroso
Restrições: mude apenas o fundo; mantenha o produto e suas bordas inalterados; sem texto; sem watermark
```

## Melhores práticas de prompting (lista breve)
- Estruture o prompt como cena -> assunto -> detalhes -> restrições.
- Inclua o uso pretendido (anúncio, mock de UI, infográfico) para definir o modo e nível de polimento.
- Use linguagem de câmera/composição para fotorrealismo.
- Cite texto exato e especifique tipografia + posicionamento.
- Para palavras tricky, soletreia letra por letra e exija renderização palavra por palavra.
- Para múltiplas entradas de imagem, referencie imagens por índice e descreva como combiná-las.
- Para edições, repita invariantes em cada iteração para reduzir variação.
- Itere com follow-ups de mudança única.
- Para execuções sensíveis à latência, comece com quality=low; use quality=high para saídas com muito texto ou críticas em detalhes.
- Para edições rigorosas (bloqueio de identidade/layout), considere input_fidelity=high.
- Se os resultados parecerem "tacky", adicione uma breve linha "Evitar:" (vibe de stock photo; cheesy lens flare; neon oversaturado; bloom duro; oversharpening; desordem) e especifique contenção ("editorial", "premium", "subtle").

Mais princípios: `references/prompting.md`. Especificações copy/paste: `references/sample-prompts.md`.

## Orientação por tipo de asset
Modelos de tipo de asset (assets de website, assets de game, wireframes, logo) são consolidados em `references/sample-prompts.md`.

## Notas de CLI + ambiente
- Comandos CLI + exemplos: `references/cli.md`
- Quick reference de parâmetro de API: `references/image-api.md`
- Se as aprovações de rede / configurações de sandbox estão atrapalhando: `references/codex-network.md`

## Mapa de referência
- **`references/cli.md`**: como *executar* geração/edições/lotes de imagens via `scripts/image_gen.py` (comandos, flags, receitas).
- **`references/image-api.md`**: que botões existem no nível de API (parâmetros, tamanhos, qualidade, fundo, campos apenas de edição).
- **`references/prompting.md`**: princípios de prompting (estrutura, restrições/invariantes, padrões de iteração).
- **`references/sample-prompts.md`**: receitas de prompt copy/paste (fluxos de geração + edição; apenas exemplos).
- **`references/codex-network.md`**: ambiente/sandbox/troubleshooting de aprovação de rede.