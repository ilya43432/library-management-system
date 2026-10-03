from LibraryGUI.GUI import GUI

if __name__ == "__main__":
    path_to_csv = 'books.csv'
    app = GUI(path_to_csv)
    app.run()