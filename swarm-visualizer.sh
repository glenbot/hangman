#!/bin/bash

eval $(docker-machine env node1)
docker service create \
  --name=viz \
  --publish=8888:8080/tcp \
  --constraint=node.role==manager \
  --mount=type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
  dockersamples/visualizer
