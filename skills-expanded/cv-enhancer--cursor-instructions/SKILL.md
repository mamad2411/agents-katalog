# CV Builder Development Instructions

## 🛡️ CRITICAL: Safety-First Development Workflow

### Database Protection Rules
- **NEVER** automatically update production database
- **NEVER** flush or delete production data  
- **ALWAYS** require explicit passwords for production migrations
- **ALWAYS** ask for confirmation before any production changes
- **ONLY** work with local Supabase for development

### Development Workflow
1. **Local Development**: All work on local Supabase instance
2. **Schema Changes**: Only modify local DB schema
3. **Code Changes**: Use `develop` or feature branches
4. **Health Checks**: Run automatically on commits/pushes
5. **PR Validation**: Dry run DB checks for PRs to develop
6. **Production**: Manual approval + passwords required

### Safety Guarantees
- ✅ Run health checks on commits
- ✅ Validate schema changes with dry runs
- ✅ Ask for passwords before production migrations
- ✅ Never touch production data without explicit permission

### What I Will NEVER Do
- ❌ Automatically update production database
- ❌ Flush or delete production data
- ❌ Run migrations without explicit approval and passwords
- ❌ Make production changes without confirmation

### Emergency Response
If production data is at risk:
1. Stop all automated processes
2. Assess using Supabase dashboard
3. Restore from backup if necessary
4. Document incident and update procedures

**Remember: When in doubt, ask for confirmation. Production data safety is the top priority.**
