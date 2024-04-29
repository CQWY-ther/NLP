import jieba
from LAC import LAC
import wordcloud
from PIL import Image, ImageTk

from pyhanlp import *
import tkinter
import tkinter.filedialog
from tkinter.messagebox import showinfo
from utility import load_dictionary

import pku

NERTrainer = JClass('com.hankcs.hanlp.model.perceptron.NERTrainer')
PerceptronNERecognizer = JClass('com.hankcs.hanlp.model.perceptron.PerceptronNERecognizer')
PerceptronPOSTagger = JClass('com.hankcs.hanlp.model.perceptron.PerceptronPOSTagger')
PerceptronSegmenter = JClass('com.hankcs.hanlp.model.perceptron.PerceptronSegmenter')
AbstractLexicalAnalyzer = JClass('com.hankcs.hanlp.tokenizer.lexical.AbstractLexicalAnalyzer')

root = tkinter.Tk()
root.geometry("1400x1200")
root.configure(bg="wheat")
root.resizable(width=True, height=True)
root.title("分词")


# 加载停用词词典
def load_file(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        contents = f.readlines()
    stopwords = []
    for content in contents:
        stopwords.append(content.strip())  # 去除字符串两边的空格'\n','\r','\t',' '
    return stopwords


# 去停用词
def remove_stop_words(text, dic):
    result = []
    for k in text:
        if k not in dic:
            result.append(k)
    return result


def func1():
    global text
    vat_int = tkinter.messagebox.askokcancel('提示', '要打开文件吗？')
    if vat_int:
        fname = tkinter.filedialog.askopenfilename()
        try:
            with open(fname, 'r', encoding='utf-8') as all_word:
                content = all_word.read()  # 读取文件内容
                text1.insert("1.0", content)
                text = text1.get("1.0", "end-1c")
        finally:
            all_word.close()


stopwords_str = load_file('cn-stopwords.txt')

text1 = tkinter.Text(root, width=130, height=4)  # 字符数、行数
text1.grid(row=0, column=2, padx=4, pady=4)
btn0 = tkinter.Button(root, text="选择文件进行分词", width=20, font=("宋体", 20), bg="lightseagreen",
                      relief=tkinter.FLAT, command=func1)
btn0.grid(row=0, column=0, sticky="w", padx=4, pady=4)


def biaozhun_segment():
    result = tkinter.messagebox.askyesno("提示", "要执行保存文件操作吗？")
    participle = HanLP.segment(text)  # 标准匹配
    if result:
        f1 = open("no_stopwords_biaozhun.txt", "w")
        for i in range(0, len(participle)):
            if str(participle[i]).split("/")[0] not in stopwords_str:
                fenci = str(participle[i]).split("/")[0]
                text2.insert("insert", fenci + ' ')
                f1.writelines(fenci + " ")
        f1.close()
    else:
        for i in range(0, len(participle)):
            if str(participle[i]).split("/")[0] not in stopwords_str:
                fenci = str(participle[i]).split("/")[0]
                text2.insert("insert", fenci + ' ')


text2 = tkinter.Text(root, width=130, height=4)  # 字符数、行数
text2.grid(row=1, column=2, padx=4, pady=4)
btn1 = tkinter.Button(root, text="hanlp标准分词", width=20, font=("宋体", 20), bg="lightseagreen", relief=tkinter.FLAT,
                      command=biaozhun_segment)
btn1.grid(row=1, column=0, sticky="w", padx=4, pady=4)


# 正向最长匹配
def forward_segment(text, dic):
    word_list = []
    i = 0
    while i < len(text):
        longest_word = text[i]  # 当前扫描位置的单字
        for j in range(i + 1, len(text) + 1):  # 所有可能的结尾
            word = text[i: j]  # 从当前位置到结尾的连续字符串
            if word in dic:  # 在词典中
                if len(word) > len(longest_word):  # 并且更长
                    longest_word = word  # 则更优先输出
        word_list.append(longest_word)  # 输出最长值
        i += len(longest_word)  # 正向扫描
    return word_list


def forward_fenci():
    result = tkinter.messagebox.askyesno("提示", "要执行保存文件操作吗？")
    dic = load_dictionary()
    participle = forward_segment(text, dic)  # 正向最长匹配
    participle = remove_stop_words(participle, stopwords_str)
    if result:
        f1 = open("no_stopwords_zhengxiang.txt", "w")
        for i in range(0, len(participle)):
            fenci = str(participle[i])
            text3.insert("insert", fenci + ' ')
            f1.writelines(fenci + " ")
        f1.close()
    else:
        for i in range(0, len(participle)):
            fenci = str(participle[i])
            text3.insert("insert", fenci + ' ')


text3 = tkinter.Text(root, width=130, height=4)  # 字符数、行数
text3.grid(row=2, column=2, padx=4, pady=4)
btn2 = tkinter.Button(root, text="正向分词", width=20, font=("宋体", 20), bg="lightseagreen", relief=tkinter.FLAT,
                      command=forward_fenci)
btn2.grid(row=2, column=0, sticky="w", padx=4, pady=4)


def jieba_fenci():
    message = tkinter.messagebox.askyesno("提示", "要执行保存文件操作吗？")
    participle = jieba.lcut(text)
    result = remove_stop_words(participle, stopwords_str)
    if message:
        f1 = open("jieba_fenci.txt", "w")
        for i in range(0, len(result)):
            fenci = str(result[i])
            text4.insert("insert", fenci + ' ')
            f1.writelines(fenci + " ")
        f1.close()
    else:
        for i in range(0, len(result)):
            fenci = str(result[i])
            text4.insert("insert", fenci + ' ')


text4 = tkinter.Text(root, width=130, height=4)  # 字符数、行数
text4.grid(row=3, column=2, padx=4, pady=4)
btn3 = tkinter.Button(root, text="jieba分词", width=20, font=("宋体", 20), bg="lightseagreen", relief=tkinter.FLAT,
                      command=jieba_fenci)
btn3.grid(row=3, column=0, sticky="w", padx=4, pady=4)


def lac_fenci():
    message = tkinter.messagebox.askyesno("提示", "要执行保存文件操作吗？")
    lac = LAC(mode='lac')
    participle = lac.run(text)[0]
    result = remove_stop_words(participle, stopwords_str)
    if message:
        f1 = open("lac_fenci.txt", "w")
        for i in range(0, len(result)):
            fenci = str(result[i])
            text5.insert("insert", fenci + " ")
            f1.writelines(fenci + " ")
        f1.close()
    else:
        for i in range(0, len(result)):
            fenci = str(result[i])
            text5.insert("insert", fenci + " ")


text5 = tkinter.Text(root, width=130, height=4)  # 字符数、行数
text5.grid(row=4, column=2, padx=4, pady=4)
btn4 = tkinter.Button(root, text="lac分词", width=20, font=("宋体", 20), bg="lightseagreen", relief=tkinter.FLAT,
                      command=lac_fenci)
btn4.grid(row=4, column=0, sticky="w", padx=4, pady=4)


def train(corpus, model):
    trainer = NERTrainer()
    return PerceptronNERecognizer(trainer.train(corpus, model).getModel())


def perceptron():
    # 人名nr, 地名ns, 机构名nt(复合词), 专有名词nz
    message = tkinter.messagebox.askyesno("提示", "要执行保存文件操作吗？")
    recognizer = train(pku.PKU199801_TRAIN, pku.NER_MODEL)
    analyzer = AbstractLexicalAnalyzer(PerceptronSegmenter(), PerceptronPOSTagger(), recognizer)
    participle = list(analyzer.analyze(text))
    if message:
        f1 = open("Perceptron.txt", "w")
        for i in range(0, len(participle)):
            if str(participle[i]).split("/")[0] not in stopwords_str:
                text6.insert("insert", str(participle[i]) + ' ')
                f1.writelines(str(participle[i]) + " ")
        f1.close()
    else:
        for i in range(0, len(participle)):
            if str(participle[i]).split("/")[0] not in stopwords_str:
                text6.insert("insert", str(participle[i]) + ' ')


text6 = tkinter.Text(root, width=130, height=4)  # 字符数、行数
text6.grid(row=5, column=2, padx=4, pady=4)
btn5 = tkinter.Button(root, text="perceptron模型分词", width=20, font=("宋体", 20), bg="lightseagreen",
                      relief=tkinter.FLAT, command=perceptron)
btn5.grid(row=5, column=0, sticky="w", padx=4, pady=4)


def Keywords():
    geshu = text9.get("1.0", tkinter.END)
    a = eval(geshu)
    keyword_list = HanLP.extractKeyword(text, a)
    for i in range(0, a):
        text8.insert("1.0", keyword_list[i] + "\n")


text9 = tkinter.Text(root, width=10, height=4)  # 输入关键字个数
text9.grid(row=6, column=1, sticky="w", padx=4, pady=4)
text9.insert("1.0", "5")
text8 = tkinter.Text(root, width=130, height=4)  # 显示关键字
text8.grid(row=6, column=2, padx=4, pady=4)
btn6 = tkinter.Button(root, text="提取关键词", width=20, font=("宋体", 20), bg="lightseagreen", relief=tkinter.FLAT,
                      command=Keywords)
btn6.grid(row=6, column=0, sticky="w", padx=4, pady=4)


def Phrase():
    geshu = text10.get("1.0", tkinter.END)
    a = eval(geshu)
    phrase_list = HanLP.extractPhrase(text, a)
    for i in range(0, a):
        text11.insert("1.0", phrase_list[i] + "\n")


text10 = tkinter.Text(root, width=10, height=4)  # 输入短语个数
text10.grid(row=7, column=1, sticky="w", padx=4, pady=4)
text10.insert("1.0", "5")
text11 = tkinter.Text(root, width=130, height=4)  # 显示短语
text11.grid(row=7, column=2, padx=4, pady=4)
btn7 = tkinter.Button(root, text="提取短语", width=20, font=("宋体", 20), bg="lightseagreen", relief=tkinter.FLAT,
                      command=Phrase)
btn7.grid(row=7, column=0, sticky="w", padx=4, pady=4)


def Summary():
    geshu = text12.get("1.0", tkinter.END)
    a = eval(geshu)
    summary_list = HanLP.extractSummary(text, a)
    for i in range(0, a):
        text13.insert("1.0", summary_list[i] + "\n")


text12 = tkinter.Text(root, width=10, height=4)  # 输入摘要个数
text12.grid(row=8, column=1, sticky="w", padx=4, pady=4)
text12.insert("1.0", "5")
text13 = tkinter.Text(root, width=130, height=4)  # 显示摘要
text13.grid(row=8, column=2, padx=4, pady=4)
btn8 = tkinter.Button(root, text="提取摘要", width=20, font=("宋体", 20), bg="lightseagreen", relief=tkinter.FLAT,
                      command=Summary)
btn8.grid(row=8, column=0, sticky="w", padx=4, pady=4)


def show_wordcloud():
    participle = jieba.lcut(text)
    txt = " ".join(participle)
    w = wordcloud.WordCloud(font_path='msyh.ttc').generate(txt)
    w.to_file("groundcloud.png")
    rst = Image.open("groundcloud.png")
    rst = rst.resize((200, 100))
    a = ImageTk.PhotoImage(rst)
    label1.config(image=a)
    label1.image = a


label1 = tkinter.Label(root, text="词云图")
label1.grid(row=10, column=1)
btn9 = tkinter.Button(root, text="词云展示", width=20, font=("宋体", 20), bg="lightseagreen", relief=tkinter.FLAT,
                      command=show_wordcloud)
btn9.grid(row=10, column=0, sticky="w", padx=4, pady=4)


def cipin():
    Top = int(text14.get("1.0", "end-1c"))
    participle = jieba.lcut(text)
    counts = {}
    for word in participle:
        if len(word) == 1:
            continue
        else:
            counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    for i in range(Top):
        word, count = items[i]
        text15.insert("end", "Top{0:<3}{1:<5}{2:>5}".format(i + 1, word, count))
        text15.insert("end", "\n")


text14 = tkinter.Text(root, width=10, height=4)  # 输入输出词语个数
text14.grid(row=9, column=1, sticky="w", padx=4, pady=4)
text14.insert("1.0", "10")
text15 = tkinter.Text(root, width=130, height=4)  # 显示
text15.grid(row=9, column=2, padx=4, pady=4)
btn10 = tkinter.Button(root, text="词频统计", width=20, font=("宋体", 20), bg="lightseagreen", relief=tkinter.FLAT,
                       command=cipin)
btn10.grid(row=9, column=0, sticky="w", padx=4, pady=4)


def clear():
    for i in range(2, 16):
        sign = eval("text" + str(i))
        sign.delete("1.0", "end")


btn = tkinter.Button(root, text="清空", width=20, font=("宋体", 20), bg="lightseagreen", relief=tkinter.FLAT,
                     command=clear)
btn.grid(row=11, column=0, sticky="w", padx=4, pady=4)

root.mainloop()
