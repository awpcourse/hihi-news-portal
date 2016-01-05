#News Portal

System prerequisites
--------------------

1. Install pip:

  ```
  wget https://bootstrap.pypa.io/get-pip.py
  sudo python get-pip.py
  ```

1. Install virtualenv

  ```
  sudo pip install virtualenv
  ```

Cerinte proiect
---------------

- sa existe cel putin 4 tipuri de utilizatori: vizitator neinregistrat, utilizator inregistrat, editor si administrator.
- orice utilizator poate vizualiza stirile aparute pe site. Pe pagina principala vor aparea stirile cele mai recente. Stirile vor fi impartite pe categorii (create dinamic): stiinta, tehnologie, sport, etc.
- stirile dintr-o anumita categorie sunt afisate intr-o pagina separata, unde pot fi sortate dupa diferite criterii: data aparitiei, alfabetic, etc.
- editorii se ocupa de publicarea stirilor noi. De asemenea, editorii pot prelua stiri de pe alte site-uri de stiri, specificand doar titlul, headline-ul si eventual o poza (sub forma de thumbnail).
- utilizatorii pot adauga comentarii la stirile aparute si pot propune stiri noi editorilor.
- stirile pot fi cautate prin intermediul unui motor de cautare propriu.
- administratorii pot activa sau revoca drepturile utilizatorilor si editorilor.
