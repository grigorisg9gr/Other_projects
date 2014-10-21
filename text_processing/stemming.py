#!/usr/bin/python
# -*- coding: cp1253 -*-
##�������� ������� ������������ - ��������� ������� ������������
##�������� �������: HOU-CS-UGP-2013-18
##"���������� ���������� �������� ��������������� ��� ��������������� �������� ���� �������� ������"
##���������� ���������
##��������� ���������: ������ �����������, ����� ��������� �/� & ������������, ������������ ������

##Implementation in Python of the greek stemmer presented by Giorgios Ntais during his master thesis with title
##"Development of a Stemmer for the Greek Language" in the Department of Computer and Systems Sciences
##at Stockholm's University / Royal Institute of Technology.

##The system takes as input a word and removes its inflexional suffix according to a rule based algorithm.
##The algorithm follows the known Porter algorithm for the English language and it is developed according to the
##grammatical rules of the Modern Greek language.

# greg, july 2014: Function stem is used to stem a word (in greek). With the function stemming_doc you can also stem a text.
# Assumptions:
# 1) all letters are capital,
# 2) they include no accent and no punctuation points.

__author__ = 'greg'

VOWELS = ['�', '�', '�', '�', '�', '�', '�', '�', '�', '�', '�', '�', '�', '�', '�', '�']

import unicodedata as ud


def ends_with(word, suffix):
    suf2 = get_decoded_input(suffix)
    return ud.normalize('NFC', word[len(word) - len(suffix):]) == ud.normalize('NFC', suf2)

