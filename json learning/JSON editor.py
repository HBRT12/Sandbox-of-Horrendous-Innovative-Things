import json
import time
dictionary_1 = {'name': None,
                'day of birth': None,
                'month of birth': None,
                'year of birth': None,
                'age': None}
name = input('What is your name>>> ')
dictionary_1['name']=name
dob = input('What day were you born on>>> ')
dictionary_1['day of birth']=dob
mob = input('What month were you born in>>> ')
dictionary_1['month of birth']=mob
yob = input('What year were you born in>>> ')
dictionary_1['year of birth']=yob
age = input('How old are you>>> ')
dictionary_1['age']=age
with open('my first json file.json','w') as file:
    json.dump(dictionary_1, file, indent=4)
print('Saved to JSON file!')
time.sleep(1)
