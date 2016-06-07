var request = require("request");

var parseHtml = function(html) {
console.log(html);
};

request("http://google.com/", function(error,response,body) {
    if (!error) {
        parseHtml(body);
    } else {
        console.log(error);
    }
});
