import os
import re

def analyze_odoo_structure(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    structure = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if '<odoo' in stripped:
            structure.append(f"Line {i}: {stripped[:60]}")
        elif '</odoo>' in stripped:
            structure.append(f"Line {i}: {stripped[:60]}")
        elif '<data' in stripped:
            structure.append(f"Line {i}: {stripped[:60]}")
        elif '</data>' in stripped:
            structure.append(f"Line {i}: {stripped[:60]}")
        elif stripped and not stripped.startswith('<!--') and not stripped.startswith('<?'):
            # Check if there's non-whitespace content between </data> and </odoo>
            if i > 3:  # After header
                if '<?xml' not in stripped and '<odoo' not in stripped and '</odoo>' not in stripped:
                    if '<' in stripped and '>' in stripped:
                        if '<data' not in stripped and '</data>' not in stripped:
                            structure.append(f"Line {i}: POSSIBLE EXTRA CONTENT: {stripped[:50]}")
    
    return structure

for module in ['cham_cong', 'nhan_su', 'tinh_luong']:
    views_path = f'd:\\Hội Nhập\\CNTT-17-03-N2\\addons\\{module}\\views'
    print(f'\n=== {module} ===')
    for f in ['menu.xml', 'bang_cham_cong.xml'][:1] if module == 'cham_cong' else ['menu.xml']:
        if module == 'cham_cong' and f == 'bang_cham_cong.xml':
            continue
        fpath = os.path.join(views_path, f)
        if os.path.exists(fpath):
            structure = analyze_odoo_structure(fpath)
            print(f'\n{f}:')
            for item in structure:
                print(f'  {item}')
