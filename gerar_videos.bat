@echo off
title TikTok Viral Bot - Gerador de Videos
cd /d "%~dp0"
echo ===================================================
echo   TIKTOK VIRAL BOT - GERADOR DE VIDEOS (EUA / EUROPA)
echo ===================================================
echo.
echo Quantos videos deseja gerar? (Exemplo: 1, 3, 5)
set /p count=Digite o numero e pressione Enter: 
if "%count%"=="" set count=1
python main.py --count %count%
echo.
echo ===================================================
echo   Concluido! Verifique os videos na pasta "output\"
echo ===================================================
pause
