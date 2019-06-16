const sections = document.querySelectorAll('main section');
const footerNavs = document.querySelectorAll('footer div');

for (let i = 0; i < sections.length; i++) {
    footerNavs[i].addEventListener('click',showSection);


    function showSection(){
        setTimeout(timed,1000);
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