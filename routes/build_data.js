var express = require('express');
var router = express.Router();

/* GET build_dataa */
router.get('/', function(req, res, next) {
  var db = req.db;
  var collection = db.collection('foobar');
  collection.drop();
  collection.insert({test:'this'}, function(err, result) {
    if (err){
      return next(err);
    }
    res.send(result);
  });
});

module.exports = router;

