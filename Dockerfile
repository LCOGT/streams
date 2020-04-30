################################################################################
# Build Image
#
# We use this image as a dumping ground to install all sorts of build-time
# dependencies (compilers, development headers, etc.). Then we build and
# install all dependencies and then our application into the /app directory
# so that we can easily copy just the final build artifacts.
#
# We don't need to worry about cleaning up nicely since we are just throwing
# this image away.
################################################################################
FROM python:3.8-slim-buster as builder

# Set working directory
WORKDIR /app

# install OS-level build dependencies
RUN apt-get -y update \
        && apt-get -y install gcc gfortran libpq-dev \
        && apt-get -y clean

# create a virtualenv and install all dependencies into it for easy copying
# into the final production image in one shot
COPY requirements.txt .
RUN python3 -m venv ./venv \
        && . ./venv/bin/activate \
        && pip --no-cache-dir install -r requirements.txt

# Install application code
COPY . .

################################################################################
# Production Image
################################################################################
FROM python:3.8-slim-buster

# Set application working directory
WORKDIR /app

# Install non-development libraries (runtime dependencies)
RUN apt-get -y update \
        && apt-get -y --no-install-recommends install \
            libgomp1 \
            libpq5 \
        && apt-get -y clean

# Make the virtualenv the first thing in the PATH so that everything in our
# container looks there first
ENV PATH=/app/venv/bin:$PATH

# Copy the whole application and all dependencies from the build image
COPY --from=builder /app /app
