# docker-flickrmirrorer

A container built version of [flickrmirrorer](https://github.com/markdoliner/flickrmirrorer) that I use for backing up my flickr account photos.

It's alpine based, built in mult-arch and published to DockerHub

## Usage

Getting set up on your host...

```
# create a flickr user
sudo useradd -u 3999 --system --no-create-home --shell /bin/false --user-group --groups photos flickr
# add the user to the 'docker' group
sudo gpasswd -a flickr docker
# create a config directory
sudo mkdir -p /var/flickr
# make sure the 'flickr' user owns the config and data folders
sudo chown -R flickr:flickr /var/flickr
sudo chown -R flickr:flickr /mnt/photos
```

Running the container...

```
docker run \
    --name flickr \
    --init \
    --rm \
    --read-only \
    --user $(id flickr -u):$(id flickr -g) \
    --volume /var/flickr:/config/.flickr \
    --volume /mnt/photos:/data \
    robertbeal/flickrmirrorer --verbose --statistics
```
