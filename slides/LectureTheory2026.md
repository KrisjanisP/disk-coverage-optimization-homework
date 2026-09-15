![img-0.jpeg](img-0.jpeg)

LATVIJAS
UNIVERSITĀTE

# Praktiskā kombinatoriālā
optimizācija

2. lekcija - Pamatjēdzieni

# Nepārtraukta problēma

(Continuous optimization)

# Diskrēta problēma

(Discrete optimization)

![img-1.jpeg](img-1.jpeg)

![img-2.jpeg](img-2.jpeg)

LATVIJAS
UNIVERSITĀTE

2

![img-3.jpeg](img-3.jpeg)

## No Free Lunch Theorem

Wolpert, D. H., & Macready, W. G. (1997). *No Free Lunch Theorems for Optimization*. IEEE Transactions on Evolutionary Computation, 1(1), 67–82.

https://doi.org/10.1109/4235.585893

![img-4.jpeg](img-4.jpeg)

LATVIJAS
UNIVERSITĀTE

3

# Pamatjēdzieni

**Definīcija 1. Kombinatoriālās optimizācijas problēma** tiek specificēta kā **risinājumu instanču kopa** un ir vai nu minimizācijas, vai maksimizācijas problēma.

**Definīcija 2.** Kombinatoriālās optimizācijas problēmas instance ir pāris $(\varphi, f)$, kur $\varphi$ ir problēmas risinājumu kopa un $f$ ir $f: \varphi \to \mathbb{R}$ izmaksu (cost) funkcija. Atrisināt optimizācijas problēmu nozīmē atrast tādu $i^* \in \varphi$, ka $\forall i \in \varphi, f(i^*) \leq f(i)$. Ar $f^* = f(i^*)$ apzīmēsim optimālās izmaksas, bet ar $\varphi^* = \{i \in \varphi | f(i) = f^*\}$ optimālo risinājumu kopu.

LATVIJAS  
UNIVERSITĀTE

4

# Pamatjēdzieni – kārtošanas piemērs

Problēma: sakārtot masīvu [5,1,3,6] dilstošā secībā!

φ

Risinājumu instanču kopa

1 5 6 3

1 6 3 5

1 5 3 6

1 3 5 6

1 6 5 3

3 1 6 5

1 3 6 5

3 1 5 6

3 6 5 1

3 5 1 6

3 6 1 5

5 3 6 1

5 1 6 3

5 6 3 1

Risinājuma instance - i

5 1 3 6

i(j) - j-tais elements masīvā i

5 3 1 6

5 6 1 3

5 3 6 1

Izmaksu funkcija

$$f(\pi) = \sum_{j=1}^n j\pi(j)$$, kur $$\pi \in \varphi$$ un $$n$$ ir masīva izmērs

6 5 3 1

Optimālā atrisinājuma instance - $$i^*$$

$$f(i) = \sum_{j=1}^4 ji(j) = 1 * 5 + 2 * 1 + 3 * 3 + 4 * 6 = 40$$

6 5 1 3

6 3 1 5

$$f(i^*) = \sum_{j=1}^4 ji^*(j) = 1 * 6 + 2 * 5 + 3 * 3 + 4 * 1 = 29 = f^*$$

6 3 5 1

Optimālo risinājumu kopa
$$\varphi^* = \{i^*\}$$

LATVIJAS
UNIVERSITĀTE

5

# Pamatjēdzieni (2)

**Definīcija 3.** Kombinatoriālās optimizācijas problēmas instancei $(\varphi, f)$ par apkārtnes (neighborhood) funkciju $V: \varphi \to 2^\varphi$ sauc funkciju, kas $\forall i \in \varphi$ definē problēmas risinājumu kopu $V(i) \subseteq \varphi$, kas ir “tuvas” risinājumam $i$ – tā apkārtni. $\forall j \in V(i)$ sauksim par $i$ kaimiņu. Tāpat pieņemsim, ka $\forall i \in \varphi \ i \in V(i)$.

LATVIJAS  
UNIVERSITĀTE

6

# Kārtošanas piemērs (2)

**Problēma:** sakārtot masīvu [5,1,3,6] dilstošā secībā!

$V(\pi) = \{k \in \varphi \mid \exists j, ka \pi(j) = k(j+1) \& \pi(j+1) = k(j) \& \forall l, kam l < j vai l > j+1, \pi(l) = k(l)\} \cup \{\pi\}$, kur $\pi \in \varphi$

