let filterBy = {
    "page": 1,
    "platform": [],
    "game": [],
    "language": []
}





document.getElementById("goto-top").addEventListener("click", ()=>{
    window.scrollTo({ top: 0, behavior: 'smooth' });
})



//
//
/* Queries filter button data */
//
//

// category fields are identical to their respective button ids
// & get request field parameter
let filter_categories = ["game", "platform", "language"];

initFilters(filter_categories);
addCategoryListeners(filter_categories);

function initFilters(categories){
    
    categories.forEach(category => {
        // get top 10 in category
        getFilterData(category, 1).then((response) =>{
            let wrapper = document.getElementById(category+"-wrapper");
            //create button for every item in response
            response.data.forEach(item => {
                let btn = document.createElement("button");
                btn.innerHTML = item;
                btn.category = category;
                btn.addEventListener("click", toggleFilter)
                if (category === "platform")
                    btn.setAttribute("id", item)
                wrapper.append(btn);
            });
        });
    });
}

function toggleFilter(e){
    let btn = e.target;
    let category = btn.category;

    //check if button is already toggled
    if(filterBy[category].includes(btn.innerHTML)){
        
        let i = filterBy[category].indexOf(btn.innerHTML);
        if (i > -1) 
            filterBy[category].splice(i, 1); //remove element from list
        btn.classList.remove("button-toggle");
    } else{
        filterBy[category].push(btn.innerHTML);
        btn.classList.add("button-toggle");
    }
    flushTable();
    updateTableByFilters(filterBy);
}


function addCategoryListeners(categories){
    categories.forEach(category => {
        document.getElementById(category).addEventListener("click", (e)=> {
            let wrapper = document.getElementById(`${category}-wrapper`);
            console.log(wrapper.style.display);
            if( wrapper.style.display === "none" || wrapper.style.display === ""){
                wrapper.style.display = "flex";
                e.target.classList.add("button-toggle");
            } else {
                wrapper.style.display = "none";
                e.target.classList.remove("button-toggle");
            }
        })
    });
}


async function getFilterData(field, page){
    /*  response format:
        {data: ["item1", "item2", "item3", ... ]}
    */
    const response = await fetch(`http://localhost:8000/${field}/${page}`)
    return await response.json();
}



//
//
/* Queries Table Data */
//
//
updateTableByFilters(filterBy);

// gets 100 more table items according to global filter
document.getElementById("load-more").addEventListener("click", () => {
    filterBy["page"]++;
    updateTableByFilters(filterBy);
    console.log(filterBy);
})

async function getPageData(data = {}){
    
    const response = await fetch('http://localhost:8000/', {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filterBy)

    });
    return await response.json();
}


function updateTableByFilters(filterBy){
    let table = document.getElementById("table");
    getPageData(filterBy).then((streams) => {
        streams = streams["data"];
        for(let i = 0; i < streams.length; i++){
            let row = table.insertRow(-1);
            streams[i]["rank"] = 100 * (filterBy["page"]-1) + i + 1; // keeps track of rank, needs refactor
            populateTableRow(row, streams[i]);    
        }
    });
}

function flushTable(){
    const table = document.getElementById("table").firstElementChild;
    
    while (table.childNodes.length > 1) {
        table.removeChild(table.lastChild);
    }
    filterBy["page"] = 1;
}


function populateTableRow(row, stream) {

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


/* Extra page functionality */