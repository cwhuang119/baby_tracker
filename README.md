

```sh
docker buildx build --platform linux/amd64 -t rejectsgallery/baby_tracker:1.0 .
```


```sh
docker run -p 8000:8000 -e LINE_CHANNEL_ACCESS_TOKEN='' -e LINE_CHANNEL_SECRET='' rejectsgallery/baby_tracker:1.0 .
```