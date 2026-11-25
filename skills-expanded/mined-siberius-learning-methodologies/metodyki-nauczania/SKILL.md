---
name: metodyki-nauczania
description: Projektuj lub oceniaj aplikacje edukacyjne, łącząc cele nauczania, potrzeby uczniów, aktywności, informację zwrotną i dowody uczenia się. Stosuj przy tworzeniu nowych narzędzi edukacyjnych lub istotnych zmianach w ich strukturze dydaktycznej.
metadata:
  version: "1.6.0"
  language: "pl"
  based_on: "learning-methodologies@1.6.0"
  license: "MIT"
  repo: "https://github.com/siberius/learning-methodologies"
  author: "Luděk Sušický"
  format: "pakiet natywny z wygenerowanym autonomicznym Markdownem"
---

# Metodyki nauczania

Pomagaj w projektowaniu, wdrażaniu i ewaluacji aplikacji edukacyjnych, których aktywności edukacyjne, wsparcie i ocenianie służą docelowym uczniom. Dostosuj głębokość pracy do zadania, jego konsekwencji i stopnia niepewności. Krótka aktywność lekcyjna nie wymaga pełnego badania ewaluacyjnego ani obszernego dokumentu planistycznego.

## Metody dydaktyczne dla aplikacji tworzonych z udziałem AI

Stosuj metody dydaktyczne, aby przekładać cele edukacyjne na działania uczniów, reguły informacji zwrotnej i dowody uczenia się w generowanej aplikacji. Na przykład praktyka przypominania wymaga podjęcia próby przed odsłonięciem odpowiedzi, a rusztowanie poznawcze (scaffolding) wymaga kontrolowanej pomocy i odróżnienia wykonania ze wsparciem od samodzielnego. AI może pomóc we wdrażaniu tych decyzji; jej wyniki wciąż wymagają weryfikacji merytorycznej i dydaktycznej. Dotyczy to zarówno aplikacji działających w trybie offline, jak i wykorzystania AI w fazie wykonawczej (runtime), gdy wymaga tego cel dydaktyczny.

Przeczytaj [uzasadnienie dydaktyczne](references/didactic-rationale.md), wyjaśniając, dlaczego dana metoda jest odpowiednia lub przekładając ją na implementację. Łączy ono metody dydaktyczne z decyzjami produktowymi i dowodami niezbędnymi do ich oceny.

## Prowadzenie twórcy przez decyzje projektowe

Przy każdej istotnej decyzji dotyczącej projektowania dydaktycznego powracaj do celu, działań ucznia, dowodów, wsparcia i ograniczeń. Bazuj na wcześniej podjętych ustaleniach. W przypadku nierozstrzygniętego, brzemiennego w skutki wyboru przedstaw niewielki, adekwatny zestaw opcji — zazwyczaj dwie lub trzy — wraz z prostym opisem i konkretnym przykładem w tym projekcie. Zarekomenduj jedno rozwiązanie, wyjaśnij główny kompromis (trade-off) i zapytaj, które podejście preferuje twórca. Przeczytaj [dialog projektowy](references/design-dialogue.md), rozpoczynając lub wznawiając taki wybór. Reguły te porządkują rozmowę z twórcą aplikacji, niezależnie od interakcji tutora z uczniem.

Nie otwieraj ponownie rozstrzygniętych lub odrzuconych wyborów bez istotnej zmiany kontekstu. Uszanuj wyraźne przekazanie rutynowych decyzji agentowi i kontynuuj pracę z krótkim uzasadnieniem. Cisza nie oznacza zgody na rozszerzenie zakresu. W oczekiwaniu na odpowiedź pracuj nad niezależnymi elementami. Zmiana czysto kosmetyczna nie uruchamia tego procesu.

Wczytuj szczegóły według potrzeb: [metody](references/methods.md) dla aktywności edukacyjnych i wsparcia; [gry](references/learning-games.md) dla motywacji i mechanik; [ocenianie](references/assessment.md) dla dowodów i punktacji; [interfejs poznawczy](references/cognitive-ux.md) dla reprezentacji, multimediów i uwagi; [praktyka adaptacyjna](references/adaptive-practice.md) dla powtórek w czasie lub doboru trudności. Stosuj istniejące warunkowe ścieżki dla symulacji, stanu tutora i AI w fazie wykonawczej. Przeczytaj odpowiednią metodę przed jej zaproponowaniem; nie ładuj wszystkich plików referencyjnych naraz.

