import os, re

def broken_file(path):
    print('Found broken file: ' + path)
    exit(1)

def read_result(path):
    '''
        read_result(path)
        this function parses result.txt files and returns a list that contains:
        [penalty, judge score, judge score with delay, raw score]
    '''

    file = open(path, 'r')
    txt = file.read()
    groups = re.search(\
        r'penalty: (\d+)%\njudge score: (\d+)\njudge score with delay: (\d+)', txt)
    if not groups:
        broken_file(path)

    ret = [int(i) for i in groups.groups()]

    exit_code = re.search(r'Exit Code=(\d+)', txt)
    if not exit_code:
        broken_file(path)

    if exit_code.groups()[0] == '0':
        raw_score = re.search(r'Score from (\d+): (\d+)', txt)
        if not raw_score:
            broken_file(path)

        raw_score = raw_score.groups()
        raw_score = float(raw_score[1]) / float(raw_score[0])
        ret.append(int(raw_score * 100))
        return ret

    else:
        ret.append(0)
        return ret

def write_to_scv(data, questions, path):
    txt = 'Student number,'
    for i in questions:
        txt += f'{i}, , , ,'
    txt += '\n ,' + 'penalty, final score, score with delay, raw score,' *\
        len(questions) + '\n'
    for i in data:
        txt += i + ', '
        for q in questions:
            if q in data[i]:
                txt += ', '.join([str(e) for e in data[i][q]]) + ', '
            else:
                txt += ', '.join(['0'] * 4) + ', '
        txt += '\n'

    with open(path, 'w') as file:
        file.write(txt)
        file.close()

if __name__ == "__main__":
    data = {}
    reg = re.compile(r'\D*(\d+)\D*')
    with open('./stdno.csv') as file:
        txt = file.read().split('\n')
        for i in txt:
            gp = reg.match(i)
            if gp:
                data[gp.groups()[0]] = {}

    questions = os.listdir('./results')
    for q in questions:
        stdid_list = os.listdir('./results/' + q)
        for stdid in stdid_list:
            ret = read_result(f'./results/{q}/{stdid}/result.txt')
            if stdid in data:
                data[stdid][q] = ret
            else:
                print(f'Student with id ({stdid}) doesn\'t exist in database.')


    write_to_scv(data, questions, 'table.csv')
