from bnetbase import *

#example
VisitAsia = Variable('Visit_To_Asia', ['visit', 'no-visit'])
F1 = Factor("F1", [VisitAsia])
F1.add_values([['visit', 0.01], ['no-visit', 0.99]])


A = Variable('A', [True, False])
B = Variable('B', [True, False])
C = Variable('C', [True, False])
D = Variable('D', [True, False])
E = Variable('E', [True, False])
F = Variable('F', [True, False])
G = Variable('G', [True, False])
H = Variable('H', [True, False])
I = Variable('I', [True, False])


PA = Factor("P(A)", [A])
PA.add_values([[True, 0.9],[False,0.1]])

PH = Factor("P(H)", [H])
PH.add_values([[True, 0.5],[False,0.5]])

PG = Factor("P(G)", [G])
PG.add_values([[True, 1.0],[False,0.0]])

PF = Factor("P(F)", [F])
PF.add_values([[True, 0.1],[False,0.9]])

PBAH = Factor("P(B|A,H)", [B,A,H])
PBAH.add_values([[True,True,True, 1.0],[True,True,False,0.0],[True,False,True,0.5],[True,False,False, 0.6],[False,True,True, 0.0],[False,True,False,1.0],[False,False,True,0.5],[False,False,False,0.4]])

PIB = Factor("P(I|B)", [I,B])
PIB.add_values([[True,True, 0.3],[True,False,0.9],[False,True,0.7],[False,False,0.1]])

PCBG = Factor("P(C|B,G)", [C,B,G])
PCBG.add_values([[True,True,True, 0.9],[True,True,False,0.9],[True,False,True,0.1],[True,False,False,1.0],[False,True,True,0.1],[False,True,False,0.1],[False,False,True,0.9],[False,False,False,0.0]])

PEC = Factor("P(E|C)", [E,C])
PEC.add_values([[True,True, 0.2],[True,False,0.4],[False, True,0.8],[False, False,0.6]])

PDCF = Factor("P(D|C,F)", [D,C,F])
PDCF.add_values([[True,True,True, 0.0],[True,True,False,1.0],[True,False,True,0.7],[True,False,False,0.2],[False,True,True,1.0],[False,True,False,0.0],[False,False,True, 0.3],[False,False,False,0.8]])

Q3 = BN('SampleQ4', [A,B,C,D,E,F,G,H,I], [PA,PH,PG,PF,PBAH,PIB,PCBG,PEC,PDCF])

print("P(b|a) ....", end = '')
A.set_evidence(True)
probs = VE(Q3, B, [A])
print('P(b|a) = {} P(-b|a) = {}'.format(probs[0],probs[1]))

print("P(c|a) ....", end = '')
A.set_evidence(True)
probs = VE(Q3, C, [A])
print('P(c|a) = {} P(-c|a) = {}'.format(probs[0],probs[1]))

print("P(c|a~e) ....", end = '')
A.set_evidence(True)
E.set_evidence(False)
probs = VE(Q3, C, [A,E])
print('P(c|a,-e) = {} P(-c|a,-e) = {}'.format(probs[0],probs[1]))

print("P(c|a~f) ....", end = '')
A.set_evidence(True)
F.set_evidence(False)
probs = VE(Q3, C, [A,F])
print('P(c|a,-f) = {} P(-c|a,-f) = {}'.format(probs[0],probs[1]))
