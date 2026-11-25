---
name: kalky
description: Najde v českém nebo slovenském textu kalky z angličtiny (doslovně přeložené vazby typu „uvnitř sedí čip", „výhoda leží v ceně"), bohemizmy ve slovenštině a antitezi „A, ne B", po které text zní jako AI. Ke každému nálezu dá přirozenou náhradu. Použij před odevzdáním jakéhokoli českého nebo slovenského textu (článek, překlad, e-mail, produktový popis), když uživatel chce text „učesat", „zkontrolovat češtinu", „najít kalky" nebo „aby to neznělo jako AI", a když při psaní narazíš na nový kalk, který v seznamu chybí.
license: MIT (kód), CC BY 4.0 (data), bohemizmy MIT (Zdeno Kuzmany)
metadata:
  author: Zdeněk Dvořák, Linki.cz
  repository: https://github.com/zdenekdvorak-linki/kalky
---

# Kalky, bohemizmy a AI obraty

Seznam vznikl při redakční práci na českých a slovenských webech. Každé
pravidlo má regex, větu, kterou musí chytit, a většinou i protipříklad,
který chytit nesmí.

## Co je ve složce

| Soubor | Obsah |
|---|---|
| `data/cs/kalky.md` | české kalky: kalk, anglický originál, přirozená náhrada |
| `data/cs/calques.json` | regexy ke kalkům, obecný vzor kalku a antiteze |
| `data/sk/kalky.md`, `data/sk/calques.json` | totéž pro slovenštinu |
| `data/sk/bohemismy.json` | česká slova a tvary ve slovenském textu |
| `data/ai-obraty.md` | obraty, podle kterých čtenář pozná text od AI (posuzuje se čtením) |
| `scripts/check.py` | kontrola textu, jen standardní knihovna Pythonu 3.9+ |
| `scripts/add_calque.py` | zápis nového kalku do dokumentu i JSONu naráz |

## Postup

1. **Zkontroluj text skriptem**, pokud umíš spustit Python. Cesty jsou
   relativní ke složce tohoto skillu:

   ```bash
   python scripts/check.py text.md              # čeština
   python scripts/check.py --lang sk text.md    # slovenčina
   python scripts/check.py --json - < text.md   # strojový výstup
   ```

   Návratový kód 0 = čisté, 1 = nálezy, 2 = rozbitá data. Sekce „Varování"
   (obecný vzor kalku, tři a víc vět začínajících „Tento/Tato/Toto") verdikt
   neovlivní, nálezy z ní posuď podle kontextu.

2. **Bez Pythonu** (chat bez spouštění kódu) si přečti `data/cs/kalky.md`
   (nebo `data/sk/kalky.md` a `data/sk/bohemismy.json`) a projdi text proti
   odrážkám sám.

3. **Projdi text proti `data/ai-obraty.md`.** Strojově se z něj kontroluje
   jen antiteze, zbytek (zmizelý konatel, trojice bez slovesa, vymyšlená
   motivace autora) musíš posoudit čtením.

4. **Oprav nálezy** podle náhrady za šipkou. Náhrada ukazuje směr, do věty
   ji přizpůsob tak, aby zůstala gramaticky správně a zachovala význam.

## Když najdeš kalk, který v seznamu chybí

Navrhni ho do repozitáře, ať ho příště chytí i ostatní. Potřebuješ pět věcí:
kalk, anglický originál, náhradu, větu, kterou má regex chytit, a protipříklad,
který chytit nesmí. Protipříklad piš vždy, bez něj vznikají příliš široké
regexy.

- **Agent s přístupem ke Gitu** (Claude Code, Codex): forkni repo, zapiš kalk
  skriptem `scripts/add_calque.py`, spusť `python -m unittest discover tests`
  a otevři pull request. Podrobnosti v `CONTRIBUTING.md` v kořeni repa.
- **Chatový agent** (claude.ai, ChatGPT): sestav uživateli odkaz na
  předvyplněné issue a nech ho odeslat jedním klikem. Tvar odkazu je
  v `AGENTS.md` v kořeni repa.

Do seznamu patří jen kalk, který je chybou v každém kontextu. Stylová
preference jednoho webu nebo redakce do něj nepatří.
