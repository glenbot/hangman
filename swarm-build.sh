#!/bin/bash

eval $(docker-machine env node1)
docker build -t localhost:5000/hangman .
docker push localhost:5000/hangman
