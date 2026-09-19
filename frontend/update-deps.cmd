@echo off
setlocal
cd /d "%~dp0"

echo Installing npm-check-updates globally...
call npm.cmd install -g npm-check-updates
if errorlevel 1 goto error

for /f "delims=" %%P in ('call npm.cmd prefix --global') do set "npm_global_prefix=%%P"

echo Running npm-check-updates (ncu)...
call "%npm_global_prefix%\ncu.cmd" -u
if errorlevel 1 goto error

echo Installing updated dependencies...
call npm.cmd install
if errorlevel 1 goto error

echo Updating transitive dependencies...
call npm.cmd update
if errorlevel 1 goto error

echo Running npm audit...
call npm.cmd audit
if errorlevel 1 goto error

echo Done!
pause
exit /b 0

:error
set "update_exit_code=%errorlevel%"
echo Update failed with exit code %update_exit_code%.
pause
exit /b %update_exit_code%
