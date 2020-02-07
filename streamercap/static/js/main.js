let filterBy = {
    "page": 1,
    "platform": ["Twitch", "Mixer"],
    "game": ["League of Legends", "Fortnite", "Just Chatting"],
    "language": []
}

updatePageFilters(filterBy);

document.getElementById("goto-top").addEventListener("click", ()=>{
    window.scrollTo({ top: 0, behavior: 'smooth' });
})

document.getElementById("load-more").addEventListener("click", () => {
    console.log(filterBy)
    filterBy["page"]++;
    updatePageFilters(filterBy);
    console.log(filterBy);
})

function updatePageFilters(filterBy){
    getPageData(filterBy).then((streams) => {
        streams = streams["data"];
        console.log(streams[0]);
    
        for(let i = 0; i < streams.length; i++){
            let row = table.insertRow(-1);
            streams[i]["rank"] = 100 * (filterBy["page"]-1) + i + 1; // keeps track of rank, needs refactor
            populateRow(row, streams[i]);    
        }
    });
}


async function getPageData(data = {}){
    let table = document.getElementById("table");
    const response = await fetch('http://localhost:8000/', {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filterBy)

    });
    return await response.json();
}

function populateRow(row, stream) {

    /*  Example response object from server:
        {
            "rank": null,
            "streamer": "summit1g",
            "viewership": 34527,
            "category": "Escape from Tarkov",
            "platform": Twitch,
            "title": "just playing howerver..."
        }
    */

    
    let classNames = Object.keys(stream);
    const logos = {
        "Twitch": document.getElementById("twitch-logo").src,
        "Mixer": document.getElementById("mixer-logo").src
    }
    
    
    classNames.forEach(className => {
        let cell = row.insertCell();
        
        // creates hyperlink
        if (className === "streamer"){
            let url = "https://" + stream["platform"] + ".com/" + stream["streamer"];
            let link = document.createElement("a");
            link.href = url;
            link.innerHTML = stream[className];
            cell.appendChild(link);
        
        // creates truncated title dropdown
        }else if (className === "title" && stream[className].length > 25){
            let title = stream[className];
            let truncatedTitle = title.slice(0, 25);
            cell.innerHTML = truncatedTitle + "...";
            let tooltip = document.createElement("span");
            tooltip.classList.add("tooltip")
            tooltip.innerHTML = title;
            cell.appendChild(tooltip);   

        // add logo icons
        }else if (className === "platform"){
            let platform = stream["platform"];
            let img =  new Image();
            img.classList.add(platform);
            img.classList.add("logo");
            img.src = logos[platform];
            console.log(img.src);
            img.onclick = () => {
                window.open("https://www."+platform+".com/");
            };
            cell.appendChild(img);
            
        } else if (className === "viewership"){
            //gives viewer numbers commas
            cell.innerHTML = stream["viewership"].toLocaleString()
        } else
            cell.innerHTML = stream[className];
        
        cell.classList.add(className);
    });
}


