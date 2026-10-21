@echo off
rem Builds the games into Games\, ready to zip for a release:
rem
rem   Games\
rem     resources\            shared images and sounds
rem     Game Guide.docx
rem     Scuba Reader\
rem       Scuba Reader.exe
rem       scuba_words.txt     editable word list, copied from resources\scuba\
rem
rem Usage:  build.cmd                   rebuild only the games that changed since their last build
rem         build.cmd "Star CVC"        rebuild just the named game(s), changed or not
rem         build.cmd --all             wipe Games\ and rebuild everything (use this for releases)
rem
rem The game list and the change checking are in tools\build_games.py.
setlocal
cd /d "%~dp0"

if not exist .venv\Scripts\python.exe (
    echo Creating .venv...
    py -3 -m venv .venv || goto :error
)
set "PY=%CD%\.venv\Scripts\python.exe"
"%PY%" -m pip install --disable-pip-version-check -q -r requirements.txt || goto :error

"%PY%" tools\build_games.py %* || goto :error
exit /b 0

:error
echo.
echo Build failed.
exit /b 1
