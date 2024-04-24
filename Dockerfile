# Run "docker build -t myapp:latest" to build docker
# Run "docker run -p 3000:3000 myapp:latest" to launch docker

# Base image that supports Node/Express and Python
FROM nikolaik/python-nodejs:latest

# Set working directory - subsequent commands added to /app
WORKDIR /app

# Install OpenGL library (with updates) from OpenCV
RUN apt-get update && apt-get install -y \libgl1-mesa-glx

# Copy package.json and package-lock.json for Node dependencies in /app
COPY package*.json ./

# Install Node dependencies
RUN npm install

# Copy requirements.txt for Python dependencies in /app
COPY requirements.txt ./

# Install Python dependencies without storing cache for smaller images
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to container's workspace (COPY source dest)
COPY . .

# Hint which port Node app runs on
EXPOSE 3000

# Start Node app
CMD ["npm", "start"]