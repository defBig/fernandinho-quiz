from getch.getch import find_getch
from tikasuport import tikasuport
from unidecode import unidecode
import os
import atexit
import argparse
from subprocess import Popen
from tika import parser
import re

home = os.path.expanduser('~')
argsparser = argparse.ArgumentParser(prog='fbquiz', description='Programa de auxílio à resolução de questões da apostila de Fernandinho.')
argsparser.add_argument('apostila', help='Caminho do arquivo PDF da apostila.')
argsparser.add_argument('--download', dest='should_download', action='store_true', \
help='Baixa o tika-server-1.24.jar de um site remoto para ' + home + '.tika/')
argsparser.add_argument('--tika-path', dest='tika_server_path', default=home + '/.tika/tika-server-1.24.jar', \
help='Indica o caminho para tika-server-1.24.jar.')

args = argsparser.parse_args()
getch = find_getch()

if args.should_download:
    tikasuport.download_tika(home, args.tika_server_path)
else:
    tikasuport.check_tika_exists(args.tika_server_path)

pipe = os.pipe()
server = Popen(['java', '-jar', args.tika_server_path], stdout=pipe[1], stdin=None, stderr=pipe[1])
atexit.register(server.terminate)

tikasuport.wait_for_tika(pipe[0])

raw = parser.from_file(args.apostila, "http://localhost:9998/tika")
content = list(filter(lambda a: a != '', raw['content'].split('\n')))
content = list(filter(lambda a: len(a) != 1, content))

gabarito = list()
gabarito_index = 0
for i in content:
    if "PRÉ-AULA PRÉ-AULA" in i:
        gabarito_index = content.index(i)

to_remove = ["PRÉ-AULA " * 6, "AULA DE REVISÃO " * 6, "TEREFA DE CASA " * 6]

gabarito = list(filter(lambda a: not a in to_remove, content[gabarito_index:]))

gabarito = list(filter(lambda a: not re.match("^\s|\d*$", a), ''.join(gabarito).split()))
romano_i = 0

for i in gabarito:
    if re.match("^I|^V", i):
        del gabarito[gabarito.index(i)]
for i in gabarito:
    print(i, end=' ')
getch()

#for week in range(0, 4):
#    for subject in range(0, 6):
#        for lesson in range(0, 3):
#            if lesson

print("Selecione a semana que deseja estudar (número): ")

def _is_not_num(a):
    for i in range(1, 10):
        if a[0] == str(i):
            return False
    return True
#for i in content:
#    print(i)
getch()
content_no_page_num = list(filter(_is_not_num, content))
#for i in range(0, 160):
#    print(content[i])
semanas = []
gabarito = []
for row in content:
    if len(semanas) == 4:
        break
    if "SEMANA" in row:
        semanas.append(row)
print(semanas)

num_semana = getch()
semana = ''
for match in semanas:
    if match[7] == num_semana:
        semana = match
        semana_i = semana.index(match)

print('Agora, selecione a disciplina que quer estudar: ')
print('[B]iologia [F]ísica [Q]uímica [M]atemática [L]inguagens [H]umanas')
subject = getch().upper()
subject_i = ['B', 'F', 'Q', 'M', 'L', 'H'].index(subject)

print('Por fim, selecione uma categoria: \n[P]ré-aula [R]evisão [C]asa')
category = getch().upper()
category_i = ['P', 'R', 'C'].index(category)

page = content_no_page_num[ \
content_no_page_num.index(semana) + \
{'B': 1, 'F': 6, 'Q': 11, 'M': 16, 'L': 21, 'H': 26}[subject] + \
{'P': 2, 'R': 3, 'C': 4}[category] ]\
[::-1][:3][::-1]
page_i = content.index(page)
output = []

for i in range(2, 7):
    for i in range(page_i + 1, content.index(list(filter(lambda a: f'0{i})' in a, content[page_i + 2:]))[0])):
        output.append(content[i])
    for line in output:
        print(line)
    answer = getch()
    if answer == gabarito[semana_i * 150 + category_i * 30 + subject_i]:
        print("Resposta correta!")
    else:
        print(f"Resposta errada! Gabarito: {gabarito[semana_i * 150 + category_i * 30 + subject_i]}")
#for i in range(1, 6):
#    print('\n'.join(output).split('0' + str(i) + ')'))
