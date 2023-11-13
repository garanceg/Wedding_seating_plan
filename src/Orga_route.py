from flask_bcrypt import generate_password_hash, check_password_hash
from flask import flash,  get_flashed_messages,render_template, redirect, url_for,  session, request, Blueprint
from peewee import *
from functools import wraps

from profil import db, Guest, Player, Orga, Tables
from form import orga_login, orga_register, ExchangeSeats, SendMail
from send_email import *


def orga_login_required_id(ident):
    """
    This wrap function restrain certain pages only to user that are connected as organizers
   
    :param ident: id of the user
    :type ident: int
    
    """
    def orga_login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if str('orga' + str(ident)) not in session:
                flash("Vous devez être enregistré en tant qu'organisateur si vous souhaitez accéder à cette page")
                return redirect(url_for('orga.log_orga'))
            return f(*args, **kwargs)
        return decorated_function
    return orga_login_required


db.connect()
db.create_tables([Guest, Player, Orga, Tables])


bp = Blueprint('orga', __name__)


@bp.route('/orga.log_orga', methods=['get', 'post'])
def log_orga():
    """
    This function 'log_orga' handles the back-end of 'orga_log.html' page. If a user fills correct informations, 
    an email that is in the Database and the correct password, then he can go to the Page de Garde for the organizers.

    :return: Log Orga page or Page de Garde page
    :rtype: template
    """
    form = orga_login()
    if request.method == 'POST':
        if form.validate_on_submit():
            orga = Orga.get_orga_mail(form.mariage.data, form.email.data)  # trying to get the organizer
            if orga is None:
                flash("Mariage ou email introuvable")
                return redirect(url_for('orga.log_orga'))
            else:
                if check_password_hash(orga.password, form.password.data):
                    ident = orga.id  # getting the identifier
                    # Connecting to the server: 
                    session[str('orga' + str(ident))] = True
                    return redirect(url_for('page_de_garde_login', statut='orga', ident=ident))
                else: 
                    flash("Mot de passe incorrect")
                    return redirect(url_for('orga.log_orga'))
        else:
            flash("Veuillez entrer un mail correct")  # Email error
            return redirect(url_for('orga.log_orga'))
    else: 
        return render_template('orga_log.html', title="Orga login", form=form, messages = get_flashed_messages())


@bp.route('/orga_register', methods=['get','post'])
def orga_reg():
    """
    This function 'orga_reg' handles the back-end of 'orga_register.html' page, meaning the page where a user
     can register himself. If a user fills correct informations asked by the form, then he can go to the Page de Garde 
     for organizers.

    :return: Orga Register page or Page de Garde page
    :rtype: template
    """
    form = orga_register()
    if request.method == 'POST':
        if form.validate_on_submit():
            mariage = form.mariage.data
            email = form.email.data
            organizer = Orga.get_orga_mail(mariage, email)
            if organizer is not None:  # Checking is the organizer has already registered 
                flash("Vous êtes déjà enregistré pour l'organisation de ce mariage, veuillez vous identifier")
                return redirect(url_for('orga.log_orga'))
            else:
                hashed_password = generate_password_hash(form.password.data).decode('utf-8')
                orga = Orga.create(
                        email = form.email.data, 
                        password = hashed_password,
                        mariage = mariage,
                        name = form.name.data,
                        surname = form.surname.data,
                        groom_name = form.groom_name.data, 
                        groom_surname = form.groom_surname.data,
                        bride_name = form.bride_name.data,
                        bride_surname = form.bride_surname.data
                    )
                orga.save()

                # Connecting to the server
                session[str('orga' + str(orga.id))] = True
                return redirect(url_for('page_de_garde_login', statut='orga', ident=orga.id))
        else:
            flash("Veuillez entrer un mail correct svp")
            return redirect(url_for('orga.orga_reg'))
    else:
        return render_template("orga_register.html", title="Orga register", form=form, messages=get_flashed_messages())


@bp.route('/guest_list/<statut>/<mariage>/<ident>')
def guest_list(statut,mariage, ident):
    """
    The function 'guest_list' handles the back-end of 'orga_guest_list' page, meaning the page where an organizer can see the list of the Guests for his wedding. The organizer can also see the answer of the Gest and their informations.

    :param statut: statut of the user
    :type statut: str
    :param mariage: name of the mariage of the guest accessing to its personal profile
    :type mariage: str
    :param ident: id of the user
    :type ident: int
    """
    @orga_login_required_id(ident)
    def wrapper():
        query = Guest.select().where(Guest.mariage == mariage).order_by(Guest.surname)
        nb_player = Player.select().where(Player.mariage==mariage).count()
        nb_guest = query.count()
        return render_template('orga_guest_list.html', title="guest_list", query=query, Player = Player, statut=statut, ident=ident, mariage=mariage,
                                nb_player=nb_player, nb_guest=nb_guest, messages=get_flashed_messages())
    return wrapper()


