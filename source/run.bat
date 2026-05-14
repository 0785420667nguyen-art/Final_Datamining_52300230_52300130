@echo off
chcp 65001 >nul
cls
echo ========================================================================
echo   SENTIMENT ANALYSIS - YOUTUBE API
echo   Phan tich cam xuc binh luan YouTube
echo ========================================================================
echo.
echo [1/4] Kiem tra Python...
python --version
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
echo [2/4] Kiem tra thu vien...
pip show pandas >nul 2>&1
if errorlevel 1 (
    echo     Dang cai dat cac thu vien can thiet...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [X] LOI: Khong the cai dat thu vien!
        echo     Thu chay: pip install pandas numpy matplotlib seaborn textblob google-api-python-client
        echo.
        pause
        exit /b 1
    )
) else (
    echo     [OK] Cac thu vien da duoc cai dat
)
echo.
echo [3/4] Kiem tra TextBlob corpora...
python -c "import textblob" >nul 2>&1
if errorlevel 1 (
    echo     Dang tai TextBlob corpora...
    python -m textblob.download_corpora
)
echo     [OK] TextBlob san sang
echo.
echo ========================================================================
echo [4/4] BAT DAU CHAY DU AN
echo ========================================================================
echo.
echo     Thoi gian du kien: 30-50 phut
echo     Buoc 1: Thu thap du lieu (5-10 phut)
echo     Buoc 2: Chuan hoa du lieu (2-5 phut)
echo     Buoc 3: Gan nhan (20-30 phut) - LAU NHAT!
echo     Buoc 4: Truc quan hoa (1-2 phut)
echo     Buoc 5: Phan tich sau (^<1 phut)
echo     Buoc 6: Demo ung dung (^<1 phut)
echo.
echo     LUU Y: Buoc 3 se mat 20-30 phut - day la BINH THUONG!
echo            Phan tich TOAN BO du lieu (khong gioi han 10,000)
echo.
echo ========================================================================
echo.
python sentiment_analysis.py
set EXIT_CODE=%errorlevel%
echo.
echo ========================================================================
if %EXIT_CODE% EQU 0 (
    echo   [OK] HOAN TAT THANH CONG!
    echo ========================================================================
    echo.
    echo   Cac file da tao:
    echo   - youtube_raw_data.csv      : Du lieu tho
    echo   - youtube_clean_data.csv    : Du lieu sach
    echo   - youtube_labeled_data.csv  : Du lieu da gan nhan (TOAN BO!)
    echo   - distribution.png          : Bieu do phan bo
    echo   - analysis.png              : Bieu do phan tich
    echo.
    echo   Ban co the mo cac file CSV bang Excel hoac Python
    echo   Ban co the xem cac file PNG bang trinh xem anh
    echo.
) else (
    echo   [X] CO LOI XAY RA!
    echo ========================================================================
    echo.
    echo   Vui long kiem tra thong bao loi phia tren
    echo   Hoac xem file HUONG_DAN_CHAY_DU_AN.md de biet them chi tiet
    echo.
)
echo ========================================================================
pause
