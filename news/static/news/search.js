const search_icon = document.getElementById("search-icon");
const search_input = document.getElementById("search-input");
const search_icon_link = document.getElementById("search-icon-link");

search_icon.addEventListener("click", show_input);
document.addEventListener('keydown', enter_pressed);

function show_input(event){
    search_input.classList.toggle("expanded");
    search_input.focus();
    event.preventDefault();
    search_icon.removeEventListener("click", show_input);
    search_icon.addEventListener("click", set_url);
}

function set_url(){
    search_icon_link.setAttribute("href", `${window.location.pathname.slice(0,3)}/search?search=${search_input.value}`);
}

function enter_pressed(event){
    if(event.key === "Enter" && document.activeElement === search_input){
        window.location.href = `${window.location.pathname.slice(0,3)}/search?search=${search_input.value}`;
    }
}