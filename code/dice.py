from flask import Flask, render_template, request, session, redirect , url_for

app = Flask(__name__)
app.secret_key = 'softwareapplicationssecret'


@app.route('/') 
def index():#redirect to index page
	return render_template('index.html')


@app.route('/login', methods=['POST']) 
def login():# get the player's name from the form,and initialize the session
    user1 = request.form['user1']
    user2=request.form['user2']
    if (user1!="") and (user2!=""):# validate the input
        session['user1'] = user1
        session['user2']=user2
        session.setdefault('turn',1) #Check if session['turn'] is none,set to 1 if so
        session.setdefault('score1',0) #Check if session['score1'] is none, set to zero if so
        session.setdefault('score2',0) #Check if session['score2'] is none, set to zero if so
        return render_template('play.html')
    else:
        error=" * Players' name can't be null." #error message
        return render_template('index.html',error=error,user1=user1,user2=user2)

@app.route('/play', methods=['POST', 'GET']) 
def play(): # Check if player's choice is 'roll' or 'hold' ,swap the turn 
   
    if request.method == 'POST':
        choice=request.form['choice']
        if choice=='ROLL': #choice is 'Roll'
            return redirect(url_for('Roll'))
        elif session['turn']==1: #choice is 'Hold'
            session['turn']=2
        else:
            session['turn']=1   
    return render_template('play.html')        

@app.route('/Roll')
def Roll():# according to the dice value to check if to clear the running score or add scores, after adding scores, check if the score reaches the winning point,return the dice value and the winner
    value=RollDice() #call RollDice method to generate a random number 
    
    winner=0
    if value==1:
        if session['turn']==1:
            session['score1']=0  #clear Player1's running score
            session['turn']=2   #swap turn to Player 2
        else:
            session['score2']=0  #clear Player2's running score
            session['turn']=1   #swap turn to Player1
    else:
        if session['turn']==1: # check if it is player1's turn
            session['score1']=session['score1']+value #add Dice value to current running score
            if session['score1']>=20: # check If that score is greater than or equal to the winning point
                winner=1
        else:
            session['score2']=session['score2']+value #add Dice value to current running score
            if session['score2']>=20: # check If that score is greater than or equal to the winning point
                winner=2
    return render_template('play.html',dice=value,winner=winner)

def RollDice():#generate a random number between 1 & 6 and return it to user
    from random import randint 
    value=randint(1,6)
    return value

@app.route('/logout') 
def logout():# clear session and redirect to the index page,allow users to re-enter their names for a new game.
    del session['user1']
    del session['user2']
    del session['score1']
    del session['score2']
    del session['turn']
    return redirect('/')


if __name__ == '__main__': 
	app.run(debug=True) 