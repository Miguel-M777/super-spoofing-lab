
```markdown
# LabSpoofingSSL

O `LabSpoofingSSL` é uma classe Python que permite realizar um ataque de ARP spoofing e redirecionar o tráfego HTTPS destinado ao YouTube para uma máquina atacante, utilizando `sslstrip` e `iptables`. Este código deve ser usado exclusivamente em ambientes de teste controlados e com permissão explícita.

## Pré-requisitos

Antes de usar o código, certifique-se de que você possui os seguintes itens:

- Python 3 instalado.
- Bibliotecas necessárias:
  - `scapy`: Para manipulação de pacotes de rede.
  - `sslstrip`: Para redirecionamento de tráfego HTTPS.
- Acesso à linha de comando com privilégios de superusuário (root) para executar `iptables` e `sslstrip`.
- Um ambiente de teste controlado (por exemplo, uma rede local isolada).

## Instalação das dependências

Para instalar as dependências necessárias, você pode usar o `pip`:

```bash
pip install scapy
```

### Configuração do sslstrip

Certifique-se de que o `sslstrip` esteja instalado e disponível em seu PATH. Você pode encontrar instruções sobre como instalá-lo [aqui](https://github.com/moxie0/sslstrip).

### Configuração do iptables

As regras do `iptables` serão configuradas automaticamente pelo código. Certifique-se de que você tem permissões para adicionar regras ao `iptables`.

## Estrutura da Classe

### `LabSpoofingSSL`

A classe `LabSpoofingSSL` encapsula toda a funcionalidade para realizar o ataque de ARP spoofing e redirecionar o tráfego do YouTube.

#### Métodos

- **`__init__(self, target_ip, gateway_ip)`**
  - **Descrição:** Inicializa a classe com os IPs da vítima (target) e do gateway. O IP da máquina atacante é obtido automaticamente.
  - **Parâmetros:**
    - `target_ip`: O endereço IP da máquina que será a vítima do ataque (navegador).
    - `gateway_ip`: O endereço IP do gateway da rede.

- **`execute_command(self, command)`**
  - **Descrição:** Executa um comando no sistema usando `subprocess` e trata exceções.
  - **Parâmetros:**
    - `command`: O comando a ser executado no sistema.

- **`start_sslstrip(self)`**
  - **Descrição:** Inicia o `sslstrip` em segundo plano para interceptar o tráfego HTTPS.

- **`configure_iptables(self)`**
  - **Descrição:** Configura o `iptables` para redirecionar o tráfego do YouTube (tanto HTTP quanto HTTPS) para a porta onde o `sslstrip` está escutando.
  
- **`spoof_arp(self, target_ip, spoof_ip)`**
  - **Descrição:** Envia pacotes ARP spoofing para fazer com que a vítima acredite que o IP da máquina atacante é o IP do gateway ou de outro serviço.
  - **Parâmetros:**
    - `target_ip`: O IP que a vítima deve ser enganada a acreditar que está se comunicando.
    - `spoof_ip`: O IP real que está sendo spoofed (geralmente o gateway).

- **`restore_arp(self, target_ip, source_ip)`**
  - **Descrição:** Restaura a tabela ARP da vítima para a configuração original, eliminando o spoofing.
  - **Parâmetros:**
    - `target_ip`: O IP da vítima a ser restaurado.
    - `source_ip`: O IP original que a vítima deve associar ao `target_ip`.

- **`remove_iptables_rules(self)`**
  - **Descrição:** Remove as regras do `iptables` que foram adicionadas durante a configuração.

- **`run_test(self, duration=60)`**
  - **Descrição:** Executa o ataque de ARP spoofing e redirecionamento por um período especificado.
  - **Parâmetros:**
    - `duration`: Duração em segundos para o ataque (padrão é 60 segundos).

## Exemplo de Uso

```python
if __name__ == "__main__":
    target_ip = "192.168.1.5"  # IP da vítima (navegador)
    gateway_ip = "192.168.1.1"  # IP do gateway

    lab = LabSpoofingSSL(target_ip, gateway_ip)
    lab.run_test(60)  # Executa o teste por 60 segundos
```

## Nota Importante

**Uso Ético e Legal:** Este código deve ser utilizado apenas em ambientes controlados e com autorização. O uso não autorizado de técnicas de ataque pode ser ilegal e antiético. Certifique-se de seguir todas as leis e regulamentos aplicáveis.

## Contribuições

Sinta-se à vontade para contribuir com melhorias ou correções para este projeto.
```

### Observações
- **Claridade e Estrutura:** O README é estruturado de forma a facilitar a compreensão de como usar a classe e o que cada parte do código faz.
- **Aviso Legal:** A inclusão de um aviso legal enfatiza a importância do uso ético e legal do código, que é crucial ao trabalhar com técnicas de segurança de rede.
- **Instruções de instalação:** As instruções são diretas para que qualquer usuário possa configurar rapidamente seu ambiente.