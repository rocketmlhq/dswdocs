library(paws)
library(RMariaDB)
library(reticulate)
use_python('/opt/conda/bin/python',required = TRUE)
sm <- paws::secretsmanager(config=list(region="us-west-2"))
value <- sm$get_secret_value(SecretId = "arn:aws:secretsmanager:us-west-2:399991052688:secret:MariaDBCreds-RBiK6E")
js <- import('json')
secret_dict <- js$loads(value$SecretString)
pconn_r <- dbConnect(drv = RMariaDB::MariaDB(),
                     host = secret_dict$host,
                     port = 3306,
                     user = secret_dict$username,
                     dbname = 'rocketml',
                     password = secret_dict$password,
                     bigint = "integer")
query <- "SELECT * FROM milestones"
df <- dbGetQuery(pconn_r, statement = query)
View(df)
dbDisconnect(pconn_r)