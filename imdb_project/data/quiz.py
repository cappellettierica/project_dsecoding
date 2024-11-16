import numpy as np
from data import DataHandler
from retrieval import RandomRetrieval

class QuizGame:
    def __init__(self, n_options=4, difficulty='medium', random_state=None):
        # initialize data handler to load the movie dataset
        self.data_handler = DataHandler()
        self.data = self.data_handler.get_data()
        # initialize retriever for random options in the quiz
        self.retriever = RandomRetrieval(n=n_options - 1, random_state=random_state)
        self.n_options = n_options
        self.difficulty = difficulty
        self.random_state = random_state
        self.question_pool = self.create_question_pool()

    def generate_release_year_question(self, used_indices):
        filtered_data = self.data  #Ffilter out previously used movies to avoid repetition
        available_data = filtered_data[~filtered_data.index.isin(used_indices)]
        if available_data.empty: # rise error if no data is left to generate unique questions
            raise ValueError("No more data available to generate unique questions.")
        
        # randomly select a movie for the question, and then marks it as used
        correct_movie = available_data.sample(1, random_state=self.random_state).iloc[0]
        used_indices.add(correct_movie.name)

        question = f"In which year was the movie '{correct_movie['Series_Title']}' released?"
        # unique answers
        unique_years = list(set(available_data['Released_Year']) - {correct_movie['Released_Year']})
        while len(unique_years) < self.n_options-1:
            additional_years = available_data['Released_Year'].sample(self.n_options - 1 - len(unique_years), random_state=self.random_state).tolist()
            unique_years = list(set(unique_years + additional_years))
        options = np.random.choice(unique_years, self.n_options - 1, replace=False).tolist()
        options.append(correct_movie['Released_Year']) # add correct answers
        options = list(set(options))  # Removes any duplicates
        np.random.shuffle(options) # Shuffle option
        #format the options for display
        formatted_options = [f"{idx + 1}. {opt}" for idx, opt in enumerate(options)]
        correct_answer_index =options.index(correct_movie['Released_Year'])
         
        return question, formatted_options, correct_answer_index, correct_movie.name 

    def generate_director_question(self, used_indices):
        filtered_data = self.data
        available_data = filtered_data[~filtered_data.index.isin(used_indices)]
        if available_data.empty:
            raise ValueError("No more data available to generate unique questions.")

        correct_movie = available_data.sample(1, random_state=self.random_state).iloc[0]
        used_indices.add(correct_movie.name)

        question = f"Who directed the movie '{correct_movie['Series_Title']}'?"
        # uniqueness
        directors = [correct_movie['Director']] + list(available_data['Director'].unique())
        while len(directors) < self.n_options:
            directors.append(np.random.choice(directors))
        options = list(np.random.choice(directors, self.n_options - 1, replace=False)) + [correct_movie['Director']]
        np.random.shuffle(options)

        correct_answer_index = options.index(correct_movie['Director'])
        formatted_options = [f"{idx + 1}. {opt}" for idx, opt in enumerate(options)]
    

        return question, formatted_options, correct_answer_index, correct_movie.name 

    def generate_genre_question(self, used_indices):
        filtered_data = self.data
        available_data = filtered_data[~filtered_data.index.isin(used_indices)]
        if available_data.empty:
            raise ValueError("No more data available to generate unique questions.")

        correct_movie = available_data.sample(1, random_state=self.random_state).iloc[0]
        used_indices.add(correct_movie.name)

        question = f"What is the genre of the movie '{correct_movie['Series_Title']}'?"
        # generate list of possible genres for the options
        genres = [correct_movie['Genre']] + list(available_data['Genre'].unique())
        while len(genres) < self.n_options: # Add random genres to fill options
            genres.append(np.random.choice(genres))
        options = list(np.random.choice(genres, self.n_options - 1, replace=False)) + [correct_movie['Genre']]
        np.random.shuffle(options)

        correct_answer_index = options.index(correct_movie['Genre'])
        formatted_options = [f"{idx + 1}. {opt}" for idx, opt in enumerate(options)]
        
        

        return question, formatted_options, correct_answer_index, correct_movie.name

    def generate_rating_question(self, used_indices):
        filtered_data = self.data
        available_data = filtered_data[~filtered_data.index.isin(used_indices)]
        if available_data.empty:
            raise ValueError("No more data available to generate unique questions.")

        correct_movie = available_data.sample(1, random_state=self.random_state).iloc[0]
        used_indices.add(correct_movie.name)

        question = f"What is the IMDb rating of the movie '{correct_movie['Series_Title']}'?"
    
        # Get unique ratings for the incorrect options
        unique_ratings = available_data['IMDB_Rating'].unique()
        while len(unique_ratings) < self.n_options:
            unique_ratings = np.append(unique_ratings, np.random.choice(unique_ratings))
        options = list(np.random.choice(unique_ratings, self.n_options - 1, replace=False)) + [correct_movie['IMDB_Rating']]
        options = list(set(options))  
        np.random.shuffle(options)  
        formatted_options = [f"{idx + 1}. {opt}" for idx, opt in enumerate(options)]
        correct_answer_index = options.index(correct_movie['IMDB_Rating'])

        return question, formatted_options, correct_answer_index, correct_movie.name

    
    def create_question_pool(self):
        """Generate a balanced pool of 20 unique questions with specific difficulty distribution based on No_of_Votes."""
        np.random.seed(self.random_state)
        questions = []
        used_indices = set()  # Track used data indices to avoid repetition

        # Get the percentiles for No_of_Votes to determine the difficulty categories
        lower_quartile = np.percentile(self.data['No_of_Votes'], 25) 
        upper_quartile = np.percentile(self.data['No_of_Votes'], 75)  

        difficulty_counts = {'hard': 16, 'medium': 20, 'easy': 16}  
        difficulty_count = {'hard': 0, 'medium': 0, 'easy': 0}

        # Predefine the number of questions per type (question types: release_year, director, genre, rating)
        question_types = ["release_year", "director", "genre", "rating"]
        type_counts = {q_type: 13 for q_type in question_types}  

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

        np.random.shuffle(questions)  # Shuffle the final set of questionsto mix the question types and difficulties
        return questions


    def get_random_question(self):
        """Retrieve a random question from the pool."""
        question_info = np.random.choice(self.question_pool)
        return question_info["question"], question_info["options"], question_info["correct_answer_index"], question_info["difficulty"]

# initialise the QuizGame instance
quiz_game = QuizGame(random_state=42)
questions = quiz_game.question_pool
