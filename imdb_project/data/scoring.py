import matplotlib.pyplot as plt

class Scoring:
    def __init__(self, easy_scores, medium_scores, hard_scores):
        self.easy_scores = easy_scores
        self.medium_scores = medium_scores
        self.hard_scores = hard_scores

    def plot_scores(self):
        plt.figure(figsize=(8, 4))
        
        if self.easy_scores:
            easy_score = self.easy_scores[-1]  # Last score in easy_scores list
            plt.plot(self.easy_scores, label=f'Easy Scores ({easy_score}/15)', linestyle='-', marker='x')
        
        if self.medium_scores:
            medium_score = self.medium_scores[-1]  # Last score in medium_scores list
            plt.plot(self.medium_scores, label=f'Medium Scores ({medium_score}/30)', linestyle='-', marker='s')
    
        if self.hard_scores:
            hard_score = self.hard_scores[-1]  # Last score in hard_scores list
            plt.plot(self.hard_scores, label=f'Hard Scores ({hard_score}/45)', linestyle='-', marker='^')
        
        plt.title('Score Breakdown', fontsize=14)
        plt.xlabel('Game', fontsize=10)
        plt.ylabel('Score', fontsize=10)
        plt.grid(True)
        
        handles, labels = plt.gca().get_legend_handles_labels()
        if labels:
            plt.legend(fontsize=12)
        
        plt.show()



