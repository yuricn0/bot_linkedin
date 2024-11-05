import PySimpleGUI as sg
from threading import Thread
from app import automatizar_convites_linkedin


sg.theme('Reddit')

layout = [
[sg.Text('Pesquisar profissão:'), sg.Input(key='cargo', size=(20,0))],
[sg.Text('Mensagem no convite:')],
[sg.Multiline(key='mensagem', size=(48, 5))],
[sg.Text('Avisos:')],
[sg.Output(size=(48,10))],
[sg.Button('Enviar', key='botao_enviar')],
]

window = sg.Window('LinkedIn', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'botao_enviar':
        cargo = values['cargo']
        mensagem = values['mensagem']
        thread_linkedin = Thread(target=automatizar_convites_linkedin, args=(cargo, mensagem), daemon=True)
        thread_linkedin.start()

        window['cargo'].update(disabled=True)
        window['mensagem'].update(disabled=True)
        window['botao_enviar'].update(disabled=True)