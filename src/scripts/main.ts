var eel: any;

function main() {
    setup();
}

function setup() {
    init_marquees(0.5);
    init_slideshows();
}

function init_slideshows() {
    const slideshows = document.getElementsByClassName("slideshow") as HTMLCollectionOf<HTMLElement>;
    for (const slideshow of slideshows) {
        const videos = slideshow.querySelectorAll("video");
        for (const video of videos) {
            video.addEventListener("ended", () => { progress_slideshow(slideshow); });
        }
        const first = slideshow.firstElementChild as HTMLElement;
        if (first.querySelector("img")) {
            setTimeout(progress_slideshow, parseInt(first.dataset.time), slideshow);
        } else {
            first.querySelector("video").play();
        }
    }
}

function progress_slideshow(slideshow: HTMLElement) {
    const slides = slideshow.children;
    for (var slide = 0; slide < slides.length; slide++) {
        const current = slides[slide] as HTMLElement;
        const next = slides[(slide + 1) % slides.length] as HTMLElement;
        if (current.style.display === "block") {
            current.style.display = "none";
            next.style.display = "block";
            if (next.querySelector("img")) {
                setTimeout(progress_slideshow, parseInt(next.dataset.time), slideshow);
            } else {
                next.querySelector("video").play();
            }
            break;
        }
    }
}

// function init_marquees() {
//     const speed = 0.5;

//     const vertical = document.getElementsByClassName("scrolling-vertical") as HTMLCollectionOf<HTMLElement>;
//     for (const current of vertical) {
//         const marquee = current.firstElementChild as HTMLElement;
//         const copies = Math.max(Math.round(2 / (current.querySelector("p").offsetHeight / current.offsetHeight)), 2);
//         for (var i = 0; i < copies - 1; i++) {
//             marquee.appendChild(current.querySelector("p").cloneNode(true));
//         }
//         marquee.animate([
//             { transform: "translateY(0)" },
//             { transform: `translateY(-${100 / copies}%)` }
//         ], {
//             duration: marquee.offsetHeight / speed,
//             iterations: Infinity
//         });
//     }

//     const horizontal = document.getElementsByClassName("scrolling-horizontal") as HTMLCollectionOf<HTMLElement>;
//     for (const current of horizontal) {
//         const marquee = current.firstElementChild as HTMLElement;
//         const copies = Math.max(Math.round(2 / (current.querySelector("p").offsetWidth / current.offsetWidth)), 2);
//         for (var i = 0; i < copies - 1; i++) {
//             marquee.appendChild(current.querySelector("p").cloneNode(true));
//         }
//         marquee.animate([
//             { transform: "translateX(0)" },
//             { transform: `translateX(-${100 / copies}%)` }
//         ], {
//             duration: marquee.offsetWidth / speed,
//             iterations: Infinity
//         });
//     }
// }

function init_marquees(speed: number) {
    const marquees = [["vertical", "Height", "Y"], ["horizontal", "Width", "X"]];
    for (const type of marquees) {
        const scrolling = document.getElementsByClassName(`scrolling-${type[0]}`) as HTMLCollectionOf<HTMLElement>;
        for (const current of scrolling) {
            const marquee = current.firstElementChild as HTMLElement;
            const copies = Math.max(Math.round(2 / (current.querySelector("p")[`offset${type[1]}`] / current[`offset${type[1]}`])), 2);
            for (var i = 0; i < copies - 1; i++) {
                marquee.appendChild(current.querySelector("p").cloneNode(true));
            }
            marquee.animate([
                { transform: `translate${type[2]}(0)` },
                { transform: `translate${type[2]}(-${100 / copies}%)` }
            ], {
                duration: marquee[`offset${type[1]}`] / speed,
                iterations: Infinity
            });
        }
    }
}

function refresh_page() {
    location.reload();
}

document.addEventListener('DOMContentLoaded', main);
eel.expose(refresh_page);