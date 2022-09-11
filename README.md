

# Baby Tracker
## Line Bot for baby activity tracking

## Features
- Log baby activities, like feed volumn, daiper, weights, temperature
- Daiper changing or feed reminder
- Suggestion of feed volumn

## Tech
- Django - backend server

## Installation
### Docker
#### signup line message API and change CHANNEL ACCESS TOKEN & CHANNEL SECRET
```sh
docker run -p 8000:8000 -e LINE_CHANNEL_ACCESS_TOKEN='' -e LINE_CHANNEL_SECRET='' rejectsgallery/baby_tracker:1.2 .
```
Since Line bot message API only accept https, so you need to use ngork to router API to https endpoint
```sh
./ngrok http 8000
```