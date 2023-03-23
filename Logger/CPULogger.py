import psutil
import time
import datetime
import os
import sending_mail

# Festlegen der Grenzwerte
soft_limit = 10
hard_limit = 15

# Netzwerkname der Maschine
hostname = psutil.net_if_addrs()['WLAN'][0].address

# Überprüfen und Erstellen der Logdatei
log_file = './CPU-Log.txt'
if not os.path.isfile(log_file):
    with open(log_file, 'w') as f:
        f.write('Logdatei erstellt am {}\n'.format(datetime.datetime.now()))

# Funktion zum Schreiben in die Logdatei
def write_log(message):
    with open(log_file, 'a') as logfile:
        logfile.write(message + '\n')  # Hinzufügen von '\n' am Ende der Nachricht

# CPU-Frequenz abrufen und in MHz konvertieren
cpu_freq = psutil.cpu_freq().current / 1000

# CPU-Auslastung abrufen
cpu_usage = psutil.cpu_percent()

# Aktuelles Datum und Uhrzeit im ISO-Format abrufen
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

# CPU-Frequenz und Auslastung in die Log-Datei schreiben
with open(log_file, "a") as logfile:
    logfile.write(f"{timestamp}, {cpu_freq:.2f}, {cpu_usage:.2f}\n")
    
    # Warnung schreiben, falls CPU-Auslastung über Softlimit
    if cpu_usage > soft_limit:
        write_log(f"{timestamp}, CPU-Auslastung bei: {cpu_usage:.2f}%\n")

# E-Mail-Versand bei Überschreitung des Hardlimits
if cpu_usage > hard_limit:
    message = '{} - {} - ERROR: CPU usage at {}%'.format(
        datetime.datetime.now(), hostname, cpu_usage)
    write_log(message)
    subject = 'CPU exceeded on {}'.format(hostname)
    body = 'CPU usage is at {}%.'.format(cpu_usage)
    sending_mail.send_email(subject, body)