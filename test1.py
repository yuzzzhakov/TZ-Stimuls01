import os
from stimuls import Stimuls as stimuls_list

with open('events.txt') as f:
    events = f.read().splitlines()
    for i, event in enumerate(events):
        # Разделяем строку события на список строк параметров события
        splitted_event = event.split()
        d_events = dict()
        # Добавляем в словарь индекс строки и параметры
        d_events['event_id'] = i
        # d_events['frame_type'] = splitted_event[0]
        # d_events['event_type_number'] = int(splitted_event[2])
        d_events['start_time'] = int(splitted_event[3])
        d_events['end_time'] = int(splitted_event[4])
        # d_events['duration'] = int(splitted_event[5])
        # d_events['x0'] = float(splitted_event[6])
        # d_events['y0'] = float(splitted_event[7])
        # d_events['x'] = float(splitted_event[8])
        # d_events['y'] = float(splitted_event[9])
        events[i] = d_events


true_stimuls_id = []
for i, stimul in enumerate(stimuls_list):
    if stimul['tech']:
        true_stimuls_id.append(i)

time_point_list = [0]
for i, stimul in enumerate(stimuls_list):
    time_point_list.append(time_point_list[i] + stimul['length'] * 1000)

stimuls = []
for i in true_stimuls_id:
    stimuls.append({
        'stimul_id': i,
        'start_time': time_point_list[i],
        'end_time': time_point_list[i+1],
        'events_ids': []
    })

for stimul in stimuls:
    for event in events:
        if ((event['start_time'] < stimul['start_time'])
            and (event['end_time'] > stimul['end_time']))\
                or ((event['start_time'] < stimul['start_time'])
                    and (event['end_time'] > stimul['start_time'])
                    and (event['end_time'] <= stimul['end_time']))\
                or ((event['start_time'] >= stimul['start_time'])
                    and (event['start_time'] <= stimul['end_time'])
                    and (event['end_time'] > stimul['end_time']))\
                or ((event['start_time'] >= stimul['start_time'])
                    and (event['end_time'] <= stimul['end_time'])):
            stimul['events_ids'].append(event['event_id'])


print(true_stimuls_id)
print(time_point_list)
print(stimuls)
print(events)

path = os.getcwd() + '/stimul_events'

try:
    os.mkdir(path)
except OSError:
    print("Создать директорию %s не удалось" % path)
else:
    print("Успешно создана директория %s " % path)


with open('events.txt') as f:
    event_lines = f.read().splitlines()
    for stimul in stimuls:
        with open(path + '/Stimul' + str(stimul['stimul_id']+1) + '.txt', 'w') as f2:
            for event_id in stimul['events_ids']:
                f2.write(event_lines[event_id] + '\n')
