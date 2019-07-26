
// declaring variables
const footerIcons = document.querySelectorAll("footer a");
for (let i = 0; i < footerIcons.length; i++) {
    footerIcons[i].addEventListener("click", () => {
        console.log(i)
        for (let j = 0; j < footerIcons.length; j++) {
            if (j != i) {
                console.log(" ")
            }
        }
    })
}

var input = document.querySelector('.search input');
var books = document.querySelector('.books');

// asking for books from google's book's api using xmlhttprequest

// taking care of quotes on the quotes tab

function getQuote() {
    const quotes = ["There is some good in this world, and it’s worth fighting for.", "Twenty years from now you will be more disappointed by the things that you didn’t do than by the ones you did do.",
        "Well-behaved women seldom make history.", "It is better to be hated for what you are than to be loved for what you are not.", "Who, being loved, is poor?",
        "Every human life is worth the same, and worth saving.", "Get Busy Living or Get Busy Dying", "The goal isn’t to live forever, the goal is to create something that will.",
        "Travel far enough, you meet yourself.", "None of us really changes over time. We only become more fully what we are.", "Most people are nice when you finally see them.",
        "Don't Panic"];

    quoteBox.style.background = `rgb(${Math.floor(Math.random() * (255 - 120) + 120)},${Math.floor(Math.random() * (255 - 120) + 120)},${Math.floor(Math.random() * (255 - 120) + 120)})`;
    let quoteNumber = Math.floor(Math.random() * 12);
    quoteDisplay.innerHTML = `
            <p>"${quotes[quoteNumber]}"</p>
            `;
}

