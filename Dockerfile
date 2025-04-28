# Step 1: Use a Python base image (Python 3.11-slim is a lightweight image)
FROM python:3.11-slim

# Step 2: Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    ca-certificates \
    curl \
    && apt-get clean

# Step 3: Set environment variables for Chrome binary
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMIUM_PATH=/usr/bin/chromium

# Step 4: Set the working directory inside the container
WORKDIR /app

# Step 5: Copy the requirements.txt into the container
COPY requirements.txt .

# Step 6: Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 7: Copy the rest of the application code
COPY . .

# Step 8: Expose port 5000 for Flask app (you can change the port if needed)
EXPOSE 5000

# Step 9: Command to run your application
CMD ["python", "main.py"]
