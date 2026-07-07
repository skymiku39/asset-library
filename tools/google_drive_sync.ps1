# Bind assets/ to Google Drive for desktop sync.
# Usage:
#   .\tools\google_drive_sync.ps1 detect
#   .\tools\google_drive_sync.ps1 setup
#   .\tools\google_drive_sync.ps1 status
param(
    [Parameter(Position = 0)]
    [ValidateSet("detect", "setup", "status")]
    [string]$Action = "status"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path $PSScriptRoot -Parent
$LocalAssets = Join-Path $ProjectRoot "assets"
$ConfigPath = Join-Path $ProjectRoot "config\google_drive.json"
$ExampleConfig = Join-Path $ProjectRoot "config\google_drive.example.json"

function Get-GoogleDriveCandidates {
    $candidates = [System.Collections.Generic.List[string]]::new()

    foreach ($path in @(
            "G:\My Drive",
            "G:\",
            "$env:USERPROFILE\Google Drive",
            "$env:USERPROFILE\My Drive"
        )) {
        if (Test-Path $path) { $candidates.Add($path) }
    }

    $cloudRoot = Join-Path $env:USERPROFILE "Library\CloudStorage"
    if (Test-Path $cloudRoot) {
        Get-ChildItem $cloudRoot -Directory -Filter "GoogleDrive-*" -ErrorAction SilentlyContinue | ForEach-Object {
            foreach ($name in @("My Drive", "我的雲端硬碟")) {
                $drivePath = Join-Path $_.FullName $name
                if (Test-Path $drivePath) { $candidates.Add($drivePath) }
            }
        }
    }

    return $candidates | Select-Object -Unique
}

function Read-SyncConfig {
    if (-not (Test-Path $ConfigPath)) {
        $msg = "Missing config: $ConfigPath"
        throw $msg
    }
    return Get-Content $ConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json
}

function Get-CloudAssetsPath {
    $cfg = Read-SyncConfig
    $root = [string]$cfg.google_drive_root
    $remote = [string]$cfg.remote_assets_dir
    if (-not (Test-Path $root)) {
        throw "Google Drive root not found: $root"
    }
    return Join-Path $root $remote
}

function Test-Junction([string]$Path) {
    if (-not (Test-Path $Path)) { return $false }
    $item = Get-Item $Path -Force
    return (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)
}

function Get-JunctionTarget([string]$Path) {
    $raw = cmd /c "fsutil reparsepoint query `"$Path`""
    foreach ($line in $raw) {
        if ($line -match "Print Name:\s+(.+)") { return $matches[1].Trim() }
    }
    return $null
}

function Show-Detect {
    $found = @(Get-GoogleDriveCandidates)
    if ($found.Count -eq 0) {
        Write-Host "Google Drive local path not found."
        Write-Host "Install Google Drive for desktop: https://www.google.com/drive/download/"
        Write-Host "Then run: .\tools\google_drive_sync.ps1 detect"
        return
    }
    Write-Host "Detected Google Drive paths:"
    $i = 1
    foreach ($p in $found) {
        Write-Host "  [$i] $p"
        $i++
    }
    Write-Host ""
    Write-Host "Copy config\google_drive.example.json to config\google_drive.json"
    Write-Host "Set google_drive_root to one of the paths above."
}

function Show-Status {
    Write-Host "Project: $ProjectRoot"
    if (-not (Test-Path $LocalAssets)) {
        Write-Host "assets/: missing"
        return
    }
    if (Test-Junction $LocalAssets) {
        $target = Get-JunctionTarget $LocalAssets
        Write-Host "assets/: junction"
        Write-Host "  -> $target"
        if (Test-Path $target) {
            $files = (Get-ChildItem $target -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
            $bytes = (Get-ChildItem $target -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
            $gb = if ($bytes) { [math]::Round($bytes / 1GB, 2) } else { 0 }
            Write-Host "  files: $files, size: $gb GB"
        }
    }
    else {
        Write-Host "assets/: local folder (not linked to Google Drive)"
        $files = (Get-ChildItem $LocalAssets -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
        $bytes = (Get-ChildItem $LocalAssets -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        $gb = if ($bytes) { [math]::Round($bytes / 1GB, 2) } else { 0 }
        Write-Host "  files: $files, size: $gb GB"
    }
}

function Invoke-Setup {
    $cloudAssets = Get-CloudAssetsPath
    Write-Host "Cloud target: $cloudAssets"

    if (Test-Junction $LocalAssets) {
        $current = Get-JunctionTarget $LocalAssets
        if ($current -eq $cloudAssets) {
            Write-Host "Already linked. Nothing to do."
            return
        }
        throw "assets/ already linked to: $current"
    }

    New-Item -ItemType Directory -Path $cloudAssets -Force | Out-Null

    if (Test-Path $LocalAssets) {
        $hasContent = (Get-ChildItem $LocalAssets -Force -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0
        if ($hasContent) {
            Write-Host "Moving local assets/ to cloud (may take several minutes)..."
            robocopy $LocalAssets $cloudAssets /E /MOVE /R:2 /W:2 /NFL /NDL /NP | Out-Null
            if ($LASTEXITCODE -ge 8) { throw "robocopy failed, exit=$LASTEXITCODE" }
            Remove-Item $LocalAssets -Recurse -Force -ErrorAction SilentlyContinue
        }
        else {
            Remove-Item $LocalAssets -Force
        }
    }

    cmd /c "mklink /J `"$LocalAssets`" `"$cloudAssets`""
    if (-not (Test-Junction $LocalAssets)) { throw "Failed to create junction." }

    Write-Host ""
    Write-Host "Done. assets/ is now linked to Google Drive."
    Write-Host "  local path: $LocalAssets"
    Write-Host "  cloud path: $cloudAssets"
    Write-Host ""
    Write-Host "Download tools still write to assets/. Google Drive desktop app will sync."
}

switch ($Action) {
    "detect" { Show-Detect }
    "status" { Show-Status }
    "setup"  { Invoke-Setup }
}
