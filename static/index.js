document.addEventListener('DOMContentLoaded', () => {

    if (!localStorage.getItem('stored-channel'))
        localStorage.setItem('stored-channel', 'General');
    console.log(localStorage.getItem('stored-channel'), "Hallo");
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {

        // Sending channel input server side
        document.querySelector('#channelForm').onsubmit = () => { 
            const channel = document.querySelector('#channelInput').value;            
            socket.emit('create channel', {'channel' :channel});
            document.querySelector('#channelInput').value = '';
            return false;
        }
        
        document.querySelector('#messageForm').onsubmit = () => {
            const message = document.querySelector('#messageInput').value;
            document.querySelector('#messageInput').value = '';
            var sender = document.querySelector('#username').innerHTML;
            var now = new Date();
            
            // Getting hours and determining whether AM or PM
            var timeConvention = "AM"
            var hours = now.getHours();
            if (hours > 12) {
                hours -= 12;
                timeConvention = "PM"
            }

            // Getting and formatting minutes
            var minutes = now.getMinutes();
            if (minutes < 10) {
                minutes = '0' + minutes;
                console.log(minutes);
            }

            // Formatting the today's date with the time together
            var time = hours + ':' + minutes + ' ' + timeConvention;
            var date = (now.getMonth() + 1) + '/' + now.getDate() + '/' + now.getFullYear();
            date += ' ' + time;
            
            // Submitting the data to store server side
            socket.emit('store message', {'sender': sender, 'message': message, 'channel': 'General', 'date': date});
            return false;
        }

        document.querySelectorAll('.room').forEach(a => {
            a.onclick = () => {
                console.log(a.innerHTML)
                localStorage.setItem('stored-channel', a.innerHTML);
            }
        });

        
    
    });

    socket.on('add channel', (data) => {
        // Replace these with JS template and also use it to format the text messages
        // Creating a link for the new channel
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
        last = items[items.length - 1];
        last.scrollIntoView();
        
    });
});