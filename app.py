from flask import Flask,render_template,request
import csv
import pandas as pd

app = Flask(__name__)

class Students:

    def Register(self, studentID, studentName, gender, dob, city, state, studentEmail, qualification, stream):
        self.studentID=studentID
        self.studentName=studentName
        self.gender=gender
        self.dob=dob
        self.city=city
        self.state=state
        self.studentEmail=studentEmail
        self.qualification=qualification
        self.stream=stream
        with open('students.csv', mode='a',newline='') as students:
            colleges_writer = csv.writer(students, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            colleges_writer.writerow([self.studentID,self.studentName,self.gender,self.dob,self.city,self.state,self.studentEmail,self.qualification, self.stream])

    def Display(self):
        clg = pd.read_csv('students.csv', header=None,names=['Student_ID', 'Student_Name', 'Gender', 'DoB', 'City', 'State', 'Student_Email','Qualification', 'Stream'])
        clg.set_index('Student_ID')
        return clg


    def Filter(self, id):
        self.id=id
        list=[self.id]
        clg = pd.read_csv('students.csv', header=None, names=['Student_ID', 'Student_Name', 'Gender', 'DoB', 'City', 'State', 'Student_Email','Qualification', 'Stream'])
        clg.set_index('Student_ID')
        return clg[clg.Student_ID.isin(list)]
        # return clg.values.tolist()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        studentID = request.form['id']
        studentName = request.form['name']
        gender = request.form['gender']
        dob = request.form['dob']
        city = request.form['city']
        state = request.form['state']
        studentEmail = request.form['email']
        qualification = request.form['qualification']
        stream = request.form['stream']
        clgreg = Students()
        clgreg.Register(studentID,studentName,gender,dob,city,state,studentEmail,qualification,stream)
        return render_template("index.html", alert='Student ID '+studentID+' Successfully Registered!')
    return render_template("add_student.html")

@app.route("/display", methods=["GET", "POST"])
def display():
    clgdel = Students()
    try:
        x = clgdel.Display()
    except(FileNotFoundError):
        return render_template("display.html", info="No record.")
    return render_template("display.html", column_names=x.columns.values, row_data=list(x.values.tolist()))

@app.route("/search", methods=["GET", "POST"])
def filter_display():
    if request.method == "POST":
        studentID=request.form['studentId']
        clgfilt=Students()
        try:
            x=clgfilt.Filter(studentID)
        except(FileNotFoundError):
            return render_template("search_id.html", info="No record.")
        row = list(x.values.tolist())
        if not row:
            return render_template("search_id.html", info="No data found.")
        else:
            row = row[0]
            return render_template("search_id.html", header=None, length=len(row), column_names=x.columns.values, row_data=row)
    return render_template("search_id.html")

if __name__ == "__main__":
    app.run()
