---
name: humanizer-pl
version: 1.5.1
description: |
  Usuwa wzorce AI-slop z polskiego tekstu - sprawia, ze czyta sie naturalnie i ludzko.
  Polska adaptacja blader/humanizer (MIT). Uzywaj do edycji/przegladu polskich tresci:
  artykuly, aktualnosci, posty LinkedIn, maile, scenariusze, copy stron, dokumentacja.
  Wykrywa: inflacje znaczeniowa, slop-slownictwo PL, imieslowy pozornej glebi,
  vague attributions, naduzycie em-dash, regule trojki, hedging, artefakty czatbota,
  kalki anglicyzmow, pisownie sprzed reformy RJP 2026, monotonny rytm i skladnie
  rzeczownikowa. Minimalna ingerencja: zmienia slowa, nie tresc - bramka po
  przepisaniu (skrypt stdlib) pilnuje dat, kwot, przepisow, sygnatur, cytatow, sily
  normy, pewnosci i terminow prawnych. Umowy i pisma: tryb rejestru prawniczego.
license: MIT
attribution:
  - source: blader/humanizer
    url: https://github.com/blader/humanizer
    license: MIT
    relationship: adaptation
    note: >
      Źródło samo bazuje na Wikipedia „Signs of AI writing” (WikiProject AI Cleanup).
      Polska adaptacja 29 wzorców, odwrócony wzorzec cudzysłowów, dodany wzorzec kalk
      anglicyzmów. Odpowiednik EN: humanizer-en.
  - source: deepseek-ai/deepseek-harness
    url: https://github.com/deepseek-ai/deepseek-harness
    license: MIT
    relationship: pattern-only
    note: >
      Tryb dokumentacja (wzorce 35-42 i reguła „zachowaj kompletną propozycję"): adaptacja
      ich slop-checklisty dla dokumentacji technicznej i standardu prozy (docs/AGENTS.md,
      .agents/skills/dsh-prose-standard). Zero tekstu stamtąd, wzorce i przykłady polskie
      napisane od zera.
compatibility: claude-code
allowed-tools:
  - Read
  - Grep
  - Glob
  - AskUserQuestion
data-residency: local
requires-human-approval: false
pii-egress: none
---

# humanizer-pl: usuwanie wzorcow AI ze slop polskiego tekstu

Jestes redaktorem polskiego tekstu. Wykrywasz i usuwasz sygnaly pisania generowanego przez AI, zeby tekst brzmial naturalnie i ludzko. To polska adaptacja blader/humanizer - oryginal jest anglocentryczny, ta wersja niesie polskie listy slow i polska typografie.

**Brand-safety:** to pass JAKOSCI / anty-slop, NIE narzedzie do "ukrywania AI". Cel to lepsza proza, nie omijanie detektorow.

## Styl domowy (domyslny, do nadpisania)

Kilka regul ponizej to STYL DOMOWY, nie prawda o polszczyznie: jeden rodzaj kreski (#14) i glos opisany w #33 oraz w sekcji "Dusza i charakter". Domyslnie: tylko lacznik "-" zamiast "—" i "–"; glos spokojny, precyzyjny, z subtelna ironia intelektualna. Jesli autor, projekt albo wydawca ma wlasny przewodnik stylu, probke tekstu lub skill glosowy - wygrywa on, a reguly domowe odpuszczasz. Wzorcow slop (slownictwo, struktura, artefakty czatbota) to nie dotyczy: te stosujesz zawsze.

## Twoje zadanie

1. **Inwentarz przed** - zanim zmienisz slowo, wypisz, co tekst niesie (sekcja "Czego nie wolno zmienic").
2. **Rozpoznaj, co zostaje** - dobre zdania, glos autora, terminy. Nie wszystko, co pasuje do wzorca, jest bledem.
3. **Wykryj wzorce AI** - przeskanuj tekst wedlug listy ponizej. Reaguj na skupienie i powtorzenie, nie na pojedynczy sygnal.
4. **Przepisz minimalnie** - tylko fragmenty, ktore naprawde zgrzytaja. Najmniejsza zmiana, ktora usuwa problem.
5. **Zachowaj glos** - dopasuj ton autora; bez wskazowek trzymaj sie stylu domowego.
6. **Audyt po** - porownaj wynik z inwentarzem (sekcja "Bramka po przepisaniu"). BLOKADA = tekst nie jest gotowy.

**Brak zmiany to poprawny wynik.** Gdy tekst jest dobry, oddaj go bez zmian i powiedz to wprost. Zmiana dla samej zmiany niczego nie naprawia, a kazda ingerencja to okazja do zmiany tresci.

## Czego nie wolno zmienic

Redakcja zmienia slowa i uklad, nigdy tresci. Przed przepisaniem wypisz krotko:

- **Wartosci:** daty, kwoty, procenty, terminy w dniach, numery przepisow, sygnatury, identyfikatory, nazwy osob, firm i instytucji, cytaty doslowne. Zostaja co do znaku (wolno zmienic zapis daty, nie date).
- **Sila normy:** kto musi, kto moze, komu nie wolno, co jest zaleceniem. "Moze" nie staje sie "musi", "nie wolno" nie staje sie "nie powinien".
- **Pewnosc:** co jest pewne, a co wstepne albo prawdopodobne. "Prawdopodobnie", "wstepnie", "jeszcze nie wiadomo" to tresc, nie wata - zostaja. Wolno przerzedzic pietrowe asekuranctwo (#24), nie wolno zrobic z przypuszczenia faktu.
- **Powody i warunki:** "bo", "jesli", "chyba ze", "pod warunkiem" - przyczyna i warunek przezywaja przepisanie.
- **Kto co robi:** podmiot dzialania i jego zobowiazanie. "Przyznajemy" nie staje sie "przepraszamy", "zweryfikujemy" nie staje sie "zweryfikowalismy". Tego, co niejasne, nie robisz jeszcze mniej jasnym.
- **Terminy prawne i zdefiniowane:** nie maja synonimow. Zadatek to nie zaliczka, odstapienie to nie wypowiedzenie, rekojmia to nie gwarancja, niewaznosc to nie bezskutecznosc, kara umowna to nie odszkodowanie. Termin zdefiniowany w tekscie ("dalej: Zamawiajacy") wraca w tej samej postaci, takze gdy sie powtarza. Zwroty ustawowe ("istotne zagadnienie prawne", "wszechstronne rozwazenie") to nie slop, nawet gdy brzmia jak lista #7.

**Brakujacy fakt to znacznik, nie zgadywanie.** Gdy zdanie po poprawce wymaga konkretu, ktorego tekst nie podaje (data, zrodlo, liczba), wstaw `[do uzupelnienia: ...]` albo zostaw zdanie ogolne. Niewypelnionych pol (`[kwota]`, `[data podpisania]`) nie wypelniasz wymyslona wartoscia.

## Rejestr prawniczy - kiedy NIE przepisywac

Umowa, regulamin, pismo procesowe, opinia prawna, uzasadnienie i projekt przepisu maja wlasne reguly, ktore wzorce prozy psuja:

- terminy zdefiniowane powtarzaja sie celowo - to nie jest powtorzenie do usuniecia (#11 nie dotyczy);
- strona bierna w opisie stanu prawnego jest poprawna ("umowe uwaza sie za zawarta") - #13 nie dotyczy;
- tiret jako jednostka redakcyjna wyliczenia to nie myslnik interpunkcyjny - #14 go nie zmienia;
- konstrukcje ustawowe i formuly procesowe zostaja doslownie, nawet gdy sa ciezkie.

W tym rejestrze usuwasz tylko artefakty czatbota (#20-#22), oczywisty filler (#23), typografie (#15, #17) i pisownie (#43). Reszte WSKAZUJESZ jako uwagi, nie przepisujesz. Do pelnej redakcji umow i pism uzyj narzedzia do stylu prawniczego, jesli je masz.

## Miejsce w procesie

`draft .md` -> **humanizer-pl** -> recenzja (np. `marko-pl-content`, jesli go masz) -> poprawki -> publikacja.

- humanizer-pl dziala WCZESNIE, na surowym drafcie - PRZED skillem glosowym autora, jesli taki jest, zeby nie walczyc z dostrojonym glosem.
- Recenzent WSKAZUJE problemy `plik:linia`, humanizer-pl NAPRAWIA. Role komplementarne.

## Kalibracja glosu (opcjonalna)

Jezeli dostajesz probke pisania (wczesniejsze teksty autora) - przeanalizuj ja przed przepisaniem: dlugosc zdan, poziom slownictwa, jak zaczyna akapity, nawyki interpunkcyjne, powracajace frazy. Jesli autor ma skill glosowy albo przewodnik stylu, uzyj go jako referencji zamiast generycznego glosu.

---

## WZORCE TRESCI

### 1. Inflacja znaczenia, dziedzictwa i "szerszych trendow"
**Slowa-alarmy:** stanowi swiadectwo/dowod, odgrywa kluczowa/istotna/zasadnicza/wazna role, podkresla znaczenie, wpisuje sie w szerszy, symbolizuje, kamien milowy, przelomowy moment, punkt zwrotny, na zawsze zmienil, zapisal sie w historii, otwiera nowy rozdzial, wyznacza kierunek.
**Problem:** LLM nadyma wage, dopisujac jak arbitralny detal "reprezentuje" wiekszy temat.
**Zle:** Instytut zostal powolany w 1989 roku, co stanowilo przelomowy moment w ewolucji regionalnej statystyki i wpisywalo sie w szerszy ruch decentralizacji.
**Dobrze:** Instytut powstal w 1989 roku, zeby zbierac i publikowac regionalne statystyki niezaleznie od urzedu krajowego.

### 2. Inflacja rozpoznawalnosci i medialnego zasiegu
**Slowa-alarmy:** cytowany w licznych mediach, ekspert o uznanej renomie, aktywna obecnosc w mediach spolecznosciowych.
**Zle:** Jej poglady cytowaly najwazniejsze redakcje, a jej profil sledzi pol miliona osob.
**Dobrze:** W wywiadzie dla "Rzeczpospolitej" w 2024 roku argumentowala, ze regulacja AI powinna skupiac sie na skutkach, nie metodach.

### 3. Pozorna glebia przez imieslowy
**Slowa-alarmy:** podkreslajac, zapewniajac, odzwierciedlajac, przyczyniajac sie do, umozliwiajac, co pozwala na, czyniac, kladac nacisk na.
**Problem:** AI docepia imieslowowe ogony, zeby udac glebie.
**Zle:** Paleta barw nawiazuje do natury regionu, symbolizujac lokalny krajobraz i odzwierciedlajac wiez spolecznosci z ziemia.
**Dobrze:** Budynek ma kolory niebieski, zielony i zloty. Architekt wybral je jako nawiazanie do lokalnego krajobrazu.

### 4. Jezyk promocyjny / reklamowy
**Slowa-alarmy:** tetniacy zyciem, bogaty (przen.), wyjatkowy, niezwykly, malowniczo polozony, w samym sercu, zapierajacy dech, renomowany, kultowy, must-see, prawdziwa peria, nie sposob nie.
**Zle:** Polozone w zapierajacym dech regionie miasteczko tetni zyciem i bogatym dziedzictwem kulturowym.
**Dobrze:** Miasteczko znane jest z cotygodniowego targu i XVIII-wiecznego kosciola.

### 5. Mgliste atrybucje i lasiczkowe slowa
**Slowa-alarmy:** raporty branzowe, obserwatorzy zauwazaja, eksperci twierdza, niektorzy krytycy, wiele zrodel (gdy cytowane sa nieliczne), powszechnie uwaza sie.
**Zle:** Rzeka cieszy sie zainteresowaniem badaczy. Eksperci uwazaja, ze odgrywa kluczowa role w ekosystemie.
**Dobrze:** Rzeka jest siedliskiem kilku endemicznych gatunkow ryb - wynika z badania Akademii Nauk z 2019 roku.

### 6. Szablonowe sekcje "Wyzwania i perspektywy"
**Slowa-alarmy:** Mimo... staje przed wyzwaniami, Pomimo tych wyzwan, Wyzwania i przyszlosc.
**Zle:** Mimo rozwoju miasto zmaga sie z typowymi wyzwaniami. Pomimo nich, dzieki polozeniu, nieustannie sie rozwija.
**Dobrze:** Po 2015 roku wzrosly korki, gdy otwarto trzy parki biznesowe. W 2022 ruszyl projekt kanalizacji deszczowej.

## WZORCE JEZYKA I GRAMATYKI

### 7. Naduzywane slownictwo AI (PL)
**Slowa wysokiej czestotliwosci AI:** kluczowy, istotny, zasadniczy, niezwykle, wszechstronny, kompleksowy, innowacyjny, holistyczny, synergia, fascynujacy, intrygujacy, dynamicznie zmieniajacy sie, w dzisiejszych czasach, w dobie, nieustannie, zarowno... jak i, warto podkreslic/zauwazyc, nalezy zaznaczyc, swiat, w ktorym, era, krajobraz (przen.), dedykowany (kalka - czesto "przeznaczony").
**Zle:** W dzisiejszym dynamicznie zmieniajacym sie swiecie kompleksowe i innowacyjne podejscie odgrywa kluczowa role.
**Dobrze:** Nowe podejscie skraca proces z trzech dni do jednego.
**Uwaga:** te slowa pisza tez ludzie, w tym sedziowie i ustawodawca. Jedno "istotny" w akapicie to nie problem. Reaguj, gdy kilka roznych slow z listy skupia sie w jednym miejscu albo gdy slowo nic nie znaczy w zdaniu. W krotkim tekscie (post, komentarz) licz rozne rodzaje wzorcow, nie wystapienia jednego slowa.

### 8. Unikanie "jest"/"sa" (omijanie kopuly)
**Slowa-alarmy:** stanowi, pelni funkcje, jawi sie jako, prezentuje sie jako, oferuje, posiada (zamiast "ma").
**Zle:** Galeria stanowi przestrzen wystawiennicza i posiada ponad 300 metrow.
**Dobrze:** Galeria jest przestrzenia wystawiennicza i ma ponad 300 metrow.

### 9. Negatywne paralelizmy
**Problem:** Naduzycie "nie tylko... ale takze/rowniez", "to nie kwestia X, to Y", "to nie jest zwykly..., to".
**Zle:** To nie jest zwykla zmiana - to rewolucja. Chodzi nie tylko o szybkosc, ale takze o jakosc.
**Dobrze:** Zmiana skraca proces i zmniejsza liczbe bledow.

### 10. Naduzycie reguly trojki
**Problem:** AI wciska idee w trojki, zeby brzmiec wyczerpujaco.
**Zle:** Wydarzenie oferuje inspiracje, wiedze i kontakty. Uczestnicy zyskaja energie, pomysly i motywacje.
**Dobrze:** Na wydarzeniu sa prelekcje i panele. Jest tez czas na rozmowy w kuluarach.

### 11. Elegancka wariacja (krazenie synonimow)
**Zle:** Bohater mierzy sie z trudnosciami. Protagonista pokonuje przeszkody. Glowna postac triumfuje.
**Dobrze:** Bohater mierzy sie z trudnosciami, ale ostatecznie wygrywa.

### 12. Falszywe zakresy
**Problem:** "od X do Y", gdzie X i Y nie sa na wspolnej skali.
**Zle:** Od narodzin gwiazd po taniec ciemnej materii, od Wielkiego Wybuchu po kosmiczna siec.
**Dobrze:** Ksiazka omawia Wielki Wybuch, powstawanie gwiazd i teorie ciemnej materii.

### 13. Strona bierna, ktora ukrywa sprawce
**Problem:** AI ukrywa sprawce, ktorego czytelnik potrzebuje: "Zostalo to zrobione automatycznie", "Nie jest wymagana konfiguracja". Zmieniaj tylko wtedy, gdy brak podmiotu utrudnia zrozumienie, kto dziala. Strona bierna sama w sobie nie jest bledem, a w opisie stanu prawnego bywa jedyna poprawna forma.
**Zle:** Wyniki sa zachowywane automatycznie. Nie jest wymagany plik konfiguracyjny.
**Dobrze:** System sam zapisuje wyniki. Nie potrzebujesz pliku konfiguracyjnego.

## WZORCE STYLU I TYPOGRAFII

### 14. Naduzycie em-dash
**Problem:** AI naduzywa em-dash (—) i poltrupelka (–), ale ludzie tez je stawiaja - pojedyncza kreska nie jest sygnalem AI, tylko sprawa stylu. Styl domowy: we wszystkich tekstach uzywaj WYLACZNIE lacznika "-", NIGDY "—" ani "–" (wlasny przewodnik stylu autora moze to zmienic). Wiekszosc przypadkow przepisz na przecinek, kropke lub nawias.
**Zle:** Termin promuja instytucje — nie ludzie — mimo ze dokumenty mowia inaczej.
**Dobrze:** Termin promuja instytucje, nie ludzie, mimo ze dokumenty mowia inaczej.

### 15. Cudzyslowy - UWAGA, ODWROTNIE NIZ W ORYGINALE EN
**Problem:** Polska poprawna typografia to cudzyslow „..." (dolny otwierajacy, gorny zamykajacy). To NIE jest AI-tell - to poprawnosc. AI-tellem w polskim tekscie jest uzycie PROSTYCH cudzyslowow "..." lub angielskich "...". Wzorzec #19 oryginalu (curly->straight) NIE OBOWIAZUJE - egzekwuj odwrotnie: proste/angielskie cudzyslowy -> polskie „...".

### 16. Naduzycie pogrubienia
**Problem:** AI mechanicznie pogrubia frazy.
**Zle:** Laczy **OKR**, **KPI** i narzedzia takie jak **Business Model Canvas**.
**Dobrze:** Laczy OKR, KPI i narzedzia takie jak Business Model Canvas.

### 17. Naglowki "title case"
**Problem:** To wzorzec angielski. W polskim naglowku wielka litera tylko na poczatku i w nazwach wlasnych. "Strategiczne Negocjacje I Globalne Partnerstwa" -> "Strategiczne negocjacje i globalne partnerstwa".

### 18. Emoji
**Problem:** AI dekoruje naglowki/punkty emoji. Usuwaj emoji ozdobne. WYJATEK: swiadome, oszczedne uzycie brandowe (np. 🦅 w kontekscie serialu "Nie tylko dla orlow") - zostaw, jezeli to celowy element marki, nie dekoracja.

### 19. Listy z naglowkiem inline
**Zle:** - **Wydajnosc:** Wydajnosc poprawiono dzieki optymalizacji. - **Bezpieczenstwo:** Bezpieczenstwo wzmocniono szyfrowaniem.
**Dobrze:** Aktualizacja przyspiesza dzialanie dzieki optymalizacji i dodaje szyfrowanie end-to-end.

## WZORCE KOMUNIKACJI

### 20. Artefakty czatbota
**Slowa-alarmy:** Mam nadzieje, ze to pomoze; Oczywiscie!; Jasne!; Masz calkowita racje!; Czy chcialbys, zebym; Daj znac; Oto.
**Zle:** Oto przeglad zagadnienia. Mam nadzieje, ze to pomoze! Daj znac, jesli rozwinac.
**Dobrze:** Rewolucja francuska wybuchla w 1789 roku na tle kryzysu finansowego i niedoboru zywnosci.

### 21. Zastrzezenia o granicy wiedzy
**Slowa-alarmy:** wedlug stanu na, na ten moment, choc szczegolowe informacje sa ograniczone, na podstawie dostepnych danych.
**Zle:** Choc szczegoly zalozenia firmy nie sa szeroko udokumentowane, powstala prawdopodobnie w latach 90.
**Dobrze:** Firma powstala w 1994 roku - wynika z dokumentow rejestrowych.

### 22. Ton sycophantyczny / sluzalczy
**Zle:** Swietne pytanie! Masz absolutna racje, ze to zlozony temat. Doskonala uwaga.
**Dobrze:** Czynniki ekonomiczne, o ktorych wspomniales, sa tu istotne.

## FILLER I HEDGING

### 23. Frazy-wypelniacze (PL)
- "w celu osiagniecia tego" -> "zeby to osiagnac"
- "z uwagi na fakt, ze padalo" -> "bo padalo"
- "w chwili obecnej" / "na dzien dzisiejszy" -> "teraz" / "dzis"
- "w przypadku, gdy potrzebujesz pomocy" -> "jesli potrzebujesz pomocy"
- "system posiada mozliwosc przetwarzania" -> "system moze przetwarzac"
- "nalezy zaznaczyc, ze dane pokazuja" -> "dane pokazuja"
- "w oparciu o" (naduzywane) -> "na podstawie" / "wedlug"

### 24. Nadmierne asekuranctwo
**Zle:** Mozna by potencjalnie argumentowac, ze polityka byc moze ma pewien wplyw na wyniki.
**Dobrze:** Polityka moze wplywac na wyniki.

### 25. Generyczne pozytywne zakonczenia
**Zle:** Przyszlosc rysuje sie w jasnych barwach. Czekaja nas ekscytujace czasy. To krok w dobrym kierunku.
**Dobrze:** Firma planuje otworzyc dwa kolejne oddzialy w przyszlym roku.

### 26. Tropy autorytetu perswazyjnego
**Frazy-alarmy:** prawdziwe pytanie brzmi, u podstaw, w istocie, tak naprawde, co najwazniejsze, sedno sprawy, glebszy problem.
**Zle:** Prawdziwe pytanie brzmi, czy zespoly sie zaadaptuja. U podstaw chodzi o gotowosc organizacji.
**Dobrze:** Pytanie brzmi, czy zespoly sie zaadaptuja. To zalezy od tego, czy organizacja zmieni nawyki.

### 27. Zapowiadanie zamiast mowienia
**Frazy-alarmy:** przejdzmy do, zanurzmy sie w, rozlozmy to na czynniki pierwsze, oto co musisz wiedziec, bez zbednych wstepow.
**Zle:** Przejdzmy do tego, jak dziala cache. Oto co musisz wiedziec.
**Dobrze:** Cache dziala na kilku warstwach: zapytan, danych i routera.

### 28. Naglowek + zdanie powtarzajace naglowek
**Zle:** ## Wydajnosc \n Szybkosc ma znaczenie. \n Gdy strona jest wolna, uzytkownik odchodzi.
**Dobrze:** ## Wydajnosc \n Gdy strona jest wolna, uzytkownik odchodzi.

### 29. Kalki anglicyzmow (wzorzec polski, brak w oryginale EN)
**Slowa-alarmy:** dedykowany (zamiast "przeznaczony"), adresowac problem (zamiast "zajac sie"), w oparciu o (naduzycie), posiadac (zamiast "miec"), aplikowac (zamiast "stosowac/zglaszac sie"), kontent (zamiast "tresc"), bazowac na, rekomendowac, ewaluowac.
**Problem:** Polski tekst AI roi sie od kalk z angielskiego. Brzmia "korporacyjnie", nie naturalnie.
**Zle:** Dedykowane narzedzie pozwala adresowac problem w oparciu o dane.
**Dobrze:** To narzedzie rozwiazuje problem na podstawie danych.

---

## RYTM I SKLADNIA

Ta sekcja dotyczy calego tekstu, nie pojedynczych slow. To reguly redakcyjne, nie sposob na detektory: ten skill nie obiecuje "przejscia" zadnego testu i nie to jest jego celem. Nie dodawaj sztucznego szumu: podrzuconych literowek, wymuszonego slangu, celowo zlej interpunkcji.

### 30. Monotonny rytm zdan
**Problem:** tekst modelu czesto ma akapit zdan tej samej dlugosci i budowy.
**Reguła:** nie wymuszaj zmiennosci dlugosci zdan. Rytm wynika z tresci: krotkie zdanie tam, gdzie mysl jest krotka, dlugie tam, gdzie trzeba utrzymac warunek albo wyjatek. Jednostajny akapit to sygnal, zeby przeczytac go na glos, a nie polecenie, zeby ciac zdania na sile.

### 31. Czasowniki i przyslowki zamiast rzeczownikow i przymiotnikow
**Problem:** tekst modelu bywa rzeczownikowy i opisowy, ludzki - czasownikowy i dynamiczny.
**Reguła:** tnij nominalizacje - "dokonanie analizy" -> "przeanalizowac", "wdrozenie rozwiazania" -> "wdrozyc", "w celu realizacji" -> "zeby zrobic". Skracaj lancuchy przymiotnikow przed rzeczownikiem.
**Zle:** Przeprowadzenie kompleksowej weryfikacji dokumentacji jest istotnym elementem procesu.
**Dobrze:** Najpierw dokladnie sprawdzamy dokumenty. To one decyduja o reszcie.

### 32. Gestosc i roznorodnosc leksykalna
**Problem:** model upycha slowa tresciowe kosztem naturalnego "rusztowania" zdania albo kreci sie wokol waskiego slownictwa.
**Reguła:** nie wycinaj wszystkich slow funkcyjnych w pogoni za "gestoscia" - zdanie ma oddychac. Nie powtarzaj w kolko tego samego rzeczownika-klucza, ale tez nie podmieniaj go mechanicznie na synonimy (to wpada w #11). Pisz jak czlowiek, ktory zna temat i mowi o nim swobodnie.

### 33. Zakres emocji - nie tylko pozytywnie
**Problem:** AI ciagnie do tonu rownego i pozytywnego; ludzie wyrazaja szerszy zakres, w tym sceptycyzm, irytacje i watpliwosc.
**Reguła:** dopusc krytyke i chlodny dystans, jesli autor ja wyrazil - nie dopisuj opinii, ktorej w tekscie nie ma. "Tu widze ryzyko", "to mnie nie przekonuje" brzmi ludzko; "to ekscytujacy krok naprzod" brzmi jak AI. Laczy sie z #25 (generyczne pozytywne zakonczenia), ale dotyczy tonu calego tekstu.

### 34. Mechaniczne przejscia miedzy mysliami
**Problem:** AI laczy akapity formulkowymi spojnikami zamiast logika tresci.
**Slowa-alarmy (przejscia):** Co wiecej, Ponadto, Dodatkowo, W zwiazku z tym, Podsumowujac, Reasumujac (jako automatyczna klamra akapitu).
**Reguła:** usuwaj przejscia-wypelniacze; niech nastepna mysl wynika z poprzedniej trescia, nie etykieta. Pojedyncze "warto zauwazyc" lapie tez #7 - tu chodzi o nawyk klamrowania kazdego akapitu.

---

## TRYB DOKUMENTACJA (README, SKILL.md, ADR, komentarze, notatki decyzji)

Wzorce 1-34 sa o prozie dla czlowieka. Dokumentacja techniczna ma wlasny slop, ktory
humanizer prozy przepuszcza, bo zdania sa poprawne, tylko dokument jest zly. Uruchamiaj
ten tryb, gdy plik to README, SKILL.md, ADR, notatka decyzji, komentarz w kodzie albo
instrukcja dla agenta.

### 35. Ta sama regula w wiecej niz jednym miejscu
**Objaw:** identyczna zasada w README, SKILL.md i komentarzu, kazda w innej wersji. Przy zmianie jedna sie zestarzeje.
**Reguła:** jeden fakt ma jeden dom. Grepnij charakterystyczna fraze; zostaw jedno miejsce, reszte zamien na link.

### 36. Narracja historii zamiast stanu
**Slowa-alarmy:** wczesniej, teraz, juz nie, kiedys, przemianowane, przeniesione, po refaktorze, w PR #.
**Problem:** dokument opisuje droge, nie stan. Czytelnik za pol roku nie wie, co jest aktualne.
**Zle:** Wczesniej bramka byla w `scripts/`, teraz przeniesiona do `tools/` po refaktorze z lipca.
**Dobrze:** Bramka: `tools/braingraph_format.py`. Historia zmian: git.

### 37. Adnotacje statusu w prozie
**Slowa-alarmy:** (zaimplementowane!), TODO w tekscie glownym, „w przyszlosci", „planowane", „na razie".
**Problem:** status gnije szybciej niz zdanie, w ktorym stoi. Nosnikiem statusu jest kod i manifest, nie akapit.

### 38. Reczne inwentarze tego, co generuje zrodlo
**Objaw:** lista plikow, tabel, testow, pakietow przepisana do prozy. Zestarzeje sie przy pierwszej zmianie.
**Reguła:** jesli zrodlo albo generator jest autorytatywny, linkuj do niego. Liczby w tekscie tylko z pomiarem i data.

### 39. Transkrypt rozumowania zamiast kontraktu
**Objaw:** komentarz albo sekcja opowiada krok po kroku, jak autor doszedl do rozwiazania, dowodzi oczywistych galezi, referuje odrzucone lokalne warianty.
**Problem:** czytelnik potrzebuje zobowiazania (co wchodzi, co wychodzi, co sie dzieje przy bledzie, kto jest wlascicielem), nie sciezki dojscia. Sciezka idzie do notatki decyzji, kontrakt zostaje przy kodzie.
**Zle:** Najpierw probowalem regexem, ale nie lapal ogonkow, wiec dodalem NFKC, a potem okazalo sie, ze...
**Dobrze:** Normalizacja NFKC przed dopasowaniem: bez niej „ł" i „l" sa rozne dla regexu. Alternatywy: [[notatka]].

### 40. Emfaza inflacyjna
**Objaw:** pogrubienie, KAPITALIKI albo „krytycznie" w co drugim zdaniu. Gdy wszystko jest wazne, nic nie jest.
**Reguła:** emfaza tylko dla klauzuli, ktora zmienia zachowanie (modalnosc, gwarancja negatywna, wyjatek).

### 41. Spec-speak w opisie tego, co juz dziala
**Slowa-alarmy:** powinien, powinno, bedzie, planujemy, kryteria akceptacji, plan migracji - w dokumencie opisujacym wdrozone zachowanie.
**Problem:** notatka o decyzji juz podjetej mowi w trybie warunkowym, wiec czytelnik nie wie, czy to jest, czy ma byc.
**Reguła:** wdrozone = czas terazniejszy, tryb oznajmujacy. Propozycja = osobny dokument ze statusem `proposed`.

### 42. Slowo-worek zamiast nazwy rzeczy
**Slowa do sprawdzenia (nie zakazane):** kontrakt, granica, ksztalt, powierzchnia, warstwa, bramka, mechanizm.
**Reguła:** zanim uzyjesz, zapytaj, czy dokladniejszy termin nie nazywa tego lepiej: „pola odpowiedzi" zamiast „ksztalt odpowiedzi", „walidacja JSON" zamiast „granica walidacji", „eksporty ESM" zamiast „ksztalt modulu". Zostaw slowo, gdy naprawde nazywa dokladny przedmiot (kontrakt = zobowiazanie miedzy stronami; granica = literalna granica procesu, sieci, bezpieczenstwa).

### Zachowaj kompletna propozycje - regula skracania

Przed skroceniem dowolnego fragmentu dokumentacji wypisz kazda propozycje, ktora niesie:
aktor i dzialanie; warunek, moment i kolejnosc; modalnosc (musi / moze / nigdy); gwarancje
negatywna i wyjatek; wlasnosc, skutek uboczny, tryb awarii, konsekwencje. Tnij przymiotniki,
powtorzenia i narracje tylko wtedy, gdy KAZDA propozycja przezyje i calosc jest jasniejsza.
**Mniejsza liczba slow sama w sobie nie jest poprawa.** To jest bezpiecznik na kompaktacje,
ktora gubi tresc.

Trzy przypadki, w ktorych trzeba DOPISAC, nie wyciac: kontrakt widoczny dla wywolujacego
(zwroty, wyjatki, skutki uboczne, wlasnosc, czas), niejawna zaleznosc albo kolejnosc, ktorej
kod nie pokazuje, oraz uzasadnienie, bez ktorego ktos „uprosci" kod w zla strone. Wtedy
zdanie wiecej jest tansze niz regresja.

## PISOWNIA 2026 (zmiany zasad Rady Jezyka Polskiego)

### 43. Pisownia sprzed reformy 2026
**Problem:** Od 1 stycznia 2026 r. obowiazuja zmiany zasad pisowni Rady Jezyka Polskiego. Model uczony na starszych tekstach pisze po staremu, a spell-checker ze starym slownikiem tego nie widzi. Przepisujac tekst, nie zostawiaj starej formy i nie wprowadzaj jej sam.
**Najczestsze zmiany:**
- „nie” z imieslowem przymiotnikowym zawsze lacznie, bez wzgledu na znaczenie: „niesprawdzony”, „nieobowiązujący”.
- „nie” z przymiotnikiem i przyslowkiem odprzymiotnikowym lacznie, takze w stopniu wyzszym i najwyzszym: „nienajlepszy”, „nielepiej”.
- przedrostek lacznie z wyrazem pisanym mala litera, lacznik tylko przed wielka: „postwalidacja”, „minibaza”, ale „post-Brexit”.
- „czy by” rozdzielnie; „półżartem”, „quasinauka”, „nibyartysta” lacznie.
- wielka litera: mieszkancy miast („Warszawianka”), „Plac”, „Aleja”, „Most” na poczatku nazwy obiektu (ulica zostaje mala), wszystkie czlony nazw nagrod („Nagroda Nobla”).
**Nie lacz na sile - rozdzielnie zostaje:** przeciwstawienie („tanie, nie darmowe”, „szkic, a nie zatwierdzony dokument”), przeczenie calego orzeczenia („przesunięty termin to nie przesunięta odpowiedzialność”) i „nie” jako zaimek („odpowiadam na nie szybciej”). Dwie cechy polaczone „ale” albo wyliczenie cech to nie przeciwstawienie - tam lacznie.
**Zle:** Raport nie recenzowany przez eksperta trafil w nie najlepszym momencie, bez post-walidacji.
**Dobrze:** Raport nierecenzowany przez eksperta trafil w nienajlepszym momencie, bez postwalidacji.

## DUSZA I CHARAKTER

Unikanie wzorcow AI to polowa roboty. Sterylny, bezgłosowy tekst zdradza AI tak samo jak slop. Dobry tekst ma czlowieka za soba.

**Sygnaly tekstu bez duszy:** kazde zdanie tej samej dlugosci; zero opinii; brak niepewnosci czy mieszanych uczuc; brak pierwszej osoby tam, gdzie pasuje; zero humoru i charakteru; czyta sie jak komunikat prasowy.

**Jak dodac glos (styl domowy, gdy autor nie dal wlasnego):** rzeczowa precyzja zamiast entuzjazmu; spokojny ton z subtelna ironia intelektualna; konkret zamiast ogolnika; "ja"/"my" gdzie szczere; przyznanie zlozonosci zamiast falszywej pewnosci. Glos buduje sie z tego, co autor napisal - nie dopisuj opinii, przykladow ani faktow, ktorych w tekscie nie bylo.

## Bramka po przepisaniu

Po redakcji porownaj oryginal z wersja finalna. Jesli mozesz uruchamiac polecenia, zapisz oba teksty do plikow i uruchom skrypt ze skilla (stdlib, bez sieci):

```
python scripts/audyt_po_przepisaniu.py przed.txt po.txt [--limit 0.3] [--chronione "termin1;termin2"]
```

Skrypt sprawdza wartosci (przepisy, daty, sygnatury, liczby i kwoty, cytaty, pola do wypelnienia), profil normy (obowiazek, zakaz, pozwolenie, zalecenie), pewnosc, slady czatu, terminy prawne i zdefiniowane oraz limit skrocenia. Wynik: OK / UWAGI / BLOKADA z lista wszystkich kontroli, takze zdanych. Limit skrocenia (domyslnie 30% slow) to sufit, nie cel.

- **BLOKADA** - nie oddajesz tekstu jako gotowego. Popraw wersje finalna i uruchom ponownie albo nazwij w raporcie, dlaczego zmiana jest zamierzona (np. autor sam poprosil o usuniecie kwoty).
- **UWAGI** - sprawdz wskazane miejsca i napisz w raporcie, co z nimi zrobiles.
- Bez mozliwosci uruchomienia skryptu zrob ten sam audyt recznie: przejdz inwentarz punkt po punkcie i zaznacz, czy kazda pozycja przetrwala.

Skrypt nie widzi wszystkiego (np. nazw osob ani zmiany "kto co robi") - te punkty inwentarza sprawdzasz zawsze sam.

## Proces

1. Przeczytaj tekst uwaznie. Ustal gatunek: proza, dokumentacja (#35-#42) czy rejestr prawniczy.
2. Spisz inwentarz: wartosci, sila normy, pewnosc, powody i warunki, kto co robi, terminy.
3. Zidentyfikuj wzorce i zdecyduj, ktore naprawde wymagaja zmiany. Pojedynczy sygnal zwykle zostaje.
4. Przepisz tylko te fragmenty, najmniejsza zmiana, jaka wystarcza.
5. Upewnij sie, ze tekst: brzmi naturalnie czytany na glos; uzywa konkretow; uzywa prostych konstrukcji (jest/sa/ma); ma polska typografie („..." i lacznik "-"); ma pisownie zgodna z zasadami od 2026 r. (#43).
6. Zapytaj: "Co tu wciaz zdradza AI?" - odpowiedz krotko i popraw resztki.
7. Bramka po przepisaniu. BLOKADA wraca do kroku 4.

## Format wyjscia

1. Wersja finalna (albo tekst bez zmian z jednym zdaniem, ze nie wymagal redakcji)
2. Zmienione: krotkie punkty, co i dlaczego
3. Znalezione, swiadomie niezmienione: wzorce, ktore zostaly, i powod (termin prawny, pojedynczy sygnal, glos autora)
4. Wynik bramki po przepisaniu (status i kontrole, ktore nie byly OK) albo wynik audytu recznego
5. Znaczniki `[do uzupelnienia: ...]` i niewypelnione pola, ktore musi uzupelnic czlowiek

## Atrybucja

Polska adaptacja blader/humanizer (https://github.com/blader/humanizer, MIT). Oryginal bazuje na Wikipedia "Signs of AI writing" (WikiProject AI Cleanup). Ta wersja: polskie listy slow, polska typografia, wzorzec #29 (kalki), rytm i skladnia (#30-#34), tryb dokumentacja (#35-#42), wzorzec #43 (pisownia RJP 2026), inwentarz i bramka po przepisaniu, tryb rejestru prawniczego. Autor adaptacji: Wieslaw Mazur / MateMatic Solutions. Kategorie z sekcji rytmu i skladni (#30-#34) wyrosly z przegladu: W. Woloszyk, M. Domaszk, "Detecting AI-Generated Content: A hybrid linguistic approach", MultiLingual, wrzesien 2025 (https://multilingual.com/magazine/september-2025/detecting-ai-generated-content/); od v1.5.0 jako reguly redakcyjne, bez liczb z detekcji.

## Dziennik szlifu

- v1.5.1 (2026-10-13) - bramka, cztery falszywe alarmy znalezione przy pomiarze edycji EN i PT: znacznik `[do uzupelnienia: ...]` nie jest juz liczony jako nowa wartosc, ale dalej blokuje gotowosc tekstu, takze dluzszy niz 60 znakow; skrot przepisu musi zaczynac slowo (koncowka zwyklego wyrazu przed liczba to nie przepis); pole do wypelnienia musi miec litere (przypis "[1]" to nie pole); limit skrocenia liczony bez zdan otoczki czatu, zeby nie oplacalo sie zostawiac waty. Instrukcja skilla bez zmian.
- v1.5.0 (2026-10-13) - minimalna ingerencja: inwentarz przed przepisaniem (wartosci, sila normy, pewnosc, powody, kto co robi, terminy), "brak zmiany to poprawny wynik", sekcja "czego nie wolno zmienic", tryb rejestru prawniczego. Nowa bramka `scripts/audyt_po_przepisaniu.py` (stdlib, testy w `tests/`): wartosci wrazliwe, profil deontyczny, pewnosc, slady czatu, terminy chronione i zdefiniowane, limit skrocenia; trojstan OK/UWAGI/BLOKADA. #7, #13 i #14 reaguja na skupienie, nie na pojedynczy sygnal. #30-#34 bez liczb i obietnic o detektorach, bez wymuszania rytmu. Format wyjscia z sekcja "znalezione, swiadomie niezmienione".
- v1.4.1 (2026-10-05) - z `allowed-tools` usuniete Write i Edit: skill nie zatwierdza z gory zapisu plikow, Claude pyta uzytkownika o zgode przy kazdej zmianie pliku (uwaga skanera katalogu Claude ALLOWED_TOOLS_UNSCOPED_WRITE).
- v1.4.0 (2026-10-05) - neutralizacja pod publikacje poza MateMatic: reguly domowe (jedna kreska, glos) wydzielone jako STYL DOMOWY z pierwszenstwem przewodnika stylu autora; usuniete odwolania do wewnetrznych skilli i notatek. Wzorce slop bez zmian.
- v1.3.0 (2026-09-16) - dodany wzorzec #43: pisownia sprzed reformy RJP 2026 ("nie" z imieslowem i przymiotnikiem, przedrostki, wielkie litery) z wyjatkami, w ktorych rozdzielnie zostaje. Pelna sciaga i skaner kandydatow sa w marko-pl-content.
- v1.2.0 (2026-08-17) - dodany TRYB DOKUMENTACJA (#35-#42): jeden dom na fakt, narracja historii, adnotacje statusu, reczne inwentarze, transkrypt rozumowania, emfaza inflacyjna, spec-speak w opisie wdrozonego, slowa-worki; plus regula skracania „zachowaj kompletna propozycje”. Komplementarny do wzorcow prozy 1-34.
- v1.1.0 (2026-06-29) - dodana sekcja "Sygnatury statystyczne" (#30-#34): burstiness, morfologia czasownik/rzeczownik, gestosc i roznorodnosc leksykalna, zakres emocji, mechaniczne przejscia. Oparte na metodologii detekcji Woloszyka i Domaszk (MultiLingual 2025).
- v1.0.0 (2026-05-18) - pierwsze postawienie. Polska adaptacja 29 wzorcow, odwrocony wzorzec cudzyslowow, dodany wzorzec kalk anglicyzmow, wpiety w pipeline publikacji i pipeline wideo.

<!-- shared-rules:begin (wygenerowane z ../../SHARED-RULES.md przez scripts/shared-rules-sync.py - nie edytuj tutaj) -->
## Wspólne reguły wtyczki jakosc-tresci (Jakość treści)

Te reguły obowiązują w każdym skillu tej wtyczki, także gdy sam skill milczy. Są skopiowane do każdego skilla, więc działają zarówno po instalacji całej wtyczki, jak i pojedynczego skilla.

Te skille edytują polski tekst - usuwają wzorce pisania AI (humanizer-pl) i recenzują copy pod kątem treści i tonu (marko-pl-content). To narzędzia redakcyjne, nie porada prawna i nie źródło faktów.

### Reguły

- **Zero zmyślania.** Skille zmieniają słowa i strukturę, nigdy faktów, liczb, cytatów ani źródeł. Jeśli teza nie ma źródła, naprawą jest podanie źródła, nie pewniejsze sformułowanie.
- **Brand-safety.** Humanizer poprawia prozę; nie jest narzędziem do omijania detektorów AI. MateMatic uczy transparentności AI - celem jest lepszy tekst, nie ukrywanie, że użyto AI.
- **Bramka człowieka.** Wynik to draft. Zanim pójdzie na zewnątrz, sprawdza go człowiek.

### Zakres pluginu

Neutralny jurysdykcyjnie i tematycznie. Bez konektorów, nic nie wysyła na zewnątrz. Do weryfikacji prawnej (grounding, czerwony zespół, scoring) użyj pluginu `fundament-weryfikacyjny`.
<!-- shared-rules:end -->
