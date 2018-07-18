from . import takibi

def main():
    db = takibi.Database(takibi.db_file)
    d = takibi.Deck(db)
    m = takibi.Menu(d)

def takibiPath():
    print(takibi.file_path)