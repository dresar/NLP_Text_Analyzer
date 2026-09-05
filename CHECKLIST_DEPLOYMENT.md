# Checklist Deployment ke cPanel

Gunakan checklist ini untuk memastikan semua langkah deployment sudah dilakukan dengan benar.

## Persiapan Lokal

- [ ] Update `settings.py` dengan konfigurasi produksi yang benar
- [ ] Buat file `.env` dengan informasi yang benar (dari `.env.example`)
- [ ] Jalankan `python manage.py collectstatic` untuk mengumpulkan static files
- [ ] Pastikan semua dependensi tercantum di `requirements.txt`
- [ ] Jalankan script `deploy.bat` (Windows) atau `deploy.sh` (Linux/Mac) untuk mempersiapkan file deployment
- [ ] Periksa file `nlp_text_analyzer_deploy.zip` yang dihasilkan

## Setup cPanel

- [ ] Login ke cPanel
- [ ] Buat database MySQL baru
- [ ] Buat user database baru dan tambahkan ke database
- [ ] Berikan hak akses ALL PRIVILEGES ke user database
- [ ] Upload file `nlp_text_analyzer_deploy.zip` ke direktori yang diinginkan di cPanel
- [ ] Ekstrak file ZIP yang diupload

## Konfigurasi Aplikasi di cPanel

- [ ] Setup Python Application di cPanel
- [ ] Install dependensi dari `requirements.txt`
- [ ] Download data NLTK yang diperlukan:
  ```
  python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"
  ```
- [ ] Jalankan migrasi database: `python manage.py migrate`
- [ ] Buat superuser: `python manage.py createsuperuser`
- [ ] Pastikan file `.htaccess` sudah berada di direktori root aplikasi
- [ ] Pastikan file `passenger_wsgi.py` sudah berada di direktori root aplikasi
- [ ] Pastikan direktori `nltk_data` memiliki izin akses yang benar (755)

## Konfigurasi Domain dan SSL

- [ ] Konfigurasi domain untuk mengarah ke direktori aplikasi
- [ ] Aktifkan SSL untuk domain (gunakan AutoSSL di cPanel)

## Pengujian

- [ ] Buka website dengan domain yang sudah dikonfigurasi
- [ ] Pastikan halaman utama dapat diakses
- [ ] Login dengan superuser yang sudah dibuat
- [ ] Uji fitur-fitur utama aplikasi:
  - [ ] Analisis Sentimen
  - [ ] Ringkasan Teks
  - [ ] Pengenalan Entitas
  - [ ] Klasifikasi Teks
  - [ ] Penyimpanan Analisis
  - [ ] Dashboard Pengguna
  - [ ] Profil Pengguna
- [ ] Uji halaman error kustom:
  - [ ] Halaman 404 (Coba akses URL yang tidak ada)
  - [ ] Halaman 403 (Coba akses halaman yang memerlukan izin)
  - [ ] Halaman 500 (Perlu diuji saat terjadi error server)

## Pemecahan Masalah

Jika terjadi error, periksa:

- [ ] File log error di cPanel
- [ ] Konfigurasi database di `.env` dan pastikan `settings.py` membacanya dengan benar
- [ ] Konfigurasi Python Application di cPanel
- [ ] Hak akses file dan direktori

## Pemeliharaan

- [ ] Setup backup database berkala
- [ ] Setup backup file aplikasi berkala
- [ ] Pantau penggunaan resource server
- [ ] Pantau error log secara berkala

## Catatan Tambahan

- Jika ada perubahan pada aplikasi, ulangi proses deployment dari awal
- Pastikan untuk selalu membuat backup sebelum melakukan perubahan besar
- Jika menggunakan domain custom, pastikan DNS sudah dikonfigurasi dengan benar