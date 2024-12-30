import pandas as pd
from pypdf import PdfReader
from docx import Document
import re
import os
import math

# Membaca stopwords dari file CSV (misalnya hanya satu kolom tanpa header)
stopwords_df = pd.read_csv("stopwordbahasa.csv", header=None)
stopwords = set(stopwords_df[0].tolist())  # Mengonversi kolom pertama ke dalam set

#fungsi untuk mereturn semua file yang ada di dalam suatu directory
def cekDirectoryPath(path):
    # Memeriksa apakah path yang diberikan adalah sebuah file
    if os.path.isfile(path):
        # Melempar error jika path adalah file
        raise ValueError("Jangan input path file")
    # Memeriksa apakah path yang diberikan adalah sebuah directory
    elif os.path.isdir(path):
        # Membuat list semua file di dalam directory dengan menggunakan list comprehension
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        # Mengembalikan daftar file jika ada, atau pesan "Directory kosong" jika tidak ada file
        return files if files else "Directory kosong"
    else:
        # Melempar error jika path tidak ditemukan
        raise ValueError("Path directory invalid atau tidak ditemukan")

#fungsi untuk memfilter dokumen txt, pdf, dan docx dan mendapatkan informasi path, nama, dan ekstensi dari masing-masing dokumen tersebut dalam suatu directory    
def returnFileInfo(path):
    # Memeriksa apakah path yang diberikan adalah sebuah directory
    if not os.path.isdir(path):
        # Melempar error jika path bukan directory
        raise ValueError("Path directory tidak ada atau bukan directory")
    # Menentukan ekstensi file yang diperbolehkan untuk dimasukkan dalam hasil
    allowed_extensions = {".txt", ".pdf", ".docx"}
    result = []
    # Melakukan iterasi untuk setiap item dalam directory
    for f in os.listdir(path):
        # Membangun full path dari item yang ditemukan di directory
        full_path = os.path.join(path, f)
        # Memeriksa apakah item tersebut adalah file
        if os.path.isfile(full_path):
            # Memisahkan nama file dan ekstensi file menggunakan os.path.splitext
            name, ext = os.path.splitext(f)
            # Memeriksa apakah ekstensi file termasuk dalam daftar yang diizinkan
            if ext in allowed_extensions:
                # Menambahkan informasi file ke dalam list hasil jika ekstensi file sesuai dengan yang diizinkan
                result.append({"path": full_path, "nama": name + ext, "ekstensi": ext})
    # Mengembalikan hasil jika terdapat file yang sesuai, atau pesan jika tidak ada file yang ditemukan
    return result if result else "Tidak ada file txt/pdf/docx dalam directory ini"

#fungsi untuk mereturn isi file .txt
def returnIsiTXT(file_path):
    #membuka file txt dengan mode read
    txt = open(file_path, "r")
    return txt.read()

#fungsi untuk mereturn isi file .pdf
def returnIsiPDF(file_path):
    #membuka file pdf
    pdf = PdfReader(file_path)
    #penampung isi pdf
    isi_pdf = ""

    #melakukan iterasi setiap halaman pdf
    for i, page in enumerate(pdf.pages):
        #masukkan seluruh teks di pdf ke variabel isi_pdf
        isi_pdf += page.extract_text()

    return isi_pdf

#fungsi untuk mereturn isi file .docx
def returnIsiDOCX(file_path):
    #membuka file docs
    doc = Document(file_path)
    #penampung isi docx
    isi_docx = ""

    #print teks dari setiap paragraf
    for i, paragraph in enumerate(doc.paragraphs):
        #masukkan seluruh teks di pdf ke variabel isi_docx
        isi_docx += paragraph.text

    return isi_docx

