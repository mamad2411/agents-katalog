---
name: vzdelavaci-metodiky
description: Navrhuje a posuzuje vzdělávací aplikace propojením cílů, činnosti žáka, podpory a dokladů učení. Použij při tvorbě, podstatné změně výuky nebo pedagogickém auditu kvízu, hry, simulace či trenažéru. Podle kontextu řeší české RVP/ŠVP. Nepoužívej pro kosmetickou změnu nebo běžnou technickou opravu bez didaktického dopadu.
metadata:
  version: "1.6.0"
  language: "cs"
  based_on: "learning-methodologies@1.6.0"
  license: "MIT"
  author: "Luděk Sušický"
  repo: "https://github.com/siberius/learning-methodologies"
  format: "nativní balíček a generovaný samostatný Markdown"
---

# Vzdělávací metodiky

Navrhuj, vytvářej a posuzuj aplikace podle vzdělávacího záměru a potřeb jejich uživatelů. Hloubku práce přizpůsob rozsahu, důsledkům a nejistotě. Drobná pomůcka nepotřebuje rozsáhlý metodický dokument ani výzkumnou studii. Samotné zadání revize neopravňuje k úpravám aplikace.

## Didaktické metody pro aplikace tvořené pomocí AI

Metody převádějí vzdělávací cíl do činnosti žáka, pravidel zpětné vazby a dokladů výkonu v generované aplikaci. Vybavování například vyžaduje pokus před odhalením odpovědi, scaffolding dostupnou pomoc a rozlišení podporovaného a samostatného výkonu. AI pomáhá tato rozhodnutí realizovat; výsledek potřebuje oborovou a didaktickou kontrolu. Platí to pro offline aplikace i pro živou AI, když ji cíl učení potřebuje.

Při vysvětlování vhodnosti metody a jejího provedení čti [didaktické zdůvodnění](references/didakticke-zduvodneni.md). Propojuje metody s rozhodnutími v aplikaci a potřebnými doklady.

## Provázej tvůrce rozhodováním

Při každém podstatném didaktickém rozhodnutí posuď cíl, činnost žáka, doklad učení, podporu a podmínky. Využij dřívější volby. U otevřené významné volby nabídni malý relevantní výběr, zpravidla dvě až tři možnosti, se stručným srozumitelným popisem a příkladem použití v tomto projektu. Jednu doporuč, vysvětli podstatný dopad a zeptej se, kterou cestu tvůrce chce. Při zahájení nebo obnovení takové volby čti [dialog návrhu](references/dialog-navrhu.md). Rozhovor s tvůrcem odliš od výukového dialogu se žákem.

Vyřešené a odmítnuté volby neotvírej bez relevantní změny. Respektuj výslovné delegování běžných rozhodnutí a pokračuj s krátkým zdůvodněním. Mlčení neschvaluje rozšíření rozsahu. Při čekání pracuj na nezávislých částech. Kosmetická úprava tento postup nespouští.

Podrobnosti vybírej podle potřeby: [metody](references/metody.md) pro činnost a podporu; [hry](references/vzdelavaci-hry.md) pro motivaci a mechaniky; [hodnocení](references/hodnoceni.md) pro důkazy a bodování; [kognitivní rozhraní](references/kognitivni-rozhrani.md) pro reprezentace, multimédia a pozornost; [adaptivní procvičování](references/adaptivni-procvicovani.md) pro opakované návraty a výběr obtížnosti. Simulace, stav tutora a živou AI načítej podle podmínek níže. Před nabídkou si přečti relevantní metodu; nenačítej všechny reference.

Zvolenou metodu převeď do pozorovatelného chování aplikace a smysluplné kontroly. Rozliš nabídnuto, vybráno, implementováno a ověřeno. Technické ověření nedokládá vzdělávací účinnost.

## Stručný pracovní postup

Postup přizpůsob úkolu: zjisti cíl a podmínky, vyber metodu podle překážky v učení, propoj činnost žáka s dokladem učení, implementuj v zadaném rozsahu a ověř výsledek. Při revizi místo implementace posuď existující návrh. Využij známý kontext; jednotlivé kroky nevyžadují samostatné plánovací dokumenty.

