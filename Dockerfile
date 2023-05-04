
# Start with the base Python image
FROM python:3.11.3-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the virtual environment into the image
COPY ./env /app/env

# Activate the virtual environment
RUN . /app/env/bin/activate

# Copy the rest of the application code into the image
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
