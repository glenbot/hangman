# Hangman 2020

A telnet hangman python game for kubernetes developent and deployment example

## Requirements

1. **docker** is required. Download at https://docs.docker.com/engine/installation/
2. **minikube** is required. https://minikube.sigs.k8s.io/docs/start/
3. **kubectl** is required. https://kubernetes.io/docs/tasks/tools/install-kubectl/
4. **skaffold** is required. https://skaffold.dev/docs/quickstart/
5. **helm3** is required. https://v3.helm.sh/

## TODO

* Make words configurable

## Running development

```
$ minikube start
$ cd hangman
$ skaffold dev
```

## Deploying k8s cluster

```
$ minikube start
$ cd hangman
$ helm install hangman helm/hangman
```
