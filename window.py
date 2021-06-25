import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Button, SELECT_MODE_SINGLE
import function
from var import iconbase64
from datetime import datetime, timedelta

titulos = {
    'Login': 'BMR5 - LOGIN',
    'Registro': 'BMR5 - REGISTRO',
    'main': 'BMR5 - STAFF',
    'minhasInfo': 'Minhas informações - BMR5*',
    'postarAviso': 'Postar aviso staff - BMR5*',
    'aprovarReg': 'Aprovar registro - BMR5*',
    'desativarConta':'Desativar conta - BMR5*',
    'ativarConta': 'Ativar conta - BMR5*',
    'infoStaffs': 'Informações staffs - BMR5*',
    'bansAplicados': 'Bans aplicados - BMR5*',
    'postarBan': 'Postar ban aplicado - BMR5*',
    'AFPonto': 'Abrir/Fechar ponto - BMR5*',
    'VerPonto': 'Ver pontos abertos - BMR5*',
    'fecharPontos': 'Fechar pontos abertos - BMR5*',
    'cancelarPontos': 'Cancelar pontos abertos - BMR5*',
    'liberarRP': "Liberar para rp - BMR5*",
    'trocarCargo': "Trocar cargos - BMR5*",
    'cargaHoraria': "Carga horária staffs - BMR5*"
}


bgcolor =  '#959595'

btoff = '#FFD700'
bton = '#FFA200'


########################################### JANELA DE LOGIN ###########################################
def Login():
    sg.theme('Reddit')
    layout = [
    [sg.Text('Login: '), sg.Input(key='user')],
    [sg.Text('Senha: '), sg.Input(key='senha', password_char='●')],
    [sg.Button('Logar', button_color=('black', btoff)), sg.Button('Registrar', button_color=('black', btoff))]
    ]
    return sg.Window(
        titulos['Login'],layout=layout,size=(300, 150), icon=iconbase64, margins=(0, 0),return_keyboard_events=True, resizable=False,finalize=True)



########################################### JANELA DE REGISTRO ###########################################
def Registro():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Nome completo: ', size=(15, 1)), sg.Input(key='nc', size=(100, 1))],
        [sg.Text('Login: ', size=(15, 1)), sg.Input(key='log', size=(30, 1))],
        [sg.Text('Senha:', size=(15, 1)), sg.Input(password_char='●', key='pass', size=(30, 1))],
        [sg.Text('ID: ', size=(15, 1)), sg.Input(key='gameid', size=(5, 1))],
        [sg.Text('Serial: ', size=(15, 1)), sg.Input(key='serial', size=(32, 1))],
        [sg.Text('Número de Celular: ', size=(15, 1)), sg.Input(key='number', size=(13, 1))],
        [sg.Button('Realizar Registro', button_color=('black', btoff), key='rr'), sg.Button('Voltar', button_color=('black', btoff))]
    ]
    return sg.Window(
        titulos['Registro'],layout=layout,size=(500, 190), icon=iconbase64,margins=(0, 0),resizable=False,return_keyboard_events=True,finalize=True)



