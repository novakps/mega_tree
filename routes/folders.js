var express = require('express');
ObjectID = require('mongoskin').ObjectID
var router = express.Router();

/* GET folders */
router.get('/:id', function(req, res, next) {
  var db = req.db;
  var filterJson = req.query.filter;
  if (filterJson) {
    var filter = JSON.parse(filterJson);
    var re = new RegExp(filter[0].value);
    db.collection('nested_set').find({name:re, leaf: true}).sort({name: 1}).limit(100).toArray(function(err, items) {
      res.json(items);
    });
  } else {
    var id = req.params.id ? new ObjectID(req.params.id) : null;
    db.collection('nested_set').find({parent: id}, {name: 1, leaf: 1}).sort({name: 1}).toArray(function(err, items) {p
      res.json(items);
    });
  }
});

module.exports = router;
