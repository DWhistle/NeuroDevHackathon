'use strict';

function required(name) {
    const value = process.env[name];
    if (!value || value.startsWith('REPLACE_')) {
        throw new Error(`Set ${name} in the environment before starting the database service`);
    }
    return value;
}

exports.database = function () {
    return {
        client: 'mysql',
        connection: {
            host: process.env.DB_HOST || '127.0.0.1',
            user: required('DB_USER'),
            password: required('DB_PASSWORD'),
            database: required('DB_NAME')
        }
    };
};
exports.rpcEndpoint = process.env.RPC_ENDPOINT || 'tcp://127.0.0.1:4242';
