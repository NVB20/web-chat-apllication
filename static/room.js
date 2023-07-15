var socketio = io();
const message = document.getElementById("messages")


socketio.on("message", (data) => {
createMessage(data.name, data.message, data.time);
});


const sendMessage = () => {
    const message = document.getElementById("user_message")
    if (message.value == "") return;
    socketio.emit("message", {data: message.value})
    setTimeout(scrollChatToBottom, 100);
    message.value = "";
};


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


const leave_button = document.getElementById("leave_room");
leave_button.addEventListener("click", function() {
  console.log("Button pressed!");
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
          <span>
              <strong>${name}</strong>: ${msg}
          </span>
          <span class="muted">
              ${time}
          </span>
      </div>
      `;
    
    message.innerHTML += content;
};
