@echo off
chcp 65001 >nul
cls
echo ========================================================================
echo   SENTIMENT ANALYSIS WEB APP
echo   Ung dung web phan tich cam xuc
echo ========================================================================
echo.
echo [1/3] Kiem tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [X] LOI: Chua cai dat Python!
    echo     Vui long cai dat Python tu https://www.python.org/
    echo.
    pause
    exit /b 1
)
echo     [OK] Python da duoc cai dat
echo.
echo [2/3] Kiem tra thu vien...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo     Dang cai dat Flask...
    pip install flask
)
python -c "import textblob" >nul 2>&1
if errorlevel 1 (
    echo     Dang cai dat TextBlob...
    pip install textblob
    python -m textblob.download_corpora
)
echo     [OK] Cac thu vien da san sang
echo.
echo [3/3] Khoi dong web server...
echo.
echo ========================================================================
echo   WEB APP DANG CHAY
echo ========================================================================
echo.
echo   Mo trinh duyet va truy cap:
echo   http://localhost:5000
echo.
echo   Nhan Ctrl+C de dung server
echo.
echo ========================================================================
echo.
python app.py
pause
