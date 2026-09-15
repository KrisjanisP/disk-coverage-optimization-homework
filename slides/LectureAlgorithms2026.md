![img-0.jpeg](img-0.jpeg)

LATVIJAS
UNIVERSITĀTE

# Praktiskā kombinatoriālā
optimizācija

3. lekcija - Algoritmi

# Definējošie vienumi un to atkarības

![img-1.jpeg](img-1.jpeg)

$f = 31$

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

# META algoritms - 1. solis

![img-5.jpeg](img-5.jpeg)

**Lokālās meklēšanas process** ir *klejošana* meklēšanas telpā, orientētā grafā, kura virsotnes ir risinājumi un šķautnes realizē apkārtnes funkciju.

![img-6.jpeg](img-6.jpeg)

LATVIJAS
UNIVERSITĀTE

4

# Risinājuma konstruēšana (1)

## First Fit

First Fit Decreasing

Weakest Fit

Strongest Fit

Strongest Fit Decreasing

Allocate From Queue

Cheapest Insertion

Regret Insertion

Allocate From Pool

4-Queens

![img-7.jpeg](img-7.jpeg)

![img-8.jpeg](img-8.jpeg)

![img-9.jpeg](img-9.jpeg)

![img-10.jpeg](img-10.jpeg)

![img-11.jpeg](img-11.jpeg)

Konstruējam risinājumu, inicializējot plānošanas mainīgos pa vienam.

Pirmais labākais risinājums tiek akceptēts

![img-12.jpeg](img-12.jpeg)

LATVIJAS
UNIVERSITĀTE

5

# Risinājuma konstruēšana (2)

First Fit

**First Fit Decreasing**

Weakest Fit

Strongest Fit

Strongest Fit Decreasing

Allocate From Queue

Cheapest Insertion

Regret Insertion

Allocate From Pool

4-Queens

![img-13.jpeg](img-13.jpeg)

f=0

![img-14.jpeg](img-14.jpeg)

f=0

![img-15.jpeg](img-15.jpeg)

f=1

![img-16.jpeg](img-16.jpeg)

f=2

Grūtāk ielikt
dāmas pa vidu!

f=1

![img-17.jpeg](img-17.jpeg)

f=1

f=0

![img-18.jpeg](img-18.jpeg)

f=1

Pirmais labākais risinājums tiek akceptēts

Ievietojamie objekti tiek sarindoti pēc
*grūtības*, t.i., mēs vēlamies, lai vispirms tiktu
iekļauti tie objekti, kurus beigās ielikt ir
grūtāk.

![img-19.jpeg](img-19.jpeg)

f=2

![img-20.jpeg](img-20.jpeg)

f=1

![img-21.jpeg](img-21.jpeg)

f=2

![img-22.jpeg](img-22.jpeg)

f=2

f=0

LATVIJAS
UNIVERSITĀTE

6

# Risinājuma konstruēšana (3)

First Fit

First Fit Decreasing

Weakest Fit

Weakest Fit Decreasing

Strongest Fit

Strongest Fit Decreasing

Allocate From Queue

Cheapest Insertion

Regret Insertion

Allocate From Pool

Pirmais labākais risinājums tiek akceptēts.

Objektiem piekārtotās vērtības tiek sarindotas pēc *spēka*, t.i., mēs vēlamies, lai objektam tiktu piekārtota vērtība, kuru beigās/sākumā ielikt ir grūtāk.

Vispārinājums augstākajiem

Pirmais labākais risinājums starp visu objektu ievietošanām tiek akceptēts

Izvēlēts tāds risinājums, kur objekta ievietošana sniedz vislielāko ieguvumu salīdzinot ar šī paša objekta citām ievietošanām

Ievietojamie objekti tiek sarindoti pēc *grūtības*, t.i., mēs vēlamies, lai vispirms tiktu iekļauti tie objekti, kurus beigās ielikt ir grūtāk. (**Decreasing**)

Objektus apskata pa vienam!

Objektus apskata visus!

LATVIJAS  
UNIVERSITĀTE

7

# Risinājuma konstruēšana - tuvākais kaimiņš (4)

Pamatideja - konstruēt risinājumu pa
soļiem, katrā solī pievienojot nākošo
galamērķi. Izvēlās **tuvāko**!

![img-23.jpeg](img-23.jpeg)

Atrast gana labu risinājumu, lai
lokālai meklēšanai būtu *vieglāk*

