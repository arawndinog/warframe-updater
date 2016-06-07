var request = require("request");
var cheerio = require("cheerio");
// var PythonShell = require("python-shell");
var fs = require("fs");

var pcBL = "https://forums.warframe.com/forum/3-pc-update-build-notes/";
var xbBL = "https://forums.warframe.com/forum/253-xb1-update-build-notes/";
var psBL = "https://forums.warframe.com/forum/152-ps4-update-build-notes/";

function getPrimeLink(html) {
    $ = cheerio.load(html);
    var primeLink = $("a[href*='prime-gear-drop-locations']").first().attr('href');
    console.log(primeLink);
    return primeLink;
};

function getPrimeList(html) {
    $ = cheerio.load(html);
    var primeList = $("article.ipsBox.ipsPad").text().trim().replace(/^\t/gm, "").replace(/^\n/gm, "");
    var lines = primeList.split('\n');
    var resultStr = "";
    for (var i = 0; i<lines.length; i++) {
        resultStr += (lines[i].trim() + "\n");
    }
    return resultStr;
};

function writeToFile(primeList,platform) {
    fs.writeFile(platform + "_output.txt",primeList);
}

request(pcBL, function(error,response,body) {
    if (!error) {
        var primeLink = getPrimeLink(body);
        request(primeLink, function(error,response,body){
            var primeList = getPrimeList(body);
            writeToFile(primeList, "PC");
        })
    }
});

request(xbBL, function(error,response,body) {
    if (!error) {
        var primeLink = getPrimeLink(body);
        request(primeLink, function(error,response,body){
            var primeList = getPrimeList(body);
            writeToFile(primeList, "XB1");
        })
    }
});

request(psBL, function(error,response,body) {
    if (!error) {
        var primeLink = getPrimeLink(body);
        request(primeLink, function(error,response,body){
            var primeList = getPrimeList(body);
            writeToFile(primeList, "PS4");
        })
    }
});

// var python_options = {
//     pythonPath: '/usr/bin/python2',
// }

// PythonShell.run('generate_droptable.py', python_options, function(err) {
//     if (err) throw err;
//     console.log('Done');
// })