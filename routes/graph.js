var express = require('express');
ObjectID = require('mongoskin').ObjectID;
var router = express.Router();

/* GET data */
router.get('/data/:id', function(req, res, next) {
  var collection = req.db.collection('graph');
  var filterJson = req.query.filter;
  if (filterJson) {
    var filter = JSON.parse(filteJson);
    var re = new RegExp(filter[0].value);

  } else {
    var id = req.params.id ? new ObjectID(req.params.id) : null;
    
  }
});

/* GET view */
router.get('/view', function(req, res, next) {
  res.render('index', { title: 'Graph' });
});

/* GET rebuild */
router.get('/rebuild', function(req, res, next) {
  var collection = req.db.collection('graph');
  collection.drop();
  collection.insert({_id: '0', name: 'root'}, function(err, result) {
    if (err) {
      return next(err);
    }
    res.json(result);
  });
});

module.exports = router;
