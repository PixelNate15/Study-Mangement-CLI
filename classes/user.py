from .subject import Subject
from .revision_log import RevisionLog
from datetime import date

class User:
    def __init__(self, name, userID=None): #Initiates class
        self.name = name
        self.userID = userID
        self.subjects = []
        self.schedules = []
        self.revisionLogs = []

    def __str__(self):
        return f"{self.name} (ID: {self.userID})"
        
    def addSubject(self, subjectName, examBoard): #Adds a subject object to the subjects list and creates a subject object
        for subject in self.subjects:
            if subjectName == subject.name:
                print(f"You are already taking {subjectName}")
                return None
        subject = Subject(subjectName, examBoard)
        self.subjects.append(subject)
        print("Subject added")
        return subject
    
    def removeSubject(self, subjectName): #Removes a subject object from the subjects list
        for subject in self.subjects:
            if subject.name == subjectName:
                self.subjects.remove(subject)
                print("Subject removed")
                return
        print(f"You don't take {subjectName}")
    
    def getSubject(self, subjectName): #Gets a subject object from the subjects list, can return no subject
        for subject in self.subjects:
            if subject.name == subjectName:
                return subject
        return None
    
    def logRevision(self, topicName, subjectName, duration, notes, when = None): #Creates a log object which is then appended to the revisionLogs list
        when = when or date.today()
        log = RevisionLog(when, topicName, subjectName, duration, notes)
        self.revisionLogs.append(log)
        return log
    
    def totalRevisionTime(self): #Calculates the total revision time done by the user
        total = 0
        for log in self.revisionLogs:
            total += log.duration
        return total
