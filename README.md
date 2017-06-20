# Hangman 2017

A docker and docker swarm example with a simple hangman game with load balancing on play with docker.

## Requirements

1. **docker** is required. Download at https://docs.docker.com/engine/installation/
2. **jq** library is required. OSX: brew install jq, DEBIAN: apt-get install jq

## Running development

```
$ cd hangman
$ docker-compose up -d
```

or


```
$ cd hangman
$ docker-compose run --rm hangman bash
```

## Deploying to play with docker

#### Step 1 - Install the docker machine driver

Download the docker play-with-docker driver and put it on your path.

```
$ mkdir -p /tmp/dm
$ cd /tmp/dm
$ wget https://github.com/franela/docker-machine-driver-pwd/releases/download/v0.0.5/docker-machine-driver.tgz
$ gunzip docker-machine-driver.tgz
$ cp darwin/amd64/docker-machine-driver-pwd /usr/local/bin  # assuming osx
```

#### Step 2 - Create the Docker Swarm Cluster

Run the scripts in this order. Profit.

```
PWD_URL="<play-with-docker-url>"
./swarm-init.sh "<play-with-docker-url>"
./swarm-visualizer.sh
./swarm-registry.sh
./swarm-build.sh
```

#### Step 3 - Create the hangman stack

Lauch the application

```
$ eval $(docker-machine env node1)
$ docker stack deploy -c docker-compose-stack.yml hangman
```

#### Step 4 - Expose TCP port using ngrok (limitation of play-with-docker)

```
$ export NKEY="<yourngrokkey>"
$ export LEADER_IP=$(docker-machine inspect node1 | jq -r '.Driver | .IPAddress')
$ docker run --rm -e NGROK_AUTH="${NKEY}" -e LEADER_IP="${LEADER_IP}" -it wernight/ngrok sh -c "ngrok tcp -authtoken=\$NGROK_AUTH \$LEADER_IP:9000"
```

## Clean up

```
./swarm-clean.sh
```