import os
import logging
import pathlib
import sqlite3


from fastapi import FastAPI, Form, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "image"
origins = [ os.environ.get('FRONT_URL', 'http://localhost:3000') ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)
    

@app.get("/")
def root():
    con = sqlite3.connect("/Users/elyse/mercari-build-training-2022/mercari-build-training-2022/db/items.db")
    cur = con.cursor()
    return {"message": "Hello, world!"}

@app.get("/items")
def get_items():
    con = sqlite3.connect("/Users/elyse/mercari-build-training-2022/mercari-build-training-2022/db/items.db")
    cur = con.cursor()

    cur.execute('''SELECT * FROM items''')
    records = list(cur)
    con.close()
    items = []
    for row in records:
        items.append("name: " + row[1] + ", category: " + row[2])
    return "items: " + str(items)

@app.post("/items")
def add_item(name: str = Form(...), category: str = Form(...)):
    con = sqlite3.connect("/Users/elyse/mercari-build-training-2022/mercari-build-training-2022/db/items.db")
    cur = con.cursor()
    params = (name, category)

    cur.execute('''INSERT INTO items VALUES (NULL, ?, ?)''', (params))
    con.commit()
    con.close()
    logger.info(f"Receive item: {name}, {category}")
    open

    return {"message": f"item received: {name}, {category}"}

@app.get("/search")
async def search_item(keyword: str = Query(...)):

    con = sqlite3.connect("/Users/elyse/mercari-build-training-2022/mercari-build-training-2022/db/items.db")
    cur = con.cursor()
    params = keyword

    cur.execute('''SELECT * FROM items WHERE name=(?) OR category=(?)''', (params, params, ))
    records = list(cur)
    if len(records) == 0:
        return "This item or category does not exist."
    else:
        items = []
        for row in records:
            items.append("name: " + row[1] + ", category: " + row[2])
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
