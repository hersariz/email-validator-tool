
---
**📝 Tujuan:**

Saya ingin kamu membantuku membangun sebuah **Email Validator Tool** berbasis Python, yang bisa digunakan oleh tim sales atau growth untuk mengecek dan memvalidasi daftar email yang mereka dapatkan dari hasil scraping atau lead list. Tools ini akan digunakan untuk **meningkatkan akurasi data, menghindari email bounce**, dan **mengelompokkan jenis email** (personal vs bisnis), agar outreach lebih efektif dan efisien.

---

**📖 Latar Belakang Proyek:**

Saya sedang mengikuti seleksi program internship di Caprae Capital, sebuah perusahaan investasi dan akuisisi yang mengedepankan transformasi bisnis melalui AI dan teknologi. Salah satu tantangan pre-screening mereka adalah membuat sebuah alat yang bisa meningkatkan efektivitas proses lead generation dalam waktu maksimal 5 jam.

Setelah mempelajari model bisnis mereka (menggunakan alat seperti [SaaSquatchLeads](https://www.saasquatchleads.com/)), saya menyadari bahwa banyak data hasil scraping yang berisi email tidak valid, tidak aktif, atau bersifat sementara (disposable). Hal ini bisa mengganggu efektivitas outreach email dan menurunkan reputasi pengirim.

---

**🧩 Permintaan Teknis:**

Buatkan saya **sebuah aplikasi sederhana berbasis Streamlit** (jika memungkinkan) atau minimal Python CLI tool, yang memiliki fitur-fitur berikut:

---

### 🔍 Fitur Utama:

1. **Email Format Validation**

   * Periksa apakah format email valid (`abc@domain.com`) menggunakan regex.

2. **Domain Availability Check**

   * Cek apakah domain email (`domain.com`) masih aktif dan valid.

3. **MX Record Check**

   * Gunakan DNS lookup untuk mengecek apakah domain dapat menerima email (MX record tersedia).

4. **Disposable Email Detection**

   * Deteksi apakah domain berasal dari layanan email sementara (seperti `tempmail.com`, `10minutemail.com`, dll).

5. **Categorization: Personal vs Business Email**

   * Tandai email dengan domain umum (gmail, yahoo, hotmail) sebagai **personal**, dan domain perusahaan sebagai **business**.

6. **Input File: CSV**

   * File CSV yang berisi kolom `email`.

7. **Output:**

   * Tampilkan hasilnya dalam tabel dan beri opsi untuk mengunduh hasil sebagai file CSV.

8. **Optional Bonus (jika waktu cukup):**

   * Tambahkan *confidence score* atau tanda peringkat kualitas email (high, medium, low).
   * Integrasi ke API email validation (misalnya Hunter.io atau AbstractAPI).

---

**📂 Struktur File yang Diinginkan:**

```
email_validator/
├── app.py                 # Main streamlit app
├── validator.py           # Semua fungsi verifikasi email
├── utils.py               # Fungsi tambahan (misalnya: deteksi disposable)
├── requirements.txt       # Streamlit, dnspython, pandas, dll
├── sample_emails.csv      # Contoh input
└── README.md              # Penjelasan cara menjalankan
```

---

**💬 Output Harapan:**

* Kode yang bersih, reusable, dan terdokumentasi
* File Streamlit atau CLI yang bisa langsung dipakai
* File CSV hasil validasi (email + status + tipe + validasi lainnya)
* Bonus: draft 1-page pendek menjelaskan tool ini & fungsinya (jika sempat)

---

**🧠 Goal Bisnis dari Tools Ini:**

* Mengurangi bounce rate
* Meningkatkan targeting email outreach
* Menyaring lead buruk sejak awal
* Memberikan insight siapa yang lebih layak dikontak oleh tim sales

---