# SoftDeskAPI : API apportant une solution à la gestion de projet

---

Le projet SoftDeskAPI est une application apportant une solution web à la gestion de projet en équipe. 
Cette application est implémentée sous la forme d'une API REST. L'API est interogé à partir d'urls au travers
d'un client HTTP comme postman ou en utilisant des langages de programmation comme Python combiné à des packages comme request. 
Elle renvoie les informations demandées au format JSON.
Les points d'entrées fournis par cette API sont consultables et l'objet demandé peut être modifiables si l'utilisateur 
connecté possède les autorisations nécessaires. Pour consulter ce que peuvent faire les différents comptes/status, rendez-vous plus bas.

---

## Installation

Cette API exécutable localement peut être installée en suivant les étapes décrites ci-dessous. 

#### Installation et exécution de l'application

1. Clonez ce dépôt de code à l'aide de la commande `$ git clone https://github.com/guillaumefauvel/OC-Projet-10.git` (vous pouvez également télécharger le code [en temps qu'archive zip](https://github.com/guillaumefauvel/OC-Projet-10/archive/refs/heads/main.zip))
2. Rendez-vous depuis un terminal à la racine du répertoire softdesk avec la commande `$ cd softdesk`
3. Démarrez le serveur avec `python manage.py runserver`

Une fois l'étape 3 effectué, le serveur est fonctionnel, l'API SoftDesk peut être interrogée à partir des points d'entrée commençant par l'url de base [http://localhost:8000/api/](http://localhost:8000/api/).
Le point d'entrée principal permettant d'accéder à la liste des projets est [http://localhost:8000/api/projects/](http://localhost:8000/api/projects/).

---

## Utilisation et documentation des points d'entrées

### Authentification :

| Requête | Fonctions | Opérations CRUD |
| ----------- | ----------- | ----------- | 
| `signup/` | Création de compte | `POST` |
| `login/` | Connexion | `POST` |
| `logout/` | Déconnexion | `GET` |
| `api-token-auth/` | Renvois le token | `POST` |
||||

> Tous les points d'entrée précèdant suppose en racine l'adresse `http://localhost:8000/`. 

### Gestion de projet :

| Requête | Réponse | Opérations CRUD |
| ----------- | ----------- | ----------- |
| `users` | Une liste de tout les utilisateurs, accessible aux SuperUser uniquement |`GET` |
| `projects` | Une liste de tout les projets |`GET` `POST`| 
| `projects/<project_id>` | Un projet | `GET` `PUT` `DELETE`| 
| `projects/<project_id>/users` | Une liste des contributeurs | `GET` `POST`| 
| `projects/<project_id>/users/<contribution_id>` | Une contribution | `GET` `PUT` `DELETE`| 
| `projects/<project_id>/issues/` | Une liste des issues |`GET` `POST`| 
| `projects/<project_id>/issues/<issue_id>` | Un issue | `GET` `PUT` `DELETE`| 
| `projects/<project_id>/issues/<issue_id>/comments` | Une liste des commentaires | `GET` `POST`| 
| `projects/<project_id>/issues/<issue_id>/comments/<comment_id>/` | Un commentaire | `GET` `PUT` `DELETE`| 
||||

> Tous les points d'entrée précèdant suppose en racine l'adresse `http://localhost:8000/api/`. 

> **Si vous désirez plus de détail sur les requêtes retrouvez la documentation sur ce lien** : [https://documenter.getpostman.com/view/20119383/UVsSN3wT](https://documenter.getpostman.com/view/20119383/UVsSN3wT)


---


## Connexion et Authentification

L'authentication s'effectue en 3 étapes.
1. Commencez par créer un nouveau compte à l'adresse `http://localhost:8000/signup/`
2. Connectez-vous ensuite à l'adresse `http://localhost:8000/login/`
3. Une fois connecté vous pouvez récupérer votre **Token** en effectuant une requête `POST` en fournissant dans le body
   votre `username` et votre `password` en form-data ou au format JSON* à l'adresse suivante`http://localhost:8000/api-token-auth/`.
   Une fois votre token obtenu, veillez à le fournir dans toute vos prochaînes requêtes dans le **Header** sous cette forme : 
   KEY : `Authorization` / VALUE : `token 966e46ae995266f15aca2a3b090ae0bcaa3aef5c`
   
  JSON* - Exemple d'une requête type : 
  ```json
  {
    "username": "votre-username",
    "password": "votre-mots-de-passe"
  }
```   

##### Si vous utiliser Postman : 
1. Afin de ne pas avoir à saisir manuellement les CSRF-Token, ajoutez ce morceau de code dans les Tests de chaque requête : 
    ```
    var xsrfCookie = postman.getResponseCookie("csrftoken");
    postman.setEnvironmentVariable('csrftoken', xsrfCookie.value);
    ```
2. Créer un environnement dans Postman et ajoutez-y la variable `csrftoken`. 
3. Dans le Header, ajoutez une nouvelle paire clé-valeur où la clé = `X-CSRFToken` et la valeur = `{{csrftoken}}`.

---

## Statuts et autorisations des utilisateurs

Cette API respecte les autorisations de multiple profils qui ne sont pas tous égaux.
Afin de rajouter un contributeur à un projet, l'auteur de ce dernier doit se rendre à l'adresse `http://localhost:8000/api/projects/<project_id>/users`.
Chaque utilisateur possède un certain nombre de droits, en voici la liste :


| Nom du statut | Descriptif  | Autorisations |
| ----------- | ----------- | ----------- | 
| **Admin** | SuperUser | CRUD possible sur tout les objects |
| **Auteur** | Créateur d'un object (`project` `issue` `comment`)| CRUD possible sur l'object dont il est l'auteur |
| **Moderator** | Permission = `Moderator` dans les contributeurs d'un projet | `PUT`/`GET` possible sur tout les objects du projet  |
| **Contributor** | Permission = `Contributor` dans les contributeurs d'un projet | `GET` possible sur tout les listes/objects du projet |
| **Non-Contributor** | N'est pas inscrit dans les contributeurs d'un projet | Ne peut qu'accéder à l'aperçu d'un projet |
| **Non-Connecté** | Utilisateur non connecté | Accès aux pages d'enregistrement et de connection uniquement |

> Lors de la création d'un nouveau projet, l'auteur obtient automatiquement le statut de `Moderator`.