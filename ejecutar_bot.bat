@echo off
setlocal EnableDelayedExpansion

title Bot de WhatsApp RPA - Automatizacion

echo ======================================================================
echo           BOT DE WHATSAPP RPA - EJECUTABLE WINDOWS (.BAT)
echo ======================================================================
echo.

:: Cambiar al directorio del script
cd /d "%~dp0"

:: 1. Buscar Python ejecutable
set PYTHON_EXE=

:: A) Verificar si existe .venv en el directorio actual
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
    set "PIP_EXE=%~dp0.venv\Scripts\pip.exe"
    goto :python_found
)

:: B) Verificar si existe .venv en el directorio superior
if exist "%~dp0..\.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0..\.venv\Scripts\python.exe"
    set "PIP_EXE=%~dp0..\.venv\Scripts\pip.exe"
    goto :python_found
)

:: C) Probar comando python en PATH
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('where python 2^>nul') do (
        if not defined PYTHON_EXE (
            set "PYTHON_EXE=%%i"
        )
    )
)

:: D) Probar comando py (Python Launcher)
if not defined PYTHON_EXE (
    py -3 --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set "PYTHON_EXE=py -3"
    )
)

:: E) Probar ubicaciones comunes conocidas
if not defined PYTHON_EXE (
    if exist "%USERPROFILE%\.pyenv\pyenv-win\shims\python.bat" (
        set "PYTHON_EXE=%USERPROFILE%\.pyenv\pyenv-win\shims\python.bat"
    ) else if exist "%USERPROFILE%\.pyenv\pyenv-win\shims\python.exe" (
        set "PYTHON_EXE=%USERPROFILE%\.pyenv\pyenv-win\shims\python.exe"
    ) else if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
        set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    ) else if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
        set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    ) else if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    ) else if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
        set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
    )
)

if not defined PYTHON_EXE (
    echo [ERROR] No se encontro Python en el sistema.
    echo Por favor instala Python 3.8 o superior y asegurate de marcar
    echo la opcion "Add Python to PATH" durante la instalacion.
    echo.
    pause
    exit /b 1
)

:: 2. Si no habia .venv, crearlo con el Python encontrado
if not exist "%~dp0.venv\Scripts\python.exe" if not exist "%~dp0..\.venv\Scripts\python.exe" (
    echo [INFO] Creando entorno virtual aislado (.venv)...
    %PYTHON_EXE% -m venv "%~dp0.venv"
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
    set "PIP_EXE=%~dp0.venv\Scripts\pip.exe"
)

:python_found
echo [INFO] Utilizando ejecutable: %PYTHON_EXE%

:: 3. Verificar dependencias en requirements.txt
if not defined PIP_EXE (
    if exist "%~dp0.venv\Scripts\pip.exe" (
        set "PIP_EXE=%~dp0.venv\Scripts\pip.exe"
    ) else if exist "%~dp0..\.venv\Scripts\pip.exe" (
        set "PIP_EXE=%~dp0..\.venv\Scripts\pip.exe"
    )
)

if defined PIP_EXE (
    echo [INFO] Verificando dependencias en el entorno virtual...
    if exist "%~dp0requirements.txt" (
        "%PIP_EXE%" install -q -r "%~dp0requirements.txt"
    ) else if exist "%~dp0..\requirements.txt" (
        "%PIP_EXE%" install -q -r "%~dp0..\requirements.txt"
    )
)

:: 4. Verificar instalacion de Chromium para Playwright
echo [INFO] Verificando navegador Chromium para Playwright...
"%PYTHON_EXE%" -m playwright install chromium

echo.
echo ======================================================================
echo                INICIANDO EJECUCION DEL BOT RPA
echo ======================================================================
echo.

:: 5. Ejecutar script principal
set RUN_FROM_BAT=1
set PYTHONIOENCODING=utf-8

if exist "%~dp0main.py" (
    "%PYTHON_EXE%" "%~dp0main.py" %*
) else if exist "%~dp0..\main.py" (
    "%PYTHON_EXE%" "%~dp0..\main.py" %*
) else (
    echo [ERROR] No se encontro main.py.
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo             EJECUCION FINALIZADA - BOT DE WHATSAPP RPA
echo ======================================================================
echo.
pause
