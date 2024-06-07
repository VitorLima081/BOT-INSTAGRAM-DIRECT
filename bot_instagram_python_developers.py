import telebot
import requests
import logging
from flask import Flask, request, jsonify
from openai import OpenAI
from pathlib import Path
import uuid
import datetime
from datetime import timedelta
import time
import logging
import sqlite3
import threading


#INICIANDO O FLASK
app = Flask(__name__)
#INICIANDO O CLIENTE OPENAI
client = OpenAI(api_key='sk-proj-rwFVgr8b4MGaUfIafAJXT3BlbkFJmQABTwBnjBTupTC5MzcB')

#VARIAVEIS DE CONFIGURAÇÕES
CHAVE_TELEGRAM = '7143724464:AAEADk8anTLcBQ0A8T4xslIOD9hOSWTKyFs'
BOT = telebot.TeleBot(CHAVE_TELEGRAM)
ACCESS_TOKEN='EAAXPj6OzA3oBOxZB1jXEzEvoGMitEvEAK1mQCv0dNSDS5cjsHZBxm4WYXhPo3mjHCQ6TfaQuxLMLZCHlPZAxCwhBynn7e22oUg04kzO7ZBq3kEAjizh6HJBXgkGYU2SNGydPmZCqJ31NprkAhiMJvZCo21Qhd7o4grV8XkRZBubPSqMYeamp3ReWMGUwxbWjsN1ZAEzJJpfMP4VX2ZB8Ek'
APP_ID='104077894747816'
APP_SECRET="ac481f183cf46f41e374378b70193277"
VERSION="v19.0"
VERIFY_TOKEN="VITORXAMA"
ocupado = False

#INICIANDO ROTA PARA RECEBER AS MENSAGENS COM O NGROK:
#ngrok http 8000 --domain oryx-romantic-condor.ngrok-free.app

id_mensagens_deletadas = []

