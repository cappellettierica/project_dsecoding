import numpy as np
import random
from data import DataHandler
from retrieval import RandomRetrieval
from quiz import questions  # Importing the list of predefined questions
from scoring import Scoring


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
        # self.scores_by_difficulty = {"easy": [], "medium": [], "hard": []}  
        self.easy_scores = []  # easy questions' scores
        self.medium_scores = []  # for medium questions' scores
        self.hard_scores = []  # hard questions' scores
        self.total_scores = []  # to track total scores of all games

    def play(self):
        for i in range(self.num_questions):
            question = random.choice(self.questions)
            self.questions.remove(question)  # Avoid repeating questions
            print(f"\nQuestion {i+1} - {question['difficulty'].capitalize()}: {question['question']}")  # Added difficulty
            for idx, option in enumerate(question['options']):
                print(f"{idx + 1}. {option}")

            answer = input("Enter the number of your answer: ")
            if self.check_answer(answer, question['correct_answer_index']):
                question_score = self.calculate_score(question)
                if self.check_answer(answer, question['correct_answer_index']):
                    self.score += question_score  # Add to the total score
                if question['difficulty'] == "easy":
                    self.easy_scores.append(self.easy_scores[-1] + question_score if self.easy_scores else question_score)
                elif question['difficulty'] == "medium":
                    self.medium_scores.append(self.medium_scores[-1] + question_score if self.medium_scores else question_score)
                elif question['difficulty'] == "hard":
                    self.hard_scores.append(self.hard_scores[-1] + question_score if self.hard_scores else question_score)

                self.total_scores.append(self.total_scores[-1] + question_score if self.total_scores else question_score)

                print("Correct!\n")
            else:
                if question['difficulty'] == "easy":
                    self.easy_scores.append(self.easy_scores[-1] if self.easy_scores else 0)
                elif question['difficulty'] == "medium":
                    self.medium_scores.append(self.medium_scores[-1] if self.medium_scores else 0)
                elif question['difficulty'] == "hard":
                    self.hard_scores.append(self.hard_scores[-1] if self.hard_scores else 0)

                self.total_scores.append(self.total_scores[-1] if self.total_scores else 0)

                print(f"Incorrect. The correct answer was: {question['options'][question['correct_answer_index']]}\n")
        
        self.total_scores.append(self.score)
        print(f"Your final score is: {self.score}")

        scoring = Scoring(self.total_scores, self.easy_scores, self.medium_scores, self.hard_scores)
        scoring.plot_scores()

    def check_answer(self, answer, correct_index):
        try:
            return int(answer) - 1 == correct_index
        except ValueError:
            return False

    def calculate_score(self, question):
        base_score = 10  # Base score for medium difficulty
        difficulty_multiplier = {"easy": 0.5, "medium": 1, "hard": 1.5}  # Score multipliers
        
        # Adjust score based on difficulty
        return int(base_score * difficulty_multiplier[question['difficulty']])
    
if __name__ == "__main__":
    game = QuizGame(num_questions=10)
    game.play()
