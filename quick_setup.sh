#!/bin/bash
# Script de configuração rápida - Mínimo de comandos para configurar tudo

echo "=========================================="
echo "Configuração Rápida - Bomba Simulada"
echo "=========================================="
echo ""

# Verificar se está na Raspberry Pi
if [ ! -d "/sys/class/gpio" ]; then
    echo "❌ ERRO: Este script deve ser executado em uma Raspberry Pi!"
    exit 1
fi

# 1. Ativar SPI (se não estiver ativo)
echo "1. Verificando SPI..."
if ! grep -q "dtparam=spi=on" /boot/config.txt; then
    echo "   Ativando SPI..."
    echo "dtparam=spi=on" | sudo tee -a /boot/config.txt > /dev/null
    NEEDS_REBOOT=1
else
    echo "   ✓ SPI já está ativo"
fi

# 2. Instalar dependências do sistema
echo ""
echo "2. Instalando dependências do sistema..."
sudo apt-get update -qq
sudo apt-get install -y python3-pip python3-dev python3-spidev python3-pil > /dev/null 2>&1
echo "   ✓ Dependências instaladas"

# 3. Instalar bibliotecas Python
echo ""
echo "3. Instalando bibliotecas Python..."
pip3 install --user -q RPi.GPIO Pillow spidev
echo "   ✓ Bibliotecas instaladas"

# 4. Tornar scripts executáveis
echo ""
echo "4. Configurando scripts..."
chmod +x bomb.py test_components.py install.sh 2>/dev/null
echo "   ✓ Scripts configurados"

# Resultado
echo ""
echo "=========================================="
if [ "$NEEDS_REBOOT" = "1" ]; then
    echo "⚠️  SPI foi ativado. REINICIE o sistema:"
    echo "   sudo reboot"
    echo ""
    echo "Depois de reiniciar, você pode:"
else
    echo "✅ Configuração concluída!"
    echo ""
    echo "Próximos passos:"
fi
echo "1. Monte o hardware (veja HARDWARE_SETUP.md)"
echo "2. Teste: sudo python3 test_components.py"
echo "3. Execute: sudo python3 bomb.py"
echo "=========================================="
