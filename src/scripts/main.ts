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

function match_template(template: string): { tags: string[]; spacers: string[] } {
    const regex = /\${([^$]+)}([^$]*)/g;
    const tags = [...template.matchAll(regex)].map(match => match[1]);
    const spacers = [...template.matchAll(regex)].map(match => match[2]);
    return { tags, spacers };
}

function init_rss_feeds(): void {
    const rss_feeds = document.getElementsByClassName("rss") as HTMLCollectionOf<HTMLElement>;
    for (const rss_feed of rss_feeds) {
        const matches = match_template(rss_feed.dataset.format);
        console.log("here")
        eel.fetch_rss(rss_feed.dataset.url, matches.tags, parseInt(rss_feed.dataset.length))().then((rss: string[] | object[]) => {
            if (typeof rss[0] != "string") {
                let output_string = "";
                for (const item of rss) {
                    for (let i = 0; i < matches.tags.length; i++) {
                        output_string += `${item[matches.tags[i]]}${matches.spacers[i]}`;
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

function init_marquee(container: HTMLElement): void {
    const type = { "vertical": ["Height", "Y"], "horizontal": ["Width", "X"] }[container.className.substring(10)];
    while (container.querySelectorAll("p").length > 1) {
        container.querySelector("p").remove();
    }
    const marquee = container.firstElementChild as HTMLElement;
    if (marquee.querySelector("p")[`offset${type[0]}`] > 0) {
        const copies = Math.max(Math.ceil(container[`offset${type[0]}`] / container.querySelector("p")[`offset${type[0]}`]) + 1, 2);
        for (let i = 0; i < copies - 1; i++) {
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

interface time {
    h24: string;
    h12: string;
    min: string;
    sec: string;
    date: number;
    month: number;
    year: number;
    per: string;
    wday: string;
    mname: string;
}

function get_time(): time {
    const time = new Date();
    return {
        h24: String(time.getHours()).padStart(2, "0"),
        h12: String(time.getHours() % 12).padStart(2, "0"),
        min: String(time.getMinutes()).padStart(2, "0"),
        sec: String(time.getSeconds()).padStart(2, "0"),
        date: time.getDate(),
        month: time.getMonth(),
        year: time.getFullYear(),
        per: time.getHours() < 12 ? "AM" : "PM",
        wday: time.toLocaleString("default", { weekday: "long" }),
        mname: time.toLocaleString("default", { month: "long" })
    }
}


function refresh_clocks(): void {
    const time = get_time();
    const clocks = document.getElementsByClassName("clock") as HTMLCollectionOf<HTMLElement>;
    for (const clock of clocks) {
        const matches = match_template(clock.dataset.format);
        let output_string = "";
        for (let index = 0; index < matches.tags.length; index++) {
            output_string += `${time[matches.tags[index]]}${matches.spacers[index]}`;
        }
        const clock_text = clock.firstElementChild as HTMLElement;
        clock_text.innerText = output_string;
    }
    setTimeout(refresh_clocks, 1000);
}

function refresh_page(): void {
    location.reload();
}

document.addEventListener('DOMContentLoaded', main);
eel.expose(refresh_page);