# CSV Floor Sketcher

## Verwendung
### Verwendung als Python-Skript
1. Erstelle eine virtuelle Umgebung:
    ```
    python -m venv venv
    ```

2. Aktiviere die virtuelle Umgebung:
    - **Windows**: `venv\Scripts\activate`
    - **Mac/Linux**: `source venv/bin/activate`

3. Installiere die Abhängigkeiten:
    ```
    pip install -r requirements.txt
    ```

4. Skript ausführen
    ```
    python CSVFloorSketcher.py <PATH TO DATA.csv>
    ```

### Verwendung als Standalone
* "Normaler" Aufruf mittels cmd
    ```
    CSVFloorSketcher_v<VERSION>.exe <PATH TO DATA.csv>
    ```

* Aufruf der Hilfe-Option mittels cmd 
    ```
    CSVFloorSketcher_v<VERSION>.exe -h
    ```

## Mitarbeit

### Virtuelle Umgebung erzeugen
1. cmd auf Projekt-Verzeichnis
2. Virtuelle Umgebung erzeugen
   ```
   python -m venv venv
   ```
3. Abhängigkeiten installieren:
    ```
    pip install -r requirements.txt
    ```



### Speichern von Abhängigkeiten
```
pip freeze > requirements.txt
```	
    

### Release erzeugen
```
pyinstaller build.spec
```




# FAQ
* pip SSLCertVerificationError
	```
	pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org <package_name>
	```