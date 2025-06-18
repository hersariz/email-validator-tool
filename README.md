# Email Validator Tool

Aplikasi berbasis Python untuk memvalidasi daftar email secara akurat dan komprehensif menggunakan AbstractAPI.

## 📝 Tujuan

Email Validator Tool membantu:
- Meningkatkan akurasi data email
- Menghindari email bounce
- Mengelompokkan jenis email (personal vs business)
- Mendeteksi email disposable/sementara
- Memberikan visualisasi hasil validasi untuk analisis yang lebih baik

## 🔍 Fitur Utama

1. **Email Validation dengan AbstractAPI**
   - Validasi format email
   - Pengecekan domain dan MX record
   - Deteksi email disposable, role, dan catchall
   - Skor kualitas dan status deliverability
   - SMTP validation untuk memastikan email benar-benar valid

2. **Dashboard Analisis**
   - Grafik distribusi deliverability status
   - Grafik perbandingan personal vs business email
   - Visualisasi parameter validasi
   - Distribusi quality score
   - Indikator performa real-time

3. **Detail Validasi Komprehensif**
   - Penampilan hasil validasi dalam format yang mudah dibaca
   - Visual gauge untuk quality score
   - Penjelasan detail setiap parameter validasi
   - Tooltip informatif untuk setiap indikator

4. **Input Fleksibel**
   - Upload file CSV
   - Input manual
   - Dukungan untuk data historis

5. **Output Lengkap**
   - Tabel hasil yang informatif dengan ikon status (✅/❌)
   - Tampilan detail per email
   - Download hasil sebagai CSV
   - Opsi penyaringan hasil berdasarkan status validasi

6. **Visualisasi Interaktif**
   - Grafik Plotly interaktif
   - Filter data langsung dari visualisasi
   - Ekspor grafik sebagai gambar

7. **Autocorrect Suggestion**
   - Saran koreksi email yang terdeteksi typo
   - Opsi untuk menerapkan koreksi otomatis

## 🛠️ Teknologi yang Digunakan

- **Streamlit**: Framework untuk UI
- **Pandas**: Manipulasi data
- **AbstractAPI**: API validasi email
- **Plotly**: Visualisasi data interaktif
- **DNSPython**: Validasi tambahan untuk DNS

## 🚀 Cara Menjalankan

### Prasyarat

- Python 3.7 atau yang lebih baru
- Pip (Python package manager)

### Instalasi dengan Virtual Environment

1. Clone repositori ini:
   ```
   git clone https://github.com/hersariz/email-validator-tool.git
   cd email-validator-tool
   ```

2. Buat virtual environment:
   ```
   python -m venv venv
   ```

3. Aktifkan virtual environment:
   - Di Windows:
     ```
     .\venv\Scripts\activate
     ```
   - Di macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Menjalankan Aplikasi

1. Pastikan virtual environment sudah aktif
   
2. Jalankan aplikasi Streamlit:
   ```
   streamlit run app.py
   ```

3. Buka browser dan akses:
   ```
   http://localhost:8501
   ```

4. Setelah selesai, nonaktifkan virtual environment:
   ```
   deactivate
   ```

## 📂 Struktur File

```
email-validator-tool/
├── app.py                 # Main streamlit app dengan visualisasi
├── validator.py           # Integrasi dengan AbstractAPI
├── utils.py               # Fungsi tambahan (kategorisasi email, dll)
├── requirements.txt       # Dependencies
├── sample_emails.csv      # Contoh input
└── README.md              # Dokumentasi
```

## 📝 Cara Penggunaan

### Metode 1: Upload CSV
1. Siapkan file CSV dengan kolom 'email'
2. Upload file melalui UI
3. Klik tombol "Validasi Email"
4. Lihat hasil validasi di Dashboard, Tabel, dan Detail
5. Download hasil sebagai CSV

### Metode 2: Input Manual
1. Masukkan daftar email (satu per baris) di tab "Input Manual"
2. Klik tombol "Validasi Email"
3. Lihat hasil validasi di Dashboard, Tabel, dan Detail
4. Download hasil sebagai CSV

## 💡 Manfaat Bisnis

- **Efisiensi**: Otomatisasi proses validasi email yang biasanya memakan waktu
- **Akurasi**: Mengurangi bounce rate dengan memfilter email tidak valid
- **Targeting**: Pengelompokan email personal/business untuk strategi outreach yang tepat
- **Cost-Saving**: Mengurangi biaya pengiriman email ke alamat tidak valid
- **Analisis Data**: Visualisasi untuk memahami kualitas data email dengan lebih baik
- **Reputation**: Menjaga reputasi pengirim email dengan menghindari alamat bermasalah
- **Decision Support**: Bantu pengambilan keputusan dengan insights berbasis data

## ⚠️ Batasan

- Validasi menggunakan AbstractAPI memerlukan koneksi internet
- AbstractAPI memiliki batasan jumlah request per bulan
- Domain atau server email tertentu mungkin memblokir validasi SMTP