#fungsi untuk mendapatkan isi dari semua dokumen txt, pdf, dan docx dalam suatu directory
def bacaIsiDokumen(dir_path):
    #cek dulu apakah directory path valid apa tidak, jika tidak valid maka akan raise ValueError
    cekDirectoryPath(dir_path)

    #list penampung dictionary yang berisikan informasi path, nama, dan ekstensi dari masing-masing dokumen
    list_dokumen = []

    #jika returnFileInfo(dir_path) tidak mereturn sebuah string
    if not (type(returnFileInfo(dir_path)) == str):
        #dapatkan list dictionary yang berisi informasi path, nama, dan ekstensi dari masing-masing dokumen (txt, pdf, dan docx) dalam directory tersebut
        list_dokumen = returnFileInfo(dir_path)
    #jika returnFileInfo(dir_path) mereturn sebuah string
    else:
        #dapatkan string tersebut dan raise ValueError dengan string tersebut sebagai error message
        raise ValueError(returnFileInfo(dir_path))
    #kini listdokumen berbentuk [{"path": "", "nama": "", "ekstensi": ""}]

    #baca setiap dictionary dokumen
    for dokumen in list_dokumen:
        #jika ekstensi dokumen adalah .txt
        if dokumen["ekstensi"] == ".txt":
            #dapatkan isi dokumen.txt tersebut dalam bentuk string menggunakan fungsi returnIsiTXT() kemudian masukkan ke dalam key baru bernama konten
            dokumen["konten"] = returnIsiTXT(dokumen["path"])
        #jika ekstensi dokumen adalah .pdf
        if dokumen["ekstensi"] == ".pdf":
            #dapatkan isi dokumen.pdf tersebut dalam bentuk string menggunakan fungsi returnIsiPDF() kemudian masukkan ke dalam key baru bernama konten
            dokumen["konten"] = returnIsiPDF(dokumen["path"])
        #jika ekstensi dokumen adalah .docx
        if dokumen["ekstensi"] == ".docx":
            #dapatkan isi dokumen.docx tersebut dalam bentuk string menggunakan fungsi returnIsiDOCX() kemudian masukkan ke dalam key baru bernama konten
            dokumen["konten"] = returnIsiDOCX(dokumen["path"])

    #kini list_dokumen berbentuk [{"path": "", "nama": "", "ekstensi": "", "konten": ""}]
    return list_dokumen

#fungsi untuk menghilangkan semua tanda baca dan angka dari sebuah string
def hilangkanTandaBaca(sebuah_string):
    # Menghapus semua karakter yang bukan huruf, spasi, atau strip
    hasil = re.sub(r"[^a-zA-Z\s-]", "", sebuah_string)
    # Menghapus strip yang diapit oleh dua spasi
    hasil = re.sub(r"\s-\s", " ", hasil)
    #return string yang hanya terdiri dari huruf, spasi, dan strip (-) untuk kata yang berulang
    return hasil

#fungsi untuk menghapus whitespaces dan mendapatkan masing-masing katanya
def stringTokenizer(sebuah_string):
    #split string berdasarkan whitespaces
    list_kata = sebuah_string.split()

    #hapus string kosong dari list_kata
    while("" in list_kata):
        list_kata.remove("")

    #return list kata yang sudah dibersihkan dari string kosong
    return list_kata

#fungsi untuk membuang stopword dari list kata
def pisahkanKataPenting(list_kata):
    #list untuk menampung kata-kata penting
    list_kata_penting = []
    #untuk pengecekan stopword atau bukan
    apakah_stopword = False

    #baca setiap kata dalam list_kata
    for kata in list_kata:
        #lakukan iterasi setiap stopword pada list stopwords
        for stopword in stopwords:
            #jika kata yang dibaca adalah stopword
            if kata.lower() == stopword.lower():
                #ubah apakah_stopword menjadi True
                apakah_stopword = True
        #jika kata yang dibaca bukan stopword
        if apakah_stopword == False:
            #masukkan kata tersebut ke list_kata_penting
            list_kata_penting.append(kata.lower())
        #jika kata yang dibaca adalah stopword
        else:
            #kembalikan nilai apakah_stopword menjadi False lagi
            apakah_stopword = False
    #return list_kata_penting
    return list_kata_penting

