import numpy as np
import random
from data import DataHandler
from retrieval import RandomRetrieval
from quiz import questions  # Importing the list of predefined questions


class QuizGame:
    def __init__(self, num_questions=5):
        self.num_questions = num_questions
        self.data_handler = DataHandler()
        self.data = self.data_handler.load_data()

        # No need to filter by difficulty anymore, so use all questions
        self.questions = questions
        if len(self.questions) < num_questions:
            print(f"Warning: Only {len(self.questions)} questions available.")
            self.num_questions = len(self.questions)
        self.score = 0

    def play(self):
        """Play the quiz game."""
        for i in range(self.num_questions):
            question = random.choice(self.questions)
            self.questions.remove(question)  # Avoid repeating questions
            print(f"\nQuestion {i+1} - {question['difficulty'].capitalize()}: {question['question']}")  # Added difficulty
            for idx, option in enumerate(question['options']):
                print(f"{idx + 1}. {option}")

            answer = input("Enter the number of your answer: ")
            if self.check_answer(answer, question['correct_answer_index']):
                self.score += self.calculate_score(question)
                print("Correct!\n")
            else:
                print(f"Incorrect. The correct answer was: {question['options'][question['correct_answer_index']]}\n")

        print(f"Your final score is: {self.score}")

    def check_answer(self, answer, correct_index):
        """Check if the answer is correct."""
        try:
            return int(answer) - 1 == correct_index
        except ValueError:
            return False

    def calculate_score(self, question):
        """Calculate score based on the question's difficulty."""
        base_score = 10  # Base score for medium difficulty
        difficulty_multiplier = {"easy": 0.5, "medium": 1, "hard": 1.5}  # Score multipliers
        
        # Adjust score based on difficulty
        return int(base_score * difficulty_multiplier[question['difficulty']])

# Example of running the game
if __name__ == "__main__":
    game = QuizGame(num_questions=5)
    game.play()
