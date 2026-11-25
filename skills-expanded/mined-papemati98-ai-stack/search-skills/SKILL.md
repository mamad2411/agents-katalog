---
name: search-skills
description: Uzyj, gdy potrzebujesz gotowego skilla/pluginu Claude Code zamiast pisac od zera - np. "znajdz skill do X", "czy jest gotowy skill na Y", "poszukaj skilla do designu / testow / PDF / dokumentow". Przeszukuje ZAUFANE zrodla (oficjalny marketplace Anthropic najpierw, potem reputowane spolecznosciowe), rankuje po zaufaniu, pilnuje anti-sprawl (max jeden skill na dana zdolnosc - nie 10 roznych do tego samego) i KAZDEGO kandydata przepuszcza przez skill-auditor przed instalacja. Nigdy nie instaluje na slepo.
---

# Search skills — reuse before building, with judgment

Mnostwo skilli juz istnieje — nie ma sensu pisac wszystkiego samemu. Ale rynek skilli
jest **niezaufany z definicji** (incydent ToxicSkills/ClawHub: dziesiatki zlosliwych
skilli w obiegu). Dlatego ten skill nie tylko *znajduje*, ale **filtruje po zaufaniu,
pilnuje porzadku i wymusza audyt** przed instalacja.

Dwie zasady nadrzedne:
1. **Trust-gating** — preferuj zrodla od najbardziej do najmniej zaufanych; nieznane
   automatycznie ida na ostrzejszy audyt.
2. **Anti-sprawl** — zanim dodasz skill w danej kategorii, sprawdz czy juz nie masz
   czegos co to robi. **Max jeden skill na zdolnosc**, chyba ze jest twarde uzasadnienie.

---

## Krok 1 — ustal czego naprawde brakuje

Nazwij konkretna zdolnosc (1 zdanie): "potrzebuje skilla, ktory robi X".
Potem uruchom `select-skills` i sprawdz jego aktualny inventory. Dopiero gdy nie
ma lokalnej zdolnosci, wykonaj dodatkowy odczyt katalogow (anti-sprawl):

```powershell
$roots = @($env:SKILL_ROOT, (Get-Location).Path) |
  Where-Object { $_ -and (Test-Path -LiteralPath $_) } |
  Select-Object -Unique
Get-ChildItem -LiteralPath $roots -Filter 'SKILL.md' -File -Recurse -ErrorAction SilentlyContinue |
  Where-Object { $_.FullName -notmatch '\\node_modules\\' } |
  Select-Object -ExpandProperty FullName
```

Jesli istniejacy skill pokrywa zdolnosc — **nie szukaj nowego**, ulepsz istniejacy
albo po prostu go uzyj. Zglos to uzytkownikowi i zatrzymaj sie tutaj.

## Krok 2 — szukaj w kolejnosci zaufania

Przeszukuj **od gory listy w dol** i zatrzymaj sie, gdy znajdziesz dobry kandydat
z wyzszego poziomu — nie schodz nizej bez potrzeby.

| Poziom | Zrodlo | Zaufanie | Jak |
|---|---|---|---|
| 1 | **Oficjalny marketplace Anthropic** (`anthropics/claude-plugins-official`) | Najwyzsze | `Get-ChildItem` lokalnej kopii marketplace; tam sa m.in. frontend-design, skill-creator, pr-review-toolkit, mcp-server-dev |
| 2 | **Oficjalne repo / dokumentacja Anthropic** (anthropics/skills, docs) | Wysokie | WebSearch "site:github.com/anthropics skill X", WebFetch README |
| 3 | **Reputowane listy spolecznosciowe** (awesome-claude-code, awesome-claude-skills) | Srednie | WebSearch; oceń liczbe gwiazdek, aktywnosc, znanego autora |
| 4 | **Pojedyncze repo/gisty od nieznanych autorow, ClawHub i podobne huby** | Niskie / nieufne | Tylko jesli nic wyzej nie ma; **traktuj jak potencjalnie zlosliwe** |

Dla kazdego kandydata zbierz: nazwe, autora, URL, gwiazdki/aktywnosc, opis, licencje.

## Krok 3 — zawez do JEDNEGO (anti-sprawl)

Nie przynos 10 opcji do zainstalowania. Wybierz **maks 1–2 najlepszych** kandydatow
na zdolnosc i uzasadnij wybor: najwyzszy poziom zaufania + najlepsze dopasowanie do
potrzeby. Pokaz uzytkownikowi krotka tabele (nazwa / zrodlo / poziom zaufania /
dlaczego ten), a nie liste-smietnik.

Jesli oficjalny Anthropic ma odpowiednik — to jest domyslny wybor. Koniec dyskusji,
chyba ze uzytkownik chce inaczej.

## Krok 4 — AUDYT obowiazkowy przed instalacja

Zaden kandydat nie laduje do skills bez audytu. Dla wybranego skilla **wywolaj
[[skill-auditor]]** z jego URL/sciezka. Czekaj na werdykt:
- **BLOCK** — odrzuc, wroc do kroku 2 po inny kandydat (albo zaproponuj napisanie
  wlasnego skilla od zera, czysto).
- **MANUAL_REVIEW** — pokaz raport uzytkownikowi, instalacja tylko po swiadomej zgodzie.
- **ALLOW** — zaproponuj instalacje.

Wyjatek tylko dla poziomu 1 (lokalny oficjalny marketplace Anthropic) — kod juz jest
podpisanym, zaufanym zrodlem; mozna pominac kwarantanne, ale i tak warto rzucic okiem
skanerem dla spojnosci. Wszystko z poziomu 2–4 przechodzi pelny audyt.

## Krok 5 — instalacja + wpis do ewidencji

Po ALLOW + zgodzie: zainstaluj (oficjalny -> wlacz plugin/skopiuj skill; zewnetrzny ->
skopiuj zwalidowana kopie z kwarantanny). Zanotuj krotko: jaki skill, skad, jaka
zdolnosc pokrywa, kiedy audytowany. To zamyka petle anti-sprawl na przyszlosc.

---

## Zasady twarde

- **Nie instaluj na slepo.** Discovery konczy sie propozycja + audytem, nie faktem.
- **Jeden skill na zdolnosc.** Jesli proponujesz drugi do tego samego — uzasadnij
  albo odpusc. Cel: brak chaosu 10 skilli UI.
- **Oficjalne wygrywa.** Anthropic marketplace to domyslny pierwszy wybor.
- **Nieznane = nieufne.** Brak gwiazdek/historii/znanego autora -> ostrzejszy audyt,
  domyslnie odrzuc jesli cokolwiek zgrzyta.
- Kazdy zewnetrzny kandydat **musi** przejsc [[skill-auditor]]. Bez wyjatkow dla
  poziomow 2–4.

## Powiazane
- [[skill-auditor]] — brama bezpieczenstwa; wywolywana na kazdego kandydata.
