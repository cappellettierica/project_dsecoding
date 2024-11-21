import numpy as np
import random
from data import DataHandler
from retrieval import RandomRetrieval
from quiz import questions  # Importing the list of predefined questions
from scoring import Scoring
import ipywidgets as widgets
from IPython.display import display, clear_output


class Quiz_Game:
    def __init__(self, num_questions=9):
        self.num_questions = num_questions
        self.data_handler = DataHandler()
        self.data = self.data_handler.load_data()
        self.questions = questions  # Assuming 'questions' is a predefined list
        if len(self.questions) < num_questions:
            print(f"Warning: Only {len(self.questions)} questions available.")
            self.num_questions = len(self.questions)
        self.score = 0
        self.easy_scores = []  # Cumulative scores for easy questions
        self.medium_scores = []  # Cumulative scores for medium questions
        self.hard_scores = []  # Cumulative scores for hard questions
        self.selected_questions = self.select_questions_by_difficulty()
        self.user_answers = []  # Store answers for all questions

    def select_questions_by_difficulty(self):
        easy_questions = [q for q in self.questions if q['difficulty'] == "easy"]
        medium_questions = [q for q in self.questions if q['difficulty'] == "medium"]
        hard_questions = [q for q in self.questions if q['difficulty'] == "hard"]

        num_per_difficulty = self.num_questions // 3
        extra = self.num_questions % 3
        selected_easy = random.sample(
            easy_questions, min(len(easy_questions), num_per_difficulty + (1 if extra > 0 else 0))
        )
        selected_medium = random.sample(
            medium_questions, min(len(medium_questions), num_per_difficulty + (1 if extra > 1 else 0))
        )
        selected_hard = random.sample(hard_questions, min(len(hard_questions), num_per_difficulty))
        selected_questions = selected_easy + selected_medium + selected_hard
        random.shuffle(selected_questions)
        return selected_questions

    def display_question(self, question, question_idx):
        # Create a label to display the question above the dropdown
        question_label = widgets.HTML(value=f"<b>Q{question_idx + 1}: {question['question']}</b>")

        # Create a dropdown for selecting answers
        options_dropdown = widgets.Dropdown(
            options=[(f"{i+1}. {option}", i) for i, option in enumerate(question['options'])],
            description="Your Answer:",
            disabled=False,
        )

        return question_label, options_dropdown

    def play(self):
        self.answer_widgets = []  # Store widgets for each question's answer
        display_questions = []  # Store the question widgets

        # Display all questions and collect answers
        for idx, question in enumerate(self.selected_questions):
            question_label, question_widget = self.display_question(question, idx)
            display_questions.append(question_label)  # Add question label to display list
            display_questions.append(question_widget)  # Display the dropdown widget
            self.answer_widgets.append(question_widget)  # Keep track of answers

        # Create the submit button to submit all answers at once
        submit_button = widgets.Button(description="⭐SUBMIT⭐")
        submit_button.on_click(self.submit_answers)  # Link button click to submit method
        display(*display_questions)  # Display each question and widget
        display(submit_button)

    def submit_answers(self, button):
        clear_output(wait=True)
        self.score = 0

        # Initialize cumulative scores if empty
        if not self.easy_scores:
            self.easy_scores.append(0)
        if not self.medium_scores:
            self.medium_scores.append(0)
        if not self.hard_scores:
            self.hard_scores.append(0)

        # Collect all answers
        for idx, question in enumerate(self.selected_questions):
            selected_answer_idx = self.answer_widgets[idx].value
            if self.check_answer(selected_answer_idx, question['correct_answer_index']):
                score = self.calculate_score(question)
                self.score += score

                # Update cumulative scores
                if question['difficulty'] == 'easy':
                    self.easy_scores.append(self.easy_scores[-1] + score)
                elif question['difficulty'] == 'medium':
                    self.medium_scores.append(self.medium_scores[-1] + score)
                elif question['difficulty'] == 'hard':
                    self.hard_scores.append(self.hard_scores[-1] + score)

        print(f"Your final score is: {self.score}")

        # Display cumulative score breakdown
        scoring = Scoring(self.easy_scores, self.medium_scores, self.hard_scores)
        scoring.plot_scores()

    def check_answer(self, answer, correct_index):
        return int(answer) == correct_index

    def calculate_score(self, question):
        base_score = 10  # Base score for medium difficulty
        difficulty_multiplier = {"easy": 0.5, "medium": 1, "hard": 1.5}  # Score multipliers
        return int(base_score * difficulty_multiplier[question['difficulty']])



