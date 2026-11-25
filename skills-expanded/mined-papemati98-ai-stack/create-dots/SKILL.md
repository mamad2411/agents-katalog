---
name: create-dots
description: "Tworzy lub konfiguruje DOTS tylko na wyrazne polecenie stworzenia DOTS albo $create-dots. Nie uruchamia sie podczas zwyklych sesji ani statusow."
---

# Create DOTS

Uzyj tylko po jawnym zamowieniu DOTS. Pilot ma syntetyczne adaptery i nie
kwalifikuje prawdziwej poczty, modelu, kluczy ani wdrozenia.

Ustal org, project, identyfikator, observer/collector, kadencje UTC i budzet z
polecenia oraz istniejacej konfiguracji. Pytaj tylko o brak wymaganej decyzji.
Nie dodawaj nowego rejestru, rady, grafu ani krokow do zwyklych sesji.

Runtime pochodzi z checkoutu projektu agent-stack:
`shared/dots-farm/dots.py`. W originie pomocnik znajduje go wzgledem siebie;
w zainstalowanej kopii podaj `--runtime <ABSOLUTE_AGENT_STACK>/shared/dots-farm/dots.py`.
Nie zgaduj sciezki z katalogu agenta. Odczytaj README tego runtime tylko dla
zamowionego tworzenia/konfiguracji. Stan musi miec osobny absolutny katalog.

Przyklad wykonania (argumenty pochodza z zamowienia). `$skillDirectory` jest
absolutnym katalogiem aktualnie odczytanego SKILL.md, takze w zainstalowanym
scan-root; `$agentStackCheckout` jest absolutnym checkoutem wybranego runtime.
Obie sciezki ustal z rzeczywistych plikow, niezaleznie od biezacego CWD:

```powershell
$creator = (Resolve-Path -LiteralPath (Join-Path $skillDirectory 'scripts/create.py')).Path
$runtime = (Resolve-Path -LiteralPath (Join-Path $agentStackCheckout 'shared/dots-farm/dots.py')).Path
python -B "$creator" --runtime "$runtime" --state "$state" observer --kind observer --org pilot-org --project pilot --budget 2000000 --interval 900
python -B "$runtime" --state "$state" status --dot observer
```

Pomocnik wywoluje prawdziwe syntetyczne CLI, bez powloki, instalacji i modeli.
Nie zastapi istniejacego DOTS. Inicjalizacja globalnego budzetu jest osobna jawna
komenda `init`; domyslny globalny limit to zero, a edycja zachowuje wydatki i holds.
Zweryfikuj nowy DOTS syntetycznym zrodlem `--source` i komenda `tick` z README;
nie oznaczaj fixture jako dowodu jakosci rzeczywistego LLM.

Live wymaga osobnego konkretnego odbioru model/provider, referencji klucza,
budzetu i granic VM/uslugi. Ten skill nie aktywuje live. Cofniecie: `pause`,
zachowanie stanu i poprzedniej wersji; bez kasowania profili, kluczy lub danych.
Zmiany wspolnego skilla stosuja istniejacy autoryzowany proces: origin ->
`bootstrap.ps1 -ValidateSkills` -> overlay/sync z wymaganym prywatnym backupem
PUSHED/CURRENT. Nie dodawaj osobnej zgody ani kroku do zwyklej sesji;
zachowaj globalne granice zapisu i kasowania. Samo tworzenie DOTS nie edytuje
wspolnego skilla.
