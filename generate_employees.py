import names
import random
from faker import Faker
import randominfo
import pymysql
import datetime
fake = Faker("fr_Fr")
def random_social(social=1):
    
    while len(str(social)) < 14:
        social = social * 10 + random.randint(1, 10)
    
    return social

ids_list = list(range(1, 69))
routes_ids = list(range(1, 11))
aircrash = 10
routes = 50
list_plane = [("180", "'A320'"), ("850", "'A380'"), ("100", "'Concorde'")]
list_route = ["'Monaco'", "'Paris'", "'Lyon'", "'Tour'", "'Nice'"]


employees = ["(" + ", ".join([str(random.randint(1200, 999999)),
    str(random_social()), "\""+names.get_last_name()+"\"",
    "\""+names.get_first_name()+"\"", "\""+fake.address()+"\""])+")" for i in
    ids_list]

pilote = []
for i in range(len(ids_list)//5):
    var = random.choice(ids_list)
    ids_list.remove(var)
    pilote.append("( " + ", ".join(["\""+(datetime.datetime.now()
        + datetime.timedelta(weeks=random.randrange(900))).strftime('%Y-%m-%d')+"\"",
        "\""+(datetime.datetime.now()
        +  datetime.timedelta(weeks=random.randrange(666))).strftime('%H:%M:%S')+"\"",
        str(var)]) + ")")

cabincrew = []
for i in range(len(ids_list)//2):
    var = random.choice(ids_list)
    ids_list.remove(var)
    cabincrew.append("(" + ", ".join(["\""+(datetime.datetime.now()
        + datetime.timedelta(weeks=random.randrange(666))).strftime('%H:%M:%S')+"\"",
        random.choice(("'Otesse'", "'Security'")), str(var)]) + ")")

aircraft = ["(" + ", ".join(random.choice(list_plane)) + ")" for _ in
        range(aircrash)]
route = ["(" + ", ".join([random.choice(list_route) for _ in range(2)]) + ")" for _ in
        range(routes)]

departures = []
ids_pilotes = list(range(1, len(pilote)))
aircrews_lists = list(range(1, len(cabincrew)))
while len(ids_pilotes) > 1:    
    pilote_id = random.choice(ids_pilotes)
    ids_pilotes.remove(pilote_id)

    copilote_id = random.choice(ids_pilotes)
    ids_pilotes.remove(copilote_id)
    
    aircrew = ""
    for _ in range(random.randint(1, 4)):
        aircrew_id = random.choice(aircrews_lists)
        aircrews_lists.remove(aircrew_id)
        aircrew += ", "+str(aircrew_id)
    free_place = random.randint(1, 300)
    occupied = 850 - free_place
    departures.append("("+", ".join(["\""+(datetime.date(2021,
        3,23)+datetime.timedelta(weeks=random.randrange(666))).strftime("%Y-%m-%d")+"\"",str(pilote_id),
        str(copilote_id), str(aircrew_id,occupied), str(free_place)])+")")

print(len(departures))
fligth = []
departures_ids= list(range(1, len(departures)))
id_routes = list(range(1, len(route)))
id_devices = list(range(1, len(aircraft)))
while len(departures_ids) > 0 and len(id_routes) > 0 and len(id_deveices) > 0:
    departure_id = random.choice(departures_ids)
    route_id = random.choice(id_routes)
    device_id = ranom.choice(id_devices)

    departures_ids.remove(departure_id)
    id_routes.remove(route_id)
    id_devices.remove(device_id)

    fligth.append("("+", ".join([str(departure_id), "\""+(datetime.datetime.now()
        + datetime.timedelta(weeks=random.randrange(666))).strftime("%Y-%m-%d")+"\"",
        str(route_id), str(device_id)]))

ticket = []
departures_ids= list(range(1, len(departures)))

for _ in range(len(departures_ids)):

    depare_id = random.choice(departures_ids)
    departures_ids.remove(depare_id)

    ticket.append("(" + ", ".join(["\""+(datetime.datetime.now()+
        datetime.timedelta(weeks=random.randrange(666))).strftime("%Y-%m-%d")+"\"",
        str(random.randint(120, 300000)), str(depare_id)])+")")

passenger = []
tickets_ids = list(range(1, len(ticket)))

while len(tickets_ids) > 0:
    passenger_info = ", ".join(["\""+names.get_last_name+"\"",
        "\""+names.get_first_name()+"\"",
        "\""+fake.address()+"\"", 
        "\""+fake.job()+"\"",
        "\""+fake.iban()+"\""])
    for _ in range(random.randint(4)):
        ticket_id = random.choice(tickets_ids)
        tickets_ids.remove(ticket_id)
        passenger.append("(" + passenger_info +", " +str(ticket_id)+")")




connection = pymysql.connect(host="172.21.0.2", user="root", password="passwd", database="aircraft")
cursor = connection.cursor()

cursor.execute("SET GLOBAL FOREIGN_KEY_CHECKS=0;")
connection.commit()

Employee_query = "INSERT INTO `employees`(`salary`, `social_security`, `name`, `first_name`, `address`) VALUES "+ ",\n".join(employees)
Pilote_query = "INSERT INTO `pilote` (`licence`, `among`, `staff_id`) VALUES " + ",\n".join(pilote)
Cabincrew =  "INSERT INTO `cabincrew`(`amoung`, `fonction`, `staff_id`)  VALUES"+",\n".join(cabincrew)
Aircraft = "INSERT INTO `device`(`capacity`, `type`) VALUES " + ",\n".join(aircraft)
Route = "INSERT INTO `route`(`origin`, `arrival`) VALUES " + ",\n".join(route)
Departures = "INSERT INTO `departures`(`date`, `pilote`, `copilote`, `aircrew`,`free_places`, `occupied`) VALUES " + ",\n".join(departures) 
print(Departures)
Fligth = "INSERT INTO `flight`(`id_departures`, `arrival`, `id_route`,`id_device`) VALUES " + ", \n".join(fligth)
Ticket = "INSERT INTO `tickets`(`expire`, `price`, `departures_id`) VALUES " + ", \n".join(ticket)
Passenger = "INSERT INTO `passenger`(`name`, `first_name`, `adress`, `profession`, `bank`, `ticket_id`) VALUES " + ", \n".join(passenger)

cursor.execute(Employee_query)
cursor.execute(Pilote_query)
cursor.execute(Cabincrew)
cursor.execute(Aircraft)
cursor.execute(Route)
cursor.execute(Departures)
cursor.execute(Ticket)
cursor.execute(Passenger)

connection.commit()
connection.close()
