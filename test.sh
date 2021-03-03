#!/usr/bin/env bash

# add route
curl -X POST -H 'Content-Type: application/json' -d '{"id":"1", "title":"Write a blog post"}' localhost:8080/add

curl -X GET localhost:8080/list

