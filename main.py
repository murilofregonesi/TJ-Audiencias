from db import *
from gui import *

if __name__ == '__main__':
    
    # Database
    db = Database()

    # GUI
    root = QApplication(sys.argv)
    app = WindowAudiencias(db)
    app.show()
    sys.exit(root.exec_())