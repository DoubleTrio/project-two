document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    

    // socket.on('connect', () => {
    //     console.log("Hello")
    // });
//     console.log(document.querySelector('#channelForm'))
//     document.querySelector('#channelForm').onsubmit = () => {
//         console.log("Good, it works")

// }
});

    //     const request = new XMLHttpRequest();
    //     request.open('POST', '/createChannel');

    //     request.onload = () => {
    //         const data = JSON.parse(request.responseText);
    //         console.log("Good, it works")
            
    //         if (data.success) {
    //             document.querySelector(".room").innerHTML = data.channel;
    //             console.log(data.channel);
    //     }
    // }