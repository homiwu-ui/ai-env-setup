@echo off
chcp 65001 >nul
title 小婷語音助理 — 一鍵安裝懶人包
echo ========================================
echo   小婷語音助理 — 一鍵安裝懶人包
echo ========================================
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"
echo.
echo 按任意鍵離開...
pause >nul
