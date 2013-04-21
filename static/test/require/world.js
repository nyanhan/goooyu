define(function(require, exports) {

    var tmpl = require("test");

    exports.say = function(word){
        document.body.innerHTML = (tmpl({ hello: word }));
    };
});