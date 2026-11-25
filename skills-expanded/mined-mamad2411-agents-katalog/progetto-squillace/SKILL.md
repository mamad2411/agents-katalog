# Regole di workspace – Progetto Squillace ETL

## Regole ASSOLUTE (non negoziabili)

1. VIETATO generare file Python nella cartella scrapers/ per nuove fonti.
   Per aggiungere un nuovo portale si usa ESCLUSIVAMENTE un file YAML in config/.

2. Il punto di ingresso unico per la pipeline è skills/run_static.py o skills/run_dynamic.py.

3. OBBLIGATORIO leggere skills/SKILL.md prima di eseguire qualsiasi azione
   relativa all'aggiunta di un nuovo comune o portale.

4. VIETATO modificare i file core del progetto senza esplicita approvazione:
   - scrapers/base_scraper.py
   - scrapers/fonte1_scraper.py
   - scrapers/fonte2_scraper.py
   - transform/normalizza.py
   - load/carica_mysql.py

5. Qualsiasi nuova configurazione di portale DEVE essere salvata in config/
   seguendo i template in skills/template_static.yaml o skills/template_dynamic.yaml.

6. Dopo l'esecuzione, verifica sempre nei log del terminale che il numero di
   record inseriti su MySQL sia coerente.
