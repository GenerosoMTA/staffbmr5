version = 1.0

from function import vcon
import function
import PySimpleGUI as sg
import window as janela
from window import titulos
from datetime import datetime, timedelta
from var import iconbase64

global nomee
global prive

def clear():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

res = function.search(function.ConectarBanco(), "SELECT * FROM appconfig")
for r in res:
    dbversion = r[0]
if version < dbversion:
    sg.popup('O aplicativo está desatualizado, contate um superior para lhe ajudar.', title='Desatualizado!', icon=iconbase64)

janela1, janela2 = janela.Login(), None
clear()

function.gerarBindsHover(janela1, 'Logar')
function.gerarBindsHover(janela1, 'Registrar')

enter_buttons = [chr(13), "Return:13"]
# ABRINDO LOOP
while True:
    # LENDO JANELAS, EVENTOS E VALORES
    window, event, values = sg.read_all_windows()
########################################### CONFERINDO EVENTOS ###########################################
    
########################################### DESIGN DE BOTÕES ###########################################
    if event is not None:
        if event.endswith('AWAY+'):
            function.mouseSaiu(window, event)
        if event.endswith('OVER+'):
            function.mouseEntrou(window, event)
    

    if window.Title.endswith(' - BMR5*'):
        if event == 'Fechar':
            janela2.close()

########################################### OUTROS ###########################################
    if not window.Title.endswith(' - BMR5*'): # SE FOREM JANELAS BASE
        if event == sg.WIN_CLOSED:
            if janela1 is not None:
                janela1.close()
            if janela2 is not None:
                janela2.close()
            break
        if event == 'F5:116' and window.Title == titulos['main']:
            janela1.close()
            nomee = nomee
            prive = prive
            janela1 = janela.main(nome, priv)
            janela1.Maximize()
            function.sendDiscord(f'{nomee} acabou de relogar no aplicativo.')
########################################### JANELA DE LOGIN ###########################################
        if window.Title == titulos['Login']:
            if event == 'Logar' or event in enter_buttons:
                tentativa, priv, nome = function.checkLogin(values['user'], values['senha'])
                if tentativa is True:
                    janela1.close()
                    nomee = nome
                    prive = priv
                    janela1 = janela.main(nome, priv)
                    janela1.Maximize()
                    sg.popup('Bem-vindo(a) ao painel staff BMR5!', title='Welcome!', icon=iconbase64)
                    function.sendDiscord(f'{nomee} acabou de logar no aplicativo.')
                else:
                    sg.Popup("Login ou senha incorreto(s). (Maiúsculas e minúsculas são consideradas)", title='Incorreto!', icon=iconbase64)
            if event == 'Registrar':
                janela1.close()
                janela1 = janela.Registro()
                function.gerarBindsHover(janela1, 'rr')
                function.gerarBindsHover(janela1, 'Voltar')

########################################### JANELA DE REGISTRO ###########################################
        if window.Title == titulos['Registro']:
            if event in ['Voltar']:
                janela1.close()
                janela1 = janela.Login()
                function.gerarBindsHover(janela1, 'Logar')
                function.gerarBindsHover(janela1, 'Registrar')
            if event in ['rr']:
                if values['nc'] != "" and values['log'] != "" and values['pass'] != "" and values['gameid'] != "" and values['serial'] != "" and values['number'] != "":
                    try:
                        gid = int(values['gameid'])
                        function.update(function.ConectarBanco(), f"INSERT INTO registros(nomecompleto, login, senha, gameid, serial, numero) VALUES('{values['nc']}', '{values['log']}', '{values['pass']}', '{values['gameid']}', '{values['serial']}', '{values['number']}')")
                        sg.popup('Seu registro foi enviado, aguarde ser aprovado.', icon=iconbase64)
                    except Exception as e:
                        etostring = e
                        etostring = str(etostring)
                        if etostring.startswith("invalid literal for int() with base 10:"):
                            sg.popup('O ID precisa ser um número inteiro.', icon=iconbase64)
                        else:
                            print(e)
                else:
                    sg.popup('Algum campo está em branco!', icon=iconbase64)

########################################### JANELA PRINCIPAL ###########################################
        if window.Title == titulos['main']:
