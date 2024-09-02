# Use a lightweight Python base image
FROM python:3.9-slim

# Install Tkinter
RUN apt-get update && apt-get install -y python3-tk

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any required packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the display to use the host system's X server (for GUI)
ENV DISPLAY=:0

# Run your main Tkinter application script
CMD ["python", "ScholarSerpent.py"]
