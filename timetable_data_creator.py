import pickle
list1 = [["sun1", "sun2", "sun3", "sun4", "sun5", "sun6", "sun7"],
             ["mon1", "mon2", "mon3", "mon4", "mon5", "mon6", "mon7"],
             ["tues1", "tues2", "tues3", "tues4", "tues5", "tues6", "tues7"],
             ["wed1", "wed2", "wed3", "wed4", "wed5", "wed6", "wed7"],
             ["thurs1", "thurs2", "thurs3", "thurs4", "thurs5", "thurs6", "thurs7"]]

with open('timetable.data', 'wb') as filehandle:
    pickle.dump(list1, filehandle)