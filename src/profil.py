from flask import Markup
from peewee import *


db = SqliteDatabase('mariage.db')


class BaseModel(Model):
    class Meta:
        database = db 


class Orga(BaseModel):
    """ Storing infomations about the organizer of a wedding """
    id = AutoField()
    name = CharField(null = False)
    surname = CharField(null = False)
    email = CharField(null = False)
    password = CharField(null = False)
    mariage = CharField(null = False)
    groom_name = CharField(null = False)
    groom_surname = CharField(null=False)
    bride_name = CharField(null = False)
    bride_surname = CharField(null=False)
    
    def orga_full_name(self):
        """
        Get the full name of the organizer.

        :return: The player's name and surname separated by a space.
        :rtype: str
        """
        return str(self.name + ' ' + self.surname)


    def groom_full_name(self):
        """
        Get the full name of the groom.

        :return: the full name of the groom
        :rtype: string
        """
        return str(self.groom_name + ' ' + self.groom_surname)
    
    
    def bride_full_name(self):
        """
        Get the full name of the bride.

        :return: the full name of the bride
        :rtype: string
        """        
        return str(self.bride_name + ' ' + self.bride_surname)

    @classmethod
    def get_orga_mariage(cls, mariage):
        """
        Get the wedding organizer for the given marriage.

        :param mariage: name of the wedding
        :type mariage: char
        """
        try:
            orga = cls.get(cls.mariage == mariage)
        except DoesNotExist:
            return None
        return orga

    @classmethod
    def get_orga_mail(cls, mariage, email):
        """ 
        Get the wedding organizer for the given marriage and email.

        :param mariage: name of the wedding
        :type mariage: char
        :param email: email of the organizer
        :type email: char
        """
        try:
            orga = cls.get((cls.mariage == mariage) & (cls.email == email))
        except DoesNotExist:
            return None
        return orga


class Guest(BaseModel):
    """ Storing infomations about a guest of a wedding """
    id = AutoField()
    name = CharField(null = False)
    surname = CharField(null = False)
    email = CharField(null = False)
    mariage = CharField(null = False)

    def full_name(self):
        """
        Get the full name of the guest.

        :return: the full name of a wedding guest
        :rtype: string
        """        
        return str(self.name + ' ' + self.surname) 
    
    @classmethod
    def get_guest_mail(cls, mariage, email):
        """ 
        Get the corresponding guest for a given marriage and email.

        :param mariage: name of the wedding
        :type mariage: char
        :param email: email of the guest
        :type email: char
        """
        try:
            guest = cls.get(
                (cls.mariage == mariage) & (cls.email == email)
            )
        except DoesNotExist:
            return None
        return guest


