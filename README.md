Takibi.py
===

Takibi is a cli flashcard application. It only has basic functionality and no error messaging.

Installing
----------

Install takibi in a location that you can easily access, as adding new words is done through editing `takibi/db/import.csv`.

To install takibi, download it and then in the top directory run:

`pip3 install -e .`

Then you can call it from the command line with `takibi`.

To test takibi after installing, run the program and try importing the test word added to the `import.csv` file.

Usage
-----

To use takibi, call it from the command line along:

`takibi`

This will load the menu, which gives you 4 options:

1. study
2. save
3. import
4. quit

**Study**: begin a study session for any cards that require review.

**Save**: save the deck in its current state to the database (`db.csv`).

**Import**: import cards from `import.csv`. Clear all entries from `import.csv` after importing.

**Quit**: save and quit the application.

To add new words to takibi, enter them into `import.csv` then import them from the takibi application.

Path info
---------

Enter `takibi-path` to get the path to the takibi folder.

🔥🍞🔥
