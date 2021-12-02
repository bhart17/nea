document.addEventListener('DOMContentLoaded', () => { main() });

function main() {
    progress_slides();
}

function progress_slides() {
    const containers = document.getElementsByClassName("slideshow-container");
    for (const container of containers) {
        const current = container.children;
        for (var slide_index = 0; slide_index < current.length; slide_index++) {
            if (current[slide_index].style.display === "block") {
                current[(slide_index + 1) % current.length].style.display = "block";
                current[slide_index].style.display = "none";
                break;
            }
        }
    }
    setTimeout(progress_slides, 2000);
}