def search_items(cur, keyword):
  params = keyword
  search = cur.execute('''SELECT i.name, c.name
              FROM items i 
              INNER JOIN category c 
              ON i.category_id = c.id
              WHERE i.name = ? 
              OR c.name = ? ''', (params, params, ))
  records = list(search)

  if len(records) == 0:
      return "This item or category does not exist."
  else:
      items = []
      for row in records:
          items.append("name: " + row[0] + ", category: " + row[1])
      return "items: " + str(items)