#fungsi untuk membaca kamus kata dasar dari file dan mengonversinya menjadi set
def konversiKamusTXTMenjadiSet(file_path):
    #buka file dengan mode readmode
    with open(file_path, "r") as file:
        #masukkan setiap kata perbarisnya dari file kamus ke dalam set kamus
        kamus = set(line.strip() for line in file)
    #return set kamus
    return kamus

#fungsi untuk menghapus imbuhan awalan
def hapusImbuhanAwalan(kata, set_kamus):
    awalan = ["ber", "be", "di", "ke", "meng", "meny", "mem", "men", "me", "peng", "peny", "pem", "pen", "per", "pe", "se", "ter", "te"]
    #set kamus
    kamus = set_kamus

    #baca setiap awalan kata dari list awalan
    for a in awalan:
        #jika kata berawalan awalan kata yang sedang dibaca
        if kata.startswith(a):
            #hapus awalan kata dari kata tersebut
            kata_dasar = kata[len(a):]
            #jika kata yang sudah dihapus awalannya tersebut ada di kamus
            if kata_dasar in kamus:
                #return kata tersebut
                return kata_dasar
            
    #baca setiap awalan dari list awalan
    for a in awalan:
        #jika kata berawalan kata yang sedang dibaca
        if kata.startswith(a):
            #hapus awalan kata dari kata tersebut kemudian return kata tersebut
            return kata[len(a):]
    #return apa adanya
    return kata

#fungsi untuk menghapus imbuhan akhiran
def hapusImbuhanAkhiran(kata, set_kamus):
    akhiran = ["i", "kan", "an"]
    #set kamus
    kamus = set_kamus

    #baca setiap akhiran kata dari list akhiran
    for a in akhiran:
        #jika kata berakhiran akhiran kata yang sedang dibaca
        if kata.endswith(a):
            #hapus akhiran kata dari kata tersebut
            kata_dasar = kata[:-len(a)]
            #jika kata yang sudah dihapus akhirannya tersebut ada di kamus
            if kata_dasar in kamus:
                #return kata tersebut
                return kata_dasar

    #baca setiap akhiran kata dari list akhiran
    for a in akhiran:
        #jika kata berakhiran akhiran kata yang sedang dibaca
        if kata.endswith(a):
            #hapus akhiran kata dari kata tersebut kemudian return kata tersebut
            return kata[:-len(a)]
    #return apa adanya
    return kata

#fungsi untuk menghapus partikel
def hapusPartikel(kata):
    partikel = ["lah", "kah", "ku", "mu", "nya"]
    #baca setiap partikel dari list partikel
    for p in partikel:
        #jika kata berakhiran partikel yang sedang dibaca
        if kata.endswith(p):
            #hapus partikel dari kata tersebut kemudian return kata tersebut
            return kata[:-len(p)]
    #return apa adanya
    return kata