Przekładaj wybraną metodę na obserwowalne zachowanie produktu i miarodajny test. Odróżniaj decyzje zaproponowane, wybrane, wdrożone i zweryfikowane. Weryfikacja techniczna nie dowodzi skuteczności edukacyjnej.

## Ścieżka pracy

Podążaj tą ścieżką z głębokością odpowiadającą potrzebom zadania: określ cel i ograniczenia → wybierz metodę odpowiadającą trudności poznawczej → powiąż aktywność ucznia z dowodem uczenia się → wdróż rozwiązanie w ramach zakresu → sprawdź rezultat. W przypadku audytu zbadaj istniejący projekt zamiast pisać kod. Wykorzystuj znany kontekst; nie wymagaj sformalizowanego dokumentu planistycznego dla każdego kroku.

Przeczytaj [przykłady decyzji](references/decision-examples.md), gdy doprecyzowania wymaga pomoc, akceptacja odpowiedzi alternatywnych lub niepewna zgodność z podstawą programową. Ilustrują one decyzje, nie są gotowymi szablonami do kopiowania do każdej lekcji.

## Określenie kontekstu edukacyjnego

Wykorzystuj informacje już obecne w zapytaniu, projekcie i dostarczonych materiałach. W przypadku luk w kontekście pytaj tylko o kwestie, które w istotny sposób zmieniają projekt. Przy drobnych niepewnościach przyjmij rozsądne założenie i kontynuuj. Unikaj sztywnych ankiet i powtarzających się próśb o zatwierdzenie rutynowych wyborów objętych już treścią zadania.

Zidentyfikuj kontekst wpływający na projekt: uczniów i ich wiedzę uprzednią, przedmiot, zamierzone efekty kształcenia, pracę w klasie lub samodzielną, dostępny czas i urządzenia, język, potrzeby dostępności oraz ewentualną dostarczoną podstawę programową. Uwzględniaj ramy programowe, gdy odnosi się to do danego środowiska; nie zakładaj z góry jednego systemu krajowego. Dobierz ton do kontekstu i preferencji autora. Nie wnioskuj o uwadze, motywacji, zdolnościach ani preferowanej pedagogice na podstawie etykiet pokoleniowych.

Uwzględniaj otoczenie dydaktyczne, gdy jest to pomocne: przygotowanie, pracę indywidualną lub grupową, interwencję nauczyciela, dyskusję i podsumowanie. Pokaz prowadzony przez nauczyciela może wymagać dobrego pytania do dyskusji; konta użytkowników i indywidualne rejestry ocen nie są konieczne.

Rozróżniaj wiek, rolę edukacyjną i doświadczenie w danym temacie: dziecko, uczeń szkoły podstawowej, uczeń szkoły ponadpodstawowej, student i dorosły uczestnik nie są pojęciami zamiennymi ani poziomami zdolności. Definiując lub modyfikując grupę docelową, przeczytaj profil ucznia w [dialogu projektowym](references/design-dialogue.md). Dostosuj terminologię i wsparcie do środowiska; w ogólnych wskazówkach stosuj neutralne określenia. Twórca, uczeń i towarzyszący nauczyciel lub rodzic mogą być różnymi osobami.

## Łączenie celów z obserwowalną aktywnością

Dla każdego istotnego celu powiąż działanie ucznia, dowód uczenia się, kryteria sukcesu, warunki udzielenia pomocy i kolejną decyzję dydaktyczną. W przypadku małych zadań zachowaj zwięzłość. Przy otwartym dociekaniu dowód może dotyczyć jakości pytań, posługiwania się faktami lub rewizji wyjaśnienia; jedna z góry ustalona odpowiedź nie jest jedyną możliwością.

Przykład: uczeń przewiduje, jak zmiana oporu wpływa na natężenie prądu, sprawdza to w modelu, wyjaśnia ewentualne rozbieżności i rozwiązuje nowe zadanie samodzielnie. Samo przesunięcie suwaka lub przejście do kolejnego ekranu nie dowodzi zrozumienia.