Apkārtni iegūst samainot vietām divus blakus esošus masīva elementus

![img-5.jpeg](img-5.jpeg)

k-exchange neighbourhood

![img-6.jpeg](img-6.jpeg)

LATVIJAS
UNIVERSITĀTE

7

# Pamatjēdzieni (3)

**Definīcija 4.** Kombinatoriālās optimizācijas problēmas instancei $(\varphi, f)$ un apkārtnes funkcijai $V$ risinājumu $\hat{i} \in \varphi$ sauksim par lokāli optimālo, ja $\forall i \in V(\hat{i})$, $f(\hat{i}) \leq f(i)$. Lokāli optimālo risinājumu kopu apzīmēsim ar $\hat{\varphi}$.

**Definīcija 5.** Kombinatoriālās optimizācijas problēmas instancei $(\varphi, f)$ apkārtnes funkciju $V$ sauksim par precīzu? (exact), ja $\hat{\varphi} \subseteq \varphi^*$.

Visi lokāli optimālie risinājumi ir optimāli!

LATVIJAS
UNIVERSITĀTE

8

# Kārtošanas piemērs (3)

**Problēma:** sakārtot masīvu [5,1,3,6] dilstošā secībā!

$V(\pi) = \{k \in \varphi \mid \exists j, ka \pi(j) = k(j+1) \& \pi(j+1) = k(j) \& \forall l, kam l < j vai l > j+1, \pi(l) = k(l)\} \cup \{\pi\}$, kur $\pi \in \varphi$

Apkārtni iegūst samainot vietām divus blakus esošus masīva elementus

![img-7.jpeg](img-7.jpeg)

Izmaksu funkcija

$f(\pi) = \sum_{j=1}^n j\pi(j)$, kur $\pi \in \varphi$ un $n$ ir masīva izmērs

6 5 3 1 $f^* = 29$

Optimālā atrisinājuma instance - $i^*$

Optimizācija – meklēšana risinājumu grafā, kuram šķautnes veido apkārtnes f-ja

![img-8.jpeg](img-8.jpeg)

LATVIJAS
UNIVERSITĀTE

9

# Kārtošanas piemērs (4)

**Problēma:** sakārtot masīvu [5,1,3,6] dilstošā secībā!

$V(\pi) = \{k \in \varphi \mid \exists j, ka \pi(j) = k(j+1) \& \pi(j+1) = k(j) \& \forall l, kam l < j vai l > j+1, \pi(l) = k(l)\} \cup \{\pi\}$, kur $\pi \in \varphi$

Apkārtni iegūst samainot vietām divus blakus esošus masīva elementus

![img-9.jpeg](img-9.jpeg)

Izmaksu funkcija

$f(\pi) = \sum_{j=1}^n j\pi(j)$, kur $\pi \in \varphi$ un $n$ ir masīva izmērs

6 5 3 1 $f^* = 29$

Optimālā atrisinājuma instance - $i^*$

![img-10.jpeg](img-10.jpeg)

LATVIJAS  
UNIVERSITĀTE

10

# Kārtošanas piemērs (5)

**Problēma:** sakārtot masīvu [5,1,3,6] dilstošā secībā!

$V(\pi) = \{k \in \varphi \mid \exists j, ka \pi(j) = k(j+1) \& \pi(j+1) = k(j) \& \forall l, kam l < j vai l > j+1, \pi(l) = k(l)\} \cup \{\pi\}$, kur $\pi \in \varphi$

Apkārtni iegūst samainot vietām divus blakus esošus masīva elementus

![img-11.jpeg](img-11.jpeg)

Izmaksu funkcija

$f(\pi) = \sum_{j=1}^n j\pi(j)$, kur $\pi \in \varphi$ un $n$ ir masīva izmērs

6 5 3 1 $f^* = 29$

Optimālā atrisinājuma instance - $i^*$

![img-12.jpeg](img-12.jpeg)

LATVIJAS  
UNIVERSITĀTE

11

# Kārtošanas piemērs (6)

**Problēma:** sakārtot masīvu [5,1,3,6] dilstošā secībā!

