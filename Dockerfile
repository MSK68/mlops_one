# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# System upgrade
RUN apt-get update && apt-get install -y \
    openssl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /app
WORKDIR /app

# Add current directory code to /app in container
COPY . /app/

# Upgrade pip
RUN python3 -m pip install --upgrade pip setuptools

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Run app.py when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
