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
        var uuid = generateUUID();
        localStorage.setItem("UUID", uuid);

        //send that to the server and register them as a new user
        requestHTML("/new_user?uuid=" + uuid);
    } else {
        debug.innerHTML = localStorage.getItem("UUID");
    }
}

// reset the UUID
function resetUUID() {
    localStorage.removeItem("UUID");
}

// function to request HTML content from back end
function requestHTML(request) {
    var request_url = request;

    var xmlHttp = null;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", request_url, false );
    xmlHttp.send( null );

    return xmlHttp.responseText;
}

// load the cafe table
function loadCafeTable() {
    $( "#cafeTable" ).html( requestHTML("/cafe_table?uuid=" + localStorage.getItem("UUID")) );
}

function stampRecorded() {
    $( "#header").html( requestHTML("/record_stamp?uuid=" + localStorage.getItem("UUID") + "&stamp_id=217") );
    loadCafeTable()
}

// initialise page
function initialise() {
    checkForUUID();
    loadCafeTable();
}


