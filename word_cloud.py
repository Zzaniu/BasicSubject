import re
import itchat


def Check_the_sex_ratio(itchat):
    """统计男女比例"""
    friends = itchat.get_friends(update=True)[0:]
    male = famle = other = 0
    for i in friends:
        sex = i.get('Sex')
        if 1 == sex:
            male += 1
        elif 2 == sex:
            famle += 1
        else:
            other += 1
    total = len(friends[1:])
    print('男性好友:%.2f%%' % (float(male) / total * 100))
    print('女性好友:%.2f%%' % (float(famle) / total * 100))
    print('   其他:%.2f%%' % (float(other) / total * 100))


def generate_word_cloud(itchat):
    """词云"""
    friends = itchat.get_friends(update=True)[0:]
    tList = []
    for i in friends:
        signature = i["Signature"].replace(" ", "").replace("span", "").replace("class", "").replace("emoji", "")
        rep = re.compile("1f\d.+")
        signature = rep.sub("", signature)
        tList.append(signature)
    text = "".join(tList)
    import jieba
    wordlist_jieba = jieba.cut(text, cut_all=True)
    wl_space_split = " ".join(wordlist_jieba)

    # wordcloud词云
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    import PIL.Image as Image
    import os
    import numpy as np

    alice_coloring = np.array(Image.open('D:/E/Learn/timg.jpg'))
    my_wordcloud = WordCloud(background_color="white", max_words=2000, mask=alice_coloring,
                             max_font_size=40, random_state=42, min_font_size=10,
                             font_path='D:/E/Learn/ARIALUNI.TTF').generate(wl_space_split)

    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()
    my_wordcloud.to_file(os.path.join("D:/E/Learn/tangweila_cloud.png"))
    itchat.send_image("wechat_cloud.png", 'filehelper')


if __name__ == "__main__":
    itchat.login()
    Check_the_sex_ratio(itchat)
    generate_word_cloud(itchat)
