import base64
import os
import sqlite3

from dbd.ImageRecogniser import PerkRecogniser, KillerRecogniser, EscapeRecogniser
from decorators import login_is_required
from flask import session, render_template, request, redirect, url_for
from flask.views import MethodView
from PIL import Image

DEBUG = os.environ.get('DEBUG', 'false').lower() in ('true', '1', 't')


class Base(MethodView):
    connection = None

    def __init__(self):
        self.connection = sqlite3.connect('../data/statistics.sqlite')


class Dashboard(Base):
    @login_is_required
    def get(self):
        data = {
            'escaped': 0,
            'died': 0,
            'killed': 0,
            'disconnected': 0,
            'escapes': [],
            'killers': [],
            'killers_num': [],
            'perks': [],
            'perks_num': [],
            'session': session
        }

        self._get_escapes_statistics(data)
        self._get_escape_percentage_statistics(data)
        self._get_most_frequent_killers(data)
        self._get_most_frequent_perks(data)

        self.connection.commit()
        self.connection.close()

        return render_template('dashboard.html', data=data)

    def _get_escape_percentage_statistics(self, data):
        escaped = died = killed = disconnected = all = 0
        cursor = self.connection.cursor()
        cursor.execute('''SELECT escaped, COUNT(`escaped`) AS num FROM survivor GROUP BY escaped ORDER BY num DESC''')
        rows = cursor.fetchall()
        for db_row in rows:
            all += db_row[1]
            if db_row[0] == 'escaped':
                escaped = db_row[1]
            elif db_row[0] == 'died':
                died = db_row[1]
            elif db_row[0] == 'killed':
                killed = db_row[1]
            elif db_row[0] == 'disconnected':
                disconnected = db_row[1]
        if all == 0:
            data['escaped'] = data['died'] = data['killed'] = data['disconnected'] = 0
        else:
            data['escaped'] = round((float(escaped) / all * 100), 1)
            data['died'] = round((float(died) / all * 100), 1)
            data['killed'] = round((float(killed) / all * 100), 1)
            data['disconnected'] = round((float(disconnected) / all * 100), 1)

    def _get_most_frequent_killers(self, data):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT `type`, COUNT(`type`) AS num FROM killer GROUP BY type ORDER BY num DESC''')
        rows = cursor.fetchall()
        for db_row in rows:
            data['killers'].append(db_row[0])
            data['killers_num'].append(db_row[1])

    def _get_most_frequent_perks(self, data):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT perk, COUNT(perk) as num FROM (
        SELECT perk1 AS perk FROM killer
        UNION ALL
        SELECT perk2 AS perk FROM killer
        UNION ALL
        SELECT perk3 AS perk FROM killer
        UNION ALL
        SELECT perk4 AS perk FROM killer) WHERE perk != '-=EMPTY=-' GROUP BY perk ORDER BY num desc LIMIT 30''')
        rows = cursor.fetchall()
        for db_row in rows:
            data['perks'].append(db_row[0])
            data['perks_num'].append(db_row[1])

    def _get_escapes_statistics(self, data):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT m.id, s1.escaped, s2.escaped, s3.escaped, s4.escaped, m.id 
        FROM match AS m
        LEFT JOIN survivor s1 on m.survivor1 = s1.id
        LEFT JOIN survivor s2 on m.survivor2 = s2.id
        LEFT JOIN survivor s3 on m.survivor3 = s3.id
        LEFT JOIN survivor s4 on m.survivor4 = s4.id
        ORDER BY m.id DESC''')
        for db_row in cursor.fetchall():
            escaped = db_row.count('escaped')
            row = [db_row[0], escaped]
            data['escapes'].append(row)


class BaseMatch(Base):
    @staticmethod
    def _convert_db_row_to_view_row(db_row):
        escaped = db_row.count('escaped')
        died = db_row.count('died')
        killed = db_row.count('killed')
        disconnected = db_row.count('disconnected')
        return {'killer': db_row[0], 'perk1': db_row[1], 'perk2': db_row[2],
                'perk3': db_row[3], 'perk4': db_row[4], 'escaped': escaped, 'died': died, 'killed': killed,
                'disconnected': disconnected, 'original': '', 'id': db_row[9]}


class Match(BaseMatch):
    @login_is_required
    def get(self):
        connection = sqlite3.connect('../data/statistics.sqlite')
        data = self.get_data()
        connection.close()
        return render_template('match.html', data=data)

    @login_is_required
    def post(self):
        uploaded_files = request.files.getlist('screenshots[]')
        data = self.get_data()

        data['debug'] = DEBUG
        perk_recogniser = PerkRecogniser()
        killer_recogniser = KillerRecogniser()
        escape_recogniser = EscapeRecogniser()

        for file in uploaded_files:
            file.save('uploaded.file')
            original_image = Image.open('uploaded.file')

            with open('uploaded.file', 'rb') as image_file:
                base64encoded_original_src = 'data:image/png;base64,' + base64.b64encode(image_file.read()).decode(
                    'utf-8')
                base64encoded_original = '<img src="' + base64encoded_original_src + '" width="200" />'

            perk1_text, perk1_image = perk_recogniser.get_perk_text(original_image, 1)
            perk2_text, perk2_image = perk_recogniser.get_perk_text(original_image, 2)
            perk3_text, perk3_image = perk_recogniser.get_perk_text(original_image, 3)
            perk4_text, perk4_image = perk_recogniser.get_perk_text(original_image, 4)
            killer_text, killer_image = killer_recogniser.get_killer_text(original_image)
            survivor_statuses = escape_recogniser.get_survivor_statuses(original_image)

            escaped = survivor_statuses.count('escaped')
            died = survivor_statuses.count('died')
            killed = survivor_statuses.count('killed')
            disconnected = survivor_statuses.count('disconnected')

            row = {
                'killer': killer_text + '<br>' + killer_image,
                'killer_text': killer_text,
                'killer_image': killer_image,
                'perk1': perk1_text + '<br>' + perk1_image,
                'perk1_text': perk1_text,
                'perk1_image': perk1_image,
                'perk2': perk2_text + '<br>' + perk2_image,
                'perk2_text': perk2_text,
                'perk2_image': perk2_image,
                'perk3': perk3_text + '<br>' + perk3_image,
                'perk3_text': perk3_text,
                'perk3_image': perk3_image,
                'perk4': perk4_text + '<br>' + perk4_image,
                'perk4_text': perk4_text,
                'perk4_image': perk4_image,
                'escaped': escaped,
                'died': died,
                'killed': killed,
                'disconnected': disconnected,
                'original': base64encoded_original,
                'original_src': base64encoded_original_src,
            }

            # Store data
            # Killer
            cursor = self.connection.cursor()
            cursor.execute('INSERT INTO killer(`type`, perk1, perk2, perk3, perk4) VALUES(?, ?, ?, ?, ?)',
                           (killer_text, perk1_text, perk2_text, perk3_text, perk4_text))
            killer_id = cursor.lastrowid
            cursor.close()

            # Survivors
            survivor_ids = list()
            for i in range(4):
                cursor = self.connection.cursor()
                cursor.execute('INSERT INTO survivor(escaped) VALUES(?)', (survivor_statuses[i],))
                survivor_ids.append(cursor.lastrowid)
                cursor.close()

            # Match
            cursor = self.connection.cursor()
            cursor.execute(
                'INSERT INTO `match`(killer, survivor1, survivor2, survivor3, survivor4) VALUES(?, ?, ?, ?, ?)',
                (killer_id, survivor_ids[0], survivor_ids[1], survivor_ids[2], survivor_ids[3]))
            match_id = cursor.lastrowid
            cursor.close()
            row['id'] = match_id

            data['rows'].insert(0, row)
            os.remove('uploaded.file')

        self.connection.commit()
        self.connection.close()
        if DEBUG:
            return render_template('match.html', data=data)
        return redirect(url_for('match'), code=302)

    def get_data(self):
        data = {'rows': [], 'debug': False, 'session': session}
        # List stored data
        cursor = self.connection.cursor()
        cursor.execute('''SELECT k.type, k.perk1, k.perk2, k.perk3, k.perk4, s1.escaped, s2.escaped, s3.escaped, s4.escaped, m.id 
        FROM `match` AS m
        LEFT JOIN killer AS k on m.killer = k.id
        LEFT JOIN survivor s1 on m.survivor1 = s1.id
        LEFT JOIN survivor s2 on m.survivor2 = s2.id
        LEFT JOIN survivor s3 on m.survivor3 = s3.id
        LEFT JOIN survivor s4 on m.survivor4 = s4.id
        ORDER BY m.id DESC''')
        rows = cursor.fetchall()
        for db_row in rows:
            row = self._convert_db_row_to_view_row(db_row)
            data['rows'].append(row)

        return data


class Edit(BaseMatch):
    @login_is_required
    def get(self, id):
        data = self._get_stored_match_data(id)

        self.connection.close()
        return render_template('edit.html', data=data)

    def _get_stored_match_data(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT k.type, k.perk1, k.perk2, k.perk3, k.perk4, s1.escaped, s2.escaped, s3.escaped, s4.escaped, m.id 
        FROM match AS m
        LEFT JOIN killer AS k on m.killer = k.id
        LEFT JOIN survivor s1 on m.survivor1 = s1.id
        LEFT JOIN survivor s2 on m.survivor2 = s2.id
        LEFT JOIN survivor s3 on m.survivor3 = s3.id
        LEFT JOIN survivor s4 on m.survivor4 = s4.id
        WHERE m.id=?''', (id,))
        db_row = cursor.fetchone()
        data = self._convert_db_row_to_view_row(db_row)
        return data

    @login_is_required
    def post(self, id):
        # Get stored data
        cursor = self.connection.cursor()

        cursor.execute(
            '''UPDATE killer SET `type`=?, perk1=?, perk2=?, perk3=?, perk4=?
               WHERE id = (SELECT killer FROM `match` WHERE id=?)''',
            (request.form['killer'], request.form['perk1'], request.form['perk2'], request.form['perk3'],
             request.form['perk4'], id))
        cursor.close()

        self.connection.commit()
        self.connection.close()

        return redirect(url_for('match'), code=302)