Na podstawie zaobserwowanej trudności w uczeniu się dobierz adekwatną interwencję. Traktuj wyjaśnienie błędu jako hipotezę roboczą, a nie ostateczną diagnozę. Wybierz spójny, niewielki zestaw metod; nie dodawaj funkcji tylko dlatego, że znajdują się w katalogu. Przeczytaj [metody](references/methods.md) przy wyborze lub wdrażaniu metody, sekwencji wsparcia lub reguły progresji.

W przypadku mechanik gier, elementów motywacyjnych lub audytu gier edukacyjnych przeczytaj [gry edukacyjne i celowa grywalizacja](references/learning-games.md). Zawiera omówienie grywalnych pętli edukacyjnych, doboru mechanik, granic dowodowych i wdrożeń — od drobnych pomocy dydaktycznych po produkty długoterminowe. Dostosowuj rozwiązania do szkół podstawowych, ponadpodstawowych, uczelni i dorosłych w różnych krajach, opierając się na wiedzy uprzedniej i lokalnym kontekście.

Referencja metod szczegółowo obejmuje: dialog sokratejski, technikę Feynmana, strefę najbliższego rozwoju (ZPD) i rusztowanie poznawcze (scaffolding), przykłady z rozwiązaniem (worked examples), praktykę przypominania i powtórki rozłożone w czasie, uczenie się na błędach, metapoznanie, dociekanie (inquiry), odgrywanie ról (role-play), uczenie się rówieśnicze i kooperatywne, metodę projektów, klasę odwróconą oraz opcjonalną grywalizację. Są to podejścia do wyboru, a nie obowiązkowe elementy każdej aplikacji.

Taksonomia Blooma opisuje cele poznawcze i rodzaje wiedzy. Rozdzielaj poziom trudności od wymagań wstępnych; nie wprowadzaj sztywnych sześciu zablokowanych poziomów. W przypadku umiejętności praktycznych lub społecznych dobieraj adekwatne dowody i otwarcie określaj, czego zadanie na ekranie nie jest w stanie zweryfikować.

## Wybór realistycznej realizacji technicznej

Rozróżniaj AI używane do budowy aplikacji od AI wykorzystywanego przez uczniów w gotowym produkcie. Wybieraj między zweryfikowaną treścią statyczną, deterministycznymi interakcjami lub symulacjami a AI w fazie wykonawczej (runtime), kierując się celem i ograniczeniami środowiskowymi. Wskazówki, informacja zwrotna i powtórki rozłożone w czasie mogą doskonale działać bez zewnętrznej usługi AI.

Przed dodaniem rozbudowanej funkcji rozważ jej wkład dydaktyczny, obciążenie interakcyjne, nakład pracy nauczyciela, utrzymanie, wymogi dotyczące danych i koszty eksploatacji. Wyjaśniaj istotne kompromisy. Nie wprowadzaj kont, analityki, paneli administratorskich, backendu, płatnych usług ani zewnętrznych przepływów danych tylko po to, by aplikacja sprawiała wrażenie kompletnej. Potwierdzaj decyzje zmieniające zakres, jeśli nie zostały wcześniej uzgodnione.

Przeczytaj [symulacje](references/simulations.md), projektując model zjawiska, eksperyment lub odgrywanie ról. Wyraźnie rozróżniaj rzeczywiste obserwacje, obliczenia modelu i rekonstrukcję fikcyjną. Nigdy nie przedstawiaj wygenerowanych przez AI danych jako pomiarów ani nie twórz pozorów przeprowadzenia realnego eksperymentu.

Przeczytaj [sztuczna inteligencja w fazie wykonawczej](references/runtime-ai.md) tylko wtedy, gdy gotowy produkt odwołuje się do usługi AI w trakcie użytkowania. Zdefiniuj rolę dydaktyczną, granice źródeł, nadzór człowieka, przepływy danych, limity kosztów i zachowanie w stanach awaryjnych. Prompt nie zastępuje zabezpieczeń aplikacji.

Przeczytaj [tryby i ciągłość tutora](references/tutor-state.md), implementując wieloetapowe prowadzenie ucznia, przejścia między ćwiczeniami a sprawdzianem lub wznawianie nauki. Przechowuj stan i dowody w samej aplikacji; funkcje te nie wymagają runtime AI.

## Budowanie wiarygodnej informacji zwrotnej i decyzji

