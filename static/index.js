document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {
        
        document.querySelector('#channelForm').onsubmit = () => { 

            const channel = document.querySelector('#channelInput').value;            
            socket.emit('create channel', {'channel' :channel});
            
            document.querySelector('#channelInput').value = '';
            return false;
        }  
    });

    socket.on('add channel', (data) => {
        // Replace these with JS template
        const a = document.createElement('a');
        a.innerHTML = data;
        a.classList.add('room')
        a.setAttribute("href", "#");
        document.querySelector('ol').append(a);
        
    });
});
    
   
