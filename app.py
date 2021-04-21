from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import uuid
import json

NULL = "NULL"
# id | name | description | examples | posted['YES' / 'NO']
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Slang:
    def __init__(self, id, name, description, examples, posted):
        self.__id = id  # id
        self.__name = name  # name
        self.__description = description  # description
        self.__examples = examples  # examples
        self.__posted = posted  # posted
 
    @property
    def id(self):
        return self.__id
 
    @property
    def name(self):
        return self.__name
        
    @property
    def description(self):
        return self.__description
 
    @property
    def examples(self):
        return self.__examples
 
    @property
    def posted(self):
        return self.__posted
 
    def __str__(self):
        return "Name: {} \t Description: {} \t Examples: {} \t Id: {} \t Posted: {}".format(self.__name, self.__description, self.__examples, self.__id, self.__posted)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/get', methods=['GET'])
def getSlangs():
    data = db.session.execute(f"SELECT * FROM slangs WHERE posted = 'YES'").fetchall()
    data_out = []
    for item in data:
        id, name, description, examples, posted = item
        data_out.append({
            'name': name,
            'description': description,
            'id': id,
            'posted': posted,
            'examples': examples,
        })
    return json.dumps({'status': 200, 'data': data_out})

@app.route('/api/getUnposted', methods=['GET'])
def getSlangsUnposted():
    data = db.session.execute(f"SELECT * FROM slangs WHERE posted = 'NO'").fetchall()
    data_out = []
    for item in data:
        id, name, description, examples, posted = item
        data_out.append({
            'name': name,
            'description': description,
            'id': id,
            'posted': posted,
            'examples': examples,
        })
    return json.dumps({'status': 200, 'data': data_out})

@app.route('/api/adminAdd', methods=['POST'])
def addSlangAdmin():
    data = json.loads(request.data.decode('utf-8'))
    req = db.session.execute(f"INSERT INTO slangs VALUES {(str(uuid.uuid4()), data['name'], data['description'], '', 'YES')}")
    db.session.commit()
    return json.dumps({'status': 200, 'data': data})

@app.route('/api/userAdd', methods=['POST'])
def addSlangUser():
    data = json.loads(request.data.decode('utf-8'))
    req = db.session.execute(f"INSERT INTO slangs VALUES {(str(uuid.uuid4()), data['name'], data['description'], '', 'NO')}")
    db.session.commit()
    return json.dumps({'status': 200, 'data': data})

@app.route('/api/del', methods=['POST'])
def delSlang():  # удалить mark по id
    id = json.loads(request.data.decode('utf-8'))
    print(request.data)
    print(request.data.decode('utf-8'))
    req = db.session.execute(f"DELETE FROM slangs WHERE id = '{id}'")
    db.session.commit()
    return json.dumps({'status': 200})

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
