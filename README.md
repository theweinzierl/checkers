# Simple Checkers

## About
Simple Checkers ist eine einfache Checkers-Version, die in Python geschrieben wurde. Kein fertiges Checkers-Game!
![demoscreen](demoscreen.png)

## Projektbeschreibung
Das Spiel besteht aus folgenden Hauptklassen:
- **Board:** Repräsentiert das Spielbrett und beinhaltet Funktionen zum Zeichen des Bretts und der Spielsteine. Verwaltet Angaben zum Spielmodi sowie die Steine der Spieler. Mit executeMove() und changeTurn() sind auch die wesentlichen Funktionen bzgl. des Tätigens eines Spielzuges enthalten.
- **Stone:** Repräsentiert einen einzelnen Spielstein. Speichert z.B. die Position des Spielsteins, mögliche Züge und den Typ (normal oder König).
- **PathTree:** Ein PathTree speichert die möglichen Züge in einer Baumstruktur. Da in Checkers Mehrfachsprünge möglich sind, können sich in einer bestimmten Spielsituation für einen Stein verschiedene Sprungmöglichkeiten ergeben.
- **Move:** Ein Move entspricht einem Zug. Im Gegensatz zum PathTree enthält ein Move keine Information über die "Zwischensprünge", d.h. es werden nur Informationen 
zur Endposition und eine Liste der übersprungenen Steine gespeichert. Wichtig ist zudem, dass ein Move-Objekt eine Evaluierungs-Funktion enthält, welche die Güte des Spielzugs bewertet. Dies ist für die Berechnung und Auswahl eines optimalen Spielzuges entscheident.
- **Brain:** Die Brain-Klasse enthält die eigentliche Spiellogik und zwar zum einen die rekursive Berechnungsfunktion eines PathTrees und zum anderen die Implementierung des MiniMax-Alogrithmus, d.h. der eigentlichen KI.

Der grundsätzliche Spielablauf sieht folgendermaßen aus:
- Für jeden Stein des an der Reihe befindlichen Spielers wird ein PathTree erstellt, d.h. die möglichen Züge berechnet. Ein menschlicher Spieler klickt dann auf einen Stein und führt den gewünschten Zug aus (Achtung: Schlagzwang wird nicht durchgesetzt, da dies zum Testen besser war.)
- Die KI hingegen startet nurn eine Rekursion und ruft abwechselnd die max() und min() Funktion auf.
- Die max()-Funktion wählt dabei den für die KI besten Zug in Abhängigkeit von der unten erläuterten Bewertungsfunktion auf. Simuliert diesen Spielzug und ruft danach die min()-Funktion auf.
- Die min()-Funktion wählt schließlich den für den Gegner schlechtesten Zug aus, simuliert diesen und ruft wiederum die max()-Funktion auf usw...
- Daraus ergibt sich ein beliebig tiefer Baum an Spielzügen, wobei theoretisch alle Spielzüge vorberechnet werden könnten. Die maximale Tiefe ist mit 4 voreingestellt, was auf dem Testrechner bereits einige Berechnungszeit beanspruchte. Die Spieltiefe kann in der settings.py-Datei eingestellt werden.

## kritische Würdigung
Die Güte der KI steht und fällt mit der Bewertung der einzelnen Züge. In der vorliegenden Checkers-Implementierung wird ein Zug nach folgenden Gesichtspunkten bewertet:
- Anzahl der übersprungenen Steine * 1000
- Sprung ins Zentrum + 100
- Sprung, damit Stein zum König wird + 200
- Ein Zufallsparamter, um eine zufällige Auswahl aus gleichwertigen Sprüngen zu gewährleisten (Ansonsten kommt es zu vorhersehbaren Sprungmustern der KI!)

Dabei handelt es sich um eine sehr einfache Bewertungsfunktion. Insbesondere wird nicht bewertet, ob der Stein in eine exponierte Position bewegt wird. Die KI nimmt also keine Rücksicht darauf, ob der eigene Stein im nächsten Zug vom Gegner geschlagen werden kann.

## geplante Features
- Punkteanzeige
- automatischer Spielneustart
