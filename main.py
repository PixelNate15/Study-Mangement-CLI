#Imports
if __package__:
    from .classes.user import User
    from .classes.subject import Subject
    from .classes.topic import Topic
    from .classes.schedule import Schedule
    from .classes.revision_log import RevisionLog
else:
    # Allows the CLI to be launched directly with ``python CLI/main.py``.
    from classes.user import User
    from classes.subject import Subject
    from classes.topic import Topic
    from classes.schedule import Schedule
    from classes.revision_log import RevisionLog
from datetime import datetime, date, timedelta
import json

#Constants
CONSTUSER = 1
CONSTSUBJECT = 2
CONSTTOPIC = 3
CONSTSCHEDULE = 4
CONSTREVISIONLOG = 5

#Global Variables
users = []
subjects = []
topics = []
schedules = []


#Reusable function to convert string to date datatype
def dateDatatypeConverter(original):
    while True:
        try:
            new = datetime.strptime(original, "%Y-%m-%d").date()
            if type(new) == date:
                break
        except ValueError:
            original = input("Invalid format. Please try again (format: YYYY-MM-DD)")
    
    return new

#Reusable function to convert character to boolean datatype
def boolDatatypeConverter(original):
    while True:
        original = original.strip().upper()
        if original == 'T':
            return True
        elif original == 'F':
            return False
        original = input("Invalid input, try again (T/F): ")


