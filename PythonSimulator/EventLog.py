
class EventLog:
    log = []
    startTime = 0

    def __init__(self, object, detail):
        if EventLog.startTime is None:
            startTime = datetime.now()
        self.time = datetime.now()
        self.object = object
        self.detail = detail
        EventLog.log.append(self)

    def __str__(self):
        out = ''
        for l in EventLog.log:
            out += f'time={(l.time-EventLog.startTime).total_seconds()} {l.object} {l.detail}\n'
        return out