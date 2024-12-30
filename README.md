# Aplikasi Mesin Pencari Dokumen
Aplikasi Mesin Pencari Dokumen berbahasa indonesia dengan metode temu balik VSM.

## Cara Menjalankan Aplikasi
Install semua library yang dibutuhkan dengan perintah
```bash
pip install -r requirements.txt
```

#### Menjalankan aplikasi web
Jalankan aplikasi web dengan perintah
```bash
uvicorn main:app –reload
```

Buka aplikasi web di alamat berikut
```bash
http://127.0.0.1:8000
```

#### Menjalankan API
Jalankan API dengan perintah
```bash
uvicorn api:app –reload
```

Buka API documentation di alamat berikut
```bash
http://127.0.0.1:8000/docs
```
