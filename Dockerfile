# Use a base image with Python
FROM python:3.9-slim

# Set up working directory
WORKDIR /app

# Copy necessary files
COPY requirements.txt requirements.txt
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for inference
EXPOSE 8080

# Command to run your inference app
CMD ["python", "app.py"]
