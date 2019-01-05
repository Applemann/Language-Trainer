#!/bin/bash
word=$1
response=$(curl -d "{\"engine\":\"Google\",\"data\":{\"text\":\"$word\",\"voice\":\"en-GB\"}}" -H "Content-Type: application/json" -X POST https://api.soundoftext.com/sounds)

code=$(echo $response | awk -F'"' '{print $6}')

response=$(curl https://api.soundoftext.com/sounds/$code)

url=$(echo $response | awk -F'"' '{print $8}')

wget $url -O "sounds/${word}.mp3"