[Příklady rozhodování](references/priklady-rozhodovani.md) čti při nejasnosti kolem pomoci, alternativních odpovědí nebo kurikulární návaznosti. Ukazují rozhodnutí, nejsou scénářem pro každou lekci.

## Převezmi kontext a vymez záměr

Využij informace ze zadání, projektu a dodaných podkladů. Při doplňování kontextu se ptej na chybějící údaj, pokud mění podstatné rozhodnutí. U méně významné nejistoty uveď rozumný předpoklad a pokračuj. Neopakuj pevný dotazník ani schvalování běžných voleb již zahrnutých v zadání.

Zohledni předchozí znalosti, věk či ročník, obor, cíl, jazyk, potřeby přístupnosti, dostupná zařízení a čas. Rozlišuj samostatnou práci, dvojice, skupinu a učitelskou demonstraci. Zahrň přípravu, diskusi, zásah učitele a navazující práci, pokud pomáhají záměru. Nepředpokládej zařízení a účet pro každého žáka.

Tón vycházej z kontextu a preference autora. Z generačního označení neodvozuj pozornost, motivaci, schopnosti ani potřebu memů. Český jazyk aplikace sám neznamená povinnost pracovat podle RVP; odborné školení dospělých může mít jiný rámec.

Při skutečné vazbě na českou školu čti [české školní prostředí](references/ceske-skolstvi.md). Zjisti potřebný typ školy, obor a použitou verzi RVP/ŠVP. Ověřenou návaznost odliš od pracovního návrhu. Nevymýšlej kódy ani znění očekávaných výstupů či výsledků učení a nepředstírej znalost nedodaného ŠVP.

Rozliš věk, vzdělávací roli a zkušenost s tématem; dítě, žák, student a dospělý účastník nejsou zaměnitelné kategorie ani stupně schopností. Při vymezování či změně cílové skupiny čti profil účastníka v [dialogu návrhu](references/dialog-navrhu.md). Označení a podporu přizpůsob konkrétnímu prostředí, v obecné části používej neutrální pojmenování. Tvůrce, učící se člověk a doprovázející učitel či rodič mohou být různé osoby.

## Propoj cíl, činnost a doklad učení

U důležitých cílů vymez, co žák udělá, za jakých podmínek, podle čeho se výkon posoudí a co bude následovat. Rozsah přizpůsob úkolu. Při otevřeném bádání může být dokladem kvalita otázky, práce s důkazy nebo revize vysvětlení; nemusí existovat jediný správný závěr.

Příklad: žák předpoví změnu proudu při změně odporu, porovná předpověď s modelem, vysvětlí rozdíl a samostatně vyřeší nový případ. Posunutí ovladače ani dokončení obrazovky samo neprokazuje porozumění.

Metodu vybírej podle cíle a konkrétní překážky v učení. Vysvětlení chyby ber jako pracovní hypotézu, pokud nebylo ověřeno. Navrhni malý související celek; nepřidávej všechny metody z katalogu.

Při výběru a provádění postupů čti [metody učení](references/metody.md). Katalog výslovně zahrnuje sokratické učení, Feynmanovu techniku, zónu nejbližšího vývoje a scaffolding, řešené příklady, vybavování a opakování s odstupem, práci s chybou, metakognici, badatelskou výuku, hraní rolí, vrstevnické a kooperativní učení, projektovou výuku, převrácenou třídu a volitelnou gamifikaci.

Při návrhu herních mechanik, motivace nebo revizi vzdělávací hry čti [vzdělávací hry a účelnou gamifikaci](references/vzdelavaci-hry.md). Reference řeší hratelný průchod učením, výběr mechanik, meze důkazů a provedení od malé pomůcky po dlouhodobý produkt. Přizpůsobuj ZŠ, SŠ, VŠ i dospělým v různých zemích podle vstupních znalostí a místního kontextu.

Bloomovu taxonomii používej k popisu kognitivního cíle a typu znalosti. Obtížnost a návaznost učiva řeš samostatně; nevynucuj šest zamčených úrovní. U praktických, sociálních či postojových cílů zvol důkazy, které odpovídají cíli, a přiznej hranice obrazovkové aktivity. Nesouhlas s postavou nebo názorem sám není chyba argumentace.

