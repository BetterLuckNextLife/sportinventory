const inputItem = document.getElementById("inputItem");
const inputCount = document.getElementById("inputCount");
const selectState = document.getElementById("selectState");
const buttonSubmit = document.getElementById("buttonSubmit");

let item = null;
let count = null;
let state = null;

// Проверка авторизации


// Подтверждение добавления предмета
buttonSubmit.onclick = function() {
    item = inputItem.value;
    count = inputCount.value;
    state = selectState.value;

    console.log(`${item}, ${count}, ${state}`);
}

// Отправка данных в базу
