import { toast, buildUrl, getUserUuid } from '/static/common-utils.js';
let identity;


document.addEventListener('DOMContentLoaded', async function () {
    try {
        identity = await getUserUuid();   // get user identity

        // display active cape preview
        const active_cape = await fetchActiveCapeUuid();
        if (active_cape == null) {
            document.getElementById('active-cape-preview').innerHTML = '<i>no active cape</i>';
        } else {
            document.querySelector('#active-cape-preview .loading').remove();   // remove loading text

            const preview_url = buildUrl(`/fetch/cape/${active_cape}/preview`);
            displayCape(preview_url);
        }

        // display active accessories
        let active_accessories = await fetchActiveAccessoriesUuids();
        active_accessories = active_accessories.slice(0, 4);   // maximum 4 accessories
        if (active_accessories.length == 0) {
            document.getElementById('active-accessories-preview').innerHTML = '<i>no active accessories</i>';
        } else {
            document.querySelector('#active-accessories-preview .loading').remove();   // remove loading text
        }

        for (let uuid of active_accessories) {
            const preview_url = buildUrl(`/fetch/accessory/${uuid}/preview`);
            displayAccessory(preview_url);
        }
    } catch (error) {
        toast.error(error.message);
    }
});

async function fetchActiveCapeUuid() {
    const url = buildUrl(`/user/${identity}/cape`);

    let response;
    try {response = await fetch(url);} catch (error) {throw new Error("API unavailable (contact support)");}

    if (response.status == 404 || response.status == 422) {
        return null;
    } else if (!response.ok) {
        throw new Error(`Failed to fetch data from API (${response.status})`);
    }
    return response.json();
}

async function fetchActiveAccessoriesUuids() {
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

function createImage(preview_url) {
    const imgElement = document.createElement('img');

    imgElement.setAttribute('src', preview_url);
    imgElement.setAttribute('alt', 'item preview');

    return imgElement;
}

function displayAccessory(preview_url) {
    const container = document.getElementById('active-accessories-preview');
    container.appendChild(createImage(preview_url));
}

function displayCape(preview_url) {
    const container = document.getElementById('active-cape-preview');
    container.appendChild(createImage(preview_url));
}