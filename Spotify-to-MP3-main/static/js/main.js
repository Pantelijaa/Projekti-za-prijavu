downloadBtn = document.querySelectorAll('.download-btn');
downloadBtn.forEach(btn => {
    btn.addEventListener('focus', (e) => {
        e.target.classList.add('download-btn-modifier');
        setTimeout(() => {
            e.target.classList.remove('download-btn-modifier');
        }, 1000)
    })
})

profile = document.querySelector('#profile');
dropMenu = document.querySelector('#drop-menu');
arrow = document.querySelector('#dropdown .material-symbols-outlined');
profile.addEventListener('click', () => {
    if (arrow.innerText === 'arrow_drop_down'){
        dropMenu.classList.add('disp-block');
        profile.style.backgroundColor = 'var(--drop-down-color)';
        arrow.innerText = 'arrow_drop_up';
    } else {
        dropMenu.classList.remove('disp-block');
        profile.style.backgroundColor = 'black';
        arrow.innerText = 'arrow_drop_down';
    }
})

playlistMenuActivator = document.querySelector('#drop-side');
playlistMenu = document.querySelector('#side-menu');
playlistMenuActivator.addEventListener('mouseover', () => {
    playlistMenu.classList.add('disp-block')
})
playlistMenuActivator.addEventListener('mouseout', () => {
    playlistMenu.classList.remove('disp-block')
})

$(function() {
    $('a#logout-btn').on('click', e => {
        e.preventDefault()
        $.getJSON('/force_logout',
            function(data) {
                location.reload()
            });
            return false;
    });
});
