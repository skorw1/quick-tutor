function addNoteToTopic(pk) {
    fetch(`/add_note/${pk}/`, { // Используем шаблонную строку для формирования URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to add note to topic');
        }
        window.location.reload();
    })
    .catch(error => {
        console.error('Error adding note to topic:', error);
    });
}

function deleteNoteFromTopic(pk) {
    fetch(`/delete_note/${pk}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to delete note from topic');
        }
        window.location.reload(); // Обновляем страницу после удаления заметки
    })
    .catch(error => {
        console.error('Error deleting note from topic:', error);
    });
}

function getCookie(name) {
    const cookieString = document.cookie;
    const csrfTokenIndex = cookieString.indexOf(name + '=');
    if (csrfTokenIndex === -1) {
        return null;
    }
    let csrfToken = cookieString.substring(csrfTokenIndex + name.length + 1);
    return csrfToken;
}