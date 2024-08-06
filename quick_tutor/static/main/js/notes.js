

let btn = document.getElementById('notes-button');
let modal = document.getElementsByClassName('modal')[0];

btn.onclick = function(event) {
    modal.style.display = 'block';
    event.stopPropagation();

let xhr = new XMLHttpRequest();
xhr.open('GET', '/get_notes/', true);
xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        let notes = JSON.parse(xhr.responseText);
        let modalContent = document.querySelector('.modal-content');

        // Очищаем содержимое модального окна перед добавлением новых элементов
        modalContent.innerHTML = '';

        // Создаем элементы для каждой заметки
        notes.forEach(note => {
            // Создаем контейнер для каждой заметки
            let noteContainer = document.createElement('div');
            noteContainer.classList.add('note-container');

            // Добавляем данные заметки в контейнер
            noteContainer.innerHTML = `
                <p>ID: <strong>${note.id}</strong></p>
                <p>Topic: <strong>${note.topic}</strong></p>
                <p>Difficult: <strong>${note.topic__difficult}</strong></p>
                <img src="${note.topic__image}" alt="Note Image">
            `;

            // Добавляем контейнер с заметкой в модальное окно
            modalContent.appendChild(noteContainer);
        });
    }
};
xhr.send();

document.onclick = function(event) {
    if (event.target != modal && event.target != btn) {
        modal.style.display = 'none';
    }
};