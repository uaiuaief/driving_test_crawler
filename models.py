from datetime import datetime
import json


def asdict(obj):
    if isinstance(obj, list):
        return [asdict(element) for element in obj]

    if not hasattr(obj, '__dict__'):
        return str(obj)

    result = {}
    for attr in dir(obj): 
        attr_value = getattr(obj, attr)
        if not attr.startswith('_') and not callable(attr_value):
            result[attr] = asdict(attr_value)

    return result


class BaseClass:
    def to_json(self):
        return json.dumps(asdict(self), indent=4)


class Customer(BaseClass):
    def __init__(self, data):
        self.driving_licence_number = data['driving_licence_number']
        self.test_ref = data['test_ref']
        self.main_test_center = TestCenter(data['main_test_center'])
        self.recent_test_failure = data.get('recent_test_failure')
        self.earliest_test_date = data['earliest_test_date']
        self.latest_test_date = data['latest_test_date']
        self.info_validation = data['info_validation']
        self.acceptable_time_ranges = data['acceptable_time_ranges']

    @staticmethod
    def from_json(json_string):
        data = json.loads(json_string)

        return Customer(data)

    @property
    def recent_test_failure(self):
        return self._recent_test_failure

    @recent_test_failure.setter
    def recent_test_failure(self, value):
        if value == "null":
            self._recent_test_failure = None

    @property
    def earliest_test_date(self):
        return self._earliest_test_date

    @earliest_test_date.setter
    def earliest_test_date(self, value):
        self._earliest_test_date = datetime.strptime(value, '%Y-%m-%d').date()

    @property
    def latest_test_date(self):
        return self._latest_test_date

    @latest_test_date.setter
    def latest_test_date(self, value):
        self._latest_test_date = datetime.strptime(value, '%Y-%m-%d').date()

    @property
    def acceptable_time_ranges(self):
        return self._acceptable_time_ranges

    @acceptable_time_ranges.setter
    def acceptable_time_ranges(self, arr):
        if not arr:
            self._acceptable_time_ranges = []

            return

        self._acceptable_time_ranges = [TimeRange(each) for each in arr]

        return


class TestCenter(BaseClass):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']

class TimeRange(BaseClass):
    def __init__(self, data):
        self.start_time = data['start_time']
        self.end_time = data['end_time']
    
    @property
    def start_time(self):
        return self._start_time
    
    @start_time.setter
    def start_time(self, value):
        self._start_time = datetime.strptime(value, '%H:%M:%S').time()
        
    @property
    def end_time(self):
        return self._end_time
    
    @end_time.setter
    def end_time(self, value):
        self._end_time = datetime.strptime(value, '%H:%M:%S').time()




#test_data = {
#        "driving_licence_number": "SINHA955238IA9WL",
#        "test_ref": "45813588",
#        "main_test_center": {
#            "id": 1,
#            "name": "Worksop",
#            "created_at": "2021-05-27",
#            "last_modified": "2021-05-27",
#            "customers": []
#            },
#        "recent_test_failure": "null",
#        "earliest_test_date": "2021-05-27",
#        "latest_test_date": "2021-10-31",
#        "info_validation": "unchecked",
#        "acceptable_time_ranges": [
#            {
#                "id": 2,
#                "created_at": "2021-05-27T22:25:37.858271Z",
#                "last_modified": "2021-05-27T22:25:37.858340Z",
#                "start_time": "09:00:00",
#                "end_time": "12:00:00",
#                "customer": "SINHA955238IA9WL"
#                },
#            {
#                "id": 3,
#                "created_at": "2021-05-27T23:26:47.024807Z",
#                "last_modified": "2021-05-27T23:26:47.024876Z",
#                "start_time": "15:00:00",
#                "end_time": "18:00:00",
#                "customer": "SINHA955238IA9WL"
#                }
#            ]
#        }
