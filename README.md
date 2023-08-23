<h1>Flask Chatroom App with MongoDB</h1>
<div>
    <p>This repository contains a Flask and MongoDB application for a chatroom system that allows users to join existing chatrooms or create secret rooms using special room codes.</p>
</div>
<div>
    <h2>Features</h2>
    <ul>
        <li>Multiple chatrooms: The app supports four pre-defined chatrooms that users can choose from.</li>
        <li>Secret rooms: Users can create new secret rooms by entering a special room code.</li>
        <li>Real-time chat: The chatrooms provide real-time messaging using websockets powered by Flask-SocketIO.</li>
        <li>Data persistence: The chat messages are stored in a MongoDB database for data persistence.</li>
    </ul>
</div>
<div>
    <h2>Getting Started</h2>
    <ol>
        <li>Clone the repository:
            <code>git clone https://github.com/your-username/flask-mongodb-chatroom.git</code></li>
        <li>Install the required dependencies:
            <code>pip install -r requirements.txt</code></li>
        <li>Set up MongoDB:
            <ul>
                <li>Install MongoDB and make sure it's running.</li>
                <li>Update the MongoDB URI in <code>config.py</code> with your MongoDB connection details.</li>
            </ul>
        </li>
        <li>Start the Flask app:
            <code>python app.py</code></li>
        <li>Open your browser and navigate to <a href="http://localhost:5000">http://localhost:5000</a> to access the
            chatroom application.</li>
    </ol>
</div>
<div>
    <h2>Usage</h2>
    <ol>
        <li>Choose a chatroom: Select one of the four pre-defined chatrooms to join.</li>
        <li>Create a secret room: Enter a special room code to create a new secret room. Share the code with others
            to let them join the secret room.</li>
        <li>Start chatting: In the chatroom, send and receive real-time messages.</li>
    </ol>
</div>
<div>
    <h2>Contributing</h2>
    <p>Contributions are welcome! If you'd like to contribute to the project, please follow these steps:</p>
    <ol>
        <li>Fork the repository.</li>
        <li>Create a new branch for your feature/fix: <code>git checkout -b feature-name</code>.</li>
        <li>Make your changes and commit them.</li>
        <li>Push to your forked repository.</li>
        <li>Submit a pull request to the <code>main</code> branch of this repository.</li>
    </ol>
</div>
<div>
    <h2>Acknowledgements</h2>
    <ul>
        <li><a href="https://flask.palletsprojects.com/">Flask</a></li>
        <li><a href="https://flask-socketio.readthedocs.io/">Flask-SocketIO</a></li>
        <li><a href="https://www.mongodb.com/">MongoDB</a></li>
    </ul>
</div>