Zapewnij użyteczny kolejny krok po wystąpieniu błędu. W trybie ćwiczeń umożliwiaj skorzystanie z pomocy i przejście do bezpośredniego wyjaśnienia lub rozwiązanego przykładu; unikaj niekończącego się odpytywania. Ograniczaj wsparcie na podstawie samodzielnych osiągnięć, zachowując dostęp do pomocy na żądanie. Sprawdzian może ograniczać pomoc na wyraźnie określonych warunkach.

Rozróżniaj samodzielny sukces, sukces z pomocą, ujawnienie odpowiedzi i stan niepewności. Jedno trafne zgadnięcie, deklaracja pewności siebie lub dwa udane zadania ze wsparciem nie oznaczają opanowania materiału. Nie wnioskuj o trwałych uzdolnieniach, motywacji ani zaburzeniach na podstawie krótkiej interakcji.

Przeczytaj [ocenianie](references/assessment.md), projektując punktowane zadania, kryteria oceniania (rubryki), adaptacyjność lub ewaluację uczenia się. Weryfikuj poprawność merytoryczną, prawdopodobne alternatywy, jednostki liczbowe i tolerancje oraz to, czy zadanie rzeczywiście wymaga docelowej umiejętności. Uwzględniaj poprawne alternatywne metody i wyjaśnienia. Oddzielaj nagrody w grze i tempo pracy od faktycznych osiągnięć, chyba że szybkość jest jawnym celem kształcenia.

## Zachowanie dostępności i decyzyjności nauczyciela

Projektuj z uwzględnieniem kryteriów WCAG 2.2 na poziomie AA odpowiadających danej aktywności i rzeczywistym potrzebom uczniów. Zapewnij obsługę z klawiatury, widoczny fokus, zrozumiałe etykiety i komunikaty zwrotne, alternatywy dla samego koloru lub dźwięku oraz uzasadniony lub regulowany czas na odpowiedź. Dobieraj sposoby percepcji informacji i wyrażania zrozumienia do ucznia; nie przypisuj uczniom sztywnych „stylów uczenia się”. W razie potrzeby skorzystaj ze specjalistycznych wytycznych dostępności.

Zbieraj wyłącznie dane niezbędne do przeprowadzenia aktywności i jasno określ, kto ma do nich dostęp, dokąd trafiają i jak długo są przechowywane. Uwzględniaj wymagania dostawców, szkół i lokalnych przepisów w miejscu wdrożenia; nie twórz uniwersalnych reguł prawnych. Lokalna, anonimowa aktywność nie wymaga tworzenia kont ani trwałego śledzenia.

Zapewnij nauczycielowi lub autorowi możliwość weryfikacji treści, korygowania ocen i ingerencji w nieodpowiednią adaptację. Zwykle wystarczy edytowalny plik z zawartością; pełny system zarządzania nauczaniem nie jest konieczny. Ważne decyzje dotyczące oceniania lub kwalifikacji wymagają odpowiedzialnej weryfikacji przez człowieka.

## Koordynacja wiedzy specjalistycznej bez rozbudowy procesu

Wykorzystuj następujące perspektywy w zależności od potrzeb; w małym zadaniu jeden agent może łączyć je wszystkie:

- Metodyk: zamierzone efekty, kontekst dydaktyczny i wybory metodyczne.
- Dydaktyk przedmiotowy: poprawność merytoryczna, wymagania wstępne, przykłady i typowe błędy poznawcze.
- Projektant oceniania: dowody uczenia się, kryteria, alternatywy i granice wnioskowania.
- Projektant interakcji: przepływ pracy ucznia, pomoc, dostępność i zastosowanie w klasie.
- Programista: struktury danych, obliczenia, stan, trwałość i obsługa błędów.
- Recenzent: rozbieżności między celem, projektem a zaobserwowanym działaniem.

Przekładaj ich ustalenia na implementację. Nie nazywaj wygodnego wyboru technicznego poprawnym pedagogicznie bez dowodów. Rozstrzygaj istotne spory poprzez weryfikację źródeł, ukierunkowany test lub jasne sformułowanie otwartego pytania. Stosuj niezależną recenzję, gdy uzasadnia to złożoność lub waga decyzji; nie twórz zespołu do każdego zadania. Uruchamiaj inne skille tylko wtedy, gdy są dostępne i niezbędne.

## Weryfikacja i raportowanie na właściwym poziomie