############################### MINHA CONTA - INFORMAÇÕES ###################
            if event == 'Informações':
                if janela2 is not None:
                    janela2.close()
                res = function.search(function.ConectarBanco(), f"SELECT * FROM staffs WHERE login='{nomee}'")
                for r in res:
                    nc = r[0]
                    log = r[1]
                    gameid = r[3]
                    serial = r[4]
                    numero = r[5]
                    privLevel = r[6]
                janela2 = janela.minhasInfo(nc, log, gameid, serial, numero, privLevel)
                function.gerarBindsHover(janela2, 'Fechar')

############################### CONTROLE - POSTAR AVISO STAFF ###################
            if event == 'Postar aviso staff aplicado':
                if janela2 is not None:
                    janela2.close()
                janela2 = janela.postarAviso()
                function.gerarBindsHover(janela2, 'Aplicar aviso')
                function.gerarBindsHover(janela2, 'Fechar')

############################### CONTROLE - APROVAR REGISTRO ###################
            if event == 'Aprovar registro':
                if janela2 is not None:
                    janela2.close()
                janela2 = janela.aprovarReg()
                function.gerarBindsHover(janela2, 'Aprovar')
                function.gerarBindsHover(janela2, 'Detalhes')
                function.gerarBindsHover(janela2, 'Fechar')

############################### CONTROLE - DESATIVAR CONTA ###################
            if event == 'Desativar conta':
                if janela2 is not None:
                    janela2.close()
                janela2 = janela.desativarConta()
                function.gerarBindsHover(janela2, 'Desativar')
                function.gerarBindsHover(janela2, 'Fechar')

############################### CONTROLE - ATIVAR CONTA ###################
            if event == 'Ativar conta':
                if janela2 is not None:
                    janela2.close()
                janela2 = janela.ativarConta()
                function.gerarBindsHover(janela2, 'Ativar')
                function.gerarBindsHover(janela2, 'Fechar')

############################### CONTROLE - INFORMAÇÕES DE STAFFS ###################
            if event == 'Informações de staffs':
                if janela2 is not None:
                    janela2.close()
                janela2 = janela.infoStaffs()
                function.gerarBindsHover(janela2, 'Informações')
                function.gerarBindsHover(janela2, 'Fechar')

############################### CONTROLE - ATUALIZAR CARGOS ###################                
            if event == 'Atualizar cargo':
                if janela2 is not None:
                    janela2.close()
                janela2 = janela.trocarCargo()
                function.gerarBindsHover(janela2, 'Fechar')
                function.gerarBindsHover(janela2, 'Atualizar')

############################### ADMINISTRAÇÃO - VER PONTOS ABERTOS ###############################
            if event == 'Ver pontos abertos':
                if janela2 is not None:
                    janela2.close()
                janela2 = janela.VerPonto()
                function.gerarBindsHover(janela2, 'Fechar')

############################### ADMINISTRAÇÃO - FECHAR PONTOS ABERTOS ###############################
            if event == 'Fechar pontos abertos':
                if janela2 is not None:
                    janela2.close()
                janela2 = janela.fecharPontos()
                function.gerarBindsHover(janela2, 'Fechar Ponto')
                function.gerarBindsHover(janela2, 'Fechar')

############################### ADMINISTRAÇÃO - CANCELAR PONTOS ABERTOS ###############################
            if event == 'Cancelar pontos abertos':
                if janela2 is not None:
                    janela2.close()
                janela2 = janela.cancelarPontos()
                function.gerarBindsHover(janela2, 'Cancelar Ponto')
                function.gerarBindsHover(janela2, 'Fechar')

############################### BANS - BANS APLICADOS ###############################
            if event == 'Bans aplicados':
                if janela2 is not None:
                    janela2.close()
                janela2 = janela.bansAplicados()
                function.gerarBindsHover(janela2, 'Fechar')
                function.gerarBindsHover(janela2, 'Pesquisar') 

############################### BANS - POSTAR BAN APLICADO ###############################
            if event == 'Postar ban aplicado':
                if janela2 is not None:
                    janela2.close()
                janela2 = janela.postarBan()
                function.gerarBindsHover(janela2, 'Postar')
                function.gerarBindsHover(janela2, 'Fechar')

