#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Upgrade Script for Odoo 14
Upgrades: cham_cong, nhan_su, tinh_luong

This script attempts to upgrade the three custom modules with proper error handling and diagnostics.
"""

import os
import sys
import subprocess
import time

def print_header(text):
    """Print section header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_success(text):
    """Print success message"""
    print(f"✓ {text}")

def print_error(text):
    """Print error message"""
    print(f"✗ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ {text}")

def run_command(cmd, description):
    """Run a command and return success status"""
    print_info(f"Running: {description}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print_success(description)
            return True
        else:
            print_error(f"{description} - Return code: {result.returncode}")
            if result.stderr:
                print(f"Error output:\n{result.stderr[:500]}")
            return False
    except subprocess.TimeoutExpired:
        print_error(f"{description} - Timeout (5 minutes exceeded)")
        return False
    except Exception as e:
        print_error(f"{description} - Exception: {str(e)}")
        return False

def main():
    print_header("Odoo Module Upgrade Tool")
    
    # Get database name from user
    db_name = input("\nEnter database name (e.g., odoo14_dev): ").strip()
    if not db_name:
        print_error("Database name is required")
        return 1
    
    # Get Odoo configuration path
    project_root = os.path.dirname(os.path.abspath(__file__))
    odoo_conf = os.path.join(project_root, "odoo.conf")
    odoo_bin = os.path.join(project_root, "odoo-bin")
    
    if not os.path.exists(odoo_conf):
        print_error(f"odoo.conf not found at {odoo_conf}")
        return 1
    
    if not os.path.exists(odoo_bin):
        print_error(f"odoo-bin not found at {odoo_bin}")
        return 1
    
    print_success(f"Found Odoo configuration")
    print_info(f"Configuration: {odoo_conf}")
    print_info(f"Odoo binary: {odoo_bin}")
    
    # Build upgrade command
    modules = "cham_cong,nhan_su,tinh_luong"
    cmd = [
        sys.executable,
        odoo_bin,
        "-c", odoo_conf,
        "-d", db_name,
        "-u", modules,
        "--stop-after-init"
    ]
    
    print_info(f"Upgrading modules: {modules}")
    print_info(f"Database: {db_name}")
    
    # Run upgrade
    print_header("Starting Module Upgrade")
    success = run_command(cmd, f"Upgrade modules {modules}")
    
    if success:
        print_header("✓ Module Upgrade Successful!")
        print_info("Your modules have been upgraded successfully.")
        print_info("New features include:")
        print_info("  • Enhanced UI with gradient colors and smooth animations")
        print_info("  • Improved menu icons and visual hierarchy")
        print_info("  • Better responsive design")
        return 0
    else:
        print_header("✗ Module Upgrade Failed")
        print_error("The module upgrade encountered an error.")
        print_info("\nTroubleshooting steps:")
        print_info("1. Ensure Odoo is not running on the database")
        print_info("2. Check that PostgreSQL is running (port 5431)")
        print_info("3. Verify database credentials in odoo.conf")
        print_info("4. Try running with --log-level=debug for more details")
        print_info("\nDebug command:")
        print_info(" ".join(cmd + ["--log-level=debug"]))
        return 1

if __name__ == "__main__":
    sys.exit(main())
