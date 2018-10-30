
"""
    Transform .srt files into .txt files
"""

__author__ = "Gwena Cunha"


def srt_to_text(root_dir):

    srt_file = open(root_dir+'subtitle.srt', 'r')
    txt_file = open(root_dir+'text.txt', 'w')

    srt_sentences = srt_file.read().splitlines()
    count = 0
    sentence = ''
    for i in range(0, len(srt_sentences)):
        line = srt_sentences[i]
        if count != 2:
            count += 1
        else:
            if line.strip() != '':
                sentence += line + ' '
            else:
                txt_file.write(sentence+'\n')
                sentence = ''
                count = 0


if __name__ == '__main__':
    videos = {'BMI', 'CHI', 'CRA', 'DEP', 'FNE', 'GLA', 'LOR'}
    for v in videos:
        srt_to_text('srt_data/{}_text/'.format(v))
