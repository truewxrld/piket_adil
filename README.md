# Piket Adil: Jadwal Piket Kos/Asrama

Mini project mata kuliah **Kecerdasan Komputasional (KKA)** dengan kategori
**Constraint Satisfaction Problem (CSP)**. Dibuat menggunakan Python dan Pygame.

## Kelompok 11

| Anggota | NRP |
|---|---|
| Muhammad Elmiro Rayhan R S | 5025231296 |
| Daffa Raihan Saputra | 5025231264 |

## Konsep dan fitur

Pemain mengisi jadwal piket penghuni kos/asrama mahasiswa ITS. Setiap hari
memiliki satu tempat untuk satu penghuni. Nama dan hari berhalangan pada level
merupakan data simulasi.

- Variabel CSP: setiap hari piket.
- Domain: daftar penghuni; hari berhalangan menyaring pilihan yang tersedia.
- Constraint 1: seseorang tidak boleh piket dua hari berturut-turut.
- Constraint 2: seseorang tidak boleh piket pada hari berhalangan.
- Mode manual: klik kartu hari, kemudian klik nama penghuni. Pelanggaran berwarna merah.
- Solver otomatis dengan tiga algoritma, animasi, jeda, dan pilihan kecepatan.
- Statistik jumlah assignment, backtrack, dan waktu komputasi.
- Tiga level dengan total sembilan kombinasi level dan algoritma.

Tidak ada constraint tambahan untuk menyamakan jumlah tugas setiap penghuni.
Hari 7 dan 8 tetap berurutan; hari terakhir tidak dihubungkan kembali ke hari pertama.

| Level | Hari | Penghuni | Algoritma tersedia |
|---|---:|---:|---|
| 1: Santai | 5 | 4 | BT, BT + FC, BT + MRV |
| 2: Sibuk | 7 | 5 | BT, BT + FC, BT + MRV |
| 3: Padat | 14 | 6 | BT, BT + FC, BT + MRV |

## Struktur file

| File | Fungsi |
|---|---|
| `solver.py` | Tiga algoritma CSP, generator langkah, dan statistik |
| `game_logic.py` | Data level, validasi manual, dan keadaan permainan |
| `game_render.py` | Kartu jadwal, tombol, panel statistik, dan warna pelanggaran |
| `main.py` | Event loop Pygame dan penghubung input pemain |

## Instalasi dan menjalankan

Disarankan menggunakan Python 3.12. Proyek diuji dengan Python 3.12 dan
Pygame 2.6.1. Ekstrak ZIP, buka folder proyek di VS Code, lalu buka terminal.

Windows:

```powershell
py -m pip install pygame==2.6.1
py main.py
```

Linux/macOS:

```bash
python3 -m pip install pygame==2.6.1
python3 main.py
```

Pastikan perintah dijalankan dari folder yang berisi `main.py`. Program membuka
jendela 1200 x 720 dan tidak memerlukan aset gambar, suara, atau koneksi internet
setelah instalasi. Jika `py` tidak tersedia di Windows, gunakan `python` untuk
kedua perintah tersebut.

## Cara bermain dan kontrol

1. Pilih level dan algoritma di bagian atas.
2. Untuk mode manual, klik hari lalu nama penghuni. Nama yang berhalangan tetap
   dapat dipilih agar pelanggarannya terlihat. Perbaiki kartu merah sampai semua
   hari terisi tanpa pelanggaran.
3. Klik **Solver** untuk pencarian otomatis dari jadwal kosong. Isian manual
   sebelumnya dibersihkan supaya semua algoritma memulai dari kondisi yang sama.
4. Amati kartu berbingkai kuning, percobaan merah, langkah mundur, dan statistik.
   Gunakan kecepatan Lambat untuk demonstrasi proses.
5. Klik **Reset** untuk menghentikan pencarian dan mengosongkan jadwal.

| Kontrol | Fungsi |
|---|---|
| Klik hari, kemudian nama | Mengisi atau mengganti penghuni |
| Kosongkan hari / Delete / Backspace | Menghapus isian hari yang dipilih |
| 1 / 2 / 3 | Memilih level |
| Tab | Berpindah algoritma |
| S | Menjalankan solver |
| Spasi | Menjeda atau melanjutkan animasi |
| F | Mengganti kecepatan: Lambat, Normal, Cepat |
| R | Reset jadwal dan statistik, sekaligus membatalkan solver |
| Esc | Keluar |

