import os, logging, pathlib, sqlite3, hashlib

# API methods import
from api_methods.get_all_items import get_all_items
from api_methods.post_items import post_category, post_name_image
from api_methods.search_items import search_items
from api_methods.get_item_by_id import get_item_by_id

from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI, Form, File, HTTPException, Query
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
async def add_item(name: bytes = File(...), category: bytes = File(...), image: bytes = File(...)):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    name_string = name.decode('utf-8')
    category_string = category.decode('utf-8')

    image_hash = encode_image(image)
    post_category(cur, category_string)
    con.commit()
    
    post_name_image(cur, name_string, category_string, image_hash)
    con.commit()
    con.close()
    
    logger.info(f"Receive item: {name_string}, {category_string}, {image_hash}")
    open
    return {"message": f"item received: {name_string}, {category_string}, {image_hash}"}

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

@app.get("/image/{image_filename}")
async def get_image(image_filename):
    # Create image path
    image = images / image_filename

    if not image_filename.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"
    return FileResponse(image)

def encode_image(image):
    image_hash = hashlib.sha256(image).hexdigest() + ".jpg"
    
    with open("images/" + image_hash, "wb") as file:
        file.write(image)
    return image_hash

