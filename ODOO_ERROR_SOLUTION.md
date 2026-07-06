# Odoo RPC_ERROR: KeyError 'bang_cham_cong' - Solution Guide

## Problem Description
```
KeyError: 'bang_cham_cong'
```
This error occurs when trying to access the "Bảng chấm công" action in Odoo. The model `bang_cham_cong` is not found in the Odoo registry.

## Root Cause
The module has not been **updated/reloaded** in the Odoo database after code modifications. Odoo needs to:
1. Register all models from the module
2. Process all XML records (views, actions, menus)
3. Update the database schema

## Issues Fixed in Code

### 1. Search View Filter Expressions (FIXED ✅)
**Problem**: The search view contained invalid Python expressions that aren't available in Odoo's search context:
```xml
<!-- BEFORE - Invalid expressions -->
<filter domain="[('ngay_cham_cong','&gt;=', (context_today() - datetime.timedelta(days=context_today().weekday())).strftime('%%Y-%%m-%%d'))]"/>
```

**Solution**: Removed invalid Python method calls and kept only basic filters that work with Odoo domain syntax.

## How to Fix the Error

### Option 1: Update Module via Odoo UI (Recommended)
1. Go to **Apps** menu
2. Search for **"Chấm công"** (or "cham_cong")
3. Click on the module
4. Click the **"Upgrade"** button
5. Wait for the upgrade to complete
6. Go to **Chấm công → Bảng chấm công** to verify it works

### Option 2: Update via Terminal
**Windows PowerShell:**
```powershell
cd d:\Hội Nhập\CNTT-17-03-N2
# Stop Odoo first if running
# Then restart with -u flag:
python odoo-bin -c odoo.conf -d <your_database_name> -u "cham_cong 1"
```

**Replace `<your_database_name>` with your actual database name**

### Option 3: Development Mode (for Active Development)
1. Stop the current Odoo process
2. Restart with development flag:
```
python odoo-bin -c odoo.conf --dev=reload -d <your_database_name>
```

This mode automatically reloads modules when files change.

### Option 4: Manual Database Cleanup (Last Resort)
If upgrades keep failing, try clearing the module state:
1. Go to **Settings → Technical → Modules**
2. Search for "Chấm công"
3. Click the module
4. Click **"Mark as uninstalled"** (if you want to start fresh)
5. Or directly click **"Upgrade"** if already installed

## Verification Steps

After applying one of the above solutions:

1. **Refresh the Page**: Press `F5` or `Ctrl+R` in the browser
2. **Navigate to Module**: Go to **Chấm công → Bảng chấm công**
3. **Expected Result**: The list should load without errors
4. **Try Creating**: Click "Create" to ensure the form loads correctly

## If Error Persists

### Debug Checklist:
1. ✅ **Module files are syntactically correct** - All Python files validated
2. ✅ **Model imports are correct** - All models properly imported
3. ✅ **Dependencies exist** - `nhan_su` module is present
4. ⚠️ **Database might need restart** - Try restarting Odoo completely

### Additional Debug:
Check the Odoo server log for more detailed error messages:
```
# Look for lines containing 'cham_cong'
# Check for Python import errors or model registration failures
```

## Code Quality Improvements Made
- ✅ Removed invalid Python expressions from search filters
- ✅ Verified all model imports and definitions
- ✅ Confirmed all related models exist (`nhan_vien`, `don_tu`, etc.)
- ✅ Validated all XML view definitions

## Related Documentation
- **Odoo Model Names**: Use lowercase with underscores (e.g., `bang_cham_cong`)
- **Module Update**: Required whenever XML records or Python models change
- **Search View Domains**: Must use Odoo domain syntax, not Python expressions

## Support
If the issue persists after these steps:
1. Check the module dependency `nhan_su` is installed
2. Verify database integrity: `SELECT * FROM ir_model WHERE model LIKE '%bang_cham_cong%'`
3. Check Odoo server logs for Python import errors
