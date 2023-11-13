import unittest
import pytest
import sys
import numpy as np
sys.path.append("src")
from RO import Table, Event, Abstract_solver, PLNE_solver
from create_wed import CreateMariage
from profil import db, Player, Guest, Orga, Tables

db.connect() #connecting to the database
db.create_tables([Guest, Player, Orga, Tables]) #creating the tables

class TestTable(unittest.TestCase): 
    def test_add_guest(self):
        table = Table(1, 4, 'A')
        table.add_guest(1)
        table.add_guest(2)
        self.assertEqual(table.guests_list, [1, 2])
        self.assertEqual(table.nb_free_seats, 2)

        with self.assertRaises(OverflowError):
            table.add_guest(3)
            table.add_guest(4)
            table.add_guest(5)

    def test_remove_guest(self):
        table = Table(1, 4, 'A')
        with self.assertRaises(ValueError):
            table.remove_guest(1)

        table.add_guest(1)
        table.remove_guest(1)
        self.assertEqual(table.guests_list, [])
        self.assertEqual(table.nb_free_seats, 4)

        with self.assertRaises(ValueError):
            table.remove_guest(2)



#tests fonctionnels:

def test_add_guest_well_added():          #vérifie que add_guest ajoute bien le nouvel invité à la fin de la guests_list
    table = Table(1, 7, "mariage")
    table.guests_list = ["Lucas", "Nicolas", "Garance"]
    table.add_guest("Pilou")
    assert table.guests_list[-1] == "Pilou"

def test_add_guest_max_capacity():      #vérifie que si la capcité de la table est atteinte on ne peut rajouter qqn à cette table
    table = Table(1, 6, "mariage")
    with pytest.raises(OverflowError):
        for i in range(7):
            table.add_guest(str(i))

def test_remove_guest_well_removed():   #vérifie que si on retire un guest de la table il est bien retiré
    table = Table(1, 6, "mariage")
    table.add_guest("Lucas")
    table.add_guest("Nicolas")
    table.add_guest("Garance")
    table.remove_guest("Garance")
    for k in range(len(table.guests_list)):
        assert table.guests_list[k] != "Garance"

def test_remove_guest_not_in_guest_list():      #vérifie que renvoie une erreur si on veut remove un guest qui n'est pas à la table
    table = Table(1, 6, "mariage")
    with pytest.raises(ValueError):
        table.add_guest("Lucas")
        table.add_guest("Pilou")
        table.remove_guest("Garance")
    

def test_remove_guest_already_empty():      #vérifie que renvoie une erreur si on remove un guest alors que la table est vide 
    table = Table(1, 6, "mariage")
    with pytest.raises(ValueError):
        table.add_guest("Lucas")
        table.add_guest("Pilou")
        table.remove_guest("Lucas")
        table.remove_guest("Pilou")
        table.remove_guest("Garance")
    
# Verifie que les contraintes du PLNE sont bien respectées 
def test_seating_plan():
    mar_name = 'test_seating_plan'
    nb_table = 3
    table_capacity = 6
    nb_couple = 3
    nb_guest = 18
    prop = nb_guest/table_capacity
    mar = CreateMariage(nb_guest, [[nb_table,table_capacity]], mar_name, nb_couple)
    mar.create_player()
    mar.create_tables()
    event = Event(mar_name)
    P = PLNE_solver(event, mar_name)
    PLNE = P.seating_plan()
    feasibility, repartition = PLNE[0], PLNE[1]
    assert(feasibility == 1)
    # assert (len(repartition) == nb_table)
    ## creating the matrices of the MILP : 
    x = np.zeros((nb_guest, nb_table)) # x(i,j) = 1 if i at table k
    y = np.zeros((nb_guest, nb_guest, nb_table)) # y(i,j,k) = 1 if i and j at table k  are in a couple
    z = np.zeros((nb_guest, nb_guest, nb_table)) # z(i,j,k) = 1 if i and j at same table k are in a couple
    query = Player.select().where(Player.mariage == mar_name)

    abs = Abstract_solver(event, mar_name)
    player_ident = abs.player_list_ident()
    
    for player in query:
        x[player_ident.index(player.id), player.table] = 1
        print(player_ident.index(player.id))

    # print(x)
    for player_y_1 in query:
        for player_y_2 in query:
            for k in range(3):
                if player_y_1.partner_name == player_y_2.id and player_y_1.table == k and player_y_2.table == k:
                    y[player_ident.index(player_y_1.id), player_ident.index(player_y_2.id), k] = 1
    # print(y)
    for player_z_1 in query:
        for player_z_2 in query:
            for k in range(3):
                if player_z_1.favorite_guest_1 == player_z_2.id and player_z_1.table == k and player_z_2.table == k: 
                    z[player_ident.index(player_z_1.id), player_ident.index(player_z_1.id), k] = 3
                if player_z_1.favorite_guest_2 == player_z_2.id and player_z_1.table == k and player_z_2.table == k: 
                    z[player_ident.index(player_z_1.id), player_ident.index(player_z_1.id), k] = 2
                if player_z_1.favorite_guest_3 == player_z_2.id and player_z_1.table == k and player_z_2.table == k: 
                    z[player_ident.index(player_z_1.id), player_ident.index(player_z_1.id), k] = 1

    couple_matrix = abs.couple_matrix()

    fav_guest_matrix = abs.favorite_guest_matrix()
    gender_list = abs.gender_list()
    family_list = abs.family_list()

    ## contrainte (1)
    for i in range (nb_guest):
        assert (sum(x[i,:]) == 1)
    ## contrainte (2)
    for k in range(nb_table):
        assert (sum(x[:, k]) <= table_capacity)

    ## contrainte (3), (4), (5), et (6)
    for k in range (nb_table):
        # contrainte (3) et (4)
        assert ( sum(prop*x[:,k][i]*gender_list[i] for i in range(nb_guest)) <= 2*prop + sum(gender_list))
        assert ( sum(prop*x[:,k][i]*gender_list[i] for i in range(nb_guest)) >= -2*prop + sum(gender_list))
        #contrainte (5) et (6)
        assert ( sum(prop*x[:,k][i]*family_list[i] for i in range(nb_guest)) <= 2*prop + sum(family_list))
        assert ( sum(prop*x[:,k][i]*family_list[i] for i in range(nb_guest)) >= -2*prop + sum(family_list))
   
    ## contraint (7):
    for i in range(nb_guest):
        for j in range (nb_guest):
            if i != j:
                for k in range (nb_table):
                    assert (y[player_ident[i]-1,player_ident[j]-1,k] <= (x[player_ident[i]-1,k] + x[player_ident[j]-1,k])*couple_matrix[i,j]/2)
                    assert (z[player_ident[i]-1,player_ident[j]-1,k] <= (x[player_ident[i]-1,k] + x[player_ident[j]-1,k])*fav_guest_matrix[i,j]/2)

    
    mar.delete_mar()


db.close()



    
    



