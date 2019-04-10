class Teacher(object):
    def __init__(self, name):
        self.name = name


class Course(object):
    def __init__(self, name, teacher, conflicts, color, combowith, audiance, lockperiod, allclass):
        self.name = name  # course name
        self.teacher = teacher
        self.conflicts = conflicts  # list of conflicts NEED SOME WORK HERE
        self.color = color  # integer used to represent the color of the map for this course placement
        self.combowith = combowith  # this course must be taught during the same period of another
        self.audiance = audiance  # list of integers freshmen = 9 sophomores = 10 etc
        self.lockperiod = lockperiod  # must be taught during a set period. defalult None
        self.allclass = allclass  # this class has all ie freshmen in it at the same time

    def conflict_num(self):
        return len(self.conflicts)


class Courseplace(object):
    def __init__(self, id, courseid, period, color, audiance):
        self.course = course
        self.teacher = teacher  # course-teacher
        self.period = period  # period of the day for this class
        self.audiance = audiance  # list of who can take this class Freshmen 9, Sophomores 10 etc


def add_teacher(t):
    teach = Teacher("KCanty")
    t.append(teach)
    teach = Teacher("BCanty")
    t.append(teach)
    teach = Teacher("KBond")
    t.append(teach)


def add_course(c):
    cor = Course("Calculus", "Kcanty", ["Physics", "AP English"], 0, "None", [11, 12], "None", False)
    c.append(cor)
    cor = Course("Algebra II", "Kcanty", ["World History", "English 3", "Computer Apps"], 0, "None", [10, 11, 12],
                 "None", False)
    c.append(cor)
    cor = Course("7th Science", "Bcanty", ["7th Math", "7th English"], 0, "None", [11, 12], "None", True)
    c.append(cor)
    cor = Course("AP English", "KBond", ["Physics", "Calculus"], 0, "None", [11, 12], "None", False)
    c.append(cor)


teacher = []
course = []
cplace = []

add_teacher(teacher)
add_course(course)

course.sort(key=lambda c: c.conflict_num(),reverse=True)
for n in range(len(course)):
    print(course[n].teacher, course[n].name, course[n].conflict_num())
