import random
from faker import Faker
from string import ascii_lowercase  # to create the passwords

from profil import db, Guest, Player,Orga, Tables

db.connect()  # connecting to data base
db.create_tables([Guest, Player, Orga, Tables])  #creating the tables to fill them

fake = Faker()  #library of name, surname... to generate fake guests


class CreateMariage:
    """
    This class allows the user to generate a random wedding .

    :param nb_guest: the number of guest wanted for this random wedding
    :type nb_guest: int
    :param nb_capa_table: list of list of number of tables of a certain capacity : nb_table[i] = [n,m] : n tables of capacity m 
    :type nb_capa_table: list
    :param mariage_name: the name of the wedding
    :type mariage_name: str
    :param nb_couple: the number of couples of this wedding
    :type nb_couple: int 

    :ivar nb_guest: the number of guest wanted for this random wedding
    :type nb_guest: int
    :ivar nb_capa_table: list of list of number of tables of a certain capacity : nb_table[i] = [n,m] : n tables of capacity m 
    :type nb_capa_table: list
    :ivar  mariage_name: the name of the wedding
    :type mariage_name: str
    :ivar nb_couple: the number of couples of this wedding
    :type nb_couple: int 
    :ivar gender_guest: list of the gender of the guest : gender[i] = gender of guest i
    :type gender_list: list
    :ivar ident_guest: list of id of the guest of this wedding
    :type ident_guets: list  

    """
    def __init__(self,nb_guest, nb_table_capa, mariage_name, nb_couple):
        self.nb_guest = nb_guest
        self.nb_table_capa = nb_table_capa  # list : nb_table[i] = [n,m] : n tables de capacite m 
        self.mariage_name = mariage_name
        self.nb_couple = nb_couple
        self.gender_guest = []
        self.ident_guest = []
        for i in range (self.nb_guest):
            gender = random.randint(0,1)
            self.gender_guest.append(gender)
            name = fake.first_name_male() if gender==1 else fake.first_name_female()
            surname = fake.last_name()
            guest = Guest.create(
                name = name,
                surname = surname,
                email = str(name + '.' + surname + "@gmail.com"), 
                mariage = self.mariage_name
            )
            self.ident_guest.append(guest.id)
            guest.save()


    def create_player(self):
        """
        This method creates the player with random caracteristics for this random wedding.

        :return: None
        :rtype: NoneType 
        """
        # Creation of a random couple list :
        rdm_id = random.sample(range(self.ident_guest[0], self.ident_guest[-1]), 2*self.nb_couple)  # choosing id for people in a couple
        rdm_couple = []
        for i in range(0, len(rdm_id)-1, 2):
            rdm_couple.append([rdm_id[i], rdm_id[i+1]])  # couple assignement 
        
        iteration = 0
        for i in self.ident_guest:
            guest_i = Guest.get(Guest.id==i)
            partner_name = None
            couple_situation = 0
            age = random.randint(2, 70)
            family = random.randint(1, 2)
            family = random.randint(0, 1)
            rdm_fav_g = random.sample(range(self.ident_guest[0],self.ident_guest[-1]), 3)
            for couple in rdm_couple:
                if couple[0] == i:
                    couple_situation = 1
                    partner_name = couple[1]
                    age = random.randint(30, 70)
                if couple[1] == i:
                    couple_situation = 1
                    partner_name = couple[0]
                    age = random.randint(30, 70)
            password = ''.join(random.choice(ascii_lowercase) for i in range(8))  # should be a hash but too long to import and unused... 
            player_i = Player.create(
                mariage = self.mariage_name,
                id = guest_i.id,
                email = guest_i.email,
                password = password,
                age = age,
                couple_situation = couple_situation,
                partner_name = partner_name,
                gender = self.gender_guest[iteration],
                family = family,
                favorite_guest_1 = rdm_fav_g[0],
                favorite_guest_2 = rdm_fav_g[1],
                favorite_guest_3 = rdm_fav_g[2]
            )
            player_i.save()
            iteration +=1


    def create_tables(self):
        """
        This method creates the tables for this random wedding.

        :return: None
        :rtype: NoneType 
        """
        for table in self.nb_table_capa:
            table_i = Tables.create(
                mariage = self.mariage_name,
                number = table[0],
                capacity = table[1]
            )
            table_i.save()

            
    def rdm_is_not_coming(self, nb_not_coming):
        """
        This method deletes randomly a certain number of player of this random wedding.

        :param nb_not_coming: the number of guest who are not coming to the wedding
        :type nb_not_coming: int
        :return: None
        :rtype: NoneType 
        """
        
        isnt_coming = random.sample(range(self.ident_guest[0], self.ident_guest[-1]), nb_not_coming)
        for ident in isnt_coming: 
            player = Player.get(Player.id == ident)
            player.delete_instance()
    

    def first_guest_isnt_coming(self):
        player = Player.select().where(Player.mariage == self.mariage_name).order_by(Player.id).get()
        email = player.email
        player.delete_instance()
        return email
    

    def guest_not_in_couple_isnt_coming(self):
        player = Player.select().where((Player.mariage == self.mariage_name) & (Player.couple_situation == 0)).get()
        email = player.email
        player.delete_instance()
        return email
        
    
    def delete_mar(self):
        """
        This method deletes the wedding

        :return: None
        :rtype: NoneType 
        """
        query_g = Guest.select().where(Guest.mariage == self.mariage_name)
        for guest in query_g: 
            guest.delete_instance()

        query_p = Player.select().where(Player.mariage == self.mariage_name)
        for player in query_p: 
            player.delete_instance()

        query_t = Tables.select().where(Tables.mariage == self.mariage_name)
        for table in query_t: 
            table.delete_instance()


db.close()
