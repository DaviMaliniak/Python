const themeBtn = document.getElementById("themeBtn");

if (localStorage.getItem("darkMode") === "1") {
    document.body.classList.add("dark-mode");
}

if (themeBtn) {
    themeBtn.addEventListener("click", async () => {
        const dark = !document.body.classList.contains("dark-mode");
        document.body.classList.toggle("dark-mode", dark);
        localStorage.setItem("darkMode", dark ? "1" : "0");

        await fetch("/tema", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({dark})
        });
    });
}
