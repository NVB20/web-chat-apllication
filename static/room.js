var socketio = io();
const message = document.getElementById("messages")

const createMessage = (name, msg) => {
    
  const date = new Date();
  const minutes = date.getMinutes().toString().padStart(2, '0');
  const hours = date.getHours().toString().padStart(2, '0');
    
    const content = `
<div class="text-message">
    <span>
        <strong>${name}</strong>: ${msg}
    </span>
    <span class="muted">`+
        hours + ":" + minutes
    +`</span>
</div>
`;
    
    message.innerHTML += content;
};

socketio.on("message", (data) => {
createMessage(data.name, data.message);
});



const sendMessage = () => {
    const message = document.getElementById("user_message")
    if (message.value == "") return;
    socketio.emit("message", {data: message.value})
    setTimeout(scrollChatToBottom, 100);
    message.value = "";
};


//post message from enter press
const input = document.getElementById("user_message");
input.addEventListener("keydown", function(event) {
  if (event.keyCode === 13) {
    sendMessage();
  }
});


function scrollChatToBottom() {
  var chatContainer = document.getElementById("messages");
  chatContainer.scrollTop = chatContainer.scrollHeight;
}