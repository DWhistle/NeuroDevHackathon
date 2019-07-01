const app = require('express')()
const http = require('http').createServer(app)
const io = (module.exports.io = require('socket.io')(http))

const PORT = 3030

const SocketManager = require('./SocketManager')

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html')
})

io.on('connection', SocketManager)

http.listen(PORT, () => {
  console.log('socket on:' + PORT)
})

