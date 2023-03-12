# Workoustic 🏃‍♂️🏃‍♀️🎶
Generate workout ideas from your music!

Are you struggling to start working out? Does your workout session feels boring?
With Workoustic, you can generate a fun workout playlist that is synced with your selected music from Spotify.

## 📌 Instructions
Currently, the service is up on [34.67.92.121](http://34.67.92.121).

There are 3 main features in this service:
1. Generate workout playlist with Spotify track IDs;
2. Generate workout playlist with Spotify track search; and
3. Open previously generated workout playlist.

### 1. Generate workout playlist with Spotify track IDs

## 💻 Development
To run on your local environment, first ask me [here](mailto:marcellinocovara@gmail.com) for the `.env` file and make sure to have [docker](https://docker.com) installed.

Go to the root directory and run:
```
docker compose up -f docker-compose.dev.yml -d --build
```

## 🚀 Deployment
To run on production environment, run:
```
docker compose up -d --build
```


## 🙏 Acknowledgements 
Thank you for [API Ninjas](https://api-ninjas.com) and [Spotify for Developers](https://developer.spotify.com) for providing the data and services needed for this project.
