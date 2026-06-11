#!/bin/bash
# Set PostgreSQL password without sudo

# Try to connect as postgres user and set password
sudo -u postgres psql << EOF
ALTER USER postgres WITH PASSWORD 'postgres123';
\q
EOF
