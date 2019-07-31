function init(){
    console.log(1);
    fetch("/popular")
    .then(response=>response.json())
    .then(data=>{
        //console.log(jsonObj)
        generateButton(data)
    })
    .catch(error => console.error('Error:', error));
}

function urlwparam(url, params){
    if (params) {
            let paramsArray = [];
            Object.keys(params).forEach(key => paramsArray.push(key + '=' + params[key]))
            if (url.search(/\?/) === -1) {
                url += '?' + paramsArray.join('&')
            } else {
                url += '&' + paramsArray.join('&')
            }
    }
    console.log(url);
    return url;
}
function movieSearch(){
    search=document.querySelector(".movie-search-button");
    search.addEventListener("click", function(e){
        var params = {'query': document.querySelector(".movie-search-input").value}
        var url = urlwparam("/search", params);
        fetch(url)
        .then(response=>response.json())
        .then(data=>{
            console.log(JSON.stringify(data))
            while (display.hasChildNodes()) {
                display.removeChild(display.lastChild);
            }
            generateButton(data)
        })
        .catch(error=> console.error("Error", error))
    })
}

function generateButton(data){
    var jsonObj = JSON.parse(JSON.stringify(data));
    for(var key in data){
        if (data.hasOwnProperty(key)){
            childElement = document.createElement('button');
            displayElement = display.appendChild(childElement);
            displayElement.innerHTML = data[key][0]["movie_name"];
            displayElement.classList.add("btn", "btn-outline-secondary", "btn-sm", "m-1", "display-elem");
            displayElement.addEventListener('click', function(e){
                e.stopPropagation();
                console.log(e.target.innerText)
                //console.log(e.target.innerHTML);
                for(var key in jsonObj){
                    if (data.hasOwnProperty(key)){
                        if (jsonObj[key][0]["movie_name"]===e.target.innerText){
                            console.log(jsonObj[key][0])
                            document.querySelector('#id_movie_name').value=jsonObj[key][0]["movie_name"];
                            document.querySelector('#id_release_date').value=jsonObj[key][0]["release_date"];
                            document.querySelector('#id_rating').value=jsonObj[key][0]["rating"];
                            document.querySelector('#id_overview').value=jsonObj[key][0]["overview"];
                            document.querySelector('#download-url').value=jsonObj[key][0]["poster_path"];
                            console.log(document.querySelector('#download-url').value);
                        }
                    }
                }
            })
        }
    }
}

display = document.querySelector('.display-result');
init();
movieSearch();



