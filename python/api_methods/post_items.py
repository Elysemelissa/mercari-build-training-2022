def post_category(cur, category_string):
    cur.execute('''INSERT INTO category 
                VALUES (NULL, ?)''', (category_string, ))

def post_name_image(cur, name_string, category_string, image_hash):
    items_params = (name_string, category_string, image_hash)
    cur.execute('''INSERT INTO items 
                VALUES (NULL, ?, (SELECT id FROM category WHERE name = ?), ?)''', (items_params))
