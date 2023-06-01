const Submit = async() => {
    let username = document.getElementById("username").value;

    try {
        const response = await fetch("127.0.0.1/makeuser/s",{
            method: "POST", //get or post
            headers: {"Content-Type": "application/json;charset=utf-8"},
            body:JSON.stringify(username)
        })
        if (response) {
            const data = await response.text();
            localStorage.setItem('playerID', data);
        }
        
    } catch(e){
        console.log(e);
    }
}
