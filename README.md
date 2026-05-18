# Aplikasi Cipher (Web)

Aplikasi web sederhana untuk demonstrasi dan pengeksplorasian beberapa algoritma sandi klasik (Caesar, Vigenère, Affine, Hill, Playfair). Dibangun dengan Python dan Flask; menyediakan antarmuka web interaktif untuk enkripsi, dekripsi, dan melihat langkah-langkah perhitungan.

## Fitur

- Enkripsi dan dekripsi: Caesar, Vigenère, Affine, Hill, Playfair
- Menampilkan langkah-langkah perhitungan detail untuk pembelajaran
- Tabel Vigenère dan langkah visual untuk Hill Cipher
- Riwayat terakhir (session) sampai 20 entri
- Validasi input kunci dan pesan dengan pesan kesalahan yang user-friendly

## Struktur Proyek

- [app.py](app.py) — Entrypoint Flask; route untuk setiap cipher dan halaman.
- /crypto — Implementasi algoritma cipher:
  - [crypto/caesar.py](crypto/caesar.py)
  - [crypto/vigenere.py](crypto/vigenere.py)
  - [crypto/affine.py](crypto/affine.py)
  - [crypto/hill.py](crypto/hill.py)
  - [crypto/playfair.py](crypto/playfair.py)
- /templates — Template Jinja2 untuk UI:
  - [templates/index.html](templates/index.html)
  - [templates/cipher.html](templates/cipher.html)
  - [templates/history.html](templates/history.html)
  - [templates/base.html](templates/base.html)
- /static — CSS/JS
  - [static/css/style.css](static/css/style.css)
  - [static/js/main.js](static/js/main.js)
- [requirements.txt](requirements.txt)

## Persyaratan

- Python 3.8+
- Dependensi ada di `requirements.txt`

## Cara Menjalankan (Local)

1. Buat virtual environment dan aktifkan (Windows PowerShell contoh):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependensi:

```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi:

```bash
python app.py
```

4. Buka browser ke: http://127.0.0.1:5000

## Penjelasan Singkat Setiap Cipher

- Caesar
  - Pergeseran sederhana pada alfabet.
  - Kunci: bilangan bulat 1–25.
  - Ditampilkan langkah per karakter dan rumus modular.

- Vigenère
  - Polyalphabetic substitution menggunakan kunci teks.
  - Kunci harus mengandung huruf (A–Z); spasi dan non-huruf diabaikan.
  - Menampilkan tabel Vigenère dan langkah per karakter.

- Affine
  - Transformasi linear: E(x) = (a x + b) mod 26.
  - Syarat: `a` harus coprime dengan 26 (jika tidak, aplikasi menolak).
  - Saat dekripsi, dihitung invers modular `a^-1`.

- Hill
  - Cipher matrix: block n×n dan perkalian matriks modulo 26.
  - Input: ukuran matriks dan elemen matriks (integer).
  - Menampilkan padding bila diperlukan, kalkulus determinan/invers untuk dekripsi.

- Playfair
  - Cipher bigram dengan matriks 5×5 (I/J digabungkan).
  - Key harus berisi minimal satu huruf; huruf ganda ditangani dengan filler (X atau Q).

## Routing / Endpoints

- `/` — Halaman utama
- `/history` — Lihat riwayat session
- `/clear_history` — Hapus riwayat
- `/caesar` — Form dan hasil Caesar
- `/vigenere` — Form dan hasil Vigenère
- `/affine` — Form dan hasil Affine
- `/hill` — Form dan hasil Hill
- `/playfair` — Form dan hasil Playfair

## Catatan Implementasi

- Riwayat disimpan di `session` Flask (secret key di-generate otomatis di `app.py`).
- Validasi input diletakkan di route handler dan modul `crypto` mengembalikan struktur `{"result": ..., "steps": [...]}` untuk ditampilkan di template.
- UI menampilkan langkah-langkah dalam HTML yang sudah dirender dari modul cipher (gunakan kelas CSS untuk tampilan).

## Pengembangan & Kontribusi

- Untuk menambah algoritma baru, tambahkan modul di folder `crypto/` dengan fungsi `process_<nama>(...)` dan daftarkan importnya di `crypto/__init__.py`.
- Buat route baru di `app.py` dan template mengacu pada `cipher.html` yang sudah ada.

## Tes Manual Singkat

- Jalankan aplikasi dan coba setiap halaman cipher.
- Periksa validasi kunci: contoh
  - Caesar: masukkan 0 atau 26 → harus error
  - Affine: masukkan `a=2` → harus error karena tidak coprime
  - Vigenère: kosongkan kunci → harus error

## Lisensi

Terserah Anda — tambahkan file `LICENSE` jika perlu.

---

Jika Anda mau, saya bisa:
- Menambahkan contoh screenshot atau GIF kecil untuk README
- Menambahkan badge dependensi atau instruksi Docker
- Menjalankan aplikasi di lingkungan Anda dan menguji endpoint