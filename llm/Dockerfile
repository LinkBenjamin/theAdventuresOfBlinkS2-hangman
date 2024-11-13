# Start with the official Ollama base image
FROM ollama/ollama:latest

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy a startup script into the container
COPY start_model.sh /usr/local/bin/start_model.sh
RUN chmod +x /usr/local/bin/start_model.sh

# Expose the necessary port for Ollama
EXPOSE 8080
EXPOSE 11434

# Run the startup script when the container starts
ENTRYPOINT ["/usr/local/bin/start_model.sh"]