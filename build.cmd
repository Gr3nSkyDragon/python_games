@echo off
rem Builds every game into Games\, ready to zip for a release:
rem
rem   Games\
rem     resources\            shared images and sounds
rem     Game Guide.docx
rem     Scuba Reader\
rem       Scuba Reader.exe
rem       scuba_words.txt     editable word list, copied from resources\scuba\
rem
rem Usage:  build.cmd                  rebuild everything (wipes Games\ first)
rem         build.cmd "Star CVC"       rebuild one game and refresh resources\
setlocal
cd /d "%~dp0"
set "ONLY=%~1"
set "FOUND="

if not exist .venv\Scripts\python.exe (
    echo Creating .venv...
    py -3 -m venv .venv || goto :error
)
set "PY=%CD%\.venv\Scripts\python.exe"
"%PY%" -m pip install --disable-pip-version-check -q -r requirements.txt || goto :error

if not defined ONLY if exist Games rmdir /s /q Games

rem       script                  exe name              icon                editable text files
call :game alphabet_blast.py      "Alphabet Blast"      apple.ico           || goto :error
call :game alphabet_galaxy.py     "Alphabet Galaxy"     telescope.ico       || goto :error
call :game cowboy.py              "Cowboy"              cowboy_hat.ico      cowboy\cowboy.txt || goto :error
call :game find_the_princess.py   "Find the Princess"   princess_icon.ico   princess\hidden_content.txt princess\rectangle_content.txt || goto :error
call :game letter_pop.py          "Letter Pop"          balloon.ico         letter_pop\poppers.txt || goto :error
call :game letter_reveal.py       "Letter Reveal"       reveal.ico          reveal\letters.txt || goto :error
call :game phonicsmon.py          "Phonicsmon"          phonics.ico         || goto :error
call :game random_wheel_spin.py   "Random Wheel Spin"   wheel.ico           || goto :error
call :game scuba_reader.py        "Scuba Reader"        snorkel.ico         scuba\scuba_words.txt || goto :error
call :game star_cvc.py            "Star CVC"            star.ico            || goto :error
call :game word_maker.py          "Word Maker"          robot.ico           || goto :error

if defined ONLY if not defined FOUND (
    echo No game named "%ONLY%". Use one of the exe names listed in build.cmd.
    exit /b 1
)

echo Copying shared resources...
rem Text files go next to each exe instead; robocopy exit codes below 8 mean success
robocopy resources Games\resources /E /XF *.txt *.py /NFL /NDL /NJH /NJS /NP >nul
if errorlevel 8 goto :error
copy /y "Game Guide.docx" Games\ >nul || goto :error

echo.
echo Done. Games are in %CD%\Games
exit /b 0


rem :game <script> <exe name> <icon> [editable text files...]
:game
if defined ONLY if /i not "%ONLY%"=="%~2" exit /b 0
set "FOUND=1"
set "NAME=%~2"
echo Building %NAME%...
if exist "Games\%NAME%" rmdir /s /q "Games\%NAME%"
"%PY%" -m PyInstaller --noconfirm --log-level WARN --onefile --windowed ^
    --name "%NAME%" --icon "%CD%\resources\icon\%~3" ^
    --distpath "Games\%NAME%" --workpath build --specpath build ^
    "%~1" || exit /b 1
:copy_text
if "%~4"=="" exit /b 0
copy /y "resources\%~4" "Games\%NAME%\" >nul || exit /b 1
shift /4
goto :copy_text


:error
echo.
echo Build failed.
exit /b 1
