from tkinter import *
import time
import sqlite3
import random
import tempfile

f = ''
flag = ''
flags = ''

login = sqlite3.connect("admin.db")
l = login.cursor()

c = sqlite3.connect("medicine.db")
cur = c.cursor()

columns = ('Sl No', 'Name', 'Type', 'Quantity Left', 'Cost', 'Purpose', 'Expiry Date', 'Rack location', 'Manufacture')


def open_win(): #tampilan awal admin
    global apt, flag
    flag = 'apt'
    apt = Tk()
    apt.title("TOKO OBAT GENESIS")
    Label(apt, text="TOKO OBAT GENESIS").grid(row=0, column=0, columnspan=3)
    Label(apt, text='*' * 80).grid(row=1, column=0, columnspan=3)
    Label(apt, text='-' * 80).grid(row=3, column=0, columnspan=3)

    Label(apt, text="Stock Maintenance", bg='green', fg='white').grid(row=2, column=0)
    Button(apt, text='Tambah produk ke Stok', bg='green', fg='white', width=25, command=stock).grid(row=4, column=0)
    Button(apt, text='Hapus produk dari stok', bg='green', fg='white', width=25, command=delete_stock).grid(row=6, column=0)

    Label(apt, text="Access Database", bg='blue', fg='white').grid(row=2, column=2)
    Button(apt, text='Cari', width=15, bg='blue', fg='white', command=search).grid(row=5, column=2)

    Button(apt, text='Logout', bg='red', fg='white', width=10, command=again).grid(row=5, column=4)
    apt.mainloop()


def delete_stock(): #untuk menghapus produk dari database
    global cur, c, flag, lb1, d
    apt.destroy()
    flag = 'd'
    d = Tk()
    d.configure(background='yellow')
    d.title("Hapus Produk dari stok")
    Label(d, text='', width=30, bg='yellow').grid(row=0, column=1)
    Label(d, text='Produk', bg='yellow').grid(row=0, column=0)
    Label(d, text='Qty.     Exp.dt.     Harga                           ', bg='yellow').grid(row=0, column=1)
    ren()
    b = Button(d, width=10, text='Delete', bg='red', fg='white', command=delt).grid(row=1, column=3)
    b = Button(d, width=15, text='Main Menu', bg='green', fg='white', command=main_menu).grid(row=3, column=3)
    d.mainloop()


def ren(): #hanya tampilan
    global lb1, d, cur, c

    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)

    def onmousewheel():
        lb1.ywiew = ('scroll', event.delta, 'units')
        lb2.ywiew = ('scroll', event.delta, 'units')
        return 'break'

    cx = 0
    vsb = Scrollbar(orient='vertical', command=onvsb)
    lb1 = Listbox(d, width=25, yscrollcommand=vsb.set)
    lb2 = Listbox(d, width=30, yscrollcommand=vsb.set)
    vsb.grid(row=3, column=2, sticky=N + S)
    lb1.grid(row=3, column=0)
    lb2.grid(row=3, column=1)
    lb1.bind('<MouseWheel>', onmousewheel)
    lb2.bind('<MouseWheel>', onmousewheel)
    cur.execute("select *from med")
    for i in cur:
        cx += 1
        s1 = [str(i[0]), str(i[1])]
        s2 = [str(i[3]), str(i[6]), str(i[4])]
        lb1.insert(cx, '. '.join(s1))
        lb2.insert(cx, '   '.join(s2))
    c.commit()
    lb1.bind('<<ListboxSelect>>', sel_del)


def sel_del(e): #penghapusan data yang ada di database
    global lb1, d, cur, c, p, sl2
    p = lb1.curselection()
    print(p)
    x = 0
    sl2 = ''
    cur.execute("select * from med")
    for i in cur:
        print(x, p[0])
        if x == int(p[0]):
            sl2 = i[0]
            break
        x += 1
    c.commit()
    print(sl2)
    Label(d, text=' ', bg='white', width=20).grid(row=0, column=1)
    cur.execute('Select * from med')
    for i in cur:
        if i[0] == sl2:
            Label(d, text=i[0] + '. ' + i[1], bg='white').grid(row=0, column=1)
    c.commit()


def delt(): #penghapusan di database
    global p, c, cur, d
    cur.execute("delete from med where sl_no=?", (sl2,))
    c.commit()
    ren()


def res():
    global st, up
    up = Entry(st)
    up.grid(row=2, column=2)
    Label(st, width=20, text='                         ').grid(row=5, column=i)


