const listF = document.querySelector('.list-b');
const listN = document.querySelector('.list-c');

function getBestFictionSeller() {
    var best = new XMLHttpRequest();
    best.open('GET', 'https://api.nytimes.com/svc/books/v3/lists/current/Combined%20Print%20and%20E-Book%20Fiction.json?api-key=CMnfq4pWCyytTakcsWba95xBGJ2khBdk')
    best.onload = function () {
        if (this.status === 200) {
            const response = JSON.parse(this.response);
            const bookList = response.results['books'];
            for (let j = 0; j < bookList.length; j++) {
                const book = bookList[j];
                listF.innerHTML +=
                    `
            <div class="b-book">
                
                <img src="${book.book_image}" alt="BestSeller" width="100" height="150">
                
            </div>
            `
            }
        }
    }
    best.send();
}
function getBestNonFictionSeller() {
    var best = new XMLHttpRequest();
    best.open('GET', 'https://api.nytimes.com/svc/books/v3/lists/current/Combined%20Print%20and%20E-Book%20Nonfiction.json?api-key=CMnfq4pWCyytTakcsWba95xBGJ2khBdk')
    best.onload = function () {
        if (this.status === 200) {
            const response = JSON.parse(this.response);
            const bookList = response.results['books'];
            for (let j = 0; j < bookList.length; j++) {
                const book = bookList[j];
                listN.innerHTML +=
                    `
                <div class="b-book">
                    <img src="${book.book_image}" alt="BestSeller" width="100" height="150">
                </div>
                `
            }
        }
    }
    best.send();
}
getBestFictionSeller();
getBestNonFictionSeller();