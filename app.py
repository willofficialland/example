from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# Inicialización
app = Flask(__name__)

# Conexión Mysql
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'Wuilangel'
app.config['MYSQL_PASSWORD'] = 'wuilangel'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# Configuraciones
app.secret_key = 'mysecretkey'

#Rutas
@app.route('/')
def Inicio():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos')
    datos = cur.fetchall()
    return render_template('index.html', contactos=datos)


@app.route('/add_contacts', methods =['POST'])
def add_contacts():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contactos (fullname,email,phone) VALUES (%s,%s,%s)',
        (fullname, email, phone))
        mysql.connection.commit()
        flash('Contacto Guardado!')
        return redirect(url_for('Inicio'))


@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id = %s', (id))
    datos = cur.fetchall()
    print (datos[0])
    return render_template('edit-contact.html', contacto = datos[0])


@app.route('/actualizar/<id>', methods=['POST'])
def actualizar_contacto(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE contactos
        SET fullname =%s,
            email = %s,
            phone = %s
        WHERE id = %s
        """, (fullname, email, phone, id))
        mysql.connection.commit()
        flash('Contacto Actualizado!')
        return redirect(url_for('Inicio'))


@app.route('/delete/<string:id>')
def delete_contacts(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto Eliminado!')
    return redirect(url_for('Inicio'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)