![alt tag](https://github.com/dfbacon/AirBnB_clone/blob/master/web_static/images/logo.png)

Holberton School AirBnB Clone Project (v3)
==========================================

The purpose of this project is to recreate the AirBnB site, from the back-end data management to the front-end user interface.

The end product will have:
* A website to display the final product
* An API that provides a communication interface between the front-end and your data
* A database or files that store data
* A command interpreter to manipulate data without a visual interface

Usage
-----
To run, execute the console.py script:
* ```python3 console.py``` or ```./console.py```

<h4>Valid Classes:</h4>
* Amenity
* BaseModel
* City
* Place
* Review
* State
* User

<h4>Base Commands</h4>
	 * create: Create an instance.
	     -> **create <class name>**
	     -> **<class name>.create(<key>=<value>)**

	 * all: Display all instances of a class.
	     -> **all <class name>**
	     -> **<class name>.all()**

	 * show: Show information about a specific object.
	     -> **show <class name> <unique id>**
	     -> **<class name>.show(<unique id>)**

	 * update: Update an instance of a class.
	     -> **update <class name> <unique id> <attribute name> <attribute value>**
             -> **<class name>.update(<unique id>, <attribute name>, <attribute value>)**
             -> **<class name>.update(<unique id>, <dictionary representation>)**

	 * destory: Destroy an instance of a class.
	     -> **destroy <class name> <unique id>**
	     -> **<class name>.destroy(<unique id>)**

	 * quit: Exit the program.
	     -> **quit**

<h4>Additional Commands</h4>
	 * count: Count and display the number of instances of a given class.
	     -> **<class name>.count()**

Versions
--------
<h4>Second Phase</h4>
Command line interpretor can now save objects into a mysql database by setting the following environmental variables:

	* MySQL user = <HBNB_MYSQL_USER>
        * MySQL password = <HBNB_MYSQL_PWD>
        * MySQL host = <HBNB_MYSQL_HOST> (typically = localhost)
        * MySQL database = HBNB_MYSQL_DB
        * HBNB_TYPE_STORAGE = db

<h4>First Phase</h4>
Creation of command line interpreter to access objects that will store user data. Users can use the console to create objects, update object attributes, remove objects, list all objects, and store and read data from a .json file.

Project Requirements
--------------------
<h4>Python Requirements</h4>
* All programs are compiled Ubuntu 14.04 LTS using python3 (version 3.4.3)
* All code conforms to [PEP 8] (https://www.python.org/dev/peps/pep-0008/)
* All your modules should have documentation
      ```python3 -c 'print(__import__("my_module").__doc__)'```

* All your classes should have documentation
      ```python3 -c 'print(__import__("my_module").MyClass.__doc__)'```

* All your functions (inside and outside a class) should have documentation
      ```python3 -c 'print(__import__("my_module").my_function.__doc__)'```

      and
      ```python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'```

<h4>Unit Test Requirements</h4>
* Must use [unittest] (https://docs.python.org/3.4/library/unittest.html#module-unittest) module
* All test files inside ```tests``` folder
* All tests execute with
      ```python3 -m unittest discover tests```

* Ability to test file by file
      ```python3 -m unittest tests/test_models/test_base_model.py```

* Must follow documentation requirements listed above.

Authors
-------
**Philip Yoo**, \<philip.yoo@holbertonschool.com>, @philipYoo10
**Jianqin Wang**, \<jianqin.wang@holbertonschool.com>, @jianqinwang94
**Anne Cognet**, \<anne.cognet@holbertonschool.com>, @1million40
**Richard Sim**, \<richard.sim@holbertonschool.com>, @rdsim8589
[**Daniel Bacon**](https://github.com/dfbacon), \<dbacon338@gmail.com>, @dbacon338
