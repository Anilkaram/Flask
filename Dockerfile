# Use an official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy app code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
