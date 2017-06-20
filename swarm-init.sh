#!/bin/bash

export PWD_URL="${1}"

if [[ -z "${PWD_URL}" ]]; then
    echo "Please pass a play-with-docker url"
    exit 1
fi

# create the swarm nodes
echo "Creating node1 ..."
docker-machine create -d pwd node1
echo "Creating node2 ..."
docker-machine create -d pwd node2
echo "Creating node3 ..."
docker-machine create -d pwd node3

# Initialize node1 as a leader
echo "Creating swarm leader on node1"
eval $(docker-machine env node1)
docker swarm init --advertise-addr eth0

# Get the join token and leader address
JOIN_TOKEN=$(docker swarm join-token -q worker)
LEADER_IP=$(docker-machine inspect node1 | jq -r '.Driver | .IPAddress')
LEADER_ADDR="${LEADER_IP}:2377"

# Have node2 join the swarm
echo "Creating swarm worker on node2"
eval $(docker-machine env node2)
docker swarm join --token "${JOIN_TOKEN}" "${LEADER_ADDR}"

# Have node3 join the swarm
echo "Creating swarm worker on node3"
eval $(docker-machine env node3)
docker swarm join --token "${JOIN_TOKEN}" "${LEADER_ADDR}"
