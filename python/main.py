import os, logging, pathlib, sqlite3, hashlib

# API methods import
from api_methods.get_all_items import get_all_items
from api_methods.post_items import post_category, post_name_image
from api_methods.search_items import search_items
from api_methods.get_item_by_id import get_item_by_id

from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI, Form, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

images = pathlib.Path(__file__).parent.resolve() / "image"
origins = [ os.environ.get('FRONT_URL', 'http://localhost:3000') ]

dotenv_path = Path('DB_PATH.env')
load_dotenv(dotenv_path=dotenv_path)
DB_PATH = os.getenv("DB_PATH")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello, world!"}

@app.get("/items")
def get_items():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    items_list = get_all_items(cur)
    con.close()
    
    return items_list

@app.post("/items")
async def add_item(name: str = Form(...), category: str = Form(...), image: str = Form(...)):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    image_hash = encode_image(image)
    post_category(cur, category)
    con.commit()
    
    post_name_image(cur, name, category, image_hash)
    con.commit()
    con.close()
    
    logger.info(f"Receive item: {name}, {category}, {image_hash}")
    open
    return {"message": f"item received: {name}, {category}, {image_hash}"}

@app.get("/search")
async def search_item(keyword: str = Query(...)):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    search_query_results = search_items(cur, keyword)
    con.close()
    
    return search_query_results

@app.get("/items/{item_id}") 
async def read_item(item_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    search_id_results = get_item_by_id(cur, item_id)
    con.close()

    return search_id_results

@app.get("/image/{items_image}")
async def get_image(items_image):
    # Create image path
    image = images / items_image

    if not items_image.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)

def encode_image(image):
    encode = image.encode(encoding = 'UTF-8', errors = 'strict')
    image_hash = hashlib.sha256(encode).hexdigest() + ".jpg"
    return image_hash