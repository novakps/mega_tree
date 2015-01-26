import json
from loremipsum import Generator
from pymongo import MongoClient, ASCENDING, DESCENDING

g = Generator()
g.sentence_mean = 2

def buildParentRef(collection):
    collection.drop()
    collection.create_index([('parent', ASCENDING)])
    root_id = collection.insert({'name': 'root', 'parent': None})
    for fid in [str(i) for i in range(1, 8)]:
        _fid = collection.insert({ 'name': fid + '.' + g.generate_sentence()[2], 'parent': root_id})

        for sid in [fid + '.' + chr(i) for i in range(ord('A'), ord('Z') + 1)]:
            _sid = collection.insert({ 'name': sid + '.' + g.generate_sentence()[2], 'parent': _fid})

            for ssid in [sid + '.' + str(i) for i in range(1, 200)]:
                _ssid = collection.insert({'name': ssid + '.' + g.generate_sentence()[2], 'parent': _sid})

                for lid in [ssid + '.' + chr(i) for i in range(ord('a'), ord('z') + 1)]:
                    collection.insert({'name': lid + '.' + g.generate_sentence()[2], 'parent': _ssid, 'leaf': True})

def buildChildRef(collection):
    collection.drop()
    collection.create_index([('children', ASCENDING)])
    root_children = []
    for fid in [str(i) for i in range(1, 8)]:
        print '.',
        fid_children = []
        for sid in [fid + '.' + chr(i) for i in range(ord('A'), ord('Z') + 1)]:
            sid_children = []
            for ssid in [sid + '.' + str(i) for i in range(1, 200)]:
                ssid_children = []
                for lid in [ssid + '.' + chr(i) for i in range(ord('a'), ord('z') + 1)]:
                    ssid_children.append(collection.insert({'_id': lid, 'name': lid + '.' + g.generate_sentence()[2], 'children': []}))
                sid_children.append(collection.insert({'_id': ssid, 'name': ssid + '.' + g.generate_sentence()[2], 'children': []}))
            fid_children.append(collection.insert({'_id': sid, 'name': sid + '.' + g.generate_sentence()[2], 'children': sid_children}))
        root_children.append(collection.insert({ '_id': fid, 'name': fid + '.' + g.generate_sentence()[2], 'children': fid_children}))
    collection.insert({'_id': '0', 'name': 'root', 'children': root_children})

def buildAncestorsArray(collection):
    collection.drop()
    collection.create_index([('ancestors', ASCENDING)])
    root_id = collection.insert({'_id': '0', 'name': 'root', 'ancestors': []})
    for fid in [str(i) for i in range(1, 8)]:
        _fid = collection.insert({ '_id': fid, 'name': fid + '.' + g.generate_sentence()[2], 'ancestors': [root_id], 'parent': root_id})

        for sid in [fid + '.' + chr(i) for i in range(ord('A'), ord('Z') + 1)]:
            _sid = collection.insert({'_id': sid, 'name': sid + '.' + g.generate_sentence()[2], 'ancestors': [root_id, _fid], 'parent': _fid})

            for ssid in [sid + '.' + str(i) for i in range(1, 200)]:
                _ssid = collection.insert({'_id': ssid, 'name': ssid + '.' + g.generate_sentence()[2], 'ancestors': [root_id, _fid, _sid], 'parent': _sid})

                for lid in [ssid + '.' + chr(i) for i in range(ord('a'), ord('z') + 1)]:
                    collection.insert({'_id': lid, 'name': lid + '.' + g.generate_sentence()[2], 'ancestors': [root_id, _fid, _sid, _ssid], 'parent': _ssid})

def buildMaterializedPath(collection):
    collection.drop()
    collection.create_index([('path', ASCENDING)])
    for fid in [str(i) for i in range(1, 8)]:
        _fid = collection.insert({ '_id': fid, 'name': fid + '.' + g.generate_sentence()[2], 'path': None})

        for sid in [fid + '.' + chr(i) for i in range(ord('A'), ord('Z') + 1)]:
            _sid = collection.insert({'_id': sid, 'name': sid + '.' + g.generate_sentence()[2], 'path': ',' + ','.join([_fid]) + ','})

            for ssid in [sid + '.' + str(i) for i in range(1, 200)]:
                _ssid = collection.insert({'_id': ssid, 'name': ssid + '.' + g.generate_sentence()[2], 'path': ',' + ','.join([_fid, _sid]) + ','})

                for lid in [ssid + '.' + chr(i) for i in range(ord('a'), ord('z') + 1)]:
                    collection.insert({'_id': lid, 'name': lid + '.' + g.generate_sentence()[2], 'path': ',' + ','.join([_fid, _sid, _ssid]) + ','})

