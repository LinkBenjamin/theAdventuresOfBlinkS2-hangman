#!/bin/bash

echo "Starting Ollama serve in the background..."
ollama serve &
serve_pid=$!

if [ $? -ne 0 ]; then
    echo "Error starting Ollama server"
    exit 1
fi

echo "Waiting for Ollama server to be ready..."
wait_time=5
max_retries=10
while true; do
    if curl -s http://localhost:11434/ > /dev/null; then
        break
    fi
    echo "Ollama server not ready, retrying in $wait_time seconds..."
    sleep $wait_time
    wait_time=$((wait_time * 2))
    ((max_retries--))
    if [ $max_retries -eq 0 ]; then
        echo "Ollama server failed to start"
        exit 1
    fi
done

echo "Ollama server is ready."

if ! ollama list | grep -q "llama3.2"; then
    echo "Model llama3.2 not found. Downloading..."
    ollama pull llama3.2
    if [ $? -ne 0 ]; then
        echo "Error downloading llama3.2 model"
        exit 1
    fi
    echo "Model llama3.2 download complete."
else
    echo "Model llama3.2 already downloaded."
fi

trap 'kill -SIGTERM $serve_pid' SIGINT SIGTERM

echo "Ollama server is now running in the background."

while true; do
    sleep 60
done