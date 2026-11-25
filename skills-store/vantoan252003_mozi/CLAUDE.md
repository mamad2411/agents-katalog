# CLAUDE.md — Claude Code Instructions

## Before writing ANY code:
1. Read /SKILL.md (master architecture guide)
2. Read the SKILL.md in the specific directory you are working in
3. Read parent directory SKILL.md files as needed

## Never:
- Import data/ from presentation/
- Import Flutter from domain/
- Create Dio instances outside DI modules
- Hardcode colors, fonts, API endpoints, route strings
- Write tokens to Hive or SharedPreferences
- Add try/catch in UseCase or BLoC layers

## Always:
- Use Either<Failure, T> for all repository methods
- Use AppColors, AppTypography, AppDimensions for styling
- Use ApiConstants for endpoint strings
- Use RouteConstants for route strings
- Follow naming conventions in master SKILL.md section 6.3