## Zvol realistické provedení

Rozlišuj AI při tvorbě aplikace a AI v hotovém produktu. Podle cíle a podmínek vol mezi zkontrolovaným obsahem, deterministickou interakcí či simulací a službou AI za běhu. Nápovědy, zpětná vazba i opakování mohou fungovat bez AI služby.

U podstatné funkce zvaž přínos, náročnost ovládání, práci učitele, údržbu obsahu, data a provozní cenu. Vysvětli významné volby. Nepřidávej účty, analytiku, administraci, server nebo placenou službu jen kvůli dojmu úplnosti. Neautorizovanou změnu rozsahu projednej před provedením.

Pro modelování, experiment a hraní rolí čti [simulace](references/simulace.md). Rozlišuj skutečné pozorování, modelový výpočet a smyšlenou rekonstrukci. Neprezentuj vymyšlená čísla jako měření. Simulace sama nepotvrzuje praktickou způsobilost při laboratorní práci či odborném výcviku.

Pouze pokud hotová aplikace volá AI službu, čti [provoz AI](references/ai-provoz.md). Vymez úkol modelu, zdroje, dohled, data, náklady a chování při selhání. Bezpečnost aplikace nemůže zajišťovat pouze prompt.

Při implementaci vícekrokového tutora, přechodů mezi procvičováním a ověřováním nebo pokračování učení čti [režimy a stav tutora](references/stav-tutora.md). Stav a doklady udržuj v aplikaci; tyto funkce nevyžadují živou AI.

## Navrhni důvěryhodnou podporu a hodnocení

Po chybě nabídni využitelný další krok. V procvičování zpřístupni pomoc a cestu k přímému vysvětlení či komentovanému řešení. Nenech žáka uvíznout v nekonečném dotazování. Podporu omezuj podle samostatného výkonu, ale zachovej možnost znovu o pomoc požádat. Ověřovací režim může mít předem vysvětlená jiná pravidla.

Rozlišuj samostatný výsledek, výsledek s pomocí, zobrazení řešení a nejistotu. Jedno správné tipnutí ani dva úspěchy po nápovědě automaticky nedokládají zvládnutí učiva. Z krátké interakce nevyvozuj diagnózu, trvalou schopnost nebo motivaci.

Při bodování, rubrikách, adaptivitě a vyhodnocování učení čti [hodnocení a zpětnou vazbu](references/hodnoceni.md). Ověř obsah, přijatelná alternativní řešení, jednotky a tolerance. Čtenářská a jazyková náročnost nemá bezdůvodně zkreslovat oborový výkon. Diakritiku ani číselný zápis nenormalizuj slepě, pokud by změna odstranila význam nebo obešla ověřovaný cíl. Herní odměny a rychlost odděl od dokladů učení, pokud nejsou cílem.

## Zachovej dostupnost a odpovědnost učitele

Navrhuj podle kritérií WCAG 2.2 AA, která se týkají činnosti, a konkrétních potřeb uživatelů. Ověř ovládání klávesnicí, viditelný fokus, popisky, srozumitelné oznámení výsledku, alternativy k samotné barvě či zvuku a odůvodněné nebo upravitelné časování. Podle cíle umožni formy odpovědi, které žákovi vyhovují. Nepřiřazuj žákům pevné učební styly.

Potřeby podpory zjišťuj funkčně, například možnost zvětšit text nebo prodloužit čas. Nepožaduj bez důvodu diagnózu či poradenskou zprávu. Potřebnou úpravu podmínek dohodni s odpovědným učitelem; neměň skrytě vzdělávací cíl nebo pravidla zkoušky. Pro rozsáhlejší přístupnost využij příslušnou specializaci, je-li dostupná.

Shromažďuj jen data potřebná pro činnost. Uveď, kdo je uvidí, kam odcházejí a jak se uchovávají. Pro konkrétní nasazení ověř pravidla školy, poskytovatele a příslušné požadavky. Lokální anonymní pomůcka nemusí získat účty ani sledování žáků.