LATVIJAS
UNIVERSITĀTE

8

# META algoritms

![img-24.jpeg](img-24.jpeg)

**Lokālās meklēšanas process** ir *klejošana* meklēšanas telpā, orientētā grafā, kura virsotnes ir risinājumi un šķautnes realizē apkārtnes funkciju.

[LOGO]

LATVIJAS
UNIVERSITĀTE

9

# Threshold Algorithms

Optimizācijas problēma

$$(\varphi, f)$$

Apkārtnes funkcija

$$V: \varphi \rightarrow 2^\varphi$$

Akceptēšanas sliekšņu saraksts.

$$t = [t[k] \in R | k = 0, 1, 2, \dots]$$

Risinājumu kopa

$$\varphi$$

Izmaksu funkcija

$$f: \varphi \rightarrow R$$

Uzkonstruē/izvēlas sākotnējo risinājumu

function THRESHOLD_ALGORITHM($\varphi, f, V, t$)

begin

best, i := INITIALIZE($\varphi, f$)

k := 0

repeat

j := GENERATE($V(i)$)

if $f(j) - f(\text{best}) < 0$ then best := j

if $f(j) - f(i) < t[k]$ then i := j

k := k + 1

until STOP_CRITERION_HOLDS()

return best

end

Izvēlas nākošā risinājuma kandidātu no apkārtnes

Nākošā risinājumu akceptē, ja tas nav sliktāks par esošo vai starpība neparsniedz šīs iterācijas slieksni

Turpina līdz izpildās apstāšanās kritēriji.

LATVIJAS
UNIVERSITĀTE

10

# Threshold Algorithms (2)

Akceptēšanas sliekšņu saraksts.

$$t = [t[k] \in R | k = 0, 1, 2, \dots]$$

function THRESHOLD_ALGORITHM($\varphi, f, V, t$)

begin

best, i := INITIALIZE($\varphi, f$)

k := 0

repeat

j := GENERATE($V(i)$)

if $f(j) - f(\text{best}) < 0$ then best := j

if $f(j) - f(i) < t[k]$ then i := j

k := k + 1

until STOP_CRITERION_HOLDS()

return best

end

![img-25.jpeg](img-25.jpeg)

Ja $\forall k, t[k] = 0$, mēs iegūstam naivo algoritmu, kas atrod lokālo optimumu.

Ja $\forall k, t[k] \geq t[k+1]$ un $\lim_{k \to \infty} t[k] = 0$, tad mēs iegūstam monotoni dilstošu sliekšņu virkni. Tas ļauj sākumā akcpetēt lielāku izmaksu palielināšanos, pamazām pārejot uz lokālā optimuma meklēšanu.

![img-26.jpeg](img-26.jpeg)

LATVIJAS
UNIVERSITĀTE

11

# Simulated Annealing - analogija ar fiziku

![img-27.jpeg](img-27.jpeg)

![img-28.jpeg](img-28.jpeg)

Daniel Delahaye, Supatcha Chaimatanan, Marcel Mongeau. Simulated annealing: From basics to applications. Gendreau, Michel; Potvin, Jean-Yves. Handbook of Metaheuristics, 272, Springer, pp.1-35.ISBN 978-3-319-91085-7, 2019, International Series in Operations Research & Management Science (ISOR), 978-3-319-91086-4. 10.1007/978-3-319-91086-4_1 . hal-01887543

https://hal-enac.archives-ouvertes.fr/hal-01887543/document

![img-29.jpeg](img-29.jpeg)

LATVIJAS
UNIVERSITĀTE

12

# Simulated Annealing

Akceptēšanas sliekšņu saraksts. "Temperatūra"

$$t = [t[k] \in R | k = 0, 1, 2, \dots]$$

Iterāciju soļu skaita saraksts.

$$L = [L[k] \in N | k = 0, 1, 2, \dots]$$

function SIMULATED_ANNEALING($\varphi, f, V, t, L$)

begin

best, i := INITIALIZE($\varphi, f$)

k := 0

repeat

for n := 0 to L[k] do

j := GENERATE(V(i))

if $f(j) - f(\text{best}) < 0$ then best := j

if $f(j) - f(i) < 0$ or random(1) < e^{\frac{f(i) - f(j)}{t[k]}}$ then i := j

k := k + 1

until $t[k] \simeq 0$

return best

end

Stohastisks, nedeterminēts, algoritms.

