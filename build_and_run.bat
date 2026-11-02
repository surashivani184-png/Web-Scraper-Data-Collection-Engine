@echo off
title Computing Aptitude Mini Project - Web Scraper
cls

echo =====================================================================
echo    COMPUTING APTITUDE MINI PROJECT: WEB SCRAPER FOR DATA COLLECTION
echo          Architecture: C++ Core  ^|  Design: CSS Glassmorphism
echo =====================================================================
echo.

cd /d "%~dp0"

:: 1. Check for g++
where g++ >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo [+] Detected MinGW/GCC C++ Compiler.
    echo [*] Compiling src/scraper.cpp...
    g++ -O2 -std=c++17 src/scraper.cpp -o scraper.exe -lws2_32 -lwininet
    if %ERRORLEVEL% equ 0 (
        echo [+] Compilation Successful! Generated scraper.exe
        echo [*] Launching C++ Embedded Web Server and Opening Browser...
        start http://127.0.0.1:8080
        scraper.exe --serve 8080
        goto :eof
    )
)

:: 2. Check for MSVC cl.exe
where cl >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo [+] Detected MSVC C++ Compiler.
    echo [*] Compiling src/scraper.cpp...
    cl /O2 /EHsc /std:c++17 src\scraper.cpp /Fe:scraper.exe ws2_32.lib wininet.lib
    if %ERRORLEVEL% equ 0 (
        echo [+] Compilation Successful! Generated scraper.exe
        echo [*] Launching C++ Embedded Web Server and Opening Browser...
        start http://127.0.0.1:8080
        scraper.exe --serve 8080
        goto :eof
    )
)

:: 3. Check for Python
where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo [+] Running project via Python Runner (zero external pip packages needed)...
    python run_project.py
    goto :eof
)

:: 4. Fallback: Launch standalone web interface directly
echo [!] Direct compiler or Python not found in current PATH.
echo [*] Launching modern Web Scraper Dashboard in default browser directly...
start "" "%~dp0web\index.html"
echo [+] Opened web/index.html. The dashboard is fully functional in offline mode.
pause
