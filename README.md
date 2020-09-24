# Iearn svetainė su backendu

Komplikuotas, bet ŽIAURIAI lengvas būdas gauti galvos skausmą

Dėl pagalbos kreipkitės į Justą.

## Kaip paleisti tinklapį savo kompiuteryje
> **NEPLATINKITE NIEKUR ŠIO KODO!**  
> (_Cmd_ - tai komandinė eilutė)
> Komados bus atliekamos komandinėje eilutėje

*   ### Norint paleisti tinklapį kompiuteryje, būtina parsisiųsti Git:  ###
    https://git-scm.com/downloads

* ### Instaliuotis Python3 ###

    Jeigu Python3 dar neturite, jį parsisiusti galima [čia](https://www.python.org/downloads/).

* ### Parsisiųsti šia repozitoriją naudojant `git` komandą ###
    > Parsisiųsti šios repozitorijos .zip failo negalima, nes taip Git komandos neveiks.
    Atsidarykite Cmd pasiriktame aplankale ir įrašykite komandą:
    ```
    git clone https://github.com/iEARNZZM/iearnas.git
    ```
* ### Atidarykite "iearn_web" aplankalą Cmd ###
    ```
    git branch Backend
    cd iearn_web
    ```
* ### Instaliuokite "bibliotekas" skirtas tinklapiui ###
    ```
    pip install -r requirements.txt
    ```
    Jei komanda neveikia, pasitikrinkite ar buvo automatiskai instaliuotas `pip` kartu su Python.
* ### Paleiskite tinklapį ###
    Paleskite serverį ir kodą kompiuteryje:
    ```
    python run.py
    ```
    Toliau Naršyklėje atsidarykite tinklapį:  
    Nuoroda turetų būti http://127.0.0.1:5000/
    
    Norint išjungti serveri Cmd lange paspauskite `ctrl` + `c`
    
# Baigta!