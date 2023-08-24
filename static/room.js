var socketio = io();
const message = document.getElementById("messages")


socketio.on("message", (data) => {
  createMessage(data.name, data.message, data.time);
});



const input = document.getElementById("user_message");
input.addEventListener("keydown", function(event) {
  if (event.key === 'Enter') {
    event.preventDefault();
    sendMessage();
  }
});

const sendMessage = () => {
  const message = document.getElementById("user_message")
  if (message.value == "") return;
  socketio.emit("message", {data: message.value})
  setTimeout(scrollChatToBottom, 100);
  message.value = "";
};


const leave_button = document.getElementById("leave_room");
leave_button.addEventListener("click", function() {
  console.log("Leave pressed!");
  socketio.emit("disconnect")
});


async function load_messages() {
  return await fetch("/get_messages")
    .then(async function (response) {
      return await response.json();
    })
    .then(function (text) {
      console.log(text);
      return text;
    });
}


window.onload = async function () {
  var msgs = await load_messages();
  for (i = 0; i < msgs.length; i++) {

    const name = msgs[i][0];  
    const message = msgs[i][1];
    const time = msgs[i][2];
    
    createMessage(name, message, time);
  };
};


const createMessage = (name, msg, time) => {
    
    const content = `
      <div class="text-message">
        <div class="name">
          ${name}
        </div>
        <div class="message-time-container">
          <div class="msg">
            ${msg}
          </div>
          <div class="time">
            ${time}
          </div>
        </div>
      </div>
      `;
    
    message.innerHTML += content;
    scrollChatToBottom();
};

function scrollChatToBottom() {
  var chatContainer = document.getElementById("messages");
  chatContainer.scrollTop = chatContainer.scrollHeight;
}
