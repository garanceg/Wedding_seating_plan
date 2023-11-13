from peewee import DoesNotExist
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, RadioField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email

from profil import db, Guest, Player, Orga

db.connect()
db.create_tables([Guest, Player, Orga])

class orga_login(FlaskForm):

    """
    The orga_register class inherits from the FlaskForm class of WTForms.
    It allows a organizer to log in the website.

    :param email: Field for entering the organizer's email address. It is required and must be a valid email address.
    :type email: StringField 
    :param password: Field for entering the organizer's password. It is required.
    :type password: PasswordField 
    :param mariage: Field for entering the name of the wedding to which the organizer wants to log in. It is required.
    :type mariage: StringField
    :param submit: Button to submit the form.
    :type submit: SubmitField
    """
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de Passe', validators=[DataRequired()])
    mariage = StringField('Mariage', validators=[DataRequired()])
    submit = SubmitField("Se connecter")


class orga_register(FlaskForm):
    """
    The orga_register class inherits from the FlaskForm class of WTForms.
    It allows a organizer to sign in the website.

    :param email: Field for entering the organizer's email address. It is required and must be a valid email address.
    :type email: StringField 
    :param password: Field for entering the organizer's password. It is required.
    :type password: PasswordField 
    :param mariage: Field for entering the name of the wedding to which the organizer wants to sign in. It is required.
    :type mariage: StringField
    :param submit: Button to submit the form.
    :type submit: SubmitField

    Methods:
    validate_email(self, email): This method is used to validate the organizer's email address.
    validate_password(self, password): This method is used to validate the organizer's password.

    Example of use:
    form = orga_reg()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        mariage = form.mariage.data
        # Perform the login
    """

    name = StringField('Votre prénom', validators=[DataRequired()])
    surname = StringField('Votre nom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email("Email invalide")])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    mariage = StringField('Mariage', validators=[DataRequired()])
    groom_name = StringField('Prénom du marié', validators=[DataRequired()])
    groom_surname = StringField('Nom du marié', validators=[DataRequired()])
    bride_name = StringField('Prénom de la mariée', validators=[DataRequired()])
    bride_surname = StringField('Nom de la mariée', validators=[DataRequired()])    
    submit = SubmitField("S'inscrire")


class guest_login(FlaskForm):
    """
    The guest_login class inherits from the FlaskForm class of WTForms. 
    It allows guests to log in the website.

    :param email: Field for entering the guest's email address. It is required and must be a valid email address.
    :type email: StringField 
    :param password: Field for entering the guest's password. It is required.
    :type password: PasswordField 
    :param mariage: Field for entering the name of the wedding to which the user wants to log in. It is required.
    :type mariage: StringField
    :param submit: Button to submit the form.
    :type submit: SubmitField
   

    Methods:
    validate_email(self, email): This method is used to validate the guest's email address.
    validate_password(self, password): This method is used to validate the guest's password.

    Example of use:
    form = guest_login()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        mariage = form.mariage.data
        # Perform the login
    """

    email = StringField('Email', validators=[DataRequired(), Email()])
    mariage = StringField('Mariage', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField("Se connecter")

class player_register_init(FlaskForm):

    """
    :param email: Field for entering the guest's email address. It is required and must be a valid email address.
    :type email: StringField  
    :param password: Field for entering the guest's password. It is required. It will be crypted. 
    :type password: PasswordField
    :param mariage: Field for entering the name of the wedding to which the guest wants to sign in. It is required. The guest needs to already be invited to this wedding.
    :type mariage: StringField
    :param submit: Button to submit the form.
    :type submit: SubmitField  
    """

    email = StringField('Email', validators=[DataRequired(), Email()])
    mariage = StringField('A quel mariage êtes-vous invité ?', validators=[DataRequired()])
    submit = SubmitField("S'inscrire")


class player_register(FlaskForm):
    """
    The player_register class inherits from the FlaskForm class of WTForms.
    It allows guests to sign in the website and to enter their information.

    :param mariage: Field for entering the name of the wedding to which the guest wants to log in. It is required. The guest needs to already be invited to this wedding.
    :type mariage: StringField
    :param password: Field for entering the guest's password. It is required. It will be crypted. 
    :type password: PasswordField
    :param age: Field for entering the age of the guest. It is required.
    :type age: IntegerField
    :param couple_situation: Field for entering the couple situation of a guest : 0 if not in a couple, 1 if in a couple. It is required.
    :type couple_situation: RadioField)
    :param partner_name: Field for entering the name of his partner among the guest's list (if their is one). It is required if the guest is in a couple.
    :type partner_name: SelectField
    :param gender: Field for entering the gender of the guest. It is required.
    :type gender: RadioField
    :param family: Field for entering the family of the guest. It is required.
    :type family: RadioField
    :param favorite_guest_1: Field for entering the first choice of guest who the guest wants to be seated next to.
    :type favorite_guest_1: SelectField
    :param favorite_guest_2: Field for entering the second choice of guest who the guest wants to be seated next to.
    :type favorite_guest_2: SelectField
    :param favorite_guest_3: Field for entering the third choice of guest who the guest wants to be seated next to.
    :type favorite_guest_3: SelectField
    :param submit: Button to submit the form.
    :type submit: SubmitField
    """

    def __init__(self, ident, mariage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ident = ident
        self.mariage = mariage
        self.set_choices()

    password = PasswordField('Définir un mot de passe', validators=[DataRequired()])
    age = IntegerField('Votre age', validators=[DataRequired()])
    couple_situation = RadioField('Etes-vous en couple ?', choices=[('1', 'Oui'), ('0', 'Non')], validators=[DataRequired()])
    partner_name = SelectField('Si oui, veuillez renseigner le nom de votre partenaire.')
    gender = RadioField('Votre genre', choices = [('1', 'Homme'), ('0', 'Femme')], validators=[DataRequired()])
    family = RadioField('De la part de qui venez-vous ?', validators=[DataRequired()])
    favorite_guest_1 = SelectField('1er choix')
    favorite_guest_2 = SelectField('2e choix')
    favorite_guest_3 = SelectField('3e choix')
    submit = SubmitField("S'inscrire")
    
    def set_choices(self):
        query_partner = Guest.select().where((Guest.mariage == self.mariage) & (Guest.id != self.ident)).order_by(Guest.surname)
        self.partner_name.choices = [(0, "-- selectionner une option --")]+[(g.id, g.full_name()) for g in query_partner]
        self.favorite_guest_1.choices = [(0, "-- selectionner une option --")]+[(g.id, g.full_name()) for g in query_partner]
        self.favorite_guest_2.choices = [(0, "-- selectionner une option --")]+[(g.id, g.full_name()) for g in query_partner]
        self.favorite_guest_3.choices = [(0, "-- selectionner une option --")]+[(g.id, g.full_name()) for g in query_partner]

        orga = Orga.get(Orga.mariage == self.mariage)
        self.family.choices = [('1', orga.groom_full_name()), ('2', orga.bride_full_name())]


class ChangePassword(FlaskForm):

    """
    The ChangePassword class inherits from the FlaskForm class of WTForms.
    It allows guests or organizers to change their passwords.

    :param actual_password: Field for entering the actual password. It is required.
    :type actual_password: PasswordField
    :param new_password: Field for entering the new password. It is required. It will be crypted. 
    :type password: PasswordField
    :param confirm: Field for entering a second time the new password. It is required. It will be crypted. 
    :type age: PasswordField
    :param submit: Button to submit the form.
    :type submit: SubmitField
    """

    actual_password = PasswordField("Mot de passe actuel ", validators=[DataRequired()])
    new_password = PasswordField("Nouveau mot de passe ", validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired()])
    submit = SubmitField("Modifer")

    def must_be_equal(self):
        """
        This method verifies if the new password and the confirm password are the same.

        :return: True if the new password and the confirm password are the same, False otherwise
        :rtype: bool
        """
        
        if self.confirm_password.data == self.new_password.data:
            return True
        else:
            return False
            
    def verify_code(self, code):
        if self.actual_password.data == code:
            return True
        else: 
            return False

class UploadFile(FlaskForm):
    """
    The UploadFile class inherits from the FlaskForm class of WTForms.
    It allows organizers to upload files to give the guest's list or the number of tables and their capacity.

    :param file_guest: Field to upload a file containing the list of guests.
    :type file_guest: FileField
    :param file_tables: Field to upload a file containing the tables and their capacities.
    :type file_tables: FileField
    :param submit: Button to submit the form.
    :type submit: SubmitField

    """

    file_guest = FileField("Fichier contenant les invités", validators=[DataRequired()])
    file_tables = FileField("Fichier pour les tables", validators=[DataRequired()])
    submit = SubmitField("Envoyer les fichiers")

class ResetPassword(FlaskForm):
    """
    The ResetPassword class inherits from the FlaskForm class of WTForms.
    It allows organizers and guests to reset their password if they have forgotten it.

    :param mariage: Field for entering the name of the wedding to which the guest or the organizer is invited. It is required.
    :type mariage: StringField
    :param email: Field for entering the guest or organizer's email address. It is required and must be a valid email address.
    :type email: StringField  
    :param submit: Button to submit the form.
    :type submit: SubmitField
    """

    mariage = StringField("Nom du mariage", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Recevoir un code")

class ExchangeSeats(FlaskForm):
    """
    The ExchangeSeats class inherits from the FlaskForm class of WTForms.
    It allows organizers to exchange guests who are at different tables. 

    :param player_1: Field for selecting the first guest to exchange.
    :type player_1: SelectField
    :param player_2: Field for selecting the second guest to exchange.
    :type player_2: SelectField  
    :param submit: Button to submit the form.
    :type submit: SubmitField
    """

    def __init__(self, mariage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mariage = mariage
        self.set_choices()
    
    player_1 = SelectField("Première personne que vous souhaitez échanger: ")
    player_2 = SelectField("Deuxième personne que vous souhaitez échanger: ")
    submit = SubmitField("Echanger")

    def set_choices(self):
        """
        This method gives the different options of guests we can exchange which means aall the guests that are coming to the wedding.

        :return: None
        """

        query = Player.select().join(Guest, on=(Guest.id == Player.id)).where(Player.mariage == self.mariage).order_by(Guest.surname)
        self.player_1.choices = [(0, "-- selectionner une option --")]+[(g.id, g.full_name()) for g in query]
        self.player_2.choices = [(0, "-- selectionner une option --")]+[(g.id, g.full_name()) for g in query]



class nb_guest_couple(FlaskForm):
    """
    The nb_guest_couple class inherits from the FlaskForm class of WTForms.
    It allows the user to give the number of guest and couples he wants for his fake wedding. 

    :param name: Field for entering the name of the weeding we want to create. It is required.
    :type name: StringField
    :param nb_guest: Field for entering the number of guests for the weeding we want to create. It is required.
    :type nb_guest: IntegerField  
    :param nb_couple: Field for entering the number of couples for the weeding we want to create. It is required.
    :type nb_couple: IntegerField  
    :param submit: Button to submit the form.
    :type submit: SubmitField
    """
    name = StringField("Choisissez le nom du mariage que vous souhaitez créer", validators=[DataRequired()])
    nb_guest = IntegerField("Nombre de participants", validators=[DataRequired()])
    nb_couple = IntegerField("Choisissez le nombre de couples au sein de votre mariage", validators=[DataRequired()])
    submit = SubmitField("Enregistrer")

    def name_orga_available(self):
        """
        This method verifies if no organizers have this wedding name.

        :return: True if it is available, False otherwise
        :rtype: bool
        """
        try:
            Orga.get(Orga.mariage == self.name.data)
        except DoesNotExist:
            return True
        return False
    
    def name_player_available(self):
        """
        This method verifies if no guests have this wedding name.

        :return: True if it is available, False otherwise
        :rtype: bool
        """
        try:
            Guest.get(Guest.mariage == self.name.data)
        except DoesNotExist:
            return True
        return False

    def verify_nb_couple(self):
        """
        This method verifies if the number of couples we want is feasible regarding to the number of guests.

        :return: True if it is possible, False otherwise
        :rtype: bool
        """
        if self.nb_couple.data*2 > self.nb_guest.data:
            return False
        else:
            return True
    
class TablesFakeMariage(FlaskForm):
    """
    The TablesFakeMariage class inherits from the FlaskForm class of WTForms.
    It allows the user to choose the composition of tables he want for his fake wedding. 

    :param table_capacity_number: Field for entering the name of the weeding we want to create. It is required.
    :type table_capacity_number: SelectField
    :param submit: Button to submit the form.
    :type submit: SubmitField
    """

    def __init__(self, nb_guest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nb_guest = nb_guest
        self.set_choices()
    
    table_capacity_number = SelectField("Choisissez la capacité et le nombre de tables de cette capacité", validators=[DataRequired()])
    submit = SubmitField("Générer un mariage")


    def set_choices(self):
        """
        This method gives the different possibilites for the composition of tables when the number of guests is given.

        :return: None
        """
        #we use euclidian division in order to have enought seats for the wedding
        self.table_capacity_number.choices = [([[int(self.nb_guest)//j + 1,j ]], str(str(int(self.nb_guest)//j + 1) + " table de " + str(j))) for j in [4,5,6,7,8,9,10]] 

class ContactUs(FlaskForm):
    """
    The ContactUs class inherits from the FlaskForm class of WTForms.
    It allows a user to send an email if he has any question.

    :param name: Field for entering the name of the person who wants to contact us. It is required.
    :type name: StringField
    :param email: Field for entering the email of the person who wants to contact us. It is required and must be a valid email address.
    :type email: StringField
    :param subject: Field for entering the subject of the mail. It is required.
    :type subject: StringField
    :param body: Field for entering the content of the mail. It is required.
    :type body: TextAreaField
    :param submit: Button to submit the form.
    :type submit: SubmitField
    """
    name= StringField("Votre nom", validators=[DataRequired()])
    email=StringField("Votre mail", validators=[DataRequired(), Email()])
    subject = StringField("Objet du mail", validators=[DataRequired()])
    body = TextAreaField("Contenu du mail", validators=[DataRequired()]) 
    submit = SubmitField("Envoyer")

class SendMail(FlaskForm):
    subject = StringField("Objet du mail", validators=[DataRequired()])
    body = TextAreaField(" Contenu du mail", validators=[DataRequired()])
    submit = SubmitField("Envoyer", validators=[DataRequired()])

db.close()
