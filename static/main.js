const sections = document.querySelectorAll('main section');
const footerNavs = document.querySelectorAll('footer div');
const input = document.querySelector('.search input');
const searchButton = document.querySelector('.search a');
const books = document.querySelector('.books');


searchButton.addEventListener('click', getbook);
input.addEventListener('keydown', (event) => {
    if (event.which === 13) {
        getbook();
    }
});


for (let i = 0; i < sections.length; i++) {
    footerNavs[i].addEventListener('click', showSection);


    function showSection() {
        setTimeout(timed, 0);
        function timed() {
            footerNavs[i].classList.add("active-button");
            sections[i].classList.add("active");
            for (let j = 0; j < sections.length; j++) {
                if (j !== i) {
                    footerNavs[j].classList.remove("active-button");
                    sections[j].classList.remove("active");
                }
            }
        }
    }
}
function getbook() {
    let a = input.value;
    books.innerHTML = " ";
    if (a != "") {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', "https://www.googleapis.com/books/v1/volumes?q=" + a);
        xhr.onload = function () {
            if (this.status == 200) {
                var answer = JSON.parse(this.response);
                var group = []
                for (let i = 0; i < answer.items.length; i++) {
                    x = answer.items[i].volumeInfo;
                    if (!x.ratingsCount) {
                        x.averageRating = "0";
                        x.ratingsCount = "0";
                    }
                    let cover;
                    cover = !x.imageLinks ? "" : x.imageLinks.smallThumbnail;
                    let author;
                    author = !x.authors ? "Not Available" : x.authors[0];

                    books.innerHTML +=
                        `<div class="book">
                    <div class="cover">
                        <img src="${cover}" alt="Cover" width="80" height="100">
                    </div>
                    <div class="details">
                        <a href="#" class="title">${x.title}</a>
                        <p class="author">By ${author}</p>
                        <p class="rating">Rating : ${x.averageRating} out of (${x.ratingsCount}) rating(s)</p>
                        <p class="pages">${x.pageCount} Pages</p>
                    </div>
                 </div>`;
                }
            }
        }
        xhr.send();
    }
}

const quoteDisplay = document.querySelector('.quote');
const quoteBox = document.querySelector('.quote-box');
const quoteChanger = document.querySelector('.quote-changer');

quoteChanger.addEventListener('click', getQuote);
function getQuote() {
    const quotes = ["There is some good in this world, and it’s worth fighting for.", "Twenty years from now you will be more disappointed by the things that you didn’t do than by the ones you did do.",
        "Well-behaved women seldom make history.", "It is better to be hated for what you are than to be loved for what you are not.", "Who, being loved, is poor?",
        "Every human life is worth the same, and worth saving.", "Get Busy Living or Get Busy Dying", "The goal isn’t to live forever, the goal is to create something that will.",
        "Travel far enough, you meet yourself.", "None of us really changes over time. We only become more fully what we are.", "Most people are nice when you finally see them.",
        "Don't Panic"];

    const authors = ["J.R.R. Tolkien", "H.Jackson Brown", " Laurel Thatcher Ulrich", "André Gide", "Oscar Wilde", "J.K. Rowling", "Stephen King", "Chuck Palahniuk", "David Mitchell", "Anne Rice", "Harper Lee", "Douglas Adams"];
    const books = ["The Two Towers", "P.S. I Love You", "Well-Behaved Women Seldom Make History", "Autumn Leaves", "A Woman of No Importance", "Harry Potter and Deathly Hallows",
        "Different Seasons", "Diary", "Cloud Atlas", "The Vampire Lestat", "To Kill a Mockingbird", "The Hitchhiker’s Guide to the Galaxy"];

    console.log(quotes.length, authors.length, books.length)

    quoteBox.style.background = `rgb(${Math.floor(Math.random() * (255 - 120) + 120)},${Math.floor(Math.random() * (255 - 120) + 120)},${Math.floor(Math.random() * (255 - 120) + 120)})`;
    let quoteNumber = Math.floor(Math.random()*12);
    quoteDisplay.innerHTML = `
            <p>"${quotes[quoteNumber]}"</p>
            <p class="a-b"> By ${authors[quoteNumber]} from ${books[quoteNumber]}</p>
            `;
}

