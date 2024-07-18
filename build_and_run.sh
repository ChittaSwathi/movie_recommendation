#!/bin/bash

# Build Docker image
docker build -t fast_api:latest .

# removing existing docker container
docker stop my_container
docker rm my_container

# Run Docker container
docker run --name my_container -p 80:80 -v /Users/swathichitta/Desktop/Codebase/MoviesRecommendation:/code fast_api:latest

