# informatii despre un nod din arborele de parcurgere (nu din graful initial)
def get_keys_from_value(d, val):
    return [k for k, v in d.items() if v == val]
viz=[0]*21
mb=[]
tc=0
class NodParcurgere:
    graf = None  # static

    def __init__(self, id, info, parinte, cost, h):
        self.id = id  # este indicele din vectorul de noduri
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # costul de la radacina la nodul curent
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self.info];
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte.info)
            nod = nod.parinte
        return l

    def afisDrum(self,tc):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        print(("->").join(l))
        cv=0
        for i in range(len(l)):
            if i<len(l)-1:
                print("->", end="")
                if tc == startmin or (tc - startmin) % vStartMin[mb[dictstops[l[i]]][dictstops[l[i + 1]]] - 1] == 0:
                    print("0", end=" min ")
                else:
                    print((tc-vStartMin[mb[dictstops[l[i]]][dictstops[l[i + 1]]] - 1])%vStartMin[mb[dictstops[l[i]]][dictstops[l[i + 1]]] - 1]+1, end=" min ")

                if cv==-1:
                    print(vbus[mb[dictstops[l[i]]][dictstops[l[i+1]]]-1],end=" t=")
                    print(vEndMin[mb[dictstops[l[i]]][dictstops[l[i + 1]]] - 1], end="min")
                    tc+=vEndMin[mb[dictstops[l[i]]][dictstops[l[i + 1]]] - 1]
                else:
                    print(vbus[mb[dictstops[l[i]]][dictstops[l[i + 1]]] - 1], end=" t=")
                    if cv!=vbus[mb[dictstops[l[i]]][dictstops[l[i + 1]]] - 1]:
                        print(vEndMin[mb[dictstops[l[i]]][dictstops[l[i + 1]]] - 1], end="min")
                    else:
                        print(vEndMin[mb[dictstops[l[i]]][dictstops[l[i + 1]]] - 1], end="min")
                    tc += vEndMin[mb[dictstops[l[i]]][dictstops[l[i + 1]]] - 1]
                cv = vbus[mb[dictstops[l[i]]][dictstops[l[i + 1]]] - 1]
            else:
                print()



        #print(l)
        print("Cost: ", self.g)
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += self.info + "("
        sir += "id = {}, ".format(self.id)
        sir += "drum="
        drum = self.obtineDrum()
        sir += ("->").join(drum)
        sir += " g:{}".format(self.g)
        sir += " h:{}".format(self.h)

        sir += " f:{})".format(self.f)
        return (sir)


class Graph:  # graful problemei
    def __init__(self, noduri, matriceAdiacenta, matricePonderi, start, scopuri, lista_h):
        self.noduri = noduri
        self.matriceAdiacenta = matriceAdiacenta
        self.matricePonderi = matricePonderi
        self.nrNoduri = len(matriceAdiacenta)
        self.start = start
        self.scopuri = scopuri
        self.lista_h = lista_h

    def indiceNod(self, n):
        return self.noduri.index(n)

    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []
        for i in range(self.nrNoduri):
            if self.matriceAdiacenta[nodCurent.id][i] == 1 and not nodCurent.contineInDrum(self.noduri[i]):
                nodNou = NodParcurgere(i, self.noduri[i], nodCurent, nodCurent.g + self.matricePonderi[nodCurent.id][i],
                                       self.calculeaza_h(self.noduri[i]))
                listaSuccesori.append(nodNou)
        return listaSuccesori

    def calculeaza_h(self, infoNod):
        return self.lista_h[self.indiceNod(infoNod)]

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


##############################################################################################
#                                 Initializare problema                                      #
##############################################################################################

# pozitia i din vectorul de noduri da si numarul liniei/coloanei corespunzatoare din matricea de adiacenta
start = ""
end = ""
#obtinem data necesara
linie=0
vbus=[]
vprice=[]
vEndMin=[]
vStartMin=[]
dictstops={}
countStops=0
ok=0
nrPers=0
vNume=[]
vBuget=[]
i=0
routes=[]
busRoutes=[]
nrbus=0
with open("data/input1") as f:
    line = f.readline()
    while line.split()[1] != "oameni":
        #print(line)
        if linie == 0:
            end = line.split()[1]
            start = line.split()[0]
            startmin = int(start.split(":")[0]) * 60 + int(start.split(":")[1])
            endmin = int(end.split(":")[0]) * 60 + int(end.split(":")[1])
            linie = 1
        elif line.split()[1] != "oameni" and ok == 0 :
            a=line.split(",")
            vbus.append(a[0])
            busRoutes.append([])
            vprice.append(float(a[1].split("l")[0]))
            vStartMin.append(int(a[2].split("m")[0]))
            vEndMin.append(int(a[3].split("m")[0]))
            for i in a[4:]:
                if i.replace("\"","").replace("\n","") in dictstops.keys():
                    busRoutes[nrbus].append(dictstops[i.replace("\"", "").replace("\n", "")])
                    #continue
                else:
                    dictstops[i.replace("\"","").replace("\n","")] = countStops
                    countStops = countStops+1
                    busRoutes[nrbus].append(dictstops[i.replace("\"", "").replace("\n", "")])

            nrbus=nrbus+1
        else: ok=1

        line = f.readline()
    linie=0
    nrPers = int(line.split()[0])
    for j in range(nrPers):
        routes.append([])
    line = f.readline()
    while line:
        # print(line)
        a = line.split(",")
        vNume.append(a[0])
        vBuget.append(float(a[1].split("l")[0]))
        for i in a[2:]:
            routes[linie].append(i.replace("\"","").replace("\n",""))
        linie+=1
        line = f.readline()
