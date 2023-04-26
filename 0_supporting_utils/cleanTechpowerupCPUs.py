import json
import jsonlines
import re

def clean_clock_string(clock_speed):
    print(clock_speed)
    if 'mhz' in clock_speed:
        clock_speed = re.sub('mhz', '', clock_speed).strip()
        clock_speed = float(clock_speed.strip())/1024
        return clock_speed
    if 'ghz' in clock_speed:
        clock_speed = re.sub('ghz', '', clock_speed).strip()
        clock_speed = float(clock_speed.strip())
        return clock_speed
    clock_speed = float(clock_speed.strip())
    return clock_speed

def clean_cpu_obj(cur_obj):
    cur_dict = {}
    cur_dict['name'] = cur_obj['name']
    cur_dict['Codename'] = cur_obj['Codename']
    cur_dict['Socket'] = cur_obj['Socket']
    cur_dict['Company'] = cur_obj['Company']

    try:
        cores = cur_obj['Cores'].split('/')
        if len(cores) == 2:
            cur_dict['core_1'],cur_dict['core_2'] = int(cores[0].strip()),int(cores[1].strip())

        elif len(cores) == 1 and cores[0] != '':
            cur_dict['core_1'] = int(cores[0].strip())
            cur_dict['core_2'] = -1
    except:
        cur_dict['core_1'] = -1
        cur_dict['core_2'] = -1

    try:
        clock = cur_obj['Clock'].split('to')
        if len(clock) == 2:
            cur_dict['lower_clock_speed_ghz'] = clean_clock_string(clock[0].lower())
            cur_dict['higher_clock_speed_ghz'] = clean_clock_string(clock[1].lower())
        elif len(clock) == 1:
            cur_dict['lower_clock_speed_ghz'] = clean_clock_string(clock[0].lower())
            cur_dict['higher_clock_speed_ghz'] = -1
    except:
        cur_dict['lower_clock_speed_ghz'] = -1
        cur_dict['higher_clock_speed_ghz'] = -1

    try:
        process = re.sub('nm','',cur_obj['Process']).strip()
        cur_dict['process'] = int(process)
    except:
        cur_dict['process'] = -1

    try:
        l3_cache = cur_obj['L3 Cache'].lower()
        if 'mb' in l3_cache:
            l3_cache = re.sub('mb','',l3_cache).strip()
            cur_dict['l3_cache'] = int(l3_cache)
        else:
            cur_dict['l3_cache'] = -1
    except:
        cur_dict['l3_cache'] = -1

    try:
        tdp = cur_obj['TDP'].lower()
        if 'w' in tdp:
            tdp = re.sub('w', '', tdp).strip()
            cur_dict['tdp'] = int(tdp)
        else:
            cur_dict['tdp'] = -1
    except:
        cur_dict['tdp'] = -1

    try:
        released = int(cur_obj['Released'].split(',')[-1].strip())
        cur_dict['released'] = released
    except:
        cur_dict['released'] = -1

    return cur_dict


if __name__ == '__main__':
    with jsonlines.open('../data_with_ids/techpowerup_cpu_cleaned.jl','w') as writer:
        with jsonlines.open('../data_with_ids/techpowerup_cpu.jl') as reader:
            for cur_obj in reader:
                key,val = list(cur_obj.items())[0][0],list(cur_obj.items())[0][1]
                cur_dict = clean_cpu_obj(val)
                write_obj = {key:cur_dict}
                writer.write(write_obj)










