var express = require('express');
var router = express.Router();


/* Get html */
router.get('/', function(req, res, next) {
    res.render('index', { title: 'Add Column Tree' }); 
});

module.exports = router;
