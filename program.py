from tinydb import TinyDB,Query
import os
import easygui as eg


# Map color program
class State:
    def __init__(self,id,name,color,borders):
        self.id = id
        self.name = name
        self.color = color
        self.borders = borders

    def total_borders(self):
        return len(self.borders)

# Map color program
class StateS:
    def __init__(self,id,name,color,borders):
        self.id = id
        self.name = name
        self.color = color
        self.borders = borders

    def total_borders(self):
        return len(self.borders)


class Color:
    def __init__(self,colornum,conflicts):
        self.colornum = colornum
        self.conflicts = conflicts


def menu():
    title = 'Color Map'
    msg = 'Select an option'
    opts = []
    dict_opts = {'Add States':'A', 'Enter Borders':'B', 'Color States':'C', 'Show States':'S',
                 'Purge Database':'P', 'Exit':'X', 'Q':'Q' }
    for key, val in dict_opts.items():
        opts.append(key)
    btn_pressed = eg.buttonbox(msg, title, opts)
    return dict_opts.get(btn_pressed)

def enter_states(db,qry):
    while True:
        n = eg.enterbox("Enter State Name: X to exit","Map Color")
        if n is not None:
           n = n.upper()
        if n == "X" or n is None:
            break
        else:
            db.insert({'name': n, 'color': 0, 'borders': []})

def read_states(db,qry):
    state = []
    for item in db:
        s = State(id=item.doc_id, name=item['name'], color=item['color'], borders=item['borders'])
        state.append(s)
    return state


def show_states(db,qry):
    msg = 'Id  Name  Color  Conflicts'
    title = 'Map Color'
    text = ''
    for item in db:
        text = text + str(item.doc_id)+\
               ' '+item['name']+' '+str(item['color']) + ' ' + ''.join(str(item['borders'])+'\n')
    eg.textbox(msg, title, text)

def purge_db(db,qry):
    db.purge()

def xqspecial(db,qry,wstate,wborders):
    # update_border(db,qry,wstate,wborders)
    """db and qry are from the database, wstate is the working state, wborders are
    the working borders"""
    for wb in wborders:
        result = db.get(qry.doc_id == wb)
        if result is not None:
            print(result)


def read_states_for_borders(db, qry):
    state = []
    for item in db:
        s = State(id=item.doc_id, name=item['name'], color=item['color'], borders=set(item['borders']))
        state.append(s)
    return state




def oldenter_borders(db,qry):
    map = read_states_for_borders(db,qry)
    title = "Map Color"
    state_set = set()
    state_dict = dict()
    state_dict_name_id = dict()
    state_dict_borders = dict()
    for state in map:
        # make a set of the state names to be used to build the
        # borders to be checked against
        state_set.add(state.id)
        state_dict[state.id] = state.name
        state_dict_name_id[state.name] = state.id

 ########       #this is to be used to update the borders list for selected states
        #it puts co into nm when nm is selected as a border for co
        #this does not work yet. The dictionary is not used yet.
        state_dict_borders[state.name] = state.borders

    for state in map:
        # get available states to check for borders
        border_states_available = state_set.difference(state.borders)
        s_id = state.id
        s_name = state.name
        tlist = []  # make a list of border states available
        for b_id in border_states_available:
            s_n = state_dict[b_id]
            tlist.append(s_n)

        tlist.remove(s_name)  # don't enter a border with itself
        msg = "Enter Borders for " + s_name
        nlist = eg.multchoicebox(msg, title, tlist)
        if nlist is not None:
            dlist = set()
            for n in nlist:
                """create a set of borders for this state"""
                s = state_dict_name_id[n]
                dlist.add(s)


            # update this states borders
            state.borders = state.borders | dlist
            # update the borders for this state
            db.update({'borders': list(dlist)}, doc_ids = [s_id])



def enter_borders(db,qry):
    title = "Map Color"
    state_set = set()
    state_dict = dict()
    for state in db:
        # make a set of the state names
        state_set.add(state.doc_id)
        state_dict[state.doc_id]=state['name']

    for state in db:
        # make a set of the borders
        border_set = set(state['borders'])
        border_states_available = state_set.difference(border_set)
        #print('borders available: ',border_states_available)
        s_id = state.doc_id
        s_name = state['name']
        tlist = []  # make a copy of the borders list, not an alias to the borders list
        for b_id in border_states_available:
            s_n = state_dict[b_id]
            tlist.append(s_n)

        tlist.remove(s_name)  # don't enter a border with itself
        msg = "Enter Borders for " + s_name
        nlist = eg.multchoicebox(msg, title, tlist)
        #print(nlist, 'nlist')
        if nlist is not None:
            dlist = []
            for n in nlist:
                s = db.get(qry.name == n)
                dlist.append(s.doc_id)
            # update the borders for this state
            db.update({'borders': dlist}, doc_ids = [s_id])
            # update the borders for this state
            # update the states that this state borders
            for d in dlist:
                s = db.get(doc_id = d)
                if s is not None:
                    border_set = set(s['borders'])
                    border_set.add(state.doc_id)
                    blist = list(border_set)
                    db.update({'borders': blist}, doc_ids = [d])
                else:
                    print('state not found')

def sort_states_by_borders(state):
    """ Input list of states into state
        Output the same list but sorted by the total borders"""
    state.sort(key=lambda c: c.total_borders(),reverse=True)
    return state

def color_states(db,qry):
    # read db into working list
    map = read_states(db,qry)
    map = sort_states_by_borders(map)

    # BLANK out the coloring so a new coloring can be done
    for state in map:
        state.color = 0

    # con is [color],[list of states this color]
    con = []
    conadd = Color(1, map[0].borders)
    con.append(conadd)
    last_colornum = 1
    for state in map:
        for chk in con:
            if state.id not in chk.conflicts:
                state.color = chk.colornum
                chk.conflicts.extend(state.borders)
                break

        # state has not been colored by any previous colors so a new color is needed
        if state.color == 0:
            last_colornum += 1
            state.color = last_colornum
            conadd = Color(last_colornum, state.borders)
            con.append(conadd)

    #for state in map:
    #   print(state.name,state.color)

    # make changes permanent
    for s in map:
        s_id = []
        s_id.append(s.id)
        db.update({'color': s.color}, doc_ids=s_id)

def wqspecial(db,qry):
#--------------------------------------problem with qspecial
    state_to_edit = State(0,' ',0,[])
    state_list = []
    for item in db:
        state_list.append(item.doc_id,item.name,item.color,item.borders)
        print(item['name'])
    s = db.get(qry.name=='CO')
    print('document id for CO',s.doc_id)


def open_database(dbname):
    filename = os.path.join(os.path.abspath('.'), 'States', dbname + '.json')
    the_db = TinyDB(filename)
    the_qry = Query()
    return the_db,the_qry


def close_database(db):
    db.close()


def main():
    dbname = 'state_data'
    db,qry = open_database(dbname)
    #remove_state()
    #add_state_to_existing_map()
    #edit_state_borders()
    #reciprocal_state_borders()
    #print_states_by_color()
    while True:
        #action = print_menu()
        action = menu()
        if action == 'X':
            close_database(db)
            break
        elif action == 'A':
            enter_states(db,qry)
        elif action == 'B':
            enter_borders(db,qry)
        elif action == 'C':
            color_states(db,qry)
        elif action == 'S':
            show_states(db,qry)
        elif action == 'P':
            purge_db(db,qry)
        elif action == 'Q':
            oldenter_borders(db,qry)


states = []
main()
