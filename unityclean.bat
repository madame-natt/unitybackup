@echo off
setlocal enabledelayedexpansion

:: Set root path: first argument or current directory
if "%~1"=="" (
    set "ROOT_PATH=%CD%"
) else (
    set "ROOT_PATH=%~1"
)

echo Root path: %ROOT_PATH%
echo.

:: Change to root path and iterate subfolders
cd /d "%ROOT_PATH%"
for /d %%d in (*) do (
    if exist "%%d\Assets\" (
        echo Cleaning project: %%d
        rmdir /s /q "%%d\Library" 2>nul
        rmdir /s /q "%%d\Temp" 2>nul
        rmdir /s /q "%%d\obj" 2>nul
        rmdir /s /q "%%d\Logs" 2>nul
        echo Done with %%d
        echo.
    ) else (
        echo Skipping %%d ^(not a Unity project^)
        echo.
    )
)

echo Cleanup complete! Reopen projects in Unity to rebuild.
pause