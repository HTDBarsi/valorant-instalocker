const http = require('http');
const fs = require('fs');
const url = require('url');
const runCmd = require("node-run-cmd");

let counter = 0;
http.createServer(function (req, res) {
    p = url.parse(req.url,true)
    console.log(p.pathname)
    switch(p.pathname){
        case "/lock":
            console.log(`Locking ${p.query.agent}..`);
            runCmd.run(`py ./insta.py ${p.query.agent}`)
            .then(() => {
                console.log("Executed");
              })
              .catch((error) => {
                console.log(`Error: ${error.message}`);
            });
        case "/":
            p = "/index.html";
        default:
            if (!fs.existsSync("."+p.pathname)){p.pathname = "/index.html";}
            fs.readFile("."+p.pathname, function(err, data) {
                try{
                    res.write(data);
                } catch {return "Error!"}
                return res.end();
            });
            break;
    }
}).listen(80);