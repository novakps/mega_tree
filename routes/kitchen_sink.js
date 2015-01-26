/*global   */
var express = require('express');
var router = express.Router();
var lorem = require('lorem');
var ObjectId = require('promised-mongo').ObjectId;
var q = require('q');

/* GET data */
router.get('/data/:id', function(req, res, next) {
  var collection = req.db.collection('kitchen_sink');

  var filterJson = req.query.filter;

  if (filterJson) {
    // return filtered tree
    var filter = JSON.parse(filterJson);
    var re = new RegExp(filter[0].value);
    var matchedLeafs = { $match : { name: re, leaf: true } };
    var sortLeftAscending = { $sort: { left: 1 }};
    var limit2 = { $limit: 100};
    var groupIds = { $group: {'_id': '$ancestors', 'leafs': {$push: '$_id'}}};
    var unionAllIds = { $project: {_id: { $setUnion: [ '$_id', '$leafs' ]}}};
    var unwindId = { $unwind: '$_id'};
    var groupById = { $group: {_id: '$_id'}};

    var loadChildNodes = function(parentNode, filterNodeIds) {
      return collection.find({parent: parentNode._id, _id: { $in: filterNodeIds } }, {name: 1, left: 1, leaf: 1})
             .sort( {left:1}).toArray()
             .then(function(childNodes) {
               parentNode.children = childNodes;
               return q.all(childNodes.map(function(node) {
                 if (!node.leaf) {
                   node.expanded = true;
                 }
                 return loadChildNodes(node, filterNodeIds);
               }));
             })
             .then(function(childNodes) {
               return parentNode;
      });
    };

    var loadRootNode = collection.findOne({parent: null})

    var loadFilterNodeIds = collection.aggregate([
      matchedLeafs,
      sortLeftAscending,
      limit2,
      groupIds,
      unionAllIds,
      unwindId,
      groupById
      ])
    .then(function(treeNodes) {
      return treeNodes.map(function(node) {
        return node._id;
      });
    });

    q.all([loadRootNode, loadFilterNodeIds])
    .spread(loadChildNodes)
    .then(function(node) {
      res.json(node);
    });
  } else {
    // return direct children nodes
    var id = req.params.id
    if (id !== '0') {
       id = ObjectId(req.params.id);
    }
    collection
    .aggregate( [ { $match: {parent: id}},
                  { $sort: {left: 1} },
                  { $project: {name: 1} }
                ] )
    .then(function(items) {
      res.json(items);
    }).done();
  }
});

/* GET html */
router.get('/view', function(req, res, next) {
    res.render('index', { title: 'Kitchen Sink' }); 
});

module.exports = router;
