import art



def header_text():

    text_GPA = art.text2art("GPA", font='lean', chr_ignore=True, space=1)
    text_full = '***** Your Genius Personal Assistant ******'.upper()

    print(text_GPA, f'{text_full:^55}')


header_text()




