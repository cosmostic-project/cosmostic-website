document.addEventListener("DOMContentLoaded", function () {
    // retrieve theme from local storage
    let darkMode = localStorage.getItem("darkMode");
    darkMode = darkMode === 'true';

    // update icon
    toggleIcons(darkMode);
});

document.addEventListener('click', (event) => {
    if (event.target.classList.contains('toggle-theme-button')) {
        // toggle dark mode value
        let darkMode = localStorage.getItem("darkMode");
        darkMode = darkMode === 'true';
        darkMode = !darkMode;
        localStorage.setItem("darkMode", darkMode);
        
        // toggle theme
        document.body.classList.toggle("dark-mode");
        toggleIcons(darkMode);
    }
});


function toggleIcons(darkMode) {
    const lightIcon = document.getElementById("light-icon");
    const darkIcon = document.getElementById("dark-icon");
    if (darkMode) {
        lightIcon.style.display = "block";
        darkIcon.style.display = "none";
    } else {
        lightIcon.style.display = "none";
        darkIcon.style.display = "block";
    }
}