Pemilihan level, algoritma, dan pengeditan manual dinonaktifkan selama solver
berjalan, termasuk saat dijeda. Tekan Reset terlebih dahulu untuk mengubahnya.
Pergantian level/algoritma mengosongkan jadwal dan statistik. Edit manual setelah
solver selesai menghapus statistik lama karena jadwalnya sudah berubah.

## Penjelasan algoritma

**Backtracking (BT).** Mengisi hari kosong dari nomor terkecil. Penghuni dicoba
sesuai urutan pada data level. Jika pilihan melanggar aturan, coba penghuni lain.
Jika seluruh pilihan gagal, batalkan penempatan sebelumnya dan cari cabang lain.

**Backtracking + Forward Checking (FC).** Setelah penempatan yang valid,
hapus penghuni tersebut dari domain hari tetangga yang belum terisi. Jika ada
domain yang kosong, langsung mundur. Setiap cabang memakai salinan domain agar
domain sebelumnya pulih ketika backtracking. Urutan hari tetap kronologis.

**Backtracking + MRV.** Pilih hari kosong dengan jumlah kandidat valid paling
sedikit berdasarkan jadwal saat ini. Jika sama, pilih nomor hari terkecil.
Pemeriksaan harus melihat tetangga di kiri dan kanan karena urutan pengisian
bisa melompat. Implementasi MRV ini tidak digabungkan dengan Forward Checking.

Ketiga algoritma menyaring penghuni berhalangan sebelum pencarian dan memakai
urutan penghuni yang sama. Semua mencari solusi pertama yang valid.

## Arti statistik dan animasi

- **Assignment:** jumlah percobaan menempatkan penghuni, termasuk percobaan
  yang langsung ditolak. Nilai yang sudah disaring dari domain tidak dicoba.
- **Backtrack:** jumlah penempatan valid yang dibatalkan karena cabangnya gagal.
  Penolakan langsung terhadap kandidat yang melanggar tidak menambah backtrack.
- **Waktu komputasi:** akumulasi waktu saat generator solver dijalankan dengan
  `perf_counter()`. Tidak mencakup jeda animasi, jeda pengguna, atau menggambar UI.
  Ini pengukuran implementasi solver, termasuk pencatatan langkahnya.

Generator menghasilkan langkah `assign`, `reject`, dan `backtrack`. Event loop
tetap berjalan sehingga jendela bisa menerima input selama animasi. Kecepatan
Cepat memproses paling banyak 100 langkah per frame.

Data Level 3 sengaja menyediakan banyak hari berhalangan dan beberapa hari
dengan satu pilihan. Dengan data bawaan, hasil hitungnya:

| Algoritma | Assignment | Backtrack |
|---|---:|---:|
| Backtracking | 39 | 11 |
| Backtracking + FC | 25 | 11 |
| Backtracking + MRV | 19 | 0 |

Jumlah langkah yang lebih sedikit tidak selalu berarti waktu lebih singkat.
FC memerlukan penyalinan domain dan MRV menghitung kandidat. Pada contoh kecil,
overhead ini bisa lebih besar daripada penghematan pencarian. Waktu juga dapat
berubah antarpercobaan dan komputer; bandingkan beberapa kali pada level sama.

## Mengubah data level

Edit `LEVELS` di `game_logic.py`. `unavailable` memetakan nama penghuni ke
himpunan nomor hari berhalangan, **mulai dari 1**. Contoh: `"Daffa": {2, 4}`.
Indeks list jadwal di dalam kode dimulai dari 0. Semua nama harus unik dan nomor
hari berhalangan harus berada dalam rentang level. Solver juga menangani data
yang tidak memiliki solusi dan menampilkan pesan kegagalan.

## Referensi

- Russell, S., & Norvig, P. (2021). *Artificial intelligence: A modern approach*
  (4th ed.). Pearson.
- Mackworth, A. K. (1977). Consistency in networks of relations.
  *Artificial Intelligence, 8*(1), 99–118.
- Haralick, R. M., & Elliott, G. L. (1980). Increasing tree search efficiency for
  constraint satisfaction problems. *Artificial Intelligence, 14*(3), 263–313.
- Pygame Community. (n.d.). *Pygame documentation*. https://www.pygame.org/docs/
