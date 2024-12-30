# Aplikasi Mesin Pencari Dokumen
Aplikasi Mesin Pencari Dokumen berbahasa indonesia dengan metode temu balik VSM.

## Cara Menjalankan Aplikasi
Install semua library yang dibutuhkan dengan perintah
```http
pip install -r requirements.txt
```

#### Menjalankan aplikasi web
Jalankan aplikasi web dengan perintah
```http
uvicorn main:app –reload
```

Buka aplikasi web di alamat berikut
```http
http://127.0.0.1:8000
```

#### Menjalankan API
Jalankan API dengan perintah
```http
uvicorn api:app –reload
```

Buka API documentation di alamat berikut
```http
http://127.0.0.1:8000/docs
```
