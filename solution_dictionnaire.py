import json
with open('employes-data.json', 'r') as fichier:
    donnees = json.load(fichier)

branch_list = [key for key in donnees.keys()] #extraction des noms de filiale du json
    #retourne la liste des 3 filiales

workers_list = [] #extraction des noms du personnel et ajout du nom de la filiale dans chaque dictionnaire

for branch in branch_list:
    for key in donnees[branch]:
        key["Filiale"]=str(branch)
        workers_list.append(key)



for element in workers_list:
    if element['weekly_hours_worked'] > element['contract_hours']:
        element['salary']=(element['contract_hours']*element["hourly_rate"]+(element["weekly_hours_worked"]-element["contract_hours"])*element["hourly_rate"]*1.5)*4
    else:
        element['salary']=element["weekly_hours_worked"]*element["hourly_rate"]*4

somme = 0
for element in workers_list:
    somme += element['salary']

def stats_globales():
    # somme = 0
    somme = sum(workers_list, lambda element: element['salary'])
    # somme = [somme+=element['salary'] for element in workers_list]
    # for element in workers_list:
    #     somme += element['salary']
    min_global_salary = workers_list[0]['salary']
    max_global_salary = 0
    for element in workers_list:
        if element['salary'] > max_global_salary:
            max_global_salary = element['salary']
        if element['salary'] < min_global_salary:
            min_global_salary = element['salary']
    return(somme/len(workers_list), max_global_salary, min_global_salary)

# def stats_filiales():




# #if worked_hours > contract_hours:
#             salary = (contract_hours * hourly_rate + (worked_hours-contract_hours)*hourly_rate*1.5)*4
#         else:
#             salary = worked_hours * hourly_rate *4