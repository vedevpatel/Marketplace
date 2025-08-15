# Use an official Node.js image as the base
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Add this line to update system packages and patch vulnerabilities
RUN apk update && apk upgrade

# Copy the package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend source code into the container
COPY . .

# Tell Docker that the container listens on port 3000
EXPOSE 3000

# Specify the new command to run the Vite dev server
CMD ["npx", "vite", "--host"]