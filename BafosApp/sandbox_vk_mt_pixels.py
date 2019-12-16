import requests
import json
import time


header = {'Host': 'target.my.com', 'Content-Type': 'application/json',
          'Accept-Encoding': 'gzip, deflate, compress',
          'Authorization': 'Bearer RPUkr7kbGtJajbOPnJABanuWkiOSNZn9Q54RxVF8qJLjqTco8jdyJMSnDINVz5BpOjVVnIfnBQ1MPBwaLaIGyaegG1Y2oN9JxIOMujMnaGShEx81H8FMlvzos3l56Arp8yP5Urymv0oq1JvmD7bwo3i2iVyfqSI51QxAKVWLg1nJ5LgK39dfaGQHRm0zkOUh5Fbc67wQOHnXcqvRNvrAh9Gvr9PAwOD06seaeFAR2os1UHaiu40XCG6EbKg'}

data = {"name":"Совсем Новейший счетчик",
    "url":"http://example.com",
    "email":"test@example.com",
    "password":"12345678"}

counter = requests.post('https://target.my.com/api/v2/remarketing/counters.json',data=json.dumps(data), headers=header)
#counter = requests.get('https://target-sandbox.my.com/api/v2/remarketing/counters.json', headers=header)
print('counter')
print(counter.json())
print(counter.json()['counter_id'])


time.sleep(35)

counter_data = {"name":"новейший пиксель",
                "condition":"jse",
                "substr": "trg-pixel-USER_ID-TIMESTAMP"}

#No access to counter goals
#Failed to add Top@Mail.ru counter goal
counter_goals = requests.post('https://target.my.com/api/v2/remarketing/counters/'+str(counter.json()['counter_id'])+'/goals.json',data=json.dumps(counter_data), headers=header)
print('counter_goals')
print(counter_goals.json())
print(counter_goals.status_code)


segment_data = {"name":"TEST_SEGMENT",
                "pass_condition":1,
                "relations":[{"object_type":"remarketing_counter",
                              "params":{"source_id":counter.json()['counter_id'],"right":0,
                                        "left":365,"type":"positive",
                                        "goal_id":"jse:trg-pixel-USER_ID-TIMESTAMP"}}],
                "logicType":"or"}

segment = requests.post('https://target.my.com/api/v2/remarketing/segments.json',data=json.dumps(segment_data), headers=header)
print('segmnent')
print(segment.json())