$V(\pi) = \{k \in \varphi \mid \exists j, ka \pi(j) = k(j+1) \& \pi(j+1) = k(j) \& \forall l, kam l < j vai l > j+1, \pi(l) = k(l)\} \cup \{\pi\}$, kur $\pi \in \varphi$

Apkārtni iegūst samainot vietām divus blakus esošus masīva elementus

![img-13.jpeg](img-13.jpeg)

Izmaksu funkcija

$f(\pi) = \sum_{j=1}^n j\pi(j)$, kur $\pi \in \varphi$ un $n$ ir masīva izmērs

6 5 3 1 $f^* = 29$

Optimālā atrisinājuma instance - $i^*$

![img-14.jpeg](img-14.jpeg)

LATVIJAS  
UNIVERSITĀTE

12

# Kārtošanas piemērs (7)

**Problēma:** sakārtot masīvu [5,1,3,6] dilstošā secībā!

$V(\pi) = \{k \in \varphi \mid \exists j, ka \pi(j) = k(j+1) \& \pi(j+1) = k(j) \& \forall l, kam l < j vai l > j+1, \pi(l) = k(l)\} \cup \{\pi\}$, kur $\pi \in \varphi$

Apkārtni iegūst samainot vietām divus blakus esošus masīva elementus

![img-15.jpeg](img-15.jpeg)

LATVIJAS
UNIVERSITĀTE

13

# META algoritms

![img-16.jpeg](img-16.jpeg)

**Lokālās meklēšanas process** ir *klejošana* meklēšanas telpā, orientētā grafā, kura virsotnes ir risinājumi un šķautnes realizē apkārtnes funkciju.

**Kad šo procesu beigt?**

![img-17.jpeg](img-17.jpeg)

LATVIJAS
UNIVERSITĀTE

14

# Definējošie vienumi un to atkarības

![img-18.jpeg](img-18.jpeg)

[LOGO]

LATVIJAS
UNIVERSITĀTE

15

# N-Queens problēma

Dots **nxn laukums** un **n** šaha **dāmas**. Atrast tādu dāmu izvietojumu, lai tās viena otru neapdraudētu.

Plānošanas mainīgie!

Risinājumu kopa $\varphi$ ir visu iespējamo pozīciju kopa, kur pozīcija ir masīvs Q garumā **n**, kas satur pārīšus (**c,r**), kas raksturo katras dāmas novietojumu – kolonu un rindu, kurā tā atrodas. Ja $x \in Q$, tad $\mathbf{x}_c - x$ kolonas numurs, $\mathbf{x}_r - x$ rindas numurs.

![img-19.jpeg](img-19.jpeg)

$$|\varphi| = 64^8 \approx 10^{14}$$

Izmaksu funkcija: $f(q) = \sum_{\substack{i, j \in q \\ i \neq j}} (eq(i_c, j_c) + eq(i_r, j_r) + eq(i_c + i_r, j_c + j_r) + eq(i_c - i_r, j_c - j_r))$

$$eq(i, j) = \begin{cases} 1, i = j \\ 0, cit\bar{a}di \end{cases}$$

Apkārtnes f-ja: pārvietojam dāmu!

Ja mēs nofiksējam katru dāmu savā kolonā, tad mēs dāmai varam mainīt tikai rindu.

LATVIJAS
UNIVERSITĀTE

16

# Traveling Salesman Problem (TSP)

Dota **n**-pilsētu kopa un **nxn** distanču matrica **D**, kur matricas elements **dij** apzīmē attālumu no pilsētas **i** uz pilsētu **j**. **Atrast visīsāko maršrutu**, kas apmeklē katru pilsētu tieši vienreiz un atgriežas sākuma punktā.

Risinājumu kopa $\varphi$ ir visu **Hamiltona ciklu c** kopa pilnā, svarotā grafā **G**, kura virsotnes atbilst pilsetām, bet šķautņu (i,j) svari attālumiem starp pilsētām.

Par risinājumu kopu $\varphi$ var uzskatīt arī visu iespējamo pilsētu kombināciju ar fiksētu pirmo pilsētu kopu.

$$f(c) = \sum_{i=1}^{n-1} (d_{c(i-1),c(i)}) + d_{c(n-1),c(0)}$$

$$f(c) = \sum_{i,j} d_{ij}$$

Apkārtnes f-ja (k-exchange) izņemam k šķautnes un aizstājam tās ar citām!

