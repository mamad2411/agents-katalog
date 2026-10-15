---
name: debug-500
description: Diagnostiquer et corriger une erreur 500 ou une exception Laravel. Utiliser automatiquement quand l'utilisateur signale une erreur 500, un crash, une exception ou un bug backend.
allowed-tools: Bash, Read, Grep, Glob
---

# Debug erreur 500 / Exception Laravel

Contexte de l'erreur : $ARGUMENTS

## Procedure de diagnostic

### Etape 1 : Lire les logs

```bash
docker exec laravel_app tail -100 /var/www/html/storage/logs/laravel.log
```

Chercher :
- Le message d'exception exact
- La stack trace (fichier + ligne)
- Le timestamp (pour isoler l'erreur recente)

### Etape 2 : Identifier la cause

Causes frequentes dans ce projet :
1. **Chemin de fichier invalide** : disk S3 vs local, double prefixe (ex: `templates/templates/`)
2. **Config cachee** : `docker exec laravel_app php artisan config:clear`
3. **Relation Eloquent** : relation null non geree, N+1 query
4. **team_id manquant** : scope global qui filtre tout
5. **Permission fichier** : `storage/` non writable
6. **Package manquant** : composer require oublie
7. **Migration non executee** : colonne inexistante

### Etape 3 : Reproduire

Identifier la route exacte et les parametres :
```bash
docker exec laravel_app php artisan route:list --path=<route-concernee>
```

### Etape 4 : Corriger

- Appliquer le fix minimal
- Verifier avec `config:clear` si modification de config
- Tester que l'erreur ne se reproduit plus

### Etape 5 : Verifier

```bash
docker exec laravel_app tail -20 /var/www/html/storage/logs/laravel.log
```

Confirmer qu'aucune nouvelle erreur n'apparait.
