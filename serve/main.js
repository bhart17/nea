document.addEventListener('DOMContentLoaded', () => { main() });

function main() {
    setup_slides();
    progress_slides();
    //scroll_text();
}

function setup_slides() {
    for (const container of document.getElementsByClassName("slideshow-container")) {
        container.children[0].style.display = "block";
    }
}

function progress_slides() {
    var containers = document.getElementsByClassName("slideshow-container");
    for (const container of containers) {
        const current = container.children;
        for (var slide_index = 0; slide_index < current.length; slide_index++) {
            if (current[slide_index].style.display === "block") {
                current[(slide_index + 1) % current.length].style.display = "block";
                current[slide_index].style.display = "none";
                break;
            }
        }
        // var slide_index = (current++ < slides.length) ? current++ : 1;
        // for (const slide of slides) { slide.style.display = "none" }
        // slides[slide_index - 1].style.display = "block";
        // setTimeout(progress_slides.bind(this, slide_index), 2000);
    }
    setTimeout(progress_slides, 2000);
}

function scroll_text() {
    var scrolling_text = document.getElementsByClassName("marquee");
    for (var element of scrolling_text) {
        const speed = 5;
        const time = element.children[0].offsetWidth / (2 * speed);
        console.log(time);
        element.style.animation = "marquee 15s linear infinite;";
    }
}

// for (var slide; slide < slides.length; slide++) {
//     slides[i].style.display = (slide === slideIndex - 1) ? "block" : "none";
// }