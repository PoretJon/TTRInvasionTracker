import requests, time
from .invasion import Invasion


class InvasionTracker:
    API_URL = "https://www.toontownrewritten.com/api/invasions"

    current_invasions = set()

    def __init__(self):
        return

    def refresh_current_invasions(self):
        resp = requests.get(self.API_URL)
        if resp.status_code == 200:
            dat = resp.json()["invasions"]
            current_districts = [invasion for invasion in dat]
            temp = set()
            for inv in current_districts:
                invasion_obj = Invasion(dat[inv]["type"], inv, dat[inv]["progress"])
                temp.add(invasion_obj)

        new_invasions = temp - self.current_invasions
        ended_invasions = (
            self.current_invasions - temp
        )  # get ended invasions to remove them from the list

        for inv in new_invasions:
            print(f"New invasion: {inv.printOut()}\n")
            self.current_invasions.add(inv)

        for inv in ended_invasions:
            print(f"Ended invasion: {inv.printOut()}\n")
            self.current_invasions.remove(inv)

    def get_cur_invasions_message(self) -> str:
        if len(self.current_invasions) == 0:
            return "No current invasions."

        msg = "Current invasions:\n"
        for inv in self.current_invasions:
            msg += inv.printOut() + "\n\n"
        return msg


# testing code

# tracker = InvasionTracker()
# tracker.refresh_current_invasions()

# print(tracker.get_cur_invasions_message())
