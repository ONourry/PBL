import tkinter as tk
from PIL import ImageTk, Image
from PBL.Controller import orderItemController
from PBL.Model import item

class ItemComponent(tk.Frame):

    def __init__(self, parent, item):
        tk.LabelFrame.__init__(self, parent)
        self.parent = parent
        self.item = item
        self.grid()
        #frame for checkbox, image
        self.pic_frame = tk.Frame(self)#, background="light green")
        self.pic_frame.grid(row=0, column=0, sticky="nsew")
        #frame for name, weight, button
        self.info_frame = tk.Frame(self)#, background="pink")
        self.info_frame.grid(row=0, column=1, sticky="nsew")

        self.status = 0
        #self.status.set(0)
        self.status_control = tk.Radiobutton(self.pic_frame, variable = self.status, value=0, command=self.activeItem)
        self.status_control.grid(row=0, column=0, padx=15)

        self.canvas_width = 100
        self.canvas_height= 100
        self.pic_canvas = tk.Canvas(self.pic_frame, width=self.canvas_width, height=self.canvas_height, background="white")
        self.pic_canvas.grid(row=0, column=1, padx=15, pady=10)

        self.image = self.process_image(self.item.imgPath, 102)
        self.image = ImageTk.PhotoImage(self.image)
        self.pic_canvas.create_image(0,0, anchor="nw", image=self.image)

        self.testlabel = tk.Label(self.pic_canvas)
        self.testlabel.image = self.image
        self.testlabel.configure(image=self.image)
        #self.testlabel.grid(row=1,column=1,padx=15,pady=10)
        #
        self.itemName_label = tk.StringVar()
        self.itemName_label.set(self.item.name)
        self.name_label = tk.Label(self.info_frame, textvariable=self.itemName_label, width=10, fg="#008080",anchor="sw", font=("Arial",15))
        self.name_label.grid(row=0, padx=20, pady=8, sticky="w")
        #
        self.progressBar = tk.Canvas(self.info_frame, width=150, height=20, background="light grey")
        self.progressBar.grid(row=1, padx=15, pady=4, sticky="nsew")

        self.current_weight = 100
        self.progressBar.create_rectangle(0,0,self.current_weight,25, fill="#00C5CD")

        self.order_button = tk.Button(self.info_frame, text="Order", width=12, height=2, command=self.orderItem, font=("Arial",12))
        self.order_button.grid(row=2, padx=15, pady=8)

    def orderItem(self): #order Button
        self.orderController = orderItemController.OrderItemController()
        self.orderController.orderItem(self.item)
        self.orderController.closeDriver()

    def activeItem(self):
        #self.status.set(self.status_control['value'])
        #print(self.status_control['value'])
        #print(self.status)
        pass


    def process_image(self, path, target_size):
        image = self.load_image(path)
        image = self.resize_image(image, target_size)
        image = self.paste_image(image, target_size)
        return image

    def load_image(self, path):
        return Image.open(path)

    def resize_image(self, image, target_size):
        w, h = image.size
        assert (target_size<=w and target_size<=h), "target_size must smaller than height and width"
        target_size = int(target_size)
        if w<h:
            ratio = h/target_size
            new_w = int(w/ratio)
            out = image.resize((new_w, target_size))
        else:
            ratio = w/target_size
            new_h = int(h/ratio)
            out = image.resize((target_size, new_h))
        return out

    def paste_image(self, image, target_size):
        new_image = Image.new(image.mode, (target_size, target_size), "white")
        w, h = image.size
        left = int(target_size/2 - w/2)
        right = int(target_size/2 + w/2)
        upper = int(target_size/2 - h/2)
        lower = int(target_size/2 + h/2)
        box = (left, upper, right, lower)
        new_image.paste(image, box)
        return new_image
