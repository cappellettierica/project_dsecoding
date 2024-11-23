import matplotlib.pyplot as plt

class Percentage:
    def __init__(self, easy_scores, medium_scores, hard_scores):
        self.easy_scores = easy_scores
        self.medium_scores = medium_scores
        self.hard_scores = hard_scores

    def plot_percentage_contribution(self):
        # Calculate the total score
        total_score = sum([self.easy_scores[-1], self.medium_scores[-1], self.hard_scores[-1]])

        # Calculate percentage contributions
        easy_percentage = (self.easy_scores[-1] / total_score) * 100 if total_score > 0 else 0
        medium_percentage = (self.medium_scores[-1] / total_score) * 100 if total_score > 0 else 0
        hard_percentage = (self.hard_scores[-1] / total_score) * 100 if total_score > 0 else 0
        
        # Plotting the bar chart for percentage contribution
        categories = ['Easy', 'Medium', 'Hard']
        percentages = [easy_percentage, medium_percentage, hard_percentage]

        plt.figure(figsize=(8, 6))
        plt.bar(categories, percentages, color=['#448cc4', '#ff842c', '#3ca43c'])
        
        # Add labels and title
        plt.title('Percentage Contribution to Total Score', fontsize=14)
        plt.ylabel('Percentage (%)', fontsize=10)
        plt.ylim(0, 120)  # Y-axis limits from 0 to 100%
        
        # Display the percentage on top of each bar
        for i, v in enumerate(percentages):
            plt.text(i, v + 2, f'{v:.1f}%', ha='center', fontsize=12, color='black')
        
        plt.show()  



