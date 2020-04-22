# myclub - kleine Anwendung zur Verwaltung einer Tennisclub Rangliste

## Technology
Python 3.8, Django 2.2.7, Mysql etc

## Versionshinweise

### v0.1.0
* Startseite zur Ansicht von Ranglisten und Spielen
* Button zur Ansicht der Regelwerks
* Spielerhistorie beim Klick auf den Spieler in der Rangliste
* Admin Funktionalität zur Bearbeitung von Ranglisten, Spielern, Ranglisten Positionen
* Automatische Ranglistenverschiebung (Positionswechsel) bei Eingabe eines Spiels durch den Admin

### v0.2.0
* Ranglisten Statistiken eingeführt für "die meisten Spiele"
* Startseite zeigt nur die letzten 10 Spiele an > Button für Spielearchiv
* Spielarchiv mit Jahresauswahl neu einführt 

### v0.2.1
* Umgestellt auf Django User Modell anstatt Player

### v0.2.2
* Ranglisten "deaktivieren" im Admin damit die Statistiken von neu anfangen, aber die Spiele / Ranking erhalten bleiben
* Aktuelle Herausforderungen hinzugefügt
* Neue Button "Tabelle" bei der Rangliste zum ein- und ausblenden

### v0.2.3
* Startseite hinsichtlichen Spieletabellen angepasst
* Bugfix: Name auf Spielerhistorie wird nicht angezeigt

### v0.2.4
* Admin Listen und Formulare optimiert
* Einführung von Ranglisten Admins und entsprechender Berechtigungen

### v0.2.5
* Spiel Validierungen bei fehlender Ranglisten Position der Spieler

### v0.3.0
* Einführung des Modell für Clubs
* Neue Rollen im Admin "ClubAdmin" und "RankingAdmin" und Berechtigungen

## Deployment Hinweise
* Benutze ein ".env" Datei zum Setzen des SECRET_KEY und der DB Zugriffsdetails in "myclub/settings.py" z. B. wie hier beschrieben:
https://help.pythonanywhere.com/pages/environment-variables-for-web-apps/

## Mögliche Features
* Tendenz eines Spielers in der Rangliste anzeigen
* Usermanagement: Login, Registrierung, Passwort vergessen
* Herausforderungen aussprechen und anzeigen
* Spieleingabe Wizard für eingeloggten User
* Regelwerk kann modifiziert werden
* Doppel Rangliste
