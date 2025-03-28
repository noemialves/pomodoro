import time
from pygame import mixer
import os
import sys
from datetime import datetime

mixer.init()

def play_alarm():
    try:
        mixer.music.load('/usr/share/sounds/freedesktop/stereo/complete.oga')
        mixer.music.play()
        time.sleep(1)
    except:
        print("\a")

def dynamic_countdown(seconds, block_info):
    start_time = time.time()
    end_time = start_time + seconds
    try:
        print(f"⏳ {block_info} | Tempo restante: {seconds//60:02d}:{seconds%60:02d} ", end="\r")
        
        while time.time() < end_time:
            remaining = end_time - time.time()
            mins, secs = divmod(int(remaining), 60)
            
            print(f"⏳ {block_info} | Tempo restante: {mins:02d}:{secs:02d} ", end="\r")
            time.sleep(1)
            
        print() 
    except KeyboardInterrupt:
        print("\n") 
        return int(end_time - time.time())

def run_block(block, block_number, remaining_seconds=None):
    os.system('clear')
    total_duration = block["duration"] * 60
    remaining = remaining_seconds if remaining_seconds is not None else total_duration
    
    print(f"\n📅 Período: {'MANHÃ' if block_number < 9 else 'TARDE' if block_number < 17 else 'NOITE'}")
    print(f"⏰ Horário: {block['start']} - {block['end']}")
    print(f"📝 Atividade: {block['name']}\n")
    
    remaining = dynamic_countdown(remaining, block['type'].upper())
    
    if remaining is not None:
        print(f"⏸ Pausa manual - {remaining//60:02d}:{remaining%60:02d} restantes")
        return remaining
    
    play_alarm()
    return None

full_schedule = [
    # Manhã
    {"start": "08:00", "end": "08:40", "name": "Bloco de foco", "duration": 40, "type": "trabalho"},
    {"start": "08:40", "end": "08:45", "name": "Intervalo curto", "duration": 5, "type": "intervalo"},
    {"start": "08:45", "end": "09:25", "name": "Bloco de foco", "duration": 40, "type": "trabalho"},
    {"start": "09:25", "end": "09:30", "name": "Intervalo curto", "duration": 5, "type": "intervalo"},
    {"start": "09:30", "end": "10:10", "name": "Bloco de foco", "duration": 40, "type": "trabalho"},
    {"start": "10:10", "end": "10:20", "name": "Intervalo longo", "duration": 10, "type": "intervalo"},
    {"start": "10:20", "end": "11:00", "name": "Bloco de foco", "duration": 40, "type": "trabalho"},
    {"start": "11:00", "end": "11:05", "name": "Intervalo curto", "duration": 5, "type": "intervalo"},
    {"start": "11:05", "end": "11:45", "name": "Bloco de foco", "duration": 40, "type": "trabalho"},
    {"start": "12:45", "end": "13:45", "name": "Pausa Almoço", "duration": 60, "type": "intervalo"},  

    # Tarde 
    {"start": "13:45", "end": "14:25", "name": "Bloco de foco", "duration": 40, "type": "trabalho"},
    {"start": "14:25", "end": "14:30", "name": "Intervalo curto", "duration": 5, "type": "intervalo"},
    {"start": "14:30", "end": "15:10", "name": "Bloco de foco", "duration": 40, "type": "trabalho"},
    {"start": "15:10", "end": "15:20", "name": "Intervalo longo", "duration": 10, "type": "intervalo"},
    {"start": "15:20", "end": "16:00", "name": "Bloco de foco", "duration": 40, "type": "trabalho"},
    {"start": "16:00", "end": "16:05", "name": "Intervalo curto", "duration": 5, "type": "intervalo"},
    {"start": "16:05", "end": "16:45", "name": "Bloco de foco", "duration": 40, "type": "trabalho"},
    {"start": "16:45", "end": "17:00", "name": "Intervalo longo", "duration": 15, "type": "intervalo"},

    # Noite 
    {"start": "17:00", "end": "17:40", "name": "Estudos específicos", "duration": 40, "type": "estudo"},
    {"start": "17:40", "end": "17:45", "name": "Intervalo curto", "duration": 5, "type": "intervalo"},
    {"start": "17:45", "end": "18:25", "name": "Estudos específicos", "duration": 40, "type": "estudo"},
    {"start": "18:25", "end": "18:30", "name": "Intervalo curto", "duration": 5, "type": "intervalo"},
    {"start": "18:30", "end": "19:10", "name": "Estudos específicos", "duration": 40, "type": "estudo"},
    {"start": "19:10", "end": "19:15", "name": "Intervalo curto", "duration": 5, "type": "intervalo"},
    {"start": "19:15", "end": "19:55", "name": "Último Bloco", "duration": 40, "type": "estudo"}
]

def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M").time()

def get_current_block_index(current_time):
    for i, block in enumerate(full_schedule):
        start_time = parse_time(block["start"])
        end_time = parse_time(block["end"])
        
        if start_time <= current_time.time() < end_time:
            return i
        if i == len(full_schedule) - 1 and current_time.time() >= end_time:
            return len(full_schedule) - 1
    return 0

def calculate_remaining_time(block, current_time):
    block_end = datetime.combine(current_time.date(), parse_time(block["end"]))
    if current_time < block_end:
        return (block_end - current_time).seconds
    return 0

def main():
    print("⏰ Iniciando Agenda de Produtividade Dinâmica ⏰")
    print("Atalhos:\nCtrl+C → Pausar bloco atual\n")
    
    try:
        while True:
            current_time = datetime.now()
            start_index = get_current_block_index(current_time)
            
            if start_index >= len(full_schedule):
                print("🏁 Todos os blocos programados foram concluídos!")
                if input("Deseja reiniciar do início? (s/n): ").lower() != 's':
                    print("\n🎉 Bom descanso! Até a próxima!")
                    break
                continue
                
            current_block = full_schedule[start_index]
            remaining_seconds = calculate_remaining_time(current_block, current_time)
            remaining = run_block(current_block, start_index, remaining_seconds)
            os.system('clear')
            
    except KeyboardInterrupt:
        print("\n\n⏹ Agenda interrompida pelo usuário")

if __name__ == "__main__":
    main()