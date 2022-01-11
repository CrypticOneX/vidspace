var u = document.URL
var u_data = u.split('=')
var video_id = u_data[1]
var url = `/comment/${this.video_id}`

var xhr = new XMLHttpRequest()
xhr.open('GET', url, true)
xhr.onload = function() {
    if (this.status == 200) {
        var data = JSON.parse(this.responseText)
        var data2 = data.comments
        console.log(data.comments)
        for (var i = 0; i < data2.length; i++) {
            document.querySelector('#comment-list').innerHTML += `
                <div class="single-video-info-content box mb-3">
                    <h6 class="main-title">${data2[i].first_name}</h6>
                    <p>${data2[i].comment}</p>
                    <p><small>${data2[i].date}</small></p>
                </div>            
            `
            console.log(data2[i].comment)
        }
      
    }
}

xhr.send()
