# Cursor Project Rules — UGC 3D (TS/WebGPU)

## Priorytety
1) Zielone `pnpm ci` (typecheck, lint, test, bench). 2) Bez regresji perf > 5%. 3) Zero side-effectów w top-level modułów.

## Styl
- TS strict, funkcjonalne moduły, brak singletons dla stanu globalnego.
- Commity: Conventional Commits (feat:, fix:, refactor:, perf:, test:).
- PR-y atomowe: jeden temat = jeden PR.

## Testy i perf
- Zanim zmienisz architekturę → najpierw dodaj test ujawniający problem.
- Każdy PR: min. 1 test jednostkowy + 1 integracyjny (jeśli dotyka runtime/editor).
- Odpal `pnpm bench` i dołącz różnice (JSON + .md).

## Render/ECS
- ECS: deterministyczny tick order; systemy nie czytają się nawzajem, tylko dane.
- Render: preferuj batching/instancing; kolejkuj draw calls wg. materiału/stanu.

## Edytor
- Inspector generowany z metadanych komponentów.
- Undo/redo przez command-stack. Każda edycja w UI = command.

## Jak odpowiadasz w PR
- Krótkie „Design notes” + ryzyka + plan rollbacku.
- Jeśli zadanie jest większe → podziel na „waves” i otwórz serię PR-ów.
