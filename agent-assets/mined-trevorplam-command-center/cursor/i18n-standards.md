---
description: Run Internationalization (i18n) Standards Check
globs: ["src/components/**/*.tsx", "src/app/**/*.tsx", "src/lib/i18n/**/*.ts"]
---
# Frontend: Internationalization (i18n) Standards

<audit_rules>
- You MUST ensure all user-facing text is wrapped in translation functions (e.g., `t('key')` from `next-intl` or `i18next`) and NOT hardcoded as strings in components.
- You MUST verify that dates, times, and numbers use locale-aware formatting (e.g., `Intl.DateTimeFormat`, `Intl.NumberFormat`) and are NOT hardcoded to a specific locale.
- You MUST ensure currency values use proper locale formatting and include the correct currency symbol/position (e.g., `$1,000.00` vs `1.000,00 €`).
- You MUST verify that images or icons with text content are not hardcoded; they should support multiple languages or use locale-specific assets.
- You MUST enforce that URL slugs and paths are not hardcoded with language-specific text; use translation keys for dynamic routing.
</audit_rules>

<example_good>
```tsx
import { useTranslations } from 'next-intl';
import { format } from 'date-fns';
import { es, enUS } from 'date-fns/locale';

export function UserProfile({ user }: { user: User }) {
  const t = useTranslations('user');
  const locale = useLocale();
  
  return (
    <div>
      <h1>{t('profile.title')}</h1>
      <p>{t('profile.memberSince', { date: format(user.createdAt, 'PPP', { locale: locale === 'es' ? es : enUS }) })}</p>
      <p>{t('profile.balance', { amount: new Intl.NumberFormat(locale, { style: 'currency', currency: 'USD' }).format(user.balance) })}</p>
    </div>
  );
}
```
</example_good>

<example_bad>
```tsx
// BAD: Hardcoded strings
export function UserProfile({ user }: { user: User }) {
  return (
    <div>
      <h1>User Profile</h1>
      <p>Member since: {user.createdAt.toLocaleDateString('en-US')}</p>
      <p>Balance: ${user.balance.toFixed(2)}</p>
    </div>
  );
}
```
</example_bad>

