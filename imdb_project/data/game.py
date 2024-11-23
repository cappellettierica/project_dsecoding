import numpy as np
import random
from data import DataHandler
from quiz import questions  
from scoring import Scoring
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML


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
        self.feedback = []  # To store feedback for each question

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

    def display_welcome_message(self):
        welcome_message = widgets.HTML(
            value="""
            <div style='font-family: Arial, sans-serif; line-height: 1.6;'>
                <h2><b>Welcome to the IMDb Movie Quiz Game 🎬!</b></h2>
                <p>In this game, you’ll answer 9 questions about movies. The questions can be easy, medium, or hard, depending on the movie's popularity 😎.</p>
                <ul>
                    <li><b>3 Easy Questions</b> 🙂: Earn <b>5 points</b> for each correct answer!</li>
                    <li><b>3 Medium Questions</b> 😐: Earn <b>10 points</b> for each correct answer!</li>
                    <li><b>3 Hard Questions</b> 🙁: Earn <b>15 points</b> for each correct answer!</li>
                </ul>
                <p>If you answer incorrectly, you’ll score <b>0 points</b> ❌.</p>
                <p>At the end of the game, a graph will display your performance across the difficulty levels. Good luck! 🎉</p>
            </div>
            """
        )
        display(welcome_message)

    def display_question(self, question, question_idx):
        # Create a label to display the question above the dropdown
        question_label = widgets.HTML(value=f"<b style='color:#4CAF50;'>Q{question_idx + 1}: {question['question']}</b>")

        # Create a dropdown for selecting answers
        options_dropdown = widgets.Dropdown(
            options=[(f"{i+1}. {option}", i) for i, option in enumerate(question['options'])],
            description="Your Answer:",
            disabled=False,
        )

        return question_label, options_dropdown

    def play(self):
        self.display_welcome_message()  # Display the welcome message
        self.answer_widgets = []  # Store widgets for each question's answer
        display_questions = []  # Store the question widgets

        # Display all questions and collect answers
        for idx, question in enumerate(self.selected_questions):
            question_label, question_widget = self.display_question(question, idx)
            display_questions.append(question_label)  # Add question label to display list
            display_questions.append(question_widget)  # Display the dropdown widget
            self.answer_widgets.append(question_widget)  # Keep track of answers

        # Create the submit button to submit all answers at once
        submit_button = widgets.Button(description="⭐SUBMIT⭐", button_style='success')
        submit_button.on_click(self.submit_answers)  # Link button click to submit method
        display(*display_questions)  # Display each question and widget
        display(submit_button)

    def submit_answers(self, button):
        clear_output(wait=True)
        self.score = 0
        self.feedback = []

        # Initialize cumulative scores
        if not self.easy_scores:
            self.easy_scores.append(0)
        if not self.medium_scores:
            self.medium_scores.append(0)
        if not self.hard_scores:
            self.hard_scores.append(0)

        # Collect answers and generate feedback
        for idx, question in enumerate(self.selected_questions):
            selected_answer_idx = self.answer_widgets[idx].value
            correct = self.check_answer(selected_answer_idx, question['correct_answer_index'])
            score = self.calculate_score(question) if correct else 0
            self.score += score

            # Update cumulative scores
            if question['difficulty'] == 'easy':
                self.easy_scores.append(self.easy_scores[-1] + score)
            elif question['difficulty'] == 'medium':
                self.medium_scores.append(self.medium_scores[-1] + score)
            elif question['difficulty'] == 'hard':
                self.hard_scores.append(self.hard_scores[-1] + score)

            # Generate feedback for this question with emojis and difficulty
            result = f"<span style='color:green; font-weight:bold;'>You were correct! 😊</span>" if correct else f"<span style='color:red; font-weight:bold;'>You were wrong 😢</span>"
            self.feedback.append({
                "question": question["question"],
                "your_answer": question['options'][selected_answer_idx] if selected_answer_idx is not None else "No Answer",
                "correct_answer": question['options'][question['correct_answer_index']],
                "result": result,
                "score": score,
                "difficulty": question['difficulty']  # Storing the difficulty level
            })

        display(HTML(f"<b style='font-size:20px; color:#4CAF50;'>Your final score is: {self.score}/90</b>"))

        # Display detailed feedback
        self.display_feedback()

        # Display cumulative score breakdown
        scoring = Scoring(self.easy_scores, self.medium_scores, self.hard_scores)
        scoring.plot_scores()

        # Show replay or quit options
        self.show_replay_options()

    def show_replay_options(self):
        # Display buttons to let the player decide to play again or quit
        replay_button = widgets.Button(description="▶️Play Again▶️", button_style='info')
        quit_button = widgets.Button(description="⏹️Quit⏹️", button_style='danger')
        # set button callbacks
        replay_button.on_click(self.replay_game)
        quit_button.on_click(self.quit_game)
        button_box = widgets.HBox([replay_button, quit_button])
        display(button_box)

    def replay_game(self, button):
        # to reset the game and play again
        clear_output(wait=True)
        self.score = 0
        self.easy_scores = []
        self.medium_scores = []
        self.hard_scores = []
        self.selected_questions = self.select_questions_by_difficulty()
        self.user_answers = []
        self.feedback = []
        self.play()

    def quit_game(self, button):
        # thank-you message and end the game
        clear_output(wait=True)
        display(HTML("<h2 style='color:#4CAF50;'>Thank you for playing the IMDb Quiz Game!🍿</h2>"))

    def display_feedback(self):
        feedback_html = ""
        for idx, item in enumerate(self.feedback):
            feedback_html += f"""
            <div style='padding: 10px; border: 2px solid #ccc; margin: 5px;'>
                <b style='color:#3b5998;'>Q{idx + 1}: {item['question']}</b><br>
                <p style='color:#ADD8E6;'>This question was {item['difficulty'].capitalize()}</p>  <!-- Displaying difficulty level -->
                <b>Your Answer:</b> {item['your_answer']}<br>
                <b>Correct Answer:</b> {item['correct_answer']}<br>
                <b>Result:</b> {item['result']}<br>
                <b>Score:</b> {item['score']} points
            </div>
            """
        display(HTML(feedback_html))

    def check_answer(self, answer, correct_index):
        return int(answer) == correct_index

    def calculate_score(self, question):
        base_score = 10  # Base score for medium difficulty
        difficulty_multiplier = {"easy": 0.5, "medium": 1, "hard": 1.5}  # Score multipliers
        return int(base_score * difficulty_multiplier[question["difficulty"]])
