let IsTimeUp = false;
AtStart();

function AtStart() {
    FetchFirstData();
    AssignCaptions("caption1", "input1");
}

async function FetchFirstData(){

    //setting up the timer and changing the IsTimeUp bool once time is up
    let timer = 20;
    const inter = setInterval(function(){
        timer = CountTime(timer);
        if (timer <= -1){
            IsTimeUp = true;
            clearInterval(inter);
        }
    }, 1000);
} 

function CountTime(timer) {
    let seconds = timer % 60;
    let minutes = Math.floor(timer / 60);
    document.getElementById("timer").innerHTML = `${minutes < 10 ? `0${minutes}`: minutes}: ${seconds < 10 ? `0${seconds}`:seconds}`;
    return timer -1;
}

//Assigning an EventListener to a caption and an input so that when i change the input the caption will change too
function AssignCaptions(captionId,inputId){
    let caption1 = document.getElementById(captionId)
    console.log("hi");
    document.querySelector(`#${inputId}`).addEventListener("input", async (event) => {
        caption1.innerHTML = event.target.innerHTML;
    })
}

async function ReRollMeme() {
    //fetch the meme id and the caption amount, also make sure that if the meme is changed manualy the server wont give the mene
}

function SubmitMeme() {
    //create a var for post request which contains everything that is needed so that the server will keep the meme
    //example:
    // var finalMeme = {
    //     memeNumer,
    //     url:`${MemeUrl}`,
    //     text: [`${caption1.innerHTML}`, `${caption2.innerHTML}`]
    // };

    //fetch the post request and transfer user to the waiting page
}