Apkārtnes f-jas (k-exchange): 2-opt, 3-opt, Or-opt ...

Apkārtnes f-jas (citas): Lin-Kernighan (LK), Helsgauna LK, Dynasearch, ...

![img-20.jpeg](img-20.jpeg)

![img-21.jpeg](img-21.jpeg)

![img-22.jpeg](img-22.jpeg)

![img-23.jpeg](img-23.jpeg)

![img-24.jpeg](img-24.jpeg)

![img-25.jpeg](img-25.jpeg)

![img-26.jpeg](img-26.jpeg)

ABCD
ABDC
ACBD
ACDB
ADBC
ADCB

|   | A | B | C | D  |
| --- | --- | --- | --- | --- |
|  A | 0 | 3 | 5 | 5  |
|  B | 5 | 0 | 4 | 1  |
|  C | 5 | 6 | 0 | 5  |
|  D | 5 | 5 | 7 | 0  |

LATVIJAS
UNIVERSITĀTE

17

Mixed Integer Programs (MIPs)

# Veselo skaițiu optimizācija

https://docs.mosek.com/modeling-cookbook/index.html

# TSP Dantzig–Fulkerson–Johnson formulation

Label the cities with the numbers 1, ..., n and define:

$$x_{ij} = \begin{cases} 1 & \text{the path goes from city } i \text{ to city } j \\ 0 & \text{otherwise} \end{cases}$$

Take $c_{ij} > 0$ to be the distance from city $i$ to city $j$. Then TSP can be written as the following integer linear programming problem:

$$\min \sum_{i=1}^n \sum_{j \neq i, j=1}^n c_{ij} x_{ij}:$$

$$\sum_{i=1, i \neq j}^n x_{ij} = 1 \quad j = 1, \dots, n;$$

$$\sum_{j=1, j \neq i}^n x_{ij} = 1 \quad i = 1, \dots, n;$$

$$\sum_{i \in Q} \sum_{j \neq i, j \in Q} x_{ij} \leq |Q| - 1 \quad \forall Q \subsetneq \{1, \dots, n\}, |Q| \geq 2$$

https://en.wikipedia.org/wiki/Travelling_salesman_problem

18

LATVIJAS
UNIVERSITĀTE

# Naivais (kalnā kāpšanas) algoritms.

1. Konstruējam sākotnējo risinājumu
2. Atrodam apkārtni
3. Novērtējam apkārtni
4. Izvēlamies labāko no apkārtnes
5. Ja šis risinājums ir labāks par tekošo, tad atceramies to un pārejam pie punkta 2.
6. Šibrīža risinājumu pasludinām par galīgo.

![img-27.jpeg](img-27.jpeg)

Algoritms atrod LOKĀLO optimumu!

LATVIJAS
UNIVERSITĀTE

19

# Rastrigin + Michalewicz + Alpine in 3D

![img-28.jpeg](img-28.jpeg)

Rastrigina, Mihaļeviča un Alpīnes kompozitfunkcija trīs dimensiļās (E.Bergholcs, 2026, Maģistra darbs ĢENĒTISKO ALGORITMU STĀVOKĻA DIAGNOSTIKA, IZMANTOJOT TOPOLOĢISKO DATU ANALĪZI)

LATVIJAS
UNIVERSITĀTE

20

# Naivā iteratīvā lokālā meklēšana.

1. **Konstruējam** sākotnējo risinājumu ar kādu no konstruēšanas heiristikām.
2. **Meklējam** lokālo optimumu un **atceramies** to.
3. **Kamēr nav** izpildījušies pārtraukšanas kritēriji
   3.1. **Izvēlamies** jaunu risinājumu, vēlams tālāk no atrastā lokālā optimuma.
   3.2. **Meklējam** lokālo optimumu un **atceramies** to.
   3.3. Ja atrastais optimums ir labāks par iepriekšējo, tad **piefiksējam** to
4. **Labāko** atrasto risinājumu **pasludinām** par galīgo.

LATVIJAS
UNIVERSITĀTE

21

# Definējošie vienumi un to atkarības

![img-29.jpeg](img-29.jpeg)

[LOGO]

LATVIJAS
UNIVERSITĀTE

22

Tas arī viss!

![img-30.jpeg](img-30.jpeg)

![img-31.jpeg](img-31.jpeg)

LATVIJAS
UNIVERSITĀTE