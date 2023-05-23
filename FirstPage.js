const sheet = new CSSStyleSheet();

AtStart();

let memeInfo = {
    cContent:[],
}

function AtStart() {
    FetchFirstData();
    AssignCaptions("caption1", "input1");
}

async function FetchFirstData(){
    var data;
    var response = await fetch("127.0.0.1/FirstPage?s=f&a=startgame");
    data = await response.json();
    console.log(data);

    let timer = 320;
    if (data){
        timer = data.time;
    }
    
    const inter = setInterval(function(){
        timer = CountTime(timer);
        if (timer <= -1){
            SubmitMeme();
            clearInterval(inter);
        }
    }, 1000);

    ReRollMeme(data.memeIndex,data.captions,data.styles)

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
        if (event.target.innerHTML.length >= 100){
            event.target.innerHTML = caption1.innerHTML;
        }
        else {
            caption1.innerHTML = event.target.innerHTML;
            if (caption1.innerHTML.length >= 50){
                caption1.style.fontSize = `${1.25 - caption1.innerHTML.length/200}vw`;
                event.target.style.fontSize = `${1.25 - event.target.innerHTML.length/200}vw`;
            }
        }
    })
}

async function ReRollMeme(memeIndex, captions, styles) {
    //fetch the meme id and the caption amount, also make sure that if the meme is changed manualy the server wont give the mene

    let data = {
        memeIndex,
        captions,
        styles,
    }

    memeInfo = {...data,...memeInfo};
    let inputDiv = document.getElementById("inputDiv");
    let meme = document.getElementById("meme");
    let cd = document.getElementById("c1d");
    let inputField = document.getElementById("input1");
   
    sheet.replaceSync(data.styles);
    document.adoptedStyleSheets = [sheet];

    for (var i =1; i< data.captions; i++) {
        let cdClone = cd.cloneNode(true);
        cdClone.id = `c${i+1}d`;
        cdClone.childNodes[1].id = `caption${i+1}`;
        cdClone.childNodes[1].className = `meme_caption`;
        cdClone.childNodes[1].innerHTML = `Caption ${i+1}`;
        meme.appendChild(cdClone);

        let inputClone = inputField.cloneNode(true);
        inputClone.innerHTML = `Caption ${i+1}`;
        inputClone.id = `input${i+1}`;
        inputDiv.appendChild(inputClone);

        AssignCaptions(`caption${i+1}`,`input${i+1}`);

    }

}

function SubmitMeme() {
    
    //add all of the text from the captions to the meme info
    for (var i =1; i <= memeInfo.captions; i++){
        memeInfo.cContent.push(document.getElementById(`caption${i}`).innerHTML);
    }
    try{
        fetch(`127.0.0.1/FirstPage?s=t&i=${memeInfo.memeIndex}&c=[${memeInfo.cContent}]`,{
            method: "GET", //get or post
            headers: {"Content-Type": "application/json;charset=utf-8"}
        }).then(response => console.log(response.text()))
        
    }catch(err){
        console.log(err);
    }
    //create a var for post request which contains everything that is needed so that the server will keep the meme
    //example:
    // var finalMeme = {
    //     memeNumer,
    //     url:`${MemeUrl}`,
    //     text: [`${caption1.innerHTML}`, `${caption2.innerHTML}`]
    // };

    //fetch the post request and transfer user to the waiting page
    //window.location.replace("WaitingPage.html");
}