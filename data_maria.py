import sqlite3
con = sqlite3.connect("""D:/Maria/آمار/پروژه/final_program_of_minesweeper_bot/useful_data.db""")
#con_2= sqlite3.connect("D:/Maria/آمار/پروژه/Maria/maria.db", check_same_thread=False)
cur = con.cursor()
#cur_2=con_2.cursor()
ids=cur.execute(f"SELECT id FROM players").fetchall()
#print(ids)
cur.execute(f"SELECT * FROM players")
col_name=[i[0] for i in cur.description]
#print(col_name)
for i in ids:
#    print(i[0])
    id_info = cur.execute(f"SELECT * FROM players WHERE id = {i[0]}").fetchall()[0]
#    print(id_info)
    for j in id_info:
        if j==None:
            cur.execute(f"DELETE FROM players WHERE id={i[0]}")
            break
con.commit()
#con_2.commit()







#a=cur.execute(f"SELECT wins FROM our_data WHERE id = {123}").fetchall()
#cur.execute(f'INSERT INTO our_data(wins) VALUES({123})')
#cur.execute(f"UPDATE our_data SET year = '{(1,2)}' WHERE id = {123}")
#cur.execute(f"DELETE FROM our_data WHERE id={123}")
#cur.execute(f"DELETE FROM our_data WHERE wins={123}")
#print(a)

#sql = '''SELECT `id`, `gender`, `level`
#            FROM `players` WHERE `id` =77723901 '''
#print(sql)

#for i in ids:
#con.row_factory = sqlite3.Row



#a=cur.execute(f"SELECT * FROM players WHERE id = {6004467335}").fetchall()
#a=a[0]
#print(type(a))
#print(a)
#if a[0]==None:
#    print("yes")
#else:
#    print("no")
