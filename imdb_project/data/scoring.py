import matplotlib.pyplot as plt

class Scoring:
    def __init__(self, total_scores, easy_scores, medium_scores, hard_scores):
        self.total_scores = total_scores
        self.easy_scores = easy_scores
        self.medium_scores = medium_scores
        self.hard_scores = hard_scores

    def plot_scores(self):
        # Plot Easy Scores
        plt.figure(figsize=(10, 6))
        if self.easy_scores:
            plt.plot(range(1, len(self.easy_scores) + 1), self.easy_scores, marker='o', color='blue', linestyle='-', zorder=5)
        plt.title('Easy Question Cumulative Scores')
        plt.xlabel('Question Number')
        plt.ylabel('Cumulative Score')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('easy_scores.png')  # Save the Easy graph
        plt.close()

        # Plot Medium Scores
        plt.figure(figsize=(10, 6))
        if self.medium_scores:
            plt.plot(range(1, len(self.medium_scores) + 1), self.medium_scores, marker='o', color='orange', linestyle='-', zorder=5)
        plt.title('Medium Question Cumulative Scores')
        plt.xlabel('Question Number')
        plt.ylabel('Cumulative Score')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('medium_scores.png')  # Save the Medium graph
        plt.close()

        # Plot Hard Scores
        plt.figure(figsize=(10, 6))
        if self.hard_scores:
            plt.plot(range(1, len(self.hard_scores) + 1), self.hard_scores, marker='o', color='green', linestyle='-', zorder=5)
        plt.title('Hard Question Cumulative Scores')
        plt.xlabel('Question Number')
        plt.ylabel('Cumulative Score')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('hard_scores.png')  # Save the Hard graph
        plt.close()

        # Plot Total Scores
        plt.figure(figsize=(10, 6))
        if self.total_scores:
            plt.plot(range(1, len(self.total_scores) + 1), self.total_scores, marker='o', color='purple', linestyle='-', zorder=5)
        plt.title('Total Cumulative Scores')
        plt.xlabel('Question Number')
        plt.ylabel('Total Cumulative Score')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('total_scores.png')  # Save the Total graph
        plt.close()

        print("Graphs saved: 'easy_scores.png', 'medium_scores.png', 'hard_scores.png', 'total_scores.png'.")



