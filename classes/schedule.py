from datetime import datetime
import json

class Schedule: #Initiates class
    def __init__(self, user, dailyLimit, startDate, endDate):
        self.user = user
        self.dailyLimit = dailyLimit
        self.startDate = startDate
        self.endDate = endDate
        self.allocatedSessions = {}
        
    def generateSchedule(self, dates): #Generates a schedule dictionary which is then added to the allocatedSessions list
        for dateOfSchedule in dates:
            topics = []
            schedule = []
            for subject in self.user.subjects:
                for topic in subject.topics:
                    if not topic.isCompleted:
                        topics.append(topic)
            
            if not topics:  
                self.allocatedSessions[dateOfSchedule] = []
                continue
            timePerSession = self.dailyLimit // len(topics)
            for topic in topics:
                schedule.append((topic.name, topic.subject.name, timePerSession))
                
            self.allocatedSessions[dateOfSchedule] = schedule
        
    def getScheduleForDay(self, dateOfSchedule): #Returns schedule for the day
        return self.allocatedSessions.get(dateOfSchedule, [])
        
    def updateSchedule(self, dateOfSchedule, newTopic, duration): #Updates the schedule for a certain day
        if dateOfSchedule not in self.allocatedSessions:
            self.allocatedSessions[dateOfSchedule] = []
        
        subjectName = getattr(newTopic.subject, "name", newTopic.subject)
        self.allocatedSessions[dateOfSchedule].append((newTopic.name, subjectName, duration))
        
    def export(self, path): #Exports the allocatedSessions list using JSON
        data = {
            str(k): v
            for k, v in self.allocatedSessions.items()  
        }
        with open(path, "w") as f:
            json.dump(data, f, indent = 4)
        print(f"Exported schedule to {path}")
    
    def importSchedule(self, path): #Imports the allocatedSessions list using JSON
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File not found")
            return
        except json.JSONDecodeError:
            print("Invalid JSON")
            return 0
        added = 0
        for dayStr, sessions in data.items():
            try:
                day = datetime.strptime(dayStr, "%Y-%m-%d").date()
            except (TypeError, ValueError):
                print(f"Skipping invalid date: {dayStr}")
                continue
            normalised = []
            for entry in sessions:
                try:
                    topicName, subjectName, duration = entry
                    normalised.append((str(topicName), str(subjectName), int(duration))) #Adds the information to the list
                except Exception:
                    print(f"Skipping malformed session on {dayStr}: {entry}")
                    continue

            self.allocatedSessions[day] = normalised #Adds the list to the allocatedSessions dictionary
            added += 1

        print(f"Imported {added} day(s) into this schedule from {path}")
        return added
