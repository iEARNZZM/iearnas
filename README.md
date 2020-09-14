# Iearn svetainė su backendu

Komplikuotas, bet ŽIAURIAI lengvas būdas gauti galvos skausmą

Dėl pagalbos kreipkitės į Justą.

## Kaip paleisti tinklapį savo kompiuteryje
> **NEPLATINKITE NIEKUR ŠIO KODO!**  
> (_Cmd_ - tai komandinė eilutė)

Norint paleisti tinklapį kompiuteryje, būtina parsisiųsti Git  
https://git-scm.com/downloads

* ### Instaliuotis Python3 ###

    Jeigu Python3 dar neturite, jį parsisiusti galima [čia](https://www.python.org/downloads/).

* ### Parsisiųsti šia repozitoriją ###

    * **Tai galima padaryti per šia svetaine tiesiogiai:**
    
        Nueiti į repozitorijos pradzia -> paspausti ant  'Code' -> paspausti ant 'Dowload Zip'.
    * **Arba galima parsisiusti naudojant `git` komandą:**
    
        Atsidarykite Cmd pasiriktame aplankale ir įrašykite komandą:
        ```
        git clone --single-branch --branch Backend https://github.com/iEARNZZM/iearnas.git
        ```
* ### Atidarykite "iearn_web" aplankalą Cmd ###
    ```
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
    
    Norint išjungti serveri paspauskite `ctrl` + `c`
    
# Baigta!

        
    
