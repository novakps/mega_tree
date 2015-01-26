var express = require('express');
var router = express.Router();

/* search folders */
router.get('/', function(req, res, next) {
  var db = req.db;
  var regEx = new RegExp(req.query.text);
  db.collection('nested_set').find({name: regEx}).limit(100).sort( {left: 1} ).toArray(function(err, items) {
    res.json(items);
  });                               
});

module.exports = router;
