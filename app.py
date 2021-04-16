from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json

NULL = "NULL"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Jst srvr"

@app.route('/api/get')
def slangsGet():
    return json.dumps({'status': '200', 'data': db.session.execute("SELECT * FROM slangs")})

@app.route('/api/add', methods=['POST'])
def slangAdd():
    data = json.loads(request.data.decode('utf-8'))
    label = data["label"]
    db.session.execute("SELECT slangs FROM users WHERE label = '{label}'")
    if(db.session.fetchone() is None):
        req = db.session.execute(f"INSERT INTO slangs VALUES (?, ?, ?, ?)", (data["label"], data["description"], data["id"], "YES"))
    else:
        return json.dumps({'status': '405'})
    db.session.commit()
    return json.dumps({'status': '200'})

@app.route('/api/del', methods=['POST'])
def slangDelete():
    id = json.loads(request.data.decode('utf-8'))
    req = db.session.execute(f"DELETE FROM slangs WHERE id = '{id}'")
    db.session.commit()
    return json.dumps({'status': '200'})


# @app.route('/api/shop/del', methods=['POST'])
# def shopDel():  # удалить магазин по id
#     data = json.loads(request.data.decode('utf-8'))
#     shopID = data["id"]
#     # req = db.session.execute(f"SELECT * FROM shops WHERE id = '{shopID}'").fetchone()
#     req = _getShop(shopID)
#     if not req:
#         return json.dumps({'status': '404', 'error': f'Магазина {shopID} не существует'})
#     # DELETE from films
#     # where year < 1985
#     req = db.session.execute(f"DELETE FROM Marks WHERE shopID = '{shopID}'")
#     req = db.session.execute(f"DELETE FROM Shops WHERE id = '{shopID}'")
#     db.session.commit()
#     return json.dumps({'status': '200'})


# @app.route('/api/shop/get', methods=['POST'])
# def shopGet():  # получить магазин по id
#     data = json.loads(request.data.decode('utf-8'))
#     shopID = data["id"]
#     # req = db.session.execute(f"SELECT * FROM shops WHERE id = '{shopID}'").fetchone()
#     req = _getShop(shopID)
#     if not req:
#         return json.dumps({'status': '404', 'error': f'Магазина {shopID} не существует'})
#     ID, name, descript, imagePath, website, lat, lng, city = req
#     req = db.session.execute(f"SELECT * FROM Marks WHERE shopID = '{shopID}'").fetchall()
#     marks = []
#     for mark in req:
#         IDM, nameM, descriptM, latM, lngM, shopIDM = mark
#         marks.append({"id": IDM, "name": nameM, "description": descriptM, "position": {"lat": latM, "lng": lngM}})

#     out_data = {'status': '200',
#                 "id": ID, "name": name, "description": descript,
#                 "image": imagePath,
#                 "website": website,
#                 "marks": marks,
#                 "position": {"lat": lat, "lng": lng},
#                 "city": city}

#     return json.dumps(out_data)


# @app.route('/api/shop/put', methods=['POST'])
# def shopPut():  # новый магазин
#     data = json.loads(request.data.decode('utf-8'))
#     ID = data['id']
#     # req = db.session.execute(f"SELECT id FROM shops WHERE id = '{ID}'").fetchone()
#     req = _getShop(ID)
#     if req:
#         print("ERROR shopPut", ID, f'Магазина {ID} уже существует')
#         return json.dumps({'status': '208', 'error': f'Магазина {ID} уже существует'})
#     imagePath = data.get("image", "NULL")
#     # INSERT INTO имя_таблицы(названия_полей*) VALUES(значения)
#     website = data.get("website", "NULL")
#     pos = data.get("position", {"lat": NULL, "lng": NULL})
#     lat, lng = pos["lat"], pos["lng"]
#     city = data.get("city", NULL)
#     req = db.session.execute(
#         f"INSERT INTO shops VALUES{(ID, data['name'], data['description'], imagePath, website, lat, lng, city)}")
#     for mark in data.get("marks", []):
#         IDM = mark.get("id")
#         if _getMark(IDM):
#             print("ERROR shopPut", ID, f'Марка {IDM} уже существует')
#             return json.dumps({'status': '209', 'error': f'Марка {IDM} уже существует', 'id': IDM})
#         descript = mark.get("description", "NULL")
#         pos = mark.get("position", {"lat": NULL, "lng": NULL})
#         lat, lng = pos["lat"], pos["lng"]
#         db.session.execute(
#             f"INSERT INTO marks(id, name, description, lat, lng, shopID) "
#             f"VALUES{(IDM, mark['name'], descript, lat, lng, ID)}")
#     db.session.commit()
#     print("shopPut", ID)
#     return json.dumps({'status': '201'})