def stem(word):
    done = len(word) <= 3

    ##rule-set  1
    ##���������->����, ������->����
    if not done:
        for suffix in ['�����', '����', '����']:
            #print len(word)
            #print len(suffix)
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                remaining_part_does_not_end_on = True
                for s in ['��', '���', '���', '�����', '�����', '����', '�����', '���', '���', '�����']:
                    if ends_with(word, s):
                        remaining_part_does_not_end_on = False
                        break
                if remaining_part_does_not_end_on:
                    word = word + get_decoded_input('��')
                done = True
                break

    ##rule-set  2
    ##�������->���, �������->�����
    if not done:
        for suffix in ['����', '����']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                for s in ['��', '��', '���', '��', '���', '���', '�����', '���']:
                    if ends_with(word, s):
                        word = word + get_decoded_input('��')
                        break
                done = True
                break

    ##rule-set  3
    ##���������->����, ��������->������
    if not done:
        for suffix in ['�����', '�����']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                for s in ['���', '������', '�����', '���', '����', '��', '�', '��', '��', '���', '����', '��', '��', '����', '��']:
                    if ends_with(word, s):
                        word = word + get_decoded_input('���')
                        break
                done = True
                break

    ##rule-set  4
    ##���������->������, ����->��
    if not done:
        for suffix in ['���', '���']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                for s in ['�', '�', '��', '���', '�', '�', '��', '���']:
                    if ends_with(word, s):
                        word = word + get_decoded_input('�')
                        break
                done = True
                break

    ##rule-set  5
    ##������->����, �������->�����
    if not done:
        for suffix in ['��', '���', '���']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                for s in VOWELS:
                    if ends_with(word, s):
                        word = word + get_decoded_input('�')
                        break
                done = True
                break

    ##rule-set  6
    ##���������->������, ��������->������
    if not done:
        for suffix in ['���', '����', '����', '����', '���', '���']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['��', '��', '���', '����', '�������', '��', '����', '�����', '���', '����', '���', '����', '����',
                            '������', '�����', '����', '����', '�������', '����', '����', '���', '���', '�������', '����', '����',
                            '������', '������', '����', '�������', '������', '����', '�����', '����', '����', '�����', '�����',
                            '���']:
                    word = word + get_decoded_input('��')
                else:
                    for s in VOWELS:
                        if ends_with(word, s):
                            word = word + get_decoded_input('��')
                            break
                done = True
                break

    ##rule-set  7
    ##���������->����, �������->������
    if not done:
        if word == '�����': word = 2*word
        for suffix in ['�������', '�����', '�����', '������', '�����']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['�']:
                    word = word + get_decoded_input('����')
                done = True
                break
        if not done and ends_with(word, '���'):
            word = word[:len(word) - len('���')]
            if word in ['����', '����', '����', '�����', '����', '���', '���', '���', '����', '���', '���', '�']:
                word = word + get_decoded_input('��')
            done = True

    ##rule-set  8
    ##���������->����, �������->������
    if not done:
        for suffix in ['��������', '�������', '�������', '�������', '������', '������', '������', '�����', '�����',
                       '�����', '�����']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['��', '��', '�']:
                    word = word + get_decoded_input('����')
                done = True
                break
        if not done and ends_with(word, '���'):
            word = word[:len(word) - len('���')]
            if word in ['�����', '�����', '�����', '�', '�������', '�', '�������', '������', '������', '�����', '������', '�',
                        '��������', '�', '���', '�', '�����', '��', '�����', '������', '��������', '�����', '�������', '���',
                        '�����', '����', '��������', '�', '������', '��', '���', '���', '���', '���', '����', '��������', '���',
                        '���', '������', '�', '����', '��', '����', '���', '���', '������', '�����', '���', '���', '��', '����',
                        '����', '����', '�', '��', '����', '�����', '����', '����', '�����', '����', '����', '������', '���',
                        '����', '�������', '������', '������', '����', '����', '�����', '���', '�����������', '�������', '����',
                        '�������', '���', '�����������', '�����������', '����', '��������', '��������', '������', '�������',
                        '�����', '������', '����', '�������', '�������', '����', '���', '���', '������', '������', '���������',
                        '�������']:
                word = word + get_decoded_input('��')
            else:
                for s in VOWELS:
                    if ends_with(word, s):
                        word = word + get_decoded_input('��')
                        break
            done = True

    ##rule-set  9
    ##���������->����, ������->�����
    if not done:
        if ends_with(word, '�����'):
            word = word[:len(word) - len('�����')]
            done = True
        elif ends_with(word, '���'):
            word = word[:len(word) - len('���')]
            if word in ['����', '���', '����', '���', '��', '��', '��', '���', '�����', '���', '��', '���', '����', '���', '���',
                        '�������', '����', '����', '����', '���', '�', '�', '��', '����', '�']:
                word = word + get_decoded_input('��')
            else:
                for s in ['��', '���', '���', '���', '����', '��', '���', '���', '���', '�����', '���', '���', '���', '��', '���',
                          '���', '����', '���', '����', '���', '���', '��', '���', '���', '���', '���', '���', '���', '���', '���',
                          '����'] + VOWELS:
                    if ends_with(word, s):
                        word = word + get_decoded_input('��')
                        break
            done = True

    ##rule-set 10
    ##���������->����, ����������->�������
    if not done:
        for suffix in ['�����', '�����']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['���']:
                    word = word + get_decoded_input('���')
                elif word in ['�����', '���']:
                    word = word + get_decoded_input('���')
                done = True
                break

    ##rule-set 11
    ##�����������->����, ��������->�������
    if not done:
        for suffix in ['�������', '������']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['��']:
                    word = word + get_decoded_input('�����')
                done = True
                break

    ##rule-set 12
    ##���������->����, ������->�����
    if not done:
        for suffix in ['�����']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['�', '��', '����', '�����', '�����', '������']:
                    word = word + get_decoded_input('����')
                done = True
                break
    if not done:
        for suffix in ['����']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['��', '��', '�����', '�', '�', '�', '�������', '��', '���', '���']:
                    word = word + get_decoded_input('���')
                done = True
                break

    ##rule-set 13
    ##��������->�����, ��������->������
    if not done:
        for suffix in ['�����', '������', '�����']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                done = True
                break
    if not done:
        for suffix in ['���', '����', '���']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['����', '�', '���������', '�����', '����']:
                    word = word + get_decoded_input('��')
                else:
                    for suffix in ['����', '�����', '����', '��', '��', '���']:
                        if ends_with(word, suffix):
                            word = word + get_decoded_input('��')
                            break
                done = True
                break

    ##rule-set 14
    ##���������->����, ��������->������
    if not done:
        for suffix in ['����', '�����', '����']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['������', '���', '���', '�����', '����', '�����', '������', '���', '�', '���', '�', '�', '���', '�����',
                            '�������', '��', '���', '����', '������', '��������', '��', '��������', '�������', '���', '���']:
                    word = word + get_decoded_input('���')
                else:
                    for s in ['�����', '����', '������', '����', '������', '����', '�����', '���', '���', '���', '��', '����'] + VOWELS:
                        if ends_with(word, s):
                            word = word + get_decoded_input('���')
                            break
                done = True
                break

    ##rule-set 15
    #��������->����, ��������->�����
    if not done:
        for suffix in ['���', '����', '���']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['�����', '�����', '����', '����', '�', '���', '��', '����', '������', '�����', '����', '�����', '����',
                            '������', '������', '���', '����', '�����', '����', '����', '�����', '��������', '����', '����', '�',
                            '����', '���', '����', '������', '����', '����', '�����', '����', '��', '����', '��������', '�������',
                            '�', '���', '�����', '���', '�', '��', '�']:
                    word = word + get_decoded_input('��')
                else:
                    for s in ['��', '���', '����', '��', '��', '��', '��', '���', '����']:
                        # ����������: '��'
                        if ends_with(word, s):
                            if not word in ['���', '������']:
                                word = word + get_decoded_input('��')
                            break
                done = True
                break

    ##rule-set 16
    ##�������->����, �����->���
    if not done:
        for suffix in ['���', '����', '���']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['�', '������', '�������', '������', '�������', '�����', '������']:
                    word = word + get_decoded_input('��')
                done = True
                break

    ##rule-set 17
    ##��������->����, ������->�����
    if not done:
        for suffix in ['����']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['���', '��', '���', '��', '���', '�����', '�����', '����', '�������', '������']:
                    word = word + get_decoded_input('���')
                done = True
                break

    ##rule-set 18
    ##��������->����, �������->������
    if not done:
        for suffix in ['����', '������', '������']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['�', '�', '���', '�����������', '���������', '����']:
                    word = word + get_decoded_input('OYN')
                done = True
                break

    ##rule-set 19
    ##��������->����, �����->����
    if not done:
        for suffix in ['����', '������', '������']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                if word in ['��������', '�', '�', '������', '��', '��������', '�����']:
                    word = word + get_decoded_input('���')
                done = True
                break

    ##rule-set 20
    ##������->���, ������->�����
    if not done:
        for suffix in ['����', '�����', '�����']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                word = word + get_decoded_input('�')
                done = True
                break

    ##rule-set 21
    if not done:
        for suffix in ['���������', '��������', '��������', '��������', '��������', '�������', '�������', '�������', '�������',
                       '�������', '�������', '�������', '�������', '�������', '�������', '�������', '������', '������', '������',
                       '������', '������', '������', '������', '������', '������', '������', '������',  '�����', '�����', '�����',
                       '�����', '�����', '�����', '�����', '�����', '�����', '�����', '�����', '�����', '�����',  '�����',
                       '�����', '�����', '�����', '�����',  '����', '����', '����', '����', '����', '����', '����', '����',
                       '����', '����', '����', '����', '����', '����', '����', '����',  '���',  '���',  '���',  '���', '���',
                       '���',  '��', '��', '��', '��', '��', '��', '��', '��', '��', '��', '��', '��', '��', '�', '�', '�', '�',
                       '�',  '�', '�']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                break

    ##rule-set 22
    ##������������->�����, ����������->�����, ���������->����
    if not done:
        for suffix in ['�����', '�����', '����', '����', '����', '����', '����', '����']:
            if ends_with(word, suffix):
                word = word[:len(word) - len(suffix)]
                break

    return word


