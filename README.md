# Project Management Tool - NLP Text Analyzer

## Deskripsi Aplikasi

NLP Text Analyzer adalah aplikasi berbasis web yang dibangun dengan Django untuk melakukan analisis teks menggunakan teknik Natural Language Processing (NLP). Aplikasi ini menyediakan beberapa fitur analisis teks, termasuk:

1. **Analisis Sentimen**: Menentukan apakah teks memiliki sentimen positif, negatif, atau netral.
2. **Ringkasan Teks**: Membuat ringkasan otomatis dari teks panjang.
3. **Pengenalan Entitas (NER)**: Mengidentifikasi entitas seperti nama orang, organisasi, lokasi, dll. dalam teks.
4. **Klasifikasi Teks**: Mengkategorikan teks ke dalam kategori seperti bisnis, teknologi, kesehatan, pendidikan, atau hiburan.

## Fitur Utama

- **Analisis Teks**: Analisis teks dengan berbagai metode NLP.
- **Penyimpanan Analisis**: Menyimpan hasil analisis untuk referensi di masa mendatang.
- **Dashboard Pengguna**: Melihat dan mengelola analisis yang telah disimpan.
- **Template Teks**: Menyimpan template teks untuk digunakan kembali.
- **Berbagi Analisis**: Membuat analisis menjadi publik untuk dibagikan dengan pengguna lain.
- **Komentar**: Menambahkan komentar pada analisis yang dibagikan.
- **Tag**: Menambahkan tag pada analisis untuk pengorganisasian yang lebih baik.
- **Profil Pengguna**: Mengelola informasi profil dan preferensi analisis.

## Teknologi yang Digunakan

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **Database**: SQLite (development), MySQL (production)
- **NLP Libraries**: spaCy, NLTK
- **Authentication**: Django Authentication System

## Persyaratan Sistem

- Python 3.8 atau lebih tinggi
- Django 4.2.x
- spaCy dan NLTK dengan model bahasa Inggris
- Webserver (Apache/Nginx) untuk deployment
- Database MySQL (untuk production)

## Cara Penggunaan

1. **Halaman Utama**: Masukkan teks yang ingin dianalisis, pilih jenis analisis, dan klik tombol "Analyze".
2. **Dashboard**: Lihat semua analisis yang telah Anda simpan, filter berdasarkan jenis analisis atau kata kunci.
3. **Detail Analisis**: Lihat hasil analisis secara detail, tambahkan komentar, atau bagikan dengan pengguna lain.
4. **Profil**: Perbarui informasi profil dan preferensi analisis Anda.

## Instalasi Lokal

1. Clone repositori ini
2. Buat virtual environment: `python -m venv venv`
3. Aktifkan virtual environment: 
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependensi: `pip install -r requirements.txt`
5. Download model spaCy: `python -m spacy download en_core_web_sm`
6. Download resource NLTK: 
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('vader_lexicon')
   ```
7. Buat file `.env` dari `.env.example` dan sesuaikan konfigurasi
8. Jalankan migrasi database: `python manage.py migrate`
9. Buat superuser: `python manage.py createsuperuser`
10. Jalankan server: `python manage.py runserver`

Akses aplikasi di http://localhost:8000

## Deployment

Untuk deployment ke server produksi, ikuti langkah-langkah di [TUTORIAL_HOSTING_CPANEL.md](TUTORIAL_HOSTING_CPANEL.md) dan gunakan [CHECKLIST_DEPLOYMENT.md](CHECKLIST_DEPLOYMENT.md) sebagai panduan.

### Catatan Penting untuk NLTK Data

Aplikasi ini memerlukan data NLTK untuk berfungsi dengan baik. Pastikan data NLTK diunduh dengan benar di server produksi:

1. Secara otomatis melalui `passenger_wsgi.py` (sudah dikonfigurasi)
2. Atau secara manual melalui terminal:
   ```python
   python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"
   ```
3. Pastikan direktori `nltk_data` memiliki izin akses yang benar (755)

## Kontribusi

Kontribusi untuk pengembangan aplikasi ini sangat diterima. Silakan buat pull request atau laporkan issue jika Anda menemukan bug atau memiliki saran untuk perbaikan.

## Lisensi

Aplikasi ini dilisensikan di bawah [MIT License](LICENSE).