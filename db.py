import sqlite3

class Database:
    def __init__(self):
        self.create_db()
        self.audiencia_columns = ('vara', 'processo', 'tipo', 'urgente', 'horario', 'data_audiencia', 'data_despacho')
        self.atividade_columns = ('processo', 'data_audiencia', 'tipo', 'descricao', 'realizado', 'mpc', 'publicacao', 'respondido', 'envolvido', 'reu_preso')

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
                    (processo TEXT NOT NULL,
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

    def insert_audiencia(self, vara, processo, tipo, urgente, horario, data_audiencia, data_despacho):      
        # input verification
        if (len(processo) != 13):
            print('Audiência não inserida. Processo não válido.')
            return

        horario = horario.replace('.',':').replace('h',':').replace('-',':').replace('/',':')
        if (len(horario) != 5):
            horario = ''

        data_audiencia = data_audiencia.replace('.','/').replace('|','/').replace('-','/').replace('_','/').replace(',','/')
        if (len(data_audiencia) != 10):
            print('Audiência não inserida. Data de audiência inválida.')
            return

        data_despacho = data_despacho.replace('.','/').replace('|','/').replace('-','/').replace('_','/').replace(',','/')
        if (len(data_despacho) != 10):
            data_despacho = ''

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
        horario = horario.replace('.',':').replace('h',':').replace('-',':').replace('/',':')
        if (len(horario) != 5):
            horario = ''

        data_despacho = data_despacho.replace('.','/').replace('|','/').replace('-','/').replace('_','/').replace(',','/')
        if (len(data_despacho) != 10):
            data_despacho = ''

        if (int(urgente) == 2):
            urgente = 'Sim'
        else:
            urgente = 'Não'
        
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

    def get_atividades(self):
        conn = sqlite3.connect('TJ_Audiencias.db')
        db = conn.cursor()
        db.execute('''SELECT * FROM atividade;''')
        atividades = db.fetchall()
        conn.close()
        return atividades

    def get_audiencia_columns(self):
        return self.audiencia_columns

    def get_atividade_columns(self):
        return self.atividade_columns
