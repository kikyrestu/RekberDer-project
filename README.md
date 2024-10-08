# Web Rekber (Rekening Bersama) dengan Fitur Chatting
---

## 📚 Deskripsi Proyek

Proyek ini bertujuan untuk menyediakan platform transaksi yang aman melalui rekening bersama, dilengkapi dengan fitur **realtime chat** yang menggunakan **Firebase** (pada tahap pengembangan). Pada server produksi, fitur chat akan menggunakan **Supabase**. Admin dapat memantau transaksi, melihat total penghasilan dari fee, dan mengelola transaksi yang bermasalah.

---

## 🛠️ Teknologi yang Digunakan

### Backend:
- **Django**: Untuk manajemen user, transaksi, dan pengelolaan database.
- **Node.js + Firebase**: Untuk pengembangan fitur **realtime chat** (untuk server produksi akan beralih ke **Supabase**).

### Database:
- **PostgreSQL**: Database utama untuk menyimpan data user, transaksi, room chat, dan fee.

### Caching dan Messaging:
- **Redis**: Untuk caching dan sebagai message broker untuk komunikasi realtime pada chat.

### Autentikasi:
- **JWT (JSON Web Token)**: Untuk autentikasi user antara Django dan Node.js.

### Server:
- **Windows Server**: Digunakan untuk pengembangan dan testing di localhost.
- **Linux**: Digunakan untuk server produksi, memberikan stabilitas dan performa yang lebih baik.

---

## 🧩 Struktur Utama Sistem

### A. Register dan Login
- **Register**: User dapat membuat akun baru.
- **Login**: User login ke akun mereka. Sistem menghasilkan token autentikasi (**JWT**) yang digunakan untuk mengakses berbagai fitur, termasuk room chat.

### B. Dashboard User (Buyer/Seller)
- **Dashboard**: Terintegrasi untuk buyer dan seller, memungkinkan user untuk bertindak sebagai buyer atau seller.
- **Form Transaksi**: User mengisi form untuk melakukan transaksi.
- **Button "Buat Room"**: Memulai transaksi dan membuat room chat.
- **Popup Konfirmasi**: Menampilkan total nominal transaksi + fee, dengan opsi "Batal" atau "Lanjut".
- **Total Transaksi di Room Chat**: Jika lanjut, total nominal muncul di header room chat.

### C. Perhitungan Fee
Fee dihitung secara otomatis berdasarkan nominal transaksi:
- 10K - 100K: Fee 5K
- 101K - 300K: Fee 10K
- 301K - 650K: Fee 15K
- 651K - 950K: Fee 20K
- 951K - 2Jt: Fee 25K
- 2Jt - 3,5Jt: Fee 35K
- 3,5Jt - 6,5Jt: 2,5%
- 6,5Jt - 10Jt: 3,4%
- 10Jt - 20Jt: 4,2%

### D. Room Chat
- Fitur **realtime chat** di-handle oleh **Firebase** pada tahap pengembangan.
- Pada server produksi, fitur chat akan menggunakan **Supabase**.
- Room chat dibuat setelah user menyetujui nominal transaksi dan fee, dan kedua pihak dapat berkomunikasi untuk menyelesaikan transaksi.

### E. Dashboard Admin
- **Total Penghasilan Fee**: Admin dapat melihat total penghasilan dari fee harian.
- **Jumlah Transaksi Harian**: Admin dapat memantau jumlah transaksi yang berhasil setiap hari.
- **Fitur Tambahan**:
  - Grafik jumlah transaksi atau fee per hari/bulan menggunakan **Chart.js**.
  - Daftar transaksi bermasalah atau pending.
  - Data pengguna aktif harian.

---

## 🔄 Alur Logika dan Flow

### A. Flow User untuk Transaksi:
1. User login.
2. Mengisi form harga di dashboard.
3. Klik "Buat Room".
4. Popup menampilkan total nominal + fee.
5. User memilih "Batal" atau "Lanjut".
6. Jika lanjut, room chat dibuat, dan total nominal muncul di header room chat.

### B. Alur Penghitungan Fee:
1. User memasukkan nominal transaksi.
2. Sistem menghitung fee secara otomatis.
3. Total nominal transaksi (harga + fee) ditampilkan di popup konfirmasi.

### C. Alur Dashboard Admin:
1. Admin login.
2. Melihat total penghasilan fee harian.
3. Melihat jumlah transaksi harian.
4. Mengelola transaksi bermasalah dan pengguna aktif.

---

## 🛠️ Tools dan Fitur Tambahan

- **nginx**: Untuk reverse proxy antara Django dan Node.js.
- **Docker**: Untuk containerization, jika dibutuhkan deployment yang scalable.
- **Celery**: Untuk job background seperti penghitungan fee atau laporan transaksi.

---

## 🚀 Cara Menjalankan Proyek

### Prasyarat
Untuk menjalankan proyek ini, Anda memerlukan:
- **Docker** *(optional)*: Untuk menjalankan proyek dalam container.
- **Python 3.x**: Untuk backend **Django**.
- **Node.js**: Untuk server realtime chat.
- **Firebase**: Digunakan untuk fitur realtime chat saat pengembangan.
- **Supabase** *(opsional untuk produksi)*: Untuk fitur realtime chat di server produksi.
- **PostgreSQL**: Sebagai database utama.
- **Redis**: Untuk caching dan message broker.
