# Construction Plan Creator
## Installation

1. Erstelle eine virtuelle Umgebung:
    ```bash
    python -m venv venv
    ```

2. Aktiviere die virtuelle Umgebung:

    - **Windows**: `venv\Scripts\activate`
    - **Mac/Linux**: `source venv/bin/activate`

3. Installiere die Abhängigkeiten:

    ```bash
    pip install -r requirements.txt
    ```

## Speichern von Abhängigkeiten:
    
	```bash
    pip freeze > requirements.txt
    ```

## Verwendung

    ```bash
    python ConstructionPlanCreator.py <PATH TO DATA.csv>
    ```

    ```bash
    ConstructionPlanCreator_v<VERSION>.exe <PATH TO DATA.csv>
    ```

## Release

    ```bash
    pyinstaller build.spec
    ```


## FAQ
* pip SSLCertVerificationError
	```bash
	pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org <package_name>
	```