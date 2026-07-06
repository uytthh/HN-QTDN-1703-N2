#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nâng cấp Odoo Modules - Cham Cong, Nhan Su, Tinh Luong
Cải thiện giao diện với CSS enhancement
"""

import subprocess
import sys
import time
from pathlib import Path

def main():
    # Cấu hình
    odoo_path = Path("d:/Hội Nhập/CNTT-17-03-N2")
    odoo_bin = odoo_path / "odoo-bin.py"
    odoo_conf = odoo_path / "odoo.conf"
    
    modules_to_upgrade = ["cham_cong", "nhan_su", "tinh_luong"]
    
    # Hỏi database name
    print("=" * 60)
    print("🔄 Nâng cấp Odoo Modules - UI Enhancement")
    print("=" * 60)
    print()
    
    db_name = input("Nhập tên cơ sở dữ liệu Odoo: ").strip()
    if not db_name:
        print("❌ Lỗi: Tên cơ sở dữ liệu không được để trống!")
        sys.exit(1)
    
    print()
    print(f"📦 Database: {db_name}")
    print(f"🔧 Modules: {', '.join(modules_to_upgrade)}")
    print()
    
    # Xây dựng lệnh
    update_modules = ",".join(modules_to_upgrade)
    
    cmd = [
        sys.executable,
        str(odoo_bin),
        "-c", str(odoo_conf),
        "-d", db_name,
        "-u", update_modules,
        "--stop-after-init",
        "-l", "info"
    ]
    
    print("📝 Lệnh sẽ chạy:")
    print(" ".join(cmd))
    print()
    print("🚀 Bắt đầu nâng cấp...")
    print("-" * 60)
    print()
    
    try:
        # Chạy nâng cấp
        result = subprocess.run(cmd, cwd=str(odoo_path))
        
        print()
        print("-" * 60)
        if result.returncode == 0:
            print()
            print("✅ Nâng cấp thành công!")
            print()
            print("📋 Tính năng mới:")
            print("   ✓ Menu icons đẹp")
            print("   ✓ Gradient backgrounds")
            print("   ✓ Smooth animations")
            print("   ✓ Better color scheme")
            print("   ✓ Enhanced cards styling")
            print("   ✓ Improved buttons")
            print()
            print("🌐 Truy cập: http://localhost:8069")
            print()
        else:
            print()
            print("❌ Nâng cấp thất bại!")
            print(f"Exit code: {result.returncode}")
            sys.exit(1)
            
    except Exception as e:
        print()
        print(f"❌ Lỗi: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
