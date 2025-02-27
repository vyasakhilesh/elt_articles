!/bin/bash

# Generate the private key for the CA
openssl genrsa -out ca.key 4096

# Generate the CA certificate
openssl req -new -x509 -days 365 -key ca.key -out ca.crt -subj "/CN=MyCA"

# Generate the private key for the server
openssl genrsa -out server.key 4096

# Generate a certificate signing request (CSR) for the server
openssl req -new -key server.key -out server.csr -subj "/CN=localhost"

# Sign the server certificate with the CA
openssl x509 -req -days 365 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt

# 