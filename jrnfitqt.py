import os
from PyQt5 import QtWidgets, QtCore, QtGui
import datetime

entriesDict = {}

class CalendarWidget(QtWidgets.QCalendarWidget):

    def paintCell(self, painter, rect, date):
        # painter.setRenderHint(QtWidgets.QPainter.Antialiasing, True)

        pydate = date.toPyDate()

        if entriesDict.__contains__(pydate):
            QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)
            painter.save()
            # painter.drawRect(rect)
            painter.setPen(QtGui.QColor(168, 34, 3))
            painter.setFont(QtGui.QFont('Decorative', 10))            
            # painter.drawText(QtCore.QRectF(rect), QtCore.Qt.TextSingleLine|QtCore.Qt.AlignCenter, str(date.day()))
            painter.drawText(rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, self.parseActivityAndGetShorts(entriesDict[pydate])) 

            painter.restore()
        else:
            QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)

    def parseActivityAndGetShorts(self, entry):
        act = []
        test = entry.lower()

        if "garten" in test:
            act.append("Ga")
        if "tanzen" in test:
            act.append("Tz")
        if "laufen" in test:
            act.append("La") 
        if "radfahren" in test:
            act.append("Rf") 
        if "schwimmen" in test:
            act.append("Sw")
        if "yoga" in test:
            act.append("Y")
        if "meditation" in test:
            act.append("M")
        if "bankdrücken" in test:
            act.append("Bd")
        if "trifecta" in test:
            act.append("Tri")
        if "klimmz" in test:
            act.append("Kl")
        if "klettern" in test:
            act.append("Kt")
        if "bauchauf" in test:
            act.append("Ba")

        if "krank" in test:
            act.append("kr")

        return ",".join(act)


class Calendar(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        

        self.importAllEntries() # Alle Einträge importieren 

        # Kalender-Widget initialisieren
        self.calendar = CalendarWidget(self)
        self.calendar.setGridVisible(True)
        # self.calendar.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.LongDayNames)
        self.calendar.clicked[QtCore.QDate].connect(self.show_entries)
        self.calendar.currentPageChanged.connect(self.show_entries)
        
        # Einträge-ListWidget initialisieren
        #self.entry_list = QtWidgets.QListWidget(self)
        self.entry_list = QtWidgets.QTextEdit(self)
        self.entry_list.setMaximumHeight(150)
        
        # Layouts erstellen
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.calendar)
        layout.addWidget(self.entry_list)
        
        # Fenster-Eigenschaften festlegen
        self.setGeometry(300, 300, 450, 550)
        self.setWindowTitle("Einträge-Kalender")
        self.show()
        
        
        # Alle Einträge abrufen und Kalender markieren
        self.show_entries()
        
    def importAllEntries(self):
        # Alle Einträge aus dem Ordner importieren
        folder = "C:\\Users\\cheuer\\OneDrive\\Documents\\# Calender\\Entries"
        for filename in os.listdir(folder):
            if filename.endswith(".txt"):
                date = datetime.datetime.strptime(filename, "%Y-%m-%d.txt").date()
                with open(os.path.join(folder, filename), mode='r', encoding='utf-8') as f:
                    entry = f.read()
                    entriesDict[date] = entry


    def show_entries(self):
        selected_date = self.calendar.selectedDate().toPyDate()
        self.entry_list.clear()

       
        if entriesDict.__contains__(selected_date):
            # fill QTextEdit widget with text
            self.entry_list.setText(entriesDict[selected_date])

        
        # Kalender-Tage markieren, für die Einträge existieren
        self.calendar.setDateTextFormat(QtCore.QDate(), QtGui.QTextCharFormat()) # Markierungen entfernen


        for date in entriesDict.keys():
            #if date.year == selected_date.year and date.month == selected_date.month:
                char_format = QtGui.QTextCharFormat()
                char_format.setBackground(QtGui.QColor("#c8e6c9")) # Hintergrundfarbe setzen    
                self.calendar.setDateTextFormat(QtCore.QDate(date), char_format)
            
        
        # Aktion ausführen
        self.do_something(selected_date)
    
    def do_something(self, selected_date):
        # Diese Methode wird aufgerufen, wenn ein Datum ausgewählt wird
        print("Das ausgewählte Datum ist:", selected_date)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Calendar()
    app.exec_()