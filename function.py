from discord_webhook import DiscordWebhook
from sqlite3 import Error
import sqlite3
from threading import local
import window as button
from datetime import datetime, timedelta
import pytz

def gerarBindsHover(window, element):
    window[element].bind('<Enter>', '+MOUSE OVER+')
    window[element].bind('<Leave>', '+MOUSE AWAY+')

def mouseEntrou(window, event):
    theevent = event
    theevent = str(theevent)
    theevent = theevent.split('+')[0]
    window[theevent].update(button_color=('black', button.bton))

def mouseSaiu(window, event):
    theevent = event
    theevent = str(theevent)
    theevent = theevent.split('+')[0]
    window[theevent].update(button_color=('black', button.btoff))


def ConectarBanco():
    import mysql.connector
    con = None
    con = mysql.connector.connect(host='sql10.freemysqlhosting.net',database='sql10420912',user='sql10420912',password='CSZK8May9P')
    if con.is_connected():
        return con

vcon = ConectarBanco()

def search(conexao,sql):
    c=conexao.cursor()
    c.execute(sql)
    resultado=c.fetchall()
    return resultado

def update(conexao, sql):

    try:
        c = conexao.cursor()
        c.execute(sql)
        conexao.commit()
    except Error as ex:
        print(ex)


def checkLogin(login, senha):
    login = str(login)
    senha = str(senha)
    res = search(vcon, f"SELECT login, senha, privLevel FROM staffs WHERE login='{login}'")
    if res != []:
        for r in res:
            password = r[1]
            privLevel = r[2]
        if str(password) == senha:
            return True, privLevel, login
        else:
            return False, 0, 'a'
    else:
        return False, 0, 'a'

def checkPrivLevel(privLevel):
    if privLevel == 1:
        return 'Ajudante'
    elif privLevel == 2:
        return 'Assistente'
    elif privLevel == 3:
        return 'Moderador'
    elif privLevel == 4:
        return 'Super Moderador'
    elif privLevel == 5:
        return 'Aux. Eventos'
    elif privLevel == 6:
        return 'Aux. Gang'
    elif privLevel == 7:
        return 'Aux. Corp'
    elif privLevel == 8:
        return 'Admin. Gang'
    elif privLevel == 9:
        return 'Admin. Corp'
    elif privLevel == 10:
        return 'Admin. Evento'
    elif privLevel == 11:
        return 'Aux. Coordenativo'
    elif privLevel == 12:
        return 'Coordenador'
    elif privLevel == 13:
        return 'Aux. Administrativo'
    elif privLevel == 14:
        return 'Administrador'
    elif privLevel == 15:
        return 'Admin. Geral'
    elif privLevel == 16:
        return 'Supervisor de Eventos'
    elif privLevel == 17:
        return 'Supervisor'
    elif privLevel == 18:
        return 'Supervisor Geral'
    elif privLevel == 19:
        return 'ELITE BMR'
    elif privLevel == 20:
        return 'ELITE SUPREMA BMR'
    elif privLevel == 21:
        return 'Desenvolvedor'


def checkTimeDate(dayweek: bool=False):
    timezone = pytz.timezone("Etc/GMT+3")
    local_time = datetime.now(timezone)
    current_time = local_time.strftime("%H:%M:%S")
    current_date = str(local_time).split()[0]
    if dayweek is True:
        current_weekday = local_time.strftime("%w")
        return current_time, current_date, current_weekday
    else:
        return current_time, current_date

def checkDistance(s1, s2):
    tdelta = datetime.strptime(s2, '%H:%M:%S') - datetime.strptime(s1, '%H:%M:%S')
    
    return tdelta

def ultimaSemana():
    from datetime import date
    from dateutil.relativedelta import relativedelta, SU
    today = date.today()
    last_monday = today + relativedelta(weekday=SU(-2))
    ultimodia = last_monday + timedelta(days=6)
    listadias = []
    dias = {
        'dom': last_monday,
        'seg': last_monday + timedelta(days=1),
        'ter': last_monday + timedelta(days=2),
        'qua': last_monday + timedelta(days=3),
        'qui': last_monday + timedelta(days=4),
        'sex': last_monday + timedelta(days=5),
        'sab': ultimodia
    }
    listadias.append(last_monday.strftime("%Y-%m-%d"))
    listadias.append(dias['seg'].strftime("%Y-%m-%d"))
    listadias.append(dias['ter'].strftime("%Y-%m-%d"))
    listadias.append(dias['qua'].strftime("%Y-%m-%d"))
    listadias.append(dias['qui'].strftime("%Y-%m-%d"))
    listadias.append(dias['sex'].strftime("%Y-%m-%d"))
    listadias.append(dias['sab'].strftime("%Y-%m-%d"))
    return listadias

def sendDiscord(message):
    hora, data = checkTimeDate()
    url = 'https://discord.com/api/webhooks/857092837522014269/Aqe5N30lHfeA36gJ3rFPmHr4gOmuE9e7c4WH8MeQINTgC9i8kXWoPkl7iase6TB4esWD'
    webhook = DiscordWebhook(url=url, content=f'`[{hora}]` - {message}\n`[{data}]`')
    response = webhook.execute()
