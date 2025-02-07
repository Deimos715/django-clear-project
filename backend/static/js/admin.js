//hide filter admin panel
document.addEventListener("DOMContentLoaded", ready);

function ready() {

    let title_filter = document.querySelectorAll('#changelist-filter > h2')[0];
    let filter = document.querySelectorAll('#changelist-filter')[0];
    let toge = JSON.parse(localStorage.getItem('my_admin_filter'))
    if  (toge) {
        filter.classList.toggle('toge');
        filter.style.position = 'absolute'
        filter.style.right = "15px"
        let div = document.querySelectorAll('#changelist-filter details');
        display(div);
        div = document.querySelectorAll('#changelist-filter h3');
        display(div);
        div = document.querySelectorAll('#changelist-filter ul');
        display(div);
    }

    title_filter.onclick = function () {
        filter.classList.toggle('toge');
        let div = document.querySelectorAll('#changelist-filter details');
        display(div);
        div = document.querySelectorAll('#changelist-filter h3');
        display(div);
        div = document.querySelectorAll('#changelist-filter ul');
        display(div);

        div.forEach(el => {
            if (el.style.display == 'none') {
                filter.style.position = 'absolute'
                filter.style.right = "15px"
                localStorage.setItem('my_admin_filter', true);
            } else {
                filter.style.position = 'inherit';
                localStorage.setItem('my_admin_filter', false);
            }
        });
    }

    function display(div) {
        div.forEach(el => {
            if (el.style.display !== 'none') {
                el.style.display = 'none';
            } else {
                el.style.display = 'block';
            }
        });
    }

}