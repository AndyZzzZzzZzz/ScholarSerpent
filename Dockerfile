# Use a lightweight Python base image
FROM python:3.9-slim

# Install necessary dependencies for Tkinter and X11 forwarding
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-tk \
    libx11-6 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements.txt first to leverage Docker caching
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Set the display to use the host system's X server (for GUI)
ENV DISPLAY=:0

# Run the Tkinter application
CMD ["python", "ScholarSerpent.py"]
