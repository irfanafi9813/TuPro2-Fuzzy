import pandas as pd
import matplotlib.pyplot as plt
import operator

#Membaca data dari file
def bacaFile():
  df = pd.read_excel('bengkel.xlsx')
  return df


#Fuzzification
def fuzzyfication(tipe, nilai):
  if tipe=='servis':
    arrFuzServis = []
    arrFuzServis.append(nilai)

    #trapesium, a=1 b=1 c=30 d=50
    if nilai<1:
      kurang = 1
    elif nilai>=50:
      kurang = 0
    elif nilai>=1 and nilai<=30:
      kurang = 1
    elif nilai>30 and nilai<=50:
      kurang = -(nilai-50)/(50-30)

    #segitiga, a=40 b=70 c=80
    if nilai<=40 or nilai>=80:
      sedang = 0
    elif nilai>40 and nilai<=70:
      sedang = (nilai-40)/(70-40)
    elif nilai>70 and nilai<=80:
      sedang = -(nilai-80)/(80-70)

    #trapesium, a=70 b=85 c=100 d=100
    if nilai<=70:
      baik = 0
    elif nilai>=100:
      baik = 1
    elif nilai>70 and nilai<85:
      baik = (nilai-70)/(85-70)
    elif nilai>=85 and nilai<=100:
      baik = 1

    arrFuzServis.append(kurang)
    arrFuzServis.append(sedang)
    arrFuzServis.append(baik)
    return arrFuzServis
  else:
    arrFuzHarga = []
    arrFuzHarga.append(nilai)

    #trapesium a=1 b=2 c=3 d=5
    if nilai<1:
      murah = 1
    elif nilai>=5:
      murah = 0
    elif nilai>=1 and nilai<=3:
      murah = 1
    elif nilai>3 and nilai<=5:
      murah = -(nilai-5)/(5-3)

    #trapesium a=4 b=5 c=6 d=7
    if nilai<=4 or nilai>=7:
      sedang = 0
    elif nilai>4 and nilai<5:
      sedang = (nilai-4)/(5-4)
    elif nilai>=5 and nilai<=6:
      sedang = 1
    elif nilai>6 and nilai<=7:
      sedang = -(nilai-7)/(7-6)

    #trapesium a=6 b=7 c=8 d=9
    if nilai<=6 or nilai>=9:
      mahal = 0
    elif nilai>6 and nilai<7:
      mahal = (nilai-6)/(7-6)
    elif nilai>=7 and nilai<=8:
      mahal = 1
    elif nilai>8 and nilai<=9:
      mahal = -(nilai-9)/(9-8)

    #trapesium a=8 b=9 c=10 d=10
    if nilai<=8:
      mahalSekali = 0
    elif nilai>10:
      mahalSekali = 1
    elif nilai>8 and nilai<9:
      mahalSekali = (nilai-8)/(9-8)
    elif nilai>=9 and nilai<=10:
      mahalSekali = 1

    arrFuzHarga.append(murah)
    arrFuzHarga.append(sedang)
    arrFuzHarga.append(mahal)
    arrFuzHarga.append(mahalSekali)
    return arrFuzHarga


#Inferensi
def inferensi(servis, harga):
  arrInferensi = []
  rendah1 = min(harga[1], servis[1])
  rendah2 = min(harga[2], servis[1])
  rendah3 = min(harga[3], servis[1])
  rendah4 = min(harga[4], servis[1])
  rendah5 = min(harga[3], servis[2])
  rendah6 = min(harga[4], servis[2])
  rendah7 = min(harga[4], servis[3])
  tinggi1 = min(harga[1], servis[2])
  tinggi2 = min(harga[2], servis[2])
  tinggi3 = min(harga[1], servis[3])
  tinggi4 = min(harga[2], servis[3])
  tinggi5 = min(harga[3], servis[3])

  arrInferensi.append(max(rendah1, rendah2, rendah3, rendah4, rendah5, rendah6, rendah7))
  arrInferensi.append(max(tinggi1, tinggi2, tinggi3, tinggi4, tinggi5))
  return arrInferensi


#Defuzzification
def defuzzyfication(rendah, tinggi):
  if rendah+tinggi==0:
    return 0
  else:
    ting = 80
    ren = 50
    hitung = (rendah*ren)+(tinggi*ting)/(rendah+tinggi)
    return hitung


#Menyimpan output ke file
def exportFile(file):
  dictFuzzFinal = {}
  dictFuzzSorted = sorted(file.items(), key=operator.itemgetter(1), reverse=True)
  i=0
  for k,v in dictFuzzSorted:
    if i!=10:
      dictFuzzFinal[k] = v
      i+=1

  export = pd.DataFrame(data=dictFuzzFinal, index=[0])
  export = pd.DataFrame(list(dictFuzzFinal.items()),columns = ['ID','Skor Fuzzy']) 
  export.to_excel('peringkat.xlsx', index=False)


#Plot
def plotServis():
  x1 = [1, 1, 30, 50]
  y1 = [1, 1, 1, 0]
  x2 = [40, 70, 80]
  y2 = [0, 1, 0]
  x3 = [70, 85, 100, 100]
  y3 = [0, 1, 1, 1]
  plt.plot(x1, y1,'r-',label = 'Kurang') 
  plt.plot(x2, y2,'b-',label = 'Sedang') 
  plt.plot(x3, y3,'g-',label = 'Baik')
  plt.title('Kualitas Servis') 
  plt.legend()
  plt.show()

def plotHarga():
  x1 = [1, 2, 3, 5]
  y1 = [1, 1, 1, 0]
  x2 = [4, 5, 6, 7]
  y2 = [0, 1, 1, 0]
  x3 = [6, 7, 8, 9]
  y3 = [0, 1, 1, 0]
  x4 = [8, 9, 10, 10]
  y4 = [0, 1, 1, 1]
  plt.plot(x1, y1,'r-',label = 'Murah') 
  plt.plot(x2, y2,'b-',label = 'Sedang') 
  plt.plot(x3, y3,'g-',label = 'Mahal')
  plt.plot(x4, y4,'y-',label = 'Sangat Mahal')
  plt.title('Harga') 
  plt.legend()
  plt.show()

def plotDefuzz():
  plt.axvline(x = 50, color = 'b', label = 'Rendah')
  plt.axvline(x = 80, color = 'r', label = 'Tinggi')
  plt.title('Defuzzification') 
  plt.legend()
  plt.show()


#Main
df = bacaFile()

arrDefuzz = []
dictFuzz = {}
for i in range(100):  
  x = df.at[i, 'servis']
  y = df.at[i, 'harga']
  
  hasilFuzzServis = fuzzyfication('servis', x)
  hasilFuzzHarga = fuzzyfication('harga', y)

  hasilInferensi = inferensi(hasilFuzzServis, hasilFuzzHarga)

  hasilDefuzz = defuzzyfication(hasilInferensi[0], hasilInferensi[1])

  dictFuzz[i+1] = hasilDefuzz

exportFile(dictFuzz)