var request = require("request");

request("https://forums.warframe.com/forum/3-pc-update-build-notes/", function(error,response,body) {
    if (!error) {
        console.log(body);
    } else {
        console.log(error);
    }
});
