var source_url = "http://localhost:8080";
//var source_url = "http://idoenjoyanicecupoftea.appspot.com";
//var source_url = "";
var header_dim = "width:320px"

var header = document.getElementById("header");
var cafeTable = document.getElementById("cafeTable");

var debug = document.getElementById("debug");


// get the header image to start listening for touches
header.addEventListener("touchstart", touchStarted, false);


// generate the UUID
function generateUUID() {
    var d = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,
        function(c) {
            var r = (d + Math.random()*16)%16 | 0;
            d = Math.floor(d/16);
            return (c=='x' ? r : (r&0x7|0x8)).toString(16);
        }
        );
    return uuid;
}
// check if a UUID for the browser has beem created, and create one if it hasn't
function checkForUUID() {
    if (localStorage.getItem("UUID") == null) {
        debug.innerHTML = "No data saved";
        localStorage.setItem("UUID", generateUUID());
    } else {
        debug.innerHTML = localStorage.getItem("UUID");
    }
}
// reset the UUID
function resetUUID() {localStorage.removeItem("UUID");}
// load the header image
function loadHeader() {
    var img_url = source_url + "/static/images/header.jpg";
    header.innerHTML = "<img src = '"
    + img_url
    + "' style = '"
    + header_dim
    + "'>";
}
// load the cafe table
function loadCafeTable() {
    var string = "";
    for (i = 0; i < 1; i++) {
        string = string + "<img src = '" + source_url + "/static/images/Cafe_data/dose_espresso/0_cell.jpg' style = 'width:320px'><br>";
    }
    cafeTable.innerHTML = string;
}

function stampRecorded() {
    var request_url = source_url
    + "/pageStampedRedirectToCardImageURL/"
    + localStorage.getItem("UUID")
    + "/"
    + "217";

    var xmlHttp = null;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", request_url, false );
    xmlHttp.send( null );

    //debug.innerHTML = xmlHttp.responseText;
    /*
    header.innerHTML = "<img src = '"
    + img_url
    + "' style = '"
    + header_dim
    + "'>";
    */
    header.innerHTML = xmlHttp.responseText;
}

// initialise page
function initialise() {
    checkForUUID();
    loadHeader();
    loadCafeTable();
}