############################### FERRAMENTAS - ABRIR/FECHAR PONTO ###############################
            if event == 'Abrir/Fechar bate-ponto':
                if janela2 is not None:
                    janela2.close()
                res = function.search(function.ConectarBanco(), f"SELECT hora_inicio, hora_fim FROM pontos WHERE(staff='{nomee}' AND hora_fim='00:00:00')")
                if res == []:
                    aberto = False
                else:
                    aberto = True
                if aberto:
                    for r in res:
                        inicio = r[0]
                        __ = str(inicio)
                        inicio = __
                        de, ___ = function.checkTimeDate()
                        dec = function.checkDistance(inicio, de)
                else:
                    dec = 'FECHADO'
                janela2 = janela.AFPonto(dec)
                if dec == 'FECHADO':
                    janela2['bt_AF'].update('Abrir ponto')
                else:
                    janela2['bt_AF'].update('Fechar ponto')
                function.gerarBindsHover(janela2, "bt_AF")
                function.gerarBindsHover(janela2, "Fechar")
                
                #function.update(function.ConectarBanco(), f"INSERT INTO pontos(staff, hora_inicio, data) VALUES ('{nomee}', '{current_time}', '{current_date}')")

############################### FERRAMENTAS - LIBERAR PRA RP ###############################
            if event == 'Liberar pra RP':
                if janela2 is not None:
                    janela2.close()
                janela2 = janela.liberarRP()
                function.gerarBindsHover(janela2, 'Liberar RP')
                function.gerarBindsHover(janela2, 'Fechar')

            if event == 'Carga horária':
                if janela2 is not None:
                    janela2.close()
                janela2 = janela.cargaHoraria()
                function.gerarBindsHover(janela2, 'Fechar')
                function.gerarBindsHover(janela2, 'Encontrar')
        
        
    else: # SE NÃO FOREM JANELAS BASES


########################################### FERRAMENTAS ###########################################
################### ABRIR/FECHAR PONTO ###################
            if window.Title == titulos['cargaHoraria']:
                if event == 'Encontrar':
                    pontos = []
                    total = timedelta(hours=0, minutes=0, seconds=0)
                    ostaff = values['in-name']
                    data = f"{values['-in-year']}-{values['-in-month']}-{values['-in-day']}"
                    res = function.search(function.ConectarBanco(), f"SELECT total FROM pontos WHERE(tipo='ATD' AND staff='{ostaff}' AND data='{data}')")
                    for r in res:
                        bb = r[0]
                        total += bb
                    if res != []:
                        pontos.append(f'{ostaff} {total}')
                    janela2['tablepontosf'].update(values=pontos)

            if window.Title == titulos['trocarCargo']:
                if event == 'Atualizar':
                    novo = values['in-new']
                    staff = values['listastf'][0].split(' | ')[0]
                    function.update(function.ConectarBanco(), f"UPDATE staffs SET privLevel='{novo}' WHERE login='{staff}'")
                    sg.popup('Atualizado!', icon=iconbase64)
                    nv = function.checkPrivLevel(int(novo))
                    function.sendDiscord(f"{nomee} atualizou o cargo de {staff}| Novo cargo: {nv}")
            if window.Title == titulos['AFPonto']:
                if event == 'bt_AF':
                    if window[event].get_text() == 'Abrir ponto':
                        current_time, current_date = function.checkTimeDate()
                        function.update(function.ConectarBanco(), f"INSERT INTO pontos(staff, hora_inicio, data, tipo) VALUES ('{nomee}', '{current_time}', '{current_date}', 'ATD')")
                        if janela2 is not None:
                            janela2.close()
                        res = function.search(function.ConectarBanco(), f"SELECT hora_inicio, hora_fim FROM pontos WHERE(staff='{nomee}' AND hora_fim='00:00:00')")
                        if res == []:
                            aberto = False
                        else:
                            aberto = True
                        if aberto:
                            for r in res:
                                inicio = r[0]
                                __ = str(inicio)
                                inicio = __
                                de, ___ = function.checkTimeDate()
                                dec = function.checkDistance(inicio, de)
                        else:
                            dec = 'FECHADO'
                        janela2 = janela.AFPonto(dec)
                        if dec == 'FECHADO':
                            janela2['bt_AF'].update('Abrir ponto')
                        else:
                            janela2['bt_AF'].update('Fechar ponto')
                        function.gerarBindsHover(janela2, "bt_AF")
                        function.gerarBindsHover(janela2, "Fechar")
                        sg.popup('Ponto aberto!', title='Sucesso!', icon=iconbase64)

                    if window[event].get_text() == 'Fechar ponto':
                        current_time, current_date = function.checkTimeDate()
                        res = function.search(function.ConectarBanco(), f"SELECT hora_inicio FROM pontos WHERE(staff='{nomee}' AND hora_fim='00:00:00')")
                        for r in res:
                            inicio = r[0]
                        fim = current_time
                        inicio = r[0]
                        __ = str(inicio)
                        inicio = __
                        total = function.checkDistance(inicio, fim)
                        function.update(function.ConectarBanco(), f"UPDATE pontos SET total='{total}' WHERE(staff='{nomee}' AND hora_fim='00:00:00')")
                        function.update(function.ConectarBanco(), f"UPDATE pontos SET hora_fim='{fim}' WHERE(staff='{nomee}' AND hora_fim='00:00:00')")
                        if janela2 is not None:
                            janela2.close()
                        res = function.search(function.ConectarBanco(), f"SELECT hora_inicio, hora_fim FROM pontos WHERE(staff='{nomee}' AND hora_fim='00:00:00')")
                        if res == []:
                            aberto = False
                        else:
                            aberto = True
                        if aberto:
                            for r in res:
                                inicio = r[0]
                                __ = str(inicio)
                                inicio = __
                                de, ___ = function.checkTimeDate()
                                dec = function.checkDistance(inicio, de)
                        else:
                            dec = 'FECHADO'
                        janela2 = janela.AFPonto(dec)
                        if dec == 'FECHADO':
                            janela2['bt_AF'].update('Abrir ponto')
                        else:
                            janela2['bt_AF'].update('Fechar ponto')
                        function.gerarBindsHover(janela2, "bt_AF")
                        function.gerarBindsHover(janela2, "Fechar")
                        sg.popup('Ponto fechado!', title='Sucesso!', icon=iconbase64)

