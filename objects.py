from typing import List, Dict
from datetime import datetime, timedelta
import pandas as pd

def pretty_time(d: timedelta) -> str:
    return str(d).split(".")[0]

def append_df(df, row):
    return pd.concat([df, pd.DataFrame.from_records([row])])   

def str_to_datetime(d: str) -> datetime:
    return datetime.strptime(d, '%y-%m-%d %H:%M:%S.%f')

def datetime_to_str(d: datetime) -> str:
    return d.strftime('%y-%m-%d %H:%M:%S.%f')

class ActivityInstance:
    start_time: datetime
    end_time: datetime
    duration: timedelta

    def __init__(self, start_time: datetime = None, end_time: datetime = None, duration: timedelta = None):
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
    
    def to_string(self) -> str:
        return datetime_to_str(self.start_time)

class Activity:
    name: str
    instances: List[ActivityInstance]

    def __init__(self, name: str, instances: List[ActivityInstance] = []):
        self.name = name
        self.instances = instances

    def add_instance(self):
        self.instances.append(ActivityInstance())

    def delete_instance(self, start_time: str) -> bool:
        if start_time == None:
            print("Delete Instance: No start time")
            return False
        instance = None
        for i in self.instances:
            if datetime_to_str(i.start_time) == start_time:
                instance = i
                break
        if instance == None:
            print(f"Delete Instance: could not find start time \"{start_time}\"")
            return False
        self.instances.remove(instance)
        return True

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
    
    def get_hours_last_week(self) -> timedelta:
        now = datetime.now()
        last_week = now - timedelta(days=7, hours=now.hour, minutes=now.minute)
        total_time = timedelta(days=0)
        instances_last_week = [i for i in self.instances if i.start_time >= last_week]
        for i in instances_last_week:
            total_time += i.duration
        return total_time
        
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
    
    def set_activity(self, name) -> bool:
        if self.name_available(name):
            print(f"Set Activity: Activity {name} not available")
            return False
        if self.timer_running():
            print("Set Activity: Timer is currently running")
            return False
        if self.get_current_activity() != None:
            print("Set Activity: Activity already set")
            return False
        self.current_activity = name
        return True

    def unload_activity(self) -> bool:
        if self.get_current_activity() == None:
            return
        if self.timer_running():
            self.stop_timer()
        self.current_activity = None
    
    def start_timer(self, name) -> bool:
        if self.name_available(name):
            return False
        if self.timer_running():
            self.stop_timer()
        if self.get_current_activity() == None:
            return False
        self.activities[name].add_instance()

    def stop_timer(self) -> timedelta | None:
        if not self.timer_running():
            return None
        current_activity = self.get_current_activity()
        duration = current_activity.stop_timer()
        if duration is None:
            return None
        self.current_activity = None
        return duration
    
    def to_dataframe(self) -> pd.DataFrame:
        self.stop_timer()
        df = pd.DataFrame(columns=["Activity", "Start", "End"])
        for a in self.activities.values():
            for i in a.instances:
                df = append_df(df, {
                    "Activity": a.name,
                    "Start": datetime_to_str(i.start_time),
                    "End": datetime_to_str(i.end_time)
                })
        
        return df
    
    def from_dataframe(df: pd.DataFrame):
        instances = { }
        for _, row in df.iterrows():
            name = row["Activity"]
            if not name in instances:
                instances[name] = [ ]
            start = str_to_datetime(row["Start"])
            end = str_to_datetime(row["End"])
            duration = end - start
            instances[name].append(ActivityInstance(start, end, duration))

        activities = { }
        for k in instances.keys():
            activities[k] = Activity(k, instances[k])
        return ActivityTracker(activities)