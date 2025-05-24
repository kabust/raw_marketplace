# frontend/Dockerfile (for a standard Vue.js SPA)

# Stage 1: Build the Vue.js application
# Use a slim Node.js image for building
FROM node:20-alpine AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
# This means npm install will only run if these files change
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of the Vue.js application source code
COPY . .

# Build the Vue.js application for production
# 'npm run build' typically outputs to a 'dist' directory
RUN npm run build

# Stage 2: Serve the built application with Nginx
# Use a very lightweight Nginx image
FROM nginx:alpine

# Copy the built Vue.js application from the builder stage to Nginx's HTML directory
# The 'dist' directory is where 'npm run build' places the compiled assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy a custom Nginx configuration file
# This is crucial for single-page applications (SPAs) like Vue.js
# It ensures that all routes are handled by index.html (client-side routing)
COPY nginx.conf /etc/nginx/conf.d/

# Expose port 80, which Nginx will listen on
EXPOSE 80

# The default command for Nginx is to start the server, which is fine
CMD ["nginx", "-g", "daemon off;"]