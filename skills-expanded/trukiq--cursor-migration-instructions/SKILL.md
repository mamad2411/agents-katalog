# 🗄️ Database Migration Instructions

**Status:** ✅ Production secrets set  
**Next Step:** Run database migrations

---

## Quick Migration (2 minutes)

### Option 1: Browser Console (Recommended)

1. **Visit the app:** https://trukiq.fly.dev
2. **Sign in** to your account
3. **Open browser console:**
   - Chrome/Edge: Press `F12` or `Ctrl+Shift+J` (Windows) / `Cmd+Option+J` (Mac)
   - Firefox: Press `F12` or `Ctrl+Shift+K` (Windows) / `Cmd+Option+K` (Mac)
   - Safari: Press `Cmd+Option+C` (enable Developer menu first)
4. **Go to Console tab**
5. **Copy and paste this code:**

```javascript
(async function runMigration() {
  console.log('🚀 Starting TrukIQ Database Migration...');
  try {
    const response = await fetch('/api/ai/migrations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include'
    });
    const data = await response.json();
    console.log('✅ Migration Result:', data);
    if (data.success) {
      console.log('📊 Tables created:', data.results?.tables_created?.length || 0);
      data.results?.tables_created?.forEach((table, i) => {
        console.log(`   ${i + 1}. ${table}`);
      });
      console.log('✅ Migration completed successfully!');
    } else {
      console.error('❌ Migration failed:', data.error);
    }
  } catch (error) {
    console.error('❌ Error:', error);
  }
})();
```

6. **Press Enter**
7. **Check the console output** - you should see:
   - ✅ Migration completed successfully!
   - List of tables created

---

### Option 2: Migration HTML Page

1. **Visit:** https://trukiq.fly.dev/run-migration.html
2. **Click "Run Migration" button**
3. **Check the response message**

---

## Expected Results

After successful migration, you should see these tables created:

- ✅ `load_analyses` - Stores load profitability predictions
- ✅ `trip_completions` - Stores completed trip data
- ✅ `driver_models` - Stores personalized driver models
- ✅ `network_corridor_stats` - Stores network intelligence
- ✅ `network_trip_pool` - Stores anonymized trip data
- ✅ `model_metrics` - Stores model performance metrics
- ✅ `feature_flags` - Stores feature flag configuration
- ✅ `user_profit_summary` - Materialized view for profit summaries

---

## Troubleshooting

### Error: "Authentication required"
- **Solution:** Make sure you're signed in to the app first

### Error: "Migration already complete"
- **Status:** ✅ This is good! Migration was already run
- **Action:** No action needed, proceed to testing

### Error: "Database connection failed"
- **Solution:** Check that `DATABASE_URL` secret is set correctly in Fly.io
- **Verify:** `flyctl secrets list --app trukiq`

### Error: Network error or timeout
- **Solution:** 
  1. Check app is accessible: https://trukiq.fly.dev
  2. Check Fly.io logs: `flyctl logs --app trukiq`
  3. Try again in a few minutes

---

## Verify Migration Success

After migration, you can verify by checking the console output or running:

```javascript
// Check migration status
fetch('/api/ai/migrations')
  .then(r => r.json())
  .then(data => {
    console.log('Migration Status:', data);
    if (data.migration_complete) {
      console.log('✅ Migration complete!');
      console.log('Tables:', data.tables || 'N/A');
    }
  });
```

---

## Next Steps

After migration completes:

1. ✅ **Test Critical Flows** (see `.cursor/scripts/test-production-flows.md`)
   - Sign up
   - Sign in
   - Dashboard
   - AI Feed
   - Fleet management

2. ✅ **Verify App Functionality**
   - Check all pages load
   - Test core features
   - Verify no console errors

3. ✅ **Launch!** 🚀
   - App is already live
   - Monitor first users
   - Collect feedback

---

**Ready?** Visit https://trukiq.fly.dev, sign in, and run the migration code above!

