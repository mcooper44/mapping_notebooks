import json
import csv
from collections import defaultdict
from shapely.geometry import MultiPoint, Point

fname = 'Voting_Subdivision.geojson'
add_file = 'addresses.csv'

poll = None

with open(fname) as f:
    poll = json.load(f)

# these are the polls with the highest amount of voter turnout
targets = [(8,30),(8,15),(1,30),(2,10),(1,15),(7,30),(9,5),(2,25),
           (8,35),(3,15),(3,25),(2,5),(2,15),(2,60),(7,35), (7,40),
           (4,15),(7,25),(7,45)]

# for the sake of convenience create a dictionary to hold a list
# of the target polls in each ward
lu = defaultdict(list)
for t in targets:
    w, p = t
    lu[w].append(p)

shape_lu = defaultdict(list)


class add_line:
    def __init__(self, line):
        self.x = float(line[0])
        self.y = float(line[1])
        self.street_n = line[11]
        self.street = line[4]
        self.ward = line[16]
        self.poll = line[17]
        self.roadseg = line[10]
        self.street_str = f'{self.street_n} {self.street}'
        self.point = Point((self.x, self.y))
        self.poll_key = None
        self.csv_list = None

    def set_csv(self):
        self.csv_list = [self.x, self.y,
                         self.street_n, self.street,
                         self.roadseg, self.street_str,
                         self.ward, self.poll, self.poll_key]

    def __str__(self):
        return self.street_str


for p in poll['features']:
    # print a list of all the polls in each ward
    print(f"{p['properties']['WARD']} {p['properties']['POLLING_STATION_NAME']} {p['properties']['POLL']}")
    pl = p['properties']['POLL']
    wd = p['properties']['WARD']
    # add colour attributes to the target wards
    is_tgt = lu.get(int(wd), [None])
    if int(pl) in is_tgt:
        shape = MultiPoint([(float(x[0]), float(x[1])) for x in p['geometry']['coordinates'][0]]).convex_hull
        shape_lu[wd].append((pl, shape))


street_set = set()

out_file = open('target_polls.csv', 'a+', newline='')
f_write = csv.writer(out_file)

with open(add_file, 'r') as csvfile:
    ka = csv.reader(csvfile)
    next(ka)
    for row in ka:
        l = add_line(row)
        if l.street_str not in street_set:
            for ward, polls in shape_lu.items():
                for pl, shape in polls:
                    if l.point.within(shape) and (l.street_str not in street_set):
                        l.poll_key = f'W{ward}-P{pl}'
                        l.ward = ward
                        l.poll = pl
                        l.set_csv()
                        f_write.writerow(l.csv_list)
                        street_set.add(l.street_str)




