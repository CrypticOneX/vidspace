document.querySelector('.hmenu-action').addEventListener('click', openMenu)
// var deleteBtn = document.querySelectorAll('.delete-btn')
// var deleteModal = document.querySelector('.delete-modal')
// var editModal = document.querySelector('.edit-modal')
// var editBtn = document.querySelectorAll('.edit-btn')
// var backdrop = document.querySelector('.backdrop');
// var btnCancel = document.querySelector('.btn-cancel').addEventListener('click', cancelModal)
// var btnCancelEdit = document.querySelectorAll('.btn-cancel-edit')
sidemenu = document.querySelector('#side-nav')

// for (var i = 0; i < deleteBtn.length; i++) {
//     deleteBtn[i].addEventListener('click', function(e) {
//         deleteModal.classList.add('show-item')
//         backdrop.classList.add('show-item')
//     })
// }

// for (var i = 0; i < btnCancel.length; i++) {
//     btnCancel[i].addEventListener('click', function() {
//         if (backdrop.classList.contains('show-item') && deleteModal.classList.contains('show-item')) {
//             deleteModal.classList.remove('show-item')
//             backdrop.classList.remove('show-item')
//         }
//     })
// }

// for (var i = 0; i < editBtn.length; i++) {
//     editBtn[i].addEventListener('click', function(e) {
//         editModal.classList.add('show-item')
//         backdrop.classList.add('show-item')
//     })
// }

// for (var i = 0; i < btnCancelEdit.length; i++) {
//     btnCancelEdit[i].addEventListener('click', function() {
//         if (backdrop.classList.contains('show-item') && editModal.classList.contains('show-item')) {
//             editModal.classList.remove('show-item')
//             backdrop.classList.remove('show-item')
//         }
//     })
// }

function openMenu(e) {
    if (sidemenu.classList.contains('show-item')) {
        hideMenu()
    } else {
        showMenu()
    }
}

function showMenu() {
    sidemenu.classList.add('show-item')
}

function hideMenu() {
    sidemenu.classList.remove('show-item')
}

