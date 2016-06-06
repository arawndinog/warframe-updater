var request = require("request");
var cheerio = require("cheerio");

var pcBL = "https://forums.warframe.com/forum/3-pc-update-build-notes/";
var xbBL = "https://forums.warframe.com/forum/253-xb1-update-build-notes/";
var psBL = "https://forums.warframe.com/forum/152-ps4-update-build-notes/";

function getPrimeLink(html) {
    $ = cheerio.load(html);
    return $("a[href*='prime-gear-drop-locations']").first().attr('href');
};

request(pcBL, function(error,response,body) {
    if (!error) {
        var primeLink = getPrimeLink(body);
        console.log(primeLink);
        request(primeLink, function(error,response,body){
            console.log(body);
        })
    } else {
        console.log(error);
    }
});