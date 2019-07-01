const logger = require('morgan');
const axios = require('axios');
const bodyParser = require('body-parser');
const app = require('express')();
const mysql = require('mysql');
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


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use(logger('dev'));
const http = require('http').createServer(app);
const io = (module.exports.io =  require('socket.io')(http));

const PORT = process.env.PORT || 3030;

//const socketManager = require('./socketManager');

app.get('/', (req, res) => {
    async function f(){
        let data = await knex.from('instances').select("*");
        console.log(data);
    }
    f();
    res.sendFile(
        __dirname + '/index.html'
    )});

app.post('/input', async (req, res) => {
    //save data to db
    await knex('instances').insert({jsonFile: req.body.data, experiment: req.body.tag}).then(() => {
        console.log('ok?');
    })
});
    app.post('/finish', async (req, res) => {
        //get BIG data from db and send to zerorpcserver
        //waiting rpc answer and send res to client!
console.log(req.body.title, 'hi from finish');
let kek = await axios.get('http://13.58.26.230:3035/' + req.body.title).then((item) => {console.log(item.data, 'from axios')}).catch((e)=> {console.log(e)});
console.log(kek.data);   
//io.on('TEST', (data) => {
//console.log(data);
//})
return res.send(kek.data);
});

app.post('/get', async (req, res) =>{
	console.log(req.body.id);
	await axios.get('http://13.58.26.230:3035/get/' + req.body.id);
let test;	
io.on('TEST', (res) => {
		console.log(res);
		test = res;
})
res.send('ALE');
});

//io.on('connection', socketManager);
    http.listen(PORT, () => {
        console.log('server started on ' + PORT);
    });


