# Cursor Development Rules - Vibe Code Deploy Plugin

**Project:** Vibe Code Deploy WordPress Plugin  
**Purpose:** Enforce WordPress plugin development best practices and coding standards  
**Last Updated:** 2025

---

## WordPress Plugin Development Standards

### Required Standards

All code must follow **WordPress Plugin Development Best Practices**:

- **Reference**: See `docs/WORDPRESS_PLUGIN_BEST_PRACTICES.md` for comprehensive guidelines
- **WordPress Plugin Handbook**: https://developer.wordpress.org/plugins/
- **WordPress Coding Standards**: https://developer.wordpress.org/coding-standards/

### Plugin Lifecycle Hooks

**REQUIRED**: All plugins must implement proper activation, deactivation, and uninstall hooks.

- **Activation Hook**: Set default options, flush rewrite rules, schedule cron jobs
- **Deactivation Hook**: Clear scheduled events, flush rewrite rules
- **Uninstall Hook**: Delete options, transients, clean up database (preserve user data)

**Reference**: See `docs/WORDPRESS_PLUGIN_BEST_PRACTICES.md#plugin-lifecycle-hooks`

### Security Requirements

**ALWAYS**:
- Check `ABSPATH` at the top of all PHP files
- Use `current_user_can( 'manage_options' )` for admin pages
- Use `check_admin_referer()` or `wp_verify_nonce()` for form submissions
- Sanitize all input with WordPress functions (`sanitize_text_field()`, `sanitize_email()`, etc.)
- Escape all output with WordPress functions (`esc_html()`, `esc_attr()`, `esc_url()`)
- Use prepared statements for database queries

**Reference**: See `docs/WORDPRESS_PLUGIN_BEST_PRACTICES.md#security-best-practices`

### Code Organization

**File Structure**:
```
plugin-name/
├── plugin-name.php          # Main plugin file
├── uninstall.php            # Uninstall handler
├── includes/
│   ├── Bootstrap.php       # Plugin initialization
│   ├── Settings.php        # Settings management
│   ├── Services/           # Service classes
│   └── Admin/              # Admin pages
├── assets/
│   ├── css/
│   └── js/
└── tests/                  # Unit tests
```

**Namespace**: Use `VibeCode\Deploy` for core, `VibeCode\Deploy\Services` for services, `VibeCode\Deploy\Admin` for admin pages.

### PHP Standards

**WordPress PHP Coding Standards**:
- **Indentation**: Use tabs (not spaces)
- **Brace Style**: Opening brace on same line
- **Naming**: Use `snake_case` for functions, `PascalCase` for classes
- **Type Declarations**: Use type hints for parameters and return types (PHP 8.0+)
- **Visibility**: Always declare visibility (`public`, `private`, `protected`)
- **Final Classes**: Use `final` for service classes that shouldn't be extended

**Reference**: See `docs/WORDPRESS_PLUGIN_BEST_PRACTICES.md#wordpress-coding-standards`

### Internationalization (i18n)

**REQUIRED**: All user-facing strings must be translatable.

- Use text domain: `vibecode-deploy`
- Use WordPress translation functions: `__()`, `_e()`, `esc_html__()`, `esc_html_e()`
- Always escape translated output

**Reference**: See `docs/WORDPRESS_PLUGIN_BEST_PRACTICES.md#internationalization-i18n`

### Database Management

**REQUIRED**: Track database schema versions and handle upgrades.

- Use `dbDelta()` for table creation
- Track schema version in options
- Handle upgrades in activation hook or upgrade routine

**Reference**: See `docs/WORDPRESS_PLUGIN_BEST_PRACTICES.md#database-management`

### Version Management

**🚨 CRITICAL RULES:**

1. **Auto-increment on build** - The build script (`scripts/build-plugin-zip.sh`) automatically increments the patch version (third number) by 1 on each build
   - Example: `0.1.1` → `0.1.2` → `0.1.3`
   - The script updates both the `Version:` header and `VIBECODE_DEPLOY_PLUGIN_VERSION` constant
2. **Do NOT manually edit version** - Never manually change version numbers in `vibecode-deploy.php`; the build script handles this automatically
3. **Version format**: Semantic versioning (`MAJOR.MINOR.PATCH`, e.g., `0.1.2`)
4. **Why**: Version increments ensure browser cache busting for CSS/JS assets and proper upgrade detection

**Example**:
```php
// vibecode-deploy.php (auto-updated by build script)
 * Version: 0.1.2
define( 'VIBECODE_DEPLOY_PLUGIN_VERSION', '0.1.2' );
```

