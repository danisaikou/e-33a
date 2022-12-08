// Initialize time clock
let time = 0;
// Initilaie timer 
let timer = null;

//Start timer
function startTimer() {
    // if not running, start
    if (!timer) {
        timer = setInterval(function() {
            time++;
            //update display with new time
            updateTimeDisplay();
        }, 1000);
    }
}

function stopTimer() {
    //if running, stop
    if (timer) {
        clearInterval(timer);
        timer=null;
    }
}

//update display
function updateTimeDisplay() {
    //get current time in h/m/s
    let hours = Math.floor(time / 3600);
    let minutes = Math.floor((time % 3600) / 60 );
    let seconds = time % 60;

    //format time as stringformat
    let timeString = `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;

    // update time display with fomratted string
    document.getElementById("time-display").innerHTML = timeString;
}

function stopTimerAndSaveTime() {
    // stop the timer
    stopTimer();

    // send time to server 
    fetch
}