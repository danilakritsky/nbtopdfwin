1.  install nbconvert
    `pip install nbconvert`

2. install [pandoc](https://pandoc.org/installing.html)
    - installed at C:\Users\kdad\AppData\Local\Pandoc
    - add to PATH: export PATH=$PATH:/c/Users/kdad/AppData/Local/Pandoc/


3. download and install [MiKTeX](https://miktex.org/download)
    - installed at C:\Users\kdad\AppData\Local\Programs\MiKTeX
    - add to PATH: export PATH=$PATH:/c/Users/kdad/AppData/Local/Programs/MiKTeX/
    - !!! Reboot

4. convert file (make sure to remove all non-printable characters - otherwise the conversion will fail)
    - py -3.10 -m jupyter nbconvert --to pdf test_latex.ipynb --Application.log_level=10

    