import os
import logging
import pathlib
import sqlite3
import hashlib


from fastapi import FastAPI, Form, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = logging.getLogger("uvicorn")
# logger.level = logging.INFO
logger.setLevel(logging.DEBUG)

images = pathlib.Path(__file__).parent.resolve() / "image"
origins = [ os.environ.get('FRONT_URL', 'http://localhost:3000') ]
db_path = "/Users/elyse/mercari-build-training-2022/mercari-build-training-2022/db/items.db"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    return {"message": "Hello, world!"}

@app.get("/items")
def get_items():
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute('''SELECT i.name, c.name, i.image 
                FROM items i 
                INNER JOIN category c 
                ON i.category_id = c.id''')
    records = list(cur)
    con.close()
    items = []
    for row in records:
        items.append("name: " + row[0] + ", category: " + row[1] + ", image: " + row[2])
    return "items: " + str(items)

@app.post("/items")
async def add_item(name: str = Form(...), category: str = Form(...), image: str = Form(...)):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    encode = image.encode(encoding = 'UTF-8', errors = 'strict')
    image_hash = hashlib.sha256(encode).hexdigest() + ".jpg"

    cur.execute('''INSERT INTO category 
                VALUES (NULL, ?)''', (category, ))
    con.commit()

    items_params = (name, category, image_hash)
    cur.execute('''INSERT INTO items 
                VALUES (NULL, ?, (SELECT id FROM category WHERE name = ?), ?)''', (items_params))
    con.commit()
    con.close()
    logger.info(f"Receive item: {name}, {category}, {image_hash}")
    open

    return {"message": f"item received: {name}, {category}, {image_hash}"}

@app.get("/search")
async def search_item(keyword: str = Query(...)):

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    params = keyword

    cur.execute('''SELECT i.name, c.name
                FROM items i 
                INNER JOIN category c 
                ON i.category_id = c.id
                WHERE i.name = ? 
                OR c.name = ? ''', (params, params, ))

    records = list(cur)
    print(records)
    if len(records) == 0:
        return "This item or category does not exist."
    else:
        items = []
        for row in records:
            items.append("name: " + row[0] + ", category: " + row[1])
        return "items: " + str(items)

@app.get("/items/{item_id}") 
async def read_item(item_id):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    params = item_id
    cur.execute('''SELECT i.id, i.name, c.name, i.image
                FROM items i 
                INNER JOIN category c 
                ON i.category_id = c.id 
                WHERE i.id=(?)''', (params, ))

    records = list(cur)
    if len(records) == 0:
        return "This item id does not exist."
    else:
        items = []
        for row in records:
            items.append("name: " + row[1] + ", category: " + row[2] + ", image: " + row[3])
        return "items: " + str(items)

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