########################################### JANELA PRINCIPAL ###########################################
def main(nome: str('.'), privLevel: int=1):
    sg.theme('Reddit')
    layout_menu = []
    if privLevel == 1:
        layout_menu.append(['Ferramentas', ['Abrir/Fechar bate-ponto']])
        layout_menu.append(['Bans aplicados', ['Bans aplicados']])

    if privLevel >= 2 and privLevel < 11:
        layout_menu.append(['Ferramentas', ['Abrir/Fechar bate-ponto']])
        layout_menu.append(['Bans', ['Bans aplicados', 'Postar ban aplicado']])

    if privLevel >= 11:
        layout_menu.append(['Ferramentas', ['Abrir/Fechar bate-ponto', 'Liberar pra RP']])
        layout_menu.append(['Bans', ['Bans aplicados', 'Postar ban aplicado']])

    if privLevel == 14:
        layout_menu.append(['Administração', ['Ver pontos abertos']])

    if privLevel == 15:
            layout_menu.append(['Administração', ['Ver pontos abertos', 'Fechar pontos abertos']])

    if privLevel >= 16:
            layout_menu.append(['Administração', ['Ver pontos abertos', 'Fechar pontos abertos', 'Cancelar pontos abertos']])

    if privLevel >= 17:
            layout_menu.append(['Controle', ['Postar aviso staff aplicado', 'Aprovar registro', 'Desativar conta', 'Ativar conta', 'Informações de staffs', 'Atualizar cargo', 'Carga horária']])

    layout_menu.append(['Minha conta', ['Informações']])
    cargo = function.checkPrivLevel(privLevel)

    layout = [
        [sg.Menu(layout_menu)],
        [sg.Text(f'{nome}                              {cargo}', size=(100, 1), justification='center',font=('Arial', 18, 'bold'))]
    ]
    return sg.Window(
        titulos['main'],layout=layout,size=(500, 150), icon=iconbase64,margins=(0, 0),resizable=True, return_keyboard_events=True,finalize=True)


########################################### MINHA CONTA ###########################################
################### INFORMAÇÕES ###################
def minhasInfo(nc, login, gameid, serial, numero, privLevel):
    cargo = function.checkPrivLevel(privLevel)
    layout = [
        [sg.Text(f'Nome completo: {nc}', background_color=bgcolor)],
        [sg.Text(f'Login: {login}', background_color=bgcolor)],
        [sg.Text(f'ID: {gameid}', background_color=bgcolor)],
        [sg.Text(f'Serial: {serial}', background_color=bgcolor)],
        [sg.Text(f'Número: {numero}', background_color=bgcolor)],
        [sg.Text(f'Cargo: {cargo}', background_color=bgcolor)],
        [sg.Button(f'Fechar', button_color=('black', btoff))]
    ]
    return sg.Window(
        titulos['minhasInfo'],layout=layout, icon=iconbase64,size=(400, 200),margins=(0, 0),resizable=False, return_keyboard_events=True,finalize=True, no_titlebar=True, background_color=bgcolor)




########################################### CONTROLE ###########################################
################### POSTAR AVISO STAFF ###################
def postarAviso():
    staffs = []
    res = function.search(function.ConectarBanco(), "SELECT login, gameid FROM staffs")
    for r in res:
        staffs.append(f'{r[0]} | {r[1]}')
    layout = [
        [sg.Listbox(values=staffs, size=(300, 8), key='listt')],
        [sg.Text('Motivo:', background_color=bgcolor, size=(20, 1)), sg.Input(key='motivo')],
        [sg.Text('Prova:', background_color=bgcolor, size=(20, 1)), sg.Input(key='prova')],
        [sg.Button("Aplicar aviso", button_color=('black', btoff)), sg.Button('Fechar', button_color=('black', btoff))]
    ]
    return sg.Window(
        titulos['postarAviso'],layout=layout, icon=iconbase64,size=(400, 250),margins=(0, 0),resizable=False, return_keyboard_events=True,finalize=True, no_titlebar=True, background_color=bgcolor)


################### APROVAR REGISTROS ###################
def aprovarReg():
    listamembros = []
    res = function.search(function.ConectarBanco(), f"SELECT login, gameid FROM registros")
    for r in res:
        listamembros.append(f'{r[0]} | {r[1]}')
    if listamembros == []:
        sss = None
    else:
        sss = listamembros[0]
    layout = [
        [sg.Listbox(values=listamembros, size=(300, 8), key='listamem', default_values=sss)],
        [sg.Button('Aprovar', button_color=('black', btoff)), sg.Button('Detalhes', button_color=('black', btoff)), sg.Button('Fechar', button_color=('black', btoff))]
    ]
    return sg.Window(
        titulos['aprovarReg'],layout=layout, icon=iconbase64,size=(400, 250),margins=(0, 0),resizable=False, return_keyboard_events=True,finalize=True, no_titlebar=True, background_color=bgcolor)