try:
    @app.route('/', methods=['GET', 'POST'])
    def handle_request():
        if request.method == 'GET':
            hub_challenge = request.args.get('hub.challenge', '')
            logging.info("Received hub.challenge: %s", hub_challenge)
            return hub_challenge, 200
        elif request.method == 'POST':
            try:
                logging.info("Received POST request from Facebook")
                data = request.json
                print(data)
                id_usuario = data['entry'][0]['messaging'][0]['sender']['id']
                mensagem_recebida = data['entry'][0]['messaging'][0]['message'].get('text', '')
                is_deleted = data['entry'][0]['messaging'][0]['message'].get('is_deleted', False)

                conn = sqlite3.connect('usuarios_instagram.db')
                cursor = conn.cursor()

                if is_deleted:
                    cursor.execute('SELECT * FROM clientes WHERE chat_id = ?', (id_usuario,))
                    resultado = cursor.fetchone()
                    if resultado:
                        cursor.execute('DELETE FROM clientes WHERE chat_id = ?', (id_usuario,))
                        conn.commit()
                    print('O USUARIO EXCLUIU A MENSAGEM E FOI EXPULSO DO BANCO DE DADOS!')
                else:
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS clientes (
                            chat_id INTEGER PRIMARY KEY,
                            compra TEXT
                        )
                    ''')
                    cursor.execute('INSERT OR REPLACE INTO clientes (chat_id, compra) VALUES (?, ?)',
                                (id_usuario, mensagem_recebida))
                    conn.commit()
                
                conn.close()
                return jsonify({"status": "success"}), 200
            except Exception as e:
                logging.error("Error processing POST request: %s", e)
                return jsonify({"status": "error", "message": str(e)}), 500

    def enviando_mensagem_instagram(id_usuario, texto):
        try:
            url = f"https://graph.facebook.com/{VERSION}/{APP_ID}/messages"
            data = {
                "recipient": {"id": id_usuario},
                "message": {"text": f'https://drive.google.com/file/d/1ClzssRkpOUru_XaNhdoSfJnKb3bSTGhZ/view?usp=sharing\n\n {texto}\n\n🚨 Após a leitura do documento, caso tenha interesse em iniciar o processo para desenvolver seu BOT para WhatsApp, por favor, entre em contato conosco VIA WHATSAPP!\n\n📞 81995447857'},
                "messaging_type": "RESPONSE",
                "access_token": ACCESS_TOKEN
            }
            response = requests.post(url, json=data)
            print(response.json())
            if response.status_code == 200:
                print("Mensagem enviada com sucesso!")
            else:
                print("Erro ao enviar a mensagem:", response.text) 

            conn = sqlite3.connect('usuarios_instagram.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM clientes WHERE chat_id = ?', (id_usuario,))
            resultado = cursor.fetchone()
            if resultado:
                cursor.execute('DELETE FROM clientes WHERE chat_id = ?', (id_usuario,))
                conn.commit()  
            print('O USUARIO FOI EXCLUIDO DO BANCO DE DADOS E A MENSAGEM FOI ENVIADA!')    

        except Exception as e:
            BOT.send_message(5416509396, f'O BOT DO INSTAGRAM DA PYTHON DEVELOPERS FALHOU! {e}') 
    
    
    def enviando_mensagem_telegram(id_usuario, texto):
        try:
            url = f"https://graph.facebook.com/{VERSION}/{APP_ID}/messages"
            data = {
                "recipient": {"id": id_usuario},
                "message": {"text": f'https://drive.google.com/file/d/1LOrcUEi0iIPJ6yOQuVbxOse_6x3B6ZJw/view?usp=sharing\n\n {texto}\n\n 🚨 Após a leitura do documento, caso tenha interesse em iniciar o processo para desenvolver seu BOT para WhatsApp, por favor, entre em contato conosco VIA WHATSAPP!\n\n📞 81995447857'},
                "messaging_type": "RESPONSE",
                "access_token": ACCESS_TOKEN
            }
            response = requests.post(url, json=data)
            print(response.json())
            if response.status_code == 200:
                print("Mensagem enviada com sucesso!")
            else:
                print("Erro ao enviar a mensagem:", response.text) 

            conn = sqlite3.connect('usuarios_instagram.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM clientes WHERE chat_id = ?', (id_usuario,))
            resultado = cursor.fetchone()
            if resultado:
                cursor.execute('DELETE FROM clientes WHERE chat_id = ?', (id_usuario,))
                conn.commit()  
            print('O USUARIO FOI EXCLUIDO DO BANCO DE DADOS E A MENSAGEM FOI ENVIADA')    

        except Exception as e:
            BOT.send_message(5416509396, f'O BOT DO INSTAGRAM DA PYTHON DEVELOPERS FALHOU! {e}')  

    def enviando_mensagem_whatsapp(id_usuario, texto):
        try:
            url = f"https://graph.facebook.com/{VERSION}/{APP_ID}/messages"
            data = {
                "recipient": {"id": id_usuario},
                "message": {"text": f'https://drive.google.com/file/d/1hqE4Wgfr_lTmLuVvrdeyKYosPWO68Hjh/view?usp=sharing\n\n {texto}\n\n 🚨 Após a leitura do documento, caso tenha interesse em iniciar o processo para desenvolver seu BOT para WhatsApp, por favor, entre em contato conosco VIA WHATSAPP!\n\n📞 81995447857'},
                "messaging_type": "RESPONSE",
                "access_token": ACCESS_TOKEN
            }
            response = requests.post(url, json=data)
            print(response.json())
            
            if response.status_code == 200:
                print("Mensagem enviada com sucesso!")
            else:
                print("Erro ao enviar a mensagem:", response.text) 

            conn = sqlite3.connect('usuarios_instagram.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM clientes WHERE chat_id = ?', (id_usuario,))
            resultado = cursor.fetchone()
            if resultado:
                cursor.execute('DELETE FROM clientes WHERE chat_id = ?', (id_usuario,))
                conn.commit()  
            print('O USUARIO FOI EXCLUIDO DO BANCO DE DADOS E A MENSAGEM FOI ENVIADA!')    
        
        except Exception as e:
            BOT.send_message(5416509396, f'O BOT DO INSTAGRAM DA PYTHON DEVELOPERS FALHOU! {e}')  
    
    def enviando_mensagem(id_usuario, texto):
        try:
            url = f"https://graph.facebook.com/{VERSION}/{APP_ID}/messages"
            data = {
                    "recipient": {"id": id_usuario},
                    "message": {"text": texto},
                    "messaging_type": "RESPONSE",
                    "access_token": ACCESS_TOKEN
                }
            response = requests.post(url, json=data)
            print(response.json())
            if response.status_code == 200:
                print("Mensagem enviada com sucesso!")
            else:
                print("Erro ao enviar a mensagem:", response.text) 
            conn = sqlite3.connect('usuarios_instagram.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM clientes WHERE chat_id = ?', (id_usuario,))
            resultado = cursor.fetchone()
            if resultado:
                cursor.execute('DELETE FROM clientes WHERE chat_id = ?', (id_usuario,))
                conn.commit()  
            print('O USUARIO FOI EXCLUIDO DO BANCO DE DADOS E A MENSAGEM FOI ENVIADA!')    

        except Exception as e:
            BOT.send_message(5416509396, f'O BOT DO INSTAGRAM DA PYTHON DEVELOPERS FALHOU! {e}')        
    
    def recebendo_mensagem():
        
        while True:
            time.sleep(10)
            nova_conn = sqlite3.connect('usuarios_instagram.db')
            novo_cursor = nova_conn.cursor()
            novo_cursor.execute('SELECT chat_id FROM clientes')
            todos_chat_ids = novo_cursor.fetchall()  
            if todos_chat_ids is None:
                print('O BANCO DE DADOS ESTA VAZIO!')
            else:
                for id_usuario in todos_chat_ids:
                    novo_cursor.execute('SELECT compra FROM clientes WHERE chat_id = ?', (id_usuario[0],))
                    mensagem_tratada = novo_cursor.fetchone()
                    mensagem_recebida = mensagem_tratada[0]

                    if mensagem_recebida[0] not in ['1', '2', '3', '4']:
                        texto_menu = '🤖💬 OLÁ, BEM VINDO(A) AO UNIVERSO PYTHON DEVELOPERS!\n Envie o numero correspondente ao que você deseja explorar hoje ⬇️\n\n 1. Criar BOT para WhatsApp!\n 2. Criar BOT para Instagram!\n 3. Criar BOT para Telegram!\n 4. Outros serviços!'
                        enviando_mensagem(id_usuario[0], texto_menu)

                    elif mensagem_recebida == '1':
                        texto_bot_whatsapp = '🤖💬 Segue acima um link de um arquivo PDF que serve como introdução a todas as informações necessárias para desenvolver um BOT para WhatsApp conosco, incluindo custos e as informações solicitadas pela API da plataforma!'
                        enviando_mensagem_whatsapp(id_usuario[0], texto_bot_whatsapp)

                    elif mensagem_recebida == '2':
                        texto_bot_instagram = '🤖💬 Segue acima um link de um arquivo PDF que serve como introdução a todas as informações necessárias para desenvolver um BOT para Instagram conosco, incluindo custos e as informações solicitadas pela API da plataforma!'
                        enviando_mensagem_instagram(id_usuario[0], texto_bot_instagram)
                    
                    elif mensagem_recebida == '3':
                        texto_bot_telegram = '🤖💬 Segue acima um link de um arquivo PDF que serve como introdução a todas as informações necessárias para desenvolver um BOT para Telegram conosco, incluindo custos e as informações solicitadas pela API da plataforma!'
                        enviando_mensagem_telegram(id_usuario[0], texto_bot_telegram)
                    
                    elif mensagem_recebida == '4':
                        texto_audio_agora = '🤖💬 Além dos serviços mencionados, nós da Python Developers estamos sempre abertos a novos desafios e oportunidades.\nCaso você tenha necessidades específicas ou projetos diferentes em mente, ficaremos feliz em conversar e entender melhor sua demanda. Juntos, podemos explorar as possibilidades e verificar como podemos contribuir para o sucesso do seu negócio.\n\n Entre em contato conosco via WhatsApp para explicitar sua demanda! ⬇️\n\n 📱 81995447857'
                        enviando_mensagem(id_usuario[0], texto_audio_agora) 

except Exception as e:
    BOT.send_message(5416509396, f'O BOT DA PYTHON DEVELOPERS NO INSTAGRAM FALHOU! {e}')

        
if __name__ == "__main__":
    logging.info("Flask app started")
    thread = threading.Thread(target=recebendo_mensagem)
    thread.start()
    app.run(host="0.0.0.0", port=8000)
