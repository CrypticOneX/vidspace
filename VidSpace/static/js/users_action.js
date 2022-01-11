var subscribeMe = document.querySelector('#subscribe-me').addEventListener('submit', subscribe)
var subscribeValue = document.querySelector('#subscribe').value

// like button
var likeVideo = document.querySelector('#like-video').addEventListener('submit', like)
var likeValue = document.querySelector('#like').value

// dislike button
var dislikeVideo = document.querySelector('#dislike-video').addEventListener('submit', dislike)
var dislikeValue = document.querySelector('#dislike').value

// playlists
var addPlaylist = document.querySelector('#add-playlist').addEventListener('submit', createPlaylist)
var pname = document.querySelector('#pname')
var privacy = document.querySelector('#make-private')

function subscribe(e) {
    e.preventDefault()
    var data = new FormData()
    data.append('subscribe', subscribeValue)
    var xhr = new XMLHttpRequest()
    xhr.open('POST', '/subscribe', true)
    xhr.onload = function() {
        if (this.status == 200) {
            var resData = JSON.parse(this.responseText)
            if (resData.status == 1) {
                document.querySelector('#subscribe').classList.remove('subscribe-btn')
                document.querySelector('#subscribe').classList.add('subscribed-btn-disabled')
                document.querySelector('#subscribe').innerHTML = `Subscribed  <strong>${resData.subscriber}</strong>`
            }

            if (resData.status == 0) {
                document.querySelector('#subscribe').classList.remove('subscribed-btn-disabled')
                document.querySelector('#subscribe').classList.add('subscribe-btn')
                document.querySelector('#subscribe').innerHTML = `Subscribe <strong>${resData.subscriber}</strong>`
            }
        }
    }
    xhr.send(data)
}

function like(e) {
    e.preventDefault()
    var data = new FormData()
    data.append('video_id', likeValue)
    var xhr = new XMLHttpRequest()
    xhr.open('POST', '/like', true)
    xhr.onload = function() {
        if (this.status == 200) {
            var resData = JSON.parse(this.responseText)
            if (resData.status == 1) {
                document.querySelector('#like').classList.add('vtn-btn-done')
                document.querySelector('#like').innerHTML = `<i class="fas fa-thumbs-up"></i> ${resData.likes}`
                document.querySelector('#dislike').classList.remove('vtn-btn-done')
                document.querySelector('#dislike').innerHTML = `<i class="fas fa-thumbs-down"></i> ${resData.dislikes}`
            } 

            if (resData.status == 0) {
                document.querySelector('#like').classList.remove('vtn-btn-done')
                document.querySelector('#like').innerHTML = `<i class="fas fa-thumbs-up"></i> ${resData.likes}`
                document.querySelector('#dislike').classList.remove('vtn-btn-done')
                document.querySelector('#dislike').innerHTML = `<i class="fas fa-thumbs-down"></i> ${resData.dislikes}`
            }
        }
    }
    xhr.send(data)
}

function dislike(e) {
    e.preventDefault()
    var data = new FormData()
    data.append('video_id', dislikeValue)
    var xhr = new XMLHttpRequest()
    xhr.open('POST', '/dislike', true)
    xhr.onload = function() {
        if (this.status == 200) {
            var resData = JSON.parse(this.responseText)
            if (resData.status == 1) {
                document.querySelector('#dislike').classList.add('vtn-btn-done')
                document.querySelector('#dislike').innerHTML = `<i class="fas fa-thumbs-down"></i> ${resData.dislikes}`
                document.querySelector('#like').classList.remove('vtn-btn-done')
                document.querySelector('#like').innerHTML = `<i class="fas fa-thumbs-up"></i> ${resData.likes}`
            } 

            if (resData.status == 0) {
                document.querySelector('#dislike').classList.remove('vtn-btn-done')
                document.querySelector('#dislike').innerHTML = `<i class="fas fa-thumbs-down"></i> ${resData.dislikes}`
                document.querySelector('#like').classList.remove('vtn-btn-done')
                document.querySelector('#like').innerHTML = `<i class="fas fa-thumbs-up"></i> ${resData.likes}`
            }
        }
    }
    xhr.send(data)
}

function createPlaylist(e) {
    e.preventDefault()
    
    var data = new FormData()
    data.append('pname', pname.value)
    data.append('privacy', privacy.value)

    var xhr = new XMLHttpRequest()
    xhr.open('POST', '/playlist/create-playlist', true)
    xhr.onload = function() {
        if (this.status == 200) {
            console.log("Worked")
        }
    }
    xhr.send(data)
}