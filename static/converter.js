const obj2gltf = require('obj2gltf');
const fs = require('fs');
const options = {
    binary : true
}
const gltf = obj2gltf(process.argv[2]+'/result.obj', options)
    .then(function(glb) {
        fs.writeFileSync(process.argv[2]+'/model.glb', glb);
    });
