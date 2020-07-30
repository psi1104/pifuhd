const obj2gltf = require('obj2gltf');
const fs = require('fs');

const gltf = obj2gltf(process.argv[2]+'/result.obj') // 경로로 수정 필요
    .then(function(gltf) {
        const data = Buffer.from(JSON.stringify(gltf));
        fs.writeFileSync(process.argv[2]+'/model.gltf', data);
        // process.stdout.write(data)
    });

