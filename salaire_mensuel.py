# brief: Calcul salaire mensuel

#import du JSON
import json
with open('employes-data.json', 'r') as fichier:
    donnees = json.load(fichier)



def branch_data_extract() -> list:
    """
    extrait les données du JSON par branche.

    [Args]
    Pas de données, fonctionne directement sur l'import JSON nommé donnees

    """
    branch_list = [key for key in donnees.keys()] #extraction des noms de filiale du json
    #retourne la liste des 3 filiales

    workers_list = [] #extraction des noms du personnel et ajout du nom de la filiale dans chaque dictionnaire

    for branch in branch_list:
        for key in donnees[branch]:
            key["Filiale"]=str(branch)
            workers_list.append(key)
    #retourne une liste avec des dictionnaires par employés contenant les infos personnelles plus le nom de la filiale
    return(workers_list)

workers_list = branch_data_extract()

#calcul salaire mensuel
def worker_name_and_salary_function(data: list) -> list:
    """
    Prend la liste workers_list et calcule le salaire en fonction des nombres d'heures, contrat et salaire horaire

    [Args]
    data (list): Liste avec des dictionnaires par employés contenant les infos personnelles plus la filiale

    """
    worker_name_and_salary = []
    for worker in data:
        name = worker['name']
        hourly_rate = worker['hourly_rate']
        worked_hours = worker["weekly_hours_worked"]
        contract_hours = worker["contract_hours"]
        if worked_hours > contract_hours:
            salary = (contract_hours * hourly_rate + (worked_hours-contract_hours)*hourly_rate*1.5)*4
        else:
            salary = worked_hours * hourly_rate *4
        worker_name_and_salary.append((name,worker['job'],salary,worker['Filiale']))
    #sort une liste avec des tuples contenant le nom, le job, le salaire et la filiale
    return(worker_name_and_salary)

worker_name_and_salary_list = worker_name_and_salary_function(workers_list)


def average_salary(data: list) -> list:
    """
    Prend la liste worker_name_and_salary_list et calcule les stats salariales sur tout le personnel

    [Args]
    data (list): Liste avec des tuples contenant le nom, le job, le salaire et la filiale 

    Sort une liste avec le salaire moyen de l'entreprise, le salaire max et le salaire min
    """
    salary_list = []
    for salary in data:
        salary_list.append(salary[2])
    average_sal = sum(salary_list)/len(salary_list)
    max_salary = max(salary_list)
    min_salary = min(salary_list)
    return(average_sal, max_salary, min_salary)

average_salary_company_list = average_salary(worker_name_and_salary_list)

def branch_average_salary(data: list) -> list: #worker name and salary list
    """
    Prend la liste worker_name_and_salary_list et calcule les stats salariales par filiale

    [Args]
    data (list): Liste avec des tuples contenant le nom, le job, le salaire et la filiale 

    Sort une liste avec pour chaque filiale, le salaire moyen, le salaire max et le salaire min
    """
    branch_list = [] #extraction des noms de filiale du json
    for key in donnees.keys():
        branch_list.append(key)

    salary_list_by_branch = []
    for branch in branch_list:
        somme = 0
        effectif = 0
        max = 0
        min = data[0][2]
        for key in data: #key est un tuple composé du nom, du job, le salaire et la filiale
            if key[3] == branch:
                somme+= key[2]
                effectif +=1
                if key[2]>max:
                     max = key[2]
                if key[2]<min:
                    min = key[2]
        salary_list_by_branch.append((branch,max, min, round(somme/effectif,1))) #liste avec des tuples contenant le nom de la filière, le salaire max, min et moyen)
    return(salary_list_by_branch)



branch_average_salary_list = branch_average_salary(worker_name_and_salary_list)

# -------------fonctions d'affichage



def affichage_stat_salariales():
    """
    Fonction d'affichage qui  imprime les données de average_salary_company_list
    [Args]
    aucun    

    """
    liste_stat_compagnie = average_salary_company_list
    print(f"\n\nDans l'entreprise Big CORP:\n\n\
        le salaire moyen est de {liste_stat_compagnie[0]},\n\
        le salaire maximal est de {liste_stat_compagnie[1]},\n\
        le salaire minimal est de {liste_stat_compagnie[2]}\n\n\n")

affichage_stat_salariales()

def affichage_stat_salariale_filiale():
    """
    Fonction d'affichage qui  imprime les données de branch_average_salary_list après un input de la filiale souhaitée
    [Args]
    aucun    

    """
    wished_branch = input("Inscrivez le nom de la filiale dont vous souhaitez obtenir les statistiques salariales\n\
TechCorp, DesignWorks ou ProjectLead \nExit pour sortir : ")
    if wished_branch in donnees.keys():
        print(f"\n\n !!! Attention données confidentielles !!! \n\nFiliale: {wished_branch}\n")
        liste_de_la_filiale = []
        for worker in worker_name_and_salary_list:
            if wished_branch == worker[3]:
            # print(f"{worker[0]:<15}|{worker[1]:<15}|Salaire mensuel : {round(float(worker[2]),2)}€")
                liste_de_la_filiale.append(worker)
        liste_de_la_filiale.sort(key=lambda x: x[2], reverse=1)
        for worker in liste_de_la_filiale:
            print(f"{worker[0]:<15}|{worker[1]:<15}|Salaire mensuel : {round(float(worker[2]),2)}€")
        for data in branch_average_salary_list:
            if data[0] == wished_branch:
                average_salary = data[3]
                max_salary = data[1]
                min_salary = data[2]
        print("============================================================\n")
        print(f"Statistiques des salaires pour la filiale {wished_branch}\n\
            Salaire moyen: {average_salary} €\n\
            Salaire le plus élevé: {max_salary} €\n\
            Salaire le moins élevé: {min_salary} €\n")
        print("============================================================\n")
        affichage_stat_salariale_filiale()
    elif wished_branch == "Exit":
        return
    else:
        print("Cette entrée n'est pas valable")
        affichage_stat_salariale_filiale()



affichage_stat_salariale_filiale()


import csv

with open('brief1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["Name", "Job", "Salary", "Filiale"]

    writer.writerow(field)
    for element in worker_name_and_salary_list:
        writer.writerow(element)

    writer.writerow("")
    writer.writerow("")
    writer.writerow("")

    branche_list = ["branch","max", "min", "average"]
    writer.writerow(branche_list)
    for element in branch_average_salary_list :
        writer.writerow(element)

    
