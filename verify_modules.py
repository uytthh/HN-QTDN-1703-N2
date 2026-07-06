#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Verification Script
Verifies that all modules are properly structured and ready for upgrade.
"""

import os
import sys
import xml.etree.ElementTree as ET
import ast

def print_status(icon, message):
    print(f"{icon} {message}")

def check_xml_validity(fpath):
    """Check if XML file is valid"""
    try:
        ET.parse(fpath)
        return True, None
    except Exception as e:
        return False, str(e)

def check_python_syntax(fpath):
    """Check if Python file has valid syntax"""
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        return True, None
    except SyntaxError as e:
        return False, str(e)

def verify_module(module_name):
    """Verify a single module"""
    print(f"\n{'='*50}")
    print(f"  Verifying: {module_name}")
    print(f"{'='*50}")
    
    module_path = f'addons/{module_name}'
    
    # Check module exists
    if not os.path.exists(module_path):
        print_status("✗", f"Module path not found: {module_path}")
        return False
    
    all_ok = True
    
    # Check manifest
    manifest_path = os.path.join(module_path, '__manifest__.py')
    if os.path.exists(manifest_path):
        ok, err = check_python_syntax(manifest_path)
        if ok:
            print_status("✓", "__manifest__.py is valid")
            with open(manifest_path, 'r', encoding='utf-8') as f:
                try:
                    manifest = ast.literal_eval(f.read())
                    print_status("✓", f"  Name: {manifest.get('name')}")
                    print_status("✓", f"  Version: {manifest.get('version')}")
                    if 'assets' in manifest:
                        print_status("✓", "  Assets defined: ✓")
                except:
                    pass
        else:
            print_status("✗", f"__manifest__.py syntax error: {err[:60]}")
            all_ok = False
    else:
        print_status("✗", "__manifest__.py not found")
        all_ok = False
    
    # Check XML files
    xml_count = 0
    xml_ok = 0
    for root, dirs, files in os.walk(module_path):
        for f in files:
            if f.endswith('.xml'):
                xml_count += 1
                fpath = os.path.join(root, f)
                ok, err = check_xml_validity(fpath)
                if ok:
                    xml_ok += 1
                else:
                    rel_path = os.path.relpath(fpath, module_path)
                    print_status("✗", f"Invalid XML: {rel_path}")
                    print(f"    Error: {err[:80]}")
                    all_ok = False
    
    if xml_count > 0:
        if xml_ok == xml_count:
            print_status("✓", f"All {xml_count} XML files are valid")
        else:
            print_status("✗", f"Only {xml_ok}/{xml_count} XML files are valid")
            all_ok = False
    
    # Check Python model files
    py_count = 0
    py_ok = 0
    models_path = os.path.join(module_path, 'models')
    if os.path.exists(models_path):
        for f in os.listdir(models_path):
            if f.endswith('.py'):
                py_count += 1
                fpath = os.path.join(models_path, f)
                ok, err = check_python_syntax(fpath)
                if ok:
                    py_ok += 1
                else:
                    print_status("✗", f"Invalid Python: models/{f}")
                    print(f"    Error: {err[:80]}")
                    all_ok = False
    
    if py_count > 0:
        if py_ok == py_count:
            print_status("✓", f"All {py_count} Python model files are valid")
        else:
            print_status("✗", f"Only {py_ok}/{py_count} Python files are valid")
            all_ok = False
    
    # Check CSS assets
    css_path = os.path.join(module_path, 'static/src/css/ui_enhancement.css')
    if os.path.exists(css_path):
        size = os.path.getsize(css_path)
        print_status("✓", f"CSS asset exists ({size} bytes)")
    else:
        print_status("✗", "CSS asset not found: static/src/css/ui_enhancement.css")
    
    return all_ok

def main():
    print("\n" + "="*60)
    print("  ODOO MODULE VERIFICATION TOOL")
    print("="*60)
    
    modules = ['cham_cong', 'nhan_su', 'tinh_luong']
    results = {}
    
    for module in modules:
        results[module] = verify_module(module)
    
    # Summary
    print(f"\n{'='*60}")
    print("  VERIFICATION SUMMARY")
    print(f"{'='*60}")
    
    all_ok = True
    for module, ok in results.items():
        icon = "✓" if ok else "✗"
        status = "Ready for upgrade" if ok else "Has issues"
        print_status(icon, f"{module}: {status}")
        if not ok:
            all_ok = False
    
    if all_ok:
        print_status("✓", "\nAll modules are ready for upgrade!")
        print("\nNext steps:")
        print("  1. Stop any running Odoo instances")
        print("  2. Run: python upgrade_modules_interactive.py")
        print("  3. Enter your database name")
        print("  4. Wait for the upgrade to complete")
        return 0
    else:
        print_status("✗", "\nSome modules have issues. Please fix them before upgrading.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
