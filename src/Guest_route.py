from flask import flash, get_flashed_messages, render_template, redirect, url_for, request, session, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from peewee import *
from functools import wraps

from form import player_register, guest_login, player_register_init
from profil import db, Guest, Player, Orga, Tables


def login_required_id(ident_user):
    """
    This wrap function restrain certain pages only to user that are connected.

    :param ident_user: id of the user
    :type ident_user: int
    """
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if str('guest' + str(ident_user)) in session:
                return f(*args, **kwargs)
            if str('orga' + str(ident_user)) in session:
                return f(*args, **kwargs)
            else:
                flash("Vous devez être connecté pour pouvoir accéder à cette page")
                return redirect(url_for('page_de_garde'))
        return decorated_function
    return login_required


def guest_login_required_id(ident):
    """
    This wrap function restrain certain pages only to user that are connected as guest.

    :param ident: id of the user
    :type ident: int
    """
    def guest_login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if str('guest' + str(ident)) not in session:
                flash("Vous devez être enregistré en tant qu'invité pour pouvoir accéder à cette page")
                return redirect(url_for('guest.log_guest'))
            return f(*args, **kwargs)
        return decorated_function
    return guest_login_required


db.connect()  # connecting to the databas
db.create_tables([Guest, Player, Orga, Tables])  # creating the tables from the database


bp = Blueprint('guest', __name__)


@bp.route('/log_guest', methods=['get', 'post'])
def log_guest():
    """
    The function 'log_guest' handle the back-end of the 'log_guest()' form.

    :return: The same page if the informations are incorrect (not invited to the wedding, incorrect email or password)
    :rtype: template
    """
    form = guest_login()
    if request.method == 'POST':
        if form.validate_on_submit():  # check if the form is valid and submitted
            # checking if the guest has registered yet
            player = Player.get_player_mail(form.mariage.data, form.email.data)
            if player is None:
                flash("Mariage ou email introuvable")
                return redirect(url_for('guest.log_guest'))
        
            if check_password_hash(player.password, form.password.data):  # Check if the password is correct
                session[str('guest' + str(player.id))] = True
                return redirect(url_for('page_de_garde_login', statut = 'guest', ident=player.id))
            else:
                flash("Mot de passe incorrect")
                return redirect(url_for('guest.log_guest'))
        else:
            flash("Veuillez entrer un mail correct")
            return redirect(url_for('guest.log_guest'))
    else:
        return render_template('guest_log.html', title="guest login", form=form, messages = get_flashed_messages())


@bp.route('/player_register_init', methods=['get','post'])
def player_reg_init():
    """
    The function 'player_reg_init' handle the back-end of the 'player_reg_init()' form.

    :return: The same page if the informations are incorrect (not invited to the wedding or incorrect email)
    :rtype: template
    """
    form = player_register_init()
    if request.method == 'POST':
        if form.validate_on_submit():
            # checking if the guest is invited to the wedding
            guest = Guest.get_guest_mail(form.mariage.data, form.email.data)
            if guest is None: 
                flash ("Mariage ou email introuvable")
                return redirect(url_for("guest.player_reg_init"))
            
            # Checking if this guest is already registered
            player = Player.get_player_mail(form.mariage.data, form.email.data)
            if player is not None:
                flash("Vous êtes déjà enregistré pour ce mariage, veuillez vous connecter")
                return redirect(url_for('guest.log_guest'))
            
            # Checking if an organizer is registered for this wedding
            orga = Orga.get_orga_mariage(form.mariage.data)
            if orga is None:
                flash("Aucun organisateur n'est lié à ce mariage")
                return redirect(url_for('guest.log_guest'))
            else:
                ident = guest.id
                mariage = form.mariage.data
                full_name = guest.full_name()
                email = form.email.data
                return (redirect(url_for("guest.player_reg", ident=ident, mariage=mariage, full_name=full_name, email=email)))
        else: 
            flash("Veuillez entrer un mail correct")
            return redirect(url_for("guest.player_reg_init"))
    return render_template("player_reg_init.html", form=form, messages = get_flashed_messages())


@bp.route('/player_register/<ident>/<full_name>/<mariage>/<email>', methods=['get','post'])
def player_reg(ident, full_name, mariage, email):
    """
    This function 'player_reg' handle the back-end of the 'guest_login()' form.

    :param mariage: name of the mariage of the guest accessing to its personal profile
    :type mariage: str
    :param ident: id of the user
    :type ident: int
    :param full_name: full name of the player
    :type full_name: str
    :param email: email of the player
    :type email: str
    
    :return: The same page if the informations are incorrect (not invited to the wedding, incorrect email or password)
    :rtype: template
    """
    form = player_register(ident, mariage)
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data).decode('utf-8')  # encrypt the password
            # Creating the player instance 
            player = Player.create(
                    id = ident,
                    mariage = mariage,
                    email = email,
                    password = hashed_password,
                    age = form.age.data,
                    couple_situation = form.couple_situation.data,
                    partner_name = form.partner_name.data,
                    gender = form.gender.data,
                    family = form.family.data,
                    favorite_guest_1 = form.favorite_guest_1.data,
                    favorite_guest_2 = form.favorite_guest_2.data,
                    favorite_guest_3 = form.favorite_guest_3.data
                )
            player.save()
            # Connecting to the server
            session[str('guest' + str(ident))] = True
            return redirect(url_for('page_de_garde_login', statut='guest', ident= ident))
        else:
            flash("Certain champs renseignés sont incorrects")
            return redirect(url_for("guest.player_reg", ident=ident, full_name=full_name, mariage=mariage, email=email))
    return render_template("player_register.html", title="player register", form=form, messages = get_flashed_messages(), full_name=full_name)


