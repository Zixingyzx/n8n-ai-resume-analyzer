@echo off
setlocal
cd /d "%~dp0"
python src\resume_analyzer.py --resume sample_data\sample_resume.txt --job sample_data\sample_job_description.txt --target-role "Working Student AI Automation" --output-dir outputs
if errorlevel 1 (
  echo.
  echo Demo failed. Check that Python is installed and available in PATH.
  pause
  exit /b 1
)
echo.
echo Demo completed successfully.
pause
