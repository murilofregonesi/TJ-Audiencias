from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QCheckBox, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QLineEdit, QDateEdit, QTimeEdit
from PyQt5.QtCore import QDate, QTime, QSize
from PyQt5.QtGui import QIcon, QFont
from gui_atividades import *
import sys

class WindowAudiencias(QWidget):

    def __init__(self, db, parent=None):
        super(WindowAudiencias, self).__init__(parent)
        self.db = db
        self.setWindowIcon(QIcon("static/logo.ico"))
        self.setWindowTitle("Audiências do Tribunal de Justiça")
        self.resize(800, 600)
        self.filtered_date = False
        self.filtered_vara = False

        # buttons
        x_btn = 600
        y_btn_gap = 20
        y_btn_step = 50

        self.btn_font = QFont()
        self.btn_font.setBold(True)
        self.btn_font.setPixelSize(12)

        def create_button(window, on_click, text, tip, pos):
            button = QPushButton(text, window)
            button.setToolTip(tip)
            button.move(x_btn, y_btn_gap + y_btn_step * pos)
            button.clicked.connect(on_click)
            button.resize(150, 40)
            button.setFont(self.btn_font)
            return button

        self.btn_insert_audiencia = create_button(self, self.on_click_insert_audiencia, 
            'Inserir Audiência', 'Criar uma nova Audiência no banco de dados.', 0)
        self.btn_update_audiencia = create_button(self, self.on_click_update_audiencia, 
            'Atualizar Audiência', 'Atualizar uma Audiência do banco de dados.', 1)
        self.btn_delete_audiencia = create_button(self, self.on_click_delete_audiencia, 
            'Remover Audiência', 'Remover uma Audiência do banco de dados.', 2)
        self.btn_atividades = create_button(self, self.on_click_open_atividades, 
            'Atividades Audiência', 'Abrir a janela de atividades da Audiência.', 3)
        
        # filter buttons
        def create_filter_button(window, on_click, icon, tip, x):
            filter_button = create_button(window, on_click, '', tip, 3.5)
            filter_button.setIcon(QIcon('./static/{}'.format(icon)))
            filter_button.resize(40, 40)
            filter_button.move(x, y_btn_gap + y_btn_step * 3.5)
            filter_button.setIconSize(QSize(25, 25) )
            return filter_button

        self.btn_filter_vara = create_filter_button(self, self.on_click_filter_vara, 
            'filter.png', 'Filtrar Audiências pela Vara.', 300)
        self.btn_filter_date = create_filter_button(self, self.on_click_filter_date, 
            'filter.png', 'Filtrar Audiências por data da Audiência.', 350)
        self.btn_remove_filter_date = create_filter_button(self, self.on_click_remove_filters, 
            'rm_filter.png', 'Remover filtros das Audiências.', 400)

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

        create_label(self, 'Vara', x_in_1, 0)
        create_label(self, 'Processo', x_in_1, 1)
        create_label(self, 'Tipo', x_in_1, 2)
        create_label(self, 'Audiências', x_in_1, 4)

        create_label(self, 'Horário', x_in_2, 0)
        create_label(self, 'Data Audiência', x_in_2, 1)
        create_label(self, 'Data Despacho', x_in_2, 2)

        # line edit
        y_gap = 37
        y_step = 50

        def create_line_edit(window, x, pos):
            line_edit = QLineEdit(window)
            line_edit.move(x, y_gap + pos * y_step)
            line_edit.resize(150, 24)
            return line_edit

        self.line_processo = create_line_edit(self, x_in_1, 1)

        # date edit
        def create_date_edit(window, x, pos):
            date_edit = QDateEdit(self)
            date_edit.move(x, y_gap + pos * y_step)
            date_edit.resize(150, 24)
            return date_edit

        self.date_data_audiencia = create_date_edit(self, x_in_2, 1)
        self.date_data_despacho = create_date_edit(self, x_in_2, 2)

        # time edit
        self.time_horario = QTimeEdit(self)
        self.time_horario.move(x_in_2, y_gap + 0 * y_step)
        self.time_horario.resize(150, 24)

        # combo-box
        def create_cb(window, list_items, x, pos):
            combo_box = QComboBox(window)
            combo_box.addItems(list_items)
            combo_box.move(x, y_gap + pos * y_step)
            combo_box.resize(150, 24)
            return combo_box

        self.cb_vara = create_cb(self, ["1", "2"], x_in_1, 0)
        self.cb_tipo = create_cb(self, ["Instrução e Julgamento", "Oitiva", "Interrogatório", "Depoimento Especial", "UNA", "Continuação", "Carta Precatória"], x_in_1, 2)

        # check-box
        self.ck_urgente = QCheckBox("Urgente", self)
        self.ck_urgente.move(x_in_1, y_gap-17 + 3 * y_step)

        # table
        self.table_audiencias = QTableWidget(self)
        self.table_audiencias.move(50, 240)
        self.table_audiencias.resize(700, 300)
        self.table_audiencias.itemSelectionChanged.connect(self.table_audiencias_select)
        self.set_table_audiencias_content(self.filtered_date, self.filtered_vara)


    # table functions
    def set_table_audiencias_content(self, filtered_date, filtered_vara):
        audiencias = self.db.get_audiencias()
        self.table_audiencias.clear()
        
        headers = list(self.db.get_audiencia_columns())
        n_rows = len(audiencias)
        self.table_audiencias.setRowCount(n_rows)
        if (n_rows <= 0):
            return

        self.table_audiencias.setColumnCount(len(audiencias[0]))
        self.table_audiencias.setHorizontalHeaderLabels(headers)
        
        ignored_rows = []
        for row, record in enumerate(audiencias):
            ignore_row = False
            for column, content in enumerate(record):
                self.table_audiencias.setItem(row, column, QTableWidgetItem(content))

                if (filtered_date):
                    if (headers[column] == 'data_audiencia' and content != self.get_date_data_audiencia()):
                        if (row not in ignored_rows):
                            ignored_rows.append(row)

                if (filtered_vara):
                    if (headers[column] == 'vara' and content != self.get_cb_vara()):
                        if (row not in ignored_rows):
                            ignored_rows.append(row)
            
        for i, row in enumerate(ignored_rows):
            self.table_audiencias.removeRow(row-i)

    def table_audiencias_select(self):
        currentRow = self.table_audiencias.currentRow()
        self.table_audiencias.selectRow(currentRow)

        vara_index = self.cb_vara.findText(self.table_audiencias.item(currentRow, 0).text())
        self.cb_vara.setCurrentIndex(vara_index)

        tipo_index = self.cb_tipo.findText(self.table_audiencias.item(currentRow, 2).text())
        self.cb_tipo.setCurrentIndex(tipo_index)

        status_urgente = self.table_audiencias.item(currentRow, 3).text()
        status_urgente = 2 if status_urgente == 'Sim' else 0
        self.ck_urgente.setCheckState(status_urgente)

        txt_horario = self.table_audiencias.item(currentRow, 4).text()
        self.time_horario.setTime(self.transform_to_qtime(txt_horario)) 

        select_processo = self.table_audiencias.item(currentRow, 1)
        select_data_audiencia = self.table_audiencias.item(currentRow, 5)

        if (select_processo and select_data_audiencia):
            select_processo = select_processo.text()
            self.line_processo.setText(select_processo)

            date_to_set = self.transform_to_qdate(select_data_audiencia.text())
            self.date_data_audiencia.setDate(date_to_set)

        select_data_despacho = self.table_audiencias.item(currentRow, 6)
        if (select_data_despacho):
            date_to_set = self.transform_to_qdate(select_data_despacho.text())
            self.date_data_despacho.setDate(date_to_set)

    # get data functions
    def transform_to_qdate(self, date_str):
        date_list = date_str.split('/')
        return QDate(int(date_list[2]), int(date_list[1]), int(date_list[0]))

    def transform_to_qtime(self, time_str):
        time_list = time_str.split(':')
        return QTime(int(time_list[0]), int(time_list[1])) 

    def get_ck_urgente(self):
        return self.ck_urgente.checkState()

    def get_cb_vara(self):
        return self.cb_vara.currentText()

    def get_cb_tipo(self):
        return self.cb_tipo.currentText()

    def get_line_processo(self):
        return self.line_processo.text()

    def get_time_horario(self):
        return self.time_horario.text()

    def get_date_data_audiencia(self):
        return self.date_data_audiencia.text()

    def get_date_data_despacho(self):
        return self.date_data_despacho.text()

    # button functions
    def on_click_filter_date(self):
        self.filtered_date = True
        self.set_table_audiencias_content(self.filtered_date, self.filtered_vara)

    def on_click_filter_vara(self):
        self.filtered_vara = True
        self.set_table_audiencias_content(self.filtered_date, self.filtered_vara)

    def on_click_remove_filters(self):
        self.filtered_date = False
        self.filtered_vara = False
        self.set_table_audiencias_content(self.filtered_date, self.filtered_vara)

    def on_click_insert_audiencia(self):
        self.db.insert_audiencia(vara=self.get_cb_vara(), 
                                 processo=self.get_line_processo(), 
                                 tipo=self.get_cb_tipo(), 
                                 urgente=self.get_ck_urgente(), 
                                 horario=self.get_time_horario(), 
                                 data_audiencia=self.get_date_data_audiencia(), 
                                 data_despacho=self.get_date_data_despacho())
        self.set_table_audiencias_content(self.filtered_date, self.filtered_vara)

    def on_click_delete_audiencia(self):
        currentRow = self.table_audiencias.currentRow()
        drop_processo = self.table_audiencias.item(currentRow, 1)
        drop_data_audiencia = self.table_audiencias.item(currentRow, 5)

        if (drop_processo and drop_data_audiencia):
            drop_processo = drop_processo.text()
            drop_data_audiencia = drop_data_audiencia.text()
            self.db.delete_audiencia(drop_processo, drop_data_audiencia)
            
            print('Audiência removida do banco de dados.')
            self.set_table_audiencias_content(self.filtered_date, self.filtered_vara)

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
                                     horario=self.get_time_horario(), 
                                     data_audiencia=update_data_audiencia, 
                                     data_despacho=self.get_date_data_despacho())
            self.set_table_audiencias_content(self.filtered_date, self.filtered_vara)

    def on_click_open_atividades(self):
        use_processo = self.get_line_processo()
        use_data_audiencia = self.get_date_data_audiencia()

        if (len(use_processo) != 13 or len(use_data_audiencia) != 10):
            print('Audiência selecionada é inválida.')
        else:
            self.windowAtividades = WindowAtividades(self.db, use_processo, use_data_audiencia, self.get_cb_vara())
            self.windowAtividades.show()
        