################### LIBERAR PRA RP ###################
            if window.Title == titulos['liberarRP']:
                if event == 'Liberar RP':
                    staff = values['listalib'][0].split(' | ')[0]
                    current_time, current_date = function.checkTimeDate()
                    function.update(function.ConectarBanco(), f"INSERT INTO pontos(staff, hora_inicio, data, tipo) VALUES ('{staff}', '{current_time}', '{current_date}', 'RP')")
                    sg.popup('Staff liberado com sucesso!', title='Liberado!', icon=iconbase64)
                    function.sendDiscord(f"{staff} liberado para RP por {nomee}")




#####################################################################################################################



########################################### BANS ###########################################
################### BANS APLICADOS ###################
            if window.Title == titulos['bansAplicados']:
                if event == 'Pesquisar':
                    try:
                        bans = []
                        res = function.search(function.ConectarBanco(), f"SELECT * FROM bans WHERE playerid='{int(values['searchban'])}'")
                        for r in res:
                            staff = r[0].replace(' ', '-')
                            gameid = str(r[1])
                            gameid = gameid.replace(' ', '-')
                            motivo = r[2].replace(' ', '-')
                            duracao = r[3].replace(' ', '-')
                            prova = r[4].replace(' ', '-')
                            bans.append(f'{staff} {gameid} {motivo} {duracao} {prova}')
                        window["tablebans"].update(values=bans)
                    except Exception as e:
                        etostring = e
                        etostring = str(etostring)
                        if etostring.startswith("invalid literal for int() with base 10:"):
                            sg.popup('O ID precisa ser um número inteiro.', icon=iconbase64)
                        else:
                            print(e)

