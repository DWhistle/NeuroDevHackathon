const io = require('./ws').io;
const {HELLO} = require('./Events');
const zerorpc = require('zerorpc');

const dbknex = {
    client: 'mysql',
    connection: {
        host: '35.204.124.30',
        user: 'root',
        password: 'admin',
        database: 'new_schema'
    }
};

const knex = require('knex')(dbknex);

module.exports = async function(socket) {
    var client = new zerorpc.Client();
//console.log(client);
    client.connect("tcp://127.0.0.1:4242");
    console.log('socket id: ' + socket.id);
await client.invoke('streaming_range', 1,2,3, (req, res) =>{console.log(res)});

socket.on('GETTOP', async(id) => {
console.log(id, 'hi from gettop'); 
await client.invoke('streaming_range', 1,2,3, (req, res) => {
io.emit('RETURNDATA', res);
});
});

	socket.on('FINISH', async (exp) =>{
    await knex.from('instances').select('*').where('experiment', '=', exp)
.then(async (arr) => {
let newarr = [];
await arr.forEach((item) => {newarr.push(JSON.parse(item.jsonFile))});
console.log(newarr);
 client.invoke('streaming_range', 1, newarr, 3, (error,res, more) => {
console.log(res, error, more);
socket.emit('TEST', res);
})
})
})
};
