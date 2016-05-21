#!/usr/bin/env python
import sqlite3 as lite
import sys

con = lite.connect('tweet.db')

with con:
	cur = con.cursor()
	cur.execute("SELECT * FROM Player")

	rows = cur.fetchall()


	# MSG = open('msg.txt', 'r').read()
	TITLE = 'SPACE DRIFT'

	htmlF = open('index.html', 'w')

	htmlF.write('''
<!DOCTYPE html>

<html>
<head>
	<meta charset="utf-8">
	<title>SPACE DRIFT</title>
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
    <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
    <link href="css/main.css" rel="stylesheet" type="text/css">	
</head>		

<body>
    <header>
        <h1>SPACE DRIFT</h1>
    </header>
    
    <div class="empty"></div>
    
    <div class="inner">
        <div class="row">
            <div class="col-md-8"></div>
            <div class="col-md-4" align="right"><a href="https://twitter.com"><img src="image/twii.png" onmouseover="this.src='image/twitter.png'" onmouseout="this.src='image/twii.png'" /></a></div>
        </div>
        
        <h2>Story</h2>
        <p>The last thing you remember before awaking from chryostasis, is the captain being decapitated by some flying debris. There was a battle. You don't know if the enemy was destroyed, but obviously your ship is intact. The onboard computer reports that you have been in stasis for 345 years. The ship has been drifting the entire time.
        <br><br>
        You are 81000 light years from home, but the solar sails are functional.
        <br><br>
        You may return to stasis and allow the ship to drift at any time. Or, if you have fuel, you can head toward home. Perhaps one of these nearby planets has something interesting.</p>
        
        <br><br><br>
        
        <h2>Result</h2>

        <!-- Important Table -->
        <table class="table table-striped table-hover">
            <tr>
                <th>#</th>
                <th>User Name</th>
                <th>Date &amp; Time</th>
                <th>Success</th>
                <th>Success Total</th>
            </tr>
		''')



	for row in rows:
		htmlF.write('''
			<tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>
            ''' % (row[0], row[1], row[2], row[3], row[4]))

	htmlF.write('''
	   </table>
    </div> 

    <div class="emptyBot"></div>
    <footer>
        <h3>Twitter Bot---></h3>
    </footer>    
    
</body>    
</html>
	''')

con.close()