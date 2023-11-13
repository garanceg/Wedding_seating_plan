import numpy as np
from gurobipy import GRB, quicksum
import gurobipy
from peewee import *
from abc import abstractmethod

from profil import db, Orga, Tables, Guest, Player

db.connect()
db.create_tables([Guest, Player, Orga, Tables])

class Table:
    """
    This class represents a table in the wedding.

    :param capacity: the capacity of a table
    :type capacity: int
    :param id:
    :type id: int
    :param mariage: name of the wedding
    :type mariage: char
    """
    def __init__(self, id, capacity, mariage):
        self.C = capacity
        self.id = id
        self.nb_free_seats = self.C
        self.guests_list = []
        self.mariage = mariage
        self.pt = []


    def add_guest(self, i):
        """
        This function 'add_guest' adds the guest i to the table. It checks if the table max capacity isn't reached.
        If there is no seat left, then it raises an OverflowError. It updates the number of free seats left.

        :param i: id of the guest to add to the table
        :type i: int
        :return: None
        :rtype: None
        """
        if self.nb_free_seats == 0:
            raise OverflowError("Maximum capacity for table "+str(self.id)+" reached !")
        self.guests_list.append(i)
        self.nb_free_seats -= 1


    def remove_guest(self, i):
        """
        This function 'remove_guest' removes the guest i from the table. It checks if the table isn't empty initially and if the
        guest to remove is at this table initially. It updates the number of free seats left.

        :param i: id of the guest to remove from the table
        :type i: int
        :return: None
        :rtype: None
        """
        if self.nb_free_seats == self.C:
            raise ValueError("Table "+str(self.id)+" is already empty !")
        if i not in self.guests_list:
            raise ValueError("Guest "+i+" cannot be remove as "+i+" not at table "+str(self.id)+".")
        self.guests_list.remove(i)
        self.nb_free_seats += 1


class Event:
    """
    This class creates the tables of the wedding according to the number of tables of each capacity available for the event.
    It contains a list of the capacity of each table and a list containing all the instances tables of the event.

    :param mariage: name of the wedding
    :type mariage: char
    """
    def __init__(self, mariage):
        self.mariage = mariage
        self.table_capacity_list = []
        self.nb_seats = 0
        query = Tables.select().where(Tables.mariage == self.mariage)
        for table in query:
            for i in range (int(table.number)):
                self.table_capacity_list.append(table.capacity)
                self.nb_seats += table.capacity

        self.table_list = []
        for (i, x) in enumerate(self.table_capacity_list):
            self.table_list.append(Table(i, x, mariage))


class Abstract_solver():
    """
    This class contains all the methods needed to use the MILP solver.

    :param event: event on which we want to generate a table plan
    :type event: instance
    :param mariage: name of the wedding
    :type mariage: char
    """
    def __init__(self, event, mariage):
        self.nb_table = len(event.table_list)
        self.table_list = event.table_list
        self.nb_seats = event.nb_seats
        self.table_guest = [] # seating plan is empty at the beginning
        self.mariage = mariage


    def player_list_ident(self):
        """
        This function returns a list of the players attended to the wedding.

        :return: the id of the players attended to the wedding that we need to place on the tables.
        :rtype: list
        """
        L_id = []
        query = Player.select().where(Player.mariage == self.mariage)
        for player in query:
            L_id.append(player.id)
        return L_id


    def couple_matrix(self):
        """
        This function returns the couple matrix containing 1 on line i column j if i is in couple with j.

        :return: matrix of the couples
        :rtype: array
        """
        player_ident = self.player_list_ident()
        nb_player = len(self.player_list_ident())
        matrix = np.zeros((nb_player,nb_player))

        query = Player.select().where(
            (Player.couple_situation == 1) & (Player.mariage == self.mariage)
            )
        for player in query:
            partner = Guest.get(Guest.id == player.partner_name) # player's partner is partner (in guest because maybe the partner has not filled the form yet)
            if partner.id in player_ident:
                # filling the matrix
                i = player_ident.index(player.id)
                j = player_ident.index(partner.id)
                matrix[i][j] = 1
                matrix[j][i] = 1
        return matrix

    def favorite_guest_matrix(self):
        """
        This function returns the choices matrix containing 1, 2 or 3 on line i column j if guest i wants to be placed with
        guest j with a preference of 3, 2 or 1.

        :return: matrix of the choices
        :rtype: array
        """
        player_ident = self.player_list_ident()
        nb_player = len(self.player_list_ident())
        matrix = np.zeros((nb_player,nb_player))
        query = Player.select().where(Player.mariage == self.mariage)
        for player in query:
            if (player.favorite_guest_1) > 0 and (player.favorite_guest_1) in player_ident:
                matrix[player_ident.index(player.id)][player_ident.index(player.favorite_guest_1)] = 3
            if (player.favorite_guest_2) > 0 and (player.favorite_guest_2) in player_ident:
                matrix[player_ident.index(player.id)][player_ident.index((player.favorite_guest_2))] = 2
            if (player.favorite_guest_3) > 0 and (player.favorite_guest_3) in player_ident:
                matrix[player_ident.index(player.id)][player_ident.index((player.favorite_guest_3))] = 1
        return matrix


    def gender_list(self):
        """
        This function returns the gender of the players attended to the wedding.

        :return: list of the gender of the players
        :rtype: list
        """
        player_ident = self.player_list_ident()
        list = []
        for ident in player_ident:
            player = Player.get(Player.id == ident)
            list.append(player.gender)
        return list

    def family_list(self):
        """
        This function returns whether the groom or thr bride invited the player attended to the wedding.

        :return: list of who invited each players
        :rtype: list
        """
        player_ident = self.player_list_ident()
        list = []
        for ident in player_ident:
            player = Player.get(Player.id == ident)
            list.append(player.family)
        return list


    @abstractmethod
    def seating_plan(self):
        pass


