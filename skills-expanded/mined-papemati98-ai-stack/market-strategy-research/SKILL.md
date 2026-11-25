---
name: market-strategy-research
description: "Prowadzi research-only badania strategii rynkowych i tradingowych: jakość danych, jednoznaczne reguły, koszty wykonania, walk-forward, OOS, final holdout, ogony i reżimy. Użyj przy backtestach, sygnałach, portfelach i modelach rynkowych; nigdy do składania zleceń ani autonomicznego handlu."
---

# Market strategy research

Ten skill daje zgodę wyłącznie na badanie. Wynik backtestu nie jest zgodą na paper trading, promocję ani produkcję.

## Procedura

1. Zdefiniuj hipotezę, instrumenty, horyzont, częstotliwość, sygnał, wykonanie, benchmark i metrykę ekonomiczną przed obejrzeniem finalnego holdoutu.
2. Przypnij źródło danych oraz datę `as-of`. Sprawdź timestampy, strefy czasowe, corporate actions, survivorship, look-ahead, braki i duplikaty.
3. Zapisz jednoznaczne reguły wejścia, wyjścia, pozycji, limitów, konfliktów sygnałów i postępowania z brakującymi danymi.
4. Policz koszty wykonania: spread, prowizje, slippage, funding/borrow, impact i opóźnienie. Pokaż wynik brutto i netto.
5. Rozdziel IS, validation, walk-forward/OOS i nietknięty final holdout. Każda zmiana po obejrzeniu wyniku wraca do etapu hipotezy.
6. Oceń stabilność po reżimach, instrumentach, okresach, perturbacji parametrów oraz w ogonach rozkładu.
7. Porównaj z prostym baseline'em i uwzględnij wielokrotne próby. Raportuj pełną ścieżkę eksperymentów, także porażki.
8. Zakończ werdyktem badawczym `PROMISING`, `INCONCLUSIVE` albo `REJECTED`, nigdy automatycznym `DEPLOY`.

## Granice

- Zakaz połączenia z brokerem, składania zleceń, zmiany konfiguracji handlowej i aktywacji produkcji.
- Nie uzupełniaj brakujących kosztów, kursów ani semantyki danych założeniami bez jawnego oznaczenia.
- Dla modelu ML użyj też `new-training`; dla symulacji `simulation-and-optimization`.
- Promocja wymaga osobnego kontraktu właściciela, czystego OOS i niezależnej bramki.

Kontrakt badania znajduje się w `references/research-contract.md`, a granice
aktywacji w `references/trigger-cases.json`.
