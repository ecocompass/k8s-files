# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Set the working directory in the container
WORKDIR /app
ENV PYTHONUNBUFFERED=1
# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r req.txt


# Run flask-api.py when the container launches
CMD ["python", "-u", "rabbit-app.py"]