################### POSTAR BANS APLICADOS ###################
            if window.Title == titulos['postarBan']:
                if event == 'Postar':
                    did = values['in-id']
                    dmotivo = values['in-motivo']
                    dprova = values['in-prova']
                    dduracao = values['in-duracao']
                    if did != "" and dmotivo != "" and dprova != "" and dduracao != "":
                        try:
                            did = int(did)
                            thestaff = nomee
                            function.update(function.ConectarBanco(), f"INSERT INTO bans(staff, playerid, motivo, duracao, prova) VALUES('{thestaff}','{did}', '{dmotivo}', '{dduracao}', '{dprova}')")
                            janela2.close()
                            sg.popup('Postado com sucesso!', title='Postado!', icon=iconbase64)
                            function.sendDiscord(f"Novo ban postado por {nomee}")
                        except Exception as e:
                            etostring = e
                            etostring = str(etostring)
                            if etostring.startswith("invalid literal for int() with base 10:"):
                                sg.popup('O ID precisa ser um número inteiro.', icon=iconbase64)
                            else:
                                print(e)
                    else:
                        sg.popup('Algum campo está em branco!', icon=iconbase64)



#####################################################################################################################




########################################### ADMINISTRAÇÃO ###########################################
################### VER PONTOS ABERTOS ###################

################### FECHAR PONTOS ABERTOS ###################
            if window.Title == titulos['fecharPontos']:
                if event == 'Fechar Ponto':
                    staff = values['listpontosab'][0].split(' | ')[0]
                    inicio = values['listpontosab'][0].split(' | ')[1]
                    fim, ___ = function.checkTimeDate()
                    total = function.checkDistance(inicio, fim)
                    function.update(function.ConectarBanco(), f"UPDATE pontos SET total='{total}' WHERE(staff='{staff}' AND hora_fim='00:00:00')")
                    function.update(function.ConectarBanco(), f"UPDATE pontos SET hora_fim='{fim}' WHERE(staff='{staff}' AND hora_fim='00:00:00')")
                    janela2.close()
                    janela2 = janela.fecharPontos()
                    sg.popup(f'O ponto de {staff} foi fechado com sucesso!', title='Fechado!', icon=iconbase64)     
                    function.sendDiscord(f"{nomee} fechou o ponto de {staff} ({total})")           


################### CANCELAR PONTOS ABERTOS ###################
            if window.Title == titulos['cancelarPontos']:
                if event == 'Cancelar Ponto':
                    staff = values['listpontosab2'][0].split(' | ')[0]
                    inicio = values['listpontosab2'][0].split(' | ')[1]
                    function.update(function.ConectarBanco(), f"DELETE FROM pontos WHERE(staff='{staff}' AND hora_fim='00:00:00')")
                    janela2.close()
                    janela2 = janela.cancelarPontos()
                    function.gerarBindsHover(janela2, 'Cancelar Ponto')
                    function.gerarBindsHover(janela2, 'Fechar')
                    sg.popup(f'O ponto de {staff} foi cancelado com sucesso!', title='Cancelado!', icon=iconbase64)   
                    function.sendDiscord(f"{nomee} cancelou o ponto de {staff} (Iniciado às {inicio})")



#####################################################################################################################




########################################### CONTROLE ###########################################
################### POSTAR AVISO STAFF ###################
            if window.Title == titulos['postarAviso']:
                if event == 'Aplicar aviso':
                    aplicador = nomee
                    nomestaff = values['listt'][0].split(' | ')[0]
                    idstaff = values['listt'][0].split(' | ')[1]
                    motivo = values['motivo']
                    prova = values['prova']
                    function.update(function.ConectarBanco(), f"INSERT INTO avisostaff(aplicador, staffid, motivo, prova) VALUES('{aplicador}', '{idstaff}', '{motivo}', '{prova}')")
                    sg.popup('Aviso aplicado com sucesso!', title='Aplicado!', icon=iconbase64)
                    function.sendDiscord(f"{nomee} aplicou um aviso staff em {nomestaff} ({motivo})")

