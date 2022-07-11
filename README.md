# dbd_stats

This application can generate statistics about the **Dead by Daylight** game end result screenshots.
It uses **Pillow** to crop the small images and in case of perks change the background to uniform black.
It uses tensorflow to recognise the killer, the killer's rank and the killer's perks.
The application has a UI created in flask

## Requirements

- Python 3.10+
- Flask 2.1.0
- Pillow 8.3.2
- tensorflow 2.9.1
- numpy 1.23.0
- scipy 1.8.1

## Run the application

1. You need to install the required dependencies

 ```
pip install -r requirements.txt
```

2. In the src folder you can start the flask application with the following command.
```
flask run --host=0.0.0.0
```

3. Open the http://localhost:5000/ page in a browser.
