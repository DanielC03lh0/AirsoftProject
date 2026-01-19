#!/usr/bin/env python3
"""
Script para testar componentes individuais da bomba simulada
"""

import sys
import time
import RPi.GPIO as GPIO

def test_leds():
    """Testa os LEDs"""
    print("\n=== Teste de LEDs ===")
    from config import LED_PINS
    from leds import LEDController
    
    try:
        leds = LEDController()
        print(f"LEDs configurados nos pins: {LED_PINS}")
        print("Testando LEDs...")
        
        print("1. Ligando todos os LEDs por 2 segundos...")
        leds.turn_on()
        time.sleep(2)
        
        print("2. Desligando todos os LEDs...")
        leds.turn_off()
        time.sleep(1)
        
        print("3. Piscando LEDs por 3 segundos...")
        leds.start_blinking()
        time.sleep(3)
        leds.stop_blinking()
        
        print("✓ LEDs funcionando corretamente!")
        leds.cleanup()
        return True
    except Exception as e:
        print(f"✗ Erro ao testar LEDs: {e}")
        return False

def test_display():
    """Testa o display"""
    print("\n=== Teste de Display ===")
    from display import LCDDisplay
    
    try:
        display = LCDDisplay()
        print("Testando display...")
        
        print("1. Limpando display...")
        display.clear()
        time.sleep(1)
        
        print("2. Escrevendo texto de teste...")
        display.print("TESTE DISPLAY", 0, 2)
        display.print("FUNCIONANDO!", 1, 3)
        time.sleep(3)
        
        print("3. Testando formatação de tempo...")
        display.clear()
        for i in range(5, 0, -1):
            display.print_time(i * 60)
            display.print_status(f"Teste: {i}")
            time.sleep(1)
        
        display.clear()
        display.print("TESTE OK!", 0, 3)
        time.sleep(2)
        
        print("✓ Display funcionando corretamente!")
        display.close()
        return True
    except Exception as e:
        print(f"✗ Erro ao testar display: {e}")
        print("  Verifique as conexões I2C e o endereço em config.py")
        return False

def test_keypad():
    """Testa o teclado"""
    print("\n=== Teste de Teclado ===")
    from keypad import KeypadReader
    
    try:
        print("Escolha o tipo de teclado:")
        print("1. Teclado USB (recomendado)")
        print("2. Teclado Matricial 4x4")
        choice = input("Escolha (1 ou 2): ").strip()
        
        use_matrix = (choice == "2")
        keypad = KeypadReader(use_matrix=use_matrix)
        
        print("\nTestando teclado...")
        print("Pressione algumas teclas (pressione 'q' para sair):")
        
        start_time = time.time()
        while time.time() - start_time < 10:  # 10 segundos de teste
            key = keypad.get_key()
            if key:
                if key.lower() == 'q':
                    break
                print(f"Tecla pressionada: '{key}'")
            time.sleep(0.1)
        
        print("\n✓ Teclado funcionando corretamente!")
        keypad.cleanup()
        return True
    except Exception as e:
        print(f"✗ Erro ao testar teclado: {e}")
        return False

def test_buzzer():
    """Testa o buzzer"""
    print("\n=== Teste de Buzzer ===")
    from config import BUZZER_PIN
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUZZER_PIN, GPIO.OUT)
        
        print(f"Buzzer configurado no pin: {BUZZER_PIN}")
        print("Tocando 3 beeps...")
        
        for i in range(3):
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(0.2)
        
        print("✓ Buzzer funcionando corretamente!")
        GPIO.cleanup()
        return True
    except Exception as e:
        print(f"✗ Erro ao testar buzzer: {e}")
        print("  Buzzer pode não estar conectado (opcional)")
        GPIO.cleanup()
        return False

def main():
    """Função principal de teste"""
    print("="*50)
    print("TESTE DE COMPONENTES - BOMBA SIMULADA")
    print("="*50)
    
    results = {}
    
    # Testar cada componente
    results['LEDs'] = test_leds()
    time.sleep(1)
    
    results['Display'] = test_display()
    time.sleep(1)
    
    results['Teclado'] = test_keypad()
    time.sleep(1)
    
    results['Buzzer'] = test_buzzer()
    
    # Resumo
    print("\n" + "="*50)
    print("RESUMO DOS TESTES")
    print("="*50)
    for component, status in results.items():
        status_symbol = "✓" if status else "✗"
        print(f"{status_symbol} {component}: {'OK' if status else 'FALHOU'}")
    
    all_ok = all(results.values())
    if all_ok:
        print("\n✓ Todos os componentes estão funcionando!")
    else:
        print("\n⚠ Alguns componentes falharam. Verifique as conexões.")
    
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTeste interrompido pelo usuário.")
        GPIO.cleanup()
        sys.exit(0)
