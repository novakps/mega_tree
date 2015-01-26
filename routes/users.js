var express = require('express');
var router = express.Router();

/* GET users. */
router.get('/userlist', function(req, res, next) {
  var db = req.db;
  db.collection('userlist').find().toArray(function(err, items) {
    res.json(items);
  });
});

module.exports = router;