def readInteger(prompt="", minimum=None, maximum=None):
    """Read an integer without terminating the CLI on invalid input."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")
            continue
        if minimum is not None and value < minimum:
            print(f"Please enter a number of at least {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Please enter a number no greater than {maximum}.")
            continue
        return value

#Reusable function to get all datas in a range
def getAllDates(d1, d2):
    dates = []
    while True:
        if d1 <= d2:
            dates.append(d1)
            d1 += timedelta(days = 1)
        else:
            break
        
    return dates


#Function to create a user object
def createUser():
    name = input("What is your name? ")
    userID = input("What is your ID? ")
    newUser = User(name, userID)
    users.append(newUser)
    return newUser

#Function to select user object
def selectUser():
    if not users:
        print("You need to create a user first")
        return None
    for i, u in enumerate(users, start=1):
        print(f"{i}: {u.name} (ID: {u.userID})")
    idx = readInteger("Which user is the user you would like to select? ")
    if idx >= 1 and idx <= len(users):
        return users[idx - 1]
    print("Invalid Selection")
    return None

#Function to create a subject object
def createSubject():
    name = input("What is the name of the subject? ")
    examBoard = input("What exam board does this subject use? ")
    newSubject = Subject(name, examBoard)
    subjects.append(newSubject)
    return newSubject

#Function to select subject object
def selectSubject():
    if not subjects:
        print("You need to create a subject first")
        return None
    for i, s in enumerate(subjects, start=1):
        print(f"{i}: {s.name} (Exam Board: {s.examBoard})")
    idx = readInteger("Which subject is the subject you would like to select? ")
    if idx >= 1 and idx <= len(subjects):
        return subjects[idx - 1]
    print("Invalid Selection")
    return None

#Function to create topic object
def createTopic():
    topicName = input("What is the name of the topic? ")
    subject = selectSubject()
    if not subject:
        return None
    difficulty = readInteger("Rate the difficulty of this topic (1-10): ", 1, 10)
    estimatedHours = readInteger("How many hours do you think this topic will take to revise? ", 1)
    isCompleted = boolDatatypeConverter(input("Is the topic complete (Enter T/F)? "))
    newTopic = subject.addTopic(topicName, difficulty, estimatedHours, isCompleted)
    if newTopic is not None:
        topics.append(newTopic)
    return newTopic

#Function to select topic object
def selectTopic():
    if not topics:
        print("You need to create a topic first")
        return None
    for i, t in enumerate(topics, start=1):
        print(f"{i}: {t.name} (Subject: {t.subject})")
    idx = readInteger("Which topic is the topic you would like to select? ")
    if idx >= 1 and idx <= len(topics):
        return topics[idx - 1]
    print("Invalid Selection")
    return None

#Function to create a schedule object
def createSchedule(user):
    dailyLimit = readInteger("How long each day can you revise for? ", 1)
    startDate = dateDatatypeConverter(input("What date would you like to start revising? (YYYY-MM-DD) "))
    endDate = dateDatatypeConverter(input("What date would you like to stop revising? (YYYY-MM-DD) "))
    while endDate < startDate:
        print("The end date cannot be before the start date.")
        endDate = dateDatatypeConverter(input("What date would you like to stop revising? (YYYY-MM-DD) "))
    newSchedule = Schedule(user, dailyLimit, startDate, endDate)
    schedules.append(newSchedule)
    user.schedules.append(newSchedule)
    newSchedule.generateSchedule(getAllDates(startDate, endDate))
    return newSchedule

#Function to select schedule object
def selectSchedule():
    if not schedules:
        print("You need to create a schedule first")
        return None
    for i, s in enumerate(schedules, start=1):
        print(f"{i}: {s.user.name} ({s.startDate} to {s.endDate})")
    idx = readInteger("Which schedule is the schedule you would like to select? ")
    if idx >= 1 and idx <= len(schedules):
        return schedules[idx - 1]
    print("Invalid Selection")
    return None

#List revision logs
def listLogs(user):
    if not user.revisionLogs:
        print("No logs yet")
        return
    for i, log in enumerate(user.revisionLogs, start = 1):
        print(f"{i}: {log.date} ({log.subjectName} - {log.topicName}: {log.duration})")
        
#Export log to JSON
def exportLogToJSON(user, path):
    data = [log.toDict() for log in user.revisionLogs]
    with open(path, "w") as f:
        json.dump(data, f, indent = 4)
    print(f"Exported {len(data)} logs to {path}")
    
#Import log from JSON
def importLogToJSON(user, path):
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("File not found")
        return
    added = 0
    for item in data:
        user.revisionLogs.append(RevisionLog.fromDict(item))
        added += 1
    print(f"Imported {added} logs from {path}")


#Main Menu
def mainMenu():
    print("Select an option from the below options:")
    print("1: User")
    print("2: Subject")
    print("3: Topic")
    print("4: Schedule")
    print("5: Revision Log")
    print("6: Quit")
    option = readInteger("Choice: ")
    if option == 6:
        return False
    elif option < 1 or option > 6:
        print("Invalid Option, try again")
    else:
        subMenus(option)
    return True

#Sub-Menus
def subMenus(option):
    while True:
        #User Sub-Menu
        if option == CONSTUSER:
            print("Select an option from the below options:")
            print("1: Create User")
            print("2: Add subject")
            print("3: Remove subject")
            print("4: Get subject")
            print("5: Log revision")
            print("6: Total revision time")
            print("7: Back to main menu")
            choice = readInteger("Choice: ")
            if choice == 1:
                createUser()
            elif choice == 2:
                user = selectUser()
                if not user:
                    continue
                subjectName = input("What is the name of the subject? ")
                examBoard = input("What is the name of the exam board? ")
                subject = user.addSubject(subjectName, examBoard)
                if subject is not None:
                    subjects.append(subject)
            elif choice == 3:
                user = selectUser()
                if not user:    
                    continue
                subjectName = input("What is the name of the subject? ")
                user.removeSubject(subjectName)
            elif choice == 4:
                user = selectUser()
                if not user:
                    continue
                subjectName = input("What is the name of the subject? ")
                subject = user.getSubject(subjectName)
                print(subject if subject is not None else "Subject not found")
            elif choice == 5:
                user = selectUser()
                if not user:
                    continue
                topicName = input("What is the name of the topic you revised?")
                subjectName = input("What is the name of the subject? ")
                duration = readInteger("How long did you revise today? ", 1)
                notes = input("Where there any brief notes you would like to make about this session? ")
                user.logRevision(topicName, subjectName, duration, notes)
            elif choice == 6:
                user = selectUser()
                if not user:
                    continue
                print(user.totalRevisionTime())
            elif choice == 7:
                break
            else:
                print("Invalid Choice, try again")
        #Subject Sub-Menu
        elif option == CONSTSUBJECT:
            print("Select an option from the below options:")
            print("1: Create Subject")
            print("2: Add Topic")
            print("3: Remove topic")
            print("4: Get topic")
            print("5: Count Completed Topics")
            print("6: Back to main menu")
            choice = readInteger("Choice: ")
            if choice == 1:
                createSubject()
            elif choice == 2:
                subject = selectSubject()
                if not subject:
                    continue
                topicName = input("What is the name of the topic? ")
                difficulty = readInteger("How difficult is the topic (1-10)? ", 1, 10)
                estimatedHours = readInteger("How many hours do you estimate you need to revise this topic? ", 1)
                isCompleted = boolDatatypeConverter(input("Is the topic complete (Enter T/F)? "))
                topic = subject.addTopic(topicName, difficulty, estimatedHours, isCompleted)
                if topic is not None:
                    topics.append(topic)
            elif choice == 3:
                subject = selectSubject()
                if not subject:
                    continue
                topicName = input("What is the name of the topic? ")
                subject.removeTopic(topicName)
            elif choice == 4:
                subject = selectSubject()
                if not subject:
                    continue
                topicName = input("What is the name of the topic? ")
                topic = subject.getTopic(topicName)
                print(topic if topic is not None else "Topic not found")
            elif choice == 5:
                subject = selectSubject()
                if not subject:
                    continue
                subject.countCompletedTopics()
            elif choice == 6:
                break
            else:
                print("Invalid Choice, try again")
        #Topic Sub-Menu
        elif option == CONSTTOPIC:
            print("Select an option from the below options:")
            print("1: Add topic")
            print("2: Mark Completed")
            print("3: Add test score")
            print("4: Average score")
            print("5: Back to main menu")
            choice = readInteger("Choice: ")
            if choice == 1:
                createTopic()
            elif choice == 2:
                topic = selectTopic()
                if not topic:
                    continue
                topic.markCompleted()
            elif choice == 3:
                topic = selectTopic()
                if not topic:
                    continue
                score = readInteger("What was the score in the test from this topic? ", 0)
                dateOfTest = dateDatatypeConverter(input("What date did you take the test (YYYY-MM-DD)? "))
                topic.addTestScore(score, dateOfTest)
            elif choice == 4:
                topic = selectTopic()
                if not topic:
                    continue
                topic.averageScore()
            elif choice == 5:
                break
            else:
                print("Invalid Choice, try again")
        #Schedule Sub-Menu
        elif option == CONSTSCHEDULE:
            print("Select an option from the below options:")
            print("1: Create schedule")
            print("2: Get schedule for the day")
            print("3: Update a schedule")
            print("4: Export a schedule")
            print("5: Import a schedule")
            print("6: Back to main menu")
            choice = readInteger("Choice: ")
            if choice == 1:
                user = selectUser()
                if not user:
                    continue
                createSchedule(user)
            elif choice == 2:
                schedule = selectSchedule()
                if not schedule:
                    continue
                dateOfSchedule = dateDatatypeConverter(input("What date did you want to view the schedule for (YYYY-MM-DD)? "))
                day = schedule.getScheduleForDay(dateOfSchedule)
                print(f" The schedule for that day is: {day}")
            elif choice == 3:
                schedule = selectSchedule()
                if not schedule:
                    continue
                dateOfSchedule = dateDatatypeConverter(input("What date did you want to update schedule (YYYY-MM-DD)? "))
                newTopic = selectTopic()
                if not newTopic:
                    continue
                duration = readInteger("How long would you like to revise for? ", 1)
                schedule.updateSchedule(dateOfSchedule, newTopic, duration)
            elif choice == 4:
                schedule = selectSchedule()
                if not schedule:
                    continue
                path = input("What is the path you want to export to? ")
                schedule.export(path)
            elif choice == 5:
                schedule = selectSchedule()
                if not schedule:
                    continue
                path = input("What is the path you want to import from? ")
                schedule.importSchedule(path)
            elif choice == 6:
                break
            else:
                print("Invalid Choice, try again")
        #Revision Log Sub-Menu
        elif option == CONSTREVISIONLOG:
            print("Select an option from the below options:")
            print("1: List Logs")
            print("2: Add a log")
            print("3: Export logs (JSON)")
            print("4: Import logs (JSON)")
            print("5: Back to main menu")
            choice = readInteger("Choice: ")
            if choice == 1:
                user = selectUser()
                if not user:
                    continue
                listLogs(user)
            elif choice == 2:
                user = selectUser()
                if not user:
                    continue
                dateOfLog = dateDatatypeConverter(input("What date did you want to log your revision for (YYYY-MM-DD)? "))
                topicName = input("What topic did you revise? ")
                subjectName = input("What is the name of the subject you revised? ")
                duration = readInteger("How long did you revise for? ", 1)
                notes = input("Did you make any brief notes about the session? ")
                user.logRevision(topicName, subjectName, duration, notes, dateOfLog)
                print("Revision logged")
            elif choice == 3:
                user = selectUser()
                if not user:
                    continue
                path = input("What is the path to the file? ")
                exportLogToJSON(user, path)
            elif choice == 4:
                user = selectUser()
                if not user:
                    continue
                path = input("What is the path to the file? ")
                importLogToJSON(user, path)
            elif choice == 5:
                break
            else:
                print("Invalid Choice, try again")


def main():
    print("Study Plan CLI")
    try:
        while mainMenu():
            pass
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye")


if __name__ == "__main__":
    main()
