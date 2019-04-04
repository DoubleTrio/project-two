document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {
        
        document.querySelector('#channelForm').onsubmit = () => { 

            const channel = document.querySelector('#channelInput').value;            
            socket.emit('create channel', {'channel' :channel});
            
            document.querySelector('#channelInput').value = '';
            
            return false;
        }
        
        document.querySelector('#messageForm').onsubmit = () => {
            const message = document.querySelector('#messageInput').value;
            
            var now = new Date();
            
            
            document.querySelector('#messageInput').value = '';
            var timeConvention = "AM"
            var hours = now.getHours();
            if (hours > 12) {
                hours -= 12;
                timeConvention = "PM"
            }

            
            var minutes = now.getMinutes();
            if (minutes < 10) {
                minutes = '0' + minutes;
                console.log(minutes);
            }

            var time = hours + ':' + minutes + ' ' + timeConvention;
            var date = (now.getMonth() + 1) + '/' + now.getDate() + '/' + now.getFullYear();
            date += ' ' + time;
            var sender = document.querySelector('#username').innerHTML;
            socket.emit('store message', {'sender': sender, 'message': message, 'channel': 'Placeholder', 'date': date});
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

    });

    socket.on('send message', (data) => {

        // Formatting the user's message in a template and posting it
        const template = Handlebars.compile(document.querySelector('#sent-message').innerHTML);
        const content = template({'sender': data.sender, 'message': data.message, 'date': data.date});
        document.querySelector('#chatlog').innerHTML += content;

        // Scroll to the bottom of the chat when a message is posted
        // Source Code: https://stackoverflow.com/questions/31716529/how-can-i-scroll-down-to-the-last-li-item-in-a-dynamically-added-ul/31716758
        // From Eduard Florinescu's answer
        items = document.querySelectorAll(".message-format");   
        last = items[items.length-1];
        last.scrollIntoView();
        
    });
});
    
   
