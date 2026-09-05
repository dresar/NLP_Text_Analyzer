# Tutorial Hosting Aplikasi Django di cPanel

Tutorial ini akan memandu Anda langkah demi langkah untuk menghosting aplikasi Django "NLP Text Analyzer" di cPanel.

## Persiapan Sebelum Hosting

### 1. Persiapkan Aplikasi Django Anda

1. **Perbarui settings.py untuk production**:
   - Buka file `nlp_app/settings.py`
   - Ubah `DEBUG = False`
   - Perbarui `ALLOWED_HOSTS` dengan domain Anda: `ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']`
   - Tambahkan konfigurasi untuk static files dan media files:
   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = BASE_DIR / 'static_root'
   MEDIA_URL = '/media/'
   MEDIA_ROOT = BASE_DIR / 'media_root'
   ```
   - Tambahkan konfigurasi untuk halaman error kustom:
   ```python
   HANDLER404 = 'analyzer.views.custom_404'
   HANDLER500 = 'analyzer.views.custom_500'
   HANDLER403 = 'analyzer.views.custom_403'
   ```

2. **Buat file .htaccess**:
   - Buat file `.htaccess` di direktori root proyek dengan konten berikut:
   ```
   <IfModule mod_rewrite.c>
   RewriteEngine On
   RewriteBase /
   RewriteRule ^index\.php$ - [L]
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteCond %{REQUEST_FILENAME} !-d
   RewriteRule . /index.php [L]
   </IfModule>
   ```

3. **Buat file passenger_wsgi.py**:
   - Buat file `passenger_wsgi.py` di direktori root proyek dengan konten berikut:
   ```python
   import os
   import sys
   
   # Tambahkan direktori proyek ke path
   sys.path.insert(0, os.path.dirname(__file__))
   
   # Atur variabel lingkungan untuk settings Django
   os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nlp_app.settings")
   
   # Import aplikasi WSGI Django
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

