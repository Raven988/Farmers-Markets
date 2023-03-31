"""
My Class View
"""
import tkinter as tk
from tkinter import ttk
import class_model as cm

rating_lst = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
my_font = [("Arial", 8, "bold", "italic"), ("Arial", 12, "italic"), ("Arial", 12, "bold", "italic")]
my_bg = ['lavender', 'lightgray', 'PaleGreen1', 'Pink']
my_text = ['Input ID Farmer Market', 'Show Reviews And Ratings', 'Leave Reviews And Ratings',
           'Input ID FM', 'Input Review', 'Select Rating', 'List Farmers Markets', 'All Cities',
           'Find by ZIP', 'Find by City and State', 'Details about FM', 'Review and Rating FM',
           'Farmers Markets App', 'Input ZIP CODE', 'Input City and State', 'Search Results']


def close_window(win_list, btn):
    """activates the buttons"""
    try:
        win_list.destroy()
        btn['state'] = 'normal'
    except tk.TclError:
        pass


class FarmersMarkets(tk.Tk):
    """main window app"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        super().__init__()
        self.database = cm.Model('server.db')
        self.title('Farmers Markets')
        self.resizable(width=False, height=False)
        self.configure(background=my_bg[3])
        self.cmd_frame = tk.Frame(width=500, height=300, bg=my_bg[3])
        self.found_frame = tk.Frame(width=570, height=400, bg=my_bg[0])
        self.found_frame.configure(highlightbackground="black", highlightthickness=1)
        self.cmd_frame.grid(row=0, column=0)
        self.found_frame.grid(row=1, column=0, pady=10, padx=10, sticky='we')

        self.lbl_title = tk.Label(self.cmd_frame, text=my_text[12], font=my_font[2], bg=my_bg[3])
        self.lbl_zip = tk.Label(self.cmd_frame, text=my_text[13], font=my_font[0], bg=my_bg[3])
        self.lbl_city = tk.Label(self.cmd_frame, text=my_text[14], font=my_font[0], bg=my_bg[3])
        self.lbl_id = tk.Label(self.cmd_frame, text=my_text[0], font=my_font[0], bg=my_bg[3])
        self.lbl_result = tk.Label(self.found_frame, text=my_text[15], font=my_font[2], bg=my_bg[0])

        self.lbl_found = tk.Label(self.found_frame, font=my_font[1], bg=my_bg[0], justify=tk.LEFT)
        self.lbl_found.place(x=10, y=50)

        self.lbl_title.grid(row=0, column=0, columnspan=3, sticky='we')
        self.lbl_zip.grid(row=2, column=1, columnspan=2, sticky='we')
        self.lbl_city.grid(row=4, column=1, columnspan=2, sticky='we')
        self.lbl_id.grid(row=6, column=1, columnspan=2, sticky='we')
        self.lbl_result.place(x=10, y=5)

        self.btn_listfm = tk.Button(self.cmd_frame, text=my_text[6], font=my_font[1], bg=my_bg[2],
                                    command=self.list_market)
        self.btn_allcity = tk.Button(self.cmd_frame, text=my_text[7], font=my_font[1], bg=my_bg[2],
                                     command=self.all_cities)
        self.btn_findzip = tk.Button(self.cmd_frame, text=my_text[8], font=my_font[1], bg=my_bg[2],
                                     command=self.find_by_zip)
        self.btn_findcity = tk.Button(self.cmd_frame, text=my_text[9], font=my_font[1], bg=my_bg[2],
                                      command=self.find_by_city)
        self.btn_dtls = tk.Button(self.cmd_frame, text=my_text[10], font=my_font[1], bg=my_bg[2],
                                  width=30, command=self.details_fm)
        self.btn_rev = tk.Button(self.cmd_frame, text=my_text[11], font=my_font[1], bg=my_bg[2],
                                 command=ReviewAndRating)

        self.btn_listfm.grid(row=1, column=0, sticky='we', ipadx=5, ipady=5, pady=5, padx=5)
        self.btn_allcity.grid(row=1, column=1, columnspan=2, sticky='we', ipadx=5, ipady=5, pady=5,
                              padx=5)
        self.btn_findzip.grid(row=3, column=0, sticky='we', ipadx=5, ipady=5, pady=5, padx=5)
        self.btn_findcity.grid(row=5, column=0, sticky='we', ipadx=5, ipady=5, pady=5, padx=5)
        self.btn_dtls.grid(row=7, column=0, sticky='we', ipadx=5, ipady=5, pady=5, padx=5)
        self.btn_rev.grid(row=9, column=0, columnspan=3, sticky='we', ipadx=5, ipady=5, pady=5,
                          padx=5)

        self.ent_zip = tk.Entry(self.cmd_frame, width=30, bg=my_bg[1], font=my_font[1],
                                justify=tk.CENTER)
        self.ent_city = tk.Entry(self.cmd_frame, width=15, bg=my_bg[1], font=my_font[1],
                                 justify=tk.CENTER)
        self.ent_state = tk.Entry(self.cmd_frame, width=15, bg=my_bg[1], font=my_font[1],
                                  justify=tk.CENTER)
        self.ent_id = tk.Entry(self.cmd_frame, width=30, bg=my_bg[1], font=my_font[1],
                               justify=tk.CENTER)

        self.ent_zip.grid(row=3, column=1, columnspan=2, sticky='we', ipadx=5, ipady=5, pady=5,
                          padx=5)
        self.ent_city.grid(row=5, column=1, sticky='we', ipadx=5, ipady=5, pady=5, padx=5)
        self.ent_state.grid(row=5, column=2, sticky='we', ipadx=5, ipady=5, pady=5, padx=5)
        self.ent_id.grid(row=7, column=1, columnspan=2, sticky='we', ipadx=5, ipady=5, pady=5,
                         padx=5)

    def list_market(self):
        """show list of markets"""
        fm_list = self.database.list_markets()
        self.btn_listfm['state'] = 'disabled'
        win_list = tk.Tk()
        win_list.title("List Farmers Markets")
        win_list.geometry("500x800")
        win_list.resizable(width=False, height=False)
        list_box = tk.Listbox(win_list, height=500, width=800, bg='PaleGreen1')
        scrollbar = tk.Scrollbar(win_list, orient="vertical", command=list_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        list_box["yscrollcommand"] = scrollbar.set
        numb = 1
        for i in fm_list:
            n_i = str(numb) + ". " + i
            list_box.insert(tk.END, n_i)
            numb += 1
        list_box.pack()
        win_list.protocol('WM_DELETE_WINDOW', lambda: close_window(win_list, self.btn_listfm))

    def all_cities(self):
        """show all cities"""
        cities_list = self.database.all_cities()
        self.btn_allcity['state'] = 'disabled'
        win_list = tk.Tk()
        win_list.title("List All Cities")
        win_list.geometry("200x800")
        win_list.resizable(width=False, height=False)
        list_box = tk.Listbox(win_list, height=200, width=800, bg='PaleGreen1')
        scrollbar = tk.Scrollbar(win_list, orient="vertical", command=list_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        list_box["yscrollcommand"] = scrollbar.set
        for i in cities_list:
            list_box.insert(tk.END, i)
        list_box.pack()
        win_list.protocol('WM_DELETE_WINDOW', lambda: close_window(win_list, self.btn_allcity))

    def find_by_zip(self):
        """find markets by ZIP CODE"""
        self.lbl_found['text'] = ''
        all_zip_tpl = self.database.all_zip()
        all_zip = []
        for zip_fm in all_zip_tpl:
            all_zip.append(str(zip_fm[0]))
        zip_code = self.ent_zip.get()
        if zip_code in all_zip and len(zip_code) > 0:
            value = self.database.find_by_zip(zip_code)
            self.ent_zip['bg'] = 'lightgray'
            in_lbl = ''
            for name_fm in value:
                in_lbl += name_fm[1] + ' - ' + name_fm[0] + '\n'
            self.lbl_found['text'] = in_lbl
            self.lbl_found['wraplength'] = 550
            self.lbl_found.place(x=10, y=50)
        else:
            self.ent_zip['bg'] = 'red'
            self.lbl_found['text'] = 'ZIP CODE not found\n\n\nPlease, try again'
            self.lbl_found['wraplength'] = 550
            self.lbl_found.place(x=10, y=50)

    def find_by_city(self):
        """find markets by ZIP CODE"""
        self.lbl_found['text'] = ''
        city = self.ent_city.get()
        state = self.ent_state.get()
        cities_in_db = self.database.all_cities()
        states_in_db = self.database.all_state()
        if city and state:
            if city.capitalize() in cities_in_db and state.capitalize() in states_in_db:
                value = self.database.find_by_city(city.capitalize(), state.capitalize())
                self.ent_city['bg'] = 'lightgray'
                self.ent_state['bg'] = 'lightgray'
                founds_fm = ''
                for market in value:
                    founds_fm += market[0] + '\n'
                if city:
                    if value:
                        self.lbl_found['text'] = founds_fm
                        self.lbl_found['wraplength'] = 550
                        self.lbl_found.place(x=10, y=50)
            elif city.capitalize() not in cities_in_db:
                self.ent_city['bg'] = 'red'
                self.lbl_found['text'] = 'There is no such city in the database'
                self.lbl_found['wraplength'] = 550
                self.lbl_found.place(x=10, y=50)
            elif state.capitalize() not in states_in_db:
                self.ent_state['bg'] = 'red'
                self.lbl_found['text'] = 'There is no such state in the database'
                self.lbl_found['wraplength'] = 550
                self.lbl_found.place(x=10, y=50)
        else:
            self.ent_city['bg'] = 'red'
            self.ent_state['bg'] = 'red'
            self.lbl_found['text'] = 'Input City and State'
            self.lbl_found['wraplength'] = 550
            self.lbl_found.place(x=10, y=50)

    def details_fm(self):
        """show details about markets"""
        self.lbl_found['text'] = ''
        all_id_tpl = self.database.all_id()
        all_id = []
        for id_fm in all_id_tpl:
            all_id.append(id_fm[0])
        market = self.ent_id.get()
        if str(market) in all_id:
            show = ''
            if market:
                details = self.database.detailed_data(market.strip())
                self.ent_id['bg'] = 'lightgray'
                show += f'- Market Name: {details[0][17]}\n'
                show += f'- Street of market: {details[0][0]}\n'
                show += f'- City: {details[0][8]}\n'
                show += f'- County: {details[0][10]}\n'
                show += f'- State: {details[0][9]}\n'
                show += f'- ZIP CODE: {details[0][4]}\n'
                show += '- Media:\n'
                for i in details[0][11:16]:
                    if len(i) > 0:
                        show += i + '\n'
                show += f'- coordinates Y: {details[0][5]},  X: {details[0][6]}'
            if market:
                self.lbl_found['text'] = show
                self.lbl_found['wraplength'] = 550
                self.lbl_found.place(x=10, y=50)
        else:
            self.ent_id['bg'] = 'red'
            self.lbl_found['text'] = 'ID not found\n\nEnter the correct market ID\n\n' \
                                     'You can see all the IDs by clicking' \
                                     'on the button \'List Farmers Markets\''
            self.lbl_found['wraplength'] = 550
            self.lbl_found.place(x=10, y=50)


class ReviewAndRating:
    """window review and rating"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.database = cm.Model('server.db')
        farmers_m.btn_rev['state'] = 'disabled'
        self.win = tk.Tk()
        self.win.title('Review and Rating')
        self.win.resizable(width=False, height=False)
        self.win.configure(background=my_bg[2])
        self.main_lbl = tk.Label(self.win, text=my_text[0], font=my_font[0], bg=my_bg[2])
        self.bt_show = tk.Button(self.win, text=my_text[1], font=my_font[1], bg=my_bg[0])
        self.ent_id = tk.Entry(self.win, font=my_font[1], width=35, bg=my_bg[1])
        self.txt_show = tk.Text(self.win, height=10, bg=my_bg[0], state='disabled')
        self.bt_leave_rv = tk.Button(self.win, text=my_text[2], font=my_font[1], bg=my_bg[0])
        self.lbl_id = tk.Label(self.win, text=my_text[3], font=my_font[0], bg=my_bg[2])
        self.lbl_rv = tk.Label(self.win, text=my_text[4], font=my_font[0], bg=my_bg[2])
        self.lbl_rt = tk.Label(self.win, text=my_text[5], font=my_font[0], bg=my_bg[2])
        self.ent_id_in = tk.Entry(self.win, font=my_font[1], width=10, bg=my_bg[1])
        self.txt_rv = tk.Text(self.win, font=my_font[0], height=10, bg=my_bg[1])
        self.cmbox = ttk.Combobox(self.win, values=rating_lst, state='readonly', width=3,
                                  font=my_font[1])

        self.main_lbl.grid(row=0, column=2, columnspan=2, sticky='we')
        self.bt_show.grid(row=1, column=0, columnspan=2, sticky='we', padx=5, pady=5)
        self.ent_id.grid(row=1, column=2, columnspan=2, sticky='ns', padx=5, pady=5)
        self.txt_show.grid(row=2, column=0, columnspan=4, sticky='we', padx=5, pady=5)
        self.bt_leave_rv.grid(row=3, column=0, columnspan=4, sticky='we', padx=5, pady=5)
        self.lbl_id.grid(row=4, column=0, sticky='we', padx=5, pady=5)
        self.lbl_rv.grid(row=4, column=1, columnspan=2, sticky='we', padx=5, pady=5)
        self.lbl_rt.grid(row=4, column=3, sticky='we', padx=5, pady=5)
        self.ent_id_in.grid(row=5, column=0, sticky='n', padx=5, pady=5)
        self.txt_rv.grid(row=5, column=1, columnspan=2, sticky='we', padx=5, pady=5)
        self.cmbox.grid(row=5, column=3, sticky='n', padx=5, pady=5)

        self.bt_show.configure(command=self.show_rev_and_rat)
        self.bt_leave_rv.configure(command=self.leave_rev_and_rat)

        self.win.protocol('WM_DELETE_WINDOW', lambda: close_window(self.win, farmers_m.btn_rev))

    def show_rev_and_rat(self):
        """showing found reviews and ratings"""
        get_id = self.ent_id.get()
        all_id = self.database.all_id()
        id_list = []
        for id_fm in all_id:
            id_list.append(id_fm[0])
        if get_id in id_list:
            datas = self.database.comm_market(get_id)
            rating = self.database.rating_market(get_id)
            self.ent_id['bg'] = 'lightgray'
            self.txt_show.configure(state='normal')
            in_table = f'average rating: {rating[0][0]}\n\n'
            for i in datas:
                in_table += '- ' + i[0] + '\n\n'
            self.txt_show.replace('1.0', tk.END, in_table)
            self.txt_show.configure(state='disabled')
        else:
            self.ent_id['bg'] = 'red'
            self.txt_show.configure(state='normal')
            self.txt_show.replace('1.0', tk.END, 'Error! There is no such id in the database')
            self.txt_show.configure(state='disabled')

    def leave_rev_and_rat(self):
        """add in DB reviews and ratings"""
        get_id = self.ent_id_in.get()
        get_review = self.txt_rv.get("1.0", tk.END)
        get_rating = self.cmbox.get()
        if get_rating and get_review:
            all_id = self.database.all_id()
            list_id = []
            for idfm in all_id:
                list_id.append(idfm[0])
            if get_id in list_id:
                self.database.comments(get_review, get_id)
                self.database.rating(get_rating, get_id)
                self.ent_id_in['bg'] = 'lightgray'
                self.txt_show.configure(state='normal')
                self.txt_show.replace('1.0', tk.END, 'Your review is added.')
                self.txt_show.configure(state='disabled')
                self.txt_rv.delete("1.0", tk.END)
                self.ent_id_in.delete(0, tk.END)
            else:
                self.ent_id_in['bg'] = 'red'
                self.txt_show.configure(state='normal')
                self.txt_show.replace('1.0', tk.END, 'Error! There is no such id in the database')
                self.txt_show.configure(state='disabled')

        else:
            self.txt_show.configure(state='normal')
            self.txt_show.replace('1.0', tk.END, 'Input your reviews and rating, please.')
            self.txt_show.configure(state='disabled')


if __name__ == '__main__':
    farmers_m = FarmersMarkets()
    farmers_m.mainloop()