Konverģē uz globālo optimumu ...
pie bezgalīgi daudzām iterācijām :(

Veids, kā virzīties uz pareizo
"baseinu"

![img-30.jpeg](img-30.jpeg)

![img-31.jpeg](img-31.jpeg)

Simulated annealing accept/reject new solution
candidate based on probability

LATVIJAS
UNIVERSITĀTE

13

# Simulated Annealing

L=[3,3,2,2,2]

t=[2.0, 1.6, 1.2, 0.8, 0.4]

t var mainīt lineāri,

ģeometriski, ...

![img-32.jpeg](img-32.jpeg)

$$e^{\frac{f(i) - f(j)}{t[k]}}$$

UNIVERSITAS

LATVIJAS

UNIVERSITĀTE

14

# Lokālā meklēšana ar atmiņu - *Tabu search*

**Problēma** - apskatot neuzlabojošus risinājumus, iespējami **cikli!**

function LOCAL_SEARCH_WITH_MEMORY($\varphi, f, V'$)

begin

best, i := INITIALIZE($\varphi, f$)

$M$ =CHANGE($M, i$)

repeat

**Izmaina** atmiņu atkarībā no izvēlētā risinājuma

i := GENERATE($V'(i, M)$)

if $f(i) - f(\text{best}) < 0$ then best := i

$M$ =CHANGE($M, i$)

until STOP_CRITERION_HOLDS()

return best

end

**Beigt**, kad:

- $V'(i, M) = \emptyset$

- pēc noteikta iterāciju skaita

- kad būtiski uzlabojumi nav notikuši noteiktu laiku

Nepieciešama **atmiņa** - $M$

Atceramies jau redzēto!

Apkārtnes izvēle kļūst atkarīga no atmiņas!

Piemēram, ja $M = (i^*, T)$, tad $V'(i, M) = V(i) - T$

$T = [T[k] \in \varphi | k = 0, 1, \dots, n]$

## Ko var glabāt atmiņā?

Piemēram, atceramies, kad pēdējo reizi šāds **risinājums** ir redzēts. Vai kad pēdējo reizi dotais **objekts** ir piedalījies gājienā. Vai kad pēdējo reizi dotā **vertība** ir piešķirta objektam. Vai kad dotais **gājiens** ir pielietots. Kad vietā (*short term*) var uzskaitīt arī **reizes** (*long term*)!

LATVIJAS
UNIVERSITĀTE

15

# Tabu search - atmiņa

4-Queens

![img-33.jpeg](img-33.jpeg)

|  -1 | 0 | 1 | 2  |
| --- | --- | --- | --- |
|  2 | 0 | 1 | 3  |

Pirms, cik iterācijām dāma ir bijusi pārvietota!

Cik reizes katra no dāmām ir pārvietota

Iterācijas numurs, kad tika pārvietota

Tas ļauj salīdzināt/izvērtēt potenciālās izmaiņas attiecībā pret meklēšanas vesturi! Piemēram, izvēlēties mainīt tās instances, kas ir mazāk vai senāk mainītas.

|  1 | 0 | 1 | 2  |
| --- | --- | --- | --- |
|  3 | 0 | 1 | 4  |
|  4 | 1 | 0 | 0  |
|  7 | 3 | 0 | 0  |

Cik reizes katrā no lauciņiem ir nonākusi dāma

$V'(i, M) = \{ j \in V(i) | !t(i, j, M) \}$ , kur **t** ir tabu nosacījums.

$V'(i, M) = \{ j \in V(i) | !t(i, j, M) \| a(i, j, M) \}$ , kur **a** ir "amnestijas" (*aspiration*) nosacījums.

$G(i)$ - iespējamo gājienu kopa risinājumam i.

$j = i \oplus m$ - ja risinājumu j var iegūt risinājumam i pielietojot gājienu m.

$V(i) = \{ j \in \varphi | \exists m \in G(i) \& j = i \oplus m \}$

$V'(i, M) = \{ j \in V(i) | \exists m \in G(i) \& j = i \oplus m \& (!t(i, m, M) \| a(i, m, M)) \}$

LATVIJAS  
UNIVERSITĀTE

16

# Tabu search - piemērs

4-Queens

T

![img-34.jpeg](img-34.jpeg)

f=2

Apzīmēsim dāmas ar Q={A,B,C,D}

Apzīmēsim gājienus ar G = {A1, B1, ..., C4, D4}

Apzīmēsim gājienus ar G(i,q) dāmas q iespējamos gājienus dotajā pozīcijā i. Piemēram, G(i,A)={A1, A2, A3}

Atmiņa $M = (i^*, T)$ – T ir rinda garumā 2, kurā atrodas pēdējās 2 redzētās dāmas.

$V'(i, M) = \{ j \in V(i) | \exists m \in G(i) \& j = i \oplus m \& (!t(i, m, M) \| a(i, m, M)) \}$

$t(i, m, (i^*, T)) = m \in G(i, T[0]) \| m \in G(i, T[1])$

![img-35.jpeg](img-35.jpeg)

f=1

Intensifikācija vs Diversifikācija
Attālums starp risinājumiem

![img-36.jpeg](img-36.jpeg)

f=1

B C

![img-37.jpeg](img-37.jpeg)

f=0

A B

LATVIJAS
UNIVERSITĀTE

17

# Late Acceptance Hill-Climbing

function LAHC($\varphi, f, V, n$)

begin

best, i := INITIALIZE($\varphi, f$)

for all $k \in [0, \dots, n-1]$

k := 0

repeat

$L_f[k] := f(i)$

j := GENERATE($V(i)$)

k := k mod n

if $f(j) - f(\text{best}) < 0$ then best := j

if $f(j) - f(i) < 0$ or $f(j) < L_f[k]$ then i := j

$L_f[k] := f(j)$
k := k + 1

until STOP_CRITERION_HOLDS()

return best

end

Ideja vienkāršot algoritmu un padarīt
to mazāk atkarīgu no domeina!

Atcerās n pēdējo apskatīto risinājumu
izmaksu vērtības! Sākuma inicializē
ar pirmā risinājuma izmaksu vērtību.

Akceptējam risinājumu, ja tas ir labāks
par esošo vai labāks par to, kas
apskatīts pirms n iterācijām!

LATVIJAS
UNIVERSITĀTE

18

# LAHC piemērs

4-Queens

![img-38.jpeg](img-38.jpeg)

f=2

![img-39.jpeg](img-39.jpeg)

f=3 >2

![img-40.jpeg](img-40.jpeg)

f=2 =2

![img-41.jpeg](img-41.jpeg)

f=3 >2

![img-42.jpeg](img-42.jpeg)

f=2 < 3 !

![img-43.jpeg](img-43.jpeg)

f=1 =2

![img-44.jpeg](img-44.jpeg)

f=2 < 3 !

![img-45.jpeg](img-45.jpeg)

f=1 < 2

![img-46.jpeg](img-46.jpeg)

f=3 >2

![img-47.jpeg](img-47.jpeg)

f=3 >2

![img-48.jpeg](img-48.jpeg)

f=2 >1

![img-49.jpeg](img-49.jpeg)

f=2 < 3 !

![img-50.jpeg](img-50.jpeg)

f=0

Vispirms tiek akceptēti gājieni, kas uzlabo esošo risinājumu.

Ja noteiktu laiku neizdodas atrast neko labāku, tad akceptē arī sliktākus risinājumus.

![img-51.jpeg](img-51.jpeg)

LATVIJAS
UNIVERSITĀTE

19

# Evolucionāro algoritmu analoģija dabā

![img-52.jpeg](img-52.jpeg)

LATVIJAS

UNIVERSITĀTE

20

# Genētiskie (Evolutionary) Algoritmi

Populācijas izmērs

function EVOLUTIONARY($\varphi, f, V, n$)
begin

I := INITIALIZE($\varphi, f, n$)

repeat

$$\sum_{i \in I} f(i)$$

avg_fitness := $\frac{i \in I}{n}$
mating_pool := SELECT(I, f, avg_fitness)
I := GENERATE(mating_pool, V, n)

until STOP_CRITERION_HOLDS()

return best

end

Izveidot populāciju (indivīdu kopa)

Izrēķināt populācijas veselību (fitness)

Izvelēties no populācijas indivīdus (mating pool)

Izmainīt izvelētos indivīdus (mutate vai/un crossover)

Atkārtot līdz iestājas beigu nosacījumi!

LATVIJAS
UNIVERSITĀTE

21

# Genētiskā algoritma piemērs

![img-53.jpeg](img-53.jpeg)

UNIVERSITAS BUDAPESTIS

LATVIJAS
UNIVERSITĀTE

22

# Citi algoritmi

**Iterated Greedy** Algorithms – atrod lokālo optimumu, **salauž** to, **konstruē** jaunu no "drupām", **meklē** lokālo optimumu, domā, vai akceptēt!

**Variable Neighborhood** Search – **izmantojam** vairākas apkārtnes f-jas!

- VN Descent - pēc kārtas kamēr katrā atrod optimumu
- Reduced VNS - iteratīvi pa solim kamēr vien ir uzlabojumi.
- Skewed VNS - vērtē attālumu starp risinājumiem

**Dynamic** Local Search – **izmaina izmaksu f-ju!** Soda noteiktas risinājuma komponentes. Meklē lokālos optimumus.

Greedy Randomized Adaptive Search Procedure (**GRASP**)- **konstruē** risinājumu **soli pa solim**, **meklē optimumu**, atkārto.

**Path-Relinking** - meklēt ceļu meklēšanas telpā uz labiem risinājumiem!

(Very) **Large** Neighborhood Search
Apkārtne tiek apstaigāta ar *destroy* (izdzēs daļu no risinājuma) un *repair* (salabo risinājumu) metodēm.

**Hyper-Heuristic** – metodes, kas mēģina izvēlēties piemērotāku algoritmu, apkārtnes f-ju (gājienus) dinamiski meklēšanas laikā.

**Dynamic Programming**

**Constraint Programming**

**Mixed-Integer Linear Programming**

LATVIJAS
UNIVERSITĀTE

23

# META algoritms

Vienreiz? Daudzreiz?

1. Atrast sākotnējo risinājumu

Nejauši? Iziet cauri visai?
Apkārtnes f-ju fiksēt?

Vai apkārtnes f-ja ņem vērā meklēšanas procesu?

Vai lauzt risinājumu?

2. Atrast apkārtni

Ņemt labāko?
Citi principi?

5. Izvēlēties nākošo risinājumu

Kad beigt?

4. Atcerēties līdz šim labāko redzēto risinājumu

3. Novērtēt apkārtni

LATVIJAS
UNIVERSITĀTE

24

# Machine learning for combinatorial optimization

https://doi.org/10.1016/j.ejor.2020.07.063

![img-54.jpeg](img-54.jpeg)

![img-55.jpeg](img-55.jpeg)

![img-56.jpeg](img-56.jpeg)

UNIVERSITAS
MDCCCXI

LATVIJAS

UNIVERSITĀTE

25

# Neural Combinatorial Optimization (NCO)

"Traditional solvers still **significantly** outperform NCO solvers in finding high-quality solutions, regardless of problem types and sizes"

Deep Learning, Deep Reinforcement Learning

## Learning Constructive Heuristics (LCH) -

pieliek nepabeigtam risinājumam nākošo

objektu!

Pointer Networks

Transformers

Graph Neural Networks

Recurrent Neural Networks (RNN)

Reinforcement Learning

Supervised vs Unsupervised

## Learning Improvement Heuristics (LIH) -

izvēlas risinājuma regionu un tā mainīšanas gājienu!

## Learning Hybrid Solvers (LHS) - ciešāk integrē NN iekš solvera!

Neural Large Neighbourhood Search – repair uztic NN.

NN palīdz izvēlēties škautnes LinKernighan-Helsgaun algoritmam (k-exchange apkārtne)

FEDERAL OF MISSIS CLASS FILES, VOL. 14, NO. 4, AUGUST 2022

## How Good Is Neural Combinatorial Optimization?

Shengcai Liu, Member, IEEE, Yu Zhang, Ke Tang, Senior Member, IEEE, and Xin Yao, Fellow, IEEE

Abstract—Traditional solvers for tackling combinatorial optimization (CCO) problems are usually designed by human experts. Recently, there has been a surge of interest in utilizing Deep Learning, especially Deep Reinforcement Learning, to automatically learn effective solvers for CCO. The resultant new paradigm is termed Neural Combinatorial Optimization (NCO). However, the advantages and disadvantages of NCO over other approaches have not been well studied empirically or theoretically. In this work, we present a comprehensive comparative study of NCO solvers and alternative solvers. Specifically, taking the Traveling Suburban Problem as the testbed problem, we assess the performance of the solvers in terms of five aspects, i.e., effectiveness, efficiency, stability, scalability and generalization ability. Our results show that in general the solvers learned by NCO approaches still fall short of traditional solvers in nearly all these aspects. A potential benefit of the former would be their superior time and energy efficiency on small-size problem instances when sufficient training instances are available. We hope this work would help better understand the strengths and weaknesses of NCO, and provide a comprehensive evaluation protocol for further benchmarking NCO approaches against other approaches.

Index Terms—Neural Combinatorial Optimization, Deep Reinforcement Learning, Comparative Study, Evaluation Protocol, Traveling Suburban Problem

Inspired by the success of Deep Learning (DL) in fields such as image classification [10], machine translation [11], and board games [12], recently there has been a surge of research interest in utilizing DL, especially Deep Reinforcement Learning (DRL), to automatically learn effective methods for CCO problems [13]. The resultant new paradigm is termed Neural Combinatorial Optimization (NCO) [14], [15]. For the sake of clarity, henceforth we will call the optimization method (either hand-engineered or automatically learned) the solver and call the way of designing a solver the design approach. Compared to traditional manual approach, NCO exhibits a significant paradigm shift in solver design. As illustrated in Figure 1, traditional solver design process is human-centered, while NCO is a learning-centered paradigm that develops a solver by training. The training process of NCO essentially calibrates the parameters of the solver (model). Albeit it would introduce more offline computational cost, the training process allows solver design to be conducted in an automated manner and thus involves much less human effort.

Despite the appealing features that NCO might bring, its advantages and disadvantages over other approaches have not been made fully clear. Specifically, although numerous

https://arxiv.org/pdf/2209.10913.pdf

"Thanks to their simple solving strategy and massively-parallel computing mode, a **major potential benefit of NCO** solvers both in terms of time and energy (10%)."

"However, when training instances have **different** problem characteristics from the testing instances, both NCO solvers and the tuned traditional solvers exhibit **performance degradation**. NCO solvers suffer from far more severe performance degradation"

LATVIJAS
UNIVERSITĀTE

26

## **Iemācīties solveri pilnībā 2015-2020**

Pointer networks, RL constructors, Attention Model, POMO.

## **Iemācīties solvera komponenti 2020-2023**

branching, cuts, neighborhoods, ACO heuristics, large-scale decoders.

## **Iemācīties risinājuma sadalījumu 2023-2025**

diffusion, Langevin methods, generative approaches.

## **Vispārināšanās, hibridizācija, *foundation* modeļi 2024-2026**

multi-problem solvers, representation learning, test-time adaptation, solver portfolios, self-improvement, search-space reduction.

LATVIJAS  
UNIVERSITĀTE

27

|  Approach | What NN learns | NN produces | Classical optimization still used? | Representative publications  |
| --- | --- | --- | --- | --- |
|  **1. Constructive solver** | How to build a solution sequentially | Next decision / action | Little / none | [1] Kool et al. (2019) – Attention Model [2] Kwon et al. (2020) – POMO  |
|  **2. Predict-then-decode** | Promising variables / edges / structural scores | Scores / heatmap / logits | Yes – decoder / search | [3] Fu et al. (2021) – heatmap + MCTS for large TSP  |
|  **3. Generative solver** | Distribution of high-quality solutions | Many candidate solutions / samples | Usually – decoding, projection or local search | [4] Sun & Yang (2023) – DIFUSCO ★ [5] Sanokowski et al. (2024) – unsupervised diffusion  |
|  **4. Improvement solver** | How to modify an incumbent solution | Move / neighborhood / rewrite / repair action | Yes | [6] Chen & Tian (2019) – NeuRewriter [7] Hottung & Tierney (2022) – Neural LNS  |
|  **5. Learned metaheuristic** | A heuristic component inside a metaheuristic | Pheromone / heuristic desirability / destroy-repair guidance | Strongly | [8] Ye et al. (2023) – DeepACO [9] Hottung & Tierney (2022) – Neural LNS  |
|  **6. Learning-enhanced exact solver** | Expensive decisions made inside exact search | Branching / cut selection / partial fixing | Yes – exact solver remains | [9] Gasse et al. (2019) – learning to branch [10] Pauks et al. (2022) – NeuralCat [11] Nair et al. (2020) – Neural Diving & Branching  |
|  **7. Search-space reduction / warm start** | Where good solutions or promising actions are likely to lie | Candidate sets / variable fixings / seeds | Yes | [11] Nair et al. (2020) – Neural Diving ★ [12] Zhou et al. (2026) – L2R search-space reduction  |
|  **8. Meta-solver / generalist** | Which solver / strategy to use, or a representation shared across problem variants | Solver choice / configuration / shared policy | Usually | ★ [13] Zhou et al. (2024) – MVMoE ★ [14] Gao et al. (2025) – Neural Solver Selection ★ [15] Berto et al. (2025) – RouteFinder  |
|  **9. Algorithm discovery** | Reusable heuristic or algorithmic code | Algorithm / program | Yes – evaluation / evolutionary search | ★ [16] Romera-Paredes et al. (2024) – FunSearch ★ [17] Novikov et al. (2025) – AlphaEvolve  |

[1] Kool, W., van Hoof, H., & Welling, M. (2019). Attention, Learn to Solve Routing Problems! ICLR 2019. Link
[2] Kwon, Y.-D., Choo, J., Kim, B., Yoon, I., Gwon, Y., & Min, S. (2020). POMO: Policy Optimization with Multiple Optima for Reinforcement Learning. NeurIPS 2020. Link
[3] Fu, Z.-H., Qiu, K.-B., & Zha, H. (2021). Generalize a Small Pre-trained Model to Arbitrarily Large TSP Instances. AAAI 2021, 35(8), 7474–7482. Link
[4] Sun, Z., & Yang, Y. (2023). DIFUSCO: Graph-based Diffusion Solvers for Combinatorial Optimization. NeurIPS 2023. Link
[5] Sanokowski, S., Hochreiter, S., & Lehner, S. (2024). A Diffusion Model Framework for Unsupervised Neural Combinatorial Optimization. ICML 2024, PMLR 235, 43346–43367. Link
[6] Chen, X., & Tian, Y. (2019). Learning to Perform Local Rewriting for Combinatorial Optimization. NeurIPS 2019. Link
[7] Hottung, A., & Tierney, K. (2022). Neural Large Neighborhood Search for Routing Problems. Artificial Intelligence, 313, 103786. Link
[8] Ye, H., Wang, J., Cao, Z., Liang, H., & Li, Y. (2023). DeepACO: Neural-enhanced Ant Systems for Combinatorial Optimization. NeurIPS 2023. Link
[9] Gasse, M., Chetelat, D., Ferroni, N., Charlin, L., & Lodi, A. (2019). Exact Combinatorial Optimization with Graph Convolutional Neural Networks. NeurIPS 2019. Link
[10] Paulus, M. B., Zarpellon, G., Krause, A., Charlin, L., & Maddison, C. (2022). Learning to Cut by Looking Ahead: Cutting Plane Selection via Imitation Learning. ICML 2022, PMLR 162, 17584–17600. Link
[11] Nair, V., Bartanov, S., Gimeno, F., et al. (2020). Solving Mixed Integer Programs Using Neural Networks. arXiv:2012.13349. (Neural Diving and Neural Branching.) Link
[12] Zhou, C., Lin, X., Wang, Z., & Zhang, Q. (2026). Learning to Reduce Search Space for Generalizable Neural Routing Solver (L2R). Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining. Link
[13] Zhou, J., Cao, Z., Wu, Y., Song, W., Ma, Y., Zhang, J., & Xu, C. (2024). MVMoE: Multi-Task Vehicle Routing Solver with Mixture-of-Experts. ICML 2024, PMLR 255, 61804–61824. Link
[14] Gao, C., Shang, H., Xue, K., & Qian, C. (2025). Neural Solver Selection for Combinatorial Optimization. ICML 2025, PMLR 267, 18528–18549. Link
[15] Berto, F., Hua, C., Zepeda, N. G., Hottung, A., Wouda, N. A., Lan, L., Park, J., Tierney, K., & Park, J. (2025). RouteFinder: Towards Foundation Models for Vehicle Routing Problems. Transactions on Machine Learning Research. Link
[16] Romera-Paredes, B., Barakaran, M., Novikov, A., et al. (2024). Mathematical Discoveries from Program Search with Large Language Models. Nature, 625, 468–475. (FunSearch.) Link
[17] Novikov, A., Vü, N., Eisenberger, M., et al. (2025). AlphaEvolve: A Coding Agent for Scientific and Algorithmic Discovery. arXiv:2506.13131. Link

LATVIJAS UNIVERSITĀTE

28

# Evolution of Heuristics (Using LMM)

https://arxiv.org/pdf/2401.02051

Performance (objective)

![img-57.jpeg](img-57.jpeg)

LUX ET VERITAS

LATVIJAS
UNIVERSITĀTE

29

"Through a unified empirical study, we reveal that while current ML methods—including both neural and LLM-based solvers—show potential, they still lag behind state-of-the-art human-designed algorithms in terms of efficiency, generalization, and scalability."

![img-58.jpeg](img-58.jpeg)

Figure 2: Primal gap (%) across eight CO problems on easy and hard sets (lower is better). Classical (blue), neural (green), and LLM-based agents (red). Bars marked with * indicate at least one infeasible run on that test set; in such cases we assign gap 1 and time 3600 seconds (see Section 3.1).

# FRONTIERCO: REAL-WORLD AND LARGE-SCALE EVALUATION OF MACHINE LEARNING SOLVERS FOR COMBINATORIAL OPTIMIZATION

Shengyu Feng* Weiwei Sun* Shanda Li Ameet Talwalker Yiming Yang
School of Computer Science, Carnegie Mellon University
{shengyuf, weiwes, shandal, atalwalk, yiming}@cs.cmu.edu

# ABSTRACT

Machine learning (ML) has shown promise for tackling combinatorial optimization (CO), but much of the reported progress relies on small-scale, synthetic benchmarks that fail to capture real-world structure and scale. A core limitation is that ML methods are typically trained and evaluated on synthetic instance generators, leaving open how they perform on irregular, competition-grade, or industrial datasets. We present FRONTIERCO, a benchmark for evaluating ML-based CO solvers under real-world structure and extreme scale. FRONTIERCO spans eight CO problems, including routing, scheduling, facility location, and graph problems, with instances drawn from competitions and public repositories (e.g., DIMACS, TSPLib). Each task provides both easy sets (historically challenging but now solvable) and hard sets (open or computationally intensive), alongside standardized training/validation resources. Using FRONTIERCO, we evaluate 16 representative ML solvers—graph neural approaches, hybrid neural-symbolic methods, and LLM-based agents—against state-of-the-art classical solvers. We find a persistent performance gap that widens under structurally challenging and large instance sizes (e.g., TSP up to 10M nodes; MIS up to 8M), while also identifying cases where ML methods outperform classical solvers. By centering evaluation on real-world structure and orders-of-magnitude larger instances, FRONTIERCO provides a rigorous basis for advancing ML for CO. Our benchmark is available at https://huggingface.co/datasets/CO-Bench/FrontierCO.

I INTRODUCTION

# Neural vs Classical (2026)

https://proceedings.idr.cc/paper_files/paper/2026/hash/c131c8875c7b1133ffdad2b53cb10e91-Abstract-Conference.html

[LOGO]

LATVIJAS
UNIVERSITÄTE

30

# Mazais praktiskais darbs!

https://agris.oranzais.lumii.lv/index.php/PKO_Piem%C4%93ri

- **Izvēlieties** un **saskaņojiet** ar pasniedzēju **uzdevumu** (piemēram, TSP, VRP, Sudoku, utml. ...).
- **Izvēlieties** optimizācijas **algoritmu** (piemēram, SA, TS, LA, utml. ...).
- **Implementējiet problēmu** un optimizācijas **algoritmu** Jūsu izvēlētā vidē (piemēram, Python, Java, C#, utml. ...).
  **!! Neizmantojiet gatavas optimizācijas algoritmu implementācijas !!**
- **Sagatavojiet** vairākus dažāda izmēra problēmu testa piemērus un **veiciet testēšanu**, piefiksējot **izpildes laiku** un **risinājuma kvalitāti, salīdzinot ar optimālo vai labāko zināmo risinājumu**.
- **Īsi (2-3 lpp.) aprakstiet** padarīto.
- **Iesniedziet** e-studijās izdarītā **aprakstu (vienu PDF failu)**, kas satur:
  1. Uzdevuma formulējumu;
  2. Uzprogrammētā aprakstu, kas ietver apakšnodāļas: a)domēns; b)novērtēšana; c)gājiens; d)algoritms;
  3. Testēšanas procesa un rezultātu aprakstu;
  4. Saiti uz Git(hub) repozitoriju, kas satur programmas kodu un testēšanas piemērus.

Termiņš ir ~3,5 nedēļas - līdz 11. oktobra plkst. 23:59.

Praktiskais darbs ir obligāts priekšnosacījums pozitīva vērtējuma saņemšanai.

LATVIJAS
UNIVERSITĀTE

31

Tas arī viss!

![img-59.jpeg](img-59.jpeg)

![img-60.jpeg](img-60.jpeg)

LATVIJAS
UNIVERSITĀTE