def sel_mn(e):
    global n, name_, name_mn, sl, c, cur
    name_mn = ''
    p = name_.curselection()
    print(p)
    x = 0
    sl = ''
    cur.execute("select * from med")
    for i in cur:
        print(x, p[0])
        if x == int(p[0]):
            sl = i[0]
            break
        x += 1
    c.commit()
    print(sl)
    name_nm = n[int(sl)]
    print(name_nm)


def stock(): #menginput produk
    global cur, c, columns, accept, flag, sto, apt
    apt.destroy()
    flag = 'sto'
    accept = [''] * 10
    sto = Tk()
    sto.configure(background='yellow')
    sto.title('STOCK ENTRY')
    Label(sto, text='ENTER NEW PRODUCT DATA TO THE STOCK', bg='yellow').grid(row=0, column=0, columnspan=2)
    Label(sto, text='-' * 50, bg='yellow').grid(row=1, column=0, columnspan=2)
    for i in range(1, len(columns)):
        Label(sto, width=15, text=' ' * (14 - len(str(columns[i]))) + str(columns[i]) + ':', bg='yellow').grid(row=i + 2, column=0)
        accept[i] = Entry(sto)
        accept[i].grid(row=i + 2, column=1)
    Button(sto, width=15, text='Submit', bg='blue', fg='white', command=submit).grid(row=12, column=1)
    Label(sto, text='-' * 165, bg='yellow').grid(row=13, column=0, columnspan=7)
    Button(sto, width=15, text='Reset', bg='red', fg='white', command=reset).grid(row=12, column=0)
    Button(sto, width=15, text='Refresh stock', bg='skyblue', fg='black', command=ref).grid(row=12, column=4)
    for i in range(1, 6):
        Label(sto, text=columns[i], bg='yellow').grid(row=14, column=i - 1)
    Label(sto, text='Exp     Rack      Manufacture        ', bg='yellow').grid(row=14, column=5)
    Button(sto, width=10, text='Main Menu', bg='green', fg='white', command=main_menu).grid(row=12, column=5)
    ref()
    sto.mainloop()


def ref(): #tampilan
    global sto, c, cur

    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)
        lb3.yview(*args)
        lb4.yview(*args)
        lb5.yview(*args)
        lb6.yview(*args)

    def onmousewheel():
        lb1.ywiew = ('scroll', event.delta, 'units')
        lb2.ywiew = ('scroll', event.delta, 'units')
        lb3.ywiew = ('scroll', event.delta, 'units')
        lb4.ywiew = ('scroll', event.delta, 'units')
        lb5.ywiew = ('scroll', event.delta, 'units')
        lb6.ywiew = ('scroll', event.delta, 'units')

        return 'break'

    cx = 0
    vsb = Scrollbar(orient='vertical', command=onvsb)
    lb1 = Listbox(sto, yscrollcommand=vsb.set)
    lb2 = Listbox(sto, yscrollcommand=vsb.set)
    lb3 = Listbox(sto, yscrollcommand=vsb.set, width=10)
    lb4 = Listbox(sto, yscrollcommand=vsb.set, width=7)
    lb5 = Listbox(sto, yscrollcommand=vsb.set, width=25)
    lb6 = Listbox(sto, yscrollcommand=vsb.set, width=37)
    vsb.grid(row=15, column=6, sticky=N + S)
    lb1.grid(row=15, column=0)
    lb2.grid(row=15, column=1)
    lb3.grid(row=15, column=2)
    lb4.grid(row=15, column=3)
    lb5.grid(row=15, column=4)
    lb6.grid(row=15, column=5)
    lb1.bind('<MouseWheel>', onmousewheel)
    lb2.bind('<MouseWheel>', onmousewheel)
    lb3.bind('<MouseWheel>', onmousewheel)
    lb4.bind('<MouseWheel>', onmousewheel)
    lb5.bind('<MouseWheel>', onmousewheel)
    lb6.bind('<MouseWheel>', onmousewheel)
    cur.execute("select *from med")
    for i in cur:
        cx += 1
        seq = (str(i[0]), str(i[1]))
        lb1.insert(cx, '. '.join(seq))
        lb2.insert(cx, i[2])
        lb3.insert(cx, i[3])
        lb4.insert(cx, i[4])
        lb5.insert(cx, i[5])
        lb6.insert(cx, i[6] + '    ' + i[7] + '    ' + i[8])
    c.commit()


