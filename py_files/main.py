import mysql.connector
from mysql.connector import errorcode
import wx
from configuration.config import config as cnf
import csv


# Adatok mentése csv fájlba
def save_to_csv(table_name, column_names, data):

    file_path = open(f'../csv_files/{table_name}.csv', 'w', encoding='utf-8')
    my_file = csv.writer(file_path, lineterminator='\n')
    my_file.writerow(column_names)
    my_file.writerows(data)
    file_path.close()


class MySQLConnector:

    # Csatlakozás az adatbázishoz config fájl adataival
    def __init__(self, config):
        self.config = config
        self.db_name = self.config["database"]

        try:
            self.cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Felhasználónév vagy jelszó nem egyezik")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Adatbázis nem létezik")
            else:
                print(err)

    # Táblák neveinek lekérése az adatbázisból
    def get_table_names(self):
        cursor = self.cnx.cursor()

        query = ("SELECT table_name "
                 "FROM information_schema.tables "
                 "WHERE table_type='BASE TABLE' "
                 f"AND table_schema = '{self.db_name}';")

        cursor.execute(query)

        table_names = []

        for (table_name,) in cursor:
            table_names.append(table_name)

        cursor.close()

        return table_names

    # Tábla adatainak lekérése az adatbázisból
    def get_table_data(self, table_name):
        cursor = self.cnx.cursor()

        query = f"SELECT * FROM {self.db_name}.{table_name};"

        cursor.execute(query)

        rows = cursor.fetchall()

        columns = [i[0] for i in cursor.description]

        cursor.close()

        return columns, rows


class GUI(wx.Frame):

    # Interfész inicializáslása
    def __init__(self, parent, title, connector):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        self.connector = connector

        self.panel = wx.Panel(self, 1, style=wx.MAXIMIZE)

        # Tábla nevek lekérése
        tables = self.connector.get_table_names()

        if len(tables) == 0:
            wx.MessageBox(message="Nem találhatók táblák!", style=wx.OK)

        # Tábla nevek táblázatba rendezése
        self.table_check_list = wx.ListCtrl(self.panel, style=wx.LC_REPORT)
        self.table_check_list.EnableCheckBoxes()
        self.table_check_list.InsertColumn(0, "Kiválaszt")
        self.table_check_list.InsertColumn(1, "Tábla név")

        for i, table in enumerate(tables):
            self.table_check_list.InsertItem(i, "")
            self.table_check_list.SetItem(i, 1, table)

        # Mentés gomb létrehozása
        save_button = wx.Button(self.panel, wx.ID_SAVE, label="Save", size=(100, 50))
        self.Bind(wx.EVT_BUTTON, self.save_button_click, save_button)

        # Kilépő gomb létrehozása
        exit_button = wx.Button(self.panel, wx.ID_EXIT, label="Exit", size=(100, 50))
        self.Bind(wx.EVT_BUTTON, self.exit_button_click, exit_button)

        choose_text = wx.StaticText(self.panel, label="Kérem, válassza ki a konvertálandó táblákat!")

        # Kinézet elrendezése
        button_sizer = wx.BoxSizer()
        button_sizer.Add(save_button, flag=wx.ALL, border=10)
        button_sizer.Add(exit_button, flag=wx.BOTTOM | wx.ALL, border=10)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(choose_text, proportion=1, flag=wx.ALL, border=10)
        main_sizer.Add(self.table_check_list, proportion=7, flag=wx.EXPAND | wx.ALL, border=10)
        main_sizer.Add(button_sizer, proportion=2, border=10)

        self.panel.SetSizerAndFit(main_sizer)

        self.Centre()
        self.Show()

    # Mentés gomb megnyomásakor kipipált négyzetek ellenőrzése és kijelölt táblák adatainak mentése
    def save_button_click(self, event):
        for i in range(self.table_check_list.GetItemCount()):
            if self.table_check_list.IsItemChecked(i):
                table_name = self.table_check_list.GetItem(i, 1).GetText()
                column_names, data = self.connector.get_table_data(table_name)
                save_to_csv(table_name, column_names, data)

        wx.MessageBox(message="Folyamat befejezve!", style=wx.OK)

    # Kilépő gombbal való kilépés
    def exit_button_click(self, event):
        self.connector.cnx.close()
        self.Close()


def main():
    connector = MySQLConnector(cnf)
    app = wx.App()
    frame = GUI(None, 'Adatbázis konverter', connector)
    app.MainLoop()


if __name__ == "__main__":
    main()
