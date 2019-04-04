
document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {
        
        document.querySelector('#channelForm').onsubmit = () => { 

            const channel = document.querySelector('#channelInput').value;            
            socket.emit('create channel', {'channel' :channel});
            
            document.querySelector('#channelInput').value = '';
            console.log("excuse me")
            return false;
        }
        
        document.querySelector('#messageForm').onsubmit = () => {
            const message = document.querySelector('#messageInput').value;
            console.log(message);
            
            var now = new Date();
            
            console.log(now.getHours(), now.getMinutes(), now.getMonth(), now.getDay(), now.getFullYear());
            document.querySelector('#messageInput').value = '';
            var hours = now.getHours();
            if (hours > 12) {
                hours -= 12;
            }

            var timeConvention = (hours > 12) ? "AM" : "PM";
            var minutes = now.getMinutes();
            if (minutes < 10) {
                minutes = '0' + minutes;
                console.log(minutes);
            }

            var time = hours + ':' + minutes + ' ' + timeConvention;
            var date = (now.getMonth() + 1) + '/' + now.getDate() + '/' + now.getFullYear();
            var sender = document.querySelector('#username').innerHTML;
            socket.emit('store message', {'sender': sender, 'message': message, 'channel': 'Placeholder', 'date': date, 'time': time});
            return false;
        }
    
    });

    socket.on('add channel', (data) => {
        // Replace these with JS template and also use it to format the text messages
        const a = document.createElement('a');
        a.innerHTML = data;
        a.classList.add('room');
        a.setAttribute("href", "#");
        document.querySelector('ol').append(a);
        console.log("well");
    });

    socket.on('send message', (data) => {
        // Replace these with JS template and also use it to format the text messages
        console.log("Yee haw!");
        console.log(data);
    });

});
    
   
