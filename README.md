# Hangman 2017

A docker and docker swarm example with a simple hangman game with load balancing on play with docker.

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

### Step 1

Download the docker play-with-docker driver and put it on your path.

```
$ wget https://github.com/franela/docker-machine-driver-pwd/releases/download/v0.0.5/docker-machine-driver.tgz
```

### Step 2

Run the scripts in this order. Profit.

```
PWD_URL="<play-with-docker-url>"
./swarm-init.sh "<play-with-docker-url>"
./swarm-visualizer.sh
./swarm-registry.sh
./swarm-build.sh
```

### Step 3

Lauch the application

```
$ eval $(docker-machine env node1)
$ docker stack deploy -c docker-compose-stack.yml hangman
```

### Clean up

```
./swarm-clean.sh
```