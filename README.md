# 🎓 Sistem Deteksi Gaya Belajar Siswa

Aplikasi web berbasis Python Streamlit untuk mendeteksi gaya belajar siswa menggunakan metode VAK (Visual, Auditory, Kinesthetic) dengan sistem pakar rule-based.

## 👥 Tim Pengembang - Kelompok 3

1. **Muhammad Irbabul Salas** (25083010055) - Project Manager
2. **Furqon Hanif** (25083010125) - Backend Developer
3. **Rafinda Mutiara Nurfitriati** (25083010012) - Frontend Developer
4. **Kasnanda Holymapah Siagian** (25083010039) - UI/UX Designer

## 📋 Deskripsi Proyek

Sistem pakar ini dirancang untuk membantu siswa mengetahui gaya belajar mereka melalui kuisioner interaktif. Aplikasi akan menganalisis jawaban dan memberikan:
- Deteksi tipe gaya belajar dominan (Visual, Auditori, atau Kinestetik)
- Visualisasi hasil dalam bentuk grafik (radar, pie, bar chart)
- Rekomendasi metode belajar yang sesuai
- Tips belajar efektif dan menghadapi ujian
- Tools/aplikasi yang cocok untuk gaya belajar tersebut

## ✨ Fitur Utama

### 1. Landing Page
- Hero section dengan CTA
- Tim pengembang dengan foto/avatar placeholder
- Penjelasan gaya belajar VAK
- Cara kerja sistem
- FAQ section
- Footer dengan daftar referensi akademik

### 2. Form Data Responden
- Input nama, usia, jenjang pendidikan, jenis kelamin
- Upload foto profil (opsional)
- Validasi form

### 3. Kuisioner Interaktif
- 25 pertanyaan dengan skala Likert (1-5)
- Progress bar
- Navigasi antar pertanyaan
- Auto-save jawaban

### 4. Sistem Pakar
- Rule-based inference engine
- Perhitungan skor untuk Visual, Auditori, Kinestetik
- Penentuan tipe dominan berdasarkan skor tertinggi

### 5. Hasil Analisis
- Profil responden dengan foto/avatar
- Grafik visualisasi (Plotly):
  - Radar chart
  - Pie chart
  - Bar chart
- Rekomendasi metode belajar spesifik
- Tips dan tools yang cocok
- Download hasil ke PDF

### 6. Fitur Tambahan
- Halaman "Tentang Gaya Belajar" dengan penjelasan detail
- FAQ (Frequently Asked Questions)
- Halaman Kontak
- Riwayat tes dengan database PostgreSQL
- Opsi tes ulang

## 🛠️ Teknologi yang Digunakan

### Backend & Framework
- **Python 3.11**
- **Streamlit** - Framework web app
- **SQLAlchemy** - ORM untuk database
- **PostgreSQL** - Database

### Data Processing & Visualization
- **Pandas** - Manipulasi data
- **NumPy** - Komputasi numerik
- **Plotly** - Visualisasi grafik interaktif

### PDF Generation
- **ReportLab** - Generate PDF hasil tes

### Image Processing
- **Pillow (PIL)** - Upload dan resize foto

### UI Components
- **Streamlit-extras** - Komponen UI tambahan
- Custom CSS untuk styling

## 📦 Struktur Proyek

```
.
├── app.py                  # File utama aplikasi Streamlit
├── database.py             # Model database SQLAlchemy
├── kuisioner_data.py       # Data pertanyaan kuisioner
├── expert_system.py        # Sistem pakar rule-based
├── team_data.py            # Data tim dan referensi
├── pdf_generator.py        # Generator PDF hasil
├── README.md               # Dokumentasi ini
├── pyproject.toml          # Dependencies Python
├── .streamlit/
│   └── config.toml        # Konfigurasi Streamlit
└── attached_assets/        # Folder untuk foto dan assets
```

## 🚀 Cara Menjalankan di Replit

### Prasyarat
Aplikasi ini sudah dikonfigurasi untuk berjalan di Replit dengan PostgreSQL built-in.

### Langkah-langkah:

1. **Pastikan dependencies terinstall**
   ```bash
   uv sync
   ```

2. **Database sudah otomatis dikonfigurasi**
   - PostgreSQL Replit sudah tersedia
   - Tabel akan dibuat otomatis saat pertama kali run

3. **Jalankan aplikasi**
   ```bash
   streamlit run app.py --server.port 5000
   ```
   
   Atau gunakan tombol **Run** di Replit.

4. **Akses aplikasi**
   - Aplikasi akan berjalan di `https://[repl-name].[username].repl.co`
   - Atau lihat di Webview Replit

### Environment Variables (Sudah Otomatis)
Replit sudah menyediakan environment variables berikut:
- `DATABASE_URL` - Connection string PostgreSQL
- `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`

## 🚂 Deployment ke Railway (Opsional)

Jika Anda ingin deploy ke Railway:

### 1. Persiapan

Buat file `requirements.txt` dari `pyproject.toml`:
```bash
uv pip compile pyproject.toml -o requirements.txt
```

