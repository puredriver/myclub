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

## Deployment Hinweise
* Benutze ein ".env" Datei zum Setzen des SECRET_KEY und der DB Zugriffsdetails in "myclub/settings.py" z. B. wie hier beschrieben:
https://help.pythonanywhere.com/pages/environment-variables-for-web-apps/

## Mögliche Features
* Rankinglist Stats z. B. die meisten Spiele
* Startseite 20 Spiele mit link auf "Alle Spiele"
* "Alle Spiele" mit Jahresfilter 2020, 2019 etc
* Ranglisten "deaktivieren" damit die Statistiken von neu anfangen, aber die Spiele / Ranking erhalten bleiben
* Usermanagement: Login, Registrierung, Passwort vergessen
* Herausforderungen aussprechen und anzeigen
* Spieleingabe Wizard für eingeloggten User
* Doppel Rangliste
