set "ENV_NAME=env"
echo Activating environment "%ENV_NAME%"...
call "%USERPROFILE%\.virtualenvs\%ENV_NAME%\Scripts\activate.bat"
if errorlevel 1 (
  echo Error activating environment! Exiting...
  exit /b 1
)

echo Running Streamlit app...
streamlit run APP.py

pause  ; Wait for user input before closing the command prompt