**Manual version edits (if needed):**
- Only edit version manually if you need to increment MAJOR or MINOR (not PATCH)
- PATCH version is always auto-incremented by the build script
- If you manually change MAJOR or MINOR, the next build will increment PATCH from your manual value

### Build Process

**🚨 CRITICAL RULES:**

1. **ALWAYS build plugin zip after code changes** - After making ANY changes to plugin code, you MUST build the plugin zip:
   ```bash
   cd /Users/tlowing/CascadeProjects/windsurf-project/VibeCodeCircle
   ./scripts/build-plugin-zip.sh
   ```
   - The zip file is required for WordPress installation
   - Build script is at: `scripts/build-plugin-zip.sh`
   - Output goes to: `dist/vibecode-deploy-{version}.zip`
   - **Never commit without building the zip first**

2. **Only versioned zip is created** - The build script creates only `dist/vibecode-deploy-{version}.zip`, NOT an unversioned `vibecode-deploy.zip`
   - Example output: `dist/vibecode-deploy-0.1.2.zip`
   - The unversioned zip is redundant and not created
3. **Version auto-incremented** - Each build automatically increments the patch version by 1
4. **Version updated in code** - The build script automatically updates:
   - `Version:` header in `vibecode-deploy.php`
   - `VIBECODE_DEPLOY_PLUGIN_VERSION` constant in `vibecode-deploy.php`
5. **Build command**: `./scripts/build-plugin-zip.sh`
6. **Output location**: `dist/vibecode-deploy-{version}.zip` (versioned only)

**Why versioned only?**
- Prevents confusion about which version is "latest"
- Enables multiple versions to coexist in `dist/`
- Makes it clear which version was deployed
- Follows WordPress plugin distribution best practices

**Reference**: See `docs/BUILD.md` for complete build documentation

### Admin UI Standards

**REQUIRED**: Follow WordPress admin UI standards.

- Use `wrap` class for page containers
- Use `form-table` for form layouts
- Use WordPress notice classes (`notice`, `notice-success`, `notice-error`, etc.)
- Use `submit_button()` for form submissions
- Use `get_admin_page_title()` for page titles

**Reference**: See `docs/WORDPRESS_PLUGIN_BEST_PRACTICES.md#admin-ui-standards`

### Performance

**REQUIRED**: Optimize for performance.

- Use WordPress transients for caching
- Optimize database queries (use `WP_Query` with appropriate parameters)
- Load assets only when needed
- Use lazy loading for images and scripts

**Reference**: See `docs/WORDPRESS_PLUGIN_BEST_PRACTICES.md#performance`

### Error Handling

**REQUIRED**: Use WordPress error handling patterns.

- Use `WP_Error` for errors
- Use `Logger::error()` for plugin-specific logging
- Use WordPress debug logging when `WP_DEBUG` is enabled

**Reference**: See `docs/WORDPRESS_PLUGIN_BEST_PRACTICES.md#error-handling`

### Testing

**REQUIRED**: Write automated tests for all critical functionality.

- Use PHPUnit with `WP_UnitTestCase`
- Test activation, deactivation, and uninstall hooks
- Test database operations
- Test REST API endpoints
- Test form validation and security

**Reference**: See `docs/WORDPRESS_PLUGIN_BEST_PRACTICES.md#testing`

## Code Standards

### PHP

- **PHP Version**: 8.0+ (required)
- **Type Declarations**: Use type hints for all parameters and return types
- **Visibility**: Use `public static` for service methods
- **Final Classes**: All service classes should be `final`
- **Namespace**: `VibeCode\Deploy` for core, `VibeCode\Deploy\Services` for services, `VibeCode\Deploy\Admin` for admin

### Documentation

- All public methods must have PHPDoc blocks
- Include parameter descriptions and return types
- Document exceptions that may be thrown
- Follow WordPress PHPDoc standards

### Security

- Always check `ABSPATH` at the top of files
- Use `current_user_can( 'manage_options' )` for admin pages
- Use `check_admin_referer()` for form submissions
- Sanitize all input with appropriate WordPress functions
- Escape all output with `esc_html()`, `esc_attr()`, `esc_url()`

## Prohibited Practices

### ❌ NEVER Do These

1. Skip activation/deactivation/uninstall hooks
2. Delete user data on deactivation (only on uninstall, and preserve by default)
3. Use `var` in JavaScript (use `const` or `let`)
4. Use `!important` in CSS (breaks WordPress frameworks)
5. Hardcode URLs or paths (use WordPress functions)
6. Skip input sanitization in PHP
7. Skip output escaping in PHP
8. Use deprecated WordPress functions
9. Skip capability checks for admin pages
10. Skip nonce verification for form submissions
11. Skip internationalization for user-facing strings
12. Skip automated tests for critical functionality
13. **Make code changes without incrementing plugin version**

