import { toast, checkUuid, buildUrl, getUserUuid } from '/static/common-utils.js';
let identity;


document.addEventListener('DOMContentLoaded', async function () {
    try {
        identity = await getUserUuid();   // get user identity

        // fetch informations
        const active_cape = await fetchUserActiveCapeUuid();
        const capes = await fetchCapesUuids()

        document.getElementById('loading').remove();   // remove loading text

        // display capes
        for (let uuid of capes) {
            const data = await fetchCapeInformations(uuid);
            const preview_url = buildUrl(`${data['preview']}`);
            displayCape(data['uuid'], data['name'], preview_url, data['uuid'] == active_cape);
        }
    } catch (error) {
        toast.error(error.message);
    }
});

async function fetchUserActiveCapeUuid() {
    const url = buildUrl(`/user/${identity}/cape`)

    let response;
    try {response = await fetch(url);} catch (error) {throw new Error("API unavailable (contact support)");}
    
    if (response.status == 404 || response.status == 422) {
        return [];
    } else if (!response.ok) {
        throw new Error(`Failed to fetch data from API (${response.status})`);
    }
    return response.json();
}

async function fetchCapesUuids() {
    const url = buildUrl(`/fetch/capes`)

    let response;
    try {response = await fetch(url);} catch (error) {throw new Error("API unavailable (contact support)");}
    
    if (!response.ok) {
        throw new Error(`Failed to fetch data from API (${response.status})`);
    }
    return response.json();
}

async function fetchCapeInformations(uuid) {
    const url = buildUrl(`/fetch/cape/${uuid}`)

    let response;
    try {response = await fetch(url);} catch (error) {throw new Error("API unavailable (contact support)");}
    
    if (!response.ok) {
        throw new Error(`Failed to fetch data from API (${response.status})`);
    }
    return response.json();
}

function createCapeElement(uuid, name, preview_url, isActive = false) {
    const divElement = document.createElement('div');
    const imgElement = document.createElement('img');
    const buttonElement = document.createElement('button');
    const labelElement = document.createElement('label');

    divElement.classList.add('cape');
    divElement.setAttribute('uuid', uuid);

    imgElement.setAttribute('src', preview_url);
    imgElement.setAttribute('alt', 'cape texture preview');

    buttonElement.textContent = isActive ? 'ACTIVE' : 'SELECT';
    buttonElement.classList.add(isActive ? 'active-select-button' : 'select-button');

    labelElement.textContent = name;

    divElement.appendChild(imgElement);
    divElement.appendChild(labelElement);
    divElement.appendChild(buttonElement);

    return divElement;
}

function displayCape(uuid, name, preview_url, active) {
    const container = document.getElementById('capes-container');
    container.appendChild(createCapeElement(uuid, name, preview_url, active));
}


// buttons click event handler
document.addEventListener('click', (event) => {
    if (event.target.classList.contains('select-button')) {
        const uuid = event.target.parentElement.getAttribute('uuid');   // get cape uuid
        
        // check if uuid is valid
        if (!checkUuid(uuid)) {
            toast.error("Invalid data provided");
            toast.info("Refresh the page and try again");
            return;
        }

        // redirect for update
        const queryString = "?cape_uuid=" + uuid   // create query string
        window.location.href += "/update" + queryString;
    }
});