from py2neo import authenticate, Graph, Path, Node, Relationship
import csv

def parse_locations():
    f = open("data/airports.csv")

    first = True
    locations = {}
    reader = csv.reader(f)
    for row in reader:

        if first:
            first = False
            continue

        locations[row[0]] = [float(row[5]), float(row[6])]

    return locations

locations = parse_locations()

#house keeping
authenticate('localhost:7474', 'neo4j', 'neo')
graph = Graph('http://localhost:7474/db/data')
file = open("data/flight-network-with-times.txt")

#nodes = []  # not used/needed?

# This will delete everything in the old database.
graph.delete_all()

# A full object probably isn't necessary here. Though it might be good if we try to add geo locations to the database.
class Airport:   # encapsulates details of any instance of an airport.
    def __init__(self, airport_id, airport, city_name, state, market):
        self.airport_id = airport_id    #numeral
        self.airport = airport          #call letters
        self.city_name = city_name.replace("\"", "").split(',')[0]      #city
        self.state = state              # state
        self.market = market            #??
        self.fliesTo = []

# Airports are uniquely identified by their "airport" field. This is the three letter code.
# AirportManager class catalogs and maintains list of airports, and the connections of each airport.
class AirportManager:
    def __init__(self):
        self.airports = []
        self.nodes = []
    # Update_airport generates node info for each unique 'ap' input.
    def update_airport(self, ap):

        n = Node("AIRPORT", airport, ap.state, state=ap.state, airport_id=ap.airport_id, airport=ap.airport,
                     city_name=ap.city_name, market=ap.market, id=len(self.airports), lat=locations[ap.airport][0],
                    lon=locations[ap.airport][1])

        # check to see if Airport already exists?
        for i in range(0, len(self.airports)):
            if self.airports[i].airport_id == ap.airport_id:
                # self.airports[i] = ap
                # self.nodes[i] = n
                #print 'fliesTo list of ' + ap.airport + ' has ' + str(len(ap.fliesTo)) + ' elements'

                return self.nodes[i]

        self.airports.append(ap)
        self.nodes.append(n)

        return n
    #add_target accepts 'origin' and 'destination' airport classes from a given line in our parsed data.
    # finds origin.airport in the airportManager database and scans origin.fliesTo list to see if the target.airport
    # exists.  If not, we add it to origin.fliesTo
    def add_target(self,ap_origin, ap_target):

        for i in range(0, len(self.airports)):
            if self.airports[i].airport_id == ap_origin.airport_id:
                a=self.airports[i]
                # check to see if Airport already exists?
                for j in range(0, len(a.fliesTo)):
                    if a.fliesTo[j].airport_id == ap_target.airport_id:
                        return #self.fliesTo[i]

                # add target city to orgin.fliesTo only if we haven't found it in our list
                a.fliesTo.append(ap_target)

        #print 'adding ' + ap_target.airport +  ' to ' + self.airport
        #print 'adding ' + ap_target.airport + ' to fliesTo list of ' + self.airport  #self.fliesTo[len(self.fliesTo)-1].airport
       # return ap_target

# Actually parse the file.=======================================
manager = AirportManager()
edges = []

first = True
# Each line in the file identifies a flight. For each flight,
# 1. get its origin and destination airports
# 2. add a relationship connecting those airports

month_index = -1
day_index = -1
carrier_index = -1
fl_num_index = -1
origin_airport_id_index = -1
origin_airport_index = -1
origin_city_name_index = -1
origin_state_name_index = -1
origin_market_index = -1
dest_airport_id_index = -1
dest_airport_index = -1
dest_city_name_index = -1
dest_state_name_index = -1
dest_market_index = -1
fl_cancelled_index = -1
fl_airtime_index = -1
fl_distance_index = -1
fl_dep_time_index = -1
fl_arr_time_index = -1

count = 0
for line in file:
    count += 1
    # Skip first line
    if first:
        first = False
        keys = line.split('\t')
        month_index = keys.index("MONTH")
        day_index = keys.index("DAY_OF_MONTH")
        carrier_index = keys.index("CARRIER")
        fl_num_index = keys.index("FL_NUM")
        origin_airport_id_index = keys.index("ORIGIN_AIRPORT_ID")
        origin_airport_index = keys.index("ORIGIN")
        origin_city_name_index = keys.index("ORIGIN_CITY_NAME")
        origin_state_name_index = keys.index("ORIGIN_STATE_ABR")
        origin_market_index = keys.index("ORIGIN_CITY_MARKET_ID")
        dest_airport_id_index = keys.index("DEST_AIRPORT_ID")
        dest_airport_index = keys.index("DEST")
        dest_city_name_index = keys.index("DEST_CITY_NAME")
        dest_state_name_index = keys.index("DEST_STATE_ABR")
        dest_market_index = keys.index("DEST_CITY_MARKET_ID")
        fl_cancelled_index = keys.index("CANCELLED")
        fl_airtime_index = keys.index("AIR_TIME")
        fl_distance_index = keys.index("DISTANCE")
        fl_dep_time_index = keys.index("DEP_TIME")
        fl_arr_time_index = keys.index("ARR_TIME")
        fl_dep_delay_index = keys.index("DEP_DELAY")
        continue

    line = line.split('\t')

    month = int(line[month_index])
    day_of_month = int(line[day_index])

    if not (month == 1 and day_of_month == 1) and not (month == 1 and day_of_month == 2):
        continue

    # # parse origin airport
    airport_id = int(line[origin_airport_id_index])
    airport = str(line[origin_airport_index])
    city_name = str(line[origin_city_name_index])
    state = str(line[origin_state_name_index])
    market = str(line[origin_market_index])

    # add it to the database
    ap_origin = Airport(airport_id, airport, city_name, state, market)
    source = manager.update_airport(ap_origin)

    # parse destination airport
    airport_id = int(line[dest_airport_id_index])
    airport = str(line[dest_airport_index])
    city_name = str(line[dest_city_name_index])
    state = str(line[dest_state_name_index])
    market = str(line[dest_market_index])


    # add it to the database
    ap_target = Airport(airport_id, airport, city_name, state, market)
    target = manager.update_airport(ap_target)


    #Skip cancelled flights
    cancelled = line[fl_cancelled_index] == '1'
    if not cancelled:
        if line[fl_airtime_index] != "":
            distance = int(line[fl_distance_index])
            airtime = int(line[fl_airtime_index])
            arr_time = int(line[fl_arr_time_index])
            dep_time = int(line[fl_dep_time_index])
            carrier = line[carrier_index]
            flight_id = line[fl_num_index]
            dep_delay = int(line[fl_dep_delay_index])

            # do we want to create an edge for every flight regardless of repeat source/target pairs?
            flight = Relationship(source, "FLIGHT", target, flight_id=flight_id, carrier=carrier, airtime=airtime, distance=distance, arr_time=arr_time, dep_time=dep_time, day=day_of_month, month=month, id=len(edges), dep_delay=dep_delay)
            edges.append(flight)

print manager.nodes, edges

for node in manager.nodes:
    graph.create(node)

for edge in edges:
    graph.create(edge)

print 'Done.'
