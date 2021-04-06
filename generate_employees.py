import names
import random
from faker import Faker
import pymysql
import datetime

# Région mis en paramètre afin d'avoir des adresses françaises
fake = Faker("fr_Fr")

# Générer un nombre à 14 chiffres pour le numéro de sécurité social
def random_social(social=1):    
    while len(str(social)) < 14:
        social = social * 10 + random.randint(1, 10)    
    return social

ids_list = list(range(1, 69))
routes_ids = list(range(1, 11))

list_planes = [("850", "'A320'"), ("850", "'A380'"), ("850", "'A663'"),
              ("850", "'A852'"), ("850", "'B545'"), ("850", "'A538'"),
              ("850", "'A234'"), ("850", "'B534'"), ("850", "'A273'"),
              ("850", "'B333'"), ("850", "'B234'"), ("850", "'A204'"),
              ("850", "'B634'"), ("850", "'B534'"), ("850", "'A432'")]
list_departures = ["'Bordeaux'", "'Paris'", "'Lyon'", "'Toulouse'", "'Nice'"]
list_arrivals = ["'Tokyo'", "'Marrakech'", "'Los Angeles'", "'Madrid'", "'Istanbul'"]
list_arrivals2 = ["Tokyo", "Marrakech", "Los Angeles", "Madrid", "Istanbul"]



# Remplissage des tables
# Table employees
employees = ["(" + ", ".join([str(random.randint(3000, 15000)),
    str(random_social()), "\""+names.get_last_name()+"\"",
    "\""+names.get_first_name()+"\"", "\""+fake.address()+ " " +random.choice(list_arrivals2)+"\""])+")" for i in
    ids_list]

# Table pilote
pilote = []
for i in range(len(ids_list)//5):
    var = random.choice(ids_list)
    ids_list.remove(var)
    pilote.append("( " + ", ".join(["\""+(datetime.datetime(2020, 1, 1,00,00)
        + datetime.timedelta(weeks=random.randrange(900))).strftime('%Y-%m-%d')+"\"",
        "\""+(datetime.datetime.now()
        +  datetime.timedelta(hours=random.randrange(666))).strftime('%H:%M:%S')+"\"",
        str(var)]) + ")")

# Table cabincrew
cabincrew = []
for i in range(len(ids_list)//2):
    var = random.choice(ids_list)
    ids_list.remove(var)
    cabincrew.append("(" + ", ".join(["\""+(datetime.datetime.now()
        + datetime.timedelta(hours=random.randrange(666))).strftime('%H:%M:%S')+"\"",
        random.choice(("'hostess'", "'steward'")), str(var)]) + ")")

# Table aircraft
aircraft = ["(" + ", ".join(random.choice(list_planes)) + ")" for _ in
        range(15)]

# Table route
route = ["(" + ", ".join([random.choice(list_departures), random.choice(list_arrivals)]) + ")" for _ in
        range(50)]

# Table departures
departures = []
ids_pilotes = list(range(1, len(pilote)))
aircrews_lists = list(range(1, len(cabincrew)))
for i in range(30):    
    pilote_id = random.choice(ids_pilotes)
    copilote_id = random.choice(ids_pilotes)    
    aircrew = ""
    for _ in range(random.randint(1, 4)):
        aircrew_id = random.choice(aircrews_lists)
        aircrew += ", " + str(aircrew_id)
    free_place = random.randint(1, 300)
    occupied = 850 - free_place
    departures.append("("+", ".join(["\""+(datetime.date(2021,
        3,23)+datetime.timedelta(weeks=random.randrange(666))).strftime("%Y-%m-%d")+"\"",str(pilote_id),
        str(copilote_id), str(aircrew_id), str(free_place), str(occupied)])+")")

# Table flight
fligth = []
departures_ids = list(range(1, len(departures)))
id_routes = list(range(1, len(route)))
id_devices = list(range(1, len(aircraft)))
for i in range(29):
    departure_id = random.choice(departures_ids)
    route_id = random.choice(id_routes)
    device_id = random.choice(id_devices)

    departures_ids.remove(departure_id)
    id_routes.remove(route_id)

    fligth.append("("+", ".join([str(departure_id),"\""+(datetime.datetime.now()).strftime("%Y-%m-%d")+"\"", "\""+(datetime.datetime.now()
        + datetime.timedelta(weeks=random.randrange(666))).strftime("%Y-%m-%d")+"\"",
        str(route_id), str(device_id)])+ ")")

# Table ticket
ticket = []
departures_ids= list(range(1, len(departures)))

for i in range(500):
    depare_id = random.choice(departures_ids)

    ticket.append("(" + ", ".join(["\""+(datetime.datetime.now()+
        datetime.timedelta(weeks=random.randrange(666))).strftime("%Y-%m-%d")+"\"",
        str(random.randint(30, 200)), str(depare_id)])+")")

# Table passenger
passenger = []
tickets_ids = list(range(1, len(ticket)))
while len(tickets_ids) > 0:
    passenger_info = ", ".join(["\""+names.get_last_name()+"\"",
        "\""+names.get_first_name()+"\"",
        "\""+fake.address()+"\"", 
        "\""+fake.job()+"\"",
        "\""+fake.iban()+"\""])
    tickets = random.randint(0, 4)
    if len(tickets_ids) < tickets:
        tickets = len(tickets_ids)
    for _ in range(tickets):
        ticket_id = random.choice(tickets_ids)
        tickets_ids.remove(ticket_id)
        passenger.append("(" + passenger_info +", " +str(ticket_id)+")")



# Connexion à la base de données
connection = pymysql.connect(host="127.0.0.1", user="root", password="", database="aircraft")
cursor = connection.cursor()
cursor.execute("SET GLOBAL FOREIGN_KEY_CHECKS=0;")
connection.commit()

# Insérer les différentes valeurs des tables dans la base de données dans de requêtes MySQL
Employee_query = "INSERT INTO `employees`(`salary`, `social_security`, `name`, `first_name`, `address`) VALUES "+ ",\n".join(employees)
Pilote_query = "INSERT INTO `pilote` (`license`, `among`, `staff_id`) VALUES " + ",\n".join(pilote)
Cabincrew =  "INSERT INTO `cabincrew`(`among`, `fonction`, `staff_id`)  VALUES"+",\n".join(cabincrew)
Aircraft = "INSERT INTO `device`(`capacity`, `type`) VALUES " + ",\n".join(aircraft)
Route = "INSERT INTO `route`(`origin`, `arrival`) VALUES " + ",\n".join(route)
Departures = "INSERT INTO `departures`(`date`, `pilote`, `copilote`, `aircrew`,`free_places`, `occupied`) VALUES " + ",\n".join(departures) 
Fligth = "INSERT INTO `flight`(`id_departures`, `validity_start`, `validity_end`, `id_route`,`id_device`) VALUES " + ", \n".join(fligth)
Ticket = "INSERT INTO `tickets`(`issue_date`, `price`, `departures_id`) VALUES " + ", \n".join(ticket)
Passenger = "INSERT INTO `passenger`(`name`, `first_name`, `address`, `profession`, `bank`, `ticket_id`) VALUES " + ", \n".join(passenger)

# Exécuter les différentes requêtes
cursor.execute(Employee_query)
cursor.execute(Pilote_query)
cursor.execute(Cabincrew)
cursor.execute(Aircraft)
cursor.execute(Route)
cursor.execute(Fligth)
cursor.execute(Departures)
cursor.execute(Ticket)
cursor.execute(Passenger)

connection.commit()
connection.close()


print("Les tables se sont remplies avec succès")