################### DESATIVAR CONTAS ###################
def desativarConta():
    staffs = []
    res = function.search(function.ConectarBanco(), "SELECT login, gameid FROM staffs")
    for r in res:
        staffs.append(f'{r[0]} | {r[1]}')
    sss = staffs[0]
    layout = [
        [sg.Listbox(values=staffs, size=(300, 8), key='listcontas', default_values=sss)],
        [sg.Button("Desativar", button_color=('black', btoff)), sg.Button('Fechar', button_color=('black', btoff))]
    ]
    return sg.Window(
        titulos['desativarConta'],layout=layout, icon=iconbase64,size=(400, 250),margins=(0, 0),resizable=False, return_keyboard_events=True,finalize=True, no_titlebar=True, background_color=bgcolor)



################### ATIVAR CONTA ###################
def ativarConta():
    staffs = []
    res = function.search(function.ConectarBanco(), "SELECT login, gameid FROM desativados")
    for r in res:
        staffs.append(f'{r[0]} | {r[1]}')
    if staffs != []:
        sss = staffs[0]
    else:
        sss = None
    layout = [
        [sg.Listbox(values=staffs, size=(300, 8), key='listcontasd', default_values=sss)],
        [sg.Button("Ativar", button_color=('black', btoff)), sg.Button('Fechar', button_color=('black', btoff))]
    ]
    return sg.Window(
        titulos['ativarConta'],layout=layout,size=(400, 250), icon=iconbase64,margins=(0, 0),resizable=False, return_keyboard_events=True,finalize=True, no_titlebar=True, background_color=bgcolor)



################### INFORMAÇÕES DOS STAFFS ###################
def infoStaffs():
    staffs = []
    res = function.search(function.ConectarBanco(), "SELECT login, gameid FROM staffs")
    for r in res:
        staffs.append(f'{r[0]} | {r[1]}')
    if staffs != []:
        sss = staffs[0]
    else:
        sss = None
    layout = [
        [sg.Listbox(values=staffs, size=(300, 8), key='listainfo', default_values=sss)],
        [sg.Button("Informações", button_color=('black', btoff)), sg.Button('Fechar', button_color=('black', btoff))]
    ]
    return sg.Window(
        titulos['infoStaffs'],layout=layout,size=(400, 250), icon=iconbase64,margins=(0, 0),resizable=False, return_keyboard_events=True,finalize=True, no_titlebar=True, background_color=bgcolor)




########################################### BANS ###########################################
################### BANS APLICADOS ###################
def bansAplicados():
    bans = []
    res = function.search(function.ConectarBanco(), "SELECT * FROM bans")
    for r in res:
        staff = r[0].replace(' ', '-')
        gameid = str(r[1])
        gameid = gameid.replace(' ', '-')
        motivo = r[2].replace(' ', '-')
        duracao = r[3].replace(' ', '-')
        prova = r[4].replace(' ', '-')
        bans.append(f'{staff} {gameid} {motivo} {duracao} {prova}')
    layout = [
        [sg.Input(key='searchban'), sg.Button('Pesquisar', button_color=('black', btoff))],
        [sg.Table(values=bans,key='tablebans', headings=['Staff', 'ID', 'Motivo', 'Duração', 'Prova'], auto_size_columns=False, col_widths=[13, 5, 15, 8, 20], select_mode='none', justification='center')],
        [sg.Button('Fechar', button_color=('black', btoff))]
    ]
    return sg.Window(
        titulos['bansAplicados'],layout=layout,size=(700, 250), icon=iconbase64,margins=(0, 0),resizable=False, return_keyboard_events=True,finalize=True, no_titlebar=True, background_color=bgcolor)



