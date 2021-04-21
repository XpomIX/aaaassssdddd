var data;
var addingName;
var addingDescription;
var adminMode = true;

function html(element, pos, html) { document.getElementById(element).insertAdjacentHTML(pos, html) }
function clearContent() { document.getElementById("content").innerHTML = ""; }

function deleteUser(id) {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/del', true)
    xhr.send(JSON.stringify(id))
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return;
        if (xhr.status != 200) {
            console.dir('fff')
        } else {
            loadSlangs()
        }
    }
}

function renderSlangList() {
    clearContent()
    html("content", "beforeend", `
        <div class="search-container">
            <div class="input-group mb-3">
              <div class="input-group-prepend">
                <span class="input-group-text" id="basic-addon1">🔎</span>
              </div>
              <input type="text" class="form-control" placeholder="Что хотите найти?" aria-describedby="basic-addon1">
            </div>
        </div>
    `);
    data.map((item) => html("content", "beforeend", `
        <div class="col-xl-3 col-lg-4 col-md-6 col-12" style="padding: 5px">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">${item['name']} ${
                        adminMode ? 
                                `<div style="float: right;width: 20px;cursor: pointer;" onClick="deleteUser('${item['id']}')">
                                    <img class="crest" style="position: relative; width: 100%;"
                                    src="/static/cross.svg"/>
                                </div>`
                            : ''
                        }</h5>
                    <p class="card-text">${item['description']}</p>
                    <a href="#" class="card-link">Читать больше...</a>
                </div>
            </div>
        </div>
    `));
}

function resetError(str) { document.getElementById(str).innerHTML = '' }
function renderAdder() {
    html('left-bar', 'afterbegin', `
        <div style="padding: 10px" class="myCard">
            <div class="card" style="padding: 10px">
                <h4 style="text-decoration: underline;text-decoration-style: dashed;text-decoration-color: #329C9C;">${adminMode ? 'Добавить' : 'Предложить'} сленг</h4>
                <div class="form-group">
                    <label for="name">Сленг<span style="color: red">*</span></label>
                    <input type="text" class="form-control" id="name" onInput="resetError('nameError')" placeholder="Введите сленг">
                    <small id="nameError" style="color: red"></small>
                </div>
                <div class="form-group">
                    <label for="description">Описание<span style="color: red">*</span></label>
                    <textarea type="textarea" class="form-control" id="description" onInput="resetError('descriptionError')" placeholder="Введите описание"></textarea>
                    <small id="descriptionError" style="color: red"></small>
                </div>
                <small style="text-align: end;"><span style="color: red">*</span> - обязательные поля</small>
                <button onClick="sendSlang()" class="btn btn-primary" style="float: right" id="formSubmitButton">${adminMode ? 'Добавить' : 'Отправить'}</button>
            </div>
        </div>
    `)
}


function renderLoading() {
    clearContent()
    html("content", "beforeend", `
        <div>
            <img 
                style="position: relative; width: 100%;" 
                src="/static/loading.gif"
            />
        </div>
    `);
}

function sendValidation(name, desc) {
    let error = {};
    // NAME
    if (name == '') { // lenght < 2 : ERROR
        error.name = 'Обязательное поле.'
    }

    // DESCRIPTION
    if (desc == '') {
        error.description = 'Обязательное поле.'
    }

    // RESULT
    if ((error.name === undefined) && (error.description === undefined)) {
        error = true;
    }
    return error
}
function renderValidationErrors(errors) {
    document.getElementById('nameError').innerHTML = errors.name !== undefined ? errors.name : '';
    document.getElementById('descriptionError').innerHTML = errors.description !== undefined ? errors.description : '';
}
function sendSlang() {
    let name = document.getElementById('name').value;
    let description = document.getElementById('description').value;
    let validation = sendValidation(name, description);
    console.dir(validation);
    if (validation === true) {
        let button = document.getElementById('formSubmitButton');
        button.setAttribute('disabled', true);
        button.innerHTML = 'Отправка...';
        let toSend = {
            name,
            description
        }
        let xhr = new XMLHttpRequest()
        xhr.open('POST', adminMode ? '/api/adminAdd' : '/api/userAdd', true)
        xhr.send(JSON.stringify(toSend))
        
        xhr.onreadystatechange = function() {
            if (xhr.readyState != 4) return;
            if (xhr.status != 200) {
                console.dir('fff')
            } else {
                loadSlangs()
            }

            button.setAttribute('disabled', false);
            button.innerHTML = adminMode ? 'Добавить' : 'Отправить';
        }
    } else {
        renderValidationErrors(validation)
    }
}

async function loadSlangs() {
    let response = await fetch('/api/get');
    renderLoading()
    if (response.ok) {
        let json = await response.json();
        data = json.data;
        renderSlangList();
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

html("root", "afterbegin", `
    <div class="row">
        <div class="col-3" id="header-left-bar"></div>
        <div class="col-6 row" id="header-content"></div>
        <div class="col-3" id="header-right-bar"></div>
    </div>
    <div class="row">
        <div class="col-xl-3 col-12" id="left-bar" style="margin-bottom: 15px;"></div>
        <div class="col-xl-6 col-12">
            <div class="row myCard" style="padding-right: 5px;padding-left: 5px;" id="content">
            </div>
        </div>
        <div class="col-xl-3 col-12" id="right-bar"></div>
    </div>
`);

renderAdder();
loadSlangs();