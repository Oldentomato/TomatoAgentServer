#!/bin/bash

docker swarm init 
docker stack deploy -c docker-compose-deploy.yml agent_stack