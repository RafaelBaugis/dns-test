import dns.resolver
import time
import matplotlib.pyplot as plt

arquivo = open('servidores.txt', 'r')

linhas = arquivo.readlines()

arquivo.close()

servidores = []

for linha in linhas:
    linha = linha.strip()
    if linha and not linha.startswith('#'):
        enderecos = linha.split()
        servidores.append(enderecos)

print(servidores)

hostes = ['google.com', 'facebook.com', 'amazon.com']

tempos = {}

for servidor in servidores:
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = servidor
    resolver.lifetime = 10

    total = 0

    tempos_hostes = []

    for hoste in hostes:
        try:
            start = time.time()

            answers = resolver.resolve(hoste)

            end = time.time()

            tempo = end - start
            total += tempo

            tempos_hostes.append(tempo)
        except dns.resolver.NXDOMAIN:
            print(f'Hoste {hoste} não encontrado no servidor {servidor}')
        except dns.resolver.Timeout:
            print(f'Servidor {servidor} não respondeu no tempo limite')
        except dns.exception.DNSException as e:
            print(f'Erro ao consultar o servidor {servidor}: {e}')

    media = total / len(hostes)

    tempos[str(servidor)] = (media, tempos_hostes)

print(tempos)

fig, ax = plt.subplots()

cores = ['r', 'g', 'b']

x_pos = 0

for servidor, (media, tempos_hostes) in tempos.items():
    y_pos = 0

    for i, tempo in enumerate(tempos_hostes):
        ax.bar(x_pos, tempo, color=cores[i], bottom=y_pos)

        y_pos += tempo
    
    x_pos += 1

ax.set_xticks(range(len(tempos)))

labels = [label.replace(',', '\n').replace('[', '').replace(']', '') for label in tempos.keys()]
ax.set_xticklabels(labels)

ax.set_ylabel('Segundos')

ax.set_title('Tempos de consulta por servidor dns')

ax.legend(hostes)

plt.show()