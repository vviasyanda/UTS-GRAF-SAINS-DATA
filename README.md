# UTS-GRAF-SAINS-DATA
Tugas UTS Graf Sains Data menggunakan dataset RetailRocket dan Neo4j


## Dataset

Dataset yang digunakan adalah RetailRocket, dengan fokus pada data interaksi pengunjung terhadap produk (events.csv).

Data dibagi menjadi dua periode:
- P1 (training): 21 Mei - 7 Juni 2015
- P2 (testing): 8 - 14 Juni 2015

Pembagian periode menggunakan waktu UTC.

Sumber dataset: https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset


## Isi Repositori

- NO_1_PENDAHULUAN.ipynb - Notebook tugas pendahuluan yang berisi persiapan environment, penggunaan Neo4j Driver, dan proses impor RetailRocket.
- UTS_GRAF_SADA.ipynb - Notebook utama yang berisi filtering dataset, analisis graf, visualisasi, perhitungan similarity, dan rekomendasi produk.
- import_retailrocket.py - Program untuk mengimpor dataset RetailRocket ke Neo4j.
- requirements.txt - Daftar dependensi Python.
- dataset/retailrocket_P1.csv - Dataset training P1.
- dataset/retailrocket_P2.csv - Dataset testing P2.
- graf sada_pertemanan.png - Visualisasi graf pertemanan Arthur menggunakan Neo4j.
- graf_sebelum_similarity.png - Graf sebelum penambahan hubungan similarity.
- graf_sesudah_similarity.png - Graf setelah penambahan hubungan similarity.


## Tahapan Pengerjaan

Pengerjaan UTS menggunakan Python 3.11.9 dengan virtual environment myenv yang dibuat menggunakan modul venv, pengenalan Python Driver Neo4j, pembuatan graf pertemanan, serta proses impor dataset RetailRocket ke Neo4j.

Selanjutnya, data interaksi dibagi menjadi periode training (P1) dan testing (P2). Data yang telah difilter digunakan untuk melihat komposisi subgraf dan membuat Vector Space Modelling (VSM) berdasarkan User dan Item.

Visualisasi graf dilakukan menggunakan NetworkX untuk melihat hubungan antar-node. Berdasarkan perbandingan proyeksi User-User dan Item-Item, dipilih proyeksi Item-Item untuk perhitungan Cosine Similarity.

Perhitungan similarity dilakukan menggunakan Python, kemudian lima nilai similarity tertinggi dari item acuan 5411 disimpan kembali ke Neo4j melalui relasi SIMILAR_TO. Graf sebelum dan sesudah penambahan similarity juga ditampilkan untuk melihat perbedaannya.

Pada tahap analytics, digunakan metode Item-Based KNN dengan `k = 5` untuk membuat rekomendasi produk. Tiga item teratas dipilih sebagai hasil rekomendasi, sedangkan lima rekomendasi teratas digunakan untuk evaluasi dengan metrik Hit@5 dan NDCG@5.


## Hasil Perhitungan Similarity

Perhitungan Cosine Similarity dilakukan menggunakan item 5411 sebagai acuan.

Lima item dengan similarity tertinggi adalah:

| Item | Cosine Similarity |
|---|---|
| 33030 | 0,167833 |
| 33956 | 0,107098 |
| 358234 | 0,080128 |
| 375492 | 0,065424 |
| 89143 | 0,061199 |

Dari hasil tersebut, item 33030 memiliki nilai similarity paling tinggi terhadap item 5411, yaitu 0,167833. Kelima hasil similarity kemudian ditambahkan ke Neo4j sebagai relasi SIMILAR_TO.


## Hasil Evaluasi

Pengujian rekomendasi dilakukan menggunakan metode Item-Based KNN dengan k = 5. User dipilih menggunakan random seed agar proses pemilihannya dapat diulang.

Hasil akhir pemilihan user, tiga item rekomendasi, serta nilai Hit@5 dan NDCG@5 dapat dilihat pada notebook UTS_GRAF_SADA.ipynb.

Evaluasi dilakukan dengan membandingkan lima rekomendasi teratas berdasarkan data training P1 dengan item yang diakses user pada periode testing P2. Hasil pengujian ini digunakan untuk melihat apakah rekomendasi yang dihasilkan sesuai dengan aktivitas user pada periode testing.
