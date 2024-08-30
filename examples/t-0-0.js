#!/usr/bin/env nodejs
var config = {
    user: 'sa',
    password: 'SaAdmin1@',
    server: '127.0.0.1',
    database: 'testing',

    options: {
        encrypt: false // Use this if you're on Windows Azure
    }
};
const stmt = "select idrow, data from t where data = 'some %% value'";

const sql = require('mssql')

sql.connect(config, err => {
    const request = new sql.Request();
    request.stream = true // You can set streaming differently for each request
    console.log('execute', stmt);
    request.query(stmt);

    request.on('recordset', columns => {
        console.log("recordset", columns);
    })

    request.on('row', row => {
        console.log("row", row);
    })

    request.on('error', err => {
        console.log("error", err);
    })

    request.on('done', result => {
        console.log("done", result);
        process.exit(0);
    })

});

sql.on('error', err => {
    console.log("error", err)
})
