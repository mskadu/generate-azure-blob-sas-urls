FROM python:3.13-slim

# Install bash shell
RUN apt-get update && \
    apt-get install -y --no-install-recommends bash 

# Install packages necessary to handle TLS/SSL
RUN apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy over the TLS/SSL certificates
COPY .cert[s] /usr/local/share/ca-certificates/
RUN update-ca-certificates -v

# Set working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --user -r requirements.txt

# Install application code
COPY . .