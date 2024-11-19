import matplotlib.pyplot as plt

class Scoring:
    def __init__(self, total_scores, easy_scores, medium_scores, hard_scores):
        # Initialise the Scoring class with the lists for cumulative scores.
        self.total_scores = total_scores
        self.easy_scores = [score * 2 for score in easy_scores]  # Multiply easy scores by 2
        self.medium_scores = medium_scores 
        self.hard_scores = [score / 1.5 for score in hard_scores]  # Divide hard scores by 1.5

    def plot_scores(self):
        plt.figure(figsize=(12, 8))  # Set the figure size

        # Plot the cumulative scores for each difficulty
        if self.easy_scores:
            plt.plot(range(1, len(self.easy_scores) + 1), self.easy_scores, 
                 marker='o', color='blue', linestyle='-', label='Easy', zorder=5)
        if self.medium_scores:
            plt.plot(range(1, len(self.medium_scores) + 1), self.medium_scores, 
                 marker='o', color='orange', linestyle='-', label='Medium', zorder=5)
        if self.hard_scores:
            plt.plot(range(1, len(self.hard_scores) + 1), self.hard_scores, 
                 marker='o', color='green', linestyle='-', label='Hard', zorder=5)
        plt.title('Cumulative Scores by Question Difficulty', fontsize=16)
        plt.xlabel('Question Number', fontsize=14)
        plt.ylabel('Cumulative Score', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12)
        #plt.tight_layout()
        plt.savefig('cumulative_scores.png')
        plt.close()

        plt.figure(figsize=(10, 6)) 
        if self.total_scores: 
            plt.plot(range(1, len(self.total_scores) + 1), self.total_scores, marker='o', color='purple', linestyle='-', zorder=5)
        plt.title('Total Cumulative Scores')  
        plt.xlabel('Question Number')  
        plt.ylabel('Total Cumulative Score')  
        plt.grid(True)  
        #plt.tight_layout()  
        plt.savefig('total_scores.png')  
        plt.close()  

    
        #print("Graphs saved: 'easy_scores.png', 'medium_scores.png', 'hard_scores.png', 'total_scores.png'.")




