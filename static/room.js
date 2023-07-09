var socketio = io();
const message = document.getElementById("messages")

const createMessage = (name, msg) => {
    const content = `
<div class="text">
    <span>
        <strong>${name}</strong>: ${msg}
    </span>
    <span class="muted">
        ${new Date().toLocaleString()}
    </span>
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
    message.value = ""
};