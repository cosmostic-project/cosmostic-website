import { toast, checkUuid, buildUrl, getUserUuid } from '/static/common-utils.js';
let identity;


document.addEventListener('DOMContentLoaded', async function () {
    try {
        identity = await getUserUuid();   // get user identity

        // fetch informations
        const active_accessories = await fetchUserActiveAccessoriesUuids();
        const accessories = await fetchAccessoriesUuids()
        
        document.getElementById('loading').remove();   // remove loading text

        // display accessories
        for (let uuid of accessories) {
            const data = await fetchAccessoryInformations(uuid);
            const preview_url = buildUrl(`${data['preview']}`);

            if (active_accessories.includes(data['uuid'])) {   // if accessory is selected
                displaySelectedAccessory(data['uuid'], data['name'], preview_url);
            } else {
                displayAccessory(data['uuid'], data['name'], preview_url);
            }
        }
    } catch (error) {
        toast.error(error.message);
    }
});

async function fetchUserActiveAccessoriesUuids() {
    const url = buildUrl(`/user/${identity}/accessories`);

    let response;
    try {response = await fetch(url);} catch (error) {throw new Error("API unavailable (contact support)");}

    if (response.status == 404 || response.status == 422) {
        return [];
    } else if (!response.ok) {
        throw new Error(`Failed to fetch data from API (${response.status})`);
    }
    return response.json();
}

async function fetchAccessoriesUuids() {
    const url = buildUrl(`/fetch/accessories`)

    let response;
    try {response = await fetch(url);} catch (error) {throw new Error("API unavailable (contact support)");}
    
    if (!response.ok) {
        throw new Error(`Failed to fetch data from API (${response.status})`);
    }
    return response.json();
}

async function fetchAccessoryInformations(uuid) {
    const url = buildUrl(`/fetch/accessory/${uuid}`)

    let response;
    try {response = await fetch(url);} catch (error) {throw new Error("API unavailable (contact support)");}

    if (!response.ok) {
        throw new Error(`Failed to fetch data from API (${response.status})`);
    }
    return response.json();
}

function createAccessoryElement(uuid, name, preview_url, isSelected = false) {
    const divElement = document.createElement('div');
    const imgElement = document.createElement('img');
    const buttonElement = document.createElement('button');
    const labelElement = document.createElement('label');

    divElement.classList.add(isSelected ? 'selected-accessory' : 'accessory');
    divElement.setAttribute('uuid', uuid);

    imgElement.setAttribute('src', preview_url);
    imgElement.setAttribute('alt', 'accessory preview');

    buttonElement.textContent = isSelected ? 'X' : 'ADD';
    buttonElement.classList.add(isSelected ? 'remove-button' : 'add-button');

    labelElement.textContent = name;

    divElement.appendChild(imgElement);
    divElement.appendChild(labelElement);
    divElement.appendChild(buttonElement);

    return divElement;
}

function displayAccessory(uuid, name, preview_url) {
    const container = document.getElementById('accessories-container');
    container.appendChild(createAccessoryElement(uuid, name, preview_url));
}

function displaySelectedAccessory(uuid, name, preview_url) {
    const container = document.getElementById('selected-accessories');
    container.prepend(createAccessoryElement(uuid, name, preview_url, true));
}


// buttons click event handler
document.addEventListener('click', (event) => {
    if (event.target.classList.contains('add-button')) {
        // check if user has already selected 5 or more accessories
        const selectedAccessoriesLength = document.getElementById('selected-accessories').childElementCount - 1;   // -1 for the save button
        if (selectedAccessoriesLength >= 5) {
            toast.info("You can only select up to 5 accessories");
            return;
        }

        // move from accessories to selected accessories
        const accessoryElement = event.target.parentElement;
        const uuid = accessoryElement.getAttribute('uuid');
        const name = accessoryElement.querySelector('label').textContent;
        const preview_src = accessoryElement.querySelector('img').getAttribute('src');

        displaySelectedAccessory(uuid, name, preview_src);
        accessoryElement.remove();
    } else if (event.target.classList.contains('remove-button')) {
        // move from selected accessories to accessories
        const accessoryElement = event.target.parentElement;
        const uuid = accessoryElement.getAttribute('uuid');
        const name = accessoryElement.querySelector('label').textContent;
        const preview_src = accessoryElement.querySelector('img').getAttribute('src');

        displayAccessory(uuid, name, preview_src);
        accessoryElement.remove();
    } else if (event.target.id == 'save-button') {
        const selectedAccessories = Array.from(event.target.parentElement.querySelectorAll('.selected-accessory')).map(accessory => accessory.getAttribute('uuid'));   // get all selected accessories uuids
        
        // check if not more than 5 accessories are selected
        if (selectedAccessories.length > 5) {
            toast.info("You can only select up to 5 accessories");
            return;
        }

        // check if uuids are valid
        for (let uuid of selectedAccessories) {
            if (!checkUuid(uuid)) {
                toast.error("Invalid data provided");
                toast.info("Refresh the page and try again");
                return;
            }
        }

        // redirect for update
        const queryString = "?accessories_uuids=" + selectedAccessories.map(uuid => `${uuid}`).join(',');   // convert array to query string
        window.location.href += "/update" + queryString;
    }
});