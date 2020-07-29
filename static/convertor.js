const obj2gltf = require('obj2gltf');
const fs = require('fs');

console.log(__dirname)
obj2gltf(__dirname+'/result_irene_body_2_512.obj')
    .then(function(gltf) {
        const data = Buffer.from(JSON.stringify(gltf));
        fs.writeFileSync('./static/model.gltf', data);
    });