# COBIT Audit Tool

Aplikasi Desktop modern berbasis Python dan CustomTkinter untuk mempermudah proses audit tata kelola IT akademik maupun profesional menggunakan kerangka kerja **COBIT 5** dan **COBIT 2019** serta model asesmen kapabilitas standar **ISO/IEC 15504 (Process Assessment Model)**.

---

## Fitur Utama

1. **Dashboard Multi-Audit**: Kelola dan simpan beberapa proyek audit organisasi dalam satu tempat dengan pemantauan progress otomatis.
2. **Goal Cascade Helper**: Panduan langkah demi langkah memetakan *Enterprise Goals* ke *Alignment Goals* dan proses tata kelola/manajemen terkait secara otomatis dengan penanda relasi *Primary* dan *Secondary*.
3. **RACI Chart & Pemetaan Jabatan**: Visualisasi matriks tanggung jawab (R/A/C/I) dengan color coding dan tabel pemetaan peran COBIT ke jabatan nyata di organisasi klien.
4. **Asesmen Kapabilitas ISO/IEC 15504**: Kuesioner atribut proses (PA 1.1 hingga PA 5.2) dengan skala rating resmi N (0-15%), P (15-50%), L (50-85%), dan F (85-100%). Dilengkapi mekanisme auto-lock level sesuai aturan hierarki standar.
5. **Analisis Gap & Pencatatan Temuan**: Rekapitulasi otomatis gap antara level aktual dan target, serta form pencatatan temuan terstruktur 5 elemen (Kondisi, Kriteria, Sebab, Dampak/Prioritas, Rekomendasi).
6. **Visualisasi Radar & Bar Chart**: Grafik perbandingan kapabilitas per domain (EDM, APO, BAI, DSS, MEA) serta diagram batang aktual vs target yang disematkan langsung di dalam aplikasi.
7. **Ekspor Laporan Resmi ke PDF**: Generate laporan audit lengkap berformat A4 dengan tata letak profesional, tabel penilaian, grafik visual tersemat, dan ringkasan temuan siap cetak.
8. **Kompilasi Standalone .exe**: Dapat dikompilasi menjadi aplikasi Windows `.exe` mandiri tanpa perlu instalasi Python di komputer target.

---

## Panduan Instalasi & Penggunaan

### 1. Prasyarat
- Python 3.10 atau versi lebih baru.

### 2. Instalasi Dependencies
Buka terminal/PowerShell di direktori `cobit-audit-tool/`:
```bash
pip install -r requirements.txt
```

### 3. Menjalankan Aplikasi
```bash
python main.py
```

### 4. Menjalankan Unit Test
Untuk memverifikasi kebenaran logika seluruh modul:
```bash
python -m pytest tests -v
```

### 5. Kompilasi ke Windows Executable (.exe)
Jalankan script build bawaan:
```bash
python build_exe.py
```
File aplikasi siap pakai akan terbentuk di direktori `dist/COBIT-Audit-Tool/COBIT-Audit-Tool.exe`.
