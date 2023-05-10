from typing import List, Dict
from datetime import datetime, timedelta

def pretty_time(d: timedelta) -> str:
    return str(d).split(".")[0]

class ActivityInstance:
    start_time: datetime
    end_time: datetime
    duration: datetime

    def __init__(self, start_time: datetime = None, end_time: datetime = None, duration: datetime = None):
        if start_time == None:
            self.start_time = datetime.now()
        else:
            self.start_time = start_time
        self.end_time = end_time
        self.duration = duration

    def currently_running(self) -> bool:
        return self.end_time is None

    def stop_instance(self) -> timedelta | None:
        if not self.currently_running():
            return None
        self.end_time = datetime.now()
        self.duration = self.end_time - self.start_time
        return self.duration
    
    def current_time(self) -> str | None:
        if self.end_time is not None:
            return None
        current_time = datetime.now()
        duration = current_time - self.start_time
        return pretty_time(duration)

class Activity:
    name: str
    instances: List[ActivityInstance]

    def __init__(self, name: str, instances: List[ActivityInstance] = []):
        self.name = name
        self.instances = instances

    def add_instance(self):
        self.instances.append(ActivityInstance())

    def get_last_instance(self) -> ActivityInstance | None:
        if len(self.instances) == 0:
            return None
        return self.instances[-1]

    def currently_running(self) -> bool:
        last_instance = self.get_last_instance()
        if last_instance is None:
            return False
        return last_instance.currently_running()
    
    def stop_timer(self) -> timedelta | None:
        if not self.currently_running():
            return None
        last_instance = self.get_last_instance()
        return last_instance.stop_instance()
    
    def get_total_time(self) -> str:
        total = sum([instance.duration for instance in self.instances], timedelta())
        return pretty_time(total)
    
    def get_current_time(self) -> str | None:
        if not self.currently_running():
            return None
        return self.get_last_instance().current_time()
        
class ActivityTracker:
    current_activity: str
    activities: Dict[str, Activity]

    def __init__(self, activities: Dict[str, Activity] = {}):
        self.activities = activities
        self.current_activity = None

    def get_current_activity(self) -> Activity | None:
        if self.current_activity is None:
            return None
        return self.activities[self.current_activity]

    def timer_running(self) -> bool:
        current_activity = self.get_current_activity()
        if current_activity is None:
            return False
        return current_activity.currently_running()

    def name_available(self, name):
        return name not in self.activities
    
    def add_activity(self, name) -> bool:
        if not self.name_available(name):
            return False
        self.activities[name] = Activity(name)
        return True

    def remove_activity(self, name) -> bool: 
        if self.name_available(name):
            return False
        del self.activities[name]
        return True
    
    def get_current_time(self) -> str | None:
        if not self.timer_running():
            return None
        return self.get_current_activity().get_current_time()
    
    def start_timer(self, name) -> bool:
        if self.name_available(name):
            return False
        if self.timer_running():
            self.stop_timer()
        self.current_activity = name
        activity: Activity = self.activities[name]
        activity.add_instance()

    def stop_timer(self) -> timedelta | None:
        if not self.timer_running():
            return None
        current_activity = self.get_current_activity()
        duration = current_activity.stop_timer()
        if duration is None:
            return None
        self.current_activity = None
        return duration