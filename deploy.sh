#!/bin/bash

# Script untuk mempersiapkan aplikasi Django untuk deployment ke cPanel

echo "Mempersiapkan aplikasi Django untuk deployment ke cPanel..."

# Pastikan kita berada di direktori proyek
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Aktifkan virtual environment jika ada
if [ -d "venv" ]; then
    echo "Mengaktifkan virtual environment..."
    source venv/bin/activate
fi

# Install dependensi
echo "Menginstall dependensi..."
pip install -r requirements.txt

# Download model spaCy jika belum ada
if ! python -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null; then
    echo "Mengunduh model spaCy..."
    python -m spacy download en_core_web_sm
fi

# Download resource NLTK jika belum ada
echo "Mengunduh resource NLTK..."
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"

# Buat file .env dari .env.example jika belum ada
if [ ! -f ".env" ]; then
    echo "Membuat file .env dari .env.example..."
    cp .env.example .env
    echo "PERHATIAN: Silakan edit file .env dengan informasi yang benar sebelum melanjutkan."
    echo "Tekan Enter untuk melanjutkan setelah mengedit file .env..."
    read
fi

# Kumpulkan static files
echo "Mengumpulkan static files..."
python manage.py collectstatic --noinput

# Buat direktori untuk logs jika belum ada
if [ ! -d "logs" ]; then
    echo "Membuat direktori logs..."
    mkdir logs
fi

# Buat direktori untuk media jika belum ada
if [ ! -d "media_root" ]; then
    echo "Membuat direktori media_root..."
    mkdir media_root
fi

# Buat arsip ZIP untuk deployment
echo "Membuat arsip ZIP untuk deployment..."
zip -r nlp_text_analyzer_deploy.zip . -x "venv/*" "__pycache__/*" ".git/*" "*.pyc" "*.pyo" "*.pyd" ".DS_Store" "*.zip"

echo "Persiapan selesai! File nlp_text_analyzer_deploy.zip siap untuk diupload ke cPanel."
echo "Silakan ikuti langkah-langkah dalam TUTORIAL_HOSTING_CPANEL.md untuk melanjutkan proses deployment."