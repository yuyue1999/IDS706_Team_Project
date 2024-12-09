# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose port 5000 for Flask
EXPOSE 8080
EXPOSE 14124

# Run the application
CMD ["python", "app.py"]