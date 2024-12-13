const inputLogin = document.getElementById("inputLogin");
const inputPassword = document.getElementById("inputPassword");
const buttonSubmit = document.getElementById("buttonSubmit");

let login = null;
let password = null;

// Авторизация
buttonSubmit.onclick = function() {
    login = inputLogin.value;
    password = inputPassword.value;

    if (login === "user" & password === "user") {
        localStorage.setItem("user", 1);
    }

    if (login === "admin" & password === "admin") {
        window.open('admin.html');
    }
}
