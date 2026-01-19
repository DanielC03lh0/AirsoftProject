"""
Módulo para ler o teclado numérico
Suporta teclado matricial 4x4 e teclado USB numérico
"""

import RPi.GPIO as GPIO
import time
import sys
import select
import termios
import tty
from config import KEYPAD_ROWS, KEYPAD_COLS, KEYPAD_MAP

class KeypadReader:
    """Classe para ler entrada do teclado"""
    
    def __init__(self, use_matrix=True):
        self.use_matrix = use_matrix
        self.current_code = ""
        self.last_key_time = time.time()
        
        if use_matrix:
            self._init_matrix_keypad()
        else:
            self._init_usb_keyboard()
    
    def _init_matrix_keypad(self):
        """Inicializa teclado matricial 4x4"""
        GPIO.setmode(GPIO.BCM)
        
        # Configurar linhas como saída
        for row in KEYPAD_ROWS:
            GPIO.setup(row, GPIO.OUT)
            GPIO.output(row, GPIO.HIGH)
        
        # Configurar colunas como entrada com pull-down
        for col in KEYPAD_COLS:
            GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    def _init_usb_keyboard(self):
        """Inicializa leitura de teclado USB"""
        # Configurar terminal para leitura de tecla única
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
    
    def read_matrix_key(self):
        """Lê tecla do teclado matricial"""
        for row_idx, row in enumerate(KEYPAD_ROWS):
            GPIO.output(row, GPIO.LOW)
            for col_idx, col in enumerate(KEYPAD_COLS):
                if GPIO.input(col) == GPIO.HIGH:
                    GPIO.output(row, GPIO.HIGH)
                    time.sleep(0.1)  # Debounce
                    return KEYPAD_MAP[row_idx][col_idx]
            GPIO.output(row, GPIO.HIGH)
        return None
    
    def read_usb_key(self):
        """Lê tecla do teclado USB"""
        if select.select([sys.stdin], [], [], 0.1)[0]:
            key = sys.stdin.read(1)
            if key.isdigit() or key in ['*', '#', '\n', '\r']:
                return key
        return None
    
    def get_key(self):
        """Obtém uma tecla pressionada"""
        if self.use_matrix:
            return self.read_matrix_key()
        else:
            return self.read_usb_key()
    
    def get_code(self, max_digits=4, timeout=None):
        """
        Obtém código numérico do usuário
        Retorna o código inserido ou None se timeout
        """
        code = ""
        start_time = time.time()
        
        print(f"\nDigite o código ({max_digits} dígitos): ", end='', flush=True)
        
        while len(code) < max_digits:
            if timeout and (time.time() - start_time) > timeout:
                print("\nTimeout!")
                return None
            
            key = self.get_key()
            
            if key:
                if key.isdigit():
                    code += key
                    print('*', end='', flush=True)
                    self.last_key_time = time.time()
                elif key in ['\n', '\r', '#']:
                    if len(code) == max_digits:
                        print()
                        return code
                elif key == '*':
                    # Limpar código
                    code = ""
                    print("\nCódigo limpo. Digite novamente: ", end='', flush=True)
            
            time.sleep(0.05)
        
        print()
        return code
    
    def cleanup(self):
        """Limpa recursos"""
        if not self.use_matrix:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
