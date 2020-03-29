import argparse
import atexit
import os
import re
from subprocess import Popen
from getch.getch import find_getch
from tika import parser
from tikasuport import tikasuport

home = os.path.expanduser('~')

argsparser = argparse.ArgumentParser(prog='fbquiz', description='Programa de auxílio à resolução de questões da '
                                                                'apostila de Fernandinho.')
argsparser.add_argument('apostila', help='Caminho do arquivo PDF da apostila.')
argsparser.add_argument('--download', dest='should_download', action='store_true',
                        help='Baixa o tika-server-1.24.jar de um site remoto para ' + home + '.tika/')
argsparser.add_argument('--tika-path', dest='tika_server_path', default=home + '/.tika/tika-server-1.24.jar',
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

raw = parser.from_file(args.apostila, 'http://localhost:9998/tika')

# Removes blank lines and page numbers
content = list(filter(lambda a: len(a) > 1, raw['content'].split('\n')))

for i in content[:178]:
    print(i)

correct_answers = list()
correct_answers_index = 0
for i in content:
    if 'PRÉ-AULA PRÉ-AULA' in i:
        correct_answers_index = content.index(i)

to_be_removed = ['PRÉ-AULA ' * 6, 'AULA DE REVISÃO ' * 6, 'TEREFA DE CASA ' * 6]

correct_answers = list(filter(lambda a: a not in to_be_removed, content[correct_answers_index:]))

correct_answers = list(filter(lambda a: not re.match('^\s|\d*$', a), ''.join(correct_answers).split()))
romano_i = 0

for i in correct_answers:
    if re.match('^I|^V', i):
        del correct_answers[correct_answers.index(i)]

print('Selecione a semana que deseja estudar (número): ')

content_no_page_num = list(filter(lambda a: not re.match('^[1-9]', a), content))

weeks = []
for row in content:
    if len(weeks) == 4:
        break
    if 'SEMANA' in row:
        weeks.append(row)
print(weeks)

week_n = getch()
week = ''
for match in weeks:
    if match[7] == week_n:
        week = match

print('Agora, selecione a disciplina que quer estudar: ')
print('[B]iologia [F]ísica [Q]uímica [M]atemática [L]inguagens [H]umanas')
subject = getch().upper()

print('Por fim, selecione uma categoria: \n[P]ré-aula [R]evisão [C]asa\n')
category = getch().upper()

# Manipulates the table of contents measuring the distance from the line 
# indicating the selected week to the line of the desired section and 
# then extracts the page number that is located in the last two digits 
# in the line.
# Distance from the week header to the subject header in the PDF table of
# contents:
w_subj_dist = {'B': 1, 'F': 6, 'Q': 11, 'M': 16, 'L': 21, 'H': 26}
# Similar
subj_cat_dist = {'P': 2, 'R': 3, 'C': 4}

page = content_no_page_num[content_no_page_num.index(week) + w_subj_dist[subject] + subj_cat_dist[category]]

# Extracts page number
page = page[::-1][:3][::-1]

# Removes trailing whitespaces before the number
page = str(page).strip() + ' '

# Search for the line containing only the page number. From the index
# of that line are located the desired exercises:
page_i = content.index(page)

# These will be used to find the right index in correct_answers:
week_i = weeks.index(week)
subject_i = ['B', 'F', 'Q', 'M', 'L', 'H'].index(subject)
category_i = ['P', 'R', 'C'].index(category)

num_of_questions = int()
if category == 'C':
    num_of_questions = 15
else:
    num_of_questions = 5
next_question_i = page_i + 1
for i in range(0, num_of_questions):
    current_question_i = next_question_i
    output = list()
    if not i + 1 == num_of_questions:
        next_question_i = content.index(list(filter(lambda a: f'0{i + 2})' in a, content[current_question_i + 2:]))[0])
    else:
        next_question_i = content.index(list(filter(lambda a: '01)' in a, content[current_question_i + 2:]))[0])
    # Appends to output all the lines from the current question to the next one:
    for ii in range(current_question_i, next_question_i):
        output.append(content[ii])
    for line in output:
        print(line)
    print('\n')
    answer = getch().upper()
    if answer == correct_answers[week_i * 150 + category_i * 30 + subject_i + i * 6]:
        print('Resposta correta!', end='\n\n')
    else:
        print(f'Resposta errada! Gabarito: {correct_answers[week_i * 150 + category_i * 30 + subject_i + i * 6]}',
              end='\n\n')
