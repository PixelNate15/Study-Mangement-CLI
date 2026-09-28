class Topic:
    def __init__(self, name, subject, difficulty, estimatedHours, isCompleted):
        self.name = name
        self.subject = subject
        self.difficulty = difficulty
        self.estimatedHours = estimatedHours
        self.isCompleted = isCompleted
        self.testScores = []

    def __str__(self):
        return f"{self.name} ({self.subject})"

    def markCompleted(self):
        self.isCompleted = True

    def addTestScore(self, score, dateOfTest=None):
        # The date is accepted because the CLI asks for it. Scores remain numeric
        # so they can be averaged and stay compatible with the GUI.
        self.testScores.append(score)
        return score

    def averageScore(self):
        if not self.testScores:
            print("No tests were taken so the average score is 0")
            return 0
        average = sum(self.testScores) / len(self.testScores)
        print(f"The average score on all the tests is {average}")
        return average
