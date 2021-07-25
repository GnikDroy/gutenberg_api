document.addEventListener("DOMContentLoaded", function() {

    const tables = document.querySelectorAll(".markdown-container table");
    for (let i = 0; i < tables.length; i++) {
        tables[i].classList.add("table", "table-dark", "table-striped", "table-bordered");
    };

    const theads = document.querySelectorAll(".markdown-container th");
    for (let i = 0; i < theads.length; i++) {
        theads[i].classList.add("thead-light");
    };

    const toctitles = document.querySelectorAll(".markdown-container .toctitle");
    for (let i = 0; i < toctitles.length; i++) {
        toctitles[i].classList.add("h1");
    };

    const tocs = document.querySelectorAll(".markdown-container .toc");
    for (let i = 0; i < tocs.length; i++) {
        tocs[i].classList.add("my-5", "fs-5");
    };

    const ul = document.querySelectorAll(".markdown-container .toc>ul");
    for (let i = 0; i < ul.length; i++) {
        ul[i].classList.add("pt-5");
    };

});