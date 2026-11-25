---
name: doc-governance
description: Classifica todo documento novo (épico, GAP, insight, ADR) na pasta certa, mantém os links Epic↔ADR nos dois sentidos e roda o verificador de refs como gate — ler ao criar, mover ou linkar qualquer .md de docs/.
---

# Governança documental — a convenção só vive se alguém a impõe

Caso de origem: pastas `epics/`, `gaps/` e `completed/` criadas sem skill que as mantivesse ficaram **vazias por 2 meses**, enquanto 15 épicos se acumulavam na raiz. Convenção sem dono morre; esta skill é o dono.

## Classificar na criação (não depois)

| É | Vai para | Registro |
|---|---|---|
| Épico (decisão de produto com fases) | `docs/epics/` (ou o `<docs>/epics/` do projeto) | linha no PENDING enquanto aberto |
| GAP Estrutural/Contratual | `docs/gaps/` + PENDING **no ato** (skill `governanca-de-decisao`) | ADR antes de executar |
| GAP de Código | **só** PENDING, nunca arquivo | morre no CHANGELOG ao corrigir |
| Pesquisa, benchmark, dump de medição | `docs/insights/` — dado bruto em subpasta datada, síntese em `.md` com data | linkado de quem o usou |
| Decisão estrutural prestes a ser executada | ADR Proposta + índice (comando `/adr`) | Epic↔ADR linkados (abaixo) |

## Links Epic↔ADR nos dois sentidos

Todo épico lista suas ADRs; toda ADR lista seu épico. Link num sentido só é link quebrado futuro — o verificador abaixo acusa.

## O gate: `verificar_refs.py` sobre a árvore de docs

```bash
python3 .harness/verificar_refs.py --docs <docs-do-projeto> --raiz .
```

- **Renomear sem rodar é quebrar sem saber.** Rode antes do commit que move, renomeia ou adiciona link.
- Path antigo vira stub de 3 linhas ("moveu para `...` em <data>"), nunca sumiço silencioso.
- Placeholder `<...>` é ignorado pelo verificador de propósito: template com campo por preencher não é ref quebrada.

## Guarda dos índices

- `ADR-INDEX.md`: próximo número livre conferido antes de criar (reservas em branches abertas contam).
- `python3 .harness/verificar_adr.py --adr-dir <docs>/adr`: ID duplicado reprova (GAP-20261015-035 do projeto de origem: duas ADR-001). Rode junto do `verificar_refs.py` antes do commit.
- Concluído sai do PENDING e entra no CONCLUSION **no mesmo commit** — um sem o outro é registro pela metade.

## Quarentena, nunca apagão

Arquivo sem link ativo há 90 dias é candidato a `_legacy/` (leitura histórica), nunca a `rm`. História apagada vira retrabalho: a próxima sessão redescobre o que já foi decidido.
