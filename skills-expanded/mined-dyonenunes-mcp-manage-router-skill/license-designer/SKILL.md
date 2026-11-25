---
name: license-designer
description: >-
  Escolhe, redige e aplica a licença de um repositório: entrevista o dono sobre o que quer
  permitir e proibir, detecta contradições (ex.: "MIT mas proibido vender"), gera o arquivo
  LICENSE com o texto oficial, escreve um resumo em linguagem simples e sincroniza
  pyproject/package.json/README. Use sempre que o usuário pedir para criar, trocar, revisar
  ou explicar uma licença, adicionar LICENSE a um projeto, proibir venda ou uso comercial,
  tornar um projeto open source ou source-available, ou perguntar "qual licença eu uso?".
tags: [license, licensing, open-source, legal, repository, spdx]
---

# License Designer (`license-designer`)

Licença errada é pior que licença nenhuma: um rótulo "MIT" sobre um texto que proíbe venda
confunde quem usa e não protege quem publica. Esta skill trata a licença como uma decisão
do dono do projeto, traduzida para um texto oficial e mantida coerente em todo o repositório.

> Você não é advogado e a skill não substitui um. Diga isso uma vez, no relatório final,
> sempre que a licença sair do padrão ou o projeto tiver peso comercial.

## Fase 1 — Diagnóstico (nunca pule)

Antes de perguntar qualquer coisa, olhe o que já existe:

1. **Licença atual:** `LICENSE*`, `COPYING*`, `NOTICE*`, campo de licença nos manifestos
   (`pyproject.toml`, `package.json`, `Cargo.toml`, `composer.json`) e seção no README.
2. **Já foi publicado?** `git log --oneline -- LICENSE` e o remoto. Versões já publicadas
   continuam valendo sob a licença antiga para quem as recebeu; trocar só vale daqui em
   diante. Avise isso.
3. **Quem escreveu o código:** `git shortlog -sn`. Com mais de um autor, relicenciar exige
   o consentimento de todos (ou um CLA). Pare e avise.
4. **Dependências:** uma dependência GPL/AGPL embutida obriga o projeto a ser compatível.
   Liste as licenças das dependências diretas quando o gerenciador permitir
   (`uv pip list` + metadados, `npm ls`, `cargo license`).

## Fase 2 — Entrevista e escolha

Pergunte só o que não deu para descobrir. São dados do dono; **nunca invente**:

