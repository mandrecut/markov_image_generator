from collections import defaultdict, Counter
from PIL import Image
import progressbar
import random

class MarkovImg(object):

    def __init__(self, order=1):
        """
        Input: Markov chain order >= 1.
        Initializes the dictionary of char transitions.
        """
        self.dct = defaultdict(Counter)
        self.order = order

    def learn(self, img, salt):
        """
        Input: some image img, 0<=salt<=1.0 improves learning.
        Returns the dictionary and the state transition probabilities.
        """
        if img.mode != "RGB":
            img = img.convert("RGB")
        x = list(img.getdata())
        if salt > 0:
            for n in range(len(x)):
                y = list(x[n])
                for i in [0,1,2]:
                    if random.random() < salt*0.5:
                        y[i] = y[i]^0x01
                x[n] = tuple(y)
        x.extend(x[0:self.order])
        bar = progressbar.ProgressBar()
        for n in bar(range(len(x)-self.order)):
            k = tuple([a for b in x[n:n+self.order] for a in b])
            self.dct[k][x[n+self.order]] += 1
        for k in self.dct:
            s = float(sum(self.dct[k].values()))
            for v in self.dct[k]:
                self.dct[k][v] = self.dct[k][v]/s

    def nextstate(self, state):
        """
        Input: current Markov state. 
        Returns next Markov state.
        """
        s,r,v = 0,random.random(),(0,0,0)
        for v in self.dct[state]:
            s = s + self.dct[state][v]
            if s >= r: 
                break
        state = list(state)[3:self.order*3]
        state.extend(list(v))
        return tuple(state)

    def generate(self, img_size):
        """
        Input: size (M,N) of image to be generated.
        """
        state = random.choice(list(self.dct.keys()))
        so3,so33,g = self.order*3,self.order*3-3,[]
        for i in range(img_size[0]):
            for j in range(img_size[1]):
                state = self.nextstate(state)
                g.append(state[so33:so3])
        im = Image.new("RGB", (img_size[0],img_size[1]))
        im.putdata(g)
        return im