def reset(): #untuk reset pengisian penambahan produk
    global sto, accept
    for i in range(1, len(columns)):
        Label(sto, width=15, text=' ' * (14 - len(str(columns[i]))) + str(columns[i]) + ':').grid(row=i + 2, column=0)
        accept[i] = Entry(sto)
        accept[i].grid(row=i + 2, column=1)


def submit(): #submit produk yang akan diinput dan akan masuk kedalam database
    global accept, c, cur, columns, sto, y

    x = [''] * 10
    cur.execute("select * from med")
    for i in cur:
        y = int(i[0])
    for i in range(1, 9):
        x[i] = accept[i].get()
    sql = "insert into med values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
    y + 1, x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8])
    cur.execute(sql)
    cur.execute("select * from med")
    c.commit()

    top = Tk()
    Label(top, width=20, text='Berhasil!').pack()
    top.mainloop()
    main_menu()


def exp_date(): #memeriksa expired date dari obat
    global exp, s, c, cur, flag, apt, flags
    apt.destroy()
    flag = 'exp'
    from datetime import date
    now = time.localtime()
    n = []
    cur.execute("select *from med")
    for i in cur:
        n.append(i[1])
    c.commit()
    exp = Tk()
    exp.configure(background='pink')
    exp.title('EXPIRY CHECK')
    Label(exp, text='Today : ' + str(now[2]) + '/' + str(now[1]) + '/' + str(now[0]), bg='pink').grid(row=0, column=0,
                                                                                           columnspan=3)
    Label(exp, text='Menjual Obat Kadaluarsa adalah hal yang terlarang!', bg='pink').grid(row=1, column=0, columnspan=3)
    Label(exp, text='-' * 80, bg='pink').grid(row=2, column=0, columnspan=3)
    s = Spinbox(exp, values=n)
    s.grid(row=3, column=0)
    Button(exp, text='Check Expiry date', bg='red', fg='white', command=s_exp).grid(row=3, column=1)
    Label(exp, text='-' * 80, bg='pink').grid(row=4, column=0, columnspan=3)
    if flags == 'apt1':
        Button(exp, text='Main Menu', bg='green', fg='white', command=main_cus).grid(row=5, column=2)
    else:
        Button(exp, width=20, text='Check Products expiring', bg='red', fg='white', command=exp_dt).grid(row=5,
                                                                                                         column=0)
        Button(exp, text='Main Menu', bg='green', fg='white', command=main_menu).grid(row=5, column=2)
    exp.mainloop()


def s_exp(): #untuk menampilkan expired date
    global c, cur, s, exp, top
    from datetime import date
    now = time.localtime()
    d1 = date(now[0], now[1], now[2])
    cur.execute("select * from med")
    for i in cur:
        if (i[1] == s.get()):
            q = i[6]
            d2 = date(int('20' + q[8:10]), int(q[3:5]), int(q[0:2]))
            if d1 > d2:
                Label(exp, text='EXPIRED! on ' + i[6], bg='pink').grid(row=3, column=2)
                top = Tk()
                top.configure(background='pink')
                Label(top, text='EXPIRED!', bg='pink').pack()
            else:
                Label(exp, text=i[6], bg='pink').grid(row=3, column=2)
    c.commit()



def search(): #untuk mencari obat
    global c, cur, flag, st, mn, sym, flags
    flag = 'st'
    apt.destroy()
    cur.execute("Select * from med")
    symp = ['nil']
    med_name = ['nil']
    for i in cur:
        symp.append(i[5])
        med_name.append(i[1])
    st = Tk()
    st.geometry('450x200')
    st.configure(background='yellow')
    st.title('SEARCH')
    Label(st, bg='green', fg='white', text=' SEARCH FOR MEDICINE ').grid(row=0, column=0, columnspan=3)
    Label(st, text='~' * 55, bg='yellow').grid(row=1, column=0, columnspan=3)
    Label(st, text='Nama Gejala', bg='yellow').grid(row=3, column=0)
    sym = Spinbox(st, values=symp)
    sym.grid(row=3, column=1)
    Button(st, width=15, text='Search', bg='blue', fg='white', command=search_med).grid(row=3, column=2)
    Label(st, text='-' * 80, bg='yellow').grid(row=4, column=0, columnspan=3)
    if flags == 'apt1':
        Button(st, width=15, text='Main Menu', bg='green', fg='white', command=main_cus).grid(row=6, column=2)
    else:
        Button(st, width=15, text='Main Menu', bg='green', fg='white', command=main_menu).grid(row=6, column=2)
    st.mainloop()


