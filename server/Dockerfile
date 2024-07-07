# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables to prevent Python from buffering stdout and to specify the Flask app
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Create a directory for the app
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that the app will run on
EXPOSE 5000

# Define the command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
