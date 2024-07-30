import json
import os
import statistics
import xml.etree.ElementTree as ET

data = {}


def read_data(path, city):
    city_data = json.load(open(f"{path}/{city}/2021_09_25.json"))
    mean_temp, mean_wind_speed, min_temp, min_wind_speed, max_temp, max_wind_speed = parse_data(city_data['hourly'])
    data[city] = {'mean_temp': float("{:.2f}".format(mean_temp)),
                  'mean_wind_speed': float("{:.2f}".format(mean_wind_speed)),
                  'min_temp': float("{:.2f}".format(min_temp)),
                  'min_wind_speed': float("{:.2f}".format(min_wind_speed)),
                  'max_temp': float("{:.2f}".format(max_temp)),
                  'max_wind_speed': float("{:.2f}".format(max_wind_speed))}


def parse_data(city_data):
    hours = len(city_data)
    mean_temp = statistics.mean([city_data[i]['temp'] for i in range(hours)])
    mean_wind_speed = statistics.mean([city_data[i]['wind_speed'] for i in range(hours)])
    min_temp = min([city_data[i]['temp'] for i in range(hours)])
    min_wind_speed = min([city_data[i]['wind_speed'] for i in range(hours)])
    max_temp = max([city_data[i]['temp'] for i in range(hours)])
    max_wind_speed = max([city_data[i]['wind_speed'] for i in range(hours)])
    return mean_temp, mean_wind_speed, min_temp, min_wind_speed, max_temp, max_wind_speed


if __name__ == '__main__':
    data_path = './source_data'
    cities = [x[0][14:] for x in os.walk(data_path)][1:]
    for c in cities:
        read_data(data_path, c)

    mean_temp = float("{:.2f}".format(statistics.mean([data[city]['mean_temp'] for city in cities])))
    mean_wind_speed = float("{:.2f}".format(statistics.mean([data[city]['mean_wind_speed'] for city in cities])))
    coldest_place = [city for city in cities
                     if data[city]['mean_temp'] == min([data[city]['mean_temp'] for city in cities])]
    warmest_place = [city for city in cities
                     if data[city]['mean_temp'] == max([data[city]['mean_temp'] for city in cities])]
    windiest_place = [city for city in cities
                      if data[city]['mean_wind_speed'] == max([data[city]['mean_wind_speed'] for city in cities])]

    root = ET.Element('weather', country='Spain', date='2021-09-25')
    summary = ET.SubElement(root, 'summary', mean_temp=str(mean_temp), mean_wind_speed=str(mean_wind_speed),
                            coldest_place=coldest_place[0], warmest_place=warmest_place[0],
                            windiest_place=windiest_place[0])

    cities_tag = ET.SubElement(root, "cities")
    for city in cities:
        city_name = city.replace(" ", "_")
        ET.SubElement(cities_tag, city_name, mean_temp=str(data[city]['mean_temp']),
                      mean_wind_speed=str(data[city]['mean_wind_speed']),
                      min_temp=str(data[city]['min_temp']),
                      min_wind_speed=str(data[city]['min_wind_speed']),
                      max_temp=str(data[city]['max_temp']),
                      max_wind_speed=str(data[city]['max_wind_speed']))

    tree = ET.ElementTree(root)
    ET.indent(tree, '  ')
    tree.write("spain_stats.xml", encoding='utf-8')
