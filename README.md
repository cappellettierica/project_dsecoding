# project_dsecoding

## IMDb Movie Quiz

This quiz tests the player's knowledge of movies based on various attributes such as release year, director, genre, and stars.

### Question Types

The quiz generates different types of questions based on various movie attributes:

- **Release Year**: In which year was the movie released?
- **Director**: Who directed the movie?
- **Genre**: What is the genre of the movie?
- **Stars**: Which actors starred in the movie?

### Difficulty Levels

The difficulty of each question is dynamically determined based on the number of votes a movie has on IMD; a level is assigned based on where the movie's number of votes falls within the overall dataset. The dataset is divided into three categories using percentiles:

- **Hard**: Movies in the **lower 25%** of the number of votes are classified as difficult.
- **Medium**: Movies in the **middle 50%** are considered of medium difficulty.
- **Easy**: Movies in the **upper 25%** of the number of votes are classified as easy.

In the Quiz, players will answer 3 questions for each difficulty level; the difficulty of the question will be revealed to the player after they submit the answers.
The scoring will depend on the difficulty leveel of each question

### Scoring System

Each question's score is based on its difficulty level:

- **Easy**: 5 points
- **Medium**: 10 points
- **Hard**: 15 points

The total score is the sum of the points for all correctly answered questions. Incorrect answers will not deduct points.
