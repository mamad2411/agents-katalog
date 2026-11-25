# CMS-Core Project Rules

## Stack
- Laravel 12, Filament 4, Jetstream Teams, Livewire 3, Spatie Permission, Tailwind

## Code Style
- Language: English for code/comments
- PHP: Allman braces style
- Routes: kebab-case (e.g., `/collaborator/list`, `/client/create`)
- Controllers: PascalCase with Controller suffix
- Models: PascalCase singular

## Restrictions
- NO automatic commits
- DO NOT modify .env
- DO NOT revert user changes
- NO new CSS styles; use existing Vuexy classes

## Teams Toggle
- Config: `config('cms.teams_enabled')` 
- Env: `APP_TEAMS=true|false`
- When `false`: hides team switcher, team settings, create team from UI
- Default: `true`

## Multi-Team Scopes
- Use `BelongsToCurrentTeam` trait in models that filter by `current_team_id`

## User Menu Structure (Filament)
1. Mi Perfil
2. Ajustes del Equipo
3. Crear Nuevo Equipo
4. Team Switcher (alphabetical order, active marked with green check, no icons on non-selected)
5. Salir (with logout icon) - always last, via POST to `Filament::getLogoutUrl()`

## Team Switcher Rules
- Teams listed alphabetically
- Active team shows green checkmark
- Non-selected teams show NO icon
- Active team stays in place (doesn't move to top)

## Logout
- Always via POST method
- URL: `Filament::getLogoutUrl()`


