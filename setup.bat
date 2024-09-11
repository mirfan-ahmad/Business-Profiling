@echo off

set "ENV_NAME=env"

if exist "%USERPROFILE%\.virtualenvs\%ENV_NAME%" (
  echo Environment "%ENV_NAME%" already exists. Activating...
  call "%USERPROFILE%\.virtualenvs\%ENV_NAME%\Scripts\activate.bat"
  if errorlevel 1 (
    echo Error activating environment! Exiting...
    exit /b 1
  )
) else (
  echo Creating virtual environment "%ENV_NAME%"...
  python -m venv "%USERPROFILE%\.virtualenvs\%ENV_NAME%"
  if errorlevel 1 (
    echo Error creating virtual environment! Exiting...
    exit /b 1
  )
  echo Environment "%ENV_NAME%" created. Activating...
  call "%USERPROFILE%\.virtualenvs\%ENV_NAME%\Scripts\activate.bat"
  if errorlevel 1 (
    echo Error activating environment! Exiting...
    exit /b 1
  )
)

echo Installing dependencies...
pip install -r requirements.txt
if !errorlevel! EQUALS 0 (
  echo Error installing dependencies! See above for details.
  exit /b 1
) else (
  echo Successfully installed dependencies.
)

pause  ; Wait for user input before closing the command prompt
