@echo off
chcp 65001 >nul
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [错误] 未找到虚拟环境 .venv，请先执行: poetry install
    pause
    exit /b 1
)

set PYTHONPATH=%~dp0
.venv\Scripts\python.exe app\main.py

pause