@bp.route('/send_email/<statut>/<mariage>/<ident>',methods=['get', 'post'])
def send_email(statut,mariage, ident):    
    """
    The function 'send_email' handles the back-end of 'orga_send_email.html' page, meaning the page where an organizer can send the invitation of his wedding to the Guests. The organizer has the opportunity to write the subject and the body of the email.

    :param statut: 
    :type statut: 
    :param mariage: The mariage to wconcerned by the inv
    :type mariage: StringField
    :param ident: 
    :type ident: 

    :return: 
    :rtype: None
    """
    @orga_login_required_id(ident)
    def wrapper():
        form = SendMail()
        if request.method == 'POST':
            if form.validate_on_submit():
                query = Guest.select(Guest.mariage == mariage)
                communication_list=[]
                for guest in query:
                    communication_list.append(guest.email)
                send_mail_organisation(form.body.data, form.subject.data,communication_list=communication_list)
                return redirect(url_for('page_de_garde_login', statut=statut, ident=ident))
            else: 
                flash("Un des champs est mal renseigné")
                return redirect(url_for('send_email', statut=statut, mariage=mariage, ident=ident))
        else:
            return render_template('orga_send_email.html', mariage=mariage, statut=statut, ident=ident)
    return wrapper()


@bp.route('/seating_plan/<statut>/<mariage>/<ident>', methods=['get', 'post'])
def seating_plan(statut, mariage, ident):
    """
    The function 'seating' handles the back-end of 'orga_table_assigment.html' page, meaning the page where 
    an organizer can see the seating plan. The organizer has the opportunity to exchange people on the seating plan.

    :param statut: statut of the user
    :type statut: str
    :param mariage: name of the mariage of the guest accessing to its personal profile
    :type mariage: str
    :param ident: id of the user
    :type ident: int
    """
    @orga_login_required_id(ident)
    def wrapper():
        seating_plan_bool = True
        table_assignement=[]
        nb_people_side_fav = [0, 0, 0]
        nb_couple_side_by_side = [0, 0]
        query = Player.select().where((Player.mariage == mariage) & (Player.table.is_null()==False))
        if not query:
            return render_template("orga_table_assigment.html", statut=statut, ident=ident, mariage=mariage, table_assignement=table_assignement,seating_plan_bool = False, nb_table=0, nb_guest=0)
        else:
            for player in query:
                table_assignement.append([player.color(),player.table])
                if player.same_table(player.favorite_guest_1):
                    nb_people_side_fav[0] += 1
                if player.same_table(player.favorite_guest_2):
                    nb_people_side_fav[1] += 1
                if player.same_table(player.favorite_guest_3):
                    nb_people_side_fav[2] += 1
            nb_guest = len(table_assignement)
            # Counting the number of tables of the wedding
            nb_table = 0
            for table in Tables.select().where(Tables.mariage == mariage):
                nb_table += table.number
            
            # Counting the number of couples that are at the same table
            nb_couple_side_by_side = 0
            couple = Player.select().where((Player.mariage == mariage) & (Player.couple_situation == 1))
            nb_couple = couple.count()
            for player in couple:
                if player.same_table(player.partner_name):
                    nb_couple_side_by_side += 1

            form = ExchangeSeats(mariage)
            if request.method == 'POST':
                if form.validate_on_submit():
                    id_1 = form.player_1.data
                    id_2 = form.player_2.data
                    if id_1 == 0 or id_2 == 0:
                        flash("Veuillez sélectionner 2 invités pour effectuer l'échange")
                        return redirect(url_for('table_assigment', mariage=mariage, statut=statut, ident=ident))
                    else:
                        player_1 = Player.get_player_id(id_1)
                        player_2 = Player.get_player_id(id_2)
                        if player_1 is None or player_2 is None: 
                            flash("L'une des deux personnes sélectionnée n'est pas invité à ce mariage.")
                            return redirect(url_for('table_assigment', mariage=mariage, statut=statut, ident=ident))
                    
                        # Exchanging the tables
                        table_1 = player_1.table
                        table_2 = player_2.table
                        player_1.table = table_2
                        player_1.save()
                        player_2.table = table_1
                        player_2.save()
                        new_table_assignement = []
                        query = Player.select().where((Player.mariage == mariage) & (Player.table.is_null(False)))
                        for player in query:
                            new_table_assignement.append([player.color(),player.table])
                        couple = Player.select().where((Player.mariage == mariage) & (Player.couple_situation == 1))
                        nb_couple = couple.count()
                        nb_couple_side_by_side = 0
                        for player in couple:
                            if player.same_table(player.partner_name):
                                nb_couple_side_by_side += 1
                        flash("Les deux invités ont bien été échangés.")
                        return render_template("orga_table_assigment.html", statut=statut, ident=ident, mariage=mariage,seating_plan_bool=seating_plan_bool,
                                                table_assignement=new_table_assignement,nb_table=nb_table, nb_guest=nb_guest, form=form, nb_couple_side_by_side=int(nb_couple_side_by_side/2), 
                                                nb_couple=int(nb_couple/2), nb_people_side_fav=nb_people_side_fav, messages=get_flashed_messages() )
        return render_template("orga_table_assigment.html", statut=statut, ident=ident, mariage=mariage, seating_plan_bool=seating_plan_bool  , table_assignement=table_assignement,nb_table=nb_table,
                                nb_guest=nb_guest, form=form, nb_couple_side_by_side=int(nb_couple_side_by_side/2), nb_couple=int(nb_couple/2), nb_people_side_fav=nb_people_side_fav, messages=get_flashed_messages() )
    return wrapper()
    

