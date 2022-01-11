document.querySelector('#upload-video').addEventListener('submit', uploadVideo)
var progressBar = document.querySelector('.progress-bar')
var progress = document.querySelector('.progress')

function uploadVideo(e) {
    e.preventDefault()
    // progress.classList.add('show-item')
    // progressBar.classList.add('show-item')
    var video = document.querySelector('#video').files[0]
    var privacy = document.querySelector('#privacy').value
    var data = new FormData()
    data.append('video-file', video)
    data.append('privacy', privacy)

    var xhr = new XMLHttpRequest()
    xhr.open('POST', '/upload', true)
    xhr.onload = function() {
        if (this.readyState == 4 && this.response == 200) {
            document.querySelector('.upload-message').innerHTML = '<p>'+ this.responseText +'</p>'
            // window.location = ''
        }
    }

    xhr.upload.addEventListener('progress', progressHandler, false)
    xhr.addEventListener('error', errorHandler, false)
    xhr.addEventListener('load', completeHandler, false)


    xhr.send(data)

}

function progressHandler(e) {
    var uploadPercent = (e.loaded / e.total) * 100
    document.querySelector('.progress-bar').style.width = uploadPercent + '%'
    document.querySelector('.upload-message').innerHTML = '<p class="uploading">Uploading .... '+ Math.round(uploadPercent) +'%</p>'
}

function errorHandler(e) {
    document.querySelector('.progress-bar').classList.add('bg-warning')
    document.querySelector('.upload-message').innerHTML = '<p class="upload-error">Something goes wrong! Please try after sometimes</p>'
}
function completeHandler(e) {
    document.querySelector('.progress-bar').classList.add('bg-danger'); 
    document.querySelector('.upload-message').innerHTML = '<p class="upload-success">Video uploaded!</p>'   
    window.location = '/publish'
}