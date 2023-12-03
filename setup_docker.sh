#!/usr/bin/env bash

docker build -t teleparser .
docker container create teleparser
docker container run teleparser