################### APROVAR REGISTRO ###################
            if window.Title == titulos['aprovarReg']:
                if event == 'Aprovar':
                    aprovado = values['listamem']
                    aprovadonome = aprovado[0].split(' | ')[0]
                    aprovadoid = aprovado[0].split(' | ')[1]
                    res = function.search(function.ConectarBanco(), f"SELECT * FROM registros WHERE login='{aprovadonome}'")
                    for r in res:
                        nc = r[0]
                        login = r[1]
                        senha = r[2]
                        gameid = r[3]
                        serial = r[4]
                        number = r[5]
                        privLl = 1
                    function.update(function.ConectarBanco(), f"INSERT INTO staffs(nomecompleto, login, senha, gameid, serial, numero, privLevel) VALUES('{nc}', '{login}', '{senha}', '{gameid}', '{serial}', '{number}', '{privLl}')")
                    function.update(function.ConectarBanco(), f"DELETE FROM registros WHERE login='{login}'")
                    janela2.close()
                    janela2 = janela.aprovarReg()
                    function.gerarBindsHover(janela2, 'Aprovar')
                    function.gerarBindsHover(janela2, 'Detalhes')
                    function.gerarBindsHover(janela2, 'Fechar')
                    function.sendDiscord(f"{nomee} aprovou um novo staff: {login}")

                if event == 'Detalhes':
                    sslog = values['listamem']
                    log = sslog[0].split(' | ')[0]
                    res = function.search(function.ConectarBanco(), f"SELECT * FROM registros WHERE login='{log}'")
                    for r in res:
                        nc = r[0]
                        senha = r[2]
                        gameid = r[3]
                        serial = r[4]
                        number = r[5]
                    sg.popup(f'Nome completo: {nc}\nLogin: {log}\nID: {gameid}\nSerial: {serial}\nNúmero: {number}\n\n\n', no_titlebar=True, grab_anywhere=True, icon=iconbase64)

################### DESATIVAR CONTA ###################
            if window.Title == titulos['desativarConta']:
                if event == 'Desativar':
                    sslog = values['listcontas']
                    log = sslog[0].split(' | ')[0]
                    res = function.search(function.ConectarBanco(), f"SELECT * FROM staffs WHERE login='{log}'")
                    for r in res:
                        nc = r[0]
                        senha = r[2]
                        gameid = r[3]
                        serial = r[4]
                        number = r[5]
                        privv = r[6]
                    function.update(function.ConectarBanco(), f"INSERT INTO desativados(nomecompleto, login, senha, gameid, serial, numero, privLevel) VALUES('{nc}', '{log}', '{senha}', '{gameid}', '{serial}', '{number}', '{privv}')")
                    function.update(function.ConectarBanco(), f"DELETE FROM staffs WHERE login='{log}'")
                    janela2.close()
                    janela2 = janela.desativarConta()
                    sg.popup('Conta desativada!', icon=iconbase64)
                    function.gerarBindsHover(janela2, 'Fechar')
                    function.gerarBindsHover(janela2, 'Desativar')
                    function.sendDiscord(f"{nomee} desativou a conta: {log}")

################### ATIVAR CONTA ###################
            if window.Title == titulos['ativarConta']:
                if event == 'Ativar':
                    sslog = values['listcontasd']
                    log = sslog[0].split(' | ')[0]
                    res = function.search(function.ConectarBanco(), f"SELECT * FROM desativados WHERE login='{log}'")
                    for r in res:
                        nc = r[0]
                        senha = r[2]
                        gameid = r[3]
                        serial = r[4]
                        number = r[5]
                        privv = r[6]
                    function.update(function.ConectarBanco(), f"INSERT INTO staffs(nomecompleto, login, senha, gameid, serial, numero, privLevel) VALUES('{nc}', '{log}', '{senha}', '{gameid}', '{serial}', '{number}', '{privv}')")
                    function.update(function.ConectarBanco(), f"DELETE FROM desativados WHERE login='{log}'")
                    janela2.close()
                    janela2 = janela.ativarConta()
                    sg.popup('Conta ativada!', icon=iconbase64)
                    function.gerarBindsHover(janela2, 'Fechar')
                    function.gerarBindsHover(janela2, 'Ativar')
                    function.sendDiscord(f"{nomee} ativou a conta: {log}")

################### INFORMAÇÕES DE STAFFS ###################
            if window.Title == titulos['infoStaffs']:
                if event == 'Informações':
                    sslog = values['listainfo']
                    log = sslog[0].split(' | ')[0]
                    res = function.search(function.ConectarBanco(), f"SELECT * FROM staffs WHERE login='{log}'")
                    for r in res:
                        nc = r[0]
                        senha = r[2]
                        gameid = r[3]
                        serial = r[4]
                        number = r[5]
                    sg.popup(f'Nome completo: {nc}\nLogin: {log}\nID: {gameid}\nSerial: {serial}\nNúmero: {number}\n\n\n', no_titlebar=True, grab_anywhere=True, icon=iconbase64)


