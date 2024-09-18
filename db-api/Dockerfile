# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5001

# Define environment variable for Flask
ENV FLASK_APP=api
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

# Run Flask app when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]