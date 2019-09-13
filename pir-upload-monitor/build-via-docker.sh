#!/bin/sh
docker run -it --rm -v `pwd`:/data node:10 /bin/sh -c 'cd /data; npm i; npm run build'
