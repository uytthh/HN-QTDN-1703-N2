# Script nâng cấp các module Odoo
# Sử dụng: ./upgrade_modules.ps1 -DatabaseName "tên_db"

param(
    [Parameter(Mandatory = $true)]
    [string]$DatabaseName
)

$odooPath = "d:\Hội Nhập\CNTT-17-03-N2"
$odooBin = "$odooPath\odoo-bin"
$odooConf = "$odooPath\odoo.conf"

# Các module cần nâng cấp
$modules = @("cham_cong", "nhan_su", "tinh_luong")

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Nâng cấp các module Odoo" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Database: $DatabaseName" -ForegroundColor Yellow
Write-Host "Modules: $($modules -join ', ')" -ForegroundColor Yellow
Write-Host ""

# Dừng Odoo nếu đang chạy
Write-Host "Dừng Odoo..." -ForegroundColor Yellow
$odooProcess = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -match "Odoo" }
if ($odooProcess) {
    Stop-Process -Id $odooProcess.Id -Force
    Start-Sleep -Seconds 3
}

# Nâng cấp từng module
foreach ($module in $modules) {
    Write-Host ""
    Write-Host "Nâng cấp module: $module" -ForegroundColor Cyan
    Write-Host "---" -ForegroundColor Gray
    
    $updateModules = $modules | ForEach-Object { $_ } | Select-Object -First ($modules.IndexOf($module) + 1)
    $updateString = ($updateModules -join ",")
    
    & python $odooBin -c $odooConf -d $DatabaseName -u $updateString --stop-after-init
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Nâng cấp $module thành công" -ForegroundColor Green
    }
    else {
        Write-Host "✗ Nâng cấp $module thất bại" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Hoàn thành!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Để khởi động Odoo bình thường, chạy:" -ForegroundColor Yellow
Write-Host "python odoo-bin -c odoo.conf -d $DatabaseName" -ForegroundColor White
