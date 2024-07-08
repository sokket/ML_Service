FROM nginx:1.27.0-alpine

# Generate SSL self-signed cert
RUN apk add openssl --no-cache && \
    openssl req -x509 -nodes -days 365 -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=www.example.com" -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt && \
    apk del openssl

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80 443