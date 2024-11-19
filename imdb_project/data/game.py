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
        self.questions = questions
        if len(self.questions) < num_questions:
            print(f"Warning: Only {len(self.questions)} questions available.")
            self.num_questions = len(self.questions)
        self.score = 0  
        self.easy_scores = []  # easy questions' scores
        self.medium_scores = []  # for medium questions' scores
        self.hard_scores = []  # hard questions' scores
        self.total_scores = []  # to track total scores of all games
        self.selected_questions = self.select_questions_by_difficulty()

    def select_questions_by_difficulty(self): #divide questions into groups by difficulty
        easy_questions = [q for q in self.questions if q['difficulty'] == "easy"]
        medium_questions = [q for q in self.questions if q['difficulty'] == "medium"]
        hard_questions = [q for q in self.questions if q['difficulty'] == "hard"]

        num_per_difficulty = self.num_questions // 3 # Calculate the number of questions for each difficulty
        extra = self.num_questions % 3  # for where num_questions is not divisible by 3
        # randomly sample questions for each difficulty
        selected_easy = random.sample(easy_questions, min(len(easy_questions), num_per_difficulty + (1 if extra > 0 else 0)))
        selected_medium = random.sample(medium_questions, min(len(medium_questions), num_per_difficulty + (1 if extra > 1 else 0)))
        selected_hard = random.sample(hard_questions, min(len(hard_questions), num_per_difficulty))
        # Combine the selected questions and shuffle them
        selected_questions = selected_easy + selected_medium + selected_hard
        random.shuffle(selected_questions)
        return selected_questions

    def play(self):
        for i in range(self.num_questions):
            question = self.selected_questions[i]
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
                    # to plot every question on the graph, cumulative. i add every score to the right list based on difficulty
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
    game = QuizGame(num_questions=9)
    game.play()