################### POSTAR BAN APLICADO ###################
def postarBan():
    layout = [
        [sg.Text('ID: ', size=(10, 1), background_color=bgcolor), sg.Input(key='in-id')],
        [sg.Text('Motivo: ', size=(10, 1), background_color=bgcolor), sg.Input(key='in-motivo')],
        [sg.Text('Prova: ', size=(10, 1), background_color=bgcolor), sg.Input(key='in-prova')],
        [sg.Text('Duração: ', size=(10, 1), background_color=bgcolor), sg.Input(key='in-duracao')],
        [sg.Button('Postar', size=(10, 1), button_color=('black', btoff)), sg.Button('Fechar', button_color=('black', btoff))]
    ]
    return sg.Window(
        titulos['postarBan'],layout=layout,size=(400, 200), icon=iconbase64,margins=(0, 0),resizable=False, return_keyboard_events=True,finalize=True, no_titlebar=True, background_color=bgcolor)


################### ABRIR/FECHAR PONTO ###################
def AFPonto(dec):
    layout = [
        [sg.Text(f'{dec}', key='txt-hf', size=(50, 1), font=('Arial', 14, 'bold'), justification='center', background_color=bgcolor)],
        [sg.Text(size=(0, 4), background_color=bgcolor)],
        [sg.Button('Abrir ponto', key='bt_AF', button_color=('black', btoff), size=(50, 1))],
        [sg.Button('Fechar', button_color=('black', btoff))]
    ]
    return sg.Window(
        titulos['AFPonto'],layout=layout,size=(400, 200), icon=iconbase64,margins=(0, 0),resizable=False, return_keyboard_events=True,finalize=True, no_titlebar=True, background_color=bgcolor)



################### LIBERAR PRA RP ###################
def liberarRP():
    staffs = []
    res = function.search(function.ConectarBanco(), "SELECT login, gameid FROM staffs")
    for r in res:
        staffs.append(f'{r[0]} | {r[1]}')
    if staffs != []:
        sss = staffs[0]
    else:
        sss = None
    layout = [
        [sg.Listbox(values=staffs, size=(300, 8), key='listalib', default_values=sss)],
        [sg.Button("Liberar RP", button_color=('black', btoff)), sg.Button('Fechar', button_color=('black', btoff))]
    ]
    
    return sg.Window(
        titulos['liberarRP'],layout=layout,size=(400, 250), icon=iconbase64,margins=(0, 0),resizable=False, return_keyboard_events=True,finalize=True, no_titlebar=True, background_color=bgcolor)


################### VER PONTOS ABERTOS ###################
def VerPonto():
    pontos = []
    res = function.search(function.ConectarBanco(), "SELECT staff, hora_inicio, data, tipo FROM pontos WHERE hora_fim='00:00:00'")
    for r in res:
        staff = r[0].replace(' ', '-')
        inicio = r[1]
        data = r[2]
        tipo = r[3]
        pontos.append(f'{staff} {inicio} {tipo} {data}')
    layout = [
        [sg.Table(values=pontos,key='tablepontos', headings=['Staff', 'Inicio', 'Tipo', 'Data'], auto_size_columns=False, col_widths=[13, 9, 4, 11], select_mode='none', justification='center')],
        [sg.Button('Fechar', button_color=('black', btoff))]
    ]
    return sg.Window(
        titulos['VerPonto'],layout=layout,size=(400, 250), icon=iconbase64,margins=(0, 0),resizable=False, return_keyboard_events=True,finalize=True, no_titlebar=True, background_color=bgcolor)



################### FECHAR PONTOS ABERTOS ###################
def fecharPontos():
    pontosab = []
    res = function.search(function.ConectarBanco(), "SELECT staff, hora_inicio FROM pontos WHERE hora_fim='00:00:00'")
    for r in res:
        pontosab.append(f'{r[0]} | {r[1]}')
    if pontosab != []:
        sss = pontosab[0]
    else:
        sss = None
    layout = [
        [sg.Listbox(values=pontosab, size=(300, 8), key='listpontosab', default_values=sss)],
        [sg.Button("Fechar Ponto", button_color=('black', btoff)), sg.Button('Fechar', button_color=('black', btoff))]
    ]
    return sg.Window(
        titulos['fecharPontos'],layout=layout,size=(400, 250), icon=iconbase64,margins=(0, 0),resizable=False, return_keyboard_events=True,finalize=True, no_titlebar=True, background_color=bgcolor)