#fungsi utama algoritma stemming sastrawi dengan beberapa perubahan
def stemmingSebuahKata(kata):
    #set kamus
    kamus = konversiKamusTXTMenjadiSet("kamus.txt")

    #jika kata adalah kata perulangan atau reduplikasi
    if "-" in kata:
        #ambil kata awal sebelum strip (-)
        kata = kata.split("-")[0]
        #jika kata awal ada di kamus
        if kata in kamus:
            #return kata dasar
            return kata

    #jika kata yang belum diproses ada di kamus
    if kata in kamus:
        #return kata dasar
        return kata

    #hapus imbuhan awalan
    kata_dasar = hapusImbuhanAwalan(kata, kamus)

    #jika kata yang sudah dihilangkan awalannya masih saja tidak ada di kamus
    if not (kata_dasar in kamus):
        #jika imbuhan awalan kata adalah "peny" atau "meny"
        if ("peny" in kata) or ("meny" in kata):
            #biasanya diawali dengan huruf "s"
            huruf_awal_lebur = "s"
            #gabungkan huruf "s" dengan kata tersebut
            huruf_plus_kata = f"{huruf_awal_lebur}{kata_dasar}"
            #jika kata yang sudah dengan huruf tersebut ada di kamus
            if huruf_plus_kata in kamus:
                #return kata tersebut
                return huruf_plus_kata
        #jika imbuhan awalan kata adalah "peng" atau "meng"
        elif ("peng" in kata) or ("meng" in kata):
            #biasanya diawali dengan huruf "k"
            huruf_awal_lebur = "k"
            #gabungkan huruf "k" dengan kata tersebut
            huruf_plus_kata = f"{huruf_awal_lebur}{kata_dasar}"
            #jika kata yang sudah dengan huruf tersebut ada di kamus
            if huruf_plus_kata in kamus:
                #return kata tersebut
                return huruf_plus_kata
        #jika imbuhan awalan kata adalah "men" atau "pen"
        elif ("men" in kata) or ("pen" in kata):
            #biasanya diawali dengan huruf "t"
            huruf_awal_lebur = "t"
            #gabungkan huruf "t" dengan kata tersebut
            huruf_plus_kata = f"{huruf_awal_lebur}{kata_dasar}"
            #jika kata yang sudah dengan huruf tersebut ada di kamus
            if huruf_plus_kata in kamus:
                #return kata tersebut
                return huruf_plus_kata
        #jika imbuhan awalan kata bukan "peny", "meny", "peng", "meng", atau "men"
        else:
            #biasanya diawali oleh satu dari huruf k/p/s/t
            huruf_awal_lebur = ["k", "p", "s", "t"]

            #coba satu-satu huruf tersebut
            for huruf in huruf_awal_lebur:
                #gabungkan huruf dengan kata tersebut
                huruf_plus_kata = f"{huruf}{kata_dasar}"
                #jika kata yang sudah dengan huruf tersebut ada di kamus
                if huruf_plus_kata in kamus:
                    #return kata tersebut
                    return huruf_plus_kata

    #hapus partikel
    kata_dasar = hapusPartikel(kata_dasar)
    #jika kata yang sudah dihapus partikelnya ada di kamus
    if kata_dasar in kamus:
        #return kata dasar
        return kata_dasar

    #hapus imbuhan akhiran
    kata_dasar = hapusImbuhanAkhiran(kata_dasar, kamus)
    
    #jika kata yang sudah dihilangkan imbuhan dan partikelnya masih saja tidak ada di kamus
    if not (kata_dasar in kamus):
        #jika imbuhan awalan kata adalah "peny" atau "meny"
        if ("peny" in kata) or ("meny" in kata):
            #biasanya diawali dengan huruf "s"
            huruf_awal_lebur = "s"
            #gabungkan huruf "s" dengan kata tersebut
            huruf_plus_kata = f"{huruf_awal_lebur}{kata_dasar}"
            #jika kata yang sudah dengan huruf tersebut ada di kamus
            if huruf_plus_kata in kamus:
                #return kata tersebut
                return huruf_plus_kata
        #jika imbuhan awalan kata adalah "peng" atau "meng"
        elif ("peng" in kata) or ("meng" in kata):
            #biasanya diawali dengan huruf "k"
            huruf_awal_lebur = "k"
            #gabungkan huruf "k" dengan kata tersebut
            huruf_plus_kata = f"{huruf_awal_lebur}{kata_dasar}"
            #jika kata yang sudah dengan huruf tersebut ada di kamus
            if huruf_plus_kata in kamus:
                #return kata tersebut
                return huruf_plus_kata
        #jika imbuhan awalan kata adalah "men" atau "pen"
        elif ("men" in kata) or ("pen" in kata):
            #biasanya diawali dengan huruf "t"
            huruf_awal_lebur = "t"
            #gabungkan huruf "t" dengan kata tersebut
            huruf_plus_kata = f"{huruf_awal_lebur}{kata_dasar}"
            #jika kata yang sudah dengan huruf tersebut ada di kamus
            if huruf_plus_kata in kamus:
                #return kata tersebut
                return huruf_plus_kata
        #jika imbuhan awalan kata bukan "peny", "meny", "peng", "meng", atau "men"
        else:
            #biasanya diawali oleh satu dari huruf k/p/s/t
            huruf_awal_lebur = ["k", "p", "s", "t"]

            #coba satu-satu huruf tersebut
            for huruf in huruf_awal_lebur:
                #gabungkan huruf dengan kata tersebut
                huruf_plus_kata = f"{huruf}{kata_dasar}"
                #jika kata yang sudah dengan huruf tersebut ada di kamus
                if huruf_plus_kata in kamus:
                    #return kata tersebut
                    return huruf_plus_kata

    #jika tidak berhasil, kembalikan kata tersebut apa adanya
    return kata_dasar

