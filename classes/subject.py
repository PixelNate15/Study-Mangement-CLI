from .topic import Topic


class Subject:
    def __init__(self, name, examBoard): #Initiates class
        self.name = name
        self.examBoard = examBoard
        self.topics = []

    def __str__(self):
        return f"{self.name} ({self.examBoard})"
        
    def addTopic(self, topicName, difficulty, estimatedHours, isCompleted): #Adds a topic object to the topics list
        for topic in self.topics:
            if topicName == topic.name:
                print(f"{topicName} already exists")
                return None
        topic = Topic(topicName, self, difficulty, estimatedHours, isCompleted)
        self.topics.append(topic)
        print("Topic added")
        return topic
    
    def removeTopic(self, topicName): #Removes a topic object to the topics list
        for topic in self.topics:
            if topic.name == topicName:
                self.topics.remove(topic)
                print("Topic removed")
                return
        print(f"You don't take {topicName}")
        
    def getTopic(self, topicName):  #Gets a topic object to the topics list
        for topic in self.topics:
            if topic.name == topicName:
                return topic
        return None
        
    def countCompletedTopics(self): #Counts the amount of completed topics
        total = sum(topic.isCompleted for topic in self.topics)
        print(f"The total amount of completed topics is {total}")
        return total
