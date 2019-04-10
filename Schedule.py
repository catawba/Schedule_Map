class Teacher(object):
    def __init__(self,first,last,id):
        self.first = first
        self.last = last
        self.id = id

class Course(object):
    def __init__(self,id,name,teacherid,subject,audience,allstudentclass,conflict,period,comboclass,lockperiod):
        self.id = id                    # unique identifier integer for this class
        self.name = name                # common name for this class ie Algebra II
        self.teacherid = teacherid      # id (integer) of the teacher as found in class teacher
        self.subject = subject          # ie Math, English
        self.audience = audience        # open to students in grades 9,10   this is a list
        self.allstudentclass = allstudentclass  # boolean to specifiy that all freshmen take this class during this period
        self.conflict = conflict        # list of the conflicts with other classes
        self.period = period            # period that this class is offered.  This will be the color also from map color
        self.comboclass = comboclass    # is this class connected to another class ie shop and FACS
        self.lockperiod = lockperiod    # does this class require being taught in a certain period? Boys PE

    def totalconflicts(self):
        return len(self.conflict)

def load_courses(c):
    cor = Course(1,"Algebra II", 1,"Math",[10,11],False,[2,5],"",False,False)
    c.append(cor)
    cor = Course(2,"English II",3,"English",[10,11],False,[1,5],"",False,False)
    c.append(cor)
    cor = Course(id = 3,
                 name = "American History",
                 teacherid = 2,
                 subject = "History",
                 audience = [9],
                 allstudentclass = True,
                 conflict = [6,8],
                 period = ""
                 comboclass = False,
                 lockperiod = False)

my_courses = []
load_courses(my_courses)


k = Teacher("Kyle","Canty",1)
print(k.first)
print(my_courses[0].name)