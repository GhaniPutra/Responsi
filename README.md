# Responsi

## **Deskripsi Aplikasi**
Aplikasi ini adalah sistem manajemen ritel berbasis GUI yang dibuat dengan Python menggunakan pustaka Tkinter untuk antarmuka pengguna. Aplikasi ini memungkinkan pengguna untuk:
- **Admin Menu**: Menambahkan, menghapus, dan memperbarui data produk.
- **User Menu**: Membeli produk dan mengelola transaksi.
- Aplikasi terhubung ke database MySQL (`retail_db`) untuk menyimpan data produk dan transaksi.

---

## **Cara Menjalankan Aplikasi**
1. **Persiapan Database**:
   - Pastikan MySQL Server telah terinstal dan berjalan.
   - Buat database bernama `retail_db` dan tabel-tabel berikut:
     - `produk` untuk data produk.
     - `transaksi` untuk data transaksi.
   - Struktur tabel terdapat pada bagian berikut.

2. **Konfigurasi Lingkungan**:
   - Pastikan Python 3.x terinstal.
   - Instal pustaka yang dibutuhkan dengan perintah:
     ```bash
     pip install mysql-connector-python
     ```

3. **Menjalankan Aplikasi**:
   - Jalankan file Python (`Responsi.py`) menggunakan perintah:
     ```bash
     python Responsi.py
     ```

4. **Navigasi dalam Aplikasi**:
   - Gunakan menu utama untuk memilih **Admin Menu** atau **User Menu**.
   - Ikuti instruksi di antarmuka untuk menambahkan, menghapus, memperbarui, atau membeli produk.

---

## **Struktur Tabel Database**
1. **Tabel `produk`**:
   - **Kolom**:
     - `id_produk` (INT, Primary Key)
     - `nama_produk` (VARCHAR)
     - `harga` (INT)
   - Contoh Query:
     ```sql
     CREATE TABLE produk (
         id_produk INT PRIMARY KEY,
         nama_produk VARCHAR(255) NOT NULL,
         harga INT NOT NULL
     );
     ```

2. **Tabel `transaksi`**:
   - **Kolom**:
     - `id_transaksi` (INT, Primary Key)
     - `id_produk` (INT, Foreign Key ke tabel `produk`)
     - `jumlah_produk` (INT)
     - `total_harga` (INT)
     - `tanggal_transaksi` (DATE)
   - Contoh Query:
     ```sql
     CREATE TABLE transaksi (
         id_transaksi INT PRIMARY KEY,
         id_produk INT NOT NULL,
         jumlah_produk INT NOT NULL,
         total_harga INT NOT NULL,
         tanggal_transaksi DATE NOT NULL,
         FOREIGN KEY (id_produk) REFERENCES produk(id_produk)
     );
     ```

---
