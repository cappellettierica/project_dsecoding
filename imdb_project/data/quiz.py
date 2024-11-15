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

    def filter_data_by_difficulty(self):
        """Filter data based on difficulty level."""
        # Compute percentiles for vote counts
        lower_quartile = np.percentile(self.data['No_of_Votes'], 25)
        upper_quartile = np.percentile(self.data['No_of_Votes'], 75)

        # Apply filters based on difficulty level
        if self.difficulty == 'easy':
            return self.data[self.data['No_of_Votes'] >= upper_quartile]
        elif self.difficulty == 'hard':
            return self.data[self.data['No_of_Votes'] <= lower_quartile]
        else:  # Medium
            return self.data[
                (self.data['No_of_Votes'] > lower_quartile) &
                (self.data['No_of_Votes'] < upper_quartile)]

    def generate_release_year_question(self, used_indices):
        filtered_data = self.filter_data_by_difficulty()
        available_data = filtered_data[~filtered_data.index.isin(used_indices)]
        if available_data.empty:
            raise ValueError("No more data available to generate unique questions.")
        
        correct_movie = available_data.sample(1, random_state=self.random_state).iloc[0]
        used_indices.add(correct_movie.name)

        question = f"In which year was the movie '{correct_movie['Series_Title']}' released?"
        incorrect_movies = self.retriever.predict(available_data)
        options = [correct_movie] + incorrect_movies[0].to_dict(orient='records')
        np.random.shuffle(options)

        formatted_options = [f"{idx + 1}. {opt['Released_Year']} - {opt['Series_Title']}" for idx, opt in enumerate(options)]
        correct_answer_index = options.index(correct_movie) + 1
        difficulty = self.difficulty

        return question, formatted_options, correct_answer_index, difficulty

    def generate_director_question(self, used_indices):
        filtered_data = self.filter_data_by_difficulty()
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
        difficulty = self.difficulty

        return question, formatted_options, correct_answer_index, difficulty

    def generate_genre_question(self, used_indices):
        filtered_data = self.filter_data_by_difficulty()
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
        difficulty = self.difficulty

        return question, formatted_options, correct_answer_index, difficulty

    def generate_rating_question(self, used_indices):
        filtered_data = self.filter_data_by_difficulty()
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
        difficulty = self.difficulty

        return question, formatted_options, correct_answer_index, difficulty
    
    def create_question_pool(self):
        """Generate a balanced pool of 20 unique questions of various types."""
        np.random.seed(self.random_state)
        questions = []
        used_indices = set()  # Track used data indices to avoid repetition
    
        # Predefine the number of questions per type for balance
        question_types = ["release_year", "director", "genre", "rating"]
        type_counts = {q_type: 5 for q_type in question_types}  # 5 questions of each type

        for question_type, count in type_counts.items():
            for _ in range(count):
                if question_type == "release_year":
                    question, options, correct_answer_index, difficulty = self.generate_release_year_question(used_indices)
                elif question_type == "director":
                    question, options, correct_answer_index, difficulty = self.generate_director_question(used_indices)
                elif question_type == "genre":
                    question, options, correct_answer_index, difficulty = self.generate_genre_question(used_indices)
                elif question_type == "rating":
                    question, options, correct_answer_index, difficulty = self.generate_rating_question(used_indices)

                questions.append({
                    "question": question,
                    "options": options,
                    "correct_answer_index": correct_answer_index,
                    "difficulty": difficulty})
                
                #print(f"Total questions in pool: {len(questions)}") - used it to check if it was cresating questions correctly and it is 


        np.random.shuffle(questions)
        return questions

    def get_random_question(self):
        """Retrieve a random question from the pool."""
        question_info = np.random.choice(self.question_pool)
        return question_info["question"], question_info["options"], question_info["correct_answer_index"], question_info["difficulty"]

# Initialize the QuizGame instance
quiz_game = QuizGame(random_state=42)
questions = quiz_game.question_pool
