def post_category(cur, category):
    cur.execute('''INSERT INTO category 
                VALUES (NULL, ?)''', (category, ))

def post_name_image(cur, name, category, image_hash):
    items_params = (name, category, image_hash)
    cur.execute('''INSERT INTO items 
                VALUES (NULL, ?, (SELECT id FROM category WHERE name = ?), ?)''', (items_params))
