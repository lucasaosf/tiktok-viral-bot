@echo off
title TikTok Live 24/7 - Roblox Streamer
cd /d "%~dp0"
echo ===================================================
echo   TIKTOK LIVE 24/7 - TRANSMISSOR ROBLOX STREAMER
echo ===================================================
echo [1] Iniciar Transmissao 24/7 (ao vivo no TikTok)
echo [2] Fazer Teste Local de 5s (valida codificacao e audio)
echo ===================================================
set /p opt="Escolha uma opcao (1 ou 2) [padrao: 1]: "
if "%opt%"=="2" (
    python live_streamer.py --test
) else (
    python live_streamer.py
)
pause