print(dictstops)
print(vbus)
print(vprice)
print(vStartMin)
print(vEndMin)
print(vNume)
print(vBuget)
print(routes)
print(busRoutes)
#aici avem matricea de adiacenta
m=[]
for i in range(countStops):
    m.append([0]*countStops)
for i in range(len(busRoutes)):
    for j in range(len(busRoutes[i])):
        if j==0:
            m[busRoutes[i][j]][busRoutes[i][j+1]]=1
            m[busRoutes[i][j + 1]][busRoutes[i][j]] = 1
        elif j<len(busRoutes[i])-1:
            m[busRoutes[i][j]][busRoutes[i][j+1]]=1
            m[busRoutes[i][j + 1]][busRoutes[i][j]] = 1
        elif j<len(busRoutes[i])-2:
            m[busRoutes[i][j]][busRoutes[i][j + 1]] = 1
            m[busRoutes[i][j + 1]][busRoutes[i][j]] = 1
            m[busRoutes[i][j]][busRoutes[i][j - 1]] = 1
            m[busRoutes[i][j - 1]][busRoutes[i][j]] = 1
#aici facem matricea ponderilor
mp=[]
for i in range(countStops):
    mp.append([0]*countStops)
print("=======================================")
for i in range(len(busRoutes)):
    for j in range(len(busRoutes[i])):
        if j==0:
            mp[busRoutes[i][j]][busRoutes[i][j+1]]= vprice[i]
            mp[busRoutes[i][j + 1]][busRoutes[i][j]] = vprice[i]
        elif j<len(busRoutes[i])-1:
            mp[busRoutes[i][j]][busRoutes[i][j+1]]=vprice[i]
            mp[busRoutes[i][j + 1]][busRoutes[i][j]] = vprice[i]
        elif j<len(busRoutes[i])-2:
            mp[busRoutes[i][j]][busRoutes[i][j + 1]] = vprice[i]
            mp[busRoutes[i][j + 1]][busRoutes[i][j]] = vprice[i]
            mp[busRoutes[i][j]][busRoutes[i][j - 1]] = vprice[i]
            mp[busRoutes[i][j - 1]][busRoutes[i][j]] = vprice[i]
for i in range(len(dictstops)):
    mb.append([0]*len(dictstops))
    for j in range(len(dictstops)):
        if mp[i][j]>0:
            mb[i][j]=vprice.index(mp[i][j])+1
        else:
            mb[i][j]=0

noduri=[]
for i in dictstops.keys():
    noduri.append(i)
print(noduri)
print(len(dictstops))
tc=startmin
def rez(linie):
    start = routes[linie][0]
    scopuri = routes[linie][1:]
    viz[dictstops[scopuri[0]]]=1
    # exemplu de euristica banala (1 daca nu e nod scop si 0 daca este)
    vect_h = [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1]
    viz[dictstops[start]]==1
    gr = Graph(noduri, m, mp, start, scopuri, vect_h)
    NodParcurgere.graf = gr;


    def a_star(gr, nrSolutiiCautate):
        # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
        c = [NodParcurgere(gr.indiceNod(gr.start), gr.start, None, 0, gr.calculeaza_h(gr.start))]
        tc = startmin
        while len(c) > 0:
            #print("Coada actuala: " + str(c))
            #input()
            nodCurent = c.pop(0)

            if gr.testeaza_scop(nodCurent) and scopuri.index(nodCurent.info) == 0:
                viz[dictstops[nodCurent.info]] = 1
                print("Solutie: ")
                nodCurent.afisDrum(tc)
                print("\n----------------\n")
                gr.start=nodCurent.info
                c = [NodParcurgere(gr.indiceNod(gr.start), gr.start, None, 0, gr.calculeaza_h(gr.start))]
                scopuri.pop(0)
                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    return
            lSuccesori = gr.genereazaSuccesori(nodCurent)
            for s in lSuccesori:
                i = 0
                gasit_loc = False
                for i in range(len(c)):
                    # diferenta fata de UCS e ca ordonez dupa f
                    if c[i].f >= s.f:
                        gasit_loc = True
                        break;
                if gasit_loc:
                    c.insert(i, s)
                else:
                    c.append(s)
    a_star(gr, nrSolutiiCautate=len(scopuri))
    #ceva update

for i in range(len(routes)):
    print(vNume[i]+" ================================")
    rez(i)
