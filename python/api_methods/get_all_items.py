def get_all_items(cur):
  cur.execute('''SELECT i.name, c.name, i.image 
                FROM items i 
                INNER JOIN category c 
                ON i.category_id = c.id''')
  records = list(cur)
  items = []
  for row in records:
      items.append("name: " + row[0] + ", category: " + row[1] + ", image: " + row[2])
  return "items: " + str(items)