FROM python:3.10-alpine AS builder
LABEL maintainer="github.com/robertbeal"

RUN apk add --no-cache \
  git \
  py3-virtualenv

WORKDIR /app

RUN git clone https://github.com/robertbeal/flickrmirrorer.git

RUN python3 -m venv /app/venv \
  && . /app/venv/bin/activate \
  && pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir flickrapi==2.4.0 python-dateutil

FROM python:3.10-alpine
LABEL maintainer="github.com/robertbeal"

ARG ID=3999

WORKDIR /app
COPY entrypoint.sh /usr/local/bin

RUN apk add --no-cache \
  su-exec \
  && mkdir -p /config \
  && addgroup -g $ID flickr \
  && adduser -s /bin/false -D -H -u $ID -G flickr flickr \
  && chown flickr:flickr /app /config \
  && chmod 500 /app \
  && chmod 700 /config

# Copy the virtual environment and application code from the builder stage
COPY --from=builder /app/venv /app/venv
COPY --from=builder /app/flickrmirrorer /app/flickrmirrorer

# Ensure entrypoint script is executable
RUN chmod 555 /usr/local/bin/entrypoint.sh

# Set environment variables
ENV PATH="/app/venv/bin:$PATH"
ENV HOME /config

# Define volumes
VOLUME /config /data

# Set entrypoint and command
ENTRYPOINT ["entrypoint.sh"]
CMD ["--help"]
