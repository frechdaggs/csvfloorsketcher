### Backlog
#### Unterscheidung zwischen berechneten und gewussten Maßen
Es muss möglich sein, bei Bemaßungen angeben zu können, ob ein Maß berechnet bzw. sich ergeben hat oder ob eine Bemaßung wissentlich eingetragen wurde.


#### Fehler: Referenzierung auf Punkte in der Payload schein nicht richtig zu funktionieren
Wird in der Payload auf bereits angelegte Punkte verwiesen, scheint es so, als würde der referenzierte Punkt falsch ausgerechnet.
Bsp:
"Haus","2-OG1","Outline",,"(0,0)","(0,0)","(400,0)","(400,-20)","(730,-20)","(730,1020)","(430,1020)","(430,870)","(0,870)",,,,,,,,,
"Bad","2-OG1","Room",,"(442,845)","(0,0)","(0,-256)","(60,-256)","(60,-296)","(280,-296)","(280,0)",,,,,,,,,,,
"Loggia","2-OG1","Room",,"(Bad-1)+(0,25)","(0,0)","(Bad-6)+(0,25)","(Haus-5)+(-9,-25)","(Haus-6)+(25,-25)",,,,,,,,,,,,,


#### Wasserzeichen in einfügen
Am Rand der Zeichnung soll erscheinen, dass der Plan mit diesem Tool inklusive Version und GitHub-URL erzeugt wurde.

#### "Debug"-Elemente ermöglichen
Es soll möglich sein über eine neue "Debug"-Spalte Einträge ausschließlich im Debug-Modus anzeigen zu lassen.

#### Fehler: Im Debug-Mode stimmt die Index-Beschriftung der Punkte nicht.
Die Index-Beschriftung soll entsprechend der Referenzierungslogik geschehen. Also mit 1 anstelle von 0 beginnen.

#### Dachschrägen
Es soll möglich sein, einen Dachschrägen im Plan einzeichnen zu können.

#### Höhenprofil
Die Beschriftung des Plan soll um Höhen-Angaben erweiterbar sein. Eine Höhen-Angabe besteht aus einer unteren und oberen Höhe und ist Raum- bzw. Partspezifisch angebbar

#### Angabe mehrerer Ebenen
Es soll möglich sein, einen Eintrag mehreren Ebenen zuzuweisen. Bspw. ist es für die "Outline" hilfreich, wenn sie für alle Ebenen gilt.


### Next: v00.001.02
#### #0006: Erzeugung von svg optional
Die Erzeugung der svg-Datei ist mehr ein Zwischenschritt als ein Feature. Im manchen Situationen - insb. zur Weiterverarbeitung - kann kann es jedoch tatsächlich Hilfreich sein, die svg-Datei zu erhalten. In allen anderen Fällen sind die svg-Dateien unnötiger Datenmüll. Die Erzeugung der svg-Dateien soll also optional aktiviert werden können.

### Release: v00.001.01
#### #0001: Bemaßungen müssen einheitliche Referenz haben
Für Bemaßungen die nicht die gleichen x- bzw. y-Werte haben liegt die Bemaßungszahl auf der Diagonale. Darüberhinaus können Bemaßungen mit Offset nicht an einander ausgerichtet werden. Hierfür ist wäre Referenzpunkt notwendig. Ist dieser nicht vorgegeben muss einer der beiden Beaßungspunkte als Referenzpunktherangezogen werden.

#### #0002: Debug-Modus
* Es soll beim Übersetzen des Bauplans möglich sein eine "Debug"-Option zu aktivieren.
* Der Debug Modus soll durch das optionale Programm-Argument '--debug' aktiviert werden
* Im Debug Modus sollen folgende zusätzliche Informationen ersichtlich sein, die das Zeichnen des Plans erleichtern
  * Indices der Punkte in Pfad-Shapes zur einfacheren Positionierung
  * Indentifiers der Parts
  * Achsen-Kreuz

#### #0003: Leerzeilen in der CSV
Zu besseren Strukturierung soll es möglich sein, dass in der csv-Datei Leerzeilen enthalten sind.

#### #0004: Beschriftung der Räume
Es soll möglich sein, die Räume mit Namen zu versehen.

#### #0005: Treppenläufe
Es soll möglich sein, einen Treppenlauf im Plan einzeichnen zu können.

### Release: v00.001.00

