# Database Schema Design

Conçoit et crée des schémas de base de données pour Supabase.

## Instructions

Paramètre : $ARGUMENTS (description de la feature nécessitant un schéma)

1. **Conventions Aurion Supabase**
   - Noms de tables en snake_case pluriel
   - Colonnes : id (uuid), created_at, updated_at
   - Foreign keys avec ON DELETE CASCADE approprié
   - RLS policies pour chaque table

2. **Design du schéma**
   - Identifie les entités nécessaires
   - Définis les colonnes avec types PostgreSQL
   - Définis les relations (1:1, 1:N, N:M)
   - Définis les indexes pour les requêtes fréquentes
   - Définis les RLS policies (qui peut lire/écrire quoi)

3. **Migration**
   - Crée le fichier : `supabase/migrations/[timestamp]_[description].sql`
   - Format : `YYYYMMDD_[description].sql`
   - Inclure : CREATE TABLE, ALTER TABLE, CREATE INDEX, RLS policies
   - Inclure le rollback en commentaire

4. **Tables existantes critiques**
   - user_credits : balance, monthly_allowance, bonus_credits, period_start, period_end
   - profiles : user metadata
   - Ne pas modifier ces tables sans review

5. **Validation**
   - SQL syntaxiquement correct
   - RLS policies testées
   - Pas de données exposées sans auth
