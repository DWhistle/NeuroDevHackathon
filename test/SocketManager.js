const io = require('./socket').io
const zerorpc = require('zerorpc')
const {PRISYAD, PRISYADONE} = require('./Events')


module.exports = function(socket) {
	console.log(socket);
  var client = new zerorpc.Client()
  client.connect('tcp://127.0.0.1:4242')
  console.log('socket id: ' + socket.id)
	socket.on('chat message', () => {
    console.log('CONNECT')
    client.invoke('streaming_range', 1, 3, 2, function(error, res) {
      io.emit('RESPONSETRAIN', res);
    })
});
  socket.on(PRISYADONE, obj => {
    console.log('CONNECT')
    client.invoke('streaming_range', 2, obj, 2, function(error, res) {
      console.log(res, 'sssss');
      io.emit('DATA', res);
    })
  })
}
