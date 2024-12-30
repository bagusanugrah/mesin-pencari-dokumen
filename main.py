from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import TemuBalik

# Inisialisasi aplikasi FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan semua asal
    allow_methods=["*"],  # Mengizinkan semua metode
    allow_headers=["*"],  # Mengizinkan semua header
    expose_headers=["Content-Disposition"],  # Mengizinkan akses header tertentu
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "data": None, "error_message": None})


# Endpoint POST untuk menerima data
@app.post("/")
async def process_data(request: Request, input_query: str = Form(...), input_directory_path: str = Form(...)):
    try:
        # Ambil data dari request
        query = input_query
        directory_path = input_directory_path
        daftar_file = TemuBalik.cekDirectoryPath(directory_path)

        #jika query tidak diisi
        if not query.strip():
            raise ValueError("Query tidak boleh kosong")
        
        #jika query tidak mengandung huruf sama sekali
        if not any(char.isalpha() for char in query):
            raise ValueError("Query harus mengandung huruf")

        query_info = TemuBalik.prosesQuery(query.lower())

        list_dokumen = TemuBalik.bacaIsiDokumen(directory_path)

        hasil_vsm = TemuBalik.temuBalikVSM(list_dokumen, query_info)

        result = {
            "directory_path": directory_path,
            "daftar_file": daftar_file,
            "query_info": query_info,
            "hasil_temu_balik": hasil_vsm,
        }

        return templates.TemplateResponse(
            "body.html", {"request": request, "data": result, "error_message": None}
        )

    except ValueError as ve:
        # Tangani error khusus untuk ValueError
        raise HTTPException(status_code=400, detail=f"{str(ve)}")
    except Exception as e:
        # Tangani error lainnya dan kirimkan respons yang sesuai
        raise HTTPException(status_code=500, detail=f"{str(e)}")

@app.exception_handler(HTTPException)
def custom_http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "status_code": exc.status_code, "detail": exc.detail},
        status_code=exc.status_code,
    )
