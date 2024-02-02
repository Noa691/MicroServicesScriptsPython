import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QGridLayout, QSpacerItem, QSizePolicy,QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt
import subprocess

import sys

pressed = False
class ScriptRunnerThread(QThread):
    
    output_signal = pyqtSignal(str)
    stopped_signal = pyqtSignal()
    error_signal = pyqtSignal()

    def __init__(self, script_path):
        super().__init__()
        self.script_path = script_path
        self.process = None  # Inicializar la referencia al proceso como None

    def run(self):
        try:
            self.process = subprocess.Popen(['python', self.script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            while self.process and self.process.poll() is None:
                line = self.process.stdout.readline()
                if line:
                    self.output_signal.emit(line.strip())
            if self.process:
                self.process.stdout.close()
                self.process.wait()
        except Exception as e:
            self.error_signal.emit()  # Emite una señal de error
            self.process = None
            self.start()

    def stop(self):
        if self.process:
            self.process.terminate()  # Enviar señal de terminación al proceso
            self.stopped_signal.emit()  # Emitir la señal de detención
            self.process = None


class Panel(QWidget):
    
    def __init__(self, parent=None, panel_id=0):
        super().__init__(parent)
        self.panel_id = panel_id
        self.runner = None 
        self.isScriptRunning = False
        self.initUI()
        
        
        self.script_paths = {
            0: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\AlertsEmailQAWarehouseInventory\\checkForAlerts.py",
            1: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\AlertasEmailPythonMaintenanceApp\\AlertsEmailDueMaintenancesPastMonth.py",
            2: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\AlertasEmailPythonMaintenanceApp\\AlertsEmailMaintenance.py",
            3: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\AlertsEmailBestBuyMSFT\\checkForAlertsMSFTBestBuy.py",
            4: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\ConverterPDFJrz\\checkForFilesSharePoint.py",
            5: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\ConverterPDFJrz\\converter.py",
            6: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\ConverterPDFJrz\\UpdateFilesSharePoint.py",
            7: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\ExecuteDataForDownTimeReports\\ExecuteDataForDownTime.py",
            8: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\ReportInOutDysonMontly\\ReceivedShippedDysonMontly.py",
            9: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\ProjectReportDaily\\DailyTest.py",
            10: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\ProjectReportDaily\\runvba.py",
            11: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\ProjectReportDaily\\sendreport.py",
            12: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\ProjectReportDailyMSFT\\dailyrunMSFT.py",
            13: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\ProjectReportDailyMSFT\\runvbamsft.py",
            14: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\ProjectReportDailyMSFT\\sendreportmsft.py",
            15: r"C:\\Users\\ELP-SERVER1\\Documents\\ScriptsPythonPograms\\TokenGeneratorAPI\\generatorToken.py",
            
            
            
            
            
            
            
           
            # ... y así sucesivamente para cada panel_id
        }
        

    def initUI(self):
        # Usar un QGridLayout para el panel
        grid = QGridLayout()
        
        
        self.playButton = self.createStartButton(self.onStartClicked, self.panel_id)
        grid.addWidget(self.playButton, 1, 0)
        self.stopButton = self.createStopButton(self.onStopClicked, self.panel_id)
        grid.addWidget(self.stopButton, 3, 0)

        # Configurar el tamaño de los botones
        self.playButton.setFixedSize(65, 40)  # 1 pulgada x 1 pulgada
        self.stopButton.setFixedSize(65, 40)  # 1 pulgada x 1 pulgada

        # Crear la ventana de texto
        self.textWindow = QTextEdit(self)
        self.textWindow.setObjectName(f"textWindow_{self.panel_id}")
        #self.textWindow.setFixedSize(288, 192)  # 3x2 pulgadas
        self.textWindow.setFixedSize(240, 192)  # 3x2 pulgadas
        self.textWindow.setStyleSheet("background-color: #0F0F0F; color: green;")  # Estilo Matrix
        grid.addWidget(self.textWindow, 1, 1, 3, 1)
        titleWindow = self.createTitleWindow(self.panel_id)
        grid.addWidget(titleWindow, 0, 1)
        # Añadir botones y ventana de texto al grid
        #grid.addWidget(self.playButton, 0, 0)  # Primera fila, primera columna
        #grid.addWidget(self.stopButton, 0, 0)  # Segunda fila, primera columna
       #grid.addWidget(self.textWindow, 0, 1, 3, 1)  # Abarca tres filas, segunda columna

        # Añadir un espaciador para empujar los botones hacia arriba
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        grid.addItem(spacer, 2, 0)  # Tercera fila, primera columna
        
       # Define y añade la primera luz
        self.light1 = QLabel(self)
        self.light1.setFixedSize(20, 20)
        self.light1.setStyleSheet("background-color: red; border-radius: 0px;")
        
        #self.playButton = self.createStartButton(self.onStartClicked, self.panel_id)
        #grid.addWidget(self.playButton, 0, 0)
        #self.stopButton = self.createStopButton(self.onStopClicked, self.panel_id)
        #grid.addWidget(self.stopButton, 1, 0)
        
        # Crea un layout vertical y añade la luz a este layout
        vLayout = QVBoxLayout()
        vLayout.addWidget(self.light1)
        vLayout.setAlignment(self.light1, Qt.AlignCenter)  # Centra la luz en el layout vertical

        # Crea un layout horizontal y añade el layout vertical
        hLayout = QHBoxLayout()
        hLayout.addLayout(vLayout)
        hLayout.setAlignment(Qt.AlignCenter)  # Centra el layout vertical en el layout horizontal

        # Añade el layout horizontal al grid
        grid.addLayout(hLayout, 2, 0)
        self.setLayout(grid)

        # Configura y inicia el temporizador para el parpadeo
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.toggleLight1)
        self.timer1.start(500)

        self.light1On = False
        self.paradeMode = "red-white"
        self.setLayout(grid)

    def toggleLight1(self):
        if self.paradeMode == "red-white":
            newColor = "#CE5353" if self.light1On else "#E0392E"
        elif self.paradeMode == "blue-green":
            newColor = "green" if self.light1On else "#1565C0"
        elif self.paradeMode == "green-white":
            newColor = "#5EF6A6" if self.light1On else "#02a356"

        self.light1.setStyleSheet(f"background-color: {newColor}; border-radius: 1px;")
        self.light1On = not self.light1On

    def changeParadeMode(self):
        self.paradeMode = "blue-green"

    
    def createTitleWindow(self, panel_id):
        title = QLabel(self)  # Crear un QLabel como título

        if panel_id == 0:
            title.setText('Check For Alerts DysonWHInventoryQA')
        elif panel_id == 1:
            title.setText('Alerts Email DueMaintenancesPast')
        elif panel_id == 2:
            title.setText('Alerts Email Maintenance')
        elif panel_id == 3:
            title.setText('Check For Alerts MSFTBestBuy')
        elif panel_id == 4:
            title.setText('ConverterPDF CheckForFilesSharePoint')
        elif panel_id == 5:
            title.setText('ConverterPDF Converter')
        elif panel_id == 6:
            title.setText('ConvertPDF UpdateFilesSharePoint')
        elif panel_id == 7:
            title.setText('Script For Execute Dyson DataForDownTime')
        elif panel_id == 8:
            title.setText('ReceivedShippedDysonMonthly')
        elif panel_id == 9:
            title.setText('DSUReport GetCloudDBData')
        elif panel_id == 10:
            title.setText('DSUReport Execute VBA')
        elif panel_id == 11:
            title.setText('DSUReport Send Report')
        elif panel_id == 12:
            title.setText('MSFTReport GetCloudDBData')
        elif panel_id == 13:
            title.setText('MSFTReport Execute VBA')
        elif panel_id == 14:
            title.setText('MSFTReport Send Report')
        elif panel_id == 15:
            title.setText('Token Generator API')
        else:
            title.setText('Unknown Script')

        title.setStyleSheet("font-weight: bold; color: #1565C0; font-size: 13px")
          # Estilo en negrita y color azul
        title.setAlignment(Qt.AlignCenter)  # Centrar el texto

        return title
 
                
   

    def createStartButton(self, action, panel_id):
        button = QPushButton(f"Start", self)
        button.setObjectName(f"startButton_{panel_id}")
        button.setStyleSheet("QPushButton {background-color: #02a356; color: white; font-weight: bold; border: none;}")
        button.setCursor(Qt.PointingHandCursor)  # Esta línea establece el cursor de mano
        button.clicked.connect(lambda: action(panel_id))
        return button

    def createStopButton(self, action, panel_id):
        button = QPushButton(f"Stop", self)
        button.setObjectName(f"stopButton_{panel_id}")
        button.setStyleSheet("QPushButton {background-color: #1565C0; color: white; font-weight: bold; border: none;}")
        button.setCursor(Qt.PointingHandCursor)  # Esta línea establece el cursor de mano
        button.clicked.connect(lambda: action(panel_id))
        return button

    
    def onStartClicked(self, panel_id): 
        button = self.findChild(QPushButton, f"startButton_{panel_id}")
        button.setStyleSheet("background-color: #018336; color: white;")

        self.textWindow.clear()
        self.isScriptRunning = True
        script_path = self.script_paths.get(panel_id)
        if script_path:
            self.runner = ScriptRunnerThread(script_path)
            self.runner.output_signal.connect(self.updateTextWindow)
            self.runner.stopped_signal.connect(self.onScriptStopped)
            self.runner.start()
        # Cambiar el modo de parpadeo a verde y blanco
        self.paradeMode = "green-white"
        self.light1On = False  # Reiniciar el estado del foco
        QTimer.singleShot(1000, lambda: button.setStyleSheet("background-color: #02a356; color: white; font-weight: bold; border: none;"))
       
    
    def onStopClicked(self, panel_id):
        button = self.findChild(QPushButton, f"stopButton_{panel_id}")

    # Cambiar el estilo del botón para indicar que está presionado
        button.setStyleSheet("background-color: #1043A0; color: white;")  # Un tono de azul más oscuro

        if self.isScriptRunning and self.runner:
            self.stopScript()
            self.paradeMode = "red-white"
            self.light1On = False  # Reiniciar el estado del foco

        # Restablecer el estilo original del botón después de 1 segundo
        QTimer.singleShot(1000, lambda: button.setStyleSheet("background-color: #1565C0; color: white; font-weight: bold; border: none;"))

    def stopScript(self):
        if self.isScriptRunning and self.runner:
            self.runner.stop()
            self.isScriptRunning = False
    
    def onScriptStopped(self):
        self.textWindow.append(">>>>>>>>>>>>>>>>>>>>>>>>>>>>The script was stopped")
    
    def updateTextWindow(self, text):
        self.textWindow.append(text)


class MyApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.panels = []
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle("<<Micro Services RLJones ELP App>>")
        self.setGeometry(100, 100, 1200, 800)  # Tamaño de la ventana principal
        self.setWindowIcon(QIcon('Images\\logo.png'))
        self.setStyleSheet("background-color: #0A0A0A;")  # Azul oscuro

        # Layout de cuadrícula para la ventana principal
        grid = QGridLayout()
        self.setLayout(grid)

        # Crear y añadir 15 paneles al grid
        for i in range(16):
            panel = Panel(self, panel_id=i)
            self.panels.append(panel)
            grid.addWidget(panel, i // 4, i % 4)

    def playAction(self):
        print("Play action")
        for panel in self.panels:
            panel.changeParadeMode() 

    def stopAction(self):
        print("Stop action")
        for panel in self.panels:
            panel.changeParadeMode() 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApplication()
    ex.show()
    sys.exit(app.exec_())
