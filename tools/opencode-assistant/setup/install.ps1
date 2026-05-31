param(
    [switch]$NoElevate
)

$ErrorActionPreference = "Stop"

# --- Auto-elevate to Admin ---
if (-not ([Security.Principal.WindowsIdentity]::GetCurrent().Groups -contains [Security.Principal.WellKnownSidType]::BuiltinAdministratorsSid)) {
    if (-not $NoElevate) {
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = "powershell.exe"
        $psi.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`" -NoElevate"
        $psi.Verb = "RunAs"
        $proc = [System.Diagnostics.Process]::Start($psi)
        Write-Host "請在 UAC 彈窗中按「是」以管理員權限執行安裝..."
        $proc.WaitForExit()
        exit $proc.ExitCode
    }
}

$ROOT = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$TMP = Join-Path $env:TEMP "xiaoting-setup"
New-Item -ItemType Directory -Path $TMP -Force | Out-Null

$NVSA_URL = "https://github.com/gexgd0419/NaturalVoiceSAPIAdapter/releases/download/v0.2.9/NaturalVoiceSAPIAdapter_v0.2.9_x86_x64.zip"
$NVSA_ZIP = Join-Path $TMP "NaturalVoiceSAPIAdapter_v0.2.9_x86_x64.zip"
$NVSA_DIR = Join-Path $TMP "NaturalVoiceSAPIAdapter"

$VOICE_URL = "https://www.cross-plus-a.com/msspeech/ms_natural_voice_zh_tw.zip"
$VOICE_ZIP = Join-Path $TMP "ms_natural_voice_zh_tw.zip"
$VOICE_DIR = Join-Path $TMP "zh-tw-installer"
$VOICE_SETUP = Join-Path $VOICE_DIR "setup.exe"

function Write-Step {
    param([string]$Msg)
    Write-Host "`n>>> $Msg" -ForegroundColor Cyan
}

function Write-OK {
    Write-Host "  [OK]" -ForegroundColor Green
}

function Write-Skip {
    param([string]$Reason)
    Write-Host "  [略過] $Reason" -ForegroundColor Yellow
}

Write-Host "========================================" -ForegroundColor Magenta
Write-Host "  小婷語音助理 — 一鍵安裝懶人包" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host "專案目錄: $ROOT`n"

# ── Step 1: Download NaturalVoiceSAPIAdapter ──
Write-Step "Step 1/4 — 下載 NaturalVoiceSAPIAdapter v0.2.9"
if (Test-Path $NVSA_ZIP) {
    Write-Skip "已存在 ($((Get-Item $NVSA_ZIP).Length / 1MB -as [int]) MB)"
} else {
    Write-Host "  下載中 (22 MB)..."
    $null = Invoke-WebRequest -Uri $NVSA_URL -OutFile $NVSA_ZIP -UseBasicParsing
    Write-OK
}
if (-not (Test-Path $NVSA_DIR\Installer.exe)) {
    Expand-Archive -LiteralPath $NVSA_ZIP -DestinationPath $NVSA_DIR -Force
    Write-Host "  解壓縮完成" -ForegroundColor Gray
}

# ── Step 2: Download zh-TW voice pack ──
Write-Step "Step 2/4 — 下載臺灣中文神經語音包 (HsiaoChen/YunJhe)"
if (Test-Path $VOICE_SETUP) {
    Write-Skip "已存在 ($((Get-Item $VOICE_SETUP).Length / 1MB -as [int]) MB)"
} else {
    Write-Host "  下載中 (36 MB)..."
    $null = Invoke-WebRequest -Uri $VOICE_URL -OutFile $VOICE_ZIP -UseBasicParsing
    Expand-Archive -LiteralPath $VOICE_ZIP -DestinationPath $VOICE_DIR -Force
    Write-OK
}

# ── Step 3: Install NaturalVoiceSAPIAdapter ──
Write-Step "Step 3/4 — 安裝 NaturalVoiceSAPIAdapter (SAPI5 橋接引擎)"
$installer = Join-Path $NVSA_DIR "Installer.exe"
if (-not (Test-Path $installer)) {
    Write-Host "  [錯誤] 找不到 Installer.exe" -ForegroundColor Red
    exit 1
}

# 檢查是否已安裝
$installed = $false
try {
    Add-Type -AssemblyName System.Speech
    $speech = New-Object System.Speech.Synthesis.SpeechSynthesizer
    foreach ($v in $speech.GetVoices()) {
        if ($v.VoiceInfo.Name -like "*HsiaoChen*") { $installed = $true; break }
    }
} catch {}

if ($installed) {
    Write-Skip "HsiaoChen Native 語音已註冊，跳過安裝"
} else {
    Write-Host "  註冊 SAPI5 引擎 (32-bit + 64-bit)..."
    # Register via regsvr32 for both architectures
    $x86_dll = Join-Path $NVSA_DIR "x86\NaturalVoiceSAPIAdapter.dll"
    $x64_dll = Join-Path $NVSA_DIR "x64\NaturalVoiceSAPIAdapter.dll"

    if (Test-Path $x86_dll) {
        $null = Start-Process regsvr32 -ArgumentList "/s `"$x86_dll`"" -Wait -NoNewWindow
        Write-Host "    32-bit: 已註冊" -ForegroundColor Gray
    }
    if (Test-Path $x64_dll) {
        $null = Start-Process regsvr32 -ArgumentList "/s `"$x64_dll`"" -Wait -NoNewWindow
        Write-Host "    64-bit: 已註冊" -ForegroundColor Gray
    }

    # Set registry config
    $reg = "HKLM:\SOFTWARE\gexgd0419\NaturalVoiceSAPIAdapter"
    if (-not (Test-Path $reg)) { New-Item -Path $reg -Force | Out-Null }
    Set-ItemProperty -Path $reg -Name "EnableEdgeOnlineVoices" -Value 1 -Force
    Set-ItemProperty -Path $reg -Name "EnableNarratorNaturalVoices" -Value 1 -Force
    Write-OK
}

# ── Step 4: Install zh-TW voice ──
Write-Step "Step 4/4 — 安裝 Microsoft HsiaoChen Native 語音"
if (Test-Path $VOICE_SETUP) {
    $already = $false
    try {
        $speech2 = New-Object System.Speech.Synthesis.SpeechSynthesizer
        foreach ($v in $speech2.GetVoices()) {
            if ($v.VoiceInfo.Name -like "*HsiaoChen Native*") { $already = $true; break }
        }
    } catch {}

    if ($already) {
        Write-Skip "HsiaoChen Native 已安裝"
    } else {
        Write-Host "  執行語音包安裝程式..."
        Write-Host "  (UAC 彈窗請按「是」)"
        $p = Start-Process -FilePath $VOICE_SETUP -Verb RunAs -Wait -PassThru
        if ($p.ExitCode -eq 0) { Write-OK }
        else { Write-Host "  [警告] 安裝程式離開代碼: $($p.ExitCode)" -ForegroundColor Yellow }
    }
} else {
    Write-Host "  [錯誤] 找不到 setup.exe" -ForegroundColor Red
    exit 1
}

# ── Verify ──
Write-Step "✓ 驗證安裝結果"
Start-Sleep -Seconds 2
try {
    $speech3 = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $voices = @()
    foreach ($v in $speech3.GetVoices()) {
        $name = $v.VoiceInfo.Name
        $cult = $v.VoiceInfo.Culture.Name
        if ($name -like "*HsiaoChen*" -or $name -like "*Hanhan*" -or $name -like "*YunJhe*") {
            $voices += "$name ($cult)"
        }
    }
    if ($voices.Count -eq 0) {
        Write-Host "  [⚠] 可用中文語音列表:" -ForegroundColor Yellow
        foreach ($v in $speech3.GetVoices()) {
            Write-Host "      $($v.VoiceInfo.Name)" -ForegroundColor Gray
        }
    } else {
        Write-Host "  已註冊的中文語音:" -ForegroundColor Green
        foreach ($v in $voices) { Write-Host "    ✅ $v" }
    }
} catch {
    Write-Host "  無法讀取語音列表: $_" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Magenta
Write-Host "  安裝完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "快速測試語音:" -ForegroundColor Cyan
Write-Host '  & "C:\Users\88690\AppData\Local\Python\pythoncore-3.14-64\python.exe" "' -NoNewline
Write-Host "$ROOT\tools\opencode-assistant\speak_msg.py" -ForegroundColor Yellow -NoNewline
Write-Host '" --raw "你好，世界！"'
Write-Host ""
Write-Host "啟動小婷主程式:" -ForegroundColor Cyan
Write-Host "  & " -NoNewline; Write-Host '"小婷go.ps1"' -ForegroundColor Yellow

pause