@bp.route('/guest_profil/<statut>/<ident>/<mariage>/<full_name>/<guest_ident>')
def guest_profil(statut,ident,mariage, full_name, guest_ident):
    """
    This function 'guest_profil' handles the back-end of the guest_profil page

    :param mariage: name of the mariage of the guest accessing to its personnal profil
    :type mariage: str
    :param statut: statut of the user
    :type statut: str
    :param ident: id of the user
    :type ident: int
    :param full_name: full name of the guest
    :type full_name: str
    :param guest_ident: id of the guest
    :type guest_ident: int
    

    :return:  Page of the guest's personal profil 
    :rtype: template
    """
    @login_required_id(ident)
    def wrapper():

        player = Player.get_player_id(guest_ident)
        if player is None : 
            flash("Vous devez être connecté pour accéder à cette page")
            return redirect(url_for('logout', statut=statut, ident=ident))
        else:
            name, surname = player.full_name().split(' ')
            name_of_partner = player.name_of_partner()
            # Getting the organizer of this wedding
            orga = Orga.get_orga_mariage(mariage)
            if orga is None :
                flash("Aucun organisateur n'est associé à ce mariage")
                return redirect(url_for('logout', statut=statut, ident=ident))
            else:
                if player.family == 1: 
                    coming_for = orga.groom_full_name()
                else: 
                    coming_for = orga.bride_full_name()
                return render_template("guest_profil.html", statut=statut, ident=ident, guest_ident=guest_ident, name=name, surname=surname,mariage=mariage, appelle=player.mr_or_miss(), full_name=full_name, age = player.age,
                                        gender = player.called_gender(), name_of_partner=name_of_partner, coming_for=coming_for, fav_1=player.name_of_fav_1(), fav_2=player.name_of_fav_2(), 
                                        fav_3=player.name_of_fav_3(), table=player.table, a_une_table=player.has_a_table(), couple_situation=player.couple_situation)
    return wrapper()


@bp.route('/table_indiv/<statut>/<ident>/<mariage>/<table>/<guest_ident>')
def table_indiv(statut, ident, mariage, table, guest_ident):
    """
    This function 'table_indiv' handles the back-end of the page accessible in the profile page that shows the table of the guest

    :param statut: statut of the user
    :type statut: str
    :param mariage: name of the mariage of the guest accessing to its personal profile
    :type mariage: str
    :param ident: id of the user
    :type ident: int
    :param guest_ident: id of the guest
    :type guest_ident: int
    :param table: id of the user
    :type ident: int
    """
    @login_required_id(ident)
    def wrapper():
        guest = Player.get_player_id(ident)
        if guest is None:
            flash("Vous n'êtes pas enregistrer pour ce mariage")
            return redirect(url_for('logout', statut=statut, ident=ident))
        query = Player.select().where(
            (Player.table == table) & (Player.mariage == mariage)
        ) 
        same_table = []
        for player in query: 
            same_table.append(player.full_name())
        nb_personne_table = len(same_table)
        return render_template("guest_table_indiv.html", statut=statut, ident=ident, guest_ident=guest_ident, full_name = guest.full_name(),
                                mariage=mariage, table=table, same_table=same_table, nb_personne_table=nb_personne_table)
    return wrapper()


#Page pour pouvoir modifier ses informations
@bp.route('/guest_change_info/<statut>/<mariage>/<ident>', methods=['get','post'])
def guest_change_info(statut, mariage, ident):
    """
    This function 'guest_change_info' handles the back-end of the page that allows the guest to modify its information

    :param statut: statut of the user
    :type statut: str
    :param mariage: name of the mariage of the guest accessing to its personal profile
    :type mariage: str
    :param ident: id of the user
    :type ident: int
    """
    @guest_login_required_id(ident)
    def wrapper():
        player = Player.get_player_id(ident)
        if player is None :
            flash("L'invité dont vous essayer de modifier les informations n'existe pas.")
            return redirect(url_for('logout', statut=statut, ident=ident))
        else:
            # Getting the former information of the player
            data = {'age' : player.age,
                'couple_situation' : player.couple_situation,
                'partner_name' : player.partner_name, 
                'gender' :player.gender, 
                'family': player.family,
                'favorite_guest_1': player.favorite_guest_1, 
                'favorite_guest_2':player.favorite_guest_2,
                'favorite_guest_3': player.favorite_guest_3
                    }
            form = player_register(ident=ident, mariage=mariage, data=data)
            if request.method == 'POST':
                if form.validate_on_submit():
                    if check_password_hash(player.password, form.password.data):
                        player.age = form.age.data
                        player.couple_situation = form.couple_situation.data
                        player.partner_name = form.partner_name.data
                        player.gender = form.gender.data
                        player.family = form.family.data
                        player.favorite_guest_1 = form.favorite_guest_1.data
                        player.favorite_guest_2 = form.favorite_guest_2.data
                        player.favorite_guest_3 = form.favorite_guest_3.data
                        player.save()  # Saving the changes
                        flash("Vos modifications ont bien été enregistées")
                        return redirect(url_for('guest.guest_profil', statut=statut, ident=ident, mariage=mariage, full_name=player.full_name(), guest_ident=ident))
                    else:
                        flash("Mot de passe incorrect")
                        return redirect(url_for("guest.guest_change_info", statut=statut, ident=ident, mariage=mariage))
                else:
                    flash("Certain champs reseignés sont incorrects")
                    return redirect(url_for("guest.guest_change_info", statut=statut, ident=ident, mariage=mariage))
            else:
                return render_template("guest_change_info.html", form=form, statut=statut, ident=ident, mariage=mariage, messages=get_flashed_messages())
    return wrapper()


db.close()
