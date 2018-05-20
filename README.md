Requirements
============
Take full control of your static website/blog generation by writing your
own simple, lightweight, and magic-free static site generator in
Python.


Content
-------

* [Feature List](#feature-list)
* [SiteMap of Blog](#sitemap-of-blog)
* [SiteMap of Build](#sitemap-of-build)
* [Process of Build](#process-of-build)
* [Links on CSS](#links-on-css)
* [Links on Python](#links-on-python)
* [Link on makesite.py](#link-on-makesite.py)


Feature List
------------
*   eigenes, simples Template System
*   responsive WebDesign
*   statische Web-Seiten
*   erweiterte Funktionalitäten nur als JavaScript im Frontend
*   so wenige Abhängigkeiten wie möglich
*   Nice-to-have: online Suche alternativ: Schlagwort-Katalog
*   Anzeige von Code-Schnipsel mit [Syntax-Highlightning](https://highlightjs.org)
*   Anzeige von Bildern
*   Anzeige von [Mathematischen Formeln](https://www.mathjax.org)
*   Generierung entspricht einem Build-Prozess, inkl. Initialisierung, CleanUp, usw.
*   Anfangs ist alles in Plain-HTML
*   später/optional ist eine Unterstützung von Markdown oder restructured Text denkbar


SiteMap of Blog
---------------
Grobe SiteMap des Static-Blog sieht wie folgt aus:
```
blog_root
├── index.html (Posts des aktuellen Monats)
├── about.html (optional)
├── impressum.html (optional)
├── keyword_catalog.html (Liste aller Schlagworte)
├── archive.html (Liste aller Monatsarchive)
├── <YYYYMM>.html (Monatsarchiv)
├── archive
│   └── <yyyymmdd_hh>.html (Blog-Artikel)
├── css (Verzeichnis)
├── js (Verzeichnis)
└── lib (Verzeichnis)
```	


SiteMap of Build
----------------
Grobe SiteMap der Build-Umgebung des Generators sieht wie folgt aus:
```
project_root
├── generator.py
├── templates
├── content
│   ├── blog
│   │   └── <yyyymmdd_hh>.html (Blog-Artikel)
│   ├── about.html (optional)
│   └── impressum.html (optional)
├── static
│   ├── css (Verzeichnis)
│   ├── js  (Verzeichnis)
│   └── lib (Verzeichnis)
├── _site (Ausgabe der fertigen Blog-Site)
└── _temp (Verzeichnis)
```	


Process of Build
----------------
Grober Ablauf des Build-Prozesses:

*   Initialisierung
*   CleanUp des letzten Builds
*   Parsen und Metadaten generieren
*   Zielverzeichnisse erstellen
*   statische Seiten und verlinkte Dateien (Bilder, PDF, usw.) kopieren
*   einzelne BlogPosts generieren
*   index.html generieren
*   archive.html generieren
*   <yyyyMM>.html generieren
*   keyword_catalog.html generieren


Links on CSS
------------
*   [Google-Search](https://www.youtube.com/results?search_query=css3+responsive+web+design)
*   [Grid CSS Responsive Website Layout - "Mobile First" Design](https://www.youtube.com/watch?v=M3qBpPw77qo)
*   [Build a Responsive Grid CSS Website Layout From Scratch](https://www.youtube.com/watch?v=moBhzSC455o)
*   [HTML5 and CSS3 Responsive design with media queries](https://www.youtube.com/watch?v=fA1NW-T1QXc)
*   [Course: Build A Blog From Scratch with CSS3 - 1](https://medium.freecodecamp.org/how-to-design-and-develop-a-beautiful-blog-from-scratch-a0cd1af46845)
*   [Course: Build A Blog From Scratch with CSS3 - 2](https://scrimba.com/g/gbuildablog)
*   [Free Images](https://www.pexels.com/)
*   [Free Icons](https://fontawesome.com/)


Links on Python
---------------
*   [Python 3 String.Template](https://docs.python.org/3/library/string.html#string.Template)
*   [Python 3 String Output-Formatting](https://docs.python.org/3/tutorial/inputoutput.html)


Link on makesite.py
-------------------
*   [Simple, lightweight, and magic-free static site/blog generator for Python coders](https://github.com/sunainapai/makesite)