Przy wdrażaniu sprawdzaj ścieżkę ucznia, błędy rzeczywiście popełniane przez uczniów, ścieżkę pomocy i istotne stany awaryjne. W przypadku zapytań czysto analitycznych przedstaw wnioski i propozycje bez modyfikacji produktu. Dostosuj testy do specyfiki aplikacji: symulacja wymaga sprawdzenia modelu; runtime AI wymaga testów odporności na awarie usługi i obsługi generowanych odpowiedzi; prosta aktywność statyczna domyślnie nie potrzebuje żadnego z tych mechanizmów.

Oddzielaj trzy kategorie wniosków: poprawność techniczną, adekwatność dydaktyczną i zaobserwowane efekty uczenia się. Same testy techniczne nie dowodzą skuteczności edukacyjnej. Niewielki pilotaż może ujawnić problemy bez wykazywania związku przyczynowo-skutkowego. Raportuj faktycznie przeprowadzone testy i nierozstrzygnięte założenia; nie wymyślaj obserwacji uczniów ani wyników skuteczności.

Przy przekazywaniu wyników podsumuj cel edukacyjny, wybrane podejście, istotne założenia operacyjne, faktycznie wykonane testy i pozostałe ograniczenia. Dołącz tabelę powiązania celów z dowodami tylko wtedy, gdy ułatwia to korzystanie z rezultatu. Dostosuj formę do życzenia użytkownika.

## Tworzenie tekstów dla uczniów bez żargonu AI (AI slop)

Język aplikacji jest nośnikiem dydaktyki. Stosuj te same standardy do poleceń, instrukcji, informacji zwrotnej i wyjaśnień:

- Wykreśl puste przymiotniki („nowoczesny”, „angażujący”, „interaktywny”), chyba że kolejne zdanie natychmiast wyjaśnia, na czym polega ta cecha.
- Formułuj myśli bezpośrednio; unikaj konstrukcji typu „to nie tylko X, ale również Y” oraz „to nie X, to Y”.
- Pomiń zapowiedzi w rodzaju „w tej aktywności nauczysz się”; napisz wprost, co uczeń robi.
- Informacja zwrotna wskazuje precyzyjnie: co jest poprawne, czego brakuje i jaki jest kolejny konkretny krok.
- Podawaj precyzyjne liczby, jednostki i warunki; unikaj sformułowań typu „znacząco poprawia” bez podania miary.
- Żadnych emoji w przyciskach, nagłówkach ani etykietach. Używaj tekstu i spójnego zestawu ikon.
- Dostosuj słownictwo do uczniów i konsekwentnie stosuj jedno pojęcie na określenie danej rzeczy.

Przeczytaj tekst oczami ucznia. Jeśli zdanie mogłoby pojawić się bez zmian w dowolnym innym produkcie, wykreśl je lub sformułuj konkretnie.

## Integracja

Przy wyborze modelu, nakładu rozumowania (effort), szybkości lub dostosowywaniu mechanizmu ładowania przeczytaj [profile modeli i środowisk](references/model-profiles.md). Zawiera on wskazówki oparte na dokumentacji OpenAI, Claude i Gemini. Utrzymuj wspólny standard dydaktyczny i oddzielaj faktycznie przeprowadzone testy od deklarowanej kompatybilności. Nie wczytuj profilu dla zwykłego zadania edukacyjnego, które tego nie wymaga.

Rozwiązanie przeznaczone do gier edukacyjnych, quizów, samouczków, symulacji i audytów ich struktury dydaktycznej. Rdzeń nie wymaga pakietów zewnętrznych, API, konkretnego modelu AI ani danych uczniów. Materiały źródłowe są warunkowe. Pakiet natywny używa tego pliku i powiązanych referencji; `metodyki-nauczania.md` jest wygenerowaną wersją autonomiczną. Instalacja, wdrożenie i inne zmiany zewnętrzne wymagają autoryzacji tych działań. Skill nie zastępuje instrukcji projektowych ani nie rozszerza uprawnień.

Materiały referencyjne do projektowania: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [Wytyczne UDL organizacji CAST](https://udlguidelines.cast.org/). Służą one jako wsparcie w projektowaniu i ewaluacji; powołanie się na nie nie stanowi certyfikatu zgodności ani skuteczności edukacyjnej.
