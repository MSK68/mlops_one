# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add current directory code to /app in container
COPY . /app/

# Upgrade pip
RUN python3 -m pip install --index-url=https://pypi.python.org/simple --trusted-host pypi.python.org --upgrade pip setuptools

# Install dependencies
RUN python3 -m pip install --index-url=https://pypi.python.org/simple --trusted-host pypi.python.org -r requirements.txt

# Run app.py when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
