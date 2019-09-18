FROM python:3.7-alpine

# Set working directory
WORKDIR /app

# Install runtime dependencies, build dependencies, Python dependencies, and
# then remove build dependencies to keep the image as small as possible
COPY requirements.pip .
RUN apk --no-cache add postgresql-libs libmagic ffmpeg \
        && apk --no-cache add --virtual .build-deps gcc musl-dev postgresql-dev \
        && pip --no-cache-dir install -r requirements.pip \
        && apk --no-cache del .build-deps

# Install application
COPY . .
