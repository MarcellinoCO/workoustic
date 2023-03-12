# Workoustic 🏃‍♂️🏃‍♀️🎶
Generate workout ideas from your music!

Are you struggling to start working out? Does your workout session feels boring? According to [an article from New York Post](https://nypost.com/2019/01/13/this-is-why-most-americans-dont-exercise-more/), 35% of people feels lack of motivation to start working out. But with **Workoustic**, you can generate a fun workout playlist that is synced with your selected music from Spotify.

This service can help people to get motivated to workout by making their session more fun by snychronizing their favorite music tracks with recommended exercise that *adapts to the mood of the music*. This service is unique because currently there are no service that can synchronize the track with the exercise. This service tries to combine track energy analysis with exercise complexity to generate a fun workout playlist.

Users that have created a playlist before can access it again by saving the id of the generated playlist. This way, users can easily come back to the playlist without needing them to save the playlist themselves.


## 📌 Instructions
Currently, the service is hosted on [34.67.92.121](http://34.67.92.121). Postman collection can be accessed [here](https://elements.getpostman.com/redirect?entityId=12147807-123694f6-3a2e-49c0-89a4-70327157e3ef&entityType=collection).

There are 3 main features in this service:

### 1. Generate workout playlist with Spotify track IDs
#### HTTP GET /
Returns a playlist of Spotify tracks and selected workout(s) to accompany each track.

#### Parameters:
- **tracks** - list of Spotify track ID, separated by comma `,`
- **difficulty** (optional) - difficulty of workout recommendation, possible values are:
    - `beginner` (default)
    - `intermediate`
    - `expert`
- **muscle** (optional) - targeted muscle group of workout recommendation, possible values are:
    - `abdominals`
    - `abductors`
    - `adductors`
    - `biceps`
    - `calves`
    - `chest`
    - `forearms`
    - `glutes`
    - `hamstrings`
    - `lats`
    - `lower_back`
    - `middle_back`
    - `neck`
    - `quadriceps`
    - `traps`
    - `triceps`

#### Response Format:
```
{
  "id": int - generated playlist's id (can be queried later),
  "exercises_tracks": [
    {
      "track": {
        "id": str - Spotify track ID,
        "href": str - Spotify track stream url,
        "title": str - track title,
        "artist": str - track artist,
        "duration": int - track duration in seconds,
        "category": str - analyzed track category for workout (low, medium, high),
      },
      "exercises": [
        "name": str - exercise name,
        "difficulty": str - exercise difficulty,
        "muscle": str - targeted muscle group,
        "equipment": str - required equipment,
        "instructions": str - instructions for the exercise,
      ],
    },
  ],
}
```

#### Sample Request:
Create a playlist with track "As It Was" by Harry Styles:

> [http://34.67.92.121?tracks=4LRPiXqCikLlN15c3yImP7](http://34.67.92.121?tracks=4LRPiXqCikLlN15c3yImP7)

#### Sample Response:
```
{
  "id": 2,
  "exercises_tracks": [
    {
      "track": {
        "id": "4LRPiXqCikLlN15c3yImP7",
        "href": "https://open.spotify.com/track/4LRPiXqCikLlN15c3yImP7",
        "title": "As It Was",
        "artist": "Harry Styles",
        "duration": 167,
        "category": "medium"
      },
      "exercises": [
        {
          "name": "Front Squats With Two Kettlebells",
          "difficulty": "beginner",
          "muscle": "quadriceps",
          "equipment": "kettlebells",
          "instructions": "Clean two kettlebells to your shoulders. Clean the kettlebells to your shoulders by extending through the legs and hips as you pull the kettlebells towards your shoulders. Rotate your wrists as you do so. Looking straight ahead at all times, squat as low as you can and pause at the bottom. As you squat down, push your knees out. You should squat between your legs, keeping an upright torso, with your head and chest up. Rise back up by driving through your heels and repeat."
        },
        {
          "name": "Skating",
          "difficulty": "beginner",
          "muscle": "quadriceps",
          "equipment": "other",
          "instructions": "Roller skating is a fun activity which can be effective in improving cardiorespiratory fitness and muscular endurance. It requires relatively good balance and coordination. It is necessary to learn the basics of skating including turning and stopping and to wear protective gear to avoid possible injury. You can skate at a comfortable pace for 30 minutes straight. If you want a cardio challenge, do interval skating â€“ speed skate two minutes of every five minutes, using the remaining three minutes to recover. A 150 lb person will typically burn about 175 calories in 30 minutes skating at a comfortable pace, similar to brisk walking."
        }
      ]
    }
  ]
}
```

### 2. Generate workout playlist with Spotify track search
#### HTTP GET /search
Returns a playlist of Spotify tracks and selected workout(s) to accompany each track.

#### Parameters:
- **queries** - list of track search query, each enclosed in quotes `"`, separated by comma `,`
- **difficulty** (optional)
- **muscle** (optional)

#### Response Format:
Identical to previous feature

#### Sample Request:
Create a playlist with track "As It Was" by Harry Styles with "expert" difficulty:

> [http://34.67.92.121/search?queries="as%20it%20was"&difficulty=expert](http://34.67.92.121/search?queries="as%20it%20was"&difficulty=expert)

#### Sample Response:
```
{
  "id": 4,
  "exercises_tracks": [
    {
      "track": {
        "id": "4LRPiXqCikLlN15c3yImP7",
        "href": "https://open.spotify.com/track/4LRPiXqCikLlN15c3yImP7",
        "title": "As It Was",
        "artist": "Harry Styles",
        "duration": 167,
        "category": "medium"
      },
      "exercises": [
        {
          "name": "Hack Squat - Gethin Variation",
          "difficulty": "expert",
          "muscle": "quadriceps",
          "equipment": "machine",
          "instructions": ""
        },
        {
          "name": "Single-arm side deadlift",
          "difficulty": "expert",
          "muscle": "quadriceps",
          "equipment": "barbell",
          "instructions": "Stand to the side of a barbell next to its center. Bend your knees and lower your body until you are able to reach the barbell. Grasp the bar as if you were grabbing a briefcase (palms facing you since the bar is sideways). You may need a wrist wrap if you are using a significant amount of weight. This is your starting position. Use your legs to help lift the barbell up while exhaling. Your arms should extend fully as bring the barbell up until you are in a standing position. Slowly bring the barbell back down while inhaling. Tip: Make sure to bend your knees while lowering the weight to avoid any injury from occurring. Repeat for the recommended amount of repetitions. Switch arms and repeat the movement.  Caution: This is not an exercise that is recommended for people with lower back problems. Also, jerking motions or doing too much weight can injure your back. Variations: The exercise can also be performed with a dumbbell as described above."
        }
      ]
    }
  ]
}
```

### 3. Open previously generated workout playlist
#### HTTP GET /playlist
Returns a saved playlist of Spotify tracks and selected workout(s) to accompany each track.

#### Path Parameter:
- **id** - id of saved playlist, returned as response from previous features

#### Response Format:
Identical to previous features

#### Sample Request:
Open playlist with id 4:

> [http://34.67.92.121/playlist/4](http://34.67.92.121/playlist/4)

#### Sample Response:
Identical to previous feature


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

## 📝 Additional Notes
On a scale from 1-10, the complexity of this service is 8. This service works in a couple of steps:
1. Fetches track metadata from Spotify API.
2. Analyzes the "energy" of the track with help of Spotify API.
3. Labels the track with an appropriate workout intensity.
4. Fetches exercise that matches the intensity from API Ninjas.
5. Merges all data, saves the playlist to a database, and returns the result to users.
