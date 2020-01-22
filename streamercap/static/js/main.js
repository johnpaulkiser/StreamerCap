
function getIndex(){
    const table = document.getElementById("table");
    fetch('http://localhost:8000/default')
        
        .then((response) => {
        return response.json();
    })
    .then((streams) => {
        streams = streams["data"];
        console.log(streams[0]);
        /*
        for each stream in streams["data"]
            create new table row element
            addRow(element, stream);

        */
       
        for(let i = 0; i < streams.length; i++){
            let row = table.insertRow(-1);
            streams[i]["rank"] = i+1;
            populateRow(row, streams[i]);    
        }

    });

}

function populateRow(row, stream) {
    
    let classNames = Object.keys(stream);

    classNames.forEach(className => {
        let cell = row.insertCell();
        cell.innerHTML = stream[className];
        cell.classList.add(className);
    });
}


//TODO create title shortener
//TODO create table links

function shortenTitle() {

}