var express = require('express');
var router = express.Router();
var ObjectId = require('promised-mongo').ObjectId;

/* get assays */
router.get('/:id', function(req, res, next) {
  var query = { column_type: 'Experimental Assays'};
  if (req.params.id) {
    query = { _id: ObjectId(req.params.id) };
  }
  var limit = parseInt(req.query.limit,10) || 100;
  var skip = parseInt(req.query.skip,10) || 0;
  var collection = req.db.collection('kitchen_sink');
  collection
  .find(query ,
        { ancestors: 0, parent: 0, right: 0, left: 0, leaf: 0 })
  .skip(skip)
  .limit(limit)
  .toArray(function(err, items) {
    res.json(items);
  });
});

module.exports = router;
