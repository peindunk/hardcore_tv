pcgame = ['英雄联盟','DNF','绝地求生','魔兽世界','DOTA2',\
              '魔兽争霸','守望先锋','炉石传说','梦幻西游','传奇']
videoGame = ['主机游戏','火影忍者']
mobileGame = ['CF手游','热门手游','王者荣耀']
outdoor_food = ['美食','户外','鱼教']
entertainment = ['颜值','二次元','星娱','音乐电台']

class Analysis:
    def __init__(self):
        self.pc_count = 0
        self.v_count = 0
        self.m_count = 0
        self.o_count = 0
        self.e_count = 0
        self.others = 0


    def analysis(self):
        with open('fenlei.txt') as f:
            data = f.read()
            li = data.split('#')
            s = set(li)
            L = []
            print('总共有%d种分类'%len(s))
            for item in s:
                num = li.count(item)
                count = (item,num)
                L.append(count)
            L = sorted(L,key=lambda x:x[1],reverse=True)
            for item in L:
                print('%s出现了:%d次'%item)
            for item in li:
                if item.strip() in pcgame:
                    self.pc_count += 1
                elif item.strip() in videoGame:
                    self.v_count += 1
                elif item.strip() in mobileGame:
                    self.m_count += 1
                elif item.strip() in outdoor_food:
                    self.o_count += 1
                elif item.strip() in entertainment:
                    self.e_count += 1
                else:
                    self.others += 1
            print('PC游戏:%d\t主机游戏:%d\t手机游戏:%d\t户外美食:%d\t娱乐:%d\t其它:%d'
                  %(self.pc_count,self.v_count,self.m_count,self.o_count,self.e_count,self.others))

if __name__ == '__main__':
    a = Analysis()
    a.analysis()