def search_med(): #untuk mencari obat pada admin dan customer untuk menampilkan harga dan ada di rak ke berapa
    global c, cur, st, sym, columns
    cur.execute("select * from med")
    y = []
    x = 0
    for i in cur:
        if i[5] == sym.get():
            y.append(
                str(i[0]) + '. ' + str(i[1]) + '  Rp. ' + str(i[4]) + '    Rack : ' + str(i[7]))
            x = x + 1
    top = Tk()
    top.geometry('200x100')
    top.configure(background='pink')
    for i in range(len(y)):
        Label(top, text=y[i], bg='pink').grid(row=i, column=0)
    Button(top, text='OK', command=top.destroy).grid(row=5, column=0)
    c.commit()
    top.mainloop()



def again(): #login page awal
    global un, pwd, flag, root, apt
    if flag == 'apt':
        apt.destroy()
    root = Tk()
    root.geometry('450x200')
    root.configure(background='yellow')
    root.title('SELAMAT DATANG')
    Label(root, text='', bg='yellow').grid(row=0, column=0, columnspan=5)
    Label(root, text="        TOKO OBAT GENESIS", bg='yellow').grid(row=1, column=0, columnspan=5)
    Label(root, text='----------------------------------------------------------------------------------------', bg='yellow').grid(row=2, column=0, columnspan=5)
    Label(root, text='Username', bg='yellow').grid(row=3, column=2)
    un = Entry(root, width=30)
    un.grid(row=3, column=3)
    Label(root, text='Password', bg='yellow').grid(row=4, column=2)
    pwd = Entry(root, width=30)
    pwd.grid(row=4, column=3)
    Label(root, text='                             ')
    Button(root, width=6, bg='blue', fg='black', text='Enter', command=check).grid(row=10, column=2, pady=10)
    Button(root, width=6, bg='red', fg='black', text='Close', command=root.destroy).grid(row=10, column=3, pady=10)
    root.mainloop()


def check(): #mengecek apakah nama user dan password sudah sesuai dengan yang ada di database
    global un, pwd, login, l, root
    u = un.get()
    p = pwd.get()
    l.execute("select * from log")
    for i in l:
        if i[0] == u and i[1] == p and u == 'admin':
            root.destroy()
            open_win()
        elif i[0] == u and i[1] == p:
            root.destroy()
            open_cus()
    login.commit()


def main_menu(): #tampilan pada main menu
    global sto, apt, flag, root, st, val, exp, st1, rev
    if flag == 'sto':
        sto.destroy()
    if flag == 'rev':
        rev.destroy()
    elif flag == 'st':
        st.destroy()
    elif flag == 'st1':
        st1.destroy()
    elif flag == 'val':
        val.destroy()
    elif flag == 'exp':
        exp.destroy()
    elif flag == 'd':
        d.destroy()
    open_win()


def main_cus():
    global st, flag, exp
    if flag == 'exp':
        exp.destroy()
    elif flag == 'st':
        st.destroy()
    open_cus()


def open_cus(): #tampilan awal customer
    global apt, flag, flags
    flags = 'apt1'
    apt = Tk()
    apt.title("Interface")
    apt.geometry('260x300')
    apt.configure(background='pink')
    Label(apt, text="*** TOKO OBAT GENESIS ***", bg='pink', fg='black').grid(row=0, column=0)
    Label(apt, text='*' * 40, bg='pink').grid(row=1, column=0)
    Label(apt, text='*  SELAMAT DATANG DI TOKO OBAT GENESIS  *', bg='pink', fg='black').grid(row=2, column=0)
    Label(apt, text='-' * 40, bg='pink').grid(row=3, column=0)

    Label(apt, text='-' * 40, bg='pink').grid(row=5, column=0)
    Button(apt, text='Search', bg='blue', fg='white', width=15, command=search).grid(row=6, column=0, pady=15)
    Button(apt, text='Expiry Check', bg='red', fg='white', width=15, command=exp_date).grid(row=7, column=0)

    Label(apt, text='-' * 40, bg='pink').grid(row=8, column=0)
    Button(apt, text='Logout', bg='green', fg='white', command=again1).grid(row=9, column=0)
    apt.mainloop()


def again1():
    global flags
    apt.destroy()
    flags = ''
    again()


again()

