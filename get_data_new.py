import sqlite3
import datetime
import argparse
import json

parser = argparse.ArgumentParser(description='Script so useful.')
parser.add_argument("--dbfile", type=str, default='C:\\work\\zoe-ha\\home-assistant_v2.db')
parser.add_argument("--days", type=int, default=7)
parser.add_argument("--battery_kwh", type=int, default=40)
parser.add_argument("--pret", type=float, default=0.8*1.21)


args = parser.parse_args()

dbfile = args.dbfile
days = args.days
pret = args.pret
battery_kwh = args.battery_kwh

response_json = "{"


connexiune = sqlite3.connect(dbfile)

gogo = connexiune.cursor()

# setam delta pentru data
data_zile=datetime.datetime.now() + datetime.timedelta(-days)

inceput= datetime.datetime.now()
#print(inceput)
#luam datele despre baterie din baza de date
SELECT_baterie = "SELECT  last_updated, state FROM states WHERE entity_id='sensor.battery_level' AND state!='unavailable' AND last_updated >  '"+  str(data_zile)+"'"
date_batierie = [a for a  in gogo.execute(SELECT_baterie)]
#print(date_batierie[0])

#luam datele despre rulaj din baza de date
SELECT_mileage = "SELECT  last_updated, state FROM states WHERE entity_id='sensor.mileage' AND state!='unavailable' AND last_updated >  '"+  str(data_zile)+"'"
date_mileage = [a for a  in gogo.execute(SELECT_mileage)]
#print(date_mileage[0])

#luam datele despre locatie din baza de date
SELECT_locatie = "SELECT  last_updated, state FROM states WHERE entity_id='device_tracker.location' AND last_updated >  '"+  str(data_zile)+"'"
date_locatii = dict()
for a  in gogo.execute(SELECT_locatie):
    #Pastram data fara secunde pentru optimizare
    date_locatii[(':').join(a[0].split(':')[:-1])] = a[1]

#Setam numarul de la care pornim
first = int(date_batierie[0][1])

def add_remove(perioada, nr):
    perioada = (':').join(perioada.split(':')[:-1])
    perioada = datetime.datetime.strptime(perioada, '%Y-%m-%d %H:%M')
    perioada =  perioada + datetime.timedelta(minutes=nr)
    return str(perioada)




def este_acasa(la_data):

    for i in range(-3,2):
        try:
            print(date_locatii[(':').join(add_remove(la_data,i).split(':')[:-1])])
            if (date_locatii[(':').join(add_remove(la_data,i).split(':')[:-1])] == 'Home'):
                return True
        except:
            continue

    return False

#Setam consumul initial
incarcat_acasa = 0 
incarcat_in_deplasare = 0
for x,y in date_batierie:
    #print(x,y)
    if(first < int(y)):
        if ( int(y) > first):
            if(este_acasa(str(x))):
                incarcat_acasa +=  int(y) - first
            else:
                incarcat_in_deplasare +=  int(y) - first

        first = int(y)        
    else:
        if(first > int(y)):
            first = int(y)   

first = int(date_batierie[0][1])
consum = 0
# Cat am consumat?
for x,y in date_batierie:
    if(first < int(y)):
        consum +=  int(y) - first
        first = int(y)
    else:
        first = int(y)

consum = consum/100*battery_kwh

# cat am mers?
km_parcursi =  int(date_mileage[-1][1]) - int(date_mileage[0][1])

kw_km = consum*100/km_parcursi

# Inlocuim incarcat de acasa
incarcat = incarcat_acasa
kw_din_procente = incarcat/100*battery_kwh

# print("KW incarcati: " + str(round(kw_din_procente,2)))

# Adaugam kw
response_json += '"kw_'+str(days) + '" : ' + str(round(kw_din_procente,2)) + ','

response_json += '"bani_'+str(days) + '" : ' +str(round(kw_din_procente*pret,2)) + ','


# Inlocuim incarcat in deplasare
incarcat = incarcat_in_deplasare
kw_din_procente = incarcat/100*battery_kwh

response_json += '"kw_deplasare_'+str(days) + '" : ' +str(round(kw_din_procente,2)) + ','

#response_json += '"bani_deplasare_'+str(days) + '" : ' +str(round(kw_din_procente*pret,2)) + ','

response_json += '"km_parcursi_'+str(days) + '" : ' +str(km_parcursi) + ','

response_json += '"consum_kw_'+str(days) + '" : ' + str(round(consum,2)) + ','

response_json += '"consum_kw_km_'+str(days) + '" : ' + str(round(kw_km,2))



response_json += "}"

print (response_json)

#print (datetime.datetime.now())
#print (datetime.datetime.now() + datetime.timedelta(-days))



connexiune.close()

diferenta= datetime.datetime.now() - inceput
#print(diferenta)