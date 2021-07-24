function change_theme(theme_type) {
    this.localStorage.setItem("theme", theme_type);
    if (theme_type == "dark") {
        document.body.classList.remove("text-dark");
        document.body.classList.remove("bg-light");
        document.body.classList.add("text-light");
        document.body.classList.add("bg-dark");
    } else {
        document.body.classList.remove("text-light");
        document.body.classList.remove("bg-dark");
        document.body.classList.add("text-dark");
        document.body.classList.add("bg-light");
    }
}

window.addEventListener("load", function() {
    // Get current/default theme.
    change_theme(this.localStorage.getItem("theme") || "dark");

    // Change state of button to reflect theme state.
    // This is checked if dark theme is used.
    const light_dark_checkbox = document.getElementById('light_dark_checkbox');
    light_dark_checkbox.checked = this.localStorage.getItem('theme') == "dark";


    // Add event listener to change theme on checkbox toggle
    light_dark_checkbox.addEventListener('change', (event) => {
        const theme = event.currentTarget.checked ? "dark" : "light";
        change_theme(theme);
    });
});