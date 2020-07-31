const obj2gltf = require('obj2gltf');
const fs = require('fs');

const gltf = obj2gltf(process.argv[2]+'/result.obj')
    .then(function(gltf) {
        const data = Buffer.from(JSON.stringify(gltf));
        fs.writeFileSync(process.argv[2]+'/model.gltf', data);
    });