class Random_solver(Abstract_solver):
    """
    This class generates a seating plan randomly without constraints. It inherits from the class Abstract_solver.

    :param event: event on which we will generate the seating plan
    :type event: instance
    :param mariage: name of the wedding
    :type mariage: char

    """

    def __init__(self, event, mariage):
        super().__init__(event, mariage)

    def seating_plan(self):
        """
        This method generates a random seating plan for the event.

        :return: list of list of guests placed on each table.
        :rtype: list
        """

        while len(self.guest_to_seat) > 0:
            x = self.guest_to_seat.pop()

            for t in self.table_list:
                if t.nb_free_seats > 0:
                    t.add_guest(x)
                    break

        for t in self.table_list:
            self.table_guest.append(t.guests_list)

        return [1, self.table_guest]


class PLNE_solver(Abstract_solver):
    """
    This class generates the seating plan with respect to the constraints of gender parity, equilibrium between the families of
    origin, of couples, of seating preferences.

    :param event: event on which we will generate the seating plan
    :type event: instance
    :param mariage: name of the wedding
    :type mariage: char
    """

    def __init__(self, event, mariage):
        super().__init__(event, mariage)
        self.player_list = self.player_list_ident()
        self.nb_guest = len(self.player_list_ident())
        self.couple = self.couple_matrix()
        self.choice = self.favorite_guest_matrix()
        self.gender = self.gender_list()
        self.family = self.family_list()


    def seating_plan(self):
        """
        The method "seating_plan" uses gurobi solver to execute the MILP in order to generate the table seating plan from the event.

        :return: the optimum solution of the MILP with the name of the players placed on each table of the wedding.
        :rtype: list
        """

        ## first, we try if the model is feasible or not :
        if self.nb_guest > self.nb_seats:
            return [0, [self.nb_guest, self.nb_seats]]

        m = gurobipy.Model();
        x = {}
        y = {}
        z = {}

        m.setParam('MIPGap', 0.0045)

        #creation of the variables
        for i in self.player_list:
            for k in range(self.nb_table):
                # x[i, k] = 1 if guest i is at table k
                x[i, k]=m.addVar(name="x"+str(i)+","+str(k), vtype = GRB.INTEGER, lb=0, ub = 1)
                for j in self.player_list:
                    # y[i, j, k]= 1 if guest i and j are in a couple and both at table k
                    y[i, j, k]=m.addVar(vtype = GRB.INTEGER, name="y"+str(i)+str(j)+str(k), lb=0, ub = 1)
                    # z[i, j, k] = 1 2 or 3 if guest i wanted to be a the same table as guest j with preference 3 2 or 1 and i and j are table k
                    z[i, j, k]=m.addVar(vtype = GRB.INTEGER, name="z"+str(i)+str(j)+str(k), lb=0, ub = 3)
                

        # objective function
        m.setObjective(quicksum(z[i, j, k] + 20*y[i, j, k] for i in self.player_list for j in self.player_list for k in range(self.nb_table)), GRB.MAXIMIZE)

        # constraint : each guest is at one table
        for i in self.player_list:
            m.addConstr(quicksum(x[i, k] for k in range(self.nb_table))==1)

        #constraints of mixing gender and mixing families
        for k in range(self.nb_table): 
            p = self.nb_guest / self.table_list[k].C
            m.addConstr(quicksum(x[i, k] for i in self.player_list) <= self.table_list[k].C)
            m.addConstr(quicksum(p*x[self.player_list[i], k]*self.gender[i] for i in range(self.nb_guest)) <= 2*p + quicksum(self.gender[i] for i in range(self.nb_guest)))
            m.addConstr(quicksum(p*x[self.player_list[i], k]*self.gender[i] for i in range(self.nb_guest)) >= - 2*p + quicksum(self.gender[i] for i in range(self.nb_guest)))
            m.addConstr(quicksum(p*x[self.player_list[i], k]*self.family[i] for i in range(self.nb_guest)) <= 2*p + quicksum(self.family[i] for i in range(self.nb_guest)))
            m.addConstr(quicksum(p*x[self.player_list[i], k]*self.family[i] for i in range(self.nb_guest)) >= - 2*p + quicksum(self.family[i] for i in range(self.nb_guest)))
            
        #constraints of putting couple and favorite guests together
        for i in range(self.nb_guest):
            for j in range(self.nb_guest):
                if i != j:
                    for k in range(self.nb_table):
                        m.addConstr(y[self.player_list[i], self.player_list[j], k] <= (1/2)*(x[self.player_list[i], k]+x[self.player_list[j], k])*abs(self.couple[i][j]))
                        m.addConstr(z[self.player_list[i], self.player_list[j], k] <= (1/2)*(x[self.player_list[i], k]+x[self.player_list[j], k])*abs(self.choice[i][j]))
                        
        m.optimize()

        for v in x.values() :
            if v.X == 1:
                lettre = v.VarName
                l = lettre[1:lettre.find(',')]
                for k in range(self.nb_table):
                    if int(lettre[lettre.find(',')+1:]) == k:
                        for i in self.player_list:
                            if int(lettre[1:lettre.find(',')])==i:
                                guest = Guest.get(Guest.id == i)
                                self.table_list[k].add_guest(str(guest.name + ' ' + guest.surname))
                                player = Player.get(Player.id == i)
                                player.table = k
                                player.save()

        for k in range(self.nb_table):
            self.table_guest.append(self.table_list[k].guests_list)

        return [1, self.table_guest]


db.close()