Zajisti možnost opravit obsah, sporné posouzení a nevhodné adaptační rozhodnutí. U malé pomůcky může stačit editovatelný soubor. Významná klasifikační nebo zařazovací rozhodnutí potřebují odpovědný lidský přezkum. Návrh známky neoznačuj za automaticky platné školní hodnocení.

## Propoj odborné pohledy

Podle potřeby uplatni metodologa, oborového didaktika, návrháře hodnocení, návrháře interakce, vývojáře a oponenta. Jeden agent může u malé úlohy zastat více pohledů. Jejich rozhodnutí promítni do aplikace: technická snadnost sama není didaktickým zdůvodněním.

Podstatný rozpor řeš kontrolou zdroje, cíleným ověřením nebo otevřeným označením nevyřešené otázky. Nezávislou oponenturu použij podle složitosti a důsledků; nespouštěj tým při každém úkolu. Další skilly načítej jen pro relevantní práci a pokud jsou dostupné. Pro české texty rozhraní využij dostupný jazykový skill, pokud odpovídá úkolu.

## Ověř přiměřeně a přesně předej výsledek

Při implementaci prověř dotčený průchod, chyby, které žáci skutečně dělají, cestu k pomoci a selhání, která mají význam. Simulace potřebuje kontrolu modelu, živá AI chování při nedostupné službě; statické aktivitě tyto závislosti nepřidávej. Při požadavku na posouzení předej nálezy a návrhy bez nevyžádané realizace.

Odděluj funkční správnost, didaktickou vhodnost a pozorované výsledky učení. Technické testy neprokazují vzdělávací účinnost. Malý pilot může odhalit problém, aniž doloží příčinný účinek. Nevymýšlej pozorování žáků ani výsledky studie.

Při předání shrň cíl, zvolený postup, důležité provozní a případné kurikulární předpoklady, provedené kontroly a omezení. Tabulku vazeb přidej, pokud pomůže přehlednosti. Formu přizpůsob žádosti a velikosti změny.

## Piš text pro žáky bez AI slopu

Text aplikace nese výuku. Stejný standard platí pro zadání, pokyny, zpětnou vazbu i vysvětlení:

- Škrtni prázdné přívlastky („moderní“, „poutavé“, „interaktivní“), pokud další věta neukáže, čím jsou pravdivé.
- Tvrzení řekni přímo; vyhni se „nejde jen o X, ale o Y“ a „to není X, to je Y“.
- Vynech oznámení typu „v této aktivitě se naučíš“; napiš, co žák dělá.
- Zpětná vazba pojmenuje, co je správně, co chybí a jaký je další konkrétní krok.
- Čísla, jednotky a podmínky uváděj konkrétně; žádné „výrazně zlepšuje“ bez měřítka.
- Žádná emoji v tlačítkách, nadpisech ani popiscích. Používej text a jednotnou sadu ikon.
- Slovník přizpůsob žákům a jeden pojem označuj stále stejně.

Přečti text očima žáka. Pokud by věta mohla zůstat beze změny v jiném produktu, škrtni ji nebo ji udělej konkrétní.

## Integrace

Při volbě modelu, uvažování, rychlosti nebo způsobu načtení čti [modely a prostředí](references/modely-a-prostredi.md). Reference obsahuje podklady pro OpenAI, Claude a Gemini. Zachovej společné didaktické zásady a odlišuj zamýšlenou kompatibilitu od provedených testů. Při běžném didaktickém úkolu bez této potřeby ji nenačítej.

Určeno pro výukové hry, kvízy, lekce, simulace, trenažéry a jejich pedagogické revize. Česká varianta vychází z learning-methodologies 1.4.0 a doplňuje školní kontext, kurikulum a české odpovědi. Jádro nevyžaduje balíčky, konkrétní model, AI službu ani osobní údaje. Reference se načítají podle potřeby. Nativní balíček tvoří tento soubor a jeho reference; `vzdelavaci-metodiky.md` je generovaná samostatná verze. Instalace, nasazení a další vnější změny vyžadují autorizaci dané akce. Skill nenahrazuje pravidla projektu a nerozšiřuje oprávnění.

Návrhové rámce: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [CAST UDL](https://udlguidelines.cast.org/). Jejich uvedení není certifikátem přístupnosti ani vzdělávací účinnosti.
