#!/bin/bash

eval $(docker-machine env node1)
docker service create --name registry --publish 5000:5000 registry:2
