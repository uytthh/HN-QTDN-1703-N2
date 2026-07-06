import os

def check_xml_structure(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the position of </data> and </odoo>
    data_close = content.rfind('</data>')
    odoo_close = content.rfind('</odoo>')
    
    if data_close != -1 and odoo_close != -1:
        between = content[data_close+7:odoo_close].strip()
        if between:
            return f"Extra content: {between[:50]}"
        else:
            return "OK"
    elif '<?xml' in content and '<odoo>' in content:
        # Check if multiple <odoo> tags or <data> tags
        odoo_count = content.count('<odoo>')
        data_count = content.count('<data>')
        if odoo_count > 1:
            return f"ERROR: {odoo_count} <odoo> tags"
        if data_count > 1:
            return f"ERROR: {data_count} <data> tags"
        return "OK"
    else:
        return "ERROR: Invalid XML"

for module in ['cham_cong', 'nhan_su', 'tinh_luong']:
    views_path = rf'd:\Hội Nhập\CNTT-17-03-N2\addons\{module}\views'
    print(f'\n=== {module} ===')
    for f in sorted(os.listdir(views_path)):
        if f.endswith('.xml'):
            result = check_xml_structure(os.path.join(views_path, f))
            status = '✓' if result == 'OK' else '✗'
            print(f'{status} {f}: {result}')