Atau manual:
```txt
streamlit>=1.51.0
plotly>=6.4.0
pandas>=2.0.0
numpy>=1.24.0
reportlab>=4.4.4
Pillow>=10.0.0
sqlalchemy>=2.0.44
psycopg2-binary>=2.9.11
streamlit-extras>=0.7.8
python-dotenv>=1.2.1
```

### 2. Buat file `Procfile`

```
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

Atau gunakan `railway.toml`:

```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"
```

### 3. Setup di Railway

1. Login ke [Railway.app](https://railway.app)
2. Klik "New Project" → "Deploy from GitHub repo"
3. Pilih repository Anda
4. Railway akan auto-detect Python app

### 4. Tambahkan PostgreSQL

1. Di Railway project, klik "New" → "Database" → "PostgreSQL"
2. Railway akan generate `DATABASE_URL` otomatis

### 5. Environment Variables

Railway sudah menyediakan:
- `DATABASE_URL` (dari PostgreSQL addon)
- `PORT` (auto-assigned)

### 6. Deploy

```bash
git add .
git commit -m "Deploy to Railway"
git push
```

Railway akan otomatis deploy aplikasi Anda.

## 📸 Upload Foto Tim

Untuk mengganti avatar placeholder dengan foto asli:

1. Simpan foto anggota tim di folder `attached_assets/team/`
   ```
   attached_assets/
   └── team/
       ├── irbabul.jpg
       ├── furqon.jpg
       ├── rafinda.jpg
       └── kasnanda.jpg
   ```

2. Update file `team_data.py` dengan path foto:
   ```python
   TEAM_MEMBERS = [
       {
           "nama": "Muhammad Irbabul Salas",
           "nim": "25083010055",
           "peran": "Project Manager",
           "initial": "MI",
           "foto": "attached_assets/team/irbabul.jpg"  # Tambahkan ini
       },
       # ... dst
   ]
   ```

3. Update `app.py` di bagian `page_home()` untuk load foto

## 📧 Update Kontak

Edit file `team_data.py` untuk menambahkan email/sosial media:

```python
KONTAK_INFO = {
    "email": "kelompok3@example.com",
    "github": "https://github.com/kelompok3",
    "instagram": "@kelompok3_sistempakar"
}
```

## 🎨 Customization

### Ubah Warna Tema

Edit di `app.py` fungsi `apply_custom_css()`:
```python
# Ganti warna gradient
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Tambah/Edit Pertanyaan

Edit file `kuisioner_data.py`:
```python
KUISIONER = [
    {
        "nomor": 26,
        "pertanyaan": "Pertanyaan baru Anda",
        "kategori": "visual"  # atau "auditori" atau "kinestetik"
    },
    # ...
]
```

### Update Referensi

Edit file `team_data.py`:
```python
REFERENSI = [
    {
        "nomor": 6,
        "teks": "Referensi tambahan Anda dalam format APA"
    }
]
```

## 🧪 Testing

Untuk menguji aplikasi:

1. **Test form validation**: Coba submit form kosong
2. **Test kuisioner**: Navigasi maju-mundur pertanyaan
3. **Test hasil**: Pastikan grafik muncul dengan benar
4. **Test PDF**: Download dan buka PDF hasil
5. **Test database**: Cek riwayat tes tersimpan

## 📚 Referensi Akademik

1. Fleming, N. D., & Mills, C. (1992). Not Another Inventory, Rather a Catalyst for Reflection. To Improve the Academy, 11, 137-155.

2. Gilakjani, A. P. (2012). Visual, Auditory, Kinaesthetic Learning Styles and Their Impacts on English Language Teaching. Journal of Studies in Education, 2(1), 104-113.

3. Dunn, R., & Griggs, S. A. (2003). Synthesis of the Dunn and Dunn Learning Styles Model Research.

4. Kolb, D. A. (1984). Experiential Learning: Experience as the Source of Learning and Development.

5. Pashler, H., McDaniel, M., Rohrer, D., & Bjork, R. (2008). Learning Styles: Concepts and Evidence. Psychological Science in the Public Interest, 9(3), 105-119.

## 🐛 Troubleshooting

### Database Error
```
Error: DATABASE_URL environment variable not found
```
**Solusi**: Pastikan PostgreSQL sudah dibuat di Replit atau Railway

### Port Error
```
Address already in use
```
**Solusi**: Restart workflow atau gunakan port 5000

### Import Error
```
ModuleNotFoundError: No module named 'X'
```
**Solusi**: Jalankan `uv sync` untuk install semua dependencies

## 📝 Lisensi

Proyek ini dibuat untuk keperluan tugas mata kuliah Sistem Pakar.

## 🙏 Acknowledgments

- Dosen Pembimbing Mata Kuliah Sistem Pakar
- Replit untuk platform development
- Streamlit untuk framework yang luar biasa
- Komunitas open-source Python

---

**© 2025 Kelompok 3 - Sistem Deteksi Gaya Belajar Siswa**
