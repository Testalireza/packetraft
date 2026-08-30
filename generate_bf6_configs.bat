@echo off
:: ============================================================================
:: Battlefield 6 WireGuard Configuration Generator - Windows Batch Script
:: ============================================================================
::
:: This batch file generates WireGuard configurations for Battlefield 6
:: compatible with PacketRaft infrastructure.
::
:: CONFIRMED from PacketRaft.exe analysis:
:: - Uses WireGuard for VPN tunnel
:: - Uses WinDivert for packet interception
:: - Internal tunnel network: 10.88.0.0/16
:: - API: https://packetraft.ir/api
::
:: Usage:
::   generate_bf6_configs.bat              - Generate single config
::   generate_bf6_configs.bat multiple     - Generate multiple configs
::   generate_bf6_configs.bat all-traffic  - Route all traffic
::
:: ============================================================================

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed.
    echo Please install Python 3.6 or later from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Create configs directory
if not exist "configs" (
    mkdir configs
)

:: Determine script directory
set "SCRIPT_DIR=%~dp0"

:: Check arguments
if "%~1" == "" (
    :: Generate single config
    echo Generating Battlefield 6 WireGuard configuration...
    echo.
    python "%SCRIPT_DIR%simple_bf6_wg_generator.py" --server ir1.packetraft.ir --port 51820 --output bf6_iran.conf
    goto :show_result
)

if "%~1" == "multiple" (
    :: Generate multiple configs
    set COUNT=5
    if not "%~2" == "" (
        set COUNT=%~2
    )
    echo Generating %COUNT% Battlefield 6 configurations...
    echo.
    python "%SCRIPT_DIR%simple_bf6_wg_generator.py" --multiple %COUNT%
    goto :show_result
)

if "%~1" == "all-traffic" (
    :: Route all traffic
    echo Generating Battlefield 6 configuration with all traffic routing...
    echo.
    python "%SCRIPT_DIR%simple_bf6_wg_generator.py" --server ir1.packetraft.ir --port 51820 --output bf6_full.conf --all-traffic
    goto :show_result
)

:: Unknown argument
echo Usage:
 echo   generate_bf6_configs.bat              - Generate single config
echo   generate_bf6_configs.bat multiple     - Generate multiple configs
echo   generate_bf6_configs.bat all-traffic  - Route all traffic
echo.
goto :eof

:show_result
:: Show generated files
echo.
echo Generated configuration files:
echo ============================================================================
for /f "delims=" %%f in ('dir /b configs\*.conf 2^>nul') do (
    echo   configs\%%f
)
echo ============================================================================
echo.
echo To use these configurations:
echo 1. Install WireGuard client from https://www.wireguard.com/install/
echo 2. Open WireGuard
echo 3. Click "Import tunnels from file"
echo 4. Select the .conf file
echo 5. Activate the tunnel
echo.
echo For full PacketRaft functionality (split tunneling):
echo - Install WinDivert64.sys and ndisrd.sys drivers
echo - Use the PacketRaft client application
echo.
pause
