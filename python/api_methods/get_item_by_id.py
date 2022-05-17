def get_item_by_id(cur, item_id):
  params = item_id
  search = cur.execute('''SELECT i.id, i.name, c.name, i.image
                FROM items i 
                INNER JOIN category c 
                ON i.category_id = c.id 
                WHERE i.id=(?)''', (params, ))
  records = list(search)
  
  if len(records) == 0:
      return "This item id does not exist."
  else:
      items = []
      for row in records:
          items.append("name: " + row[1] + ", category: " + row[2] + ", image: " + row[3])
      return "items: " + str(items)