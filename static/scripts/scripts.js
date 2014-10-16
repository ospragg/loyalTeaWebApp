var header = document.getElementById("header");
header.addEventListener("touchstart", touchStarted, false);

var prev_time;
var dt = 100.0;
var n_raw_data = 20;
var raw_data = [];
var n_packet = 2 + 8;
var indexed_touch_locs = [];
var touch_sepperation = 50.0;
var stampID = 0;
var tolerance = 0.2;

function resetTFC() {
    resetRawData();
    loadHeader();
}
function resetRawData() {
    var temp_event = raw_data[0];
    raw_data = [];
    raw_data.unshift(temp_event);

    indexed_touch_locs = [];

    stampID = 0;
}
function loadTouchEventToRawData(touch_event) {
    // calculate the dt, and add it to the event object
    var cur_time = touch_event.timeStamp;
    touch_event.dt = (cur_time - prev_time);
    prev_time = cur_time;

    // add the new touch event to the beginnige of the array
    raw_data.unshift(touch_event);

    // remove the touch event from the end of the array
    if (raw_data.length > n_raw_data) {
        raw_data.pop();
    }

    // if the event dt is significantly larger than the required dt, reset the buffer
    if (touch_event.dt > (dt * (1.0 + tolerance))) {
        resetRawData();
        return;
    }
}
function checkValidDT() {
    // make sure the dts of all but the last touch event are within bounds
    for (i = 0; i < raw_data.length - 1; i++) {
        if (raw_data.dt > (dt * (1.0 + tolerance)) ||
            raw_data.dt < (dt * (1.0 - tolerance))) {
            return 0;
        }
    }
    return 1;
}
function identifyTouchIndex(touch_event) {
    // for each of the recorded touch locations...
    for (j = 0; j < indexed_touch_locs.length; j++) {
        // if the touch location has already been recorded...
        if (touch_event.changedTouches[0].pageX > indexed_touch_locs[j].changedTouches[0].pageX - touch_sepperation &&
            touch_event.changedTouches[0].pageX < indexed_touch_locs[j].changedTouches[0].pageX + touch_sepperation &&
            touch_event.changedTouches[0].pageY > indexed_touch_locs[j].changedTouches[0].pageY - touch_sepperation &&
            touch_event.changedTouches[0].pageY < indexed_touch_locs[j].changedTouches[0].pageY + touch_sepperation) {
            // then return the index
            return j;
        }
    }

    // then save that touch location and incriment n_touch_locations for the next location
    indexed_touch_locs.push(touch_event);

    // return the index of the touch
    return indexed_touch_locs.length - 1;
}
function convertFromPacketToDecimal(data_array) {
    // convert the binary packet into a decimal
    var dec = 0;
    for (k = 0; k < data_array.length; k++) {
        dec = dec + ((1<<k) * data_array[k]);
    }
    return dec;
}
function touchStarted(event) {
    // don't register the touch if we've already found some data
    if (stampID != 0) {
        return;
    }

    // load the data to the raw data buffer
    loadTouchEventToRawData(event);

    // if we've received the right nuber of bits...
    if (raw_data.length == n_packet &&
        checkValidDT() == 1) {
        var packet = [];
        indexed_touch_locs = [];
        for (i = raw_data.length - 1; i >= 0; i--) {
            var temp = identifyTouchIndex(raw_data[i]);
            packet.push(temp);
        }

        if (packet[0] == 0 &&
            packet[1] == 1) {
            var data_array = [];
            var offset = 2;
            for (m = offset; m < packet.length; m++) {
                data_array.push(packet[m]);
            }
            stampID = convertFromPacketToDecimal(data_array);

            stampRecorded(stampID, 1);

        } else {
            stampID = 0;
        }
    }

    if (event.dt < 300) {
        event.preventDefault();
        return false;
    }
}


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

function stampRecorded(stamp_id, stamp) {
    $( "img#header" ).attr( "src", requestHTML("/record_stamp?uuid=" + localStorage.getItem("UUID") + "&stamp_id=" + stamp_id + "&stamp=" + stamp) );
    loadCafeTable();

    document.body.scrollTop = document.documentElement.scrollTop = 0;
}

// initialise page
function initialise() {
    checkForUUID();
    loadCafeTable();
    
    var height = window.innerHeight;
    var width = window.innerWidth;
    document.getElementById("header").style.height = height + "px";
    document.getElementById("header").style.width = width + "px";
    //getElementById('header').style.width = width + "px";
    //getElementById('header').style.height = height + "px";

    //document.getElementById("cafeTable").style.width = width + "px";
    //$( "img#header" ).attr( "style",
}

function go_to_cafe(cafe_id) {
    stampRecorded(217, 0);
}


