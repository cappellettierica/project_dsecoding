import numpy as np
from data import DataHandler
from retrieval import RandomRetrieval

class QuizGame:
    def __init__(self, n_options=4, difficulty='medium', random_state=None):
        self.data_handler = DataHandler()
        self.data = self.data_handler.get_data()
        self.retriever = RandomRetrieval(n=n_options - 1, random_state=random_state)
        self.n_options = n_options
        self.difficulty = difficulty
        self.random_state = random_state
        self.question_pool = self.create_question_pool()

    def generate_release_year_question(self, used_indices):
        filtered_data = self.data
        available_data = filtered_data[~filtered_data.index.isin(used_indices)]
        if available_data.empty:
            raise ValueError("No more data available to generate unique questions.")
        
        correct_movie = available_data.sample(1, random_state=self.random_state).iloc[0]
        used_indices.add(correct_movie.name)

        question = f"In which year was the movie '{correct_movie['Series_Title']}' released?"
        incorrect_movies = self.retriever.predict(available_data)
        options = [{'Series_Title': correct_movie['Series_Title'], 'Released_Year': correct_movie['Released_Year']}]
        options += [{'Series_Title': movie['Series_Title'], 'Released_Year': movie['Released_Year']} for movie in incorrect_movies[0].to_dict(orient='records')]
        np.random.shuffle(options)

        formatted_options = [f"{idx + 1}. {opt['Released_Year']} - {opt['Series_Title']}" for idx, opt in enumerate(options)]
        correct_answer_index = next(i + 1 for i, opt in enumerate(options) if opt['Series_Title'] == correct_movie['Series_Title'])
        #difficulty = self.difficulty

        return question, formatted_options, correct_answer_index, correct_movie.name #, difficulty

    def generate_director_question(self, used_indices):
        filtered_data = self.data
        available_data = filtered_data[~filtered_data.index.isin(used_indices)]
        if available_data.empty:
            raise ValueError("No more data available to generate unique questions.")

        correct_movie = available_data.sample(1, random_state=self.random_state).iloc[0]
        used_indices.add(correct_movie.name)

        question = f"Who directed the movie '{correct_movie['Series_Title']}'?"
        incorrect_movies = self.retriever.predict(available_data)
        options = [correct_movie['Director']] + [movie['Director'] for movie in incorrect_movies[0].to_dict(orient='records')]
        np.random.shuffle(options)

        formatted_options = [f"{idx + 1}. {opt}" for idx, opt in enumerate(options)]
        correct_answer_index = options.index(correct_movie['Director']) + 1
        #difficulty = self.difficulty

        return question, formatted_options, correct_answer_index, correct_movie.name #, difficulty

    def generate_genre_question(self, used_indices):
        filtered_data = self.data
        available_data = filtered_data[~filtered_data.index.isin(used_indices)]
        if available_data.empty:
            raise ValueError("No more data available to generate unique questions.")

        correct_movie = available_data.sample(1, random_state=self.random_state).iloc[0]
        used_indices.add(correct_movie.name)

        question = f"What is the genre of the movie '{correct_movie['Series_Title']}'?"
        incorrect_movies = self.retriever.predict(available_data)
        options = [correct_movie['Genre']] + [movie['Genre'] for movie in incorrect_movies[0].to_dict(orient='records')]
        np.random.shuffle(options)

        formatted_options = [f"{idx + 1}. {opt}" for idx, opt in enumerate(options)]
        correct_answer_index = options.index(correct_movie['Genre']) + 1
        #difficulty = self.difficulty

        return question, formatted_options, correct_answer_index, correct_movie.name #, difficulty

    def generate_rating_question(self, used_indices):
        filtered_data = self.data
        available_data = filtered_data[~filtered_data.index.isin(used_indices)]
        if available_data.empty:
            raise ValueError("No more data available to generate unique questions.")

        correct_movie = available_data.sample(1, random_state=self.random_state).iloc[0]
        used_indices.add(correct_movie.name)

        question = f"What is the IMDb rating of the movie '{correct_movie['Series_Title']}'?"
        incorrect_movies = self.retriever.predict(available_data)
        options = [correct_movie['IMDB_Rating']] + [movie['IMDB_Rating'] for movie in incorrect_movies[0].to_dict(orient='records')]
        options = sorted(set(options), reverse=True)[:self.n_options]
        np.random.shuffle(options)

        formatted_options = [f"{idx + 1}. {opt}" for idx, opt in enumerate(options)]
        correct_answer_index = options.index(correct_movie['IMDB_Rating']) + 1
        #difficulty = self.difficulty

        return question, formatted_options, correct_answer_index, correct_movie.name #, difficulty
    
    def create_question_pool(self):
        """Generate a balanced pool of 20 unique questions with specific difficulty distribution based on No_of_Votes."""
        np.random.seed(self.random_state)
        questions = []
        used_indices = set()  # Track used data indices to avoid repetition

        # Get the percentiles for No_of_Votes to determine the difficulty categories
        lower_quartile = np.percentile(self.data['No_of_Votes'], 25)  # 25th percentile
        upper_quartile = np.percentile(self.data['No_of_Votes'], 75)  # 75th percentile

        # Predefine the number of questions per difficulty
        difficulty_counts = {'hard': 16, 'medium': 20, 'easy': 16}  # Total 50 questions

        # Track how many questions we have for each difficulty
        difficulty_count = {'hard': 0, 'medium': 0, 'easy': 0}

        # Predefine the number of questions per type (question types: release_year, director, genre, rating)
        question_types = ["release_year", "director", "genre", "rating"]
        type_counts = {q_type: 13 for q_type in question_types}  # 5 questions of each type

        while sum(difficulty_count.values()) < 50:  # Keep generating until we have 50 questions
            for question_type, count in type_counts.items():
                if sum(difficulty_count.values()) >= 50:
                    break  # Stop if we already have 50 questions
                
                # Generate the question based on the question type
                if question_type == "release_year":
                    question, options, correct_answer_index, index = self.generate_release_year_question(used_indices)
                elif question_type == "director":
                    question, options, correct_answer_index, index = self.generate_director_question(used_indices)
                elif question_type == "genre":
                    question, options, correct_answer_index, index = self.generate_genre_question(used_indices)
                elif question_type == "rating":
                    question, options, correct_answer_index, index = self.generate_rating_question(used_indices)

                # Get the No_of_Votes for the movie
                no_of_votes = self.data.loc[index, 'No_of_Votes']

                # Determine the difficulty based on the percentiles
                if no_of_votes < lower_quartile:
                    difficulty = 'hard'
                elif no_of_votes > upper_quartile:
                    difficulty = 'easy'
                else:
                    difficulty = 'medium'

                # Only add the question if we haven't reached the max count for that difficulty
                if difficulty_count[difficulty] < difficulty_counts[difficulty]:
                    questions.append({
                        "question": question,
                        "options": options,
                        "correct_answer_index": correct_answer_index,
                        "difficulty": difficulty
                    })
                    difficulty_count[difficulty] += 1  # Increment the count for this difficulty

        np.random.shuffle(questions)  # Shuffle to mix the question types and difficulties
        return questions


    def get_random_question(self):
        """Retrieve a random question from the pool."""
        question_info = np.random.choice(self.question_pool)
        return question_info["question"], question_info["options"], question_info["correct_answer_index"], question_info["difficulty"]

# initialise the QuizGame instance
quiz_game = QuizGame(random_state=42)
questions = quiz_game.question_pool
