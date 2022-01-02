var eel: any;

function main(): void {
    setup();
}

function setup(): void {
    init_rss_feeds();
    refresh_clocks();
    init_marquees();
    init_slideshows();
}

function init_rss_feeds(): void {
    const regex = /\${([^$]+)}([^$]*)/g
    const rss_feeds = document.getElementsByClassName("rss") as HTMLCollectionOf<HTMLElement>;
    for (const rss_feed of rss_feeds) {
        var tags = [] as string[];
        var spacers = [] as string[];
        for (const match of [...rss_feed.dataset.format.matchAll(regex)]) {
            tags.push(match[1]);
            spacers.push(match[2]);
        }
        eel.fetch_rss(rss_feed.dataset.url, tags, parseInt(rss_feed.dataset.length))().then((rss: string[] | object[]) => {
            if (typeof rss[0] != "string") {
                var output_string = "";
                for (const item of rss) {
                    for (var i = 0; i < tags.length; i++) {
                        output_string += `${item[tags[i]]}${spacers[i]}`;
                    }
                }
                rss_feed.innerText = output_string;
                init_marquee(rss_feed.parentElement.parentElement);
            } else {
                console.warn(`RSS feed ${rss_feed.dataset.url} is invalid`);
            }
        });
    }
}

function init_slideshows(): void {
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

function progress_slideshow(slideshow: HTMLElement): void {
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

function init_marquees(): void {
    const marquees = document.querySelectorAll("div[class^='scrolling-']") as NodeListOf<HTMLElement>;
    for (const marquee of marquees) {
        if (!marquee.querySelector(".rss")) {
            init_marquee(marquee);
        }
    }
}

// function init_marquees(): void {
//     const marquees = [["vertical", "Height", "Y"], ["horizontal", "Width", "X"]];
//     for (const type of marquees) {
//         const scrolling = document.getElementsByClassName(`scrolling-${type[0]}`) as HTMLCollectionOf<HTMLElement>;
//         for (const current of scrolling) {
//             if (!current.getElementsByClassName("rss").length) {
//                 const marquee = current.firstElementChild as HTMLElement;
//                 if (current.querySelector("p")[`offset${type[1]}`] > 0) {
//                     //const copies = Math.max(Math.round(2 / (current.querySelector("p")[`offset${type[1]}`] / current[`offset${type[1]}`])), 2);
//                     const copies = Math.max(Math.ceil(current[`offset${type[1]}`] / current.querySelector("p")[`offset${type[1]}`]) + 1, 2);
//                     for (var i = 0; i < copies - 1; i++) {
//                         marquee.appendChild(current.querySelector("p").cloneNode(true));
//                     }
//                     //console.log(parseFloat(current.dataset.time));
//                     marquee.animate([
//                         { transform: `translate${type[2]}(0)` },
//                         { transform: `translate${type[2]}(-${100 / copies}%)` }
//                     ], {
//                         duration: marquee[`offset${type[1]}`] / parseFloat(current.dataset.time),
//                         iterations: Infinity
//                     });
//                 }
//             }
//         }
//     }
// }

function init_marquee(container: HTMLElement): void {
    const type = { "vertical": ["Height", "Y"], "horizontal": ["Width", "X"] }[container.className.substring(10)];
    while (container.querySelectorAll("p").length > 1) {
        container.querySelector("p").remove();
    }
    const marquee = container.firstElementChild as HTMLElement;
    if (marquee.querySelector("p")[`offset${type[0]}`] > 0) {
        const copies = Math.max(Math.ceil(container[`offset${type[0]}`] / container.querySelector("p")[`offset${type[0]}`]) + 1, 2);
        for (var i = 0; i < copies - 1; i++) {
            marquee.appendChild(container.querySelector("p").cloneNode(true));
        }
        marquee.animate([
            { transform: `translate${type[1]}(0)` },
            { transform: `translate${type[1]}(-${100 / copies}%)` }
        ], {
            duration: marquee[`offset${type[0]}`] / parseFloat(container.dataset.time),
            iterations: Infinity
        });
    }
}

function refresh_clocks(): void {
    const time = new Date().toTimeString().substring(0, 8);
    const clocks = document.getElementsByClassName("clock") as HTMLCollectionOf<HTMLElement>;
    for (const clock of clocks) {
        const clock_text = clock.firstElementChild as HTMLElement;
        clock_text.innerText = time;
    }
    setTimeout(refresh_clocks, 1000);
}

function refresh_page(): void {
    location.reload();
}

document.addEventListener('DOMContentLoaded', main);
eel.expose(refresh_page);