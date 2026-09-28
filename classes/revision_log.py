from datetime import datetime


class RevisionLog:
    def __init__(self, date, topicName, subjectName, duration, notes):
        self.date = date
        self.topicName = topicName
        self.subjectName = subjectName
        self.duration = duration
        self.notes = notes

    def toDict(self):
        return {
            "date": str(self.date),
            "topicName": self.topicName,
            "subjectName": self.subjectName,
            "duration": self.duration,
            "notes": self.notes,
        }

    @staticmethod
    def fromDict(data):
        return RevisionLog(
            datetime.strptime(data["date"], "%Y-%m-%d").date(),
            data["topicName"],
            data["subjectName"],
            data["duration"],
            data["notes"],
        )