@bp.route('/orga_info/<statut>/<mariage>/<ident>')
def orga_info(statut, mariage, ident):
    """
    The function 'orga_info' handles the back-end of 'orga_info.html' page, meaning the page where an organizer can see 
    the informations of his wedding.

    :param statut: statut of the user
    :type statut: str
    :param mariage: name of the mariage of the guest accessing to its personal profile
    :type mariage: str
    :param ident: id of the user
    :type ident: int
    """
    @orga_login_required_id(ident)
    def wrapper():
        table_capa_nb = []
        try: 
            orga = Orga.get((Orga.mariage == mariage) & (Orga.id == ident))
        except DoesNotExist:
            flash("Vous n'êtes pas organisateur de ce mariage. Veuillez vous reconnecter")
            return redirect(url_for("logout", statut=statut, ident=ident))
        if Tables.is_empty(mariage):
            return render_template("orga_info.html", mariage=mariage, ident=ident, statut=statut, groom_full_name = orga.groom_full_name(), 
                                   bride_full_name = orga.bride_full_name(),table_capa_nb=table_capa_nb, name=orga.name, surname = orga.surname)
        else: 
            for table in Tables.select().where(Tables.mariage == mariage):
                table_capa_nb.append([table.capacity, table.number])
            nb_table_diff = len(table_capa_nb)
            return render_template("orga_info.html", mariage=mariage, ident=ident, statut=statut, groom_full_name = orga.groom_full_name(), 
                                   bride_full_name = orga.bride_full_name(),table_capa_nb=table_capa_nb, name=orga.name, surname=orga.surname, nb_table_diff=nb_table_diff, messages=get_flashed_messages())
    return wrapper()


@bp.route('/orga_change_info/<statut>/<mariage>/<ident>', methods=['get', 'post'])
def orga_change_info(statut, mariage, ident):
    """
    The function 'orga_info' handles the back-end of 'orga_info.html' page, meaning the page where an organizer can 
    see the informations of his wedding.

    :param statut: statut of the user
    :type statut: str
    :param mariage: name of the mariage of the guest accessing to its personal profile
    :type mariage: str
    :param ident: id of the user
    :type ident: int
    """
    @orga_login_required_id(ident)
    def wrapper():
        try: 
            orga = Orga.get((Orga.mariage == mariage) & (Orga.id == ident))
        except DoesNotExist:
            flash("Vous n'êtes pas organisateur de ce mariage. Veuillez vous reconnecter")
            return redirect(url_for("logout", statut=statut, ident=ident))
        # Getting the former information of the organizer
        data = {'name' : orga.name,
            'surname' : orga.surname,
            'email' :orga.email, 
            'mariage' :mariage, 
            'groom_name': orga.groom_name,
            'groom_surname': orga.groom_surname, 
            'bride_name':orga.bride_name,
            'bride_surname': orga.bride_surname
                }
        form = orga_register(data=data)
        if request.method == 'POST':
            if form.validate_on_submit():
                if check_password_hash(orga.password, form.password.data):
                    orga.name = form.name.data
                    orga.surname = form.surname.data
                    orga.mariage = form.mariage.data
                    orga.groom_name = form.groom_name.data
                    orga.groom_surname = form.groom_surname.data
                    orga.bride_name = form.bride_name.data
                    orga.bride_surname = form.bride_surname.data
                    orga.save()
                    # If the organizer decide to change the name of the wedding, 
                    # we have to change the wedding's name of all the instances
                    Guest.update(mariage=orga.mariage).where(Guest.mariage == mariage).execute()
                    Player.update(mariage=orga.mariage).where(Player.mariage == mariage).execute()
                    Tables.update(mariage =orga.mariage).where(Tables.mariage ==mariage).execute()
                    flash("Vos données ont bien été modifiées")
                    return redirect(url_for('orga.orga_info', mariage = orga.mariage, statut =statut, ident=ident))
                else: 
                    flash("Mot de passe incorrect, veuillez réessayer")
                    return redirect(url_for("orga.orga_change_info", mariage=mariage, statut=statut, ident=ident))
            else: 
                flash("Les informations renseignées sont mauvaises")
                return redirect(url_for("orga.orga_change_info", mariage=mariage, statut=statut, ident=ident))
        else:
            return render_template("orga_change_info.html", form=form, mariage=mariage, statut=statut, ident=ident, messages=get_flashed_messages())
    return wrapper()


db.close()