#fungsi untuk membuat list hasil stemming
def buatListHasilStemming(list_kata):
    #list untuk menampung hasil stemming
    hasil_stemming = []

    #baca setiap kata dalam list
    for kata in list_kata:
        #masukkan hasil stemming kedalam list
        hasil_stemming.append({kata: stemmingSebuahKata(kata)})

    #return list
    return hasil_stemming

#fungsi untuk membuat dictionary hasil stemming
def buatDictHasilStemming(list_kata):
    #dictionary untuk menampung hasil stemming dengan format "kata_awal": "kata_dasar"
    hasil_stemming = {}

    #baca setiap kata dalam list
    for kata in list_kata:
        #masukkan kedalam dictionary dengan kata awal sebagai key dan kata dasar hasil stemming sebagai value
        hasil_stemming[kata] = stemmingSebuahKata(kata)

    #return dictionary
    return hasil_stemming

#fungsi untuk memproses query
def prosesQuery(query):
    #query pada awalnya hanya berupa string berisikan query
    #hilangankan tanda baca dari query menggunakan fungsi hilangkanTandaBaca() sehingga menyisakan huruf, whitespaces, dan strip (-) untuk kata yang berulang seperti "berkali-kali"
    #query yang sudah bersih dari tanda baca kemudian dimasukkan setiap katanya ke dalam list menggunakan fungsi stringTokenizer()
    #stringTokenizer() mengembalikan list berisi kata-kata, buang kata-kata yang tidak penting dari list menggunakan fungsi pisahkanKataPenting()
    #list yang berisi hanya kata-kata penting distem menggunakan fungsi buatListHasilStemming()
    #buatListHasilStemming() akan mengembalikan list berformat [{"kata_asal": "kata_dasar"}]
    #masukkan list yang dikembalikan oleh fungsi buatListHasilStemming() ke variabel hasil_stemming_query
    hasil_stemming_query = buatListHasilStemming(pisahkanKataPenting(stringTokenizer(hilangkanTandaBaca(query))))
    #buat query dictionary {"query": query}
    query_dict = {"query": query}
    #kemudian masukkan hasil_stemming_query ke query_dict["hasil_stemming"]
    query_dict["hasil_stemming"] = hasil_stemming_query
    #kini query_dict menjadi {"query": query, "hasil_stemming": [{"kata_asal": "kata_dasar"}]}

    #dapatkan total kata-kata yang distem dengan menghitung panjang list query_dict["hasil_stemming"]
    #masukkan nilai totalnya ke query_dict["total_stemming"]
    query_dict["total_stemming"] = len(query_dict["hasil_stemming"])
    #kini query_dict menjadi {"query": query, "hasil_stemming": [{"kata_asal": "kata_dasar"}], "total_stemming": int}

    #dicionary untuk menampung kata dasar beserta jumlahnya
    jumlah_kata_dasar = {}
    #iterasikan setiap elemen list query_dict["hasil_stemming"]
    for elemen in query_dict["hasil_stemming"]:
        #baca kata dasar dari setiap elemen
        for kata_asal, kata_dasar in elemen.items():
            #jika kata dasar sudah ada di dictionary jumlah_kata_dasar
            if kata_dasar in jumlah_kata_dasar:
                #tambahkan jumlahnya dengan 1
                jumlah_kata_dasar[kata_dasar] += 1
            #jika kata dasar belum ada di dictionary jumlah_kata_dasar
            else:
                #jadikan kata dasar tersebut sebagai key dan isi valuenya dengan 1
                jumlah_kata_dasar[kata_dasar] = 1

    #masukkan dictionary jumlah_kata_dasar ke query_dict["jumlah_kata_dasar"]
    query_dict["jumlah_kata_dasar"] = jumlah_kata_dasar
    #kini query_dict menjadi {"query": query, "hasil_stemming": [{"kata_asal": "kata_dasar"}], "total_stemming": int, "jumlah_kata_dasar": {"kata_dasar": int}}

    #dapatkan banyaknya masing-masing kata dasar dengan menghitung panjang dictionary query_dict["jumlah_kata_dasar"]
    #masukkan nilai totalnya ke query_dict["total_kata_dasar"]
    query_dict["total_kata_dasar"] = len(query_dict["jumlah_kata_dasar"])
    #kini query_dict menjadi {"query": query, "hasil_stemming": [{"kata_asal": "kata_dasar"}], "total_stemming": int, "jumlah_kata_dasar": {"kata_dasar": int}, "total_kata_dasar": int}

    #kembalikan query_dict yang berbentuk {"query": query, "hasil_stemming": [{"kata_asal": "kata_dasar"}], "total_stemming": int, "jumlah_kata_dasar": {"kata_dasar": int}, "total_kata_dasar": int}
    return query_dict

