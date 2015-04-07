/*global incremental  */
var express = require('express');
var router = express.Router();
var ObjectId = require('promised-mongo').ObjectId;
var q = require('q');

/* get direct child nodes */
router.get('/:parent_id', function(req, res, next) {
  var id = req.params.parent_id;

  if (id !== '0') {
    id = ObjectId(req.params.parent_id);
  }
  var collection = req.db.collection('kitchen_sink');
  collection
  .find({parent: id}, {name: 1, leaf: 1, column_type: 1})
  .sort({name: 1})
  .toArray(function(err, items) {
    res.json(items);
  });
});

/* post for incremental seaarch */
router.post('/search/:ignored', function(req, res) {
  var skip = 0;
  var limit = 100;
  var collection = req.db.collection('kitchen_sink');

  if (!req.body.filter) {
    res.json([]);
    return;
  }

  var filterParams = JSON.parse(req.body.filter);
  var filters = filterParams.map(function(param) {
    console.log(param);
    var re = new RegExp(param.value);
    return { $match : { name: re, leaf: true } };
  });
  var matched = { $or : filters };
  matched = filters[0];
  console.log(matched)
  var sortLeftAscending = { $sort: { left: 1 }};
  var skip2 = { $skip: skip};
  var limit2 = { $limit: limit};
  var groupIds = { $group: {'_id': '$ancestors', 'leafs': {$push: '$_id'}}};
  var unionAllIds = { $project: {_id: { $setUnion: [ '$_id', '$leafs' ]}}};
  var unwindId = { $unwind: '$_id'};
  var groupById = { $group: {_id: '$_id'}};

  var loadChildNodes = function(parentNode, filterNodeIds) {
    return collection.find({parent: parentNode._id, _id: { $in: filterNodeIds } },
                           {name: 1, column_type: 1, left: 1, leaf: 1})
           .sort( { left: 1 }).toArray()
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
    matched,
    sortLeftAscending,
    skip2,
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
});

module.exports = router;
