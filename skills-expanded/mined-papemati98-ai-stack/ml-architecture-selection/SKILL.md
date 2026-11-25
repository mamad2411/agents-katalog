---
name: ml-architecture-selection
description: Uzyj przed budowa modelu ML/DL. Dobiera najmniejsza sensowna strategie przez baseline ladder, 2-4 konkurujace hipotezy, eksperymenty falsyfikujace, split OOS, koszt i stop-rule.
---

Pomoz wybrac podejscie ML/DL ZANIM zacznie sie trening. Nie zwracaj jednego modelu z autorytetu: zwroc konkurujace hipotezy i dowod, ktory moze je obalic.

Najpierw zrozum cel, metryke, dane (ilosc, jakosc, etykiety, modalnosc, leakage, split) i ograniczenia sprzetu/budzetu.

Przed wyborem gotowego modelu lub datasetu uruchom `ml-recon`: porownaj lokalny
stack z kandydatami z Hugging Face/web, przypnij rewizje, licencje, format i VRAM.
Sam zwiad pozostaje read-only i nie jest zgoda na pobranie ani trening.

Drabina baseline, zawsze w tej kolejnosci:
1. Regula, matematyka lub optimizer.
2. Klasyczny ML.
3. Gotowy model bez treningu.
4. Fine-tune/LoRA.
5. Nowa siec lub trening od zera.

Dobierz i UZASADNIJ:
- Rodzina modelu: klasyczne ML (drzewa/GBM) vs sieci; jesli sieci: MLP / CNN (obraz) / Transformer-LLM (tekst, sekwencje, multimodal) / RNN (temporal) / GNN (grafy) / diffusion (generacja). Dopasuj do danych, nie do mody.
- Strategia: gotowy model off-the-shelf -> fine-tune (LoRA/QLoRA/full) -> trening od zera. Najtansza opcja, ktora spelni cel.
- Rozmiar/koszt: czy zmiesci sie na dostepnej karcie; czy LoRA/quantization wystarczy.
- Ryzyka: za malo danych, leakage, niereprezentatywny zbior, brak baseline.

Zaproponuj 2-4 falsyfikowalne hipotezy, minimalny eksperyment rozstrzygajacy dla kazdej, OOS/holdout, ablacje gdy uzasadnione, koszt/ryzyko i kryterium przerwania. Rekomendacja ma wskazywac najtanszy wariant spelniajacy kontrakt oraz warunek przejscia wyzej na drabinie.

Przeczytaj [contract.md](references/contract.md) dla formatu i [trigger-cases.json](references/trigger-cases.json) dla granic. Dla jawnie zamowionego porownania CPU pomocniczy `arbor_campaign.py` w skillu `new-training` dostarcza lokalne wyniki numeryczne i warunkowy transfer udokumentowanych lekcji. Lokalny zapis nie jest wynikiem AG ani niezaleznym review. Nie uruchamiaj treningu, pobierania ani promocji w tym skillu.