def buildNestedSets(collection):
    collection.drop()
    collection.create_index([('parent', ASCENDING)])
    collection.create_index([('left', ASCENDING)])
    collection.create_index([('right', ASCENDING)])

    root_id = collection.insert({'_id': '0', 'name': 'root', 'parent': None})
    for fid in [str(i) for i in range(1, 3)]:
        _fid = collection.insert({ 'name': fid + '.' + g.generate_sentence()[2], 'parent': root_id})

        for sid in [fid + '.' + str(j) for j in range(1, 16000)]:
            _sid = collection.insert({'name': sid + '.' + g.generate_sentence()[2], 'parent': _fid, 'leaf': True})

            # for ssid in [sid + '.' + str(i) for i in range(1, 4)]:
            #     _ssid = collection.insert({'name': ssid + '.' + g.generate_sentence()[2], 'parent': _sid})

            #     for lid in [ssid + '.' + chr(i) for i in range(ord('a'), ord('c') + 1)]:
            #         collection.insert({'name': lid + '.' + g.generate_sentence()[2], 'parent': _ssid, 'leaf': True})
    updateNode(collection, root_id, 1)

def buildKitchenSink(collection):
    collection.drop()
    collection.create_index([('parent', ASCENDING)])
    collection.create_index([('left', ASCENDING)])
    collection.create_index([('right', ASCENDING)])

    root_id = collection.insert({'_id': '0', 'name': 'root', 'parent': None, 'ancestors': []})
    for fid in [str(i) for i in range(1, 8)]:
        _fid = collection.insert({ 'name': fid + '.' + g.generate_sentence()[2], 'parent': root_id, 'ancestors': [root_id]})

        for sid in [fid + '.' + chr(i) for i in range(ord('A'), ord('Z') + 1)]:
            _sid = collection.insert({'name': sid + '.' + g.generate_sentence()[2], 'parent': _fid, 'ancestors': [root_id, _fid]})

            for ssid in [sid + '.' + str(i) for i in range(1, 200)]:
                _ssid = collection.insert({'name': ssid + '.' + g.generate_sentence()[2], 'parent': _sid, 'ancestors': [root_id, _fid, _sid]})

                for lid in [ssid + '.' + chr(i) for i in range(ord('a'), ord('z') + 1)]:
                    collection.insert({'name': lid + '.' + g.generate_sentence()[2], 'parent': _ssid, 'ancestors': [root_id, _fid, _sid, _ssid], 'leaf': True})
    updateNode(collection, root_id, 1)

def buildGraph(collection):
    collection.drop();
    graph = {'name': 'root', 'children': []}
    for fid in [str(i) for i in range(1, 8)]:
        fchild = {'name': fid + '.' + g.generate_sentence()[2], 'children': []}
        graph['children'].append(fchild)
        for sid in [fid + '.' + chr(i) for i in range(ord('A'), ord('C') + 1)]:
            schild = {'name': sid + '.' + g.generate_sentence()[2], 'children':[]}
            fchild['children'].append(schild)
            for ssid in [sid + '.' + str(i) for i in range(1, 3)]:
                sschild = {'name': ssid + '.' + g.generate_sentence()[2], 'children': []}
                schild['children'].append(sschild)
                for lid in [ssid + '.' + chr(i) for i in range(ord('a'), ord('c') + 1)]:
                     lchild = {'name': lid + '.' + g.generate_sentence()[2], 'children':[]}
                     sschild['children'].append(lchild)
    collection.insert(graph)

def updateNode (collection, id, left):
    right = left + 1
    for node in collection.find( {'parent': id}).sort('name'):
        right = updateNode(collection, node['_id'], right) + 1
    collection.update({'_id': id}, { '$set': {'left':left, 'right': right}})
    return right

if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')
    db = client.dummydata

    #buildParentRef(db.parent_ref)
    #buildChildRef(db.child_ref)
    #buildAncestorsArray(db.ancestor_array)
    #buildMaterializedPath(db.materialized_path)
    # buildNestedSets(db.nested_set)
    buildKitchenSink(db.kitchen_sink)
    #buildGraph(db.graph)
