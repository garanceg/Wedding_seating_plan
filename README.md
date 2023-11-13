README - EVENT ASSIGNMENT 

1) Présentation du projet:
Une des étapes clefs de l'organisation d'un mariage est la composition du plan de table. Cette tâche s'avère souvent être fastidieuse : Comment répartir convenablement les invités pour que ceux-ci soient satisfaits ? Faut-il mélanger les invités pour qu'ils fassent de nouvelles rencontres ? Ou au contraire les placer avec des gens qu'ils apprécient pour être sûrs qu'ils passent une bonne soirée ? Toutes ces questions rendent le sujet du plan de table très complexe. Et c'est d'autant plus compliqué que le nombre d'invités est élevé. C'est pourquoi nous avons décidé de créer un site web qui a pour objectif de générer des plans de table pour l'organisation de mariages. Ce site simplifie donc grandement la tâche aux mariés qui sont souvent très occupés à l'approche de leur mariage et qui n'ont pas beaucoup de temps pour placer leurs invités de la meilleure manière possible. 


2) Installations préalables:
Les modules et bibliothèques utilisés, ainsi que les versions, sont présents dans le fichier requirements.txt. Il faut donc s’assurer de disposer de tous ces modules, à la bonne version afin que le site fonctionne comme il faut. 
La particularité de notre projet réside dans le fait que nous avons eu recours à un solveur nécessitant une licence: Gurobi. En tant qu’étudiants ou chercheurs vous pouvez bénéficiez d’une licence académique: il suffit de se rendre sur le site: https://www.gurobi.com/academia/academic-program-and-licenses/ afin de demander une licence académique en utilisant son adresse mail @enpc.fr ou les serveurs eduroam. Il suffit ensuite de lancer la commande pip install gurobipy et de rentrer son numéro de licence.

Vous pouvez trouver une documentation détaillée (que nous avons effectuée avec Sphinx). Pour y accéder, il suffit depuis le dossier du projet d'aller dans le dossier build puis html et enfin cliquer sur "index".

3) Utilisation fonctionnelle du site:
Après avoir installé tous les modules Python nécessaires (Voir le fichier Requirements), vous pouvez lancer l’application, pour cela, il faut aller sur le fichier main et run le code. Cela va démarrer l’application. Ensuite, un lien va s’afficher dans le terminal de votre IDE. En cliquant sur le lien ou en le copiant dans un navigateur, vous allez arriver sur le site.


Vous avez deux possibilités d’utilisation:

-Utilisez l’application de manière normale (renseigner un mariage, ajouter une liste d’invité, leur envoyer une invitation, enfin générer un plan de table et réorganiser le plan de table selon vos envies).


-Utilisez la fonctionnalité Générez un Mariage sur la page d’accueil:


- a)Générer le mariage aléatoire:
    1. Cliquer sur l’onglet générer un mariage  
    2. Renseigner les informations suivantes en vous rappelant de celles-ci: nom du mariage, nombre de participants, nombre de couples souhaités.
    3. Cliquer sur enregistrer.
    4. Choisir la disposition des tables souhaitée dans la liste déroulante.
    5. Cliquer sur générer un mariage
    6. Notez bien le mail de l’invité qui n’a pas encore renseigné ses informations, afin de pouvoir tester cette fonctionnalité du site.

 - b)Générer votre espace organisateur:
    1. Cliquer sur l’onglet se connecter
    2. Cliquer sur l’onglet Je suis organisateur
    3. Cliquer sur S’inscrire.
    4. Renseigner les champs suivants: Nom du mariage (indiqué en aii), prénom, nom, e-mail, mot de passe souhaité, noms et prénoms des mariés.
    5. Vous êtes alors connecté dans votre espace organisateur, où vous pouvez consulter la liste de vos invités générée aléatoirement.

 - c)Compléter les informations d’un invité pour qu’il confirme sa venue:
    1. Après vous être déconnecté de votre espace organisateur (bouton Se déconnecter), cliquer sur l’onglet se connecter, puis sur l’onglet Je suis invité.
    2. Cliquer sur S’inscrire.
    3. Renseigner le nom du mariage (indiqué en a ii)) ainsi que le mail indiqué par le site à l’issue de l’étape n°a vi).
    4. Vous pouvez alors renseigner les informations complémentaires de cet invité: mot de passe, âge, situation familiale, genre, personne qui vous invite, et vos préférences de placement en fonction de la liste déroulante des invités au mariage.
    5. Cet invité est désormais compté comme présent au mariage
    6. Sur votre espace invité vous pouvez consulter diverses informations concernant l’évènement tel que le plan de table si celui-ci a été généré.
    7. Déconnectez vous.

 - d)Générer le plan de table de votre mariage:
    1. Connectez vous en tant qu’organisateur avec vos informations remplies en biv).
    2. Cliquer sur l’onglet Gérer ses invités.
    3. Puis liste des invités.
    4. Puis sur le lien générer un plan de table.
    5. Votre plan de table optimisé s’affiche, en vous montrant le contentement des différents invités (code couleur).
    6. Il est aussi possible de modifier manuellement le plan de table si celui-ci ne vous convient pas intégralement.











