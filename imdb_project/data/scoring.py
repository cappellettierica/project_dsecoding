import matplotlib.pyplot as plt

class Scoring:
    def __init__(self, easy_scores, medium_scores, hard_scores):
        self.easy_scores = easy_scores
        self.medium_scores = medium_scores
        self.hard_scores = hard_scores

    def plot_scores(self):
        plt.figure(figsize=(6, 3))
        
        # Plot easy scores
        if self.easy_scores:
            plt.plot(self.easy_scores, label='Easy Scores', linestyle='-', marker='x')
        
        # Plot medium scores
        if self.medium_scores:
            plt.plot(self.medium_scores, label='Medium Scores', linestyle='-', marker='s')
        
        # Plot hard scores
        if self.hard_scores:
            plt.plot(self.hard_scores, label='Hard Scores', linestyle='-', marker='^')
        
        plt.title('Score Breakdown', fontsize=16)
        plt.xlabel('Game', fontsize=14)
        plt.ylabel('Score', fontsize=14)
        plt.grid(True)
        
        # Check if there are any labels to include in the legend
        handles, labels = plt.gca().get_legend_handles_labels()
        if labels:
            plt.legend(fontsize=12)
        
        plt.show()





