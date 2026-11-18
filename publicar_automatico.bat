@echo off
title TikTok Bot - Publicar Video Automatico
cd /d "%~dp0"
echo ===================================================
echo   TIKTOK BOT - PUBLICAR VIDEO AUTOMATICO (STEALTH)
echo ===================================================
echo.
echo [1] Publicar o video mais recente automaticamente
echo [2] Abrir modo revisao (preenche o video e legenda para voce conferir)
echo ===================================================
set /p opt="Escolha uma opcao (1 ou 2) [padrao: 1]: "

if "%opt%"=="2" (
    python tiktok_uploader_stealth.py --no-auto-post
) else (
    python tiktok_uploader_stealth.py
)
echo.
pause
