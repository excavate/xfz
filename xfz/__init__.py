# import MySQLdb #解决mysqlclient版本过低问题

import pymysql
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()