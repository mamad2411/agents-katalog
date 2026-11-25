---
name: test-first-engineering
description: Zdefiniuj kontrakt, napisz czerwony test potwierdzajacy problem, wykonaj minimalna zmiane i odbierz ja przez testy regresji oraz przeplyw uzytkownika.
---

# Test First Engineering

Uzyj przy zmianie zachowania kodu, naprawie regresji, zmianie kontraktu API/danych lub ryzyku szerokiego blast radius.

1. Zapisz kontrakt uzytkownika, API lub danych oraz kryterium akceptacji.
2. Dodaj najmniejszy czerwony test, ktory failuje z powodu realnego problemu, i upewnij sie, ze fail jest diagnostyczny.
3. Wprowadz minimalna implementacje, uruchom test zielony, nastepnie testy sasiednie wedlug blast radius.
4. Sprawdz sciezke uzytkownika oraz backend/API, gdy zmiana dotyka obu warstw. Nie rozszerzaj poprawki poza kontrakt.
5. Raportuj testy pominiete, flaky, srodowiskowe i niezamkniete ryzyka; `PASS` oznacza dowod, nie sam status procesu.

Przeczytaj [contract.md](references/contract.md) dla formatu i [trigger-cases.json](references/trigger-cases.json) dla anti-triggerow. Dla eksperymentu jednorazowego uzyj proporcjonalnego sanity check zamiast sztucznego testu produkcyjnego.
