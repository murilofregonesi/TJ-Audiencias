import sqlite3

class Database:
    def __init__(self):
        self.create_db()
        self.audiencia_columns = ('vara', 'processo', 'tipo', 'urgente', 'horario', 'data_audiencia', 'data_despacho')
        self.atividade_columns = ('id', 'processo', 'data_audiencia', 'tipo', 'descricao', 'realizado', 'mpc', 'publicacao', 'respondido', 'envolvido', 'reu_preso')

    def create_db(self):
        conn = sqlite3.connect('TJ_Audiencias.db')
        db = conn.cursor()

        db.execute('''CREATE TABLE IF NOT EXISTS audiencia
                    (vara TEXT NOT NULL,
                    processo TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    urgente TEXT NOT NULL,
                    horario TEXT,
                    data_audiencia TEXT NOT NULL,
                    data_despacho TEXT,
                    PRIMARY KEY (processo, data_audiencia));''')

        db.execute('''CREATE TABLE IF NOT EXISTS atividade
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    processo TEXT NOT NULL,
                    data_audiencia TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    descricao TEXT,
                    realizado TEXT NOT NULL,
                    mpc TEXT NOT NULL,
                    publicacao TEXT,
                    respondido TEXT NOT NULL,
                    envolvido TEXT,
                    reu_preso TEXT NOT NULL,
                    FOREIGN KEY (processo, data_audiencia) REFERENCES audiencia(processo, data_audiencia));''')

        conn.commit()
        conn.close()

    ''' ------------------ METHODS FOR AUDIENCIAS ------------------ '''

    def insert_audiencia(self, vara, processo, tipo, urgente, horario, data_audiencia, data_despacho):      
        # input verification
        if (len(processo) != 13):
            print('Audiência não inserida. Processo não válido.')
            return

        if (int(urgente) == 2):
            urgente = 'Sim'
        else:
            urgente = 'Não'
        
        conn = sqlite3.connect('TJ_Audiencias.db')
        db = conn.cursor()
        try:
            db.execute("INSERT INTO audiencia (vara, processo, tipo, urgente, horario, data_audiencia, data_despacho) \
                VALUES({},{},{},{},{},{},{});".format("'"+vara+"'", "'"+processo+"'", "'"+tipo+"'",
                "'"+urgente+"'", "'"+horario+"'", "'"+data_audiencia+"'", "'"+data_despacho+"'"))
        except sqlite3.IntegrityError:
            print('Audiência não inserida.')
        else:
            print('Audiência inserida.')
        finally:
            conn.commit()
            conn.close()

    def delete_audiencia(self, processo, data_audiencia):
        conn = sqlite3.connect('TJ_Audiencias.db')
        db = conn.cursor()
        db.execute("DELETE FROM audiencia WHERE processo=? AND data_audiencia=?;", [processo,data_audiencia])
        conn.commit()
        conn.close()

    def update_audiencia(self, vara, processo, tipo, urgente, horario, data_audiencia, data_despacho):
        # input verification
        urgente = 'Sim' if int(urgente) == 2 else 'Não'

        horario = horario.replace('.',':').replace('h',':').replace('-',':').replace('/',':')
        if (len(horario) != 5):
            horario = ''

        data_despacho = data_despacho.replace('.','/').replace('|','/').replace('-','/').replace('_','/').replace(',','/')
        if (len(data_despacho) != 10):
            data_despacho = ''
        
        conn = sqlite3.connect('TJ_Audiencias.db')
        db = conn.cursor()
        try:
            db.execute("UPDATE audiencia SET vara=?, tipo=?, urgente=?, horario=?, data_despacho=? \
                WHERE processo=? AND data_audiencia=?;", [vara, tipo, urgente, horario, data_despacho, processo, data_audiencia])
        except sqlite3.IntegrityError:
            print('Audiência não atualizada.')
        else:
            print('Audiência atualizada.')
        finally:
            conn.commit()
            conn.close()

    def get_audiencias(self):
        conn = sqlite3.connect('TJ_Audiencias.db')
        db = conn.cursor()
        db.execute('''SELECT * FROM audiencia;''')
        audiencias = db.fetchall()
        conn.close()
        return audiencias

    def get_audiencia_columns(self):
        return self.audiencia_columns

    ''' ------------------ METHODS FOR ATIVIDADES ------------------ '''

    def insert_atividade(self, processo, data_audiencia, tipo, descricao, realizado, mpc, publicacao, respondido, envolvido, reu_preso):      
        # input verification
        realizado = 'Sim' if int(realizado) == 2 else 'Não'
        mpc = 'Sim' if int(mpc) == 2 else 'Não'
        respondido = 'Sim' if int(respondido) == 2 else 'Não'
        reu_preso = 'Sim' if int(reu_preso) == 2 else 'Não'

        conn = sqlite3.connect('TJ_Audiencias.db')
        db = conn.cursor()
        try:
            db.execute("INSERT INTO atividade (processo, data_audiencia, tipo, descricao, realizado, mpc, publicacao, respondido, envolvido, reu_preso) \
                VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {});".format("'"+processo+"'", "'"+data_audiencia+"'", "'"+tipo+"'",
                "'"+descricao+"'", "'"+realizado+"'", "'"+mpc+"'", "'"+publicacao+"'", "'"+respondido+"'", "'"+envolvido+"'", "'"+reu_preso+"'"))
        except sqlite3.IntegrityError:
            print('Atividade não inserida.')
        else:
            print('Atividade inserida.')
        finally:
            conn.commit()
            conn.close()

    def delete_atividade(self, id_atividade):
        conn = sqlite3.connect('TJ_Audiencias.db')
        db = conn.cursor()
        db.execute("DELETE FROM atividade WHERE id=?;", [id_atividade])
        conn.commit()
        conn.close()

    def get_atividades(self, processo, data_audiencia):
        conn = sqlite3.connect('TJ_Audiencias.db')
        db = conn.cursor()
        db.execute("SELECT * FROM atividade WHERE processo=? AND data_audiencia=?;", [processo, data_audiencia])
        atividades = db.fetchall()
        conn.close()
        return atividades
    
    def get_atividade_columns(self):
        return self.atividade_columns

    def update_atividade(self, id_atividade, tipo, descricao, realizado, mpc, publicacao, respondido, envolvido, reu_preso):
        # input verification
        realizado = 'Sim' if int(realizado) == 2 else 'Não'
        mpc = 'Sim' if int(mpc) == 2 else 'Não'
        respondido = 'Sim' if int(respondido) == 2 else 'Não'
        reu_preso = 'Sim' if int(reu_preso) == 2 else 'Não'
        
        conn = sqlite3.connect('TJ_Audiencias.db')
        db = conn.cursor()

        try:
            db.execute("UPDATE atividade SET tipo=?, descricao=?, realizado=?, mpc=?, publicacao=?, respondido=?, envolvido=?, reu_preso=? \
                WHERE id=?;", [tipo, descricao, realizado, mpc, publicacao, respondido, envolvido, reu_preso, id_atividade])
        except sqlite3.IntegrityError:
            print('Atividade não atualizada.')
        else:
            print('Atividade atualizada.')
        finally:
            conn.commit()
            conn.close()