4. **Perbarui Database Settings untuk MySQL**:
   - Perbarui konfigurasi database di `nlp_app/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'your_cpanel_db_name',
           'USER': 'your_cpanel_db_user',
           'PASSWORD': 'your_cpanel_db_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

5. **Kumpulkan Static Files**:
   - Jalankan perintah: `python manage.py collectstatic`

6. **Buat file requirements.txt**:
   - Pastikan file `requirements.txt` sudah berisi semua dependensi yang diperlukan.

### 2. Persiapkan Arsip Proyek

1. **Buat arsip ZIP dari proyek**:
   - Pastikan untuk menyertakan semua file yang diperlukan (termasuk `requirements.txt`, `.htaccess`, dan `passenger_wsgi.py`)
   - Jangan sertakan file yang tidak perlu seperti `venv/`, `__pycache__/`, `.git/`, dll.

## Langkah-langkah Hosting di cPanel

### 1. Login ke cPanel

1. Buka browser dan masukkan URL cPanel Anda (biasanya `yourdomain.com/cpanel`)
2. Masukkan username dan password cPanel Anda

### 2. Buat Database MySQL

1. Di dashboard cPanel, cari dan klik "MySQL Databases"
2. Buat database baru dengan mengisi nama database
3. Buat user database baru dengan mengisi nama user dan password
4. Tambahkan user ke database dan berikan semua hak akses (ALL PRIVILEGES)
5. Catat nama database, username, dan password untuk digunakan di konfigurasi Django

### 3. Upload Aplikasi Django

1. Di dashboard cPanel, cari dan klik "File Manager"
2. Navigasi ke direktori `public_html` atau subdirektori tempat Anda ingin menghosting aplikasi
3. Klik tombol "Upload" dan upload file ZIP proyek Anda
4. Setelah upload selesai, ekstrak file ZIP

### 4. Setup Python Application

1. Di dashboard cPanel, cari dan klik "Setup Python App"
2. Klik tombol "Create Application"
3. Isi formulir dengan informasi berikut:
   - Python Version: Pilih versi Python yang kompatibel (3.8 atau lebih tinggi)
   - Application Root: Path ke direktori aplikasi Django Anda (misalnya `/home/username/public_html/myapp`)
   - Application URL: URL untuk aplikasi Anda (misalnya `yourdomain.com` atau `yourdomain.com/myapp`)
   - Application Entry Point: Path ke file `passenger_wsgi.py` (biasanya `/home/username/public_html/myapp/passenger_wsgi.py`)
   - Application Startup File: Biarkan kosong
4. Klik "Create"

### 5. Install Dependensi Python

1. Di halaman "Setup Python App", klik aplikasi yang baru dibuat
2. Klik tab "Modules"
3. Klik tombol "Install Packages"
4. Pilih "From Requirements File" dan pilih file `requirements.txt` Anda
5. Klik "Install"

### 6. Migrasi Database

1. Di cPanel, cari dan klik "Terminal"
2. Navigasi ke direktori aplikasi Django Anda:
   ```
   cd public_html/myapp
   ```
3. Aktifkan virtual environment (jika ada):
   ```
   source venv/bin/activate
   ```
4. Jalankan migrasi database:
   ```
   python manage.py migrate
   ```
5. Buat superuser (opsional):
   ```
   python manage.py createsuperuser
   ```

### 7. Konfigurasi Domain dan SSL

1. Di dashboard cPanel, cari dan klik "Domains"
2. Pastikan domain Anda sudah dikonfigurasi dengan benar dan mengarah ke direktori aplikasi Django
3. Untuk mengaktifkan SSL, cari dan klik "SSL/TLS Status"
4. Klik "Run AutoSSL" untuk menginstal sertifikat SSL secara otomatis

### 8. Restart Aplikasi Python

1. Kembali ke halaman "Setup Python App"
2. Klik aplikasi Django Anda
3. Klik tombol "Restart"

## Troubleshooting

### 1. Error 500 Internal Server Error

- Periksa file log error di cPanel (cari dan klik "Error Log" di dashboard cPanel)
- Pastikan file `passenger_wsgi.py` sudah benar
- Periksa konfigurasi database di `settings.py`
- Pastikan halaman error kustom 500.html sudah dibuat dengan benar

### 2. Error NLTK Data Tidak Ditemukan

- Pastikan NLTK data sudah diunduh dengan benar
- Jika mendapatkan error seperti `nltk.data.load(lexicon_file)` atau `Resource vader_lexicon not found`, jalankan perintah berikut melalui Terminal cPanel:
  ```
  cd public_html/myapp
  python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"
  ```
- Pastikan direktori `nltk_data` memiliki izin akses yang benar (755)
- Jika masih bermasalah, coba tambahkan direktori NLTK data secara manual di `passenger_wsgi.py`:
  ```python
  import nltk
  import os
  nltk_data_dir = os.path.join(os.path.dirname(__file__), 'nltk_data')
  os.environ['NLTK_DATA'] = nltk_data_dir
  ```

### 3. Static Files Tidak Muncul

- Pastikan `STATIC_ROOT` dan `STATIC_URL` sudah dikonfigurasi dengan benar
- Jalankan `python manage.py collectstatic` lagi
- Periksa path ke direktori static di cPanel

### 4. Database Connection Error

- Periksa konfigurasi database di `settings.py`
- Pastikan username, password, dan nama database sudah benar
- Periksa apakah user database memiliki hak akses yang cukup

### 5. Import Error untuk Modul Python

- Periksa apakah semua dependensi sudah terinstal dengan benar
- Coba install dependensi secara manual melalui Terminal cPanel

### 6. Halaman Error Kustom Tidak Muncul

- Pastikan `DEBUG = False` di settings.py
- Periksa konfigurasi handler di settings.py (`HANDLER404`, `HANDLER500`, `HANDLER403`)
- Pastikan file template error (404.html, 500.html, 403.html) berada di direktori templates
- Periksa fungsi view untuk halaman error di views.py

## Tips Tambahan

1. **Keamanan**:
   - Jangan simpan SECRET_KEY di file settings.py, gunakan variabel lingkungan
   - Pastikan DEBUG = False di production
   - Gunakan HTTPS untuk semua koneksi

2. **Performa**:
   - Aktifkan caching untuk meningkatkan performa
   - Gunakan CDN untuk static files
   - Optimalkan ukuran gambar dan file CSS/JS

3. **Backup**:
   - Buat backup database secara berkala
   - Backup file aplikasi secara berkala

4. **Monitoring**:
   - Pantau penggunaan resource server
   - Pantau error log secara berkala

Dengan mengikuti langkah-langkah di atas, aplikasi Django "NLP Text Analyzer" Anda seharusnya sudah berhasil dihosting di cPanel dan siap digunakan.