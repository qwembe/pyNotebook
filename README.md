# pyNotebook

Используется стек технологий - Python 2.7 и PyQt4

БД находится в докер образе - можно запустить скрипт ./startdb.sh на linux

### Windows
Рекомендуется скачать прекомпилированную библиотеку [PyQt4]() (https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4) и установить его -
```console

python2 -m pip install path/to/pyqt4.whl

```

### Схема БД
Создается запросом 
```sql
CREATE TABLE IF NOT EXISTS auth 
            ( Username VARCHAR(100) NOT NULL ,
              Pass VARCHAR(100) NOT NULL,
              dateob DATE NOT NULL,
              PRIMARY KEY (Username)) 
              CHARACTER SET utf8mb4
              COLLATE utf8mb4_general_ci;
            
            CREATE TABLE IF NOT EXISTS notebook 
            ( Username VARCHAR(100) NOT NULL ,
              tel VARCHAR(100) NOT NULL,
              dateob DATE NOT NULL,
              PRIMARY KEY (Username, tel , dateob))
              CHARACTER SET utf8mb4
              COLLATE utf8mb4_general_ci;
```

