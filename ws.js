const app = require('express')()
const http = require('http').createServer(app)
const io = (module.exports.io = require('socket.io')(http))
const socketManager = require('./socketManager');
const PORT = 25565

//const socketManager = require('./socketManager')

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html')
})

io.on('connection', socketManager)


http.listen(PORT, () => {
    console.log('socket on:' + PORT)
})
