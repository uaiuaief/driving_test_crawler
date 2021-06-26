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
        self.id = data['id']
        profile = data['profile']
        self.driving_licence_number = profile['driving_licence_number']
        self.test_ref = profile['test_ref']
        #self.main_test_center = TestCenter(profile['main_test_center'])
        self.test_centers = profile['test_centers']
        self.recent_test_failure = profile.get('recent_test_failure')
        self.earliest_test_date = profile['earliest_test_date']
        self.latest_test_date = profile['latest_test_date']
        self.earliest_time = profile['earliest_time']
        self.latest_time = profile['latest_time']
        self.info_validation = profile['info_validation']
        self.automatic_booking = profile['automatic_booking']

    def __str__(self):
        return f"{self.driving_licence_number} ::: {self.test_ref}"

    @staticmethod
    def from_json(json_string):
        data = json.loads(json_string)

        return Customer(data)

    @property
    def test_centers(self):
        return self._test_centers

    @test_centers.setter
    def test_centers(self, value):
        arr = []
        for each in value:
            arr.append(TestCenter(each))

        self._test_centers = arr

    @property
    def recent_test_failure(self):
        return self._recent_test_failure

    @recent_test_failure.setter
    def recent_test_failure(self, value):
        if value == None:
            self._recent_test_failure = None
        else:
            self._recent_test_failure = datetime.strptime(value, "%Y-%m-%d").date()

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
        if value:
            self._latest_test_date = datetime.strptime(value, '%Y-%m-%d').date()
        else:
            self._latest_test_date = None

    @property
    def earliest_time(self):
        return self._earliest_time

    @earliest_time.setter
    def earliest_time(self, value):
        if value == "null":
            self._earliest_time = None
        else:
            self._earliest_time = datetime.strptime(value, '%H:%M:%S').time()

    @property
    def latest_time(self):
        return self._latest_time

    @latest_time.setter
    def latest_time(self, value):
        if value == "null":
            self._latest_time = None
        else:
            self._latest_time = datetime.strptime(value, '%H:%M:%S').time()


class TestCenter(BaseClass):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']


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


