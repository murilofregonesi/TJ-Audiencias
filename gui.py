from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QCheckBox, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
import sys

class WindowAudiencias(QWidget):

    def __init__(self, db, parent=None):
        super(WindowAudiencias, self).__init__(parent)
        self.db = db
        self.setWindowIcon(QIcon("static/logo.ico"))
        self.setWindowTitle("Audiências do Tribunal de Justiça")
        self.resize(800, 600)

        # buttons
        x_btn = 600
        y_btn_gap = 20
        y_btn_step = 50

        def create_button(window, on_click, text, tip, pos):
            button = QPushButton(text, window)
            button.setToolTip(tip)
            button.move(x_btn, y_btn_gap + y_btn_step * pos)
            button.clicked.connect(on_click)
            button.resize(150, 40)
            return button

        self.btn_insert_audiencia = create_button(self, self.on_click_insert_audiencia, 
            'Inserir Audiência', 'Criar uma nova Audiência no banco de dados.', 0)
        self.btn_update_audiencia = create_button(self, self.on_click_update_audiencia, 
            'Atualizar Audiência', 'Atualizar uma Audiência do banco de dados.', 1)
        self.btn_delete_audiencia = create_button(self, self.on_click_delete_audiencia, 
            'Remover Audiência', 'Remover uma Audiência do banco de dados.', 2)
        self.btn_atividades = create_button(self, self.on_click_open_atividades, 
            'Atividades da Audiência', 'Abrir a janela de atividades da Audiência.', 3)

        # labels
        def create_label(window, text, x, pos):
            label = QLabel(window)
            label.setText(text)
            y_gap = 20
            y_step = 50
            label.move(x, y_gap + pos * y_step)
            return label

        x_in_1 = 50
        x_in_2 = 220

        self.lbl_vara = create_label(self, 'Vara', x_in_1, 0)
        self.lbl_processo = create_label(self, 'Processo', x_in_1, 1)
        self.lbl_tipo = create_label(self, 'Tipo', x_in_1, 2)
        self.lbl_audiencias = create_label(self, 'Audiências', x_in_1, 4)

        self.lbl_horario = create_label(self, 'Horário', x_in_2, 0)
        self.lbl_data_audiencia = create_label(self, 'Data Audiência', x_in_2, 1)
        self.lbl_data_despacho = create_label(self, 'Data Despacho', x_in_2, 2)

        # inputs
        y_gap = 37
        y_step = 50

        def create_line_edit(window, x, pos):
            line_edit = QLineEdit(window)
            line_edit.move(x, y_gap + pos * y_step)
            line_edit.resize(150, 24)
            return line_edit

        self.line_processo = create_line_edit(self, x_in_1, 1)
        self.line_horario = create_line_edit(self, x_in_2, 0)
        self.line_data_audiencia = create_line_edit(self, x_in_2, 1)
        self.line_data_despacho = create_line_edit(self, x_in_2, 2)

        # combo-box
        def create_cb(window, list_items, x, pos):
            combo_box = QComboBox(window)
            combo_box.addItems(list_items)
            combo_box.move(x, y_gap + pos * y_step)
            combo_box.resize(150, 24)
            return combo_box

        self.cb_vara = create_cb(self, ["1", "2"], x_in_1, 0)
        self.cb_tipo = create_cb(self, ["Tipo 1", "Tipo 2", "Tipo 3"], x_in_1, 2)

        # check-box
        self.ck_urgente = QCheckBox("Urgente", self)
        self.ck_urgente.move(x_in_1, y_gap-17 + 3 * y_step)

        # table
        self.table_audiencias = QTableWidget(self)
        self.table_audiencias.move(50, 240)
        self.table_audiencias.resize(700, 300)
        self.table_audiencias.itemSelectionChanged.connect(self.table_audiencias_select)
        self.set_table_audiencias_content()


    # table functions
    def set_table_audiencias_content(self):
        audiencias = self.db.get_audiencias()

        if (len(audiencias) > 0):
            self.table_audiencias.setRowCount(len(audiencias))
            self.table_audiencias.setColumnCount(len(audiencias[0]))
            self.table_audiencias.setHorizontalHeaderLabels(list(self.db.get_audiencia_columns()))
            
            for row, audiencia in enumerate(audiencias):
                for column, cell in enumerate(audiencia):
                    self.table_audiencias.setItem(row, column, QTableWidgetItem(cell))
        else:
            self.table_audiencias.clear()

    def table_audiencias_select(self):
        currentRow = self.table_audiencias.currentRow()
        select_processo = self.table_audiencias.item(currentRow, 1)
        select_data_audiencia = self.table_audiencias.item(currentRow, 5)

        if (select_processo and select_data_audiencia):
            select_processo = select_processo.text()
            select_data_audiencia = select_data_audiencia.text()
            # set values to fields
            self.line_processo.setText(select_processo)
            self.line_data_audiencia.setText(select_data_audiencia)

    # get data functions
    def get_ck_urgente(self):
        return self.ck_urgente.checkState()

    def get_cb_vara(self):
        return self.cb_vara.currentText()

    def get_cb_tipo(self):
        return self.cb_tipo.currentText()

    def get_line_processo(self):
        return self.line_processo.text()

    def get_line_horario(self):
        return self.line_horario.text()

    def get_line_data_audiencia(self):
        return self.line_data_audiencia.text()

    def get_line_data_despacho(self):
        return self.line_data_despacho.text()

    # button functions
    def on_click_insert_audiencia(self):
        self.db.insert_audiencia(vara=self.get_cb_vara(), 
                                 processo=self.get_line_processo(), 
                                 tipo=self.get_cb_tipo(), 
                                 urgente=self.get_ck_urgente(), 
                                 horario=self.get_line_horario(), 
                                 data_audiencia=self.get_line_data_audiencia(), 
                                 data_despacho=self.get_line_data_despacho())
        self.set_table_audiencias_content()

    def on_click_delete_audiencia(self):
        currentRow = self.table_audiencias.currentRow()
        drop_processo = self.table_audiencias.item(currentRow, 1)
        drop_data_audiencia = self.table_audiencias.item(currentRow, 5)

        if (drop_processo and drop_data_audiencia):
            drop_processo = drop_processo.text()
            drop_data_audiencia = drop_data_audiencia.text()
            self.db.delete_audiencia(drop_processo, drop_data_audiencia)
            
            print('Audiência removida do banco de dados.')
            self.set_table_audiencias_content()

    def on_click_update_audiencia(self):
        currentRow = self.table_audiencias.currentRow()
        update_processo = self.table_audiencias.item(currentRow, 1)
        update_data_audiencia = self.table_audiencias.item(currentRow, 5)

        if (update_processo and update_data_audiencia):
            update_processo = update_processo.text()
            update_data_audiencia = update_data_audiencia.text()
            self.db.update_audiencia(vara=self.get_cb_vara(), 
                                     processo=update_processo, 
                                     tipo=self.get_cb_tipo(), 
                                     urgente=self.get_ck_urgente(), 
                                     horario=self.get_line_horario(), 
                                     data_audiencia=update_data_audiencia, 
                                     data_despacho=self.get_line_data_despacho())
            self.set_table_audiencias_content()

    def on_click_open_atividades(self):
        print('on_click_open_atividades click') # TODO
        
