const API_URL = `https://api.${window.location.host}`;


document.addEventListener("DOMContentLoaded", function () {
    // retrieve theme from local storage
    let darkMode = localStorage.getItem("darkMode");
    darkMode = darkMode === 'true';

    document.body.classList.toggle("dark-mode", darkMode);   // apply theme
});

document.addEventListener('click', (event) => {
    if (event.target.classList.contains('menu-button')) {   // expand menu (mobile devices only)
        const menuButton = event.target;
        const menu = document.querySelector('.menu');
        
        // open menu
        menuButton.innerHTML = menuButton.innerHTML == 'menu' ? 'close' : 'menu';
        menu.classList.toggle('open');   // toggle icon
    }
});


class Toast {
    constructor() {
        this.notyf = new Notyf({
            duration: 3000,
            ripple: true,
            position: {
                x: 'right',
                y: 'bottom'
            },
            dismissible: false,
            types: [
                {
                    type: 'success',
                    background: '#3dc763',
                    icon: {
                        className: 'material-symbols-outlined',
                        text: 'check_circle',
                        color: 'white'
                    }
                },
                {
                    type: 'error',
                    background: '#ed3d3d',
                    icon: {
                        className: 'material-symbols-outlined',
                        text: 'cancel',
                        color: 'white'
                    }
                },
                {
                    type: 'warning',
                    background: '#E38D26',
                    icon: {
                        className: 'material-symbols-outlined',
                        text: 'warning',
                        color: 'white'
                    }
                },
                {
                    type: 'info',
                    background: '#2662E3',
                    icon: {
                        className: 'material-symbols-outlined',
                        text: 'info',
                        color: 'white'
                    }
                }
            ]
        });
    }

    show(type, message) {
        this.notyf.open({
            type: type,
            message: message
        })
    }

    success(message) {
        this.show('success', message);
    }

    error(message) {
        this.show('error', message);
    }

    warning(message) {
        this.show('warning', message);
    }

    info(message) {
        this.show('info', message);
    }
}


function checkUuid(uuid) {
    const regex = /^[0-9A-F]{8}-[0-9A-F]{4}-[4][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$/i;
    return regex.test(uuid);
}

function buildUrl(endpoint) {
    return new URL(`${API_URL}${endpoint}`);
}

async function getUserUuid() {
    const url = window.origin+'/identity';

    let response;
    try {response = await fetch(url);} catch (error) {throw new Error("Unable to get identity (contact support)");}
    
    if (response.status == 401) {
        return false;
    } else if (!response.ok) {
        throw new Error(`Failed to fetch identity (${response.status})`);
    }
    return response.json();
}


// export functions
export const toast = new Toast();
export { checkUuid, buildUrl, getUserUuid }