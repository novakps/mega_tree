import json
from loremipsum import Generator
from pymongo import MongoClient, ASCENDING, DESCENDING
import random

g = Generator()
g.sentence_mean = 2

def buildNestedSets(collection):
    collection.drop()
    collection.create_index([('parent', ASCENDING)])
    collection.create_index([('left', ASCENDING)])
    collection.create_index([('right', ASCENDING)])

    root_id = collection.insert({'_id': '0', 'name': 'root', 'parent': None})
    for fid in [str(i) for i in range(1, 8)]:
        _fid = collection.insert({ 'name': g.generate_sentence()[2], 'parent': root_id})

        for sid in [fid + '.' + chr(i) for i in range(ord('A'), ord('Z') + 1)]:
            _sid = collection.insert({'name': g.generate_sentence()[2], 'parent': _fid})

            for ssid in [sid + '.' + str(i) for i in range(1, 8000)]:
                _ssid = collection.insert({'name': g.generate_sentence()[2], 'parent': _sid})

                for lid in [ssid + '.' + chr(i) for i in range(ord('a'), ord('b') + 1)]:
                    collection.insert({'name': g.generate_sentence()[2], 'parent': _ssid, 'leaf': True})

    updateNode(collection, root_id, 1)


top_level_folder_names = ['Project Favorites', 'Computed Properties', 'Computational Models', 'Experimental Assays', 'Formulas', 'Multi-Parameter Profiles']
value_types = ['string', 'float', 'integer', 'image', 'molecule', '3D']

def buildKitchenSink(collection):
    collection.drop()
    collection.create_index([('parent', ASCENDING)])
    collection.create_index([('left', ASCENDING)])
    collection.create_index([('right', ASCENDING)])

    root_id = collection.insert({'_id': '0', 'name': 'root', 'parent': None, 'ancestors': []})
    addable_column_id = 0;

    collection.insert({ 'name': '0.' + top_level_folder_names[0], 'parent': root_id, 'ancestors': [root_id]})
    for fid,name in [(str(i + 1), name) for i,name in enumerate(top_level_folder_names[1:])]:
        _fid = collection.insert({ 'name': fid + '.' + name, 'parent': root_id, 'ancestors': [root_id]})

        for sid in [fid + '.' + chr(i) for i in range(ord('A'), ord('Z') + 1)]:
            _sid = collection.insert({'name': sid + '.' + g.generate_sentence()[2], 'parent': _fid, 'ancestors': [root_id, _fid]})

            for ssid in [sid + '.' + str(i) for i in range(1, 270)]:
                _ssid = collection.insert({'name': ssid + '.' + g.generate_sentence()[2], 'parent': _sid, 'ancestors': [root_id, _fid, _sid]})

                for lid in [ssid + '.' + str(i) for i in range(1, random.randint(1,4))]:
                    addable_column_id+=1
                    collection.insert(
                        {'name': lid + '.' + g.generate_sentence()[2],
                         'parent': _ssid,
                         'ancestors': [root_id, _fid, _sid, _ssid],
                         'leaf': True,
                         'favorite': 1 == random.randint(1,100),
                         'addable_column_id': addable_column_id,
                         'column_type': random.choice(top_level_folder_names[1:]),
                         'value_type': random.choice(value_types)})
    updateNode(collection, root_id, 1)

def updateNode (collection, id, left):
    right = left + 1
    for node in collection.find( {'parent': id}):
        right = updateNode(collection, node['_id'], right) + 1
    collection.update({'_id': id}, { '$set': {'left':left, 'right': right}})
    return right

if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')
    db = client.dummydata

##  buildNestedSets(db.nested_set)
    buildKitchenSink(db.kitchen_sink)