class Player(BaseModel):
    """ Storing infomations about a guest who is coming to the wedding. He is called a player. """
    id = IntegerField(null = False)
    email = CharField(null = True)
    password = CharField(null = True)
    age = IntegerField(null = True)
    couple_situation = IntegerField(default=0) # 1 if in a couple, 0 otherwise
    partner_name = IntegerField(null = True)
    gender = IntegerField(null = True) # 1 if man, 0 if woman
    family = IntegerField(null = True)
    table = IntegerField(null = True)
    mariage = CharField(null=False)
    favorite_guest_1 = IntegerField(null = True)
    favorite_guest_2 = IntegerField(null = True)
    favorite_guest_3 = IntegerField(null = True)


    @classmethod
    def is_coming(cls, ident, mar):
        """Check if the player with id ident is coming to the wedding.

        :param ident: id of the player
        :type ident: int

        :return: 1 if the player is coming, 0 otherwise.
        :rtype: int
        """
        try:
            cls.select().where(
                (cls.id == ident) & (cls.mariage == mar)
                ).get()
            return 1
        except DoesNotExist:
            return 0
    

    def mr_or_miss(self):
        """Get the title according to the player's gender.
        
        :return: "Monsieur" if the player is male, "Madame" if female
        :rtype: str       
        """
        if self.gender == 0:
            return "Madame"
        else: 
            return "Monsieur"

        
    def called_gender(self):
        """Get the called gender according to the player's gender.
        
        :return: "Masculin" if the player is male, "Feminin" if female
        :rtype: str       
        """
        if self.gender == 0:
            return "Feminin"
        else:
            return "Masculin"


    def full_name(self):
        """
        Get the full name of the player.

        :return: The player's name and surname separated by a space.
        :rtype: str
        """
        guest = Guest.get(Guest.id == self.id)
        return str(guest.name + ' ' + guest.surname)


    def name_of_partner(self):
        """
        Get the full name of the player's partner.

        :return: The partner's name and surname separated by a space. "Pas en couple" if the player is not in a couple.
        :rtype: str
        """
        if self.couple_situation == 1:
            try: 
                partner = Guest.get(Guest.id == self.partner_name)
            except DoesNotExist:
                return "Pas en couple"
            return str(partner.name + ' ' + partner.surname)
        else: 
            return "Pas en couple"

    
    def name_of_fav_1(self):
        """
        Get the full name of the player's first favorite guest.

        :return: The first favorite guest's name and surname separated by a space. "Pas de personne favorite" if the player does not have a first favorite guest.
        :rtype: str
        """
        if self.favorite_guest_1 != 0:
            try:
                fav_1 = Guest.get(Guest.id == self.favorite_guest_1)
            except DoesNotExist:
                return "Pas de personne favorite"
            return str(fav_1.name + ' ' + fav_1.surname)
        else: 
            return "Pas de personne favorite"


    def name_of_fav_2(self):
        """
        Get the full name of the player's second favorite guest.

        :return: The second favorite guest's name and surname separated by a space. "Pas de personne favorite" if the player does not have a second favorite guest.
        :rtype: str
        """
        if self.favorite_guest_2 != 0:
            try:
                fav_2 = Guest.get(Guest.id == self.favorite_guest_2)
            except DoesNotExist:
                return "Pas de personne favorite"
            return str(fav_2.name + ' ' + fav_2.surname)
        else: 
            return "Pas de personne favorite"


    def name_of_fav_3(self):
        """
        Get the full name of the player's third favorite guest.

        :return: The third favorite guest's name and surname separated by a space. "Pas de personne favorite" if the player does not have a third favorite guest.
        :rtype: str
        """
        if self.favorite_guest_3 != 0:
            try:
                fav_3 = Guest.get(Guest.id == self.favorite_guest_3)
            except DoesNotExist:
                return "Pas de personne favorite"
            return str(fav_3.name + ' ' + fav_3.surname)
        else: 
            return "Pas de personne favorite"

    
    def has_a_table(self):
        """
        Check if the player has a table for the wedding.

        :return: True if the player has a table, False otherwise.
        :rtype: bool
        """
        if self.table is not None: 
            return True
        else: 
            return False

    
    def same_table(self, ident):
        """ 
        Check if the player is at the same table of the player's ident given.

        :return: True if they are at the same table, False otherwise. It returns a message if the player is not valid.
        :rtype: bool
        """
        try:
            guest = Player.get(
                (Player.id == ident) & (Player.mariage == self.mariage)
            ) 
        except DoesNotExist:
            return (str("L'identifiant que vous avez renseigné n'est pas bon, cette personne" +
                        "ne figure pas dans la table Player pour ce mariage"))
        
        return guest.table == self.table


    def satisfaction(self):
        """
        Calculates the satisfaction score of the player based on their seating arrangements.

        :return: The satisfaction score of the player.
        :rtype: int 
        """
        nb_point = 0
        if self.couple_situation ==1 : 
            if self.same_table(self.partner_name):
                nb_point += 3
        if self.favorite_guest_1 != 0 and self.same_table(self.favorite_guest_1):
            nb_point += 3
        if self.favorite_guest_2 != 0 and self.same_table(self.favorite_guest_2):
            nb_point += 2
        if self.favorite_guest_1 != 0 and self.same_table(self.favorite_guest_3):
            nb_point += 1
        return nb_point

    
    def color(self):
        """
        Gives the color corresponding to the satisfaction score of the player.
        """        

        very_good = "green"
        good = "orange"
        not_good = "red"

        if int(self.satisfaction()) >= 3:
            return Markup('<span style="background-color: {}">{}</span>'.format(very_good, self.full_name()))
        elif int(self.satisfaction()) >= 1:
            return Markup('<span style="background-color: {}">{}</span>'.format(good, self.full_name()))
        else:
            return Markup('<span style="background-color: {}">{}</span>'.format(not_good, self.full_name()))


    @classmethod
    def get_player_mail(cls, mariage, email):
        """ 
        Get the corresponding player for a given wedding and a given email.

        :param mariage: wedding name 
        :type id: str
        :param email: player's mail 
        :type id: str
        """
        try:
            player = cls.get((cls.mariage == mariage)&(cls.email==email))
        except DoesNotExist:
            return None
        return player


    @classmethod
    def get_player_id(cls, ident):
        """ 
        Get the corresponding player for a given id.

        :param id: player's id
        :type id: int
        """
        try:
            player = cls.get(cls.id == ident)
        except DoesNotExist:
            return None
        return player

    
    @classmethod
    def number_of_player(cls, mariage):
        return cls.select().where(cls.mariage == mariage).count()


class Tables(BaseModel):
    """ Storing infomations about the wedding's tables. """
    id = AutoField()
    mariage = CharField(null = False)
    capacity = IntegerField(null = False)
    number = IntegerField(null = False)


    @classmethod
    def get_table_capa(cls, mariage, capacity):
        try: 
            table = Tables.get((Tables.mariage == mariage) & (Tables.capacity == capacity))
        except DoesNotExist:
            return None
        return table
        

    @classmethod
    def is_empty(cls, mariage):
        if cls.select(cls.mariage == mariage).count() == 0:
            return True
        else:
            return False


db.close()
