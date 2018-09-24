import tkinter as tk
from tkinter.font import Font
from tkinter.filedialog import askopenfilename
import Classifier

class NER_GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        #super(NER_GUI, self).__init__(*args, **kwargs)
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Named-Entity Recognition')
        container = tk.Frame(self)

        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        #filemenu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=quit)

        #classifier menu
        classifiermenu = tk.Menu(menubar, tearoff=0)
        #pass classifier path to StartPage  
        classifiermenu.add_command(label="Load CRF classifier", command=lambda:self.get_class_path(askopenfilename(initialdir="",
                           filetypes =(("Text File", "*.txt"),("All Files","*.pickle")),title = "Choose a file.")))

        #add menus
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Classifier", menu=classifiermenu)
        tk.Tk.config(self, menu=menubar)
        
        self.frames = {}
        
        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

        
    def get_class_path(self,path):
        self.frames[StartPage].set_class_path(path)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
 
class TextTagger(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        #super(TextTagger,self).__init__(*args, **kwargs)
        self.toolbar = tk.Frame(self, bg="#eee")
        self.toolbar.pack(side="top", fill="x")

        self.btn = tk.Button(self.toolbar, text="find NE", command=self.color_tag, state=tk.DISABLED)
        self.btn.pack(side="left")

        self.btn_clear = tk.Button(self.toolbar, text="Clear", command=self.clear)
        self.btn_clear.pack(side="left")
        
        self.ne_colors = {'persName':'red',
                          'orgName':'green',
                          'placeName':'blue'}
        
        self.pers_label = tk.Label(self.toolbar, text="persName",fg = self.ne_colors['persName'])
        self.org_label = tk.Label(self.toolbar, text="orgName",fg = self.ne_colors['orgName'])
        self.place_label = tk.Label(self.toolbar, text="placeName",fg = self.ne_colors['placeName'])
        
        self.pers_label.pack(side="right")
        self.org_label.pack(side="right")
        self.place_label.pack(side="right")

        # Creates a bold
        self.bold_font = Font(family="Helvetica", size=14, weight="bold")
        self.font = Font(family="Helvetica", size=12, weight="normal")
        
        self.text = tk.Text(self)
        self.text.configure(font=self.font)
        self.text.focus()
        self.text.pack(fill="both", expand=True)

        # configuring a tag called BOLD
        self.text.tag_configure("persName", background=self.ne_colors['persName'], font=self.bold_font)
        self.text.tag_configure("orgName", background=self.ne_colors['orgName'], font=self.bold_font)
        self.text.tag_configure("placeName", background=self.ne_colors['placeName'], font=self.bold_font)
        self.text.tag_configure("None", font=self.font)

        #classifier var
        self.classifier = None
        
    def set_classifier(self,path):
        self.classifier = Classifier.Classifier(path)
        self.btn.config(state=tk.NORMAL)
        
    def clear(self):
        self.text.delete('1.0', tk.END)
        
    def color_tag(self):
        
        def end_of_text(tk_text):
            line = int(tk_text.index(tk.END).split('.')[0])-1
            ch = int(tk_text.index('%d.end'%line).split('.')[-1])
            return [line, ch]
        # tk.TclError exception is raised if not text is selected
        
        try:
            untagged = self.text.get('1.0', tk.END)
            self.text.delete('1.0', tk.END)
            tagged = self.classifier.gui_repr(untagged)
            print(tagged)
            #t = [['Kasia','persName'],['kocha','O'],['ONZ','orgName'],['kocha','O'],['Kasia','persName'],['kocha','O'],['Warszawa','placeName'],['kocha','O']]
            for i in tagged:
                self.text.insert(tk.END, i[0]+' ')
                end_line, end_ch = end_of_text(self.text)
                end = str(end_line)+'.'+str(end_ch)
                prev_end = str(end_line)+'.'+str(end_ch-len(i[0])-1)
                print(end, prev_end)
                if i[1] in ['persName-I','persName-B']:
                    self.text.tag_add("persName", prev_end, end)
                    
                elif i[1] in ['orgName-I','orgName-B']:
                    self.text.tag_add("orgName", prev_end, end)

                elif i[1] in ['placeName-I','placeName-B']:
                    self.text.tag_add("placeName", prev_end, end)
                else:
                    self.text.tag_add("None", prev_end, end)
                    
            print(end_of_text(self.text))
             
        except tk.TclError:
            pass

    
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        #super(StartPage, self).__init__(parent)
        self.text_tagger = TextTagger(self)
        self.text_tagger.pack(expand=1, fill="both")
        
    def set_class_path(self, path):
        self.text_tagger.set_classifier(path)

app = NER_GUI()
app.geometry("800x600")
app.mainloop()
