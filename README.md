
```
docker run \
    --name flickr \
    --init \
    --rm \
    --read-only \
    --user $(id -u):$(id -g) \
    --volume /home/me/.flickr:/config/.flickr \
    --volume /home/me/photos:/data \
    robertbeal/flickrmirrorer --verbose --statistics
```
