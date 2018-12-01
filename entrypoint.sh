#!/bin/sh
set -e

exec python3 /app/flickrmirrorer/flickrmirrorer.py "$@" /data
