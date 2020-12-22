import urllib.request, json, datetime
htmlcode = urllib.request.urlopen('https://www.codewars.com/users/leaderboard/kata')
page=str(htmlcode.read())

userlist=[]
ptslist=[]

for i in range(1,501):
    startpoint=page.index('<tr data-username=')
    x=page[startpoint-16:startpoint-10]
    x=x.replace('>','').replace(',','')
    ptslist.append(x)
    page=page[startpoint+19:]
    endpoint=page.index('"><td class="')
    user=page[:endpoint]
    userlist.append(user)

y=page.index('<div class="clearfix">')
x=page[y-48:y-43].replace(',','')
ptslist.append(int(x))
ptslist=ptslist[1:]

lista=[]
for i in range(500):
    by=[i+1,userlist[i],int(ptslist[i])]
    lista.append(by)


# zapis listy do pliku

with open("cdlists\{}.json".format(datetime.date.today()), "w") as fp:
    json.dump(lista, fp)
date=str(datetime.date.today())
with open("cdlists\lists.json", "r") as li:
    li=json.loads(li.read())
if li[-1]!=date:
    li.append(date)
prevdate=li[-2]

with open("cdlists\lists.json", "w") as fp:
    json.dump(li, fp)

# odczyt danych z poprzedniej daty
with open("cdlists\{}.json".format(prevdate), "r") as pd:
    pd=json.loads(pd.read())

# lista do druku
mgld=[]
for i in lista:
    if i[1]=='mgld':
        mgld=i
        break
temp=lista[mgld[0]-10:mgld[0]+2]

pltlist=[]
for i in temp:
    for j in pd:
         if i[1]==j[1]:
             pltlist.append(i+[i[2]-j[2]])

# progi do druku

nxtqt=mgld[0]//10*10
nxtqh=mgld[0]//100*100

for i in lista:
    if i[0]==nxtqt:nxtqt=i
    if i[0]==nxtqh:nxtqh=i

# wyświetlanie

import pygame
pygame.font.init()
background_colour = (255,255,255) # White color
(width, height) = (500, 700) # Screen size
screen = pygame.display.set_mode((width, height)) #Setting Screen
pygame.display.set_caption('Lista Codewars') #Window Name
screen.fill(background_colour)#Fills white to screen

def text(surface, y, x, text):
    font = pygame.font.SysFont('arial', 24)
    text = font.render(text, 0, (0, 0, 0))
    surface.blit(text, (x, y))



for i in range(12):
    us=pltlist[i]
    dis=str(us[0])+' - '+us[1]+':  '+str(us[2])
    text(screen, 40*i+20,20, dis)
    if i!=9:
        dt='  :  '+str(us[2]-mgld[2])
        text(screen, 40*i+20,380, dt) 
    if us[3]!=0:
        text(screen, 40*i+20,440, '+'+str(us[3]))
pygame.draw.rect(screen,(255,0,0),(5,372,200,40),2)

pygame.draw.line(screen,(0,0,0),(10,500),(width-10,500),2)
ods=20
dis=str(nxtqt[0])+' - '+nxtqt[1]+':  '+str(nxtqt[2])
dt='  :  '+str(nxtqt[2]-mgld[2])
opis='Następny próg dziesiętny'
text(screen, 500+ods,20, opis)
text(screen, 540+ods,20, dis)  
text(screen, 540+ods,400, dt)

dis=str(nxtqh[0])+' - '+nxtqh[1]+':  '+str(nxtqh[2])
dt='  :  '+str(nxtqh[2]-mgld[2])
opis='Następny próg setny'
text(screen, 580+ods,20, opis)
text(screen, 620+ods,20, dis)  
text(screen, 620+ods,400, dt)

pygame.display.flip()

#Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()