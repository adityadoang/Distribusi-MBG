# Data Mining MBG — Analisis Clustering Prioritas Distribusi

## Deskripsi Proyek
Proyek ini bertujuan untuk melakukan analisis segmentasi atau *clustering* guna menentukan prioritas distribusi program **Makan Bergizi Gratis (MBG)** di seluruh provinsi di Indonesia (38 Provinsi). 

Dengan memanfaatkan algoritma *Machine Learning* **K-Means Clustering**, proyek ini memetakan provinsi-provinsi tersebut ke dalam 3 kategori prioritas (Tinggi, Sedang, dan Rendah) berdasarkan tiga parameter utama:
1. **Prevalensi Balita Stunting** (semakin tinggi tingkat stunting = prioritas semakin tinggi)
2. **Persentase Kemiskinan** (semakin tinggi tingkat kemiskinan = prioritas semakin tinggi)
3. **Ketersediaan Satuan Pelayanan Pendidikan Gizi (SPPG)** eksisting (semakin sedikit jumlah dapur SPPG = prioritas semakin tinggi)

## Sumber Data
Analisis ini memadukan tiga sumber data spasial yang tersimpan di dalam folder `data/`:
1. `vertikalkementerian-2-od_20953_prevalensi_balita_stunting_brdsrkn_prov_di_indones_v1_data.csv`: Prevalensi balita stunting per provinsi berdasarkan survei gizi.sumber : https://opendata.jabarprov.go.id/en/dataset/prevalensi-balita-stunting-berdasarkan-provinsi-di-indonesia 
2. `Persentase Penduduk Miskin (P0) Menurut Kabupaten_Kota, 2025.csv`: Persentase penduduk miskin (P0) tingkat provinsi dari data BPS terbaru. sumber : https://www.bps.go.id/id/statistics-table/2/NjIxIzI=/persentase-penduduk-miskin-menurut-kabupaten-kota.html 
3. `rekap_bgn_sppg.csv`: Data jumlah SPPG/dapur umum operasional program MBG di tiap provinsi. sumber : https://www.bgn.go.id/operasional-sppggit 

## Metodologi dan Alur Kerja
1. **Data Preprocessing & Cleaning:**
   - **Standarisasi Nama Daerah:** Melakukan _string parsing_ untuk menyelaraskan nama ke-38 provinsi (contoh: rekonsiliasi ejaan "Kepulauan Bangka Belitung") agar _merging_ antar-CSV sinkron.
   - **Data Imputation:** Menangani *missing values* (angka 0.0%) pada provinsi hasil pemekaran baru seperti Papua Tengah dan Papua Pegunungan agar tidak terjadi *bias*.
   - **Agregasi Kemiskinan:** Ekstraksi data tingkat kemiskinan secara akurat pada baris agregat level provinsi (bukan sekadar rata-rata kabupaten).

2. **Feature Engineering & Normalisasi:**
   - Semua fitur diskalakan (*scaling*) ke rentang 0-1 menggunakan metode `MinMaxScaler`.
   - Fitur `jumlah_sppg` di-inversikan nilainya (`1 - scaled_value`) sehingga parameter ini sejajar dengan parameter lain dalam memberi bobot (infrastruktur kecil = prioritas besar).

3. **K-Means Clustering:**
   - Model dilatih menggunakan 3 fitur utama dengan jumlah kluster yang ditentukan (K=3).
   - *Labeling* kategori *Prioritas Tinggi*, *Prioritas Sedang*, dan *Prioritas Rendah* diotomatisasi melalui pengurutan rata-rata karakteristik (`total_mean`) per klusternya.

4. **Visualisasi & Output:**
   - Menghasilkan visualisasi *Scatter Plot* interaktif (ukuran gelembung menggambarkan jumlah SPPG), grafik Bar, dan Heatmap.
   - Ekspor data profil setiap kluster menggunakan besaran metrik persentase aslinya ke dalam `hasil_prioritas_mbg.csv`.

## Struktur Direktori
```text
📦 cluster
 ┣ 📂 data
 ┃ ┣ 📜 Persentase Penduduk Miskin (P0) Menurut Kabupaten_Kota, 2025.csv
 ┃ ┣ 📜 rekap_bgn_sppg.csv
 ┃ ┗ 📜 vertikalkementerian-2-od_20953_prevalensi_balita_stunting_brdsrkn_prov_di_indones_v1_data.csv
 ┣ 📜 data_mining_mbg.ipynb   # Notebook utama berisi algoritma K-Means dan EDA
 ┣ 📜 fix.py                  # Script utility (opsional)
 ┣ 📜 hasil_prioritas_mbg.csv # Tabel hasil keluaran (Output)
 ┗ 📜 README.md               # Dokumentasi Proyek
```

## Cara Menjalankan Project
1. Pastikan Anda telah menginstal pustaka Python untuk Data Science:
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn
   ```
2. Buka berkas `data_mining_mbg.ipynb` menggunakan Jupyter Notebook, JupyterLab, atau Visual Studio Code.
3. Lakukan **Run All Cells** (Jalankan semua blok kode dari atas ke bawah).
4. Laporan visualisasi akan tampil di sel terakhir, dan daftar prioritas akhir (beserta datanya) otomatis tercetak dan tersimpan di berkas `hasil_prioritas_mbg.csv`.
