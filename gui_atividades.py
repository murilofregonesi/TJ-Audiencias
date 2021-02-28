from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QCheckBox, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QIcon, QFont
import sys

class WindowAtividades(QWidget):
    def __init__(self, db, processo, data_audiencia, vara, parent=None):
        super(WindowAtividades, self).__init__(parent)
        self.db = db
        self.setWindowIcon(QIcon("static/logo.ico"))
        self.setWindowTitle("Atividades Audiência - {}a Vara".format(vara))
        self.resize(800, 600)
        self.processo = processo
        self.data_audiencia = data_audiencia

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

        self.lbl_value_font = QFont()
        self.lbl_value_font.setBold(True)

        create_label(self, 'Processo', x_in_1, 0)
        self.lbl_processo = create_label(self, self.processo, x_in_1, 0.5) # Value
        self.lbl_processo.setFont(self.lbl_value_font)

        create_label(self, 'Data Audiência', x_in_1, 1)
        self.lbl_data_audiencia = create_label(self, self.data_audiencia, x_in_1, 1.5) # Value
        self.lbl_data_audiencia.setFont(self.lbl_value_font)

        create_label(self, 'Tipo', x_in_1, 2)
        create_label(self, 'Descrição', x_in_1, 3)
        create_label(self, 'Atividades', x_in_1, 4)

        create_label(self, 'Publicação', x_in_2, 2)
        create_label(self, 'Envolvido', x_in_2, 3)

        # combo-box
        y_gap = 37
        y_step = 50

        def create_cb(window, list_items, x, pos):
            combo_box = QComboBox(window)
            combo_box.addItems(list_items)
            combo_box.move(x, y_gap + pos * y_step)
            combo_box.resize(150, 24)
            return combo_box

        self.cb_tipo = create_cb(self, ["Mandado", "Carta Precatória", "Ofício PM", "Ofício PC", "Ofício GCM", "Ofício Andamento", "Ofício Func. Públ.", "Ofício Requisição"], x_in_1, 2)
        self.cb_envolvido = create_cb(self, ["Réu", "Vítima", "Testemunha", "Outro"], x_in_2, 3)

        # check-box
        self.ck_realizado = QCheckBox("Realizado", self)
        self.ck_realizado.move(x_in_2, y_gap-17 + 0 * y_step)

        self.ck_mpc = QCheckBox("MPC", self)
        self.ck_mpc.move(x_in_2, y_gap + 0 * y_step)

        self.ck_respondido = QCheckBox("Respondido", self)
        self.ck_respondido.move(x_in_2, y_gap-34 + 1 * y_step)

        self.ck_preso = QCheckBox("Réu Preso", self)
        self.ck_preso.move(x_in_2, y_gap-17 + 1 * y_step) 

        # line edit
        def create_line_edit(window, x, pos):
            line_edit = QLineEdit(window)
            line_edit.move(x, y_gap + pos * y_step)
            line_edit.resize(150, 24)
            return line_edit

        self.descricao = create_line_edit(self, x_in_1, 3)
        self.publicacao = create_line_edit(self, x_in_2, 2)

        # table
        self.table_atividades = QTableWidget(self)
        self.table_atividades.move(50, 240)
        self.table_atividades.resize(700, 300)
        self.table_atividades.itemSelectionChanged.connect(self.table_atividades_select)
        self.set_table_atividades_content()

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

        self.btn_insert_atividade = create_button(self, self.on_click_insert_atividade, 
            'Inserir Atividade', 'Criar uma nova Atividade nesta Audiência.', 0)

        self.btn_update_atividade = create_button(self, self.on_click_update_atividade, 
            'Atualizar Atividade', 'Atualizar esta Atividade desta Audiência.', 1)

        self.btn_delete_atividade = create_button(self, self.on_click_delete_atividade, 
            'Deletar Atividade', 'Deletar esta Atividade desta Audiência.', 2)

        self.btn_close_atividade = create_button(self, self.on_click_close_atividade, 
            'Fechar Tela', 'Fechar tela de Atividades desta Audiência.', 3)


    def table_atividades_select(self):
        currentRow = self.table_atividades.currentRow()
        self.table_atividades.selectRow(currentRow)

        self.descricao.setText(self.table_atividades.item(currentRow, 4).text())
        self.publicacao.setText(self.table_atividades.item(currentRow, 7).text())

        tipo_index = self.cb_tipo.findText(self.table_atividades.item(currentRow, 3).text())
        self.cb_tipo.setCurrentIndex(tipo_index)

        envolvido_index = self.cb_envolvido.findText(self.table_atividades.item(currentRow, 9).text())
        self.cb_envolvido.setCurrentIndex(envolvido_index)

        status_realizado = self.table_atividades.item(currentRow, 5).text()
        status_realizado = 2 if status_realizado == 'Sim' else 0
        self.ck_realizado.setCheckState(status_realizado)

        status_mpc = self.table_atividades.item(currentRow, 6).text()
        status_mpc = 2 if status_mpc == 'Sim' else 0
        self.ck_mpc.setCheckState(status_mpc)

        status_respondido = self.table_atividades.item(currentRow, 8).text()
        status_respondido = 2 if status_respondido == 'Sim' else 0
        self.ck_respondido.setCheckState(status_respondido)

        status_preso = self.table_atividades.item(currentRow, 10).text()
        status_preso = 2 if status_preso == 'Sim' else 0
        self.ck_preso.setCheckState(status_preso)

    def set_table_atividades_content(self):
        atividades = self.db.get_atividades(self.processo, self.data_audiencia)
        self.table_atividades.clear()
        
        headers = list(self.db.get_atividade_columns())
        n_rows = len(atividades)
        self.table_atividades.setRowCount(n_rows)
        if (n_rows <= 0):
            return

        self.table_atividades.setColumnCount(len(atividades[0]))
        self.table_atividades.setHorizontalHeaderLabels(headers)
        
        for row, record in enumerate(atividades):
            for column, content in enumerate(record):
                self.table_atividades.setItem(row, column, QTableWidgetItem(str(content)))

    def get_tipo(self):
        return self.cb_tipo.currentText()
    
    def get_descricao(self):
        return self.descricao.text()
    
    def get_realizado(self):
        return self.ck_realizado.checkState()  
    
    def get_mpc(self):
        return self.ck_mpc.checkState()  
    
    def get_publicacao(self): 
        return self.publicacao.text()
    
    def get_respondido(self):
        return self.ck_respondido.checkState()
    
    def get_envolvido(self):
        return self.cb_envolvido.currentText()

    def get_reu_preso(self):
        return self.ck_preso.checkState()

    def on_click_insert_atividade(self):
        self.db.insert_atividade(processo=self.processo, 
                                 data_audiencia=self.data_audiencia, 
                                 tipo=self.get_tipo(), 
                                 descricao=self.get_descricao(), 
                                 realizado=self.get_realizado(), 
                                 mpc=self.get_mpc(), 
                                 publicacao=self.get_publicacao(), 
                                 respondido=self.get_respondido(), 
                                 envolvido=self.get_envolvido(),  
                                 reu_preso=self.get_reu_preso())
        self.set_table_atividades_content()

    def on_click_update_atividade(self):
        currentRow = self.table_atividades.currentRow()
        update_id = self.table_atividades.item(currentRow, 0)

        if (update_id):
            update_id = update_id.text()
            self.db.update_atividade(id_atividade=update_id,
                                     tipo=self.get_tipo(), 
                                     descricao=self.get_descricao(), 
                                     realizado=self.get_realizado(), 
                                     mpc=self.get_mpc(), 
                                     publicacao=self.get_publicacao(), 
                                     respondido=self.get_respondido(), 
                                     envolvido=self.get_envolvido(),  
                                     reu_preso=self.get_reu_preso())
            self.set_table_atividades_content()

    def on_click_delete_atividade(self):
        currentRow = self.table_atividades.currentRow()
        drop_id = self.table_atividades.item(currentRow, 0)

        if (drop_id):
            drop_id = drop_id.text()
            self.db.delete_atividade(drop_id)
            
            print('Atividade removida do banco de dados.')
            self.set_table_atividades_content()

    def on_click_close_atividade(self):
        self.close()