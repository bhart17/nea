document.addEventListener('DOMContentLoaded', (event) => { main() });

function main() {
    showSlides(0);
    scroll_text();
}

function showSlides(current) {
    var slides = document.getElementsByClassName("mySlides");
    slideIndex = (current++ < slides.length) ? current++ : 1;
    for (const slide of slides) {
        slide.style.display = "none";
    }
    slides[slideIndex - 1].style.display = "block";
    setTimeout(showSlides.bind(this, slideIndex), 2000);
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