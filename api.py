from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import TemuBalik

# Inisialisasi aplikasi FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti "*" dengan daftar domain yang diizinkan
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schema data input menggunakan Pydantic
class InputData(BaseModel):
    query: str
    directory_path: str

#API
@app.post("/api")
async def process_api(data: InputData):
    try:
        # Ambil data dari request
        query = data.query
        directory_path = data.directory_path
        daftar_file = TemuBalik.cekDirectoryPath(directory_path)

        if not query.strip():
            raise ValueError("Query tidak boleh kosong")

        if not any(char.isalpha() for char in query):
            raise ValueError("Query harus mengandung huruf")

        query_info = TemuBalik.prosesQuery(query.lower())

        list_dokumen = TemuBalik.bacaIsiDokumen(directory_path)

        hasil_vsm = TemuBalik.temuBalikVSM(list_dokumen, TemuBalik.prosesQuery(query.lower()))

        result = {
            "directory_path": directory_path,
            "daftar_file": daftar_file,
            "query_info": query_info,
            "hasil_temu_balik": hasil_vsm,
        }

        # Return hasil olahan dalam bentuk JSON
        return result

    except ValueError as ve:
        # Tangani error khusus untuk ValueError
        raise HTTPException(status_code=400, detail=f"{str(ve)}")
    except Exception as e:
        # Tangani error lainnya dan kirimkan respons yang sesuai
        raise HTTPException(status_code=500, detail=f"{str(e)}")