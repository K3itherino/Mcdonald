
from tkinter import N
from managment import accmanag
import sqlite3 as sql
from distutils.log import debug
from urllib import request
from flask import Flask, render_template, request, redirect, session, flash

app= Flask(__name__)
database = accmanag("clients.db")
app.secret_key = "cacac"  
products = accmanag("products.db")              





@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    
    
    if request.method == 'POST':
        
        if request.form["user"] and request.form["user"]:
            
            username = request.form["user"]
            password = request.form["pw"]
            
            find = database.findusername("users", username)
            
            if find:
                
                return redirect("http://127.0.0.1:5000/error")
                

                
            elif not find:
                
                
        
                database.insertRow(username, password, "users")
                
                return redirect("http://127.0.0.1:5000/login")
    
    elif request.method == 'GET':
        
        return render_template("signup.html")

@app.route("/error", methods =  ['POST', 'GET'])

def error():
    
    if request.method == 'GET':
        return render_template("error.html")
    
    elif request.method == 'POST':
        return redirect("http://127.0.0.1:5000/signup")


        
            
    

@app.route("/login", methods = ['GET', 'POST'])

def login():
    
    if request.method == 'GET':
        if "user" in session:
            return redirect("http://127.0.0.1:5000/profile")
        else:
            return render_template("login.html")
    
    elif request.method == 'POST':
        
        username = request.form['user-id']
        password = request.form['password']

        user = database.findusername('users', username)
        pass_ = database.findpassword('users', username)         
        
        
        
        if user:
            
            if  pass_[0] == password:
                
                session["user"] = username
                
                return redirect("http://127.0.0.1:5000/")
            
            else:
                
                return redirect("http://127.0.0.1:5000/error")
        
        if not user:
            return redirect("http://127.0.0.1:5000/error")

@app.route("/profile", methods = ['POST', 'GET'])
def profile_():
    if request.method == 'GET':
        
        if "user" in session:
            c=database.read("users", session["user"])
            priceN = c[0]*5
            priceS = c[1]*10
            total = priceN + priceS
  


            
            
        
  
            return render_template("profile.html", MenuNormal = str(c[0]), MenuEspecial = c[1], 
        priceN = priceN, priceS = priceS, total = total, profile = session["user"]
        )
        
        
        else:
            return redirect("/error")
    
    
    elif request.method == 'POST':

            
            try:
                food = request.form['menjar']
                num = request.form['num']
                database.updatemenu("users", session["user"], num, food)
                return redirect("/profile")
            except:
                elim = request.form["elim1"]
                elim2 = request.form["elim2"]
                c = database.read("users", session["user"])
                if elim:
                    try:
                        elim = int(elim)
                        
                        if c[0]-elim < 0:
                            elim = c[0]
                    except:
                        elim = "0"
                else:
                    elim= c[0]
                if elim2:
                    try:
                        elim2 = int(elim2)
                        
                        if c[1]-elim < 0:
                            elim2 = c[1]
                    except:
                        elim2 = "0"
                else:
                    elim2=c[1]
                database.updatemenu("users", session["user"], -int(elim), "burger")
                database.updatemenu("users", session["user"], -int(elim2), "cheeseburger")
                return redirect("/profile")
         
@app.route("/menu/normal")
def normal():
    return render_template("menunormal.html")       
@app.route("/menu/especial")
def especial():   
    if request.method == 'GET':
        return render_template("menuespecial.html")
@app.route("/checkout", methods = ['GET' , 'POST'])
def checkout():
    
    if request.method == 'GET':
        c = database.read("users", session["user"])
        return render_template("checkout.html", menu = c[0], especial = c[1])
    
    elif request.method =='POST':
        
        c = database.read("users", session["user"])
        
        if c[0] != 0:
            id = products.createid("pedido")
            products.insertProduct("pedido", session["user"], "burger", c[0], (id[0]+1))
            database.updatemenu("users", session["user"], -(c[0]), "burger")
        
        if c[1] != 0:
            id = products.createid("pedido")
            products.insertProduct("pedido", session["user"], "cheeseburger", c[1], (id[0]+1))
            database.updatemenu("users", session["user"], -(c[1]), "cheeseburger")
        return redirect("/profile")
@app.route("/pedidos", methods = ["GET", 'POST'])
def pedidos():
        if "user" in session:
            if request.method == 'GET':
                product = products.read_buy("pedido", session["user"])
                return render_template("pedidos.html", productos_ = product)
            elif request.method == 'POST':
                elim = request.form["eliminar"]
                products.delete("pedido", elim)
                return redirect("/pedidos")

        else:
            return render_template("error.html")
            
        
            
      
        

            
        
@app.route("/logout")
def logout():
    
    session.pop("user", None)
    return redirect("http://127.0.0.1:5000/login")

    
    
if __name__ == "__main__":
    app.run(debug=True)