#fungsi untuk menghitung similarity menggunakan metode VSM
def temuBalikVSM(list_dokumen, query_dict):
    #list_dokumen pada awalnya berbentuk [{"path": "", "nama": "", "ekstensi": "", "konten": ""}]
    #seluruh proses nanti menggunakan seluruh_dokumen daripada menggunakan list_dokumen secara langsung
    seluruh_dokumen = list_dokumen

    #iterasikan setiap dictionary dokumen yang ada di dalam list seluruh_dokumen
    for dokumen in seluruh_dokumen:
        #dokumen["konten"] masih berisi konten utuh dari suatu dokumen
        #hilangankan tanda baca dari konten menggunakan fungsi hilangkanTandaBaca() sehingga menyisakan huruf, whitespaces, dan strip (-) untuk kata yang berulang seperti "berkali-kali"
        #konten yang sudah bersih dari tanda baca kemudian dimasukkan setiap katanya ke dalam list menggunakan fungsi stringTokenizer()
        #stringTokenizer() mengembalikan list berisi kata-kata, buang kata-kata yang tidak penting dari list menggunakan fungsi pisahkanKataPenting()
        #list yang berisi hanya kata-kata penting distem menggunakan fungsi buatListHasilStemming()
        #buatListHasilStemming() akan mengembalikan list berformat [{"kata_asal": "kata_dasar"}]
        #masukkan list yang dikembalikan oleh fungsi buatListHasilStemming() ke dalam dokumen["hasil_stemming"]
        dokumen["hasil_stemming"] = buatListHasilStemming(pisahkanKataPenting(stringTokenizer(hilangkanTandaBaca(dokumen["konten"]))))
        #kini dokumen berbentuk {"path": "", "nama": "", "ekstensi": "", "konten": "", "hasil_stemming": [{"kata_asal": "kata_dasar"}]}
        #dapatkan total kata-kata yang distem dengan menghitung panjang list dokumen["hasil_stemming"]
        #masukkan nilai totalnya ke dokumen["total_stemming"]
        dokumen["total_stemming"] = len(dokumen["hasil_stemming"])
        #kini dokumen berbentuk {"path": "", "nama": "", "ekstensi": "", "konten": "", "hasil_stemming": [{"kata_asal": "kata_dasar"}], "total_stemming": int}
        
        #dicionary untuk menampung kata dasar beserta jumlahnya
        jumlah_kata_dasar = {}
        #iterasikan setiap elemen list dokumen["hasil_stemming"]
        for elemen in dokumen["hasil_stemming"]:
            #baca kata dasar dari setiap elemen
            for kata_asal, kata_dasar in elemen.items():
                #jika kata dasar sudah ada di dictionary jumlah_kata_dasar
                if kata_dasar in jumlah_kata_dasar:
                    #tambahkan jumlahnya dengan 1
                    jumlah_kata_dasar[kata_dasar] += 1
                #jika kata dasar belum ada di dictionary jumlah_kata_dasar
                else:
                    #jadikan kata dasar tersebut sebagai key dan isi valuenya dengan 1
                    jumlah_kata_dasar[kata_dasar] = 1
        #masukkan dictionary jumlah_kata_dasar ke dokumen["jumlah_kata_dasar"]
        dokumen["jumlah_kata_dasar"] = jumlah_kata_dasar
        #kini dokumen berbentuk {"path": "", "nama": "", "ekstensi": "", "konten": "", "hasil_stemming": [{"kata_asal": "kata_dasar"}], "total_stemming": int, "jumlah_kata_dasar": {"kata_dasar": int}}
        
        #dapatkan banyaknya masing-masing kata dasar dengan menghitung panjang dictionary dokumen["jumlah_kata_dasar"]
        #masukkan nilai totalnya ke dokumen["total_kata_dasar"]
        dokumen["total_kata_dasar"] = len(dokumen["jumlah_kata_dasar"])
        #kini dokumen berbentuk {"path": "", "nama": "", "ekstensi": "", "konten": "", "hasil_stemming": [{"kata_asal": "kata_dasar"}], "total_stemming": int, "jumlah_kata_dasar": {"kata_dasar": int}, "total_kata_dasar": int}

        #dictionary untuk menampung kata dasar yang sama dengan kata dasar di query beserta jumlahnya
        sama_dengan_query = {}
        #iterasikan setiap elemen list query_dict["hasil_stemming"]
        for elemen in query_dict["hasil_stemming"]:
            #baca kata dasar dari setiap elemen
            for kata_asal, kata_dasar in elemen.items():
                #jadikan kata dasar tersebut sebagai key dan isi valuenya dengan 0
                sama_dengan_query[kata_dasar] = 0
        #masukkan dictionary sama_dengan_query ke dokumen["sama_dengan_query"]
        dokumen["sama_dengan_query"] = sama_dengan_query
        #kini dokumen berbentuk {"path": "", "nama": "", "ekstensi": "", "konten": "", "hasil_stemming": [{"kata_asal": "kata_dasar"}], "total_stemming": int, "jumlah_kata_dasar": {"kata_dasar": int}, "total_kata_dasar": int, "sama_dengan_query": {"kata_dasar": int}}
        #untuk saat ini value kata dasar yang sama dengan query masih 0 semua

        #iterasikan setiap elemen list dokumen["hasil_stemming"]
        for elemen in dokumen["hasil_stemming"]:
            #baca kata dasar dari setiap elemen
            for kata_asal, kata_dasar in elemen.items():
                #baca setiap kata dasar dari query_dict["jumlah_kata_dasar"]
                for kata_dasar_query in query_dict["jumlah_kata_dasar"]:
                    #jika kata dasar dari elemen yang sedang dibaca sama dengan kata dasar query
                    if kata_dasar == kata_dasar_query:
                        #tambah value kata dasar yang sama dengan query dengan 1
                        dokumen["sama_dengan_query"][kata_dasar] += 1
        #kini value kata dasar yang sama dengan query sudah berisi jumlah yang tepat

    #list sebagai penampung nilai Tn (T1, T2, T3, dst)
    t = []
    #iterasikan satu dictionary dokumen saja dari list seluruh_dokumen
    for dokumen in seluruh_dokumen:
        #iterasikan setiap kata dasar yang sama dengan query
        for kata_dasar, jumlah in dokumen["sama_dengan_query"].items():
            #inisialisasi nilai Tn dengan 0 kemudian masukkan ke dalam list t
            t.append(0)
        #break di sini supaya iterasi cuma sekali
        break
    
    #iterasikan dictionary dokumen dari list seluruh_dokumen
    for dokumen in seluruh_dokumen:
        #sebagai index list t
        index_t = 0
        #baca setiap jumlah dari kata dasar yang sama dengan query
        for kata_dasar, jumlah in dokumen["sama_dengan_query"].items():
            #jika jumlah tidak 0
            if jumlah > t[index_t]:
                #isi nilai Tn dengan 1
                t[index_t] = 1
            #lanjut index berikutnya
            index_t += 1

    #ulang index list t dari 0 lagi
    index_t = 0
    #baca setiap jumlah masing-masing kata dasar query
    for kata_dasar, jumlah in query_dict["jumlah_kata_dasar"].items():
        #jika jumlah tidak 0
        if jumlah > t[index_t]:
            #isi nilai Tn dengan 1
            t[index_t] = 1
        #lanjut index berikutnya
        index_t += 1

    #iterasikan setiap dictionary dokumen dari list seluruh_dokumen
    for dokumen in seluruh_dokumen:
        #sebagai pembilang dari rumus similarity
        pembilang = 0
        #ulangin index list t dari 0 lagi
        index_t = 0
        #baca setiap jumlah dari masing-masing kata dasar yang sama dengan query dari dokumen tersebut
        for kata_dasar, jumlah in dokumen["sama_dengan_query"].items():
            #kalikan jumlah dengan Tn kemudian jumlahkan seluruhnya [(jumlah1*T1)+(jumlah2*T2)+dst]
            pembilang += (jumlah*t[index_t])
            #lanjut index berikutnya
            index_t += 1

        #sebagai penampung dari jumlah masing-masing kata dasar yang sama dengan query kuadrat yang dijumlahkan
        akar_dokumen = 0
        #baca setiap jumlah dari masing-masing kata dasar yang sama dengan query dari dokumen tersebut
        for kata_dasar, jumlah in dokumen["sama_dengan_query"].items():
            #kuadratkan jumlahnya kemudian jumlahkan semua hasil kuadratnya (jumlah1^2+jumlah2^2+dst)
            akar_dokumen += (jumlah*jumlah)
        
        #sebagai penampung dari jumlah masing-masing kata dasar query kuadrat yang dijumlahkan
        akar_query = 0
        #baca setiap jumlah dari masing-masing kata dasar query
        for kata_dasar, jumlah in query_dict["jumlah_kata_dasar"].items():
            #kuadratkan jumlahnya kemudian jumlahkan semua hasil kuadratnya (jumlah1^2+jumlah2^2+dst)
            akar_query += (jumlah*jumlah)

        #jika tidak ada satupun kata dasar dari dokumen yang sama dengan query
        if (akar_dokumen == 0):
            #beri nilai 0 untuk similarity
            dokumen["similarity"] = akar_dokumen
            #jika similarity tidak dinolkan maka akan terjadi pembagian nol bagi nol (0/0) yang mana itu akan menghasilkan error
        #jika ada kata dasar dari dokumen yang sama dengan query
        else:
            #kalikan akar sigma jumlah kata dasar dokumen yang sama dengan query kuadrat dengan akar sigma jumlah kata dasar query kuadrat
            #penyebut = sqrt((jumlah1^2+jumlah2^2+dst))*sqrt((jumlah1^2+jumlah2^2+dst))
            penyebut = math.sqrt(akar_dokumen)*math.sqrt(akar_query)
            #bagi pembilang dengan penyebut kemudian masukkan ke dokumen["similarity"]
            dokumen["similarity"] = pembilang/penyebut
        #kini dokumen berbentuk {"path": "", "nama": "", "ekstensi": "", "konten": "", "hasil_stemming": [{"kata_asal": "kata_dasar"}], "total_stemming": int, "jumlah_kata_dasar": {"kata_dasar": int}, "total_kata_dasar": int, "sama_dengan_query": {"kata_dasar": int}, "similarity": float}

    #seluruh_dokumen = [{"path": "", "nama": "", "ekstensi": "", "konten": "", "hasil_stemming": [{"kata_asal": "kata_dasar"}], "total_stemming": int, "jumlah_kata_dasar": {"kata_dasar": int}, "total_kata_dasar": int, "sama_dengan_query": {"kata_dasar": int}, "similarity": float}]
    #urutkan list seluruh_dokumen dimulai dari nilai similarity yang terbesar
    return sorted(seluruh_dokumen, key=lambda x: x["similarity"], reverse=True)