# @app.route('/api/shop/all', methods=['POST', 'GET'])
# def shopAll():  # все магазины
#     data = json.loads(request.data.decode('utf-8'))
#     city = data.get('city')
#     reqs = db.session.execute(f"SELECT * FROM Shops {f'''WHERE city = '{city}' ''' if city else ''}").fetchall()
#     shops = []
#     for req in reqs:
#         ID, name, descript, imagePath, website, lat, lng, city = req
#         shops.append({"id": ID, "name": name, 
#                       "description": descript, 
#                       "position": {"lat": lat, "lng": lng},
#                       "website": website, 'city': city})
#     return json.dumps({'status': '200', 'shops': shops})


# @app.route('/api/mark/del', methods=['POST'])
# def markDel():  # удалить mark по id
#     data = json.loads(request.data.decode('utf-8'))
#     ID = data["id"]
#     req = _getMark(ID)
#     if not req:
#         return json.dumps({'status': '404', 'error': f'Марки {ID} не существует'})
#     # DELETE from films
#     # where year < 1985
#     req = db.session.execute(f"DELETE FROM Marks WHERE id = '{ID}'")
#     db.session.commit()
#     return json.dumps({'status': '200'})


# @app.route('/api/mark/get', methods=['POST'])
# def markGet():  # получить марку по id
#     data = json.loads(request.data.decode('utf-8'))
#     IDM = data["id"]
#     req = _getMark(IDM)
#     if not req:
#         return json.dumps({'status': '404', 'error': f'Марки {IDM} не существует'})
#     ID, name, descript, lat, lng, shopID = req
#     out_data = {'status': '200',
#                 "id": ID, "name": name, "description": descript,
#                 "position": {"lat": lat, "lng": lng},
#                 "shopID": shopID}

#     return json.dumps(out_data)


# @app.route('/api/shop/mark/put', methods=['POST'])
# def markPut():  # новый марка для магазина
#     data = json.loads(request.data.decode('utf-8'))
#     ID = data['shopID']

#     # req = db.session.execute(f"SELECT id FROM Shops WHERE id = '{ID}'").fetchone()
#     req = _getShop(ID)
#     if not req:
#         print("ERROR markPut", ID, f'Магазина {ID} не существует')
#         return json.dumps({'status': '404', 'error': f'Магазин {ID} не существует'})
#     IDM = data.get('markID')
#     if _getMark(IDM):
#         print("ERROR markPut", ID, f'Марка {IDM} уже существует')
#         return json.dumps({'status': '209', 'error': f'Марка {IDM} уже существует', 'id': IDM})

#     descript = data.get("description", "NULL")
#     pos = data.get("position", {"lat": NULL, "lng": NULL})
#     lat, lng = pos["lat"], pos["lng"]
#     db.session.execute(
#         f"INSERT INTO marks(id, name, description, lat, lng, shopID) "
#         f"VALUES{(IDM, data['name'], descript, lat, lng, ID)}")

#     db.session.commit()
#     print("markPut", IDM)
#     return json.dumps({'status': '201'})


# @app.route('/api/shop/mark/all', methods=['POST', 'GET'])
# def markAll():  # все магазины
#     data = json.loads(request.data.decode('utf-8'))
#     ID = data['id']
#     req = _getShop(ID)
#     if not req:
#         print("ERROR markAll", ID, f'Магазина {ID} не существует')
#         return json.dumps({'status': '404', 'error': f'Магазин {ID} не существует'})

#     reqs = db.session.execute(f"SELECT * FROM Marks WHERE shopID = '{ID}'").fetchall()
#     marks = []
#     for req in reqs:
#         ID, name, descript, lat, lng, _ID = req
#         marks.append({"id": ID, "name": name,
#                       "description": descript,
#                       "position": {"lat": lat, "lng": lng}})
#     print("getAllMarks", ID, marks, reqs)
#     return json.dumps({'status': '200', 'marks': marks})


# @app.route('/api/city/all', methods=['POST', 'GET'])
# def cityAll():  # все города
#     reqs = db.session.execute(f"SELECT city FROM Shops GROUP BY city").fetchall()
#     cities = [r[0] for r in reqs]
#     print(reqs)
#     return json.dumps({'status': '200', "cities": cities})


if __name__ == '__main__':
    app.run(debug=True)