- **Titular do copyright** (pessoa ou empresa) e **ano**. E-mail de contato é opcional.
- **O que quer permitir e proibir.** Deixe a pessoa falar em linguagem comum ("não quero
  que vendam", "quero que melhorias voltem para mim").
- **Idioma** do resumo em linguagem simples.

Traduza a intenção para uma licença com esta tabela:

| Intenção do dono | Licença | SPDX | Observação |
|---|---|---|---|
| Liberar tudo, inclusive vender; máximo de adoção | MIT | `MIT` | Curta e conhecida |
| Idem, com proteção explícita de patentes | Apache 2.0 | `Apache-2.0` | Pede arquivo `NOTICE` se houver avisos |
| Derivados devem continuar abertos | GPL v3 | `GPL-3.0-or-later` | Copyleft forte |
| Idem, mas é biblioteca usada por software fechado | LGPL v3 | `LGPL-3.0-or-later` | Copyleft só na biblioteca |
| Idem, inclusive quando oferecido como serviço em rede | AGPL v3 | `AGPL-3.0-or-later` | Fecha a brecha do SaaS |
| Copyleft por arquivo, meio-termo | MPL 2.0 | `MPL-2.0` | Convive com código fechado |
| **Proibir a venda**, permitindo uso (até em empresa) | base permissiva + Commons Clause | `LicenseRef-<base>-Commons-Clause` | Source-available |
| **Proibir qualquer uso comercial** | PolyForm Noncommercial | `PolyForm-Noncommercial-1.0.0` | Source-available |
| Proibir oferta como serviço concorrente | Elastic 2.0 / BUSL 1.1 | `Elastic-2.0` / `BUSL-1.1` | BUSL exige data de conversão |
| Abrir mão de tudo | Unlicense / CC0 | `Unlicense` / `CC0-1.0` | Domínio público |
| Texto, documentação, arte (não é código) | Creative Commons | `CC-BY-4.0`, `CC-BY-SA-4.0`, `CC-BY-NC-4.0` | Não use CC para software |
| Código fechado | Aviso proprietário | `LicenseRef-Proprietary` | "Todos os direitos reservados" |

### Portão de contradições

Pare e explique antes de escrever qualquer arquivo quando a intenção e o rótulo brigarem:

- **Restrição + licença aberta.** Proibir venda, uso comercial ou um ramo de atividade é
  incompatível com MIT, Apache, BSD e GPL: todas autorizam vender. A saída é uma licença
  source-available, e o projeto deixa de ser "open source" na definição da OSI. Nunca
  mantenha o nome "MIT" num texto alterado.
- **"Proibido vender" x "proibido uso comercial".** São coisas diferentes: Commons Clause
  barra a revenda mas deixa uma empresa usar internamente; PolyForm Noncommercial barra os
  dois. Confirme qual das duas a pessoa quer.
- **Dependência copyleft + licença permissiva ou fechada.** Avise a incompatibilidade.

Apresente a recomendação em uma frase, com a consequência principal, e só siga depois de
o dono confirmar a escolha.

## Fase 3 — Geração do LICENSE

**Texto oficial, sem reescrever de memória.** Busque a fonte canônica:

```bash
gh api licenses/mit --jq .body                      # licenças que o GitHub conhece
curl -fsSL https://raw.githubusercontent.com/spdx/license-list-data/main/text/<SPDX>.txt
```

A Commons Clause não está na lista SPDX; use `references/commons-clause-v1.0.txt` e
preencha os três campos finais.

Regras de montagem:

- Preencha ano e titular nos marcadores do texto oficial. Não altere mais nada.
- **Licença padrão:** o arquivo contém só o texto oficial. Qualquer cabeçalho ou resumo
  dentro dele quebra a detecção automática do GitHub; o resumo vai para o README.
- **Licença composta ou source-available:** a detecção já não funciona, então o arquivo
  pode abrir com um bloco "RESUMO EM LINGUAGEM SIMPLES", marcado como informativo, seguido
  dos textos legais separados por réguas, com a condição restritiva antes da licença base.
- O resumo usa duas listas, "Você PODE" e "Você NÃO PODE", em frases curtas, no idioma
  pedido. Ele descreve o texto legal; não cria regra nova.

## Fase 4 — Sincronização do repositório

Uma licença que só existe no arquivo `LICENSE` está pela metade. Alinhe:

| Onde | O que ajustar |
|---|---|
| `pyproject.toml` | `license = "<SPDX>"` e `license-files = ["LICENSE"]` (PEP 639) |
| `package.json` | `"license": "<SPDX>"`, ou `"SEE LICENSE IN LICENSE"` se não houver SPDX |
| `Cargo.toml` | `license = "<SPDX>"` ou `license-file = "LICENSE"` |
| `README.md` | Seção "Licença" com link, titular e a tabela Pode / Não pode; selo coerente |
| `NOTICE` | Só para Apache-2.0, quando houver avisos de atribuição |

Se o projeto se descreve como "open source" e a licença escolhida é source-available,
corrija o termo no README e na descrição do repositório.

## Fase 5 — Verificação

Antes de anunciar que terminou:

1. **Coerência:** o mesmo identificador aparece no `LICENSE`, nos manifestos e no README.
   Procure sobras do nome antigo (`grep -rn "MIT" --include=*.toml --include=*.json --include=*.md`).
2. **Build:** o pacote ainda constrói (`uv build`, `npm pack --dry-run`, `cargo package --list`)
   e o `LICENSE` vai dentro do artefato.
3. **Detecção:** para licença padrão, depois do push,
   `gh repo view --json licenseInfo -q .licenseInfo.key` deve devolver o SPDX (pode levar
   alguns minutos). Para composta, diga que o GitHub não mostrará selo.
4. **Privacidade:** nada além do titular (e do e-mail, se autorizado) entrou nos arquivos.

## Relatório final

Entregue em poucas linhas: licença escolhida e por quê, o que ela permite e proíbe, os
arquivos alterados, o que muda para versões já publicadas, e o aviso de que não é
aconselhamento jurídico. Não faça commit nem push sem o dono pedir.
