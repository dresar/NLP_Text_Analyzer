@echo off
echo Mempersiapkan aplikasi Django untuk deployment ke cPanel...

:: Pastikan kita berada di direktori proyek
cd /d "%~dp0"

:: Aktifkan virtual environment jika ada
if exist venv\Scripts\activate.bat (
    echo Mengaktifkan virtual environment...
    call venv\Scripts\activate.bat
)

:: Install dependensi
echo Menginstall dependensi...
pip install -r requirements.txt

:: Download model spaCy jika belum ada
python -c "import spacy; spacy.load('en_core_web_sm')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Mengunduh model spaCy...
    python -m spacy download en_core_web_sm
)

:: Download resource NLTK
echo Mengunduh resource NLTK...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"

:: Buat file .env dari .env.example jika belum ada
if not exist .env (
    echo Membuat file .env dari .env.example...
    copy .env.example .env
    echo PERHATIAN: Silakan edit file .env dengan informasi yang benar sebelum melanjutkan.
    echo Tekan Enter untuk melanjutkan setelah mengedit file .env...
    pause
)

:: Kumpulkan static files
echo Mengumpulkan static files...
python manage.py collectstatic --noinput

:: Buat direktori untuk logs jika belum ada
if not exist logs (
    echo Membuat direktori logs...
    mkdir logs
)

:: Buat direktori untuk media jika belum ada
if not exist media_root (
    echo Membuat direktori media_root...
    mkdir media_root
)

:: Buat arsip ZIP untuk deployment
echo Membuat arsip ZIP untuk deployment...

:: Cek apakah PowerShell tersedia
powershell -Command "$PSVersionTable.PSVersion.Major" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    :: Gunakan PowerShell untuk membuat ZIP
    powershell -Command "Compress-Archive -Path *.py,*.md,*.txt,*.bat,*.sh,.htaccess,.env,analyzer,nlp_app,static,static_root,media_root,logs,templates -DestinationPath nlp_text_analyzer_deploy.zip -Force"
) else (
    echo PowerShell tidak tersedia. Silakan install aplikasi ZIP seperti 7-Zip dan buat arsip secara manual.
    echo Jangan sertakan direktori: venv, __pycache__, .git
    pause
    exit
)

echo Persiapan selesai! File nlp_text_analyzer_deploy.zip siap untuk diupload ke cPanel.
echo Silakan ikuti langkah-langkah dalam TUTORIAL_HOSTING_CPANEL.md untuk melanjutkan proses deployment.

pause