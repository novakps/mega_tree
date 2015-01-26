var express = require('express');
var ObjectId = require('promised-mongo').ObjectId;
var router = express.Router();

/* GET data */
router.get('/data/:id', function(req, res, next) {
  var collection = req.db.collection('nested_set');
  var filterJson = req.query.filter;
  if (filterJson) {
    // return filtered tree
    var filter = JSON.parse(filterJson);
    var re = new RegExp(filter[0].value);
    var matchedLeafs = { $match : { name: re, leaf: true } };
    var sortLeftAscending = { $sort: { left: 1 }};
    var limit100 = { $limit: 100 };

    collection.aggregate([
      matchedLeafs,
      sortLeftAscending,
      limit100
      ], function(err, leafs) {
        res.json(leafs);
      });
  } else {
    // return direct children nodes
    var id = req.params.id
    if (id !== '0') {
       id = ObjectId(req.params.id);
    }
    collection.find({parent: id}, {name: 1, leaf: 1}).sort({name: 1}).toArray(function(err, items) {
      res.json(items);
    });
  }
});

/* GET html */
router.get('/view', function(req, res, next) {
    res.render('index', { title: 'Nested Set' }); 
});

module.exports = router;
