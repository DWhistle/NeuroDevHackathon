const app = require('express')();
const PORT = process.env.PORT || 3035;
const client = require('socket.io-client');
const socket = client('http://127.0.0.1:25565');
const axios = require('axios');

app.get('/:id', (req, res) => {
socket.emit('FINISH', req.params.id);
let lol;
socket.on('TEST', (data) => { console.log(data);
return res.send(data)});
});

app.get('/get/:id', (req, res) => {
client.emit('GETTOP', req.params.id);
console.log(req.params.id)});
app.listen(PORT, () => {console.log('server client on :' + PORT)});


