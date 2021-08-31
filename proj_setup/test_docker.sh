#!/bin/bash

docker run -d \
           -v $(pwd):/app \
           -p 5000:5000 \
           -p 1433:1433 \
           --name test-container \
           test_init