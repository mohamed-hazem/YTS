// Vars
let search = document.querySelector("#search");
let resultsDiv = document.querySelector("#results-div");
let loaderDiv = document.querySelector("#loader");

// On load
search.focus();

fakeData = [{
    rating: "HD",
    img: "https://img.hdtoday.tv/xxrz/250x400/394/1e/c6/1ec694a9d587d509ec7a9be815aacfac/1ec694a9d587d509ec7a9be815aacfac.jpg",
    title: "Avatar: The Way Of Water",
    year: "2022",
    duration: "2hr 49min",
    quality: "1080p Bluray",
    dl: "https://www.google.com",
    size: "1.9 GB"
}];

// Fetch Search Results
function getResults() {
    loader();

    fetch("/search?search_key="+search.value)
    .then(response => response.json())
    .then(results => showResults(results))
    .catch(e => console.log(e));

}

function showResults(results) {
    search.value = "";
    search.focus();
    clearDiv(resultsDiv);
    loader(false);

    results.forEach(result => {
        addResult(result);
    });

    // Add Event Listner
    let links = document.querySelectorAll(".dl");
    Array.from(links).forEach(function(element) {
    element.addEventListener('click', getCurrentResults);
    }); 
}

// Loader
function loader(show=true) {
    let d = (show) ? "flex" : "none";
    loaderDiv.style.display = d;
}

// Add Result
function addResult(result) {
    // Main Div
    let mainDiv = document.createElement("div");
    mainDiv.setAttribute("class", "col-lg-2 col-md-6 col-sm-12 d-flex justify-content-center align-self-center");
    
    // Item Div
    let itemDiv = document.createElement("div");
    itemDiv.setAttribute("class", "item position-relative");

    let a = document.createElement("a");
    a.setAttribute("href", result['dl']);
    a.setAttribute("class", "dl");
    a.setAttribute("title", result['title'])
    a.setAttribute("data-id", result['imdb_id']);
    a.setAttribute("data-title", result['title']);
    a.setAttribute("data-year", result['year']);

    let spanQuality = document.createElement("span");
    spanQuality.setAttribute("class", "quality");
    spanQuality.textContent = result['rating'];

    // Img Div
    let imgDiv = document.createElement("div");
    imgDiv.setAttribute("class", "img-div position-relative");

    let img = document.createElement("img");
    img.setAttribute("class", "img-fluid")
    img.setAttribute("src", result['img']);
    
    // Specs Div
    let specsDiv = document.createElement("div");
    specsDiv.setAttribute("class", "specs text-center");

    let sizeSpan = document.createElement("span");
    sizeSpan.setAttribute("class", "size");
    sizeSpan.innerHTML = '<i class="fa-solid fa-folder"></i> '+result['size'];

    let durationSpan = document.createElement("span");
    durationSpan.setAttribute("class", "duration");
    durationSpan.innerHTML = '<i class="fa-solid fa-clock"></i> '+result['duration'];

    specsDiv.appendChild(sizeSpan);
    specsDiv.appendChild(durationSpan);

    // Movie Info
    let movieInfo = document.createElement("a");
    movieInfo.setAttribute("class", "movie-info");
    movieInfo.innerHTML = '<i class="fa-solid fa-info"></i>';
    movieInfo.setAttribute("href", result['movie_page']);
    movieInfo.setAttribute("target", "_blank");

    imgDiv.appendChild(img);
    imgDiv.appendChild(specsDiv);
    imgDiv.appendChild(movieInfo);

    // Detail Div
    let detailDiv = document.createElement("div");
    detailDiv.setAttribute("class", "detail ps-2");

    let title = document.createElement("h3");
    title.setAttribute("class", "title text-muted mt-1");
    title.textContent = result['title'];

    // Info Div
    let info = document.createElement("div");
    info.setAttribute("class", "info text-muted d-flex justify-content-between");

    let year = document.createElement("span");
    year.setAttribute("class", "year");
    year.innerHTML = '<i class="fa-regular fa-calendar"></i> '+result['year'];

    let qualityVersion = document.createElement("span");
    qualityVersion.setAttribute("class", "quality-version");
    qualityVersion.textContent = result['quality'];

    info.appendChild(year);
    info.appendChild(qualityVersion);

    // ------------- //
    
    detailDiv.appendChild(title);
    detailDiv.appendChild(info);
    
    // ------------- //
    
    itemDiv.appendChild(a);
    itemDiv.appendChild(spanQuality);
    itemDiv.appendChild(imgDiv);
    itemDiv.appendChild(detailDiv);
    
    // ------------- //
    mainDiv.appendChild(itemDiv);
    // ------------- //
    
    resultsDiv.appendChild(mainDiv);
}


// Show Subtitle Alert
function showAlert(data) {
    let alertDiv = document.querySelector("#success-alert");
    if (data['success']) {
        alertDiv.classList.add("alert-success");
        alertDiv.classList.remove("alert-danger");

        setTimeout(() => {
            fetch("/stop_server").then(window.close());
          }, 5000)
    }
    else {
        alertDiv.classList.add("alert-danger");
        alertDiv.classList.remove("alert-success");
    }
    alertDiv.classList.toggle("show");
    alertDiv.querySelector("strong").textContent = data['msg'];


}


// Help functions //
function clearDiv(div) {
    while (div.firstChild) {
        div.removeChild(div.firstChild);
    }
}


// EventListeners //
search.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        getResults();
    }
});

function getCurrentResults() {
    let id = this.getAttribute("data-id");
    let name = this.getAttribute("data-title");
    let year = this.getAttribute("data-year");
    
    fetch("/subtitle?imdb_id="+id+"&name="+name+"&year="+year)
    .then(response => response.json())
    .then(data => showAlert(data))
    .catch(e => console.log(e));
}