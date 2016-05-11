console.log('hello world')

function reqListener () {
  console.log(this.responseText);
}

var oReq = new XMLHttpRequest();
oReq.addEventListener("load", reqListener);
oReq.open("GET", "https://forums.warframe.com/forum/3-pc-update-build-notes/");
oReq.send();