# greg, 11 July 2014. The following code is written by me:
import sys, os.path


def get_conversion_pool():
        poolGR = u"����������������������������������������������������������������ڼ�ۿ"
        poolGL =  "abgdezh8iklmn3oprstufx4wABGDEZH8IKLMN3OPRSTYFX4WsaehiiiouuuwAEHIIOYYW"
        return dict(zip(poolGR, poolGL))


def get_decoded_input(line):
        try:
                line = line.decode("utf-8")
        except UnicodeDecodeError:
                try:
                        line = line.decode("cp1253")
                except UnicodeDecodeError:
                        line = line.decode("iso8859-7")
        return line


def convert(datasource):
        pool = get_conversion_pool()
        for line in datasource:
                line = get_decoded_input(line)
                output_line = []
                for character in line:
                        if pool.has_key(character):
                                output_line.append(pool[character])
                        else:
                                output_line.append(character)
                #sys.stdout.write("".join(output_line))
                #sys.stdout.flush()
        return output_line


def stemming_doc(src, outdir1):
    # This can be used for stemming a whole document. It first opens the doc (input, output) and then reads from input,
    # stems and then writes in output.
    fr = open(src,'r')
    f = open(outdir1, 'w')
    #output_line=convert(fr)
    for word in fr.read().split():
        #print get_decoded_input(word)
        #print type(word)
        ww = get_decoded_input(word)
        ww = ww.upper()
        #print stem(ww.encode('utf-8'))
        res = stem(ww)
        print res
        print >> f, res.encode('utf-8')
    f.close()

#stemming_doc('words.txt', 'out_greg.txt')
if __name__ == '__main__':
	stemming_doc()