################### CANCELAR PONTOS ABERTOS ###################
def cancelarPontos():
    pontosab = []
    res = function.search(function.ConectarBanco(), "SELECT staff, hora_inicio FROM pontos WHERE hora_fim='00:00:00'")
    for r in res:
        pontosab.append(f'{r[0]} | {r[1]}')
    if pontosab != []:
        sss = pontosab[0]
    else:
        sss = None
    layout = [
        [sg.Listbox(values=pontosab, size=(300, 8), key='listpontosab2', default_values=sss)],
        [sg.Button("Cancelar Ponto", button_color=('black', btoff)), sg.Button('Fechar', button_color=('black', btoff))]
    ]
    return sg.Window(
        titulos['cancelarPontos'],layout=layout,size=(400, 250), icon=iconbase64,margins=(0, 0),resizable=False, return_keyboard_events=True,finalize=True, no_titlebar=True, background_color=bgcolor)




#### TROCAR CARGO
def trocarCargo():
    staffs = []
    res = function.search(function.ConectarBanco(), "SELECT login, gameid FROM staffs")
    for r in res:
        staffs.append(f'{r[0]} | {r[1]}')
    if staffs != []:
        sss = staffs[0]
    else:
        sss = None
    layout = [
        [sg.Listbox(values=staffs, size=(300, 8), key='listastf', default_values=sss)],
        [sg.Input(key='in-new')],
        [sg.Button("Atualizar", button_color=('black', btoff)), sg.Button('Fechar', button_color=('black', btoff))]
    ]
    
    return sg.Window(
        titulos['trocarCargo'],layout=layout,size=(400, 250), icon=iconbase64,margins=(0, 0),resizable=False, return_keyboard_events=True,finalize=True, no_titlebar=True, background_color=bgcolor)


### CARGO HORARIO
def cargaHoraria():
    pontos = []
    total = timedelta(hours=0, minutes=0, seconds=0)
    staffs = []
    ress = function.search(function.ConectarBanco(), "SELECT login, gameid FROM staffs")
    dias = function.ultimaSemana()
    for rr in ress:
        total = timedelta(hours=0, minutes=0, seconds=0)
        ostaff = rr[0]
        ssstaff = ostaff.replace(' ', '-')
        res = function.search(function.ConectarBanco(), f"SELECT staff, total, data FROM pontos WHERE(tipo='ATD' AND staff='{ostaff}')")
        for r in res:
            ___ = str(r[2])
            if ___ in dias:
                bb = r[1]
                v = total
                total += bb
        pontos.append(f'{ssstaff} {total}')
        
    layout = [
        [sg.Table(values=pontos,key='tablepontosf', headings=['Staff', 'Total semanal'], auto_size_columns=False, col_widths=[13, 10], select_mode='none', justification='center')],
        [sg.Text('Data: ', background_color=bgcolor), sg.Input(key='-in-day', size=(2, 1)), sg.Input(key='-in-month', size=(2, 1)), sg.Input(key='-in-year', size=(4, 1)), sg.Text('Nome: ', background_color=bgcolor), sg.Input(key='in-name')],
        [sg.Button('Encontrar', button_color=('black', btoff)), sg.Button('Fechar', button_color=('black', btoff))]
    ]
    return sg.Window(
        titulos['cargaHoraria'],layout=layout,size=(400, 250), icon=iconbase64,margins=(0, 0),resizable=False, return_keyboard_events=True,finalize=True, no_titlebar=True, background_color=bgcolor)
