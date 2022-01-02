/**
 * Validate the form.
 * @param form {HTMLFormElement} The form element containing the form to validate.
 */
function validateForm(form) {
    /**
     * @type {HTMLTextAreaElement}
     */
    const textAreaElement = form.querySelector('textarea#form-body');
    if (textAreaElement.value.length < 15) {
        return alert("Body is <15, please add more text.");
    }
    return form.reportValidity();
}

/**
 * Submit the form.
 * @param form {HTMLFormElement} The form element containing the form to validate.
 */
function submitForm(form) {
    if (!validateForm(form)) {
        return;
    }
    const title = form.querySelector("input#form-title").value
    const isPart = form.querySelector("input#form-is-part").checked
    const boardId = form.querySelector("input#form-board-id").value
    const boardType = Array.from(form.querySelectorAll('input[name="board-type"]')).filter((item) => item.checked)[0].value
    const body = form.querySelector("textarea#form-body").value
    const data = new URLSearchParams();
    data.append("title", title);
    data.append("is_part", isPart);
    data.append("board_id", boardId);
    data.append("board_type", boardType);
    data.append("body", body);
    fetch("/api/queue", {
        method: "POST",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: data.toString()
    }).then((response) => {
        if (response.ok) {
            return response.json()
        } else {
            return alert("Failed to add to queue!");
        }
    }).then(/** @type {{id: number, html: string} | Response} */(data) => {
        if (data.id) {
            let div = document.createElement("div")
            div.id = "post-" + data.id
            div.innerHTML = data.html
            document.querySelector("#submitted-posts").prepend(div)
        }
    });
}

/**
 * Change the title type depending on whether isPart is checked.
 * @param isPart {HTMLInputElement}
 */
function changeTitleType(isPart) {
    /**
     * @type {HTMLInputElement}
     */
    const title = document.querySelector("input#form-title")
    if (isPart.checked) {
        title.type = "number";
    } else {
        title.type = "text";
    }
}
