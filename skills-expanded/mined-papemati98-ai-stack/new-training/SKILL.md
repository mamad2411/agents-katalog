---
name: new-training
description: Uzyj na poczatku KAZDEGO treningu lub fine-tuningu. Zawiera campaign contract, lokalnie-pierwszy wybor compute, baseline, resume proof, OOS, telemetryke i niezalezna bramke promocji przed kolejnym runem lub wdrozeniem.
---

Zanim ruszy trening lub fine-tuning, wypelnij campaign contract i uzyskaj niezalezny odbior. Skill nie uruchamia automatycznie treningu, pobierania, uploadu, promocji ani deployu.

Wymagaj:

- primary metric, guardrails, minimalny efekt wart kosztu i baseline;
- temporal/group OOS oraz nietkniety final holdout;
- sanity check i overfit-one-batch;
- macierz ablacji oraz HPO/DoE tylko w granicach budzetu;
- commit, environment, data/model hashes, hardware snapshot;
- checkpoint lineage, optimizer/scheduler/RNG state i udowodniony resume;
- telemetryke GPU, loss, grad norm, LR, throughput, walidacje i koszty;
- negative-results ledger, robustness/parity checks i niezaleznego reviewera.
- drabine compute: lokalny sprzet -> Hugging Face Jobs -> RunPod; cloud wolno
  wybrac dopiero po dowodzie, ze lokalny backend nie miesci modelu, terminu albo
  zatwierdzonego eksperymentu;
- rozdzielenie szybkich, prerejestrowanych eksperymentow od checkpointu refleksji:
  po ustalonej liczbie prob zatrzymaj serie, porownaj wszystkie wyniki z baseline,
  odrzuc martwe hipotezy i dopiero wtedy zaplanuj kolejna serie; nie podgladaj
  finalnego holdoutu w checkpointach refleksji.

Campaign contract:

Cel (1 zdanie - co i po co):
Kryterium sukcesu (mierzalne):
Dane (gdzie, ile, format, jakosc):
Podejscie (architektura + strategia): od zera / fine-tune / LoRA-QLoRA / off-the-shelf
Model bazowy:
Karta GPU + budzet VRAM:
Backend compute: local / hf-jobs / runpod
Uzasadnienie cloud (jesli dotyczy):
Maksymalny koszt + waluta (jesli cloud):
Flavor/obraz + timeout + teardown (jesli cloud):
Precision / batch / grad-accum:
Gdzie checkpointy (poza firmowym OneDrive):
Jak monitoruje i jak wznawiam (resume):
Kryterium stop / early stopping:

Resume proof musi pokazac: checkpoint identity, restored states, next-step determinism lub jawna tolerancje, brak duplikacji/utraty danych oraz wynik porownania z runem ciaglym. Samo istnienie pliku checkpoint nie jest dowodem wznowienia.

Checklista przed startem:
- [ ] Commit, environment i hardware snapshot zapisane.
- [ ] GPU i budzet czasu sa zgodne z kontraktem; 5070 Ti nie jest zajmowana bez zgody.
- [ ] Dane i checkpointy sa poza firmowym OneDrive.
- [ ] Baseline, OOS i final holdout sa zablokowane przed treningiem.
- [ ] Dla cloud: rewizje skryptu, modelu, datasetu i obrazu sa przypiete; licencja,
      klasyfikacja danych, limit kosztu, timeout, checkpoint persistence i teardown
      maja jawne `ALLOW`.

Po treningu: niezalezny reviewer odbiera repro package. Promotion gate wymaga primary metric, guardrails, OOS/robustness/parity, kosztu, lineage i braku naruszenia holdout. `GO` oznacza zgode reviewera, `NO-GO` lub `REVISE` zamyka sciezke promocji do czasu usuniecia wskazanych wad.

Przeczytaj [contract.md](references/contract.md) dla artefaktow,
[compute-backends.md](references/compute-backends.md) dla wyboru local/HF Jobs/RunPod,
[arbor-campaign.md](references/arbor-campaign.md) dla zautomatyzowanych kampanii Arbor CPU i transferu doswiadczen
i [trigger-cases.json](references/trigger-cases.json) dla granic.

Arbor jest warunkowym narzedziem dla jawnie zamowionych lokalnych porownan CPU.
Jego wyniki nie zastepuja niezaleznego review ani bramek promocji; staged UAT,
trwale claims i jawny eksport AG opisuje [arbor-campaign.md](references/arbor-campaign.md).
