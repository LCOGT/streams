FROM python:3.7-alpine

# Set working directory
WORKDIR /app

# Install runtime dependencies, build dependencies, Python dependencies, and
# then remove build dependencies to keep the image as small as possible
COPY requirements.txt .
RUN apk --no-cache add \
            ffmpeg \
            freetype \
            jpeg \
            lapack \
            libffi \
            libgfortran \
            libgomp \
            libmagic \
            libstdc++ \
            postgresql-libs \
            zlib \
        && apk --no-cache add --virtual .build-deps \
            freetype-dev \
            g++ \
            gcc \
            gfortran \
            jpeg-dev \
            lapack-dev \
            libffi-dev \
            musl-dev \
            postgresql-dev \
            zlib-dev \
        && pip --no-cache-dir install -r requirements.txt \
        && apk --no-cache del .build-deps

# Install application
COPY . .