## Quick Reference

### Adding a New Service

1. Create file in `includes/Services/YourService.php`
2. Use namespace `VibeCode\Deploy\Services`
3. Make class `final`
4. Use `public static` methods
5. Add PHPDoc blocks
6. Check `ABSPATH` at top
7. Require in `Bootstrap.php`
8. Write unit tests

### Adding a New Admin Page

1. Create file in `includes/Admin/YourPage.php`
2. Use namespace `VibeCode\Deploy\Admin`
3. Make class `final`
4. Use `public static` methods
5. Check capabilities
6. Verify nonces
7. Escape output
8. Require in `Bootstrap.php`
9. Register in `init()` method

### Adding a New Hook

1. Use consistent naming: `vibecode_deploy_{event}`
2. Document hook in Developer Guide
3. Fire at appropriate time
4. Pass relevant data as parameters
5. Allow filtering of data with filters

---

## File Organization Rules

### Documentation and Reports Organization - REQUIRED

**Standard Folder Structure:**
All projects must use the following folder structure for documentation and diagnostic files:

```
{project-root}/
├── docs/                          # Core project documentation
│   ├── PRD-VibeCodeDeploy.md      # Product Requirements Document
│   ├── DEPLOYMENT-GUIDE.md        # Deployment guide
│   ├── DEVELOPER_GUIDE.md         # Developer guide
│   └── ...                        # Other permanent documentation
│
├── reports/                       # Diagnostic reports and audits
│   ├── deployment/                # Deployment-related reports
│   │   ├── compliance-reviews/    # Compliance audit reports
│   │   ├── visual-comparisons/    # Visual comparison reports
│   │   └── deployment-status/     # Deployment readiness docs
│   ├── development/               # Development-related reports
│   │   ├── implementation-summaries/
│   │   ├── code-reviews/
│   │   └── feature-status/
│   └── archive/                   # Archived reports (older than 90 days)
│
└── {project files}                # Plugin code, scripts, etc.
```

**File Categorization Rules:**

1. **`docs/` Folder - Permanent Documentation**
   - Long-term project documentation that should be version-controlled
   - Examples: `PRD-VibeCodeDeploy.md`, `DEPLOYMENT-GUIDE.md`, `DEVELOPER_GUIDE.md`, `ARCHITECTURE.md`
   - Criteria: Files referenced regularly and provide ongoing value

2. **`reports/` Folder - Diagnostic Reports**
   - Audit reports, implementation summaries, code reviews, development status
   - Subfolders organize by category (deployment, development)
   - Use date-based naming: `{category}-{description}-{YYYY-MM-DD}.md`
   - Example: `development-implementation-summary-2025-01-10.md`

3. **Root Directory - Minimal Files Only**
   - Only essential project files and configuration
   - `README.md`, `CHANGELOG.md`, configuration files
   - **NOT allowed:** Diagnostic reports, audit documents, temporary documentation

**Cleanup and Archival Rules:**

1. **90-Day Rule:** Reports older than 90 days should be moved to `reports/archive/`
2. **Version Consolidation:** Keep only the most recent comprehensive version of duplicate reports
3. **Completed Fixes:** Move documentation of completed fixes to `reports/archive/` after verification
4. **Quarterly Cleanup:** Review `reports/archive/` and delete files older than 1 year (unless marked as "KEEP")

**Naming Conventions:**
- Reports: `{category}-{description}-{YYYY-MM-DD}.md`
- Documentation: `{TITLE}.md` (PascalCase or UPPERCASE)
- Avoid: `*_LATEST.md`, `*_FULL.md`, `*_v2.md` (use dates instead)

**When Creating New Reports:**
- Create in appropriate `reports/` subfolder (not root)
- Use descriptive, date-based naming
- Reference this structure in report if needed

---

For complete documentation, see:
- **Developer Guide**: `docs/DEVELOPER_GUIDE.md`
- **WordPress Plugin Best Practices**: `docs/WORDPRESS_PLUGIN_BEST_PRACTICES.md`
- **API Reference**: `docs/API_REFERENCE.md`
- **Structural Rules (all deploy projects)**: `plugins/vibecode-deploy/docs/STRUCTURAL_RULES.md` — includes **prefix requirements**: CPTs, shortcodes, taxonomies, ACF group/field names, and (recommended) post meta keys must use the project prefix (e.g. `cfa_`, `bgp_`). Plugin validates these